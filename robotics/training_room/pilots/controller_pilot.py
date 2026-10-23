"""ControllerPilot — adapt a model-based LocomotionController to the Pilot interface.

The controller reads full MuJoCo state (CoM, contacts, torso orientation), so
it needs a live env. `attach(env)` hands it the env; `act(obs)` then delegates
to the controller, which reads the env's current `data` directly.
"""
from __future__ import annotations

import numpy as np

from .base import Pilot


class ControllerPilot(Pilot):
    def __init__(self, controller_factory, name: str = "controller"):
        self._factory = controller_factory
        self.name = name
        self._controller = None

    def attach(self, env) -> None:
        self._controller = self._factory(env)

    def reset(self) -> None:
        if self._controller is not None:
            self._controller.reset()

    def act(self, obs: np.ndarray) -> np.ndarray:
        if self._controller is None:
            return np.zeros(28)
        return self._controller.act(obs)
