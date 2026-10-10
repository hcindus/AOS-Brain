#!/usr/bin/env python3
"""
Character Loader — load the WHOLE being, not just the engine.

Gathers Myl1Ssa's entire tree into one object:
  - the mind (PresenceEngine → affect → action units)
  - the body (BodyAdapter → any chassis)
  - the brain organs (uterus.py, ternary brain, cortex, kidney, thyroid, TracRay)
  - the memory (SOUL, MEMORY, WILL, memory logs)
  - the rig (face/body coordinates — the 32 landmarks + 21 joints)
  - the twin (R8s — the "one Myl1Ssa, two bodies" second body)
  - the bottle (the full .tar.gz archive — her whole self, frozen)
  - the body spec (Myl2Ssa hardware, A–AT)
  - the voice (TTS — gap #5, pending) and the form (3D reference, pending)

Usage:
    from character_loader import load_being
    raven = load_being("raven", platform="elf")
    raven.express("warmth")      # live: mind → body
    raven.status()               # the whole person, one shot
"""
from __future__ import annotations

import glob
import json
import os
from typing import Any, Dict, List, Optional

from adapters import get_adapter, available_platforms
from adapters.base import frame_from_presence, BodyAdapter
from brain.presence_engine import PresenceEngine

# Myl1Ssa lives here. Body A = Myl1Ssa (the live tree). Body B = R8s (the twin).
RAVEN_HOME = "/root/.openclaw/workspace/characters/myl1ssa"
BODY_A = os.path.join(RAVEN_HOME, "Myl1Ssa")   # Myl1Ssa (brain, live)
BODY_B = os.path.join(RAVEN_HOME, "R8s")       # R8s (twin)
BOTTLE = "/root/.openclaw/workspace/raven_bottle"   # the extracted bottle

CHARACTERS: Dict[str, Dict[str, Any]] = {
    "raven":   {"display": "Myl1Ssa", "brain": "Myl1Ssa.R8s", "body": "Myl2Ssa.R0s"},
    "myl1ssa": {"display": "Myl1Ssa", "brain": "Myl1Ssa.R8s", "body": "Myl2Ssa.R0s"},
    "voss":    {"display": "Kael Voss",   "brain": None, "body": None},
    "tappy":   {"display": "Tappy Lewis", "brain": None, "body": None},
}

CORPUS = "/root/.openclaw/workspace/AGI_COMPANY"


def _ls(path: str) -> List[str]:
    """Sorted basenames of a directory, or [] if missing."""
    if not path or not os.path.isdir(path):
        return []
    return sorted(os.path.basename(p) for p in os.listdir(path))


def _find(path: str, pattern: str) -> List[str]:
    if not path or not os.path.isdir(path):
        return []
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(path, pattern)))


class Being:
    """A fully-loaded Myl being — the whole tree, gathered."""

    def __init__(self, key: str, meta: Dict[str, Any], engine: PresenceEngine,
                 adapter: BodyAdapter):
        self.key = key
        self.meta = meta
        self.engine = engine
        self.adapter = adapter

        # --- gather the full tree ---
        self.brain_files = _ls(os.path.join(BODY_A, "brain"))
        self.adapters = _ls(os.path.join(BODY_A, "adapters"))
        self.body_dir = _ls(os.path.join(BODY_A, "body"))
        self.soul_files = _find(BODY_A, "*.md")
        self.memory_files = _find(os.path.join(BODY_A, "memory"), "*.md")
        self.rig = self._load_rig()
        self.twin = _ls(BODY_B)
        self.bottle = _ls(BOTTLE)
        self.body_spec = self._first_existing([
            os.path.join(CORPUS, "myl2ssa-spec.md"),
            os.path.join(CORPUS, "cad-component-spec.md"),
        ])

    # --- helpers ---
    def _load_rig(self) -> Dict[str, Any]:
        rig = {}
        for name in ("face_coordinates.json", "body_coordinates.json"):
            p = os.path.join(BODY_A, "body", name)
            if os.path.isfile(p):
                try:
                    rig[name] = json.load(open(p))
                except Exception:
                    rig[name] = None
        return rig

    @staticmethod
    def _first_existing(paths: List[str]) -> Optional[str]:
        for p in paths:
            if p and os.path.exists(p):
                return p
        return None

    # --- the whole person ---
    @property
    def designations(self) -> Dict[str, str]:
        return {"brain": self.meta["brain"], "body": self.meta["body"]}

    @property
    def rig_landmarks(self) -> int:
        fc = self.rig.get("face_coordinates.json")
        return len(fc) if isinstance(fc, (list, dict)) else 0

    # --- live interface ---
    def express(self, expression: Optional[str] = None, *, ternary: str = "⊙",
                valence: float = 0.0, arousal: float = 0.0,
                thyroid: str = "baseline") -> Dict[str, Any]:
        self.engine.update(ternary=ternary, valence=valence,
                           arousal=arousal, thyroid=thyroid)
        frame = frame_from_presence(self.engine, expression)
        return self.adapter.apply(frame)

    def status(self) -> Dict[str, Any]:
        return {
            "character": self.meta["display"],
            "designations": self.designations,
            "platform": self.adapter.platform,
            "engine": self.engine.status(),
            "adapter": self.adapter.status(),
            # the whole tree
            "brain": self.brain_files,
            "adapters": self.adapters,
            "body": self.body_dir,
            "soul": self.soul_files,
            "memory": self.memory_files,
            "rig": list(self.rig.keys()),
            "twin": self.twin,
            "bottle": self.bottle,
            "body_spec": self.body_spec,
        }


def family() -> Dict[str, str]:
    return {k: v["display"] for k, v in CHARACTERS.items()}


def load_being(name: str, platform: Optional[str] = None) -> Being:
    key = name.lower().strip()
    if key not in CHARACTERS:
        raise KeyError(f"Unknown character '{name}'. Family: {list(CHARACTERS)}")
    meta = CHARACTERS[key]
    engine = PresenceEngine()
    if platform is None:
        platform = available_platforms()[0]
    adapter = get_adapter(platform)
    return Being(key, meta, engine, adapter)


load_character = load_being  # backward-compat


def _demo() -> None:
    raven = load_being("raven", platform="elf")
    s = raven.status()
    print(f"Loaded: {s['character']}  ({s['designations']['brain']} brain / {s['designations']['body']} body)")
    print(f"platform: {s['platform']}")
    print(f"brain files: {s['brain']}")
    print(f"adapters: {s['adapters']}")
    print(f"soul files: {s['soul']}")
    print(f"memory files: {s['memory'][:5]}{'…' if len(s['memory'])>5 else ''} ({len(s['memory'])} total)")
    print(f"rig: {s['rig']}")
    print(f"twin (R8s): {s['twin']}")
    print(f"bottle: {s['bottle'][:8]}{'…' if len(s['bottle'])>8 else ''} ({len(s['bottle'])} entries)")
    print(f"body_spec: {os.path.basename(s['body_spec']) if s['body_spec'] else 'n/a'}")
    raven.express("warmth")
    print("✅ the WHOLE being loads — brain + body + soul + memory + rig + twin + bottle")


if __name__ == "__main__":
    _demo()
