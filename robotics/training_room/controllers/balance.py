"""BalanceController — torso-upright feedback on a PD hold (best static-stand result).

The empirically-best *static* stand for the RP1: hold every joint at nominal
with soft PD, plus actively drive the hips/waist from the root's tilt so the
torso stays upright. ~35% upright — beats the naive `hold` (29%).

A LIPM ankle strategy (CoP control) was tested and *rejected*: it regressed to
~8% upright. Root cause is physical — the RP1's feet are four tiny contact
points (±5.7° ankle roll), so the ankle has almost no CoP leverage. Ankle
strategy trades "stays up longer" for "leans more", which is not standing.

The conclusion this encodes: the RP1 cannot balance *statically*. It must
*step* to widen its support — the ZMP / footstep planner is the walking layer
that sits on top of this.

Joint axes: hip_pitch is mirrored (L +y / R -y), so a symmetric correction
needs opposite-sign torque across the legs; hip_roll shares +x and takes the
same sign.
"""
from __future__ import annotations

import numpy as np


class BalanceController:
    name = "balance"

    def __init__(self, env, gains: dict | None = None):
        self.env = env
        self.view = env.view
        g = gains or {}
        self.kp_joint = g.get("kp_joint", 60.0)   # base PD hold (all joints)
        self.kd_joint = g.get("kd_joint", 4.0)
        self.kp_torso = g.get("kp_torso", 120.0)  # torso-upright feedback
        self.kd_torso = g.get("kd_torso", 6.0)

        self.idx = {
            "l_hip_pitch": 0, "l_hip_roll": 1, "l_knee": 3,
            "l_ankle_pitch": 4, "l_ankle_roll": 5,
            "r_hip_pitch": 6, "r_hip_roll": 7, "r_knee": 9,
            "r_ankle_pitch": 10, "r_ankle_roll": 11,
            "waist_roll": 12,
        }

    def reset(self) -> None:
        pass

    def act(self, obs: np.ndarray | None = None) -> np.ndarray:
        d = self.view.data
        m = self.view.model

        up = d.xmat[self.view.root_id][6:9]
        tilt_x = float(up[0])
        tilt_y = float(up[1])
        angvel = d.qvel[3:6]

        qpos = d.qpos[self.env.joint_qpos_adr]
        qvel = d.qvel[self.env.joint_dof_adr]
        tau = -self.kp_joint * qpos - self.kd_joint * qvel

        # torso-upright feedback — hip_pitch mirrored, hip_roll same-sign
        tau[self.idx["l_hip_pitch"]] += -self.kp_torso * tilt_x - self.kd_torso * angvel[1]
        tau[self.idx["r_hip_pitch"]] += +self.kp_torso * tilt_x + self.kd_torso * angvel[1]
        tau[self.idx["l_hip_roll"]] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]
        tau[self.idx["r_hip_roll"]] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]
        tau[self.idx["waist_roll"]] += -0.5 * self.kp_torso * tilt_y

        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)
