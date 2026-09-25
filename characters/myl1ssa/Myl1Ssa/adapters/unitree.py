#!/usr/bin/env python3
"""
Unitree adapter — maps Raven's rig onto a Unitree humanoid (G1 / H1 / H2).

Unitree publishes open URDFs + ROS 2 SDKs, so this is the buildable physical
path. The axis remap + scale are done here; joint-angle output is scaffolded
for the IK stage (Pinocchio / Mink), which loads the robot URDF.

Coordinate remap → ROS REP-103 (X forward, Y left, Z up):
    Robot_X = Z,  Robot_Y = -X,  Robot_Z = Y
"""

from .base import BodyAdapter, AdapterFrame, register
from typing import Any, Dict

# Raven keypoint → Unitree joint (scaffold; exact joint names come from the URDF)
UNITREE_JOINT_MAP = {
    "pelvis": "base_link",
    "L_hip": "left_hip", "L_knee": "left_knee", "L_ankle": "left_ankle",
    "R_hip": "right_hip", "R_knee": "right_knee", "R_ankle": "right_ankle",
    "chest": "torso", "neck": "neck", "head": "head",
    "L_shoulder": "left_shoulder", "L_elbow": "left_elbow", "L_wrist": "left_wrist",
    "R_shoulder": "right_shoulder", "R_elbow": "right_elbow", "R_wrist": "right_wrist",
}

# Approximate scale factors (robot height / Raven's 169 cm)
ROBOT_SCALE = {
    "g1": 1.30 / 1.69,   # ≈ 0.77
    "h1": 1.71 / 1.69,   # ≈ 1.01
    "h2": 1.71 / 1.69,
}


def to_robot(p: Dict[str, float]) -> Dict[str, float]:
    return {"x": p["z"], "y": -p["x"], "z": p["y"]}


class UnitreeAdapter(BodyAdapter):
    platform = "unitree"

    def __init__(self, model: str = "g1"):
        self.model = model.lower()
        self.scale = ROBOT_SCALE.get(self.model, 1.0)
        # register distinct platforms per model (unitree, unitree_h1, …)
        if self.model != "g1":
            self.platform = f"unitree_{self.model}"

    def apply(self, frame: AdapterFrame) -> Dict[str, Any]:
        # remap + scale body points to the robot frame
        body = {k: {axis: v * self.scale for axis, v in to_robot(p).items()}
                for k, p in frame.body_points.items()}

        # map keypoints → robot joints (joint-angle solve is the IK stage)
        joints = {}
        for kp, joint in UNITREE_JOINT_MAP.items():
            if kp in body:
                joints[joint] = body[kp]

        return {
            "target": f"unitree_{self.model}",
            "scale_factor": round(self.scale, 3),
            "frame": "ROS REP-103 (X forward, Y left, Z up)",
            "expression": frame.expression,
            "posture": frame.posture,
            "body_points": body,
            "joint_targets": joints,
            "ik_note": "joint angles require the URDF + Pinocchio/Mink IK solve (next stage)",
        }

    def status(self) -> Dict[str, Any]:
        return {
            "platform": self.platform,
            "model": self.model,
            "scale_factor": round(self.scale, 3),
            "frame": "ROS REP-103",
            "open_sdk": True,
            "ik": "pending URDF load (Pinocchio/Mink)",
        }


register(UnitreeAdapter())
register(UnitreeAdapter("h1"))
