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
                 height_weight: float = 0.0, mjcf_path: str | None = None,
                 residual_clip: float = 15.0, popsize: int = 12, sigma: float = 0.3,
                 lr: float = 0.05, steps: int = 300, seed: int = 0):
        self.name = name
        self.forward_weight = forward_weight
        self.height_weight = height_weight
        self.residual_clip = residual_clip
        self.popsize = popsize
        self.sigma = sigma
        self.lr = lr
        self.steps = steps

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
    def _rollout(self, env, base, W) -> float:
        base.reset()
        obs = env.reset(qpos_noise=0.02)
        total = 0.0
        prev_x = 0.0
        prev_z = float(obs[0])
        done = False
        t = 0
        while not done and t < self.steps:
            resid = np.clip(W @ obs, -self.residual_clip, self.residual_clip)
            obs, r, done, info = env.step(base.act(obs) + resid)
            fwd = info["progress"] - prev_x
            prev_x = info["progress"]
            up = float(obs[0]) - prev_z
            prev_z = float(obs[0])
            total += float(info["alive"]) * (
                1.0 + self.forward_weight * fwd * 20.0 + self.height_weight * up * 20.0
            )
            t += 1
        return total

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
            self.base_disp.reset()
            obs = self.disp_env.reset(qpos_noise=0.02)
            done = False
            t = 0
            while not done and t < self.steps:
                resid = np.clip(W @ obs, -self.residual_clip, self.residual_clip)
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
