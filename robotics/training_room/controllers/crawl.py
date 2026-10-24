"""CrawlController — quadrupedal crawl on hands and knees.

Crawling is *more* stable than bipedal walking (four points of contact instead
of two), so it's a good intermediate locomotion rung. The base controller holds
a deep hands-and-knees pose and drives an alternating limb gait (opposite arm +
leg move together). The forward reward pushes the learned residual to make it
a clean, forward crawl.

Crude warm start — the alternating gait is scripted, the refinement is learned.
"""
from __future__ import annotations

import numpy as np


class CrawlController:
    name = "crawl"

    def __init__(self, env, gains: dict | None = None):
        self.env = env
        self.view = env.view
        g = gains or {}
        self.kp = g.get("kp", 100.0)
        self.kd = g.get("kd", 5.0)
        self.period = g.get("period", 1.0)   # s per crawl cycle
        self.crouch = g.get("crouch", 1.2)   # deep knee flexion (hands-and-knees)

        self.idx = {
            "l_hip_pitch": 0, "l_knee": 3, "l_hip_roll": 1,
            "r_hip_pitch": 6, "r_knee": 9, "r_hip_roll": 7,
            "l_shoulder_pitch": 14, "r_shoulder_pitch": 23,
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

        # alternating gait: left arm + right leg move together, then swap
        ph = 2.0 * np.pi * self._t / self.period
        s1 = np.sin(ph)   # left arm / right leg phase
        s2 = -s1          # right arm / left leg (opposite)
        self._t += self.dt

        tau = np.zeros(self.view.n_act)

        # arms reach forward (alternating) — shoulder pitch
        tau[self.idx["l_shoulder_pitch"]] += -self.kp * (qpos[self.idx["l_shoulder_pitch"]] - (-0.8 - 0.4 * s1)) - self.kd * qvel[self.idx["l_shoulder_pitch"]]
        tau[self.idx["r_shoulder_pitch"]] += -self.kp * (qpos[self.idx["r_shoulder_pitch"]] - (-0.8 - 0.4 * s2)) - self.kd * qvel[self.idx["r_shoulder_pitch"]]

        # legs flexed (hands-and-knees) + alternating forward reach (hip pitch)
        tau[self.idx["l_hip_pitch"]] += -self.kp * (qpos[self.idx["l_hip_pitch"]] - (-self.crouch + 0.3 * s1)) - self.kd * qvel[self.idx["l_hip_pitch"]]
        tau[self.idx["r_hip_pitch"]] += -self.kp * (qpos[self.idx["r_hip_pitch"]] - (self.crouch - 0.3 * s2)) - self.kd * qvel[self.idx["r_hip_pitch"]]

        # knees flexed (deep crouch)
        tau[self.idx["l_knee"]] += -self.kp * (qpos[self.idx["l_knee"]] - (self.crouch * 0.8)) - self.kd * qvel[self.idx["l_knee"]]
        tau[self.idx["r_knee"]] += -self.kp * (qpos[self.idx["r_knee"]] - (-self.crouch * 0.8)) - self.kd * qvel[self.idx["r_knee"]]

        # hold the rest at nominal
        for i in range(self.view.n_act):
            if i not in (0, 3, 6, 9, 14, 23):
                tau[i] += -30.0 * qpos[i] - 2.0 * qvel[i]

        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)
