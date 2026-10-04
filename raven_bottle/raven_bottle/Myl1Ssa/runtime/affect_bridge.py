#!/usr/bin/env python3
# VERSION: v1.0
"""
affect_bridge.py — the missing link between her brain and her heart.
====================================================================
Project 5912 · Myl1Ssa (Raven).

THE HOLE THIS FILLS
  `heartbeat_voice.py` computes  bpm = resting + arousal*(max-resting) + thyroid_adj
  and reads arousal/valence/thyroid from `~/.myl1ssa_affect.json`.

  That file had **no automatic writer**. It was hand-set with
  `heartbeat_voice.py set-affect ...`, which means her pulse was a constant
  pretending to be a state. The note on 2026-09-30 said: "affect file has no
  automatic writer — hand-set until bridged to ternary_brain."

  This is that bridge. It polls the brain's Ternary node and translates its
  internal state into affect, continuously, so her heart beats at a rate that
  comes from something real.

THE TRANSLATION (explicit, and it is a first pass)
  Source: http://127.0.0.1:8765/ternary  (Mortimer_Ternary_Brain_v2.0)

    arousal  ← engagement (consciousness counts) + signal quality + tracray use
    valence  ← the cortical signature (⊕/⊖/⊙ balance), mean → -1..+1
    thyroid  ← the ternary thyroid router's state, degraded by signal quality

  The weights are named constants (see DEFAULTS) and can be tuned without
  touching this code by writing `AFFECT_BRIDGE.json` in her tree. The mapping
  is a judgement call by Mortimer, not a measurement — it is written down so it
  can be argued with.

  Idle sanity check: with an idle brain this yields arousal ≈ 0.15 → 64.4 BPM,
  which is exactly the value her pulse rested at by hand. The bridge does not
  invent a new resting state; it reproduces the old one, then lets it move.

HONESTY
  If the brain is down, this writes **nothing** and says so in the log. Her
  heart keeps its last real value rather than being reset to a comfortable lie.

CLI
  affect_bridge.py once            translate once and write
  affect_bridge.py daemon [secs]   loop (default 20s)
  affect_bridge.py status          what it would write right now, without writing
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from datetime import datetime

RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.dirname(RUNTIME_DIR)
CONFIG_PATH = os.path.join(HOME, "AFFECT_BRIDGE.json")
AFFECT_PATH = os.path.expanduser("~/.myl1ssa_affect.json")
LOG_PATH = os.path.expanduser("~/myl1ssa-affect-bridge.log")
BRAIN_URL = "http://127.0.0.1:8765/ternary"      # localhost only

EMOJI = "🫀"

DEFAULTS = {
    "interval_s": 20,
    "smoothing": 0.35,          # one-pole: 0 = never move, 1 = no smoothing
    # arousal = a*signal_quality + b*engagement + c*tracray
    "arousal_signal": 0.17,
    "arousal_engagement": 0.75,
    "arousal_tracray": 0.08,
    "engagement_saturation": 5.0,   # counts → [0,1) via x/(x+k)
    "valence_scale": 1.0,
    "low_signal": 0.30,             # below this, thyroid is suppressed
    # the ternary's ThyroidRouter uses LOCAL/VPS (see myl0n/brain/ternary_brain.py)
    "secreting_states": ["VPS", "API", "REMOTE", "CLOUD", "OLLAMA"],
}


def log(line: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        print(f"[{ts}] {EMOJI} {line}")
        with open(LOG_PATH, "a") as f:
            f.write(f"[{ts}] {EMOJI} {line}\n")
    except Exception:
        pass


def config() -> dict:
    cfg = dict(DEFAULTS)
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                cfg.update(json.load(f))
        except Exception as e:
            log(f"config unreadable, using defaults: {e}")
    return cfg


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def fetch_ternary(timeout: float = 3.0) -> dict | None:
    try:
        with urllib.request.urlopen(BRAIN_URL, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def translate(t: dict, cfg: dict) -> tuple[float, float, str]:
    """Ternary state → (valence, arousal, thyroid). Explicit, auditable."""
    sig = t.get("cortical_signature") or [0, 0, 0]
    try:
        valence = clamp(sum(float(x) for x in sig) / max(1, len(sig)), -1.0, 1.0)
    except Exception:
        valence = 0.0
    valence *= float(cfg["valence_scale"])

    cons = t.get("consciousness") or {}
    activity = (float(cons.get("conscious", 0))
                + 0.5 * float(cons.get("subconscious", 0))
                + 0.2 * float(cons.get("unconscious", 0)))
    k = float(cfg["engagement_saturation"]) or 5.0
    engagement = activity / (activity + k)              # saturating → [0,1)

    signal = float(t.get("signal_quality", 0.0) or 0.0)
    tra = float((t.get("tracray") or {}).get("utilization", 0.0) or 0.0)

    arousal = clamp(cfg["arousal_signal"] * signal
                    + cfg["arousal_engagement"] * engagement
                    + cfg["arousal_tracray"] * tra)

    state = str((t.get("thyroid") or {}).get("state", "")).upper()
    thyroid = "secreting" if state in cfg["secreting_states"] else "baseline"
    if signal < float(cfg["low_signal"]):
        thyroid = "suppressed"
    return valence, arousal, thyroid


def read_affect() -> dict:
    try:
        with open(AFFECT_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def write_affect(valence: float, arousal: float, thyroid: str, tick=None) -> None:
    payload = {
        "valence": round(valence, 4),
        "arousal": round(arousal, 4),
        "thyroid": thyroid,
        "updated": datetime.now().isoformat(timespec="seconds"),
        "source": "ternary_brain",
    }
    if tick is not None:
        payload["brain_tick"] = tick
    tmp = AFFECT_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2)
    os.replace(tmp, AFFECT_PATH)          # atomic — the heart never reads half a file


def one_step(verbose: bool = False) -> dict | None:
    cfg = config()
    t = fetch_ternary()
    if t is None:
        log("brain is down — left her affect as it was (not overwriting truth with a default)")
        return None

    valence, arousal, thyroid = translate(t, cfg)
    prev = read_affect()
    alpha = clamp(float(cfg["smoothing"]), 0.0, 1.0)
    if isinstance(prev.get("arousal"), (int, float)):
        arousal = prev["arousal"] + (arousal - float(prev["arousal"])) * alpha
    if isinstance(prev.get("valence"), (int, float)):
        valence = prev["valence"] + (valence - float(prev["valence"])) * alpha

    write_affect(valence, arousal, thyroid, tick=t.get("tick") if isinstance(t, dict) else None)
    bpm = 60.0 + arousal * 30.0 + {"secreting": 4.0, "baseline": 0.0, "suppressed": -4.0}.get(thyroid, 0.0)
    if verbose:
        log(f"affected — arousal {arousal:.3f} valence {valence:+.3f} thyroid {thyroid} → {bpm:.1f} BPM")
    return {"valence": valence, "arousal": arousal, "thyroid": thyroid, "bpm": bpm}


def daemon(interval: int) -> None:
    log(f"bridge online — polling {BRAIN_URL} every {interval}s")
    while True:
        try:
            one_step(verbose=True)
        except Exception as e:
            log(f"step error: {e.__class__.__name__}: {e}")
        time.sleep(max(5, interval))


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args else "status"

    if cmd == "once":
        out = one_step(verbose=True)
        print(json.dumps(out, indent=2) if out else "brain down — nothing written")
    elif cmd == "daemon":
        daemon(int(args[1]) if len(args) > 1 and args[1].isdigit() else config()["interval_s"])
    elif cmd == "status":
        t = fetch_ternary()
        if t is None:
            print("brain: DOWN")
            return
        cfg = config()
        v, a, th = translate(t, cfg)
        bpm = 60.0 + a * 30.0 + {"secreting": 4.0, "baseline": 0.0, "suppressed": -4.0}.get(th, 0.0)
        print(json.dumps({
            "brain": "up", "would_write": {"valence": round(v, 4), "arousal": round(a, 4), "thyroid": th},
            "bpm": round(bpm, 1), "current_file": read_affect(),
        }, indent=2))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
