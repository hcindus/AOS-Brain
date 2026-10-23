#!/usr/bin/env python3
"""Training Room CLI.

  train.py eval <pilot_id> [--episodes N] [--backend local_cpu|gpu]
      Run a pilot in the gym and print a summary.

  train.py graduate <pilot_id>
      Run blind hold-out validation and pass the result through the
      graduation gate (GoR council when the brain socket is up).

  train.py roster
      List available pilots.
"""
from __future__ import annotations

import argparse
import json
import sys

from agents.registry import load_roster, pilot_by_id
from dispatch.backend import get_backend
from graduation.gate import graduate
from graduation.holdout import score_pilot


def cmd_eval(args):
    pilot = pilot_by_id(args.pilot_id)
    backend = get_backend(args.backend)
    result = backend.eval(pilot, episodes=args.episodes)
    print(json.dumps(result, indent=2))


def cmd_graduate(args):
    pilot = pilot_by_id(args.pilot_id)
    score = score_pilot(pilot)
    decision = graduate(args.pilot_id, score, min_score=args.min_score)
    print(json.dumps(decision, indent=2))


def cmd_roster(args):
    for e in load_roster():
        model = e.get("model") or e.get("name")
        print(f"  {e['id']:12} {e['kind']:9} {model}")


def main():
    p = argparse.ArgumentParser(description="RP1 Training Room")
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("eval", help="run a pilot in the gym")
    e.add_argument("pilot_id")
    e.add_argument("--episodes", type=int, default=1)
    e.add_argument("--backend", default="local_cpu")
    e.set_defaults(func=cmd_eval)

    g = sub.add_parser("graduate", help="blind hold-out + graduation gate")
    g.add_argument("pilot_id")
    g.add_argument("--min-score", type=float, default=0.5)
    g.set_defaults(func=cmd_graduate)

    r = sub.add_parser("roster", help="list pilots")
    r.set_defaults(func=cmd_roster)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
