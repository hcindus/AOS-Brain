#!/usr/bin/env python3
"""
RP1 adapter — maps the agent's mind onto the RoboParty RP1 (28-DoF) body.

This is the seam where Myl1Ssa (brain) meets Myl2Ssa (body). It implements the
same `BodyAdapter` contract as the other bodies, so `load_character("raven",
platform="rp1")` drives the RP1 the same way it drives the Elf face or a
Unitree. Two channels:

  expression  — body_points / posture / AU map onto the upper-body joint set.
  motion      — frame.motion {intent, velocity} is handed to the locomotion
                controller (BalanceController / walking controller) which emits
                the 28 joint torques. This is the missing "motion verb".

The controller lives in `robotics/training_room/`; it is attached lazily so
this adapter has no hard dependency on the sim.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from .base import BodyAdapter, AdapterFrame, register

# Raven keypoint → RP1 joint group (the RP1 has no neck/head articulation;
# the head is fixed, expressions live in the face rig, not here).
RP1_JOINT_MAP = {
    "L_ankle": ["left_ankle_pitch_joint", "left_ankle_roll_joint"],
    "L_knee": ["left_knee_joint"],
    "L_hip": ["left_hip_pitch_joint", "left_hip_roll_joint", "left_hip_yaw_joint"],
    "R_ankle": ["right_ankle_pitch_joint", "right_ankle_roll_joint"],
    "R_knee": ["right_knee_joint"],
    "R_hip": ["right_hip_pitch_joint", "right_hip_roll_joint", "right_hip_yaw_joint"],
    "pelvis": ["waist_roll_joint", "waist_yaw_joint"],
    "L_shoulder": ["left_shoulder_pitch_joint", "left_shoulder_roll_joint", "left_shoulder_yaw_joint"],
    "L_elbow": ["left_elbow_joint"],
    "L_wrist": ["left_wrist_roll_joint", "left_wrist_yaw_joint", "left_wrist_pitch_joint"],
    "R_shoulder": ["right_shoulder_pitch_joint", "right_shoulder_roll_joint", "right_shoulder_yaw_joint"],
    "R_elbow": ["right_elbow_joint"],
    "R_wrist": ["right_wrist_roll_joint", "right_wrist_yaw_joint", "right_wrist_pitch_joint"],
}


class RP1Adapter(BodyAdapter):
    platform = "rp1"

    def __init__(self):
        self._controller = None  # locomotion controller, attached lazily

    def attach_controller(self, controller) -> None:
        """Bind the locomotion controller (BalanceController / walker)."""
        self._controller = controller

    def apply(self, frame: AdapterFrame) -> Dict[str, Any]:
        # 1) expression channel — body_points → upper-body joint targets
        joint_targets: Dict[str, float] = {}
        for kp, joints in RP1_JOINT_MAP.items():
            if kp in frame.body_points:
                for j in joints:
                    # scalar placeholder: take the point's magnitude (IK refines)
                    p = frame.body_points[kp]
                    joint_targets[j] = round(
                        (p.get("x", 0.0) ** 2 + p.get("y", 0.0) ** 2 + p.get("z", 0.0) ** 2) ** 0.5, 4
                    )

        # 2) motion channel — intent → controller torques
        torques = None
        motion = frame.motion or {}
        if motion and self._controller is not None:
            # the controller reads full state from its live env; intent selects
            # the mode (stand/walk/turn) for controllers that support it.
            torques = self._controller.act()
            if hasattr(torques, "tolist"):
                torques = [round(float(t), 4) for t in torques]

        return {
            "target": "rp1",
            "frame": "RP1 (28 DoF, torque-controlled)",
            "expression": frame.expression,
            "posture": frame.posture,
            "joint_targets": joint_targets,
            "motion_intent": motion.get("intent"),
            "torques": torques,
            "ik_note": "joint angles require the RP1 URDF + IK (Pinocchio/Mink) — scaffold",
        }

    def status(self) -> Dict[str, Any]:
        return {
            "platform": self.platform,
            "dof": 28,
            "controller": type(self._controller).__name__ if self._controller else None,
            "expression_channel": bool(RP1_JOINT_MAP),
            "motion_channel": self._controller is not None,
            "ik": "pending URDF load",
        }


register(RP1Adapter())
