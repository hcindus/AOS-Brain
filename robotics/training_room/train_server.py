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
import os
import threading

import numpy as np
import websockets

from gym import RP1GymEnv
from dispatch.skill_trainer import SkillTrainer
from controllers.balance import BalanceController
from controllers.squat import SquatController
from controllers.jump import JumpController
from controllers.getup import GetUpController
from controllers.roll import RollController
from controllers.crawl import CrawlController
from controllers.walk_controller import WalkController

WS_HOST = "127.0.0.1"
WS_PORT = 8096

STAIRS = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "rp1", "RP1_description", "mjcf", "rp1_stairs.xml"
))

# (skill dicts: name, factory, plus SkillTrainer kwargs)
SKILLS = [
    {"name": "walk",    "factory": lambda env: WalkController(env), "forward_weight": 1.0},
    {"name": "run",     "factory": lambda env: WalkController(env, gains={"step_len": 0.20, "step_time": 0.5}), "forward_weight": 1.5},
    {"name": "balance", "factory": lambda env: BalanceController(env)},
    {"name": "squat",   "factory": lambda env: SquatController(env)},
    {"name": "jump",    "factory": lambda env: JumpController(env), "height_weight": 2.0},
    {"name": "climb",   "factory": lambda env: WalkController(env, gains={"lift": 0.12, "step_len": 0.12, "step_time": 1.0}), "forward_weight": 0.3, "height_weight": 1.5, "mjcf_path": STAIRS},
    {"name": "recover", "factory": lambda env: BalanceController(env), "push_interval": 100, "push_force": 250.0},
    {"name": "kneel",   "factory": lambda env: SquatController(env, gains={"knee_flex": 1.0, "hip_bend": 0.5, "period": 4.0}), "height_weight": 1.5},
    {"name": "sit",     "factory": lambda env: SquatController(env, gains={"knee_flex": 1.2, "hip_bend": 0.6, "period": 5.0}), "height_weight": 1.5},
    {"name": "crawl",   "factory": lambda env: CrawlController(env), "forward_weight": 1.2},
    {"name": "roll",    "factory": lambda env: RollController(env), "roll_weight": 1.5, "start_lying": True},
    {"name": "getup",   "factory": lambda env: GetUpController(env), "height_weight": 2.0, "start_lying": True},
]

trainers = {}
for s in SKILLS:
    kw = {k: v for k, v in s.items() if k not in ("name", "factory")}
    trainers[s["name"]] = SkillTrainer(s["name"], s["factory"], **kw)

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
