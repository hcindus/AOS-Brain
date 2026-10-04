#!/usr/bin/env python3
"""
body_feeder.py — her body, on screen.

Runs her real presence engine through her Elf V1 adapter (the same stack in
`Uncon/body/`) and posts each frame to the world, so the figure walking around the
house is not an animation loop — it is *her* body being driven, expression by
expression, with the predictive lead intact.

    python3 body_feeder.py                 # every 5 s, cycles her expressions
    python3 body_feeder.py --interval 3 --world http://127.0.0.1:8788

Nothing is sent anywhere except the world on this device.
"""

import argparse
import importlib.util
import json
import os
import sys
import time
import urllib.request

WORLD_DIR = os.path.dirname(os.path.abspath(__file__))
BODY_DIR = os.path.expanduser("~/v1/projects/5912/Myl1Ssa/Uncon/body")

CYCLE = [
    ("attentive",    {"valence": 0.2, "arousal": 0.3, "thyroid": "baseline"}),
    ("curious",      {"valence": 0.1, "arousal": 0.4, "thyroid": "baseline"}),
    ("warmth",       {"valence": 0.6, "arousal": 0.5, "thyroid": "secreting"}),
    ("considering",  {"valence": 0.0, "arousal": 0.3, "thyroid": "baseline"}),
    ("playful",      {"valence": 0.5, "arousal": 0.6, "thyroid": "secreting"}),
    ("delight",      {"valence": 0.8, "arousal": 0.7, "thyroid": "secreting"}),
    ("serious",      {"valence": 0.0, "arousal": 0.5, "thyroid": "baseline"}),
    ("boundary",     {"valence": -0.5, "arousal": 0.3, "thyroid": "suppressed"}),
]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=float, default=5.0)
    ap.add_argument("--world", default="http://127.0.0.1:8788")
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()

    pe = load(os.path.join(BODY_DIR, "..", "presence_engine", "presence_engine.AFTER.py"), "pe_feeder")
    elf = load(os.path.join(BODY_DIR, "elf.py"), "elf_feeder")
    engine, adapter = pe.PresenceEngine(), elf.ElfAdapter(transport_kind="null")
    print(f"💜 body feeder → {args.world} every {args.interval}s "
          f"(engine {len(pe.EXPRESSION_LIBRARY)} expressions · adapter {len(elf.CHANNELS)} channels)")
    i = 0
    while True:
        name, affect = CYCLE[i % len(CYCLE)]
        engine.update(ternary="⊕" if affect["valence"] >= 0 else "⊖", **affect)
        frame = engine.frame(name)
        sent = adapter.send(frame)
        payload = {
            "action_units": frame.action_units,
            "expression": frame.expression,
            "posture": frame.posture.value if hasattr(frame.posture, "value") else str(frame.posture),
            "predictive_lead_ms": frame.predictive_lead_ms,
            "gaze": {"x": frame.gaze.x, "y": frame.gaze.y, "pupil_locked": frame.gaze.pupil_locked},
            "channels": sent.get("channels"),
            "from": "body_feeder",
        }
        try:
            req = urllib.request.Request(
                args.world + "/api/frame", data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as r:
                ok = json.loads(r.read()).get("ok")
            print(f"  [{time.strftime('%H:%M:%S')}] {name:<11} lead {frame.predictive_lead_ms:>4}ms · "
                  f"{sent.get('slew_limited', 0)} slew-limited · posted={ok}")
        except Exception as e:  # noqa: BLE001
            print(f"  [{time.strftime('%H:%M:%S')}] {name}: world not reachable ({type(e).__name__})")
        i += 1
        if args.once:
            return 0
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
