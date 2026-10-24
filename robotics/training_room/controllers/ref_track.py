"""ReferenceTrackingController — PD-track a retargeted reference motion.

The "mimic a human" base controller: drives the joints toward the reference
trajectory (RP1-retargeted mocap) with a PD law. The learned residual then
refines this to account for the sim-to-real / dynamics mismatch, and the
tracking reward measures how closely the combined controller matches the
reference. This is the motion-imitation path.

The reference advances at its own fps (50 Hz) while the sim runs at 500 Hz, so
the frame index is interpolated from the sim clock.
"""
from __future__ import annotations

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "motion_data"))
from reference import ref_to_robot


class ReferenceTrackingController:
    name = "ref_track"

    def __init__(self, env, skill: str, kp: float = 60.0, kd: float = 4.0):
        self.env = env
        self.view = env.view
        self.kp = kp
        self.kd = kd
        self.ref_dof_28, self.fps = ref_to_robot(skill)
        self._t = 0.0
        self.dt = env.view.model.opt.timestep

    def reset(self) -> None:
        self._t = 0.0

    def act(self, obs: np.ndarray | None = None) -> np.ndarray:
        d = self.view.data
        m = self.view.model
        frame = min(int(self._t * self.fps), len(self.ref_dof_28) - 1)
        ref_q = self.ref_dof_28[frame]
        self._t += self.dt

        qpos = d.qpos[self.env.joint_qpos_adr]
        qvel = d.qvel[self.env.joint_dof_adr]
        tau = -self.kp * (qpos - ref_q) - self.kd * qvel
        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)
