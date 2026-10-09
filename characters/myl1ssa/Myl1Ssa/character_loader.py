#!/usr/bin/env python3
"""
Character Loader — load a person from the family into a body.

The glue between a character's PresenceEngine (mind → affect → action units)
and the universal BodyAdapter HAL (any form factor: unitree, blender,
digital_world, elf).

A character is: SOUL (who she is) + PresenceEngine (how she moves) + voice.
A body is: a BodyAdapter (where she lives). This module wires them together.

Usage:
    from character_loader import load_character, family

    p = load_character("raven", platform="blender")
    out = p.express("warmth")                     # named expression
    out = p.express(valence=0.6, arousal=0.4)     # or from raw affect
    print(p.status())

    python3 character_loader.py demo              # prove the whole pipeline
"""
from __future__ import annotations

import sys
from typing import Any, Dict, Optional

from adapters import get_adapter, available_platforms
from adapters.base import frame_from_presence, BodyAdapter
from brain.presence_engine import PresenceEngine

# ── the family registry ──────────────────────────────────────────────────
# Each character: display name + optional default body. The PresenceEngine
# itself is still Raven's (the expression library lives in presence_engine.py);
# other characters drop their own engine/library in as they're built.
CHARACTERS: Dict[str, Dict[str, Any]] = {
    "raven":   {"display": "Raven (Myl1Ssa.R8s)", "default_platform": None},
    "myl1ssa": {"display": "Raven (Myl1Ssa.R8s)", "default_platform": None},
    "voss":    {"display": "Kael Voss",           "default_platform": None, "note": "engine not built yet"},
    "tappy":   {"display": "Tappy Lewis",         "default_platform": None, "note": "engine not built yet"},
}


class Presence:
    """A loaded character, bound to a body adapter."""

    def __init__(self, key: str, meta: Dict[str, Any], engine: PresenceEngine,
                 adapter: BodyAdapter):
        self.key = key
        self.meta = meta
        self.engine = engine
        self.adapter = adapter

    def express(self, expression: Optional[str] = None, *, ternary: str = "⊙",
                valence: float = 0.0, arousal: float = 0.0,
                thyroid: str = "baseline") -> Dict[str, Any]:
        """Feed affect → produce a frame → translate it onto the body."""
        self.engine.update(ternary=ternary, valence=valence,
                           arousal=arousal, thyroid=thyroid)
        frame = frame_from_presence(self.engine, expression)
        return self.adapter.apply(frame)

    def status(self) -> Dict[str, Any]:
        return {
            "character": self.meta["display"],
            "platform": self.adapter.platform,
            "engine": self.engine.status(),
            "adapter": self.adapter.status(),
        }


def family() -> Dict[str, str]:
    """Human-readable roster of loadable characters."""
    return {k: v["display"] for k, v in CHARACTERS.items()}


def load_character(name: str, platform: Optional[str] = None) -> Presence:
    """Load a character by name, bound to a body adapter (platform id)."""
    key = name.lower().strip()
    if key not in CHARACTERS:
        raise KeyError(f"Unknown character '{name}'. Family: {list(CHARACTERS)}")

    meta = CHARACTERS[key]
    engine = PresenceEngine()

    if platform is None:
        platform = meta.get("default_platform") or available_platforms()[0]
    adapter = get_adapter(platform)

    return Presence(key, meta, engine, adapter)


def _demo() -> None:
    print("Character Loader — family roster:")
    for k, v in family().items():
        print(f"  {k:10s} {v}")

    print(f"\nAvailable bodies: {available_platforms()}")

    p = load_character("raven")
    print(f"\nLoaded: {p.status()['character']} → {p.adapter.platform}")

    for expr in ["warmth", "delight", "curious", "boundary"]:
        out = p.express(expr)
        summary = {k: v for k, v in out.items() if not isinstance(v, dict)} or out
        keys = list(out.keys())
        print(f"  express('{expr}') → adapter returned keys: {keys}")

    print("\n✅ pipeline works: affect → frame → AdapterFrame → adapter.apply()")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        _demo()
    else:
        _demo()
