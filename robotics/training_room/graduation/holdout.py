"""Blind hold-out validation — the score a pilot must earn to graduate.

Three scenarios, each run fresh and scored 0..1:

  stand         — survive upright for the full horizon
  walk          — make forward progress while staying alive
  push_recovery — absorb a lateral impulse and stay upright

The aggregate is a weighted mean. This is the same "blind hold-out" discipline
we run on the Dark Factory: no peeking at the training distribution.
"""
from __future__ import annotations

import numpy as np

from gym import RP1GymEnv

SCENARIOS = {
    "stand": 0.4,
    "walk": 0.4,
    "push_recovery": 0.2,
}


def _run_episode(env, pilot, steps: int, push_at: int | None = None, push_force=None):
    obs = env.reset(qpos_noise=0.02)
    pilot.reset()
    total_r = 0.0
    alive_frac = 0.0
    progress = 0.0
    for t in range(steps):
        if push_at is not None and t == push_at and push_force is not None:
            env.view.data.qfrc_applied[:3] += push_force
        act = pilot.act(obs)
        obs, r, done, info = env.step(act)
        total_r += r
        alive_frac += float(info["alive"])
        progress = info["progress"]
        if done:
            break
    return {
        "steps": steps,
        "alive_frac": alive_frac / steps,
        "total_reward": total_r,
        "progress": progress,
    }


def score_pilot(pilot, env: RP1GymEnv | None = None) -> dict:
    env = env or RP1GymEnv()
    pilot.attach(env)
    results = {}

    # stand
    r = _run_episode(env, pilot, steps=env.horizon)
    results["stand"] = r["alive_frac"]

    # walk
    r = _run_episode(env, pilot, steps=env.horizon)
    results["walk"] = min(1.0, max(0.0, (r["progress"] + 0.5) / 1.0) * r["alive_frac"])

    # push_recovery
    r = _run_episode(
        env, pilot, steps=env.horizon, push_at=200, push_force=np.array([0.0, 120.0, 0.0])
    )
    results["push_recovery"] = r["alive_frac"]

    overall = sum(results[k] * SCENARIOS[k] for k in SCENARIOS)
    return {"scenarios": results, "overall": float(overall)}
