"""Reference motion loader — RP1-retargeted mocap (LaFAN via UFO-MotionData).

The UFO repo already retargeted human motion capture onto the RP1's joint space,
so `dof_pos` here IS RP1 joint angles (24-DoF config: legs + waist + arms, with
single-DoF wrists). This module loads those clips and maps our skills to the
matching reference motions — the reference data motion-imitation tracks against.

Data: xuewang/UFO-MotionData (HuggingFace) → rp1_24dof_lafan_v7.pkl
  55 motions, 50 Hz, keys per motion: dof_pos, dof_vel, root_quat,
  root_trans_offset, joint_names, body_names, fps, robot_name.
"""
from __future__ import annotations

import os

import joblib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PKL = os.path.join(HERE, "ufo", "rp1_24dof_lafan_v7.pkl")

# skill -> reference motion key (and a list of alternates)
SKILL_TO_MOTION = {
    "walk": "walk1_subject1",
    "run": "run1_subject2",
    "sprint": "sprint1_subject2",
    "jump": "jumps1_subject1",
    "getup": "fallAndGetUp1_subject1",
    "roll": "ground1_subject1",
    "recover": "pushAndStumble1_subject2",
    "balance": "walk1_subject1",
    "crawl": "ground2_subject2",
    "squat": "multipleActions1_subject1",
    "kneel": "ground1_subject4",
    "sit": "ground2_subject3",
    "climb": "walk2_subject1",
    "swim": "fightAndSports1_subject1",
    "sit_stand": "fallAndGetUp2_subject2",
    "kneel_stand": "fallAndGetUp3_subject1",
}

_MOTIONS = None

# our RP1 MJCF's 28 revolute joints, in actuator order
ROBOT_JOINTS = [
    "left_hip_pitch_joint", "left_hip_roll_joint", "left_hip_yaw_joint", "left_knee_joint",
    "left_ankle_pitch_joint", "left_ankle_roll_joint",
    "right_hip_pitch_joint", "right_hip_roll_joint", "right_hip_yaw_joint", "right_knee_joint",
    "right_ankle_pitch_joint", "right_ankle_roll_joint",
    "waist_roll_joint", "waist_yaw_joint",
    "left_shoulder_pitch_joint", "left_shoulder_roll_joint", "left_shoulder_yaw_joint",
    "left_elbow_joint", "left_wrist_roll_joint", "left_wrist_yaw_joint", "left_wrist_pitch_joint",
    "right_shoulder_pitch_joint", "right_shoulder_roll_joint", "right_shoulder_yaw_joint",
    "right_elbow_joint", "right_wrist_roll_joint", "right_wrist_yaw_joint", "right_wrist_pitch_joint",
]


def ref_to_robot(skill: str):
    """Return (ref_dof_28 [T,28], fps) — the reference mapped onto our 28-DoF robot.

    The reference is 24-DoF (single wrist joint); we map each reference joint to
    its robot index by name, collapsing the single wrist onto wrist_pitch and
    leaving wrist_roll/yaw at zero.
    """
    ref = get_reference(skill)
    ref_dof = ref["dof_pos"]          # [T, 24]
    ref_joints = ref["joint_names"]   # 24 names
    fps = ref["fps"]
    mapping = []
    for jn in ref_joints:
        if jn == "left_wrist_joint":
            mapping.append(ROBOT_JOINTS.index("left_wrist_pitch_joint"))
        elif jn == "right_wrist_joint":
            mapping.append(ROBOT_JOINTS.index("right_wrist_pitch_joint"))
        else:
            mapping.append(ROBOT_JOINTS.index(jn))
    ref_dof_28 = np.zeros((len(ref_dof), len(ROBOT_JOINTS)), dtype=np.float32)
    for i, ri in enumerate(mapping):
        ref_dof_28[:, ri] = ref_dof[:, i]
    return ref_dof_28, fps


def ref_root(skill: str):
    """Return (root_pos [T,3], root_quat_wxyz [T,4], fps) for the root (free-joint) pose.

    The reference stores root_quat in xyzw order; our MuJoCo free joint uses
    wxyz, so we reorder. root_trans_offset is already (x, y, z) in a Z-up frame.
    """
    ref = get_reference(skill)
    root_pos = ref["root_trans_offset"]            # [T,3] xyz
    q = ref["root_quat"]                           # [T,4] xyzw
    root_quat_wxyz = np.stack([q[:, 3], q[:, 0], q[:, 1], q[:, 2]], axis=1)
    return root_pos, root_quat_wxyz, ref["fps"]


def motions():
    global _MOTIONS
    if _MOTIONS is None:
        _MOTIONS = joblib.load(PKL)
    return _MOTIONS


def motion_keys() -> list:
    return list(motions().keys())


def get_reference(skill: str) -> dict:
    """Return the reference motion dict for a skill (dof_pos, fps, joint_names, …)."""
    key = SKILL_TO_MOTION.get(skill)
    if key is None:
        raise KeyError(f"no reference motion mapped for skill '{skill}'")
    return motions()[key]


if __name__ == "__main__":
    m = get_reference("walk")
    print("walk reference:", m["motion_key"], "| dof_pos", m["dof_pos"].shape, "| fps", m["fps"])
    print("joints:", len(m["joint_names"]), "| duration", round(m["dof_pos"].shape[0] / m["fps"], 1), "s")
    print()
    print("available motions (%d):" % len(motions()))
    for k in sorted(motions()):
        print("  ", k)
