"""JumpController — the "jump" rung (crouch → explosive extension → land).

A jump is a squat with an *explosive* return: crouch to load the legs, then
rapidly extend the knees/hips/ankles so the momentum lifts the body off the
ground. The learned residual (with a height reward) tunes the extension to be
explosive enough to actually leave the ground — and to survive the landing.

Same joint structure and mirroring as SquatController (knee & hip_pitch are
mirrored across the legs; ankle_pitch shares its axis).
"""
from __future__ import annotations

import numpy as np


class JumpController:
    name = "jump"

    def __init__(self, env, gains: dict | None = None):
        self.env = env
        self.view = env.view
        g = gains or {}
        self.kp_joint = g.get("kp_joint", 40.0)
        self.kd_joint = g.get("kd_joint", 2.0)
        self.kp_torso = g.get("kp_torso", 120.0)
        self.kd_torso = g.get("kd_torso", 6.0)
        self.crouch = g.get("crouch", 1.2)       # max knee flexion (rad)
        self.period = g.get("period", 1.6)       # crouch + jump + land cycle (s)
        self.kp_leg = g.get("kp_leg", 160.0)     # strong leg tracking (for the explode)
        self.kd_leg = g.get("kd_leg", 4.0)

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
        """Asymmetric trajectory: slow crouch (0..0.5), fast explode (0.5..0.7),
        then a rest window (0.7..1.0) to land and re-settle."""
        p = (t % self.period) / self.period
        if p < 0.5:                       # crouch
            k = self.crouch * (p / 0.5)
        elif p < 0.7:                     # explosive extension
            k = self.crouch * max(0.0, 1.0 - (p - 0.5) / 0.2)
        else:                             # land / settle
            k = 0.0
        return k, 0.3 * k  # (knee flexion, hip bend)

    def act(self, obs: np.ndarray | None = None) -> np.ndarray:
        d = self.view.data
        m = self.view.model

        up = d.xmat[self.view.root_id][6:9]
        tilt_x = float(up[0]); tilt_y = float(up[1])
        angvel = d.qvel[3:6]
        qpos = d.qpos[self.env.joint_qpos_adr]
        qvel = d.qvel[self.env.joint_dof_adr]

        knee, hip = self._ref(self._t)
        self._t += self.dt

        tau = np.zeros(self.view.n_act)

        # leg trajectory (mirrored): knee flex negative-left / positive-right
        tau[self.idx["l_knee"]] += -self.kp_leg * (qpos[self.idx["l_knee"]] - (-knee)) - self.kd_leg * qvel[self.idx["l_knee"]]
        tau[self.idx["r_knee"]] += -self.kp_leg * (qpos[self.idx["r_knee"]] - (+knee)) - self.kd_leg * qvel[self.idx["r_knee"]]
        tau[self.idx["l_hip_pitch"]] += -self.kp_leg * (qpos[self.idx["l_hip_pitch"]] - (+hip)) - self.kd_leg * qvel[self.idx["l_hip_pitch"]]
        tau[self.idx["r_hip_pitch"]] += -self.kp_leg * (qpos[self.idx["r_hip_pitch"]] - (-hip)) - self.kd_leg * qvel[self.idx["r_hip_pitch"]]

        # ankle extends (plantar-flex) to push off — track a slight extension
        tau[self.idx["l_ankle_pitch"]] += -self.kp_leg * (qpos[self.idx["l_ankle_pitch"]] - (-0.4 * knee)) - self.kd_leg * qvel[self.idx["l_ankle_pitch"]]
        tau[self.idx["r_ankle_pitch"]] += -self.kp_leg * (qpos[self.idx["r_ankle_pitch"]] - (-0.4 * knee)) - self.kd_leg * qvel[self.idx["r_ankle_pitch"]]

        # torso upright balance
        tau[self.idx["l_hip_pitch"]] += -self.kp_torso * tilt_x - self.kd_torso * angvel[1]
        tau[self.idx["r_hip_pitch"]] += +self.kp_torso * tilt_x + self.kd_torso * angvel[1]
        tau[self.idx["l_hip_roll"]] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]
        tau[self.idx["r_hip_roll"]] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]
        tau[self.idx["waist_roll"]] += -0.5 * self.kp_torso * tilt_y

        # hold arms / waist-yaw / hip-yaw / ankle-roll at nominal
        for i in range(self.view.n_act):
            if i not in (0, 1, 3, 4, 6, 7, 9, 10, 12):
                tau[i] += -self.kp_joint * qpos[i] - self.kd_joint * qvel[i]

        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)
