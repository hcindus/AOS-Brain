"""RP1GymEnv — the sim sandbox a pilot trains/evals in.

A minimal, dependency-light MuJoCo gym wrapper. The action space is 28
torques (N·m). The observation is a compact vector a policy can consume:

    [root_height, root_quat(4), root_vel(3), root_angvel(3), qpos(28), qvel(28)]

Reward is the "stand and walk" task: stay alive + upright, move forward,
and don't thrash (energy penalty).
"""
from __future__ import annotations

import numpy as np

from .loader import ModelView, load


class RP1GymEnv:
    def __init__(
        self,
        mjcf_path: str | None = None,
        horizon: int = 1000,
        alive_height: float = 0.45,
        upright_tol: float = 0.5,
        seed: int | None = None,
    ):
        self.view: ModelView = load(mjcf_path)
        self.horizon = horizon
        self.alive_height = alive_height
        self.upright_tol = upright_tol
        self.rng = np.random.default_rng(seed)

        m = self.view.model
        self.n_act = m.nu
        self.n_q = m.nq
        self.n_v = m.nv
        # revolute joint qpos/qvel offsets (after the 7-DoF free joint)
        self.joint_qpos_adr = m.jnt_qposadr[1:]  # skip free joint
        self.joint_dof_adr = m.jnt_dofadr[1:]
        # nominal standing pose = all revolute joints at 0
        self.nominal_qpos = np.zeros(self.n_q)
        self.nominal_qpos[2] = 0.78  # root height baked into base_link pos

        self._t = 0
        self._obs_dim = 1 + 4 + 3 + 3 + 2 * m.nu

    # ------------------------------------------------------------------ #
    @property
    def obs_dim(self) -> int:
        return self._obs_dim

    def reset(self, qpos_noise: float = 0.0) -> np.ndarray:
        self.view.data = type(self.view.data)(self.view.model)  # fresh data
        d = self.view.data
        mujoco = __import__("mujoco")
        mujoco.mj_resetData(self.view.model, d)
        # set nominal standing pose
        qpos0 = self.nominal_qpos.copy()
        if qpos_noise > 0:
            qpos0[self.joint_qpos_adr] += self.rng.uniform(
                -qpos_noise, qpos_noise, size=len(self.joint_qpos_adr)
            )
        d.qpos[:] = qpos0
        mujoco.mj_forward(self.view.model, d)
        self._t = 0
        return self._observe()

    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, dict]:
        d = self.view.data
        mujoco = __import__("mujoco")
        action = np.asarray(action, dtype=np.float64)
        d.ctrl[:] = np.clip(action, self.view.model.actuator_ctrlrange[:, 0],
                            self.view.model.actuator_ctrlrange[:, 1])
        mujoco.mj_step(self.view.model, d)
        self._t += 1

        obs = self._observe()
        reward = self._reward(action)
        done = self._done() or self._t >= self.horizon
        info = {
            "alive": self._alive(),
            "upright": self._upright(),
            "progress": float(d.qpos[0]),
            "energy": float(np.sum(np.square(action))),
        }
        return obs, reward, done, info

    # ------------------------------------------------------------------ #
    def _observe(self) -> np.ndarray:
        d = self.view.data
        m = self.view.model
        root_id = self.view.root_id
        height = d.xpos[root_id][2]
        quat = d.xquat[root_id].copy()          # w x y z
        vel = d.qvel[0:3].copy()
        angvel = d.qvel[3:6].copy()
        qpos = d.qpos[self.joint_qpos_adr].copy()
        qvel = d.qvel[self.joint_dof_adr].copy()
        return np.concatenate([[height], quat, vel, angvel, qpos, qvel])

    def _alive(self) -> bool:
        d = self.view.data
        return d.xpos[self.view.root_id][2] > self.alive_height

    def _upright(self) -> bool:
        d = self.view.data
        # torso local +z should stay close to world +z (dot > tol)
        z_torso = d.xmat[self.view.root_id][6:9]
        return float(z_torso[2]) > self.upright_tol

    def _done(self) -> bool:
        return not (self._alive() and self._upright())

    def _reward(self, action: np.ndarray) -> float:
        d = self.view.data
        alive = 1.0 if self._alive() else 0.0
        upright = 1.0 if self._upright() else 0.0
        # forward progress in +x this step
        progress = float(d.qpos[0] - self._last_x) if hasattr(self, "_last_x") else 0.0
        self._last_x = float(d.qpos[0])
        energy = float(np.mean(np.square(action))) * 1e-4
        return alive * upright + 0.05 * progress - energy
