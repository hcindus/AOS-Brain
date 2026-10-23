#!/usr/bin/env python3
"""Live training server — streams RP1 training to a browser in real time.

Two background threads share state:

  train thread   — runs the ES (evolution strategy) loop, evolving a linear
                   policy (obs -> 28 torques) on MuJoCo rollouts, updating the
                   best policy + the reward history each generation.

  display thread — continuously rolls out the current best policy and captures
                   per-step body positions + telemetry, so the browser sees the
                   robot actually move (and fall) live.

A `websockets` server pushes the latest frame + reward history to each client
at ~20 Hz. The static page is served by nginx; this only serves the WS socket.
"""
from __future__ import annotations

import asyncio
import json
import threading
import time

import numpy as np
import websockets

from gym import RP1GymEnv
from pilots.neural_pilot import NeuralPilot

WS_HOST = "127.0.0.1"
WS_PORT = 8096

# --- training hyperparameters (CPU-scale) ---
POPSIZE = 16
STEPS = 300
SIGMA = 0.5
LR = 0.05

# --- model bench (controllers/pilots tested in rotation, shown live) ---
BENCH_MODELS = ["balance", "hold", "zero", "random"]
BENCH_STEPS = 500  # ~2.5 s per model at 500 Hz


class SharedState:
    def __init__(self):
        self.lock = threading.Lock()
        self.best_W = None
        self.gen = 0
        self.mean_r = 0.0
        self.max_r = 0.0
        self.history: list = []  # [gen, mean_r, max_r]
        self.bench: dict = {}          # model -> {"alive": frac, "steps": n}
        self.bench_current: str | None = None
        self.live: dict = {
            "alive": True,
            "height": 0.78,
            "tilt": 0.0,
            "com": [0.0, 0.0, 0.78],
            "bodies": [],
            "step": 0,
            "reward": 0.0,
        }

    def set_best(self, W, gen, mean_r, max_r):
        with self.lock:
            self.best_W = np.asarray(W).copy()
            self.gen = gen
            self.mean_r = float(mean_r)
            self.max_r = float(max_r)
            self.history.append([gen, float(mean_r), float(max_r)])
            # cap history so a long-running service doesn't grow the WS payload
            # (and the JSON serialization cost) without bound.
            if len(self.history) > 1000:
                self.history = self.history[-1000:]

    def get_best(self):
        with self.lock:
            return None if self.best_W is None else self.best_W.copy()

    def set_live(self, **kw):
        with self.lock:
            self.live.update(kw)

    def set_bench_current(self, model):
        with self.lock:
            self.bench_current = model

    def set_bench_result(self, model, alive_frac, steps):
        with self.lock:
            self.bench[model] = {"alive": round(alive_frac, 3), "steps": steps}

    def get_bench(self):
        with self.lock:
            return dict(self.bench), self.bench_current

    def snapshot(self):
        with self.lock:
            return dict(self.live), list(self.history), self.gen, self.mean_r, self.max_r


state = SharedState()


def train_loop(env: RP1GymEnv):
    """ES loop — evolve a linear policy, publish best + reward history.

    Runs continuously (no fixed generation cap) so the dashboard keeps
    updating and the policy keeps improving for as long as the service lives.
    """
    rng = np.random.default_rng(0)
    obs_dim, n_act = env.obs_dim, env.n_act
    W = np.zeros((n_act, obs_dim))

    gen = 0
    while True:
        eps = rng.standard_normal((POPSIZE, n_act, obs_dim))
        rewards = np.zeros(POPSIZE)
        for i in range(POPSIZE):
            pilot = NeuralPilot(obs_dim, n_act, W + SIGMA * eps[i])
            obs = env.reset(qpos_noise=0.02)
            total = 0.0
            done = False
            t = 0
            while not done and t < STEPS:
                obs, r, done, _ = env.step(pilot.act(obs))
                total += r
                t += 1
            rewards[i] = total

        A = (rewards - rewards.mean()) / (rewards.std() + 1e-8)
        W += (LR / (POPSIZE * SIGMA)) * np.einsum("i,ijk->jk", A, eps)
        state.set_best(W, gen, rewards.mean(), rewards.max())
        gen += 1


def display_loop(env: RP1GymEnv):
    """Bench loop — cycle through the hand-written controllers/pilots, evaluating
    each in the gym and streaming its live body positions + a rolling score.

    This is what the browser's 3D view shows: each model takes a turn trying to
    stand (balance, hold, zero, random), and the bench table records how each
    fared. As new controllers land (squat, walk, get-up), add them to
    BENCH_MODELS and they appear here automatically.
    """
    from agents.registry import load_roster, pilot_by_id

    roster = load_roster()
    pilots = {}
    for pid in BENCH_MODELS:
        p = pilot_by_id(pid, roster)
        p.attach(env)
        pilots[pid] = p

    while True:
        for pid in BENCH_MODELS:
            pilot = pilots[pid]
            state.set_bench_current(pid)
            obs = env.reset(qpos_noise=0.02)
            pilot.reset()
            alive = 0.0
            t = 0
            done = False
            while not done and t < BENCH_STEPS:
                obs, r, done, info = env.step(pilot.act(obs))
                alive += float(info["alive"])
                d = env.view.data
                up = d.xmat[env.view.root_id][6:9]
                state.set_live(
                    alive=bool(info["alive"]),
                    height=float(d.xpos[env.view.root_id][2]),
                    tilt=float(np.hypot(up[0], up[1])),
                    com=[float(x) for x in d.subtree_com[0]],
                    bodies=[list(map(float, p)) for p in d.xpos[: env.view.model.nbody]],
                    step=t,
                    reward=float(r),
                )
                t += 1
                time.sleep(0.02)  # ~50 Hz cap
            state.set_bench_result(pid, alive / BENCH_STEPS, t)
            time.sleep(0.4)  # brief pause so "testing X" is visible


def skeleton_info(env: RP1GymEnv) -> dict:
    m = env.view.model
    parents = [int(m.body_parentid[i]) for i in range(m.nbody)]
    names = [
        __import__("mujoco").mj_id2name(m, __import__("mujoco").mjtObj.mjOBJ_BODY, i)
        for i in range(m.nbody)
    ]
    return {"parents": parents, "names": names, "nbody": m.nbody}


async def handler(ws):
    # static skeleton topology once on connect (computed once in main)
    await ws.send(json.dumps({"type": "init", **SKELETON}))
    print("client connected", flush=True)
    try:
        while True:
            live, history, gen, mean_r, max_r = state.snapshot()
            bench, bench_current = state.get_bench()
            await ws.send(
                json.dumps(
                    {
                        "type": "frame",
                        "gen": gen,
                        "mean_r": mean_r,
                        "max_r": max_r,
                        "history": history,
                        "live": live,
                        "bench": bench,
                        "bench_current": bench_current,
                        "bench_models": BENCH_MODELS,
                    }
                )
            )
            await asyncio.sleep(0.05)
    except websockets.exceptions.ConnectionClosed:
        pass


async def main():
    global SKELETON
    train_env = RP1GymEnv()
    display_env = RP1GymEnv()
    SKELETON = skeleton_info(display_env)
    threading.Thread(target=train_loop, args=(train_env,), daemon=True).start()
    threading.Thread(target=display_loop, args=(display_env,), daemon=True).start()
    print(f"RP1 training server on ws://{WS_HOST}:{WS_PORT}", flush=True)
    async with websockets.serve(handler, WS_HOST, WS_PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
