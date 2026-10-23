#!/usr/bin/env python3
"""Skill Gym server — each skill trains in its own lane, streamed to the browser.

Three skills (walk, balance, squat) each get a SkillTrainer that runs an ES
training thread + a live display thread in parallel. The browser shows one
window per skill, so walking focuses on walking, balance on balance, etc.

A `websockets` server pushes every skill's live frame + reward history to each
client at ~20 Hz. The static page is served by nginx.
"""
from __future__ import annotations

import asyncio
import json
import threading

import numpy as np
import websockets

from gym import RP1GymEnv
from dispatch.skill_trainer import SkillTrainer
from controllers.balance import BalanceController
from controllers.squat import SquatController
from controllers.walk_controller import WalkController

WS_HOST = "127.0.0.1"
WS_PORT = 8096

# (name, base_controller_factory, forward_weight)
SKILLS = [
    ("walk", WalkController, 1.0),
    ("balance", BalanceController, 0.0),
    ("squat", SquatController, 0.0),
]

trainers = {name: SkillTrainer(name, factory, fwd) for name, factory, fwd in SKILLS}

SKELETON: dict = {}


def skeleton_info(env: RP1GymEnv) -> dict:
    m = env.view.model
    parents = [int(m.body_parentid[i]) for i in range(m.nbody)]
    return {"parents": parents, "nbody": m.nbody}


async def handler(ws):
    await ws.send(json.dumps({"type": "init", **SKELETON, "skills": list(trainers.keys())}))
    print("client connected", flush=True)
    try:
        while True:
            frame = {
                "type": "frame",
                "skills": {
                    name: {
                        "gen": t.gen,
                        "mean_r": t.mean_r,
                        "max_r": t.max_r,
                        "history": t.history,
                        "live": t.live,
                    }
                    for name, t in trainers.items()
                },
            }
            await ws.send(json.dumps(frame))
            await asyncio.sleep(0.05)
    except websockets.exceptions.ConnectionClosed:
        pass


async def main():
    global SKELETON
    SKELETON = skeleton_info(trainers["walk"].train_env)
    for t in trainers.values():
        t.start()
    print(f"Skill Gym server on ws://{WS_HOST}:{WS_PORT} — skills: {list(trainers.keys())}", flush=True)
    async with websockets.serve(handler, WS_HOST, WS_PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
