"""RollController — roll the body over on the ground.

A roll is a rotation about the body's longitudinal axis while lying down — the
natural predecessor to get-up (roll over, then rise). The base controller
drives a periodic asymmetric arm swing + hip roll to build angular momentum and
tip the body over. The roll reward (accumulated roll angle) then tells the
learned residual how to make it a clean, sustained roll.

Like get-up, this is a hard dynamic skill — the base is a warm start, not a
solved controller.
"""
from __future__ import annotations

import numpy as np


class RollController:
    name = "roll"

    def __init__(self, env, gains: dict | None = None):
        self.env = env
        self.view = env.view
        g = gains or {}
        self.kp = g.get("kp", 80.0)
        self.kd = g.get("kd", 4.0)
        self.period = g.get("period", 2.0)
        self.amp = g.get("amp", 1.5)   # arm swing amplitude

        self.idx = {
            "l_shoulder_pitch": 14, "r_shoulder_pitch": 23,
            "l_hip_roll": 1, "r_hip_roll": 7,
            "l_shoulder_roll": 15, "r_shoulder_roll": 24,
        }
        self._t = 0.0
        self.dt = env.view.model.opt.timestep

    def reset(self) -> None:
        self._t = 0.0

    def act(self, obs: np.ndarray | None = None) -> np.ndarray:
        d = self.view.data
        m = self.view.model
        qpos = d.qpos[self.env.joint_qpos_adr]
        qvel = d.qvel[self.env.joint_dof_adr]

        # periodic asymmetric swing (drive the arms + hips to roll the body)
        swing = self.amp * np.sin(2.0 * np.pi * self._t / self.period)
        self._t += self.dt

        tau = np.zeros(self.view.n_act)

        # arms swing together (both to one side then the other) — shoulder roll
        tau[self.idx["l_shoulder_roll"]] += -self.kp * (qpos[self.idx["l_shoulder_roll"]] - swing) - self.kd * qvel[self.idx["l_shoulder_roll"]]
        tau[self.idx["r_shoulder_roll"]] += -self.kp * (qpos[self.idx["r_shoulder_roll"]] - swing) - self.kd * qvel[self.idx["r_shoulder_roll"]]
        # arms pitch to add momentum
        tau[self.idx["l_shoulder_pitch"]] += -self.kp * (qpos[self.idx["l_shoulder_pitch"]] - swing) - self.kd * qvel[self.idx["l_shoulder_pitch"]]
        tau[self.idx["r_shoulder_pitch"]] += -self.kp * (qpos[self.idx["r_shoulder_pitch"]] - (-swing)) - self.kd * qvel[self.idx["r_shoulder_pitch"]]

        # hips roll to shift weight
        tau[self.idx["l_hip_roll"]] += -self.kp * (qpos[self.idx["l_hip_roll"]] - 0.5 * swing) - self.kd * qvel[self.idx["l_hip_roll"]]
        tau[self.idx["r_hip_roll"]] += -self.kp * (qpos[self.idx["r_hip_roll"]] - 0.5 * swing) - self.kd * qvel[self.idx["r_hip_roll"]]

        # hold the rest at nominal
        for i in range(self.view.n_act):
            if i not in (1, 7, 14, 15, 23, 24):
                tau[i] += -30.0 * qpos[i] - 2.0 * qvel[i]

        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)
