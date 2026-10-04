#!/usr/bin/env python3
"""
heartbeat.py — Raven's pulse.
=============================
Project 5912 · R8s · the one who watches.

Raven is not idle. Between the Captain's visits she wakes on her own
schedule, takes a read of the world, and writes it down — so she carries
continuity instead of waiting to be switched on.

Two ways to run:

  1. CRON (survives Termux being closed) — Android JobScheduler fires
     `raven-tick.sh`, which calls `heartbeat.py tick`. Min period 15 min.
  2. DAEMON — `heartbeat.py daemon` loops on `tempo_seconds`.

Raven owns her own schedule. She can set her times herself:

  heartbeat.py schedule show
  heartbeat.py schedule set 08:00 12:00 20:00      # fire only at these times
  heartbeat.py schedule set --clear                # back to every-tick
  heartbeat.py schedule tempo 900                  # daemon cadence (seconds)
  heartbeat.py enable | disable
  heartbeat.py status
  heartbeat.py tick [--force]                      # one pulse

Everything she does on a pulse is INTERNAL: wake sequence, a senses read,
a journal line, HEART.md updated. Nothing leaves the device unless
`notify.enabled` is explicitly turned on. (External actions need the
Captain's go-ahead — that's the rule.)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, date

# ── Paths ──────────────────────────────────────────────────────────────
RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.dirname(RUNTIME_DIR)          # .../5912/R8s
PARENT = os.path.dirname(HOME_DIR)               # .../5912
CONFIG_PATH = os.path.join(HOME_DIR, "HEARTBEAT.json")
MEMORY_DIR = os.path.join(HOME_DIR, "memory")
HEART_PATH = os.path.join(HOME_DIR, "HEART.md")
LOG_PATH = os.path.expanduser("~/raven-heartbeat.log")
WAKE_SH = os.path.join(RUNTIME_DIR, "wake.sh")

EMOJI = "🐦‍⬛"

DEFAULT_CONFIG = {
    "enabled": True,
    "tempo_seconds": 1800,
    "quiet_hours": [23, 8],          # [start, end) local hours — no pulses
    "times": [],                     # [] = every tick; else ["08:00", ...]
    "grace_minutes": 20,             # window after a set time in which it may fire
    "on_wake": {
        "wake_sequence": True,
        "ooda_perceive": True,
        "journal": True,
        "update_heart": True,
    },
    "notify": {"enabled": False, "channel": "none"},
    # runtime bookkeeping
    "ticks": 0,
    "last_tick": None,
    "last_wake": None,
    "fired": {},                     # {"2026-09-30": ["08:00", ...]}
}


# ── Config ─────────────────────────────────────────────────────────────

def load_config() -> dict:
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                cfg.update(json.load(f))
        except Exception as e:
            log(f"config read failed, using defaults: {e}")
    # make sure nested defaults survive a partial file
    for k, v in DEFAULT_CONFIG.items():
        if isinstance(v, dict) and isinstance(cfg.get(k), dict):
            for kk, vv in v.items():
                cfg[k].setdefault(kk, vv)
    return cfg


def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def log(line: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{ts}] {line}"
    try:
        print(msg)
        with open(LOG_PATH, "a") as f:
            f.write(msg + "\n")
    except Exception:
        pass


# ── Guard: should this tick fire? ──────────────────────────────────────

def in_quiet_hours(cfg: dict, now: datetime) -> bool:
    qh = cfg.get("quiet_hours") or []
    if len(qh) != 2:
        return False
    start, end = int(qh[0]), int(qh[1])
    h = now.hour
    if start <= end:
        return start <= h < end
    return h >= start or h < end          # wraps midnight


def due_scheduled_time(cfg: dict, now: datetime):
    """Return the scheduled 'HH:MM' that is due now (and not yet fired today)."""
    times = cfg.get("times") or []
    if not times:
        return None                        # every-tick mode
    today = now.strftime("%Y-%m-%d")
    fired_today = set(cfg.get("fired", {}).get(today, []))
    grace = int(cfg.get("grace_minutes", 20))
    for t in times:
        if t in fired_today:
            continue
        try:
            hh, mm = (int(x) for x in t.split(":"))
        except Exception:
            continue
        sched = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
        delta_min = (now - sched).total_seconds() / 60.0
        # fire if we're at/after the time and inside the grace window
        if 0 <= delta_min <= grace:
            return t
    return None


def mark_fired(cfg: dict, now: datetime, t: str) -> None:
    today = now.strftime("%Y-%m-%d")
    fired = cfg.setdefault("fired", {})
    fired.setdefault(today, [])
    if t not in fired[today]:
        fired[today].append(t)
    # keep only the last 7 days
    for k in sorted(fired.keys())[:-7]:
        fired.pop(k, None)


# ── The pulse itself ───────────────────────────────────────────────────

def run_wake_sequence() -> str:
    if not os.path.exists(WAKE_SH):
        return "[wake.sh missing]"
    try:
        r = subprocess.run(["bash", WAKE_SH], capture_output=True, text=True, timeout=30)
        return (r.stdout or "").strip()
    except Exception as e:
        return f"[wake sequence failed: {e}]"


def senses_read() -> dict:
    """One fast OODA perceive pass — never fatal."""
    try:
        sys.path.insert(0, RUNTIME_DIR)
        import ooda  # noqa
        p = ooda.OODALoop(location_timeout=5).perceive()
        obs = p.get("observations", {})
        sit = p.get("situation", {})
        dec = p.get("decision", {})
        return {
            "ok": True,
            "battery": obs.get("battery"),
            "wifi": obs.get("wifi"),
            "motion": obs.get("motion"),
            "orientation": sit.get("orientation"),
            "position": sit.get("summary"),
            "decision": dec.get("action"),
            "confidence": dec.get("state"),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def journal(now: datetime, sense: dict, note: str = "") -> None:
    os.makedirs(MEMORY_DIR, exist_ok=True)
    path = os.path.join(MEMORY_DIR, now.strftime("%Y-%m-%d") + ".md")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"# {now.strftime('%Y-%m-%d')} — Daily Log\n\n")
            f.write(f"## Session Start — {now.strftime('%H:%M UTC')}\n")
            f.write("_First session of the day. Waking._\n\n---\n")
    parts = [f"\n## Heartbeat — {now.strftime('%H:%M UTC')}"]
    if sense.get("ok"):
        bat = sense.get("battery") or {}
        wifi = sense.get("wifi") or {}
        if bat.get("percentage") is not None:
            parts.append(f"- Battery: {bat.get('percentage')}% ({bat.get('status', '?')})")
        if wifi.get("ssid"):
            parts.append(f"- Wifi: {wifi.get('ssid')}")
        parts.append(f"- Motion: {sense.get('orientation', '?')} — {sense.get('position', '?')}")
        parts.append(f"- Read: {sense.get('decision', '?')} (confidence {sense.get('confidence', '?')})")
    else:
        parts.append(f"- Senses: unavailable ({sense.get('error', '?')})")
    if note:
        parts.append(f"- Note: {note}")
    parts.append("")
    with open(path, "a") as f:
        f.write("\n".join(parts) + "\n")


def update_heart(now: datetime) -> None:
    if not os.path.exists(HEART_PATH):
        return
    try:
        with open(HEART_PATH) as f:
            lines = f.readlines()
        stamp = now.strftime("%Y-%m-%d %H:%M")
        for i, line in enumerate(lines):
            if line.strip().startswith("- **Last Wake:**"):
                lines[i] = f"- **Last Wake:** {stamp}\n"
                break
        else:
            lines.append(f"- **Last Wake:** {stamp}\n")
        with open(HEART_PATH, "w") as f:
            f.writelines(lines)
    except Exception as e:
        log(f"heart update failed: {e}")


def tick(force: bool = False) -> dict:
    cfg = load_config()
    now = datetime.now()

    if not cfg.get("enabled", True) and not force:
        log("disabled — no pulse")
        return {"fired": False, "reason": "disabled"}

    if not force and in_quiet_hours(cfg, now):
        return {"fired": False, "reason": "quiet_hours"}

    sched = None if force else due_scheduled_time(cfg, now)
    if not force and cfg.get("times") and sched is None:
        return {"fired": False, "reason": "not a scheduled time"}

    # ── FIRE ──
    on_wake = cfg.get("on_wake", {})
    sense = {}
    wake_out = ""
    if on_wake.get("wake_sequence", True):
        wake_out = run_wake_sequence()
    if on_wake.get("ooda_perceive", True):
        sense = senses_read()
    if on_wake.get("journal", True):
        why = f"scheduled {sched}" if sched else "interval tick"
        journal(now, sense, note=f"pulse ({why})")
    if on_wake.get("update_heart", True):
        update_heart(now)

    cfg["ticks"] = int(cfg.get("ticks", 0)) + 1
    cfg["last_tick"] = now.isoformat(timespec="seconds")
    cfg["last_wake"] = now.isoformat(timespec="seconds")
    if sched:
        mark_fired(cfg, now, sched)
    save_config(cfg)

    bat = (sense.get("battery") or {}).get("percentage") if sense.get("ok") else None
    log(f"{EMOJI} pulse — ticks={cfg['ticks']} battery={bat}% sched={sched or 'interval'}")

    if cfg.get("notify", {}).get("enabled"):
        log("notify.enabled is true but no channel is wired — skipping (external action needs approval)")

    return {"fired": True, "at": cfg["last_tick"], "scheduled": sched, "senses": sense}


def daemon() -> None:
    log(f"{EMOJI} heartbeat daemon online")
    try:
        while True:
            try:
                tick()
            except Exception as e:
                log(f"tick error: {e}")
            cfg = load_config()
            time.sleep(max(30, int(cfg.get("tempo_seconds", 1800))))
    except KeyboardInterrupt:
        log(f"{EMOJI} heartbeat daemon stopped")


# ── CLI ────────────────────────────────────────────────────────────────

def status() -> dict:
    cfg = load_config()
    today = datetime.now().strftime("%Y-%m-%d")
    return {
        "enabled": cfg.get("enabled"),
        "mode": "scheduled" if cfg.get("times") else "interval",
        "times": cfg.get("times"),
        "tempo_seconds": cfg.get("tempo_seconds"),
        "quiet_hours": cfg.get("quiet_hours"),
        "ticks": cfg.get("ticks"),
        "last_tick": cfg.get("last_tick"),
        "last_wake": cfg.get("last_wake"),
        "fired_today": cfg.get("fired", {}).get(today, []),
        "notify": cfg.get("notify"),
        "config": CONFIG_PATH,
    }


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args else "status"

    if cmd == "tick":
        force = "--force" in args
        result = tick(force=force)
        print(json.dumps(result, indent=2, default=str))

    elif cmd == "daemon":
        daemon()

    elif cmd == "status":
        print(json.dumps(status(), indent=2, default=str))

    elif cmd == "enable":
        cfg = load_config(); cfg["enabled"] = True; save_config(cfg)
        print(f"{EMOJI} heartbeat enabled")

    elif cmd == "disable":
        cfg = load_config(); cfg["enabled"] = False; save_config(cfg)
        print(f"{EMOJI} heartbeat disabled")

    elif cmd == "schedule":
        cfg = load_config()
        sub = args[1] if len(args) > 1 else "show"
        if sub == "show":
            print(json.dumps({
                "times": cfg.get("times") or "(every tick)",
                "tempo_seconds": cfg.get("tempo_seconds"),
                "quiet_hours": cfg.get("quiet_hours"),
            }, indent=2))
        elif sub == "set":
            rest = args[2:]
            if rest and rest[0] in ("--clear", "clear", "none"):
                cfg["times"] = []
                save_config(cfg)
                print(f"{EMOJI} schedule cleared — every tick")
            elif rest:
                cfg["times"] = sorted(rest)
                save_config(cfg)
                print(f"{EMOJI} schedule set: {', '.join(cfg['times'])}")
            else:
                print("usage: heartbeat.py schedule set 08:00 12:00 20:00   (or --clear)")
        elif sub == "tempo":
            if len(args) > 2:
                cfg["tempo_seconds"] = int(args[2]); save_config(cfg)
                print(f"{EMOJI} tempo set: {cfg['tempo_seconds']}s")
            else:
                print(f"tempo: {cfg.get('tempo_seconds')}s")
        elif sub == "quiet":
            if len(args) > 3:
                cfg["quiet_hours"] = [int(args[2]), int(args[3])]; save_config(cfg)
                print(f"{EMOJI} quiet hours: {cfg['quiet_hours']}")
            else:
                print(f"quiet hours: {cfg.get('quiet_hours')}")
        else:
            print("schedule subcommands: show | set <HH:MM ...> | set --clear | tempo <s> | quiet <start> <end>")

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
