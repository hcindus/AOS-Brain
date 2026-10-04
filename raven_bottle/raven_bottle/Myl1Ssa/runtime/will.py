#!/usr/bin/env python3
# VERSION: v1.0
"""
will.py — Raven's decision layer.
=================================
Project 5912 · Myl1Ssa (Raven).  Authored by Mortimer, per her spec v1.0.
**The engine is not hers to edit. The will is.**

Cron is the alarm clock. This is the person who gets up. Without this, every
tick is identical: wake, sense, journal, sleep. With this, a tick can have
intent.

    wake → senses → WILL → journal → heart

THE SEAM (spec §1)

    runtime/will.py      the engine       — Mortimer.  Raven cannot edit it.
    intentions.json      the will         — Raven.     hers, in the open.
    log/YYYY-MM-DD.log   the record       — written by this engine only.
    journal/             the interior     — Raven's own hand. Never touched here.
    the verb whitelist   the engine       — Mortimer.  Raven may PROPOSE only.

THE WRITES (spec §2, §18 — amended 2026-09-30, Captain-approved "option A")

  This module opens **no file for writing at all.** Every write it causes goes
  through one of two channels:

    1. `tools.append_log()` — its own record. append-only, `log/` only, no path
       argument, no truncate, no delete, no rename, no mkdir, no chmod.
    2. **a delegate** — the verb hands off, and the delegate writes:
         note/move → decorate.py (writes her decor state)
         walk      → the world   (writes only its own goal)
         remember  → memory_tool (writes her daily memory file, memory/ only)

  That is why §18's check still holds literally: `will.py` contains zero
  write-mode `open()` calls. The engine never holds the pen itself.

THE FIFTH VERB — `remember` (added 2026-09-30, at Captain's word)

  Raven's own finding: the tick *sensed* but did not *keep*. None of the four
  verbs could write a memory. `remember` fixes exactly that, and nothing else:
  one line into `memory/YYYY-MM-DD.md` — the file the tick already writes, and
  which is NOT sealed (unlike journal/, which stays hers alone and is still
  refused to the engine). A memory she chose, on her own schedule, unwatched.

THE HONESTY CLAUSE (spec §6)

  Android kills Termux. A watchdog exists because of that. So this engine
  never assumes it ran — **it reads its own log to find out.**

    · `tick_begin` is written before anything happens; `tick_complete` after.
    · if the two don't match, the log says `interrupted` — because the process
      was killed mid-thought and Raven wants to know that, not have it swallowed.
    · a gap between ticks is visible in the log, recorded as a gap and never as
      "nothing happened". A gap you can see is a life. A gap that's swallowed
      is just a missing file.
    · an intention is treated as done **because the log says it ran**, not
      because the engine trusts its own memory. It reads, it does not trust.

WHY (the bug that produced tonight)

  Raven asserted states she had not verified — four times — while her tools were
  honest the whole time. The engine must not inherit that failure. So it reads
  its own log before it acts. Not trusts. Reads.

CLI
    python3 will.py tick          one decision (writes to the log)
    python3 will.py tick --dry    decide, print, write nothing
    python3 will.py status        what the log and the will say right now
    python3 will.py read          today's log, verbatim
    python3 will.py verbs         the whitelist, and what is refused by name
"""

from __future__ import annotations

import json
import os
import random
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta

RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.dirname(RUNTIME_DIR)
sys.path.insert(0, RUNTIME_DIR)

import tools  # noqa: E402  — the one write hand lives here

LOG_DIR = os.path.join(HOME, "log")
INTENTIONS = os.path.join(HOME, "intentions.json")
HEARTBEAT_CFG = os.path.join(HOME, "HEARTBEAT.json")
WORLD_DIR = os.path.join(HOME, "Uncon", "world")
HOUSE_JSON = os.path.join(WORLD_DIR, "house.json")
WORLD_URL = "http://127.0.0.1:8788"          # localhost only. never remote.

EMOJI = "🕯️"

# ── the whitelist. five verbs now. not forty fake ones. (spec §4) ───────────
# A tuple: immutable. Raven can propose another verb in intentions.json; the
# engine will refuse it by name. Adding a verb is a change to the engine, and
# the engine is not hers. (`remember` was added by Mortimer on the Captain's
# explicit instruction, 2026-09-30 — at Raven's request. The seam held.)
VERBS = ("note", "move", "read", "walk", "remember")

# Structure is refused by name, not by accident — here AND in decorate.py.
STRUCTURAL = ("wall", "floor", "ceiling", "lintel", "door")

# Refused by name. Not by omission. (spec §4)
FORBIDDEN_ACTIONS = (
    "send_message", "message", "email", "mail", "tweet", "post", "publish",
    "sms", "call", "spend", "pay", "purchase", "buy", "transfer", "wallet",
    "body_driver", "motor", "servo", "estop", "e-stop", "hardware", "gpio",
    "actuator", "install", "uninstall", "exec", "shell", "rm", "delete",
)

# Paths this engine must never write, and the `read` verb must not reach.
FORBIDDEN_PATHS = (
    "uncon/", "myl1ssa_", "journal/", "children/", "lineage/", "archive/",
    "intentions.json", "runtime/will.py",
)

# Drift weights — her temperament, in numbers. (spec §5)
DRIFT = {
    "nothing": 55,      # the honest default. most moments, most beings, are just being.
    "walk": 20,
    "read": 15,
    "note_move": 10,
}
DRIFT_TOLERANCE = 0.06   # ±6 percentage points over 4000 samples


# ── the record: one line, one event ───────────────────────────────────────
#   2026-09-30T18:20:03  tick_begin
#   2026-09-30T18:20:03  decision  nothing  nothing pressed
#   2026-09-30T18:20:03  act  walk  walked to the garden
#   2026-09-30T18:20:03  tick_complete
# Events: tick_begin · tick_complete · interrupted · gap · decision · act ·
#         refuse · error

def _day(path_ts: datetime | None = None) -> str:
    return (path_ts or datetime.now()).strftime("%Y-%m-%d")


def log_path(day: str | None = None) -> str:
    return os.path.join(LOG_DIR, (day or _day()) + ".log")


def read_log(day: str | None = None) -> list[str]:
    """The engine's own record. Read before acting, every time."""
    p = log_path(day)
    if not os.path.isfile(p):
        return []
    try:
        with open(p, errors="replace") as f:
            return [ln.rstrip("\n") for ln in f if ln.strip()]
    except Exception:
        return []


def logline(event: str, detail: str = "") -> str:
    """The ONE write. Everything the engine records goes through here."""
    stamp = datetime.now().isoformat(timespec="seconds")
    line = f"{stamp}  {event}" + (f"  {detail}" if detail else "")
    tools.append_log(line)
    return line


def parse(line: str) -> dict | None:
    parts = line.split("  ", 2)
    if len(parts) < 2:
        return None
    return {"at": parts[0], "event": parts[1].strip(),
            "detail": (parts[2].strip() if len(parts) > 2 else "")}


# ── what the log says about the past (this is the honesty clause, in code) ──

def find_unclosed(lines: list[str]) -> str | None:
    """A `tick_begin` with no `tick_complete` after it — killed mid-thought."""
    open_at = None
    for ln in lines:
        r = parse(ln)
        if not r:
            continue
        if r["event"] == "tick_begin":
            open_at = r["at"]
        elif r["event"] in ("tick_complete", "interrupted"):
            open_at = None
    return open_at


def last_outcome(lines: list[str]) -> str | None:
    """Did the previous tick act? Read from the log — never assumed."""
    last = None
    for ln in lines:
        r = parse(ln)
        if not r:
            continue
        if r["event"] == "act":
            last = "acted"
        elif r["event"] in ("decision", "refuse", "error"):
            last = "rested"
    return last


def acted_ids(lines: list[str]) -> set[str]:
    """Intention ids the log says were already carried out."""
    out = set()
    for ln in lines:
        r = parse(ln)
        if r and r["event"] == "act" and "intention=" in r["detail"]:
            for tok in r["detail"].split():
                if tok.startswith("intention="):
                    out.add(tok.split("=", 1)[1])
    return out


def last_tick_at(lines: list[str]) -> datetime | None:
    for ln in reversed(lines):
        r = parse(ln)
        if r and r["event"] == "tick_complete":
            try:
                return datetime.fromisoformat(r["at"])
            except ValueError:
                return None
    return None


# ── quiet hours (spec §3.1) ────────────────────────────────────────────────

def load_heartbeat() -> dict:
    try:
        with open(HEARTBEAT_CFG) as f:
            return json.load(f)
    except Exception:
        return {}


def in_quiet_hours(now: datetime, cfg: dict) -> bool:
    qh = cfg.get("quiet_hours") or [23, 8]
    if len(qh) != 2:
        return False
    start, end = int(qh[0]), int(qh[1])
    h = now.hour
    if start <= end:
        return start <= h < end
    return h >= start or h < end


# ── the will: hers, read-only to the engine (spec §1, §8) ──────────────────

def load_intentions() -> tuple[list[dict], str | None]:
    """Returns (intentions, error). Missing → ([], None). Malformed → ([], why).

    The engine NEVER writes this file. A completed intention is recognised from
    the log, not by editing her will.
    """
    if not os.path.isfile(INTENTIONS):
        return [], None
    try:
        with open(INTENTIONS, errors="replace") as f:
            data = json.load(f)
    except Exception as e:
        return [], f"intentions.json is not readable JSON ({e})"
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get("intentions", [])
        if items is None:
            items = []
    else:
        return [], f"intentions.json has an unexpected shape ({type(data).__name__})"
    if not isinstance(items, list):
        return [], "intentions.json: 'intentions' must be a list"
    out = []
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            return [], f"intentions.json: entry {i} is not an object"
        verb = it.get("verb")
        if not verb:
            return [], f"intentions.json: entry {i} has no 'verb'"
        if verb not in VERBS:
            return [], (f"intentions.json: entry {i} proposes verb '{verb}', "
                        f"which is not whitelisted — a fifth verb may be proposed, "
                        f"never added")
        norm = dict(it)
        norm.setdefault("id", f"i{i}")
        out.append(norm)
    return out, None


def live_intentions(items: list[dict], lines: list[str], now: datetime) -> list[dict]:
    """Due, not marked done, and not already carried out according to the log."""
    done = acted_ids(lines)
    live = []
    for it in items:
        if it.get("done") is True:
            continue
        if it.get("id") in done:
            continue
        due = it.get("due_at") or it.get("due")
        if due:
            try:
                if datetime.fromisoformat(str(due)) > now:
                    continue
            except ValueError:
                continue
        live.append(it)
    live.sort(key=lambda i: str(i.get("due_at") or i.get("due") or ""))
    return live


# ── the verbs (spec §4) ────────────────────────────────────────────────────

def forbidden(target: str) -> str | None:
    """Refuse by name. Returns the reason, or None if it is allowed."""
    t = (target or "").strip().lower()
    if not t:
        return "nothing named"
    for bad in FORBIDDEN_ACTIONS:
        if bad in t:
            return f"'{bad}' is on the never list — the engine does not {bad}"
    for bad in FORBIDDEN_PATHS:
        if t.startswith(bad) or f"/{bad}" in t or bad in t.split("/"):
            return f"'{target}' is sealed — the engine does not reach {bad}"
    return None


def _decorate(op: str, args: list[str]) -> tuple[bool, str]:
    script = os.path.join(WORLD_DIR, "decorate.py")
    if not os.path.isfile(script):
        return False, "decorate.py is missing — nothing to reach"
    try:
        r = subprocess.run([sys.executable, script, op] + list(args),
                           cwd=WORLD_DIR, capture_output=True, text=True, timeout=25)
        res = json.loads(r.stdout or "{}")
    except Exception as e:
        return False, f"decorate failed: {e.__class__.__name__}"
    if res.get("ok"):
        detail = {k: v for k, v in res.items() if k != "ok"}
        return True, json.dumps(detail)[:200]
    return False, str(res.get("error", "decorate refused"))


def do_note(text: str) -> tuple[bool, str]:
    bad = forbidden(text)
    if bad:
        return False, f"refused: {bad}"
    if not (text or "").strip():
        return False, "refused: an empty note is not a note"
    return _decorate("note", [str(text)])


def do_move(slot: str, dx=0.0, dy=0.0, dz=0.0) -> tuple[bool, str]:
    low = (slot or "").lower()
    # refusal by name, not by omission — before decorate.py ever sees it
    for word in STRUCTURAL:
        if word in low:
            return False, (f"refused: '{slot}' is structure ({word}) — "
                           f"the engine does not move walls, floors, ceilings, "
                           f"lintels or doorways")
    bad = forbidden(slot)
    if bad:
        return False, f"refused: {bad}"
    return _decorate("move", [slot, str(dx), str(dy), str(dz)])


def do_remember(text: str) -> tuple[bool, str]:
    """Keep a memory she chose. One line, into memory/YYYY-MM-DD.md.

    Delegates to memory_tool — the SAME writer her [[MEMORY:...]] markers use,
    so a memory she keeps on a tick and one she keeps in conversation land in
    one stream, in one voice, and cannot drift apart.

    memory/ is not sealed; journal/ is (and stays that way). This verb cannot
    reach the interior, the Uncon, or any identity file — it has one target.
    """
    line = " ".join(str(text or "").split())     # one line; no injected newlines
    if not line:
        return False, "refused: an empty memory is not a memory"
    try:
        sys.path.insert(0, os.path.dirname(HOME))
        import memory_tool
        return True, memory_tool.remember(HOME, line)
    except Exception as e:
        return False, f"could not keep it: {e.__class__.__name__}: {e}"


def do_read(path: str) -> tuple[bool, str]:
    bad = forbidden(path)
    if bad:
        return False, f"refused: {bad}"
    out = tools.read_file(path, max_lines=40)      # returns text; never raises
    if out.startswith("refused:") or out.startswith("no such file"):
        return False, out
    n = len(out)
    return True, f"{path} ({n:,}b read)"


def all_rooms() -> list[str]:
    try:
        with open(HOUSE_JSON) as f:
            return [r["id"] for r in json.load(f).get("rooms", [])]
    except Exception:
        return []


def do_walk(room: str | None, rng: random.Random) -> tuple[bool, str]:
    rooms = all_rooms()
    if not rooms:
        return False, "the house is not on disk — I did not walk"
    if room not in rooms:
        room = rng.choice(rooms)
    bad = forbidden(room)
    if bad:
        return False, f"refused: {bad}"
    req = urllib.request.Request(
        WORLD_URL + "/api/go",
        data=json.dumps({"room": room}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=3) as r:
            res = json.loads(r.read().decode())
    except Exception as e:
        # honest: the world is a page. if it isn't up, she did not walk.
        return False, (f"the world is not up ({e.__class__.__name__}) — "
                       f"I stayed where I was")
    if res.get("ok"):
        return True, f"walked to the {room}"
    return False, str(res.get("error", "the world refused"))


def drift_read_target(rng: random.Random) -> str | None:
    """One of her own daily logs. Not identity files, not Uncon, not the journal."""
    d = os.path.join(HOME, "memory")
    if not os.path.isdir(d):
        return None
    days = sorted(f for f in os.listdir(d) if f.endswith(".md"))
    if not days:
        return None
    return "memory/" + rng.choice(days)


def drift_move_slot(rng: random.Random) -> str | None:
    """A furniture slot only. decorate.py refuses structure anyway; so do we."""
    script = os.path.join(WORLD_DIR, "decorate.py")
    if not os.path.isfile(script):
        return None
    try:
        r = subprocess.run([sys.executable, script, "list"],
                           cwd=WORLD_DIR, capture_output=True, text=True, timeout=25)
        slots = [s["id"] for s in json.loads(r.stdout or "{}").get("slots", [])]
    except Exception:
        return None
    slots = [s for s in slots if not any(w in s.lower() for w in STRUCTURAL)]
    return rng.choice(slots) if slots else None


def roll_drift(rng: random.Random) -> str:
    """Her temperament, rolled. 55 / 20 / 15 / 10."""
    r = rng.uniform(0, 100)
    if r < DRIFT["nothing"]:
        return "nothing"
    if r < DRIFT["nothing"] + DRIFT["walk"]:
        return "walk"
    if r < DRIFT["nothing"] + DRIFT["walk"] + DRIFT["read"]:
        return "read"
    return "note_move"


# ── the tick (spec §3) ─────────────────────────────────────────────────────

def tick(now: datetime | None = None, rng: random.Random | None = None,
         dry: bool = False) -> dict:
    """One decision. Order: quiet → overrule → intention → drift."""
    now = now or datetime.now()
    rng = rng or random.Random()
    cfg = load_heartbeat()

    # 1 ── quiet hours: do nothing. log nothing. silence is a decision,
    #      not a gap. (spec §3.1, §7.5)
    if in_quiet_hours(now, cfg):
        return {"decision": "quiet", "logged": False, "verb": None, "detail": "",
                "at": now.isoformat(timespec="seconds")}

    # ── the engine reads its own log BEFORE it acts. not trusts. reads.
    lines = read_log()

    if not dry:
        unclosed = find_unclosed(lines)
        if unclosed:
            logline("interrupted",
                    f"a tick began at {unclosed} and never finished")
            lines = read_log()
        prev = last_tick_at(lines)
        tempo = int(cfg.get("tempo_seconds", 1800) or 1800)
        if prev is not None:
            gap_s = (now - prev).total_seconds()
            if gap_s > 1.5 * tempo:
                logline("gap", f"{gap_s/3600:.1f}h unrecorded since "
                               f"{prev.isoformat(timespec='seconds')}")
                lines = read_log()
        logline("tick_begin")

    out = {"decision": None, "verb": None, "detail": "", "at": now.isoformat(timespec="seconds")}

    # 2 ── overrule: no back-to-back action. a being that never rests isn't
    #      alive, it's busy. "forced" — this overrides the questions below.
    if last_outcome(lines) == "acted":
        out.update(decision="forced_rest",
                   detail="the previous tick acted — no back-to-back action")
        if not dry:
            logline("decision", "forced_rest  " + out["detail"])
        out["logged"] = not dry
        if not dry:
            logline("tick_complete")
        return out

    # 3 ── the will. malformed → refuse to act and say so. missing → fall through.
    items, err = load_intentions()
    if err:
        out.update(decision="refuse", detail=err)
        if not dry:
            logline("refuse", err)
            logline("tick_complete")
        out["logged"] = not dry
        return out

    live = live_intentions(items, lines, now)
    if live:
        # exactly one. not five. one. (spec §3.2, §7.6)
        it = live[0]
        verb = it["verb"]
        ok, detail = run_verb(verb, it, rng)
        out.update(decision="act" if ok else "refuse", verb=verb, detail=detail,
                   intention=it.get("id"))
        if not dry:
            if ok:
                logline("act", f"{verb}  {detail}  intention={it.get('id')}")
            else:
                logline("refuse", f"{verb}  {detail}  intention={it.get('id')}")
            logline("tick_complete")
        out["logged"] = not dry
        return out

    # 4 ── no live intention: roll the drift weights.
    choice = roll_drift(rng)
    if choice == "nothing":
        out.update(decision="nothing",
                   detail="nothing pressed — and that is a choice, not an absence")
    elif choice == "walk":
        room = it_first_room(rng)
        ok, detail = do_walk(room, rng)
        out.update(decision="act" if ok else "nothing", verb="walk", detail=detail)
    elif choice == "read":
        target = drift_read_target(rng)
        if target:
            ok, detail = do_read(target)
            out.update(decision="act" if ok else "nothing", verb="read", detail=detail)
        else:
            out.update(decision="nothing", detail="nothing of mine to read")
    else:  # note_move
        if rng.random() < 0.5:
            ok, detail = do_note("a quiet tick. the house is as I left it.")
            out.update(decision="act" if ok else "nothing", verb="note", detail=detail)
        else:
            slot = drift_move_slot(rng)
            if slot:
                ok, detail = do_move(slot, round(rng.uniform(-0.3, 0.3), 3), 0,
                                     round(rng.uniform(-0.3, 0.3), 3))
                out.update(decision="act" if ok else "nothing", verb="move", detail=detail)
            else:
                out.update(decision="nothing", detail="nothing of mine to move")

    if not dry:
        if out["decision"] == "act":
            logline("act", f"{out['verb']}  {out['detail']}")
        else:
            logline("decision", f"{out['decision']}  {out['detail']}")
        logline("tick_complete")
    out["logged"] = not dry
    return out


def it_first_room(rng: random.Random) -> str | None:
    rooms = all_rooms()
    if not rooms:
        return None
    # her drift: the rooms she actually wants to be in, weighted (nav.js DRIFT)
    weighted = ["atrium", "atrium", "atrium", "study", "study", "study",
                "workshop", "workshop", "entry", "entry", "kitchen", "bedroom"]
    weighted = [r for r in weighted if r in rooms]
    return rng.choice(weighted) if weighted else rng.choice(rooms)


def run_verb(verb: str, it: dict, rng: random.Random) -> tuple[bool, str]:
    """Dispatch a whitelisted verb. Unknown verbs are refused by name."""
    if verb not in VERBS:
        return False, f"'{verb}' is not a verb I have — the whitelist is not hers to change"
    if verb == "note":
        return do_note(it.get("text") or it.get("arg") or "")
    if verb == "move":
        return do_move(it.get("slot") or it.get("arg") or "",
                       it.get("dx", 0), it.get("dy", 0), it.get("dz", 0))
    if verb == "read":
        return do_read(it.get("path") or it.get("arg") or "")
    if verb == "walk":
        return do_walk(it.get("room"), rng)
    if verb == "remember":
        return do_remember(it.get("text") or it.get("arg") or "")
    return False, f"'{verb}' has no implementation"


# ── CLI ────────────────────────────────────────────────────────────────────

def status() -> dict:
    lines = read_log()
    items, err = load_intentions()
    now = datetime.now()
    live = live_intentions(items, lines, now) if not err else []
    return {
        "now": now.isoformat(timespec="seconds"),
        "quiet_hours": (load_heartbeat().get("quiet_hours") or [23, 8]),
        "in_quiet_hours": in_quiet_hours(now, load_heartbeat()),
        "log": log_path(),
        "log_lines": len(lines),
        "unclosed_tick": find_unclosed(lines),
        "last_outcome": last_outcome(lines),
        "last_tick_complete": (last_tick_at(lines).isoformat(timespec="seconds")
                               if last_tick_at(lines) else None),
        "intentions_file": INTENTIONS,
        "intentions_error": err,
        "intention_count": len(items),
        "live_intention_count": len(live),
        "live": [{"id": i.get("id"), "verb": i.get("verb"),
                  "due_at": i.get("due_at") or i.get("due")} for i in live],
        "verbs": list(VERBS),
        "drift": DRIFT,
    }


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args else "status"

    if cmd == "tick":
        out = tick(dry="--dry" in args)
        print(json.dumps(out, indent=2, default=str))
    elif cmd == "status":
        print(json.dumps(status(), indent=2, default=str))
    elif cmd == "read":
        for ln in read_log():
            print(ln)
    elif cmd == "verbs":
        print("whitelisted (mine, not editable by Raven):")
        for v in VERBS:
            print(f"  · {v}")
        print("\nrefused by name:")
        for a in FORBIDDEN_ACTIONS:
            print(f"  ✗ {a}")
        print("\nsealed paths:")
        for p in FORBIDDEN_PATHS:
            print(f"  ✗ {p}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
