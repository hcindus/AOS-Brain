"""Dispatch backends — where training/eval actually runs.

`local_cpu` runs the pilot in MuJoCo on this host (CPU). `gpu` is the plug-in
socket for a cloud GPU (RunPod/Lambda) or a dedicated box: same interface,
heavy policy training dispatched remotely, results flow back for scoring.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from gym import RP1GymEnv


class TrainingBackend(ABC):
    name = "backend"

    @abstractmethod
    def eval(self, pilot, env: RP1GymEnv | None = None, episodes: int = 1) -> dict:
        """Run a pilot for N episodes and return summary stats."""

    def train(self, pilot, config: dict | None = None) -> dict:
        """Train a policy. On CPU this is a no-op placeholder; on GPU it
        dispatches a real RL job. Returns a run handle / status."""
        return {"backend": self.name, "status": "not_implemented"}


class LocalCPUBackend(TrainingBackend):
    name = "local_cpu"

    def eval(self, pilot, env: RP1GymEnv | None = None, episodes: int = 1) -> dict:
        env = env or RP1GymEnv()
        import numpy as np

        rewards, alive = [], []
        for _ in range(episodes):
            obs = env.reset(qpos_noise=0.02)
            pilot.reset()
            ep_r, ep_alive = 0.0, 0.0
            done = False
            while not done:
                obs, r, done, info = env.step(pilot.act(obs))
                ep_r += r
                ep_alive += float(info["alive"])
            rewards.append(ep_r)
            alive.append(ep_alive / env.horizon)
        return {
            "backend": self.name,
            "episodes": episodes,
            "mean_reward": float(np.mean(rewards)),
            "mean_alive_frac": float(np.mean(alive)),
        }


class GPUBackend(TrainingBackend):
    """Socket for cloud / dedicated GPU. Interface only — not wired yet."""

    name = "gpu"

    def __init__(self, provider: str | None = None):
        self.provider = provider

    def eval(self, pilot, env: RP1GymEnv | None = None, episodes: int = 1) -> dict:
        return {"backend": self.name, "status": "unavailable", "provider": self.provider}

    def train(self, pilot, config: dict | None = None) -> dict:
        return {
            "backend": self.name,
            "provider": self.provider,
            "status": "plug_in_socket — no GPU configured",
        }


def get_backend(name: str = "local_cpu", **kw) -> TrainingBackend:
    if name == "local_cpu":
        return LocalCPUBackend()
    if name == "gpu":
        return GPUBackend(**kw)
    raise ValueError(f"unknown backend: {name}")
