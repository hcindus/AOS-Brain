#!/usr/bin/env python3
"""
Digital World adapter — renders an agent as a point-cloud skeleton for any
game engine (Three.js, Godot, a custom canvas renderer, etc.).

This is the "digital version / world" layer: no hardware needed, the agent
exists and moves as points + connections in a virtual space. The physical
adapters (Unitree, AheadForm) later map the same AdapterFrame onto motors.

Output is a portable JSON: points (merged body+face) + skeleton connections
+ expression/posture metadata — any renderer can draw it.
"""

from .base import BodyAdapter, AdapterFrame, register
from typing import Any, Dict, List

# Skeleton topology — which points connect to which (stick-figure bones).
BODY_CONNECTIONS: List[List[str]] = [
    ["L_ankle", "L_knee"], ["L_knee", "L_hip"], ["L_hip", "pelvis"],
    ["R_ankle", "R_knee"], ["R_knee", "R_hip"], ["R_hip", "pelvis"],
    ["pelvis", "waist"], ["waist", "chest"], ["chest", "neck"], ["neck", "head"],
    ["chest", "L_shoulder"], ["L_shoulder", "L_elbow"], ["L_elbow", "L_wrist"],
    ["chest", "R_shoulder"], ["R_shoulder", "R_elbow"], ["R_elbow", "R_wrist"],
]

FACE_CONNECTIONS: List[List[str]] = [
    ["top_head", "forehead"], ["forehead", "nose_bridge"], ["nose_bridge", "nose_tip"],
    ["nose_bridge", "L_eye_inner"], ["L_eye_inner", "L_pupil"], ["L_pupil", "L_eye_outer"],
    ["nose_bridge", "R_eye_inner"], ["R_eye_inner", "R_pupil"], ["R_pupil", "R_eye_outer"],
    ["L_brow_outer", "L_brow_arch"], ["L_brow_arch", "L_brow_inner"],
    ["R_brow_inner", "R_brow_arch"], ["R_brow_arch", "R_brow_outer"],
    ["nose_tip", "L_nostril"], ["nose_tip", "R_nostril"],
    ["upper_lip", "mouth_center"], ["mouth_center", "lower_lip"],
    ["mouth_center", "L_mouth_corner"], ["mouth_center", "R_mouth_corner"],
    ["L_mouth_corner", "L_jaw"], ["R_mouth_corner", "R_jaw"],
    ["L_jaw", "chin"], ["R_jaw", "chin"],
    ["L_cheek", "L_mouth_corner"], ["R_cheek", "R_mouth_corner"],
]


class DigitalWorldAdapter(BodyAdapter):
    """Point-cloud render target — the agent as movable points + lines in a world."""

    platform = "digital_world"

    def __init__(self, world: str = "default"):
        self.world = world

    def apply(self, frame: AdapterFrame) -> Dict[str, Any]:
        # merge body + face points, with a namespace prefix to avoid collisions
        points: Dict[str, Any] = {}
        for k, v in frame.body_points.items():
            points[f"body:{k}"] = [v["x"], v["y"], v["z"]]
        for k, v in frame.face_points.items():
            points[f"face:{k}"] = [v["x"], v["y"], v["z"]]

        # translate skeleton connections to the namespaced keys
        connections: List[List[str]] = []
        for a, b in BODY_CONNECTIONS:
            connections.append([f"body:{a}", f"body:{b}"])
        for a, b in FACE_CONNECTIONS:
            connections.append([f"face:{a}", f"face:{b}"])

        return {
            "world": self.world,
            "character": "Myl1Ssa.R8s",
            "expression": frame.expression,
            "posture": frame.posture,
            "predictive_lead_ms": frame.predictive_lead_ms,
            "gaze": frame.gaze,
            "points": points,
            "connections": connections,
        }

    def status(self) -> Dict[str, Any]:
        return {
            "platform": self.platform,
            "world": self.world,
            "render": "point-cloud + skeleton lines",
            "targets": ["three.js", "godot", "custom canvas"],
        }


register(DigitalWorldAdapter())
