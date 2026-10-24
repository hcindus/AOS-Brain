"""GetUpController — stand up from lying prone on the ground.

The hardest rung: the body starts face-down on the floor and must rise to
standing. The base controller scripts a rough "push up → tuck → stand" sequence
by driving the arms (shoulder extension to push the torso off the ground), the
hips (bring the legs under), and the knees (extend to stand). The learned
residual + height reward then tune this crude motion into an actual get-up.

This is a warm start, not a solved skill — true get-up is the one rung that
really wants motion-imitation data or heavy RL. The script gives the learner
something to climb from.
"""
from __future__ import annotations

import numpy as np


class GetUpController:
    name = "getup"

    def __init__(self, env, gains: dict | None = None):
        self.env = env
        self.view = env.view
        g = gains or {}
        self.kp = g.get("kp", 100.0)
        self.kd = g.get("kd", 4.0)
        self.kp_torso = g.get("kp_torso", 120.0)
        self.kd_torso = g.get("kd_torso", 6.0)
        self.T = g.get("T", 3.0)  # seconds for the get-up sequence

        self.idx = {
            "l_hip_pitch": 0, "l_knee": 3, "l_ankle_pitch": 4,
            "r_hip_pitch": 6, "r_knee": 9, "r_ankle_pitch": 10,
            "waist_roll": 12, "waist_yaw": 13,
            "l_shoulder_pitch": 14, "r_shoulder_pitch": 23,
        }
        self._t = 0.0
        self.dt = env.view.model.opt.timestep

    def reset(self) -> None:
        self._t = 0.0

    def _targets(self, t: float) -> dict:
        """Rough time-based get-up targets (angles in rad, generic convention)."""
        if t < self.T / 3:
            # phase 1: push up — arms extend (push torso off the ground)
            p = t / (self.T / 3)
            return {"shoulder": -1.5 * p, "hip": 0.0, "knee": 0.0}
        elif t < 2 * self.T / 3:
            # phase 2: tuck — bring legs under (hip + knee flex)
            p = (t - self.T / 3) / (self.T / 3)
            return {"shoulder": -1.5, "hip": 0.8 * p, "knee": 1.0 * p}
        else:
            # phase 3: stand — extend knees + hips to zero
            p = (t - 2 * self.T / 3) / (self.T / 3)
            return {"shoulder": -1.5 * (1 - p), "hip": 0.8 * (1 - p), "knee": 1.0 * (1 - p)}

    def act(self, obs: np.ndarray | None = None) -> np.ndarray:
        d = self.view.data
        m = self.view.model

        tgt = self._targets(self._t)
        self._t += self.dt

        qpos = d.qpos[self.env.joint_qpos_adr]
        qvel = d.qvel[self.env.joint_dof_adr]
        tau = np.zeros(self.view.n_act)

        # arms push (shoulder pitch) — mirrored
        tau[self.idx["l_shoulder_pitch"]] += -self.kp * (qpos[self.idx["l_shoulder_pitch"]] - tgt["shoulder"]) - self.kd * qvel[self.idx["l_shoulder_pitch"]]
        tau[self.idx["r_shoulder_pitch"]] += -self.kp * (qpos[self.idx["r_shoulder_pitch"]] - (-tgt["shoulder"])) - self.kd * qvel[self.idx["r_shoulder_pitch"]]

        # hips (bring legs under) — mirrored
        tau[self.idx["l_hip_pitch"]] += -self.kp * (qpos[self.idx["l_hip_pitch"]] - (+tgt["hip"])) - self.kd * qvel[self.idx["l_hip_pitch"]]
        tau[self.idx["r_hip_pitch"]] += -self.kp * (qpos[self.idx["r_hip_pitch"]] - (-tgt["hip"])) - self.kd * qvel[self.idx["r_hip_pitch"]]

        # knees (tuck then stand) — mirrored
        tau[self.idx["l_knee"]] += -self.kp * (qpos[self.idx["l_knee"]] - (-tgt["knee"])) - self.kd * qvel[self.idx["l_knee"]]
        tau[self.idx["r_knee"]] += -self.kp * (qpos[self.idx["r_knee"]] - (+tgt["knee"])) - self.kd * qvel[self.idx["r_knee"]]

        # torso upright balance (helps once partially up)
        up = d.xmat[self.view.root_id][6:9]
        tilt_x = float(up[0]); tilt_y = float(up[1])
        angvel = d.qvel[3:6]
        tau[self.idx["l_hip_pitch"]] += -self.kp_torso * tilt_x - self.kd_torso * angvel[1]
        tau[self.idx["r_hip_pitch"]] += +self.kp_torso * tilt_x + self.kd_torso * angvel[1]
        tau[self.idx["waist_roll"]] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]

        # hold ankles + waist_yaw + remaining arms at nominal
        for i in range(self.view.n_act):
            if i not in (0, 3, 6, 9, 12, 14, 23):
                tau[i] += -30.0 * qpos[i] - 2.0 * qvel[i]

        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)
