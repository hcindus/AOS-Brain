"""OllamaPilot — wraps one of our Ollama models as an RP1 pilot.

This is the bridge that lets Mort_II, qwen3.5, qwen2.5:14b, tinyllama, etc.
*drive* the robot in sim. The model receives a compact observation digest and
returns 28 torque values. It is deliberately lightweight: a single prompt per
step, cached session, no streaming.

Realistically a small LM is a weak torque controller on its own — that's the
point of the Training Room. The pilot is the *student*; the graduation gate is
what tells us when it's fit to leave the gym.
"""
from __future__ import annotations

import json
import urllib.request

import numpy as np

from .base import Pilot

OLLAMA_URL = "http://localhost:11434/api/generate"


class OllamaPilot(Pilot):
    name = "ollama"

    def __init__(
        self,
        model: str,
        n_act: int = 28,
        scale: float = 20.0,
        temperature: float = 0.2,
        timeout: float = 60.0,
        max_steps_remember: int = 3,
    ):
        self.model = model
        self.n_act = n_act
        self.scale = scale
        self.temperature = temperature
        self.timeout = timeout
        self._history: list[str] = []
        self._max_hist = max_steps_remember

    def reset(self) -> None:
        self._history = []

    def act(self, obs: np.ndarray) -> np.ndarray:
        digest = self._digest(obs)
        prompt = self._prompt(digest)
        reply = self._call(prompt)
        self._history.append(reply)
        self._history = self._history[-self._max_hist :]
        return self._parse(reply)

    # ------------------------------------------------------------------ #
    def _digest(self, obs: np.ndarray) -> str:
        height = float(obs[0])
        qpos = obs[5 + 3 + 3 : 5 + 3 + 3 + self.n_act]  # joints
        return (
            f"height={height:.3f} "
            f"mean_qpos={float(np.mean(qpos)):.3f} "
            f"max_abs_qpos={float(np.max(np.abs(qpos))):.3f}"
        )

    def _prompt(self, digest: str) -> str:
        sys_msg = (
            "You are a torque controller for a 28-DoF humanoid robot in "
            "simulation. Respond ONLY with a JSON list of 28 numbers in "
            "[-1,1]. Each number is a normalized joint torque. Keep the "
            "robot upright and move it forward (+x). No explanation."
        )
        hist = "\n".join(self._history[-2:])
        return (
            f"{sys_msg}\nObservation: {digest}\n"
            f"Previous responses:\n{hist}\nResponse (JSON list of 28):"
        )

    def _call(self, prompt: str) -> str:
        payload = json.dumps(
            {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": self.temperature,
            }
        ).encode()
        req = urllib.request.Request(
            OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.loads(r.read().decode())["response"]

    def _parse(self, reply: str) -> np.ndarray:
        # pull the first JSON array of numbers out of the reply
        import re

        m = re.search(r"\[[-\d.,\s]+\]", reply)
        if not m:
            return np.zeros(self.n_act)
        try:
            vals = json.loads(m.group(0))
        except json.JSONDecodeError:
            return np.zeros(self.n_act)
        vals = [float(v) for v in vals][: self.n_act]
        if len(vals) < self.n_act:
            vals += [0.0] * (self.n_act - len(vals))
        return np.clip(np.asarray(vals) * self.scale, -self.scale, self.scale)
