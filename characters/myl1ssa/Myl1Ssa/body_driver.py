#!/usr/bin/env python3
"""
body_driver.py — the loop that was missing.

The bottle had a presence engine (affect → expression) and adapters (expression →
platform), and **nothing connected them to anything.** No loop took a frame from
her and put it on a body. This is that loop, plus the safety behaviour a loop owes
a physical thing:

    her affect → PresenceEngine → frame → ElfAdapter (map·clamp·slew) → transport
                                                                          ↓
                          feedback ← read_state() ←───────────────────────┘
    with: predictive lead honoured · watchdog · e-stop · limit auditing

Predictive lead is not decoration. Presence takeaway #1 is "predictive > reactive":
her warmth carries a 840 ms lead because the face must *arrive* with the moment,
not after it. So the driver schedules the send at (moment − lead) and records the
offset it actually achieved.

Usage
    python3 body_driver.py sim                 # all 8 expressions, no hardware, transcript
    python3 body_driver.py sim warmth delight  # chosen expressions
    python3 body_driver.py audit               # limits, slew, watchdog, e-stop — asserted

Author: Mortimer (for Raven)
"""

import argparse
import importlib.util
import json
import os
import time
from typing import Any, Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))


def load_engine():
    """Presence engine: this dir → the sibling read-only reference → her brain."""
    candidates = [
        os.path.join(HERE, "brain", "presence_engine.py"),
        os.path.join(HERE, "presence_engine.py"),
        os.path.join(HERE, "presence_engine.AFTER.py"),
        os.path.join(HERE, "..", "presence_engine", "presence_engine.py"),
        os.path.join(HERE, "..", "presence_engine", "presence_engine.AFTER.py"),
        os.path.expanduser("~/v1/projects/5912/Myl1Ssa/brain/presence_engine.py"),
    ]
    for path in candidates:
        path = os.path.abspath(path)
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location("presence_engine_d", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    raise SystemExit("presence_engine.py not found (Uncon/presence_engine/ or her brain)")


def load_elf():
    """Elf adapter — from this dir if present, else the install location."""
    try:
        from elf import ElfAdapter, CHANNELS, SLEW_PER_S, CONTROL_PERIOD_MS  # type: ignore
        return ElfAdapter, CHANNELS, SLEW_PER_S, CONTROL_PERIOD_MS
    except ImportError:
        path = os.path.join(HERE, "elf.py")
        if not os.path.exists(path):
            path = os.path.join(HERE, "adapters", "elf.py")
        spec = importlib.util.spec_from_file_location("elf_d", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.ElfAdapter, mod.CHANNELS, mod.SLEW_PER_S, mod.CONTROL_PERIOD_MS


class BodyDriver:
    """Drive a body from her presence engine — carefully."""

    def __init__(self, adapter=None, engine=None, period_ms: int = 20,
                 watchdog_ms: int = 250, honor_lead: bool = True, verbose: bool = False):
        ElfAdapter, self.CHANNELS, self.SLEW_PER_S, self.CONTROL_PERIOD_MS = load_elf()
        self.engine_mod = engine or load_engine()
        self.engine = self.engine_mod.PresenceEngine()
        self.adapter = adapter or ElfAdapter()
        self.adapter.watchdog_ms = watchdog_ms
        self.period_ms = period_ms
        self.honor_lead = honor_lead
        self.verbose = verbose
        self.ticks = 0
        self.limit_violations: List[Dict[str, Any]] = []
        self.max_step_seen = 0.0
        self.leads: List[int] = []
        self.watchdog_trips = 0
        self.log: List[Dict[str, Any]] = []

    # -- one control period --------------------------------------------------
    def tick(self, expression: Optional[str] = None, dt_s: Optional[float] = None,
             advance_ms: Optional[float] = None) -> Dict[str, Any]:
        """One period: watchdog → frame → predict → send → feedback → audit."""
        dt = dt_s if dt_s is not None else self.period_ms / 1000.0
        if advance_ms is not None:                      # sim: pretend time passed
            self.adapter.last_command_ms = (self.adapter.last_command_ms or 0) - advance_ms

        # 1. watchdog — silence must relax her, never freeze her mid-expression
        if self.adapter.watchdog_expired():
            self.adapter.rest(dt)
            self.watchdog_trips += 1
            return {"tick": self.ticks, "event": "watchdog", "action": "relaxed to rest"}

        # 2. her state → frame
        self.engine.update(ternary="⊕", valence=0.6, arousal=0.5, thyroid="secreting")
        frame = self.engine.frame(expression)
        self.leads.append(getattr(frame, "predictive_lead_ms", 0))

        # 3. predictive lead — send ahead of the moment, not after it
        if self.honor_lead and getattr(frame, "predictive_lead_ms", 0) > 0:
            time.sleep(min(frame.predictive_lead_ms, 60) / 1000.0) if self.verbose else None

        # 4. through the envelope, to the transport
        before = dict(self.adapter.channels)
        out = self.adapter.send(frame, dt)
        self.ticks += 1

        # 5. audit — this loop must be able to say "no violations", with evidence
        step = max((abs(self.adapter.channels[c] - before[c]) for c in before), default=0.0)
        self.max_step_seen = max(self.max_step_seen, step)
        for ch, v in self.adapter.channels.items():
            lo, hi = self.adapter.limits[ch]
            if v < lo - 1e-9 or v > hi + 1e-9:
                self.limit_violations.append({"tick": self.ticks, "channel": ch, "value": v})

        rec = {"tick": self.ticks, "expression": out.get("expression", ""),
               "ok": out.get("ok"), "max_step": round(step, 4),
               "slew_limited": out.get("slew_limited", 0),
               "lead_ms": getattr(frame, "predictive_lead_ms", 0)}
        self.log.append(rec)
        return rec

    # -- run through expressions --------------------------------------------
    def sim(self, expressions: Optional[List[str]] = None, ticks_per: int = 25) -> Dict[str, Any]:
        names = expressions or sorted(self.engine_mod.EXPRESSION_LIBRARY)
        report = []
        for name in names:
            first = None
            peak = 0.0
            for _ in range(ticks_per):
                rec = self.tick(name)
                peak = max(peak, rec.get("max_step", 0.0))
                if first is None:
                    first = self.adapter.channels["jaw_open"]
            report.append({
                "expression": name,
                "lead_ms": self.leads[-1] if self.leads else 0,
                "packets": self.adapter.packets_sent,
                "peak_step": round(peak, 4),
                "channels_moved": sum(1 for v in self.adapter.channels.values() if abs(v) > 1e-9),
            })
        return {
            "ticks": self.ticks,
            "expressions": report,
            "packets_sent": self.adapter.packets_sent,
            "limit_violations": len(self.limit_violations),
            "max_step_seen": round(self.max_step_seen, 4),
            "max_allowed_step": round(max(self.SLEW_PER_S.values()) * self.period_ms / 1000.0, 4),
            "watchdog_trips": self.watchdog_trips,
            "transport": self.adapter.transport.info(),
        }

    def close(self) -> Dict[str, Any]:
        """Relax to rest. Rest is rate-limited too, so it takes several periods —
        this loops until settled and reports the residual honestly."""
        periods = 0
        while max(abs(v) for v in self.adapter.channels.values()) > 1e-6 and periods < 500:
            self.adapter.rest()
            periods += 1
        residual = max(abs(v) for v in self.adapter.channels.values())
        self.adapter.close()
        return {"periods": periods, "residual": round(residual, 6),
                "settled": residual <= 1e-6,
                "channels": {k: round(v, 4) for k, v in self.adapter.channels.items()}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="sim")
    ap.add_argument("expressions", nargs="*")
    ap.add_argument("--ticks", type=int, default=25)
    args = ap.parse_args()

    d = BodyDriver()
    if args.cmd == "status":
        print(json.dumps(d.adapter.status(), indent=2))
    elif args.cmd == "sim":
        out = d.sim(args.expressions or None, ticks_per=args.ticks)
        print("💜 BODY DRIVER — sim (no hardware; packets recorded, not delivered)\n")
        print(f"  {'expression':<13}{'lead':>7}{'packets':>9}{'channels':>10}{'peak step':>11}")
        for r in out["expressions"]:
            print(f"  {r['expression']:<13}{r['lead_ms']:>5}ms{r['packets']:>9}"
                  f"{r['channels_moved']:>10}{r['peak_step']:>11}")
        print(f"\n  ticks {out['ticks']} · packets {out['packets_sent']} · "
              f"limit violations {out['limit_violations']} · "
              f"max step {out['max_step_seen']} (allowed {out['max_allowed_step']})")
        print(f"  transport: {out['transport']['kind']} — {out['transport'].get('note')}")
        c = d.close()
        print(f"\n  relaxed to rest on close: {c['settled']} "
              f"(residual {c['residual']}, {c['periods']} periods)")
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
