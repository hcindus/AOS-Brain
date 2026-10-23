"""Pilot interface + baseline pilots.

A Pilot is the thing that lives in the Training Room and produces actions.
Our "models" (the Ollama roster) get wrapped as pilots so they can drive the
RP1 in sim before ever touching a real robot.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class Pilot(ABC):
    name: str = "pilot"

    @abstractmethod
    def act(self, obs: np.ndarray) -> np.ndarray:
        """Return an action vector (28 torques) given an observation."""
        ...

    def reset(self) -> None:
        pass

    def on_episode_end(self, info: dict) -> None:
        pass


class ZeroPilot(Pilot):
    """Zero torque — the robot collapses. Baseline floor."""
    name = "zero"

    def __init__(self, n_act: int = 28):
        self.n_act = n_act

    def act(self, obs: np.ndarray) -> np.ndarray:
        return np.zeros(self.n_act)


class RandomPilot(Pilot):
    """Uniform random torque in the actuator range — flails. Baseline."""
    name = "random"

    def __init__(self, n_act: int = 28, scale: float = 10.0, seed: int | None = None):
        self.n_act = n_act
        self.scale = scale
        self.rng = np.random.default_rng(seed)

    def act(self, obs: np.ndarray) -> np.ndarray:
        return self.rng.uniform(-self.scale, self.scale, size=self.n_act)


class HoldPilot(Pilot):
    """PD controller holding the nominal (zero) pose. A naive 'stand' baseline.

    obs layout: [height, quat(4), vel(3), angvel(3), qpos(28), qvel(28)]
    """
    name = "hold"

    def __init__(self, n_act: int = 28, kp: float = 60.0, kd: float = 4.0):
        self.n_act = n_act
        self.kp = kp
        self.kd = kd
        self._q_offset = 1 + 4 + 3 + 3  # where qpos begins in obs

    def act(self, obs: np.ndarray) -> np.ndarray:
        qpos = obs[self._q_offset : self._q_offset + self.n_act]
        qvel = obs[self._q_offset + self.n_act : self._q_offset + 2 * self.n_act]
        # target = zero (nominal pose); qpos is already relative to nominal
        tau = -self.kp * qpos - self.kd * qvel
        return tau
