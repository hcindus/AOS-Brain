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
}

_MOTIONS = None


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
