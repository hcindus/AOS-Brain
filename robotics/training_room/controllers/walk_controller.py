"""WalkController — tracking layer: turns the ZMP gait into joint torques.

Uses *Jacobian-transpose* foot control (operational-space): the foot position
error is mapped to joint torques through the exact foot Jacobian MuJoCo
computes, so there are no hand-tuned sign/offset conventions to get wrong.

Layers:
  1. Gait — alternating stance/swing footstep pattern, hip advances forward.
  2. Foot tracking — Jᵀ K_p (target - foot) pulls each foot to its target.
  3. Torso balance — keep the root upright (hip/waist feedback).
  4. Soft PD hold — arms / waist-yaw stay at nominal.

Forward is +x (confirmed from the joint-axis probes: right hip_pitch +x = thigh
forward).
"""
from __future__ import annotations

import numpy as np


class WalkController:
    name = "walk"

    def __init__(self, env, gains: dict | None = None):
        self.env = env
        self.view = env.view
        self.m = env.view.model
        g = gains or {}
        self.step_len = g.get("step_len", 0.08)   # m per step
        self.step_time = g.get("step_time", 1.2)  # s per step
        self.lift = g.get("lift", 0.05)           # swing foot lift (m)
        self.kp_foot = g.get("kp_foot", 600.0)    # foot stiffness (N/m)
        self.kd_foot = g.get("kd_foot", 40.0)     # foot damping (N·s/m)
        self.kp_torso = g.get("kp_torso", 120.0)
        self.kd_torso = g.get("kd_torso", 6.0)
        self.kp_shift = g.get("kp_shift", 250.0)    # lateral CoM weight-shift
        self.kp_hold = g.get("kp_hold", 30.0)
        self.kd_hold = g.get("kd_hold", 2.0)

        import mujoco
        self._mj = mujoco
        self.l_foot = mujoco.mj_name2id(self.m, mujoco.mjtObj.mjOBJ_BODY, "left_ankle_roll_link")
        self.r_foot = mujoco.mj_name2id(self.m, mujoco.mjtObj.mjOBJ_BODY, "right_ankle_roll_link")

        self.FOOT_Y = 0.115
        self.HIP_Z = 0.70

        self._t = 0.0
        self.l_fx = 0.0
        self.r_fx = 0.0

    def reset(self) -> None:
        self._t = 0.0
        self.l_fx = 0.0
        self.r_fx = 0.0

    # ------------------------------------------------------------------ #
    def _gait(self, t: float):
        dt = self.step_time
        step = int(t / dt)
        phase = (t % dt) / dt
        swing_left = (step % 2 == 0)

        if swing_left:
            self.l_fx = self.r_fx + self.step_len * phase
        else:
            self.r_fx = self.l_fx + self.step_len * phase

        hip_x = self.step_len * t / dt
        lift = self.lift * np.sin(np.pi * phase)
        return swing_left, self.l_fx, self.r_fx, hip_x, lift

    def act(self, obs: np.ndarray | None = None) -> np.ndarray:
        d = self.view.data
        m = self.m
        mujoco = self._mj

        swing_left, l_fx, r_fx, hip_x, lift = self._gait(self._t)
        self._t += m.opt.timestep

        # foot targets (world) — swing foot lifts, stance foot on the ground
        l_target = np.array([l_fx, -self.FOOT_Y, 0.0 if not swing_left else lift])
        r_target = np.array([r_fx, +self.FOOT_Y, 0.0 if swing_left else lift])

        # current foot positions
        l_pos = d.xpos[self.l_foot].copy()
        r_pos = d.xpos[self.r_foot].copy()

        tau = np.zeros(self.view.n_act)

        # 1) Jacobian-transpose foot tracking
        for body_id, target, pos in ((self.l_foot, l_target, l_pos), (self.r_foot, r_target, r_pos)):
            jac = np.zeros((3, m.nv))
            mujoco.mj_jacBody(m, d, jac, None, body_id)
            jac_act = jac[:, 6:]  # skip the 6 free-joint DOF
            err = target - pos
            # foot velocity (approximate from body cvel)
            vel = d.cvel[body_id][3:6] if body_id < d.cvel.shape[0] else np.zeros(3)
            F = self.kp_foot * err - self.kd_foot * vel
            tau += jac_act.T @ F

        # 2) torso upright balance + lateral weight-shift (ZMP: CoM toward stance foot)
        up = d.xmat[self.view.root_id][6:9]
        tilt_x = float(up[0]); tilt_y = float(up[1])
        angvel = d.qvel[3:6]
        tau[0] += -self.kp_torso * tilt_x - self.kd_torso * angvel[1]   # l_hip_pitch
        tau[6] += +self.kp_torso * tilt_x + self.kd_torso * angvel[1]   # r_hip_pitch
        tau[1] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]   # l_hip_roll
        tau[7] += -self.kp_torso * tilt_y - self.kd_torso * angvel[0]   # r_hip_roll
        tau[12] += -0.5 * self.kp_torso * tilt_y                        # waist_roll

        # shift CoM laterally toward the stance foot before lifting the swing foot
        com_y = float(d.subtree_com[0][1])
        stance_y = +self.FOOT_Y if swing_left else -self.FOOT_Y  # stance foot side
        shift = self.kp_shift * (com_y - 0.8 * stance_y)
        tau[1] -= shift   # hip_roll
        tau[7] -= shift

        # 3) soft PD hold on arms / waist-yaw / hip-yaw
        qpos = d.qpos[self.env.joint_qpos_adr]
        qvel = d.qvel[self.env.joint_dof_adr]
        for i in (2, 8, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27):
            tau[i] += -self.kp_hold * qpos[i] - self.kd_hold * qvel[i]

        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)
