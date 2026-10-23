"""SquatController — the "squat and don't fall" rung (keystone of the curriculum).

A squat is a controlled vertical CoM motion: bend the knees + hips to lower the
center of mass, then extend back to standing — all while keeping the torso
upright and the CoM over the feet. It's the shared primitive behind get-up,
pick-up, and half of walking.

Implementation: the balance controller's torso-upright feedback, but with a
*time-varying* knee reference (a periodic squat) instead of holding the knees
at zero. As the knees flex, the CoM drops; the torso feedback keeps it upright
so it doesn't topple.

Joint axes: knee is mirrored (L -y / R +y), so the two knees flex with opposite
signs. hip_pitch is also mirrored (L +y / R -y).
"""
from __future__ import annotations

import numpy as np


class SquatController:
    name = "squat"

    def __init__(self, env, gains: dict | None = None):
        self.env = env
        self.view = env.view
        g = gains or {}
        self.kp_joint = g.get("kp_joint", 60.0)
        self.kd_joint = g.get("kd_joint", 4.0)
        self.kp_torso = g.get("kp_torso", 120.0)
        self.kd_torso = g.get("kd_torso", 6.0)
        # squat trajectory
        self.knee_flex = g.get("knee_flex", 1.0)   # max knee flexion (rad)
        self.hip_bend = g.get("hip_bend", 0.5)     # max hip pitch compensation (rad)
        self.period = g.get("period", 2.0)         # seconds per full squat cycle
        self.kp_knee = g.get("kp_knee", 120.0)
        self.kd_knee = g.get("kd_knee", 6.0)

        self.idx = {
            "l_hip_pitch": 0, "l_knee": 3, "l_ankle_pitch": 4,
            "r_hip_pitch": 6, "r_knee": 9, "r_ankle_pitch": 10,
            "l_hip_roll": 1, "r_hip_roll": 7, "waist_roll": 12,
        }
        self._t = 0.0
        self.dt = env.view.model.opt.timestep

    def reset(self) -> None:
        self._t = 0.0

    def _ref(self, t: float) -> tuple[float, float]:
        """Return (knee_flex, hip_bend) at time t — a periodic squat cycle."""
        phi = 0.5 - 0.5 * np.cos(2.0 * np.pi * t / self.period)  # 0 -> 1 -> 0
        return self.knee_flex * phi, self.hip_bend * phi

    def act(self, obs: np.ndarray | None = None) -> np.ndarray:
        d = self.view.data
        m = self.view.model

        up = d.xmat[self.view.root_id][6:9]
        tilt_x = float(up[0])
        tilt_y = float(up[1])
        angvel = d.qvel[3:6]
        qpos = d.qpos[self.env.joint_qpos_adr]
        qvel = d.qvel[self.env.joint_dof_adr]

        knee_flex, hip_bend = self._ref(self._t)
        self._t += self.dt

        # start from zero — the squat drives the legs, not a generic hold
        tau = np.zeros(self.view.n_act)

        # knee trajectory — mirrored: left knee flexes negative, right positive
        tau[self.idx["l_knee"]] += -self.kp_knee * (qpos[self.idx["l_knee"]] - (-knee_flex)) - self.kd_knee * qvel[self.idx["l_knee"]]
        tau[self.idx["r_knee"]] += -self.kp_knee * (qpos[self.idx["r_knee"]] - (+knee_flex)) - self.kd_knee * qvel[self.idx["r_knee"]]

        # hip pitch compensation (keep torso upright as CoM drops) — mirrored
        tau[self.idx["l_hip_pitch"]] += -self.kp_knee * (qpos[self.idx["l_hip_pitch"]] - (+hip_bend)) - self.kd_knee * qvel[self.idx["l_hip_pitch"]]
        tau[self.idx["r_hip_pitch"]] += -self.kp_knee * (qpos[self.idx["r_hip_pitch"]] - (-hip_bend)) - self.kd_knee * qvel[self.idx["r_hip_pitch"]]

        # ankle pitch — keep feet flat / CoM over feet while knees bend
        tau[self.idx["l_ankle_pitch"]] += -self.kp_knee * (qpos[self.idx["l_ankle_pitch"]] - (+0.3 * knee_flex)) - self.kd_knee * qvel[self.idx["l_ankle_pitch"]]
        tau[self.idx["r_ankle_pitch"]] += -self.kp_knee * (qpos[self.idx["r_ankle_pitch"]] - (+0.3 * knee_flex)) - self.kd_knee * qvel[self.idx["r_ankle_pitch"]]

        # torso upright feedback (same as balance)
        tau[self.idx["l_hip_pitch"]] += -self.kp_torso * tilt_x - self.kd_torso * angvel[1]
        tau[self.idx["r_hip_pitch"]] += +self.kp_torso * tilt_x + self.kd_torso * angvel[1]
        tau[self.idx["l_hip_roll"]] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]
        tau[self.idx["r_hip_roll"]] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]
        tau[self.idx["waist_roll"]] += -0.5 * self.kp_torso * tilt_y

        # hold the rest (arms, waist-yaw, hip-yaw, ankle-roll) at nominal
        for i in range(self.view.n_act):
            if i not in (0, 1, 3, 4, 6, 7, 9, 10, 12):
                tau[i] += -self.kp_joint * qpos[i] - self.kd_joint * qvel[i]

        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)
