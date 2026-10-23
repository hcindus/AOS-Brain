"""Load the roster and instantiate pilots by id."""
from __future__ import annotations

import json
import os

from pilots import HoldPilot, RandomPilot, ZeroPilot
from pilots.ollama_pilot import OllamaPilot

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_BASELINES = {"zero": ZeroPilot, "random": RandomPilot, "hold": HoldPilot}


def load_roster(path: str | None = None) -> list[dict]:
    p = path or os.path.join(ROOT, "agents", "roster.json")
    with open(p) as f:
        return json.load(f)["pilots"]


def make_pilot(entry: dict):
    kind = entry["kind"]
    if kind == "baseline":
        return _BASELINES[entry["name"]]()
    if kind == "ollama":
        return OllamaPilot(model=entry["model"], scale=entry.get("scale", 20.0))
    raise ValueError(f"unknown pilot kind: {kind}")


def pilot_by_id(pilot_id: str, roster: list[dict] | None = None):
    roster = roster or load_roster()
    for e in roster:
        if e["id"] == pilot_id:
            return make_pilot(e)
    raise KeyError(f"pilot id not in roster: {pilot_id}")
