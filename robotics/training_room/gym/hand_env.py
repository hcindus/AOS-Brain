"""HandGymEnv — a grasp-focused gym for the RP1 hand model.

robot_hand.xml is underactuated: 40 actuators (28 body + 12 finger) but 50
revolute joints — the 10 extra finger joints are tendon-coupled (passive).
The body env (RP1GymEnv) assumes 1:1 actuation, so the hand needs its own env.

Observation = body state + the 40 ACTUATED joint qpos/qvel (not all 50 joints).
Action = 40 torques. Reward = grasp: curl the fingers toward a target grasp
pose while keeping the body upright (the hand trains *on* a standing body).

The grasp task is "reach a target finger configuration" — there's no object in
the MJCF, so closing the fingers to a defined grasp pose is the tractable task,
analogous to the reference-tracking skills (PD toward a target, learn residual).
"""
from __future__ import annotations

import os

import numpy as np

from .loader import load, ModelView

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAND_MJCF = os.path.join(ROOT, "..", "rp1", "RP1_description", "mjcf", "robot_hand.xml")

# finger actuator indices (28..39) and their joint qpos addresses
FINGER_ACT = list(range(28, 40))

# a canonical "grasp" pose: curl each finger toward its max flexion (0..~1.4 rad)
# left then right (6 per hand, matching the actuator order).
GRASP_TARGET = np.array([
    1.2, 1.0,   # lh thumb (2 segments)
    1.1, 1.1, 1.1, 1.1,  # lh index/middle/ring/pinky
    1.2, 1.0,   # rh thumb
    1.1, 1.1, 1.1, 1.1,  # rh fingers
])


class HandGymEnv:
    def __init__(self, mjcf_path: str | None = None, horizon: int = 500,
                 seed: int | None = None):
        self.view: ModelView = load(mjcf_path or HAND_MJCF)
        self.horizon = horizon
        self.rng = np.random.default_rng(seed)

        m = self.view.model
        self.n_act = m.nu                      # 40
        # actuated joint qpos/qvel addresses (via transmission), not all joints
        self.act_qpos_adr = [int(m.jnt_qposadr[m.actuator_trnid[i, 0]]) for i in range(m.nu)]
        self.act_dof_adr = [int(m.jnt_dofadr[m.actuator_trnid[i, 0]]) for i in range(m.nu)]

        # nominal standing pose (all joints 0, root at 0.78)
        self.nominal_qpos = np.zeros(m.nq)
        self.nominal_qpos[2] = 0.78

        self._t = 0
        self._obs_dim = 1 + 4 + 3 + 3 + 2 * m.nu

    @property
    def obs_dim(self) -> int:
        return self._obs_dim

    def reset(self, qpos_noise: float = 0.0) -> np.ndarray:
        import mujoco
        self.view.data = type(self.view.data)(self.view.model)
        d = self.view.data
        mujoco.mj_resetData(self.view.model, d)
        d.qpos[:] = self.nominal_qpos.copy()
        if qpos_noise > 0:
            d.qpos[self.act_qpos_adr] += self.rng.uniform(-qpos_noise, qpos_noise, size=self.n_act)
        mujoco.mj_forward(self.view.model, d)
        self._t = 0
        return self._observe()

    def step(self, action: np.ndarray):
        import mujoco
        d = self.view.data
        m = self.view.model
        action = np.asarray(action, dtype=np.float64)
        d.ctrl[:] = np.clip(action, m.actuator_ctrlrange[:, 0], m.actuator_ctrlrange[:, 1])
        mujoco.mj_step(m, d)
        self._t += 1
        obs = self._observe()
        reward = self._reward(action)
        done = self._done() or self._t >= self.horizon
        info = {"alive": self._alive(), "upright": self._upright(), "grasp_err": self._grasp_err()}
        return obs, reward, done, info

    def _observe(self) -> np.ndarray:
        d = self.view.data
        root_id = self.view.root_id
        height = d.xpos[root_id][2]
        quat = d.xquat[root_id].copy()
        vel = d.qvel[0:3].copy()
        angvel = d.qvel[3:6].copy()
        qpos = d.qpos[self.act_qpos_adr].copy()
        qvel = d.qvel[self.act_dof_adr].copy()
        return np.concatenate([[height], quat, vel, angvel, qpos, qvel])

    def _alive(self) -> bool:
        return self.view.data.xpos[self.view.root_id][2] > 0.45

    def _upright(self) -> bool:
        z = self.view.data.xmat[self.view.root_id][6:9]
        return float(z[2]) > 0.5

    def _finger_qpos(self) -> np.ndarray:
        d = self.view.data
        # finger actuators 28..39 -> their joint qpos (via act_qpos_adr)
        return d.qpos[[self.act_qpos_adr[i] for i in FINGER_ACT]]

    def _grasp_err(self) -> float:
        return float(np.mean((self._finger_qpos() - GRASP_TARGET) ** 2))

    def _reward(self, action: np.ndarray) -> float:
        alive = 1.0 if self._alive() else 0.0
        upright = 1.0 if self._upright() else 0.0
        # grasp: close fingers to target (negative mean squared error)
        grasp = -self._grasp_err()
        energy = float(np.mean(np.square(action))) * 1e-4
        return alive * upright * (1.0 + grasp) - energy

    def _done(self) -> bool:
        return not (self._alive() and self._upright())


if __name__ == "__main__":
    env = HandGymEnv()
    obs = env.reset()
    print(f"obs_dim={env.obs_dim} (expected {1+4+3+3+2*40})")
    print(f"obs len={len(obs)}  n_act={env.n_act}")
    # run a few steps with a naive curl-fingers torque
    for _ in range(10):
        act = np.zeros(env.n_act)
        act[28:40] = 5.0  # curl fingers
        obs, r, done, info = env.step(act)
        if done:
            break
    print(f"grasp_err after curl={info['grasp_err']:.3f}  alive={info['alive']}  reward={r:.3f}")
    print("HandGymEnv self-test OK")
