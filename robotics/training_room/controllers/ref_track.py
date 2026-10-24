"""ReferenceTrackingController — PD-track a retargeted reference motion.

The "mimic a human" base controller: kinematically sets the root (free joint) to
the reference's root pose and PD-drives the joints toward the reference
trajectory. The learned residual then refines the dynamics mismatch, and the
tracking reward measures how closely the combined controller matches.

Each episode samples a random window of the (long) reference clip so a rollout
covers a meaningful motion segment, not just the standing preamble.
"""
from __future__ import annotations

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "motion_data"))
from reference import ref_to_robot, ref_root


class ReferenceTrackingController:
    name = "ref_track"

    def __init__(self, env, skill: str, kp: float = 60.0, kd: float = 4.0,
                 window_s: float = 4.0, seed: int = 0):
        self.env = env
        self.view = env.view
        self.kp = kp
        self.kd = kd
        self.ref_dof_28, self.fps = ref_to_robot(skill)
        self.root_pos, self.root_quat_wxyz, _ = ref_root(skill)
        self.rng = np.random.default_rng(seed)
        self.window = int(window_s * self.fps)
        self._t = 0.0
        self._offset = 0
        self.dt = env.view.model.opt.timestep

    def reset(self) -> None:
        self._t = 0.0
        # random window into the reference (leave room for the full window)
        hi = max(1, len(self.ref_dof_28) - self.window)
        self._offset = int(self.rng.integers(0, hi))

    def act(self, obs: np.ndarray | None = None) -> np.ndarray:
        d = self.view.data
        m = self.view.model
        frame = min(self._offset + int(self._t * self.fps), len(self.ref_dof_28) - 1)
        # kinematic root: set the free joint to the reference's root pose
        d.qpos[0:3] = self.root_pos[frame]
        d.qpos[3:7] = self.root_quat_wxyz[frame]
        d.qvel[0:6] = 0.0  # zero root velocity (kinematic)
        ref_q = self.ref_dof_28[frame]
        self._t += self.dt

        qpos = d.qpos[self.env.joint_qpos_adr]
        qvel = d.qvel[self.env.joint_dof_adr]
        tau = -self.kp * (qpos - ref_q) - self.kd * qvel
        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)
