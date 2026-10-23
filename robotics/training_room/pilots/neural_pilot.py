"""NeuralPilot — a learned policy (linear, obs → 28 torques).

This is the thing the Training Room *trains*. It has no hand-written control
law; its parameters are found by a trainer (see dispatch/cpu_train.py). A
linear policy is the honest CPU-scale baseline — an MLP is the obvious next
step when we have GPU.
"""
from __future__ import annotations

import numpy as np

from .base import Pilot


class NeuralPilot(Pilot):
    name = "neural"

    def __init__(self, obs_dim: int, n_act: int, W: np.ndarray | None = None, seed: int | None = None):
        self.obs_dim = obs_dim
        self.n_act = n_act
        self.rng = np.random.default_rng(seed)
        self.W = np.asarray(W, dtype=np.float64) if W is not None else np.zeros((n_act, obs_dim))

    def act(self, obs: np.ndarray) -> np.ndarray:
        return self.W @ np.asarray(obs, dtype=np.float64)

    def get_params(self) -> np.ndarray:
        return self.W.copy()

    def set_params(self, W: np.ndarray) -> None:
        self.W = np.asarray(W, dtype=np.float64)
