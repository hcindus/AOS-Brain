"""Residual policies — the learned additive torque on top of a base controller.

Two forms:
  Linear  — obs -> 28 torques via a weight matrix (fast, low capacity).
  MLP     — obs -> 64 tanh -> 28 tanh*clip (nonlinear, breaks the linear ceiling).

Both expose a flat parameter vector `theta` (so ES perturbs it uniformly) and a
`forward(theta, obs)` returning the 28-D residual torque.
"""
from __future__ import annotations

import numpy as np


class MLPResidual:
    """obs -> normalize -> 64 tanh -> 28 tanh*clip. ~6k params. Near-zero init."""

    def __init__(self, obs_dim: int, n_act: int, hidden: int = 64, clip: float = 15.0):
        self.obs_dim = obs_dim
        self.n_act = n_act
        self.hidden = hidden
        self.clip = clip

        self.w1_size = hidden * obs_dim
        self.b1_size = hidden
        self.w2_size = n_act * hidden
        self.b2_size = n_act
        self.n_params = self.w1_size + self.b1_size + self.w2_size + self.b2_size

        # input normalization (fixed reasonable per-dim scales)
        self.in_mean = np.zeros(obs_dim)
        self.in_mean[0] = 0.6          # root height (~0.78 standing)
        self.in_std = np.ones(obs_dim)
        self.in_std[0] = 0.3           # height
        self.in_std[1:5] = 0.7         # quat (w x y z)
        self.in_std[5:11] = 0.5        # root vel + angvel
        self.in_std[11:39] = 1.0       # qpos (28)
        self.in_std[39:67] = 2.0       # qvel (28)

    def zero(self) -> np.ndarray:
        return np.zeros(self.n_params)

    def forward(self, theta: np.ndarray, obs: np.ndarray) -> np.ndarray:
        i = 0
        w1 = theta[i:i + self.w1_size].reshape(self.hidden, self.obs_dim); i += self.w1_size
        b1 = theta[i:i + self.b1_size]; i += self.b1_size
        w2 = theta[i:i + self.w2_size].reshape(self.n_act, self.hidden); i += self.w2_size
        b2 = theta[i:i + self.b2_size]

        x = (obs - self.in_mean) / self.in_std
        h = np.tanh(w1 @ x + b1)
        return np.tanh(w2 @ h + b2) * self.clip
