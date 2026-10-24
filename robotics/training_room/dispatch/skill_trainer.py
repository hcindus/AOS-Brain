"""SkillTrainer — train each skill (walk/stand/squat) *in its own lane*.

The "skill + train on top" architecture:

    combined_torque(obs) = base_controller(env) + residual(obs)

  - base_controller is the hand-built model-based skill (walk / balance / squat).
  - residual is a *small learned* additive torque (linear, obs -> 28), trained by
    an evolution strategy to maximize a dense per-skill reward.

Each trainer owns two MuJoCo envs and two threads:
  - train thread   — ES loop, evolves the residual W, updates reward history.
  - display thread — continuously rolls out the current W (live body positions).

Reward (dense, per-step) is skill-specific via `forward_weight`:
  reward_step = alive * (1 + forward_weight * forward_velocity * 20)
"""
from __future__ import annotations

import threading
import time

import numpy as np

from gym import RP1GymEnv


class SkillTrainer:
    def __init__(self, name: str, base_factory, forward_weight: float = 1.0,
                 height_weight: float = 0.0, roll_weight: float = 0.0,
                 mjcf_path: str | None = None,
                 residual_clip: float = 15.0, popsize: int = 12, sigma: float = 0.3,
                 lr: float = 0.05, steps: int = 300, seed: int = 0,
                 push_interval: int | None = None, push_force: float = 0.0,
                 start_crouch: bool = False, start_lying: bool = False,
                 shared: list | None = None):
        self.name = name
        self.forward_weight = forward_weight
        self.height_weight = height_weight
        self.roll_weight = roll_weight
        self.residual_clip = residual_clip
        self.shared = shared or []   # list of higher-tier SkillTrainers to inherit from
        self.popsize = popsize
        self.sigma = sigma
        self.lr = lr
        self.steps = steps
        self.push_interval = push_interval   # apply a lateral push every N steps
        self.push_force = push_force          # lateral force (N)
        self.start_crouch = start_crouch      # begin each episode crouched (get-up)
        self.start_lying = start_lying        # begin lying prone on the ground

        # two envs: one for training rollouts, one for the live display
        self.train_env = RP1GymEnv(mjcf_path=mjcf_path)
        self.disp_env = RP1GymEnv(mjcf_path=mjcf_path)
        self.base_train = base_factory(self.train_env)
        self.base_disp = base_factory(self.disp_env)

        self.obs_dim = self.train_env.obs_dim
        self.n_act = self.train_env.n_act
        self.rng = np.random.default_rng(seed)

        self.lock = threading.Lock()
        self.W = np.zeros((self.n_act, self.obs_dim))
        self.gen = 0
        self.mean_r = 0.0
        self.max_r = 0.0
        self.history: list = []
        self.live: dict = {"alive": True, "bodies": [], "height": 0.78, "reward": 0.0}

    # ------------------------------------------------------------------ #
    def _reset(self, env):
        obs = env.reset(qpos_noise=0.02)
        if self.start_lying:
            d = env.view.data
            d.qpos[2] = 0.30                          # body low, near ground
            d.qpos[3:7] = [0.7071, 0.0, -0.7071, 0.0]  # prone (face down, -90° about y)
            d.qpos[env.joint_qpos_adr[3]] = -0.5      # knees slightly flexed
            d.qpos[env.joint_qpos_adr[9]] = +0.5
            import mujoco
            mujoco.mj_forward(env.view.model, d)
            obs = env._observe()
        elif self.start_crouch:
            d = env.view.data
            d.qpos[env.joint_qpos_adr[3]] = -1.3   # left knee flex (deep crouch)
            d.qpos[env.joint_qpos_adr[9]] = +1.3   # right knee flex (deep crouch)
            d.qpos[env.joint_qpos_adr[0]] = +0.5   # l hip pitch (lean forward to stay over feet)
            d.qpos[env.joint_qpos_adr[6]] = -0.5   # r hip pitch
            import mujoco
            mujoco.mj_forward(env.view.model, d)
            obs = env._observe()
        return obs

    def _maybe_push(self, env, t):
        d = env.view.data
        if self.push_interval and t % self.push_interval == 0:
            d.xfrc_applied[env.view.root_id, 1] = self.push_force  # lateral +y shove
        else:
            d.xfrc_applied[env.view.root_id, 1] = 0.0

    # ------------------------------------------------------------------ #
    def _shared_W(self) -> np.ndarray:
        """The combined inherited knowledge from all higher-tier trainers (or zero)."""
        if not self.shared:
            return np.zeros((self.n_act, self.obs_dim))
        W = np.zeros((self.n_act, self.obs_dim))
        for src in self.shared:
            with src.lock:
                W += src.W.copy()
        return W

    def _rollout(self, env, base, W) -> float:
        base.reset()
        obs = self._reset(env)
        total = 0.0
        prev_x = 0.0
        prev_z = float(obs[0])
        prev_roll = self._roll_angle(env)
        shared_W = self._shared_W()
        done = False
        t = 0
        while not done and t < self.steps:
            self._maybe_push(env, t)
            resid = np.clip((W + shared_W) @ obs, -self.residual_clip, self.residual_clip)
            obs, r, done, info = env.step(base.act(obs) + resid)
            fwd = info["progress"] - prev_x
            prev_x = info["progress"]
            up = float(obs[0]) - prev_z
            prev_z = float(obs[0])
            roll = self._roll_angle(env)
            droll = abs(roll - prev_roll)
            prev_roll = roll
            total += float(info["alive"]) * (
                1.0 + self.forward_weight * fwd * 20.0 + self.height_weight * up * 20.0 + self.roll_weight * droll * 10.0
            )
            t += 1
        return total

    def _roll_angle(self, env) -> float:
        """Body roll angle (rotation about the longitudinal axis) from the free-joint quat."""
        d = env.view.data
        qw, qx, qy, qz = d.qpos[3:7]
        import math
        return math.atan2(2.0 * (qw * qx + qy * qz), 1.0 - 2.0 * (qx * qx + qy * qy))

    # ------------------------------------------------------------------ #
    def _train(self):
        while True:
            eps = self.rng.standard_normal((self.popsize, self.n_act, self.obs_dim))
            rewards = np.zeros(self.popsize)
            for i in range(self.popsize):
                rewards[i] = self._rollout(self.train_env, self.base_train, self.W + self.sigma * eps[i])
            A = (rewards - rewards.mean()) / (rewards.std() + 1e-8)
            with self.lock:
                self.W += (self.lr / (self.popsize * self.sigma)) * np.einsum("i,ijk->jk", A, eps)
                self.gen += 1
                self.mean_r = float(rewards.mean())
                self.max_r = float(rewards.max())
                self.history.append([self.gen, self.mean_r, self.max_r])
                if len(self.history) > 500:
                    self.history = self.history[-500:]

    def _display(self):
        while True:
            with self.lock:
                W = self.W.copy()
            shared_W = self._shared_W()
            self.base_disp.reset()
            obs = self._reset(self.disp_env)
            done = False
            t = 0
            while not done and t < self.steps:
                self._maybe_push(self.disp_env, t)
                resid = np.clip((W + shared_W) @ obs, -self.residual_clip, self.residual_clip)
                obs, r, done, info = self.disp_env.step(self.base_disp.act(obs) + resid)
                d = self.disp_env.view.data
                self.live = {
                    "alive": bool(info["alive"]),
                    "height": float(d.xpos[self.disp_env.view.root_id][2]),
                    "bodies": [list(map(float, p)) for p in d.xpos[: self.disp_env.view.model.nbody]],
                    "reward": float(r),
                }
                t += 1
                time.sleep(0.03)

    def start(self):
        threading.Thread(target=self._train, daemon=True).start()
        threading.Thread(target=self._display, daemon=True).start()
