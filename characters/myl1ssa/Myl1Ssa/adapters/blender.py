#!/usr/bin/env python3
"""
Blender adapter — drives Raven's rig inside Blender.

Converts the moved points into Blender's right-handed frame
(X right, Y forward, Z up) and emits them as armature/empty-ready data,
plus the skeleton topology for building an armature via bpy.

Coordinate remap (from the original foot-midpoint map):
    Blender_X = X,  Blender_Y = Z,  Blender_Z = Y
"""

from .base import BodyAdapter, AdapterFrame, register
from typing import Any, Dict


def to_blender(p: Dict[str, float]) -> Dict[str, float]:
    return {"x": p["x"], "y": p["z"], "z": p["y"]}


class BlenderAdapter(BodyAdapter):
    platform = "blender"

    def __init__(self, units: str = "cm"):
        self.units = units

    def apply(self, frame: AdapterFrame) -> Dict[str, Any]:
        body = {k: to_blender(v) for k, v in frame.body_points.items()}
        face = {k: to_blender(v) for k, v in frame.face_points.items()}
        return {
            "target": "blender",
            "units": self.units,
            "note": "scale 0.01 for meters; import as empties or build an armature",
            "expression": frame.expression,
            "posture": frame.posture,
            "body": body,
            "face": face,
            "bpy_hint": (
                "for k, v in data['body'].items(): "
                "bpy.ops.object.empty_add(location=(v['x']/100, v['y']/100, v['z']/100))"
            ),
        }

    def status(self) -> Dict[str, Any]:
        return {
            "platform": self.platform,
            "frame": "right-handed (X right, Y forward, Z up)",
            "units": self.units,
        }


register(BlenderAdapter())
