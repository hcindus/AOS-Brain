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
from controllers.ref_track import ReferenceTrackingController
from controllers.walk_controller import WalkController

WS_HOST = "127.0.0.1"
WS_PORT = 8096

STAIRS = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "rp1", "RP1_description", "mjcf", "rp1_stairs.xml"
))

# (skill dicts: name, tier, factory, plus SkillTrainer kwargs)
# tier: 300 = foundation (shares with everyone below), 200 = intermediate,
#        100 = specific (inherits from 200 + 300).
SKILLS = [
    {"name": "walk",    "tier": 200, "factory": lambda env: ReferenceTrackingController(env, "walk"),  "reference": "walk",  "gate_reward": False, "ignore_done": True},
    {"name": "run",     "tier": 100, "factory": lambda env: ReferenceTrackingController(env, "run"),   "reference": "run",   "gate_reward": False, "ignore_done": True},
    {"name": "balance", "tier": 300, "factory": lambda env: BalanceController(env), "mlp": True, "hidden": 64, "popsize": 24, "sigma": 0.2},
    {"name": "squat",   "tier": 200, "factory": lambda env: ReferenceTrackingController(env, "squat"), "reference": "squat", "gate_reward": False, "ignore_done": True},
    {"name": "jump",    "tier": 100, "factory": lambda env: ReferenceTrackingController(env, "jump"),  "reference": "jump",  "gate_reward": False, "ignore_done": True},
    {"name": "climb",   "tier": 200, "factory": lambda env: WalkController(env, gains={"lift": 0.12, "step_len": 0.12, "step_time": 1.0}), "forward_weight": 0.3, "height_weight": 1.5, "mjcf_path": STAIRS},
    {"name": "recover", "tier": 300, "factory": lambda env: BalanceController(env), "push_interval": 100, "push_force": 250.0, "mlp": True, "hidden": 64, "popsize": 24, "sigma": 0.2},
    {"name": "kneel",   "tier": 200, "factory": lambda env: ReferenceTrackingController(env, "kneel"), "reference": "kneel", "gate_reward": False, "ignore_done": True},
    {"name": "sit",     "tier": 200, "factory": lambda env: ReferenceTrackingController(env, "sit"),   "reference": "sit",   "gate_reward": False, "ignore_done": True},
    {"name": "crawl",   "tier": 100, "factory": lambda env: ReferenceTrackingController(env, "crawl"), "reference": "crawl", "gate_reward": False, "ignore_done": True},
    {"name": "roll",    "tier": 100, "factory": lambda env: ReferenceTrackingController(env, "roll"),  "reference": "roll",  "gate_reward": False, "ignore_done": True},
    {"name": "getup",   "tier": 100, "factory": lambda env: ReferenceTrackingController(env, "getup"), "reference": "getup", "gate_reward": False, "ignore_done": True},
    {"name": "swim",    "tier": 100, "factory": lambda env: ReferenceTrackingController(env, "swim"),  "reference": "swim",  "gate_reward": False, "ignore_done": True},
    {"name": "sit_stand",   "tier": 200, "factory": lambda env: ReferenceTrackingController(env, "sit_stand"),   "reference": "sit_stand",   "gate_reward": False, "ignore_done": True},
    {"name": "kneel_stand", "tier": 200, "factory": lambda env: ReferenceTrackingController(env, "kneel_stand"), "reference": "kneel_stand", "gate_reward": False, "ignore_done": True},
    {"name": "dance",   "tier": 100, "factory": lambda env: ReferenceTrackingController(env, "dance"), "reference": "dance", "gate_reward": False, "ignore_done": True},
    {"name": "fight",   "tier": 100, "factory": lambda env: ReferenceTrackingController(env, "fight"), "reference": "fight", "gate_reward": False, "ignore_done": True},
]

trainers = {}
tiers = {}
for s in SKILLS:
    kw = {k: v for k, v in s.items() if k not in ("name", "factory", "tier")}
    trainers[s["name"]] = SkillTrainer(s["name"], s["factory"], **kw)
    tiers[s["name"]] = s["tier"]

# dynamic knowledge sharing: every skill inherits from every *more-mature*
# skill (higher gen count). The `tier` field is just documentation now — the
# actual sharing is driven by live generation counts, so any skill that trains
# past another's gen automatically starts sharing with it.
# The hand uses a different env (underactuated 40-DOF, 91-dim obs) + grasp
# reward, so it gets its own trainer rather than the walk-based SkillTrainer.
# It must NOT share residuals with the body skills — different obs/act dims.
from dispatch.hand_trainer import HandSkillTrainer
hand_trainer = HandSkillTrainer(name="hand")
hand_trainer.all_trainers = []   # no knowledge sharing (different body)
trainers["hand"] = hand_trainer

# Myl0n.r0s — the Captain's executive orchestrator, embodied with a presence
# engine. He climbs a skill ladder (balance → squat → walk → …), advancing on
# a passing reward. Not in the body-sharing pool (his controller differs).
from dispatch.myl0n_curriculum import Myl0nCurriculumTrainer
myl0n_trainer = Myl0nCurriculumTrainer(name="myl0n")
myl0n_trainer.all_trainers = []
trainers["myl0n"] = myl0n_trainer

all_trainers = [t for t in trainers.values() if t not in (hand_trainer, myl0n_trainer)]
for t in all_trainers:
    t.all_trainers = all_trainers

def skeleton_info(env) -> dict:
    m = env.view.model
    parents = [int(m.body_parentid[i]) for i in range(m.nbody)]
    return {"parents": parents, "nbody": m.nbody}


def skeleton_map() -> dict:
    """Per-skill skeleton — the hand model has 64 bodies (fingers) vs the
    walk model's 30, so each skill carries its own topology for rendering."""
    out = {}
    for name, t in trainers.items():
        out[name] = skeleton_info(t.train_env)
    return out


async def handler(ws):
    await ws.send(json.dumps({"type": "init", "skeletons": skeleton_map(),
                              "skills": list(trainers.keys())}))
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
                        # Myl0n's curriculum: what skill he's learning + progress
                        "skill": getattr(t, "skill_name", name),
                        "pass_r": getattr(t, "pass_r", None),
                        "min_gen": getattr(t, "min_gen", None),
                        "completed": getattr(t, "completed", []),
                    }
                    for name, t in trainers.items()
                },
            }
            await ws.send(json.dumps(frame))
            await asyncio.sleep(0.05)
    except websockets.exceptions.ConnectionClosed:
        pass


async def main():
    for t in trainers.values():
        t.start()
    print(f"Skill Gym server on ws://{WS_HOST}:{WS_PORT} — skills: {list(trainers.keys())}", flush=True)
    async with websockets.serve(handler, WS_HOST, WS_PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
