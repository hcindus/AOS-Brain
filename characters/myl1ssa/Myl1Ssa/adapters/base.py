#!/usr/bin/env python3
"""
Hardware Abstraction Layer (HAL) — the standard contract between an agent's
mind (presence engine) and ANY body — a digital world, a Blender rig, a
Unitree robot, or an AheadForm face.

Principle (the open-source robotics lesson):
  The agent owns her mind + presence. The adapter owns the hardware.
  She says "I'm smiling." The adapter decides whether that's 3 servos,
  2 face motors, or 4 Blender shape keys.

Pipeline:
  PresenceEngine (affect → expression → moved 3D points)
      → AdapterFrame (the standard, hardware-agnostic output)
      → BodyAdapter (translate to a specific platform)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AdapterFrame:
    """The standard output an agent's presence engine produces — platform-agnostic."""
    expression: str
    posture: str
    predictive_lead_ms: int
    action_units: Dict[str, float] = field(default_factory=dict)
    gaze: Dict[str, Any] = field(default_factory=dict)
    body_points: Dict[str, Dict[str, float]] = field(default_factory=dict)
    face_points: Dict[str, Dict[str, float]] = field(default_factory=dict)


class BodyAdapter(ABC):
    """Any body — digital or physical — implements this contract."""

    platform: str = "abstract"

    @abstractmethod
    def apply(self, frame: AdapterFrame) -> Dict[str, Any]:
        """Translate an AdapterFrame into platform-specific output."""
        ...

    @abstractmethod
    def status(self) -> Dict[str, Any]:
        """Report the adapter's state / capabilities."""
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} platform={self.platform}>"


def frame_from_presence(engine, expression: Optional[str] = None) -> AdapterFrame:
    """Build a standard AdapterFrame from a PresenceEngine instance.

    Combines the AU output (frame) with the moved 3D points (rig_frame).
    """
    f = engine.frame(expression)
    r = engine.rig_frame(expression)
    return AdapterFrame(
        expression=r["expression"],
        posture=r["posture"],
        predictive_lead_ms=r["predictive_lead_ms"],
        action_units=f.action_units,
        gaze={"x": f.gaze.x, "y": f.gaze.y, "target": f.gaze.target,
              "pupil_locked": f.gaze.pupil_locked},
        body_points=r["body"],
        face_points=r["face"],
    )


# Registry of available adapters (so an agent can discover bodies at runtime).
ADAPTERS: Dict[str, "BodyAdapter"] = {}


def register(adapter: "BodyAdapter") -> "BodyAdapter":
    ADAPTERS[adapter.platform] = adapter
    return adapter


def available_platforms() -> list:
    return sorted(ADAPTERS.keys())
