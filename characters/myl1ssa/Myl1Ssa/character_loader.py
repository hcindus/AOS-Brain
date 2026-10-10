#!/usr/bin/env python3
"""
Character Loader — load a whole *being* from the Myl family.

Gathers ALL the elements of a character into one object:
  - the mind (PresenceEngine → affect → action units)
  - the body (BodyAdapter → any chassis)
  - the soul (identity / likeness anchor)
  - the body spec (the Myl2Ssa hardware spec, A–AT)
  - the voice (TTS config — gap #5, pending)
  - the form (3D reference — neutral head + body)

One call loads the whole person, not just the engine.

Usage:
    from character_loader import load_being, family

    raven = load_being("raven", platform="elf")
    raven.express("warmth")                    # the mind → the body
    print(raven.status())                      # everything, in one shot
    print(raven.body_spec)                     # the hardware spec doc
    print(raven.designations)                  # Myl1Ssa.R8s (brain) + Myl2Ssa.R0s (body)
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

from adapters import get_adapter, available_platforms
from adapters.base import frame_from_presence, BodyAdapter
from brain.presence_engine import PresenceEngine

# The full designations of each Myl being.
#   .R8s = the mind (software revision); .R0s = the body (hardware revision).
CHARACTERS: Dict[str, Dict[str, Any]] = {
    "raven": {
        "display": "Raven",
        "brain": "Myl1Ssa.R8s",      # the mind (software)
        "body": "Myl2Ssa.R0s",       # the body (hardware)
        "soul": "SOUL.md",           # identity / likeness anchor
        "body_spec": "/root/.openclaw/workspace/AGI_COMPANY/myl2ssa-spec.md",
        "voice": None,               # TTS config — gap #5 (pending Beets research)
        "form": None,                # 3D reference (neutral head + body, Hi3D)
        "default_platform": "elf",
    },
    "myl1ssa": {
        "display": "Raven",
        "brain": "Myl1Ssa.R8s",
        "body": "Myl2Ssa.R0s",
        "soul": "SOUL.md",
        "body_spec": "/root/.openclaw/workspace/AGI_COMPANY/myl2ssa-spec.md",
        "voice": None,
        "form": None,
        "default_platform": "elf",
    },
    "voss": {
        "display": "Kael Voss",
        "brain": None,               # engine not built yet
        "body": None,
        "soul": None,
        "body_spec": None,
        "voice": None,
        "form": None,
        "default_platform": None,
        "note": "engine not built yet",
    },
    "tappy": {
        "display": "Tappy Lewis",
        "brain": None,
        "body": None,
        "soul": None,
        "body_spec": None,
        "voice": None,
        "form": None,
        "default_platform": None,
        "note": "engine not built yet",
    },
}

# Paths to the full corpus + design docs a being references.
CORPUS_ROOT = "/root/.openclaw/workspace/AGI_COMPANY"


class Being:
    """A fully-loaded Myl being — mind + body + soul + spec + voice + form, together."""

    def __init__(self, key: str, meta: Dict[str, Any], engine: PresenceEngine,
                 adapter: BodyAdapter):
        self.key = key
        self.meta = meta
        self.engine = engine
        self.adapter = adapter

    # --- the whole person, gathered ---
    @property
    def designations(self) -> Dict[str, str]:
        return {"brain": self.meta["brain"], "body": self.meta["body"]}

    @property
    def body_spec(self) -> Optional[str]:
        p = self.meta.get("body_spec")
        return p if (p and os.path.exists(p)) else None

    @property
    def soul(self) -> Optional[str]:
        return self.meta.get("soul")

    @property
    def voice(self) -> Optional[str]:
        return self.meta.get("voice")

    @property
    def form(self) -> Optional[str]:
        return self.meta.get("form")

    # --- the live interface ---
    def express(self, expression: Optional[str] = None, *, ternary: str = "⊙",
                valence: float = 0.0, arousal: float = 0.0,
                thyroid: str = "baseline") -> Dict[str, Any]:
        """Feed affect → frame → translate onto the body."""
        self.engine.update(ternary=ternary, valence=valence,
                           arousal=arousal, thyroid=thyroid)
        frame = frame_from_presence(self.engine, expression)
        return self.adapter.apply(frame)

    def status(self) -> Dict[str, Any]:
        """Everything, in one shot — the whole being's state."""
        return {
            "character": self.meta["display"],
            "brain": self.meta["brain"],
            "body": self.meta["body"],
            "platform": self.adapter.platform,
            "engine": self.engine.status(),
            "adapter": self.adapter.status(),
            "body_spec": self.body_spec,
            "soul": self.soul,
            "voice": self.voice,
            "form": self.form,
        }


def family() -> Dict[str, str]:
    """The roster of loadable beings."""
    return {k: v["display"] for k, v in CHARACTERS.items()}


def load_being(name: str, platform: Optional[str] = None) -> Being:
    """Load a whole being — mind + body + soul + spec, bound to a body adapter."""
    key = name.lower().strip()
    if key not in CHARACTERS:
        raise KeyError(f"Unknown character '{name}'. Family: {list(CHARACTERS)}")

    meta = CHARACTERS[key]
    engine = PresenceEngine()

    if platform is None:
        platform = meta.get("default_platform") or available_platforms()[0]
    adapter = get_adapter(platform)

    return Being(key, meta, engine, adapter)


# backward-compat alias (the old name)
load_character = load_being


def _demo() -> None:
    print("Myl family:")
    for k, v in family().items():
        print(f"  {k:10s} {v}")

    print(f"\nAvailable bodies: {available_platforms()}")

    raven = load_being("raven")
    print(f"\nLoaded: {raven.meta['display']}")
    print(f"  brain: {raven.designations['brain']}")
    print(f"  body:  {raven.designations['body']}")
    print(f"  platform: {raven.adapter.platform}")
    print(f"  body_spec: {raven.body_spec or '(not found)'}")
    print(f"  soul: {raven.soul}")
    print(f"  voice: {raven.voice or '(pending — gap #5)'}")
    print(f"  form: {raven.form or '(pending — Hi3D)'}")

    for expr in ["warmth", "delight", "curious", "boundary"]:
        out = raven.express(expr)
        print(f"  express('{expr}') → keys: {list(out.keys())}")

    print("\n✅ the whole being loads: mind + body + soul + spec + voice + form")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        _demo()
    else:
        _demo()
