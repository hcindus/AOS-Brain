"""BalanceController — keep the RP1 upright via torso feedback on top of a PD hold.

The empirically-validated recipe (see the sign sweep): hold every joint at its
nominal pose with soft PD, *plus* actively drive the hips and waist from the
root's tilt so the torso stays upright. This is the "keep the torso upright on
purpose" fix the Asimov-1 video identifies as the difference between a puppet
and a walker — a naive PD hold resists, but this one actively corrects.

Joint axes (from the MJCF) matter here: `hip_pitch` is mirrored across the
legs (left +y, right -y), so a symmetric correction needs opposite sign torque
left vs right. hip_roll / ankle_roll / ankle_pitch share their axis across the
legs, so they take the same sign.
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

        # actuator indices (joint order of the 28-DoF model)
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

        # --- torso orientation (root's local +z in world) ---
        up = d.xmat[self.view.root_id][6:9]
        tilt_x = float(up[0])          # forward/backward lean
        tilt_y = float(up[1])          # lateral lean
        angvel = d.qvel[3:6]           # root angular velocity

        # --- base PD hold: drive every joint to its nominal (0) pose ---
        qpos = d.qpos[self.env.joint_qpos_adr]
        qvel = d.qvel[self.env.joint_dof_adr]
        tau = -self.kp_joint * qpos - self.kd_joint * qvel

        # --- torso-upright feedback on top ---
        # hip_pitch is mirrored (L +y / R -y): opposite sign across legs.
        tau[self.idx["l_hip_pitch"]] += -self.kp_torso * tilt_x - self.kd_torso * angvel[1]
        tau[self.idx["r_hip_pitch"]] += +self.kp_torso * tilt_x + self.kd_torso * angvel[1]
        # hip_roll / waist_roll share the +x axis: same sign across legs.
        tau[self.idx["l_hip_roll"]] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]
        tau[self.idx["r_hip_roll"]] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]
        tau[self.idx["waist_roll"]] += -0.5 * self.kp_torso * tilt_y

        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)
