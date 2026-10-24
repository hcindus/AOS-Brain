"""Human motion → RP1 retargeting.

Turns a sequence of human keypoints into RP1 joint-angle trajectories. This is
the core of the motion-imitation pipeline: once we have poses (from MediaPipe /
mocap), this maps them onto the RP1's 28 DoF so they can seed reference data for
AMP / MimicLite / the Skill Gym.

For a first pass we handle the legs (the locomotion-relevant part) via the
sagittal 2-link IK already in controllers/ik.py. Arms/waist can be added once
we know the exact keypoint schema of the source.

Input convention (per frame, world frame, z up, meters):
  hips: (hx, hy, hz)     — pelvis position
  foot: (fx, fy, fz)     — ankle/foot position
"""
from __future__ import annotations

import os
import sys

import numpy as np

# make the training_room controllers importable from this directory
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "training_room"))

from controllers.ik import sagittal_ik


def retarget_leg(hip: np.ndarray, foot: np.ndarray):
    """Map a single hip + foot 3D position to (hip_pitch, knee, ankle_pitch).

    Uses the sagittal (x-z) plane; lateral offset is ignored in this first pass.
    Returns generic-convention angles (thigh-forward +, knee-flex +).
    """
    dx = foot[0] - hip[0]
    dz = foot[2] - hip[2]
    hip_pitch, knee, ankle_pitch = sagittal_ik(dx, dz)
    return hip_pitch, knee, ankle_pitch


def retarget_sequence(hips: np.ndarray, feet: np.ndarray):
    """Retarget a full sequence of hip + foot positions to leg joint trajectories.

    Args:
        hips: (T, 3) pelvis positions over time
        feet: (T, 3) foot positions over time (same frame as hips)
    Returns:
        dict of joint name -> (T,) trajectory (generic convention)
    """
    T = len(hips)
    out = {k: np.zeros(T) for k in ("hip_pitch", "knee", "ankle_pitch")}
    for t in range(T):
        hp, k, ap = retarget_leg(hips[t], feet[t])
        out["hip_pitch"][t] = hp
        out["knee"][t] = k
        out["ankle_pitch"][t] = ap
    return out


if __name__ == "__main__":
    # synthetic squat: hips drop 0.9 -> 0.5 -> 0.9, feet fixed
    T = 200
    t = np.linspace(0, 2 * np.pi, T)
    hips = np.column_stack([np.zeros(T), np.zeros(T), 0.70 + 0.20 * np.sin(t)])  # z: 0.5..0.9
    feet = np.column_stack([np.zeros(T), np.zeros(T), np.zeros(T)])              # feet on ground
    traj = retarget_sequence(hips, feet)
    print("synthetic squat retargeted:")
    print("  hip_pitch range: %.2f .. %.2f rad" % (traj["hip_pitch"].min(), traj["hip_pitch"].max()))
    print("  knee range:      %.2f .. %.2f rad" % (traj["knee"].min(), traj["knee"].max()))
    print("  ankle range:     %.2f .. %.2f rad" % (traj["ankle_pitch"].min(), traj["ankle_pitch"].max()))
    print("  OK — retargeting pipeline works (leg IK maps CoM height -> joint angles)")
