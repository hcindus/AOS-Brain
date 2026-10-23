"""CPU RL training — evolutionary strategy (ES) on MuJoCo rollouts.

This is the answer to "we should be able to train on the VPS / a laptop."
No GPU needed: it evolves a linear policy (obs → 28 torques) by sampling
Gaussian perturbations, scoring each on a short rollout, and moving the mean
toward reward-weighted perturbations (the classic ES gradient). MuJoCo runs
on CPU, so this trains right here — slower than an H20 cluster, but real.

The UFO / Isaac Lab path (dispatch/gpu.py) remains the heavy-lift option when
we want a deep policy at reference scale.
"""
from __future__ import annotations

import numpy as np

from pilots.neural_pilot import NeuralPilot


def train_cpu(
    env,
    generations: int = 20,
    popsize: int = 16,
    steps: int = 200,
    sigma: float = 0.5,
    lr: float = 0.05,
    seed: int = 0,
    progress: bool = True,
) -> tuple[np.ndarray, list]:
    rng = np.random.default_rng(seed)
    obs_dim = env.obs_dim
    n_act = env.n_act
    W = np.zeros((n_act, obs_dim))
    history = []

    for gen in range(generations):
        eps = rng.standard_normal((popsize, n_act, obs_dim))
        rewards = np.zeros(popsize)

        for i in range(popsize):
            Wi = W + sigma * eps[i]
            pilot = NeuralPilot(obs_dim, n_act, Wi)
            obs = env.reset(qpos_noise=0.02)
            total = 0.0
            done = False
            t = 0
            while not done and t < steps:
                obs, r, done, _ = env.step(pilot.act(obs))
                total += r
                t += 1
            rewards[i] = total

        # normalize rewards → ES gradient step
        std = rewards.std()
        A = (rewards - rewards.mean()) / (std + 1e-8)
        W += (lr / (popsize * sigma)) * np.einsum("i,ijk->jk", A, eps)

        history.append((gen, float(rewards.mean()), float(rewards.max())))
        if progress:
            print(f"gen {gen:3d}  mean_r={rewards.mean():8.2f}  max_r={rewards.max():8.2f}")

    return W, history
