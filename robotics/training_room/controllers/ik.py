"""Leg inverse kinematics — map a foot position (relative to the hip) to joint angles.

The RP1 leg is a 3-DoF hip + 1-DoF knee + 2-DoF ankle. For sagittal walking we
solve the 2-link thigh/shin chain (hip_pitch, knee, ankle_pitch); lateral (roll)
is handled by the balance controller.

Geometry (measured from the MJCF at nominal pose):
  thigh  L1 = 0.356 m  (hip → knee)
  shin   L2 = 0.308 m  (knee → ankle)

The foot target is expressed relative to the hip joint in world frame (z up).
"""
from __future__ import annotations

import numpy as np

L1 = 0.356   # thigh
L2 = 0.308   # shin


def sagittal_ik(fx: float, fz: float) -> tuple[float, float, float]:
    """Solve hip_pitch, knee, ankle_pitch for a foot at (fx, fz) relative to hip.

    Returns angles in radians. Conventions match the RP1's *left* leg:
      hip_pitch  — thigh angle from straight-down (+ = thigh forward)
      knee       — bend (0 = straight, + = flexed)
      ankle_pitch — foot angle relative to shin (0 = foot ⊥ shin)
    """
    fx = float(fx)
    fz = float(fz)  # negative below hip
    d = np.hypot(fx, fz)
    d = min(d, L1 + L2 - 1e-4)  # clamp to reachable

    # knee bend (interior): law of cosines
    cos_k = (d * d - L1 * L1 - L2 * L2) / (2.0 * L1 * L2)
    cos_k = float(np.clip(cos_k, -1.0, 1.0))
    knee = np.arccos(cos_k)  # bend angle (positive = flexed)

    # hip: angle of the foot vector from straight-down, minus the thigh offset
    alpha = np.arctan2(fx, -fz)               # foot direction from vertical-down
    beta = np.arctan2(L2 * np.sin(knee), L1 + L2 * np.cos(knee))
    hip_pitch = alpha - beta

    # ankle: keep the foot flat (foot ⊥ world up) → ankle = -(hip_pitch + knee)
    ankle_pitch = -(hip_pitch + knee)

    return hip_pitch, knee, ankle_pitch


def sagittal_fk(hip_pitch: float, knee: float) -> tuple[float, float]:
    """Forward kinematics — foot position relative to hip, given hip_pitch & knee."""
    a = hip_pitch
    b = knee
    fx = L1 * np.sin(a) + L2 * np.sin(a + b)
    fz = -(L1 * np.cos(a) + L2 * np.cos(a + b))
    return fx, fz
