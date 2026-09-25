#!/usr/bin/env python3
"""
Adapters — the Hardware Abstraction Layer for the agent family.

An agent's presence engine outputs a hardware-agnostic AdapterFrame; these
adapters translate it onto a specific body (digital world, Blender, Unitree).

Usage:
    from adapters import get_adapter, available_platforms
    from presence_engine import PresenceEngine
    from adapters.base import frame_from_presence

    engine = PresenceEngine()
    frame = frame_from_presence(engine, "warmth")

    unitree = get_adapter("unitree")     # or "unitree_h1", "blender", "digital_world"
    print(unitree.apply(frame))
"""

from .base import (AdapterFrame, BodyAdapter, frame_from_presence,
                   ADAPTERS, register, available_platforms)
from . import digital_world  # noqa: F401  (registers itself)
from . import blender        # noqa: F401
from . import unitree        # noqa: F401


def get_adapter(platform: str) -> BodyAdapter:
    """Return a registered adapter by platform id (e.g. 'unitree', 'unitree_h1', 'blender')."""
    if platform in ADAPTERS:
        return ADAPTERS[platform]
    # try prefix match (unitree_h1 → unitree with model h1)
    raise KeyError(f"No adapter '{platform}'. Available: {available_platforms()}")


__all__ = [
    "AdapterFrame", "BodyAdapter", "frame_from_presence",
    "get_adapter", "available_platforms", "register", "ADAPTERS",
]
