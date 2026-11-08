#!/usr/bin/env python3
"""
Single-skill cycling trainer.

Per Captain's directive: train ONE skill at a time to ~mid-200s generations,
then switch to the next skill, cycling through all body skills. This keeps CPU
to a single MuJoCo env at a time instead of 19 skills × 2 envs.

State (theta + gen) persists per skill under runs/cycle/, so progress survives
restarts and each skill resumes where it left off on its next turn in the cycle.

Usage:
  python3 cycle_train.py            # run the cycle (one full pass)
  python3 cycle_train.py --forever  # keep cycling until interrupted
  python3 cycle_train.py --status   # show per-skill progress
"""
from __future__ import annotations

import argparse
import gc
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

TARGET_GEN = 250          # "mid-200s"
STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs", "cycle")

STAIRS = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "rp1", "RP1_description",
    "mjcf", "rp1_stairs.xml"))

# Same skill list as train_server.py (body skills only — hand/myl0n are separate
# curricula with different obs/act dims and are intentionally excluded here).
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


def state_path(name):
    return os.path.join(STATE_DIR, f"{name}.npz")


def load_state(name):
    p = state_path(name)
    if os.path.exists(p):
        d = np.load(p)
        return d["theta"], int(d["gen"]), float(d["mean_r"]), float(d["max_r"])
    return None, 0, 0.0, 0.0


def save_state(name, tr):
    os.makedirs(STATE_DIR, exist_ok=True)
    np.savez(state_path(name), theta=tr.theta, gen=tr.gen, mean_r=tr.mean_r, max_r=tr.max_r)


def train_to(tr, target_gen):
    """Bounded ES loop (replicates SkillTrainer._train, but stops at target_gen)."""
    while tr.gen < target_gen:
        eps = tr.rng.standard_normal((tr.popsize, tr.n_params))
        rewards = np.zeros(tr.popsize)
        for i in range(tr.popsize):
            rewards[i] = tr._rollout(tr.train_env, tr.base_train, tr.theta + tr.sigma * eps[i])
        rewards = np.nan_to_num(rewards, nan=-1e3, posinf=-1e3, neginf=-1e3)
        A = (rewards - rewards.mean()) / (rewards.std() + 1e-8)
        with tr.lock:
            tr.theta += (tr.lr / (tr.popsize * tr.sigma)) * np.einsum("i,ij->j", A, eps)
            tr.gen += 1
            tr.mean_r = float(rewards.mean())
            tr.max_r = float(rewards.max())
    return tr


def build_trainer(skill):
    kw = {k: v for k, v in skill.items() if k not in ("name", "factory", "tier")}
    return SkillTrainer(skill["name"], skill["factory"], **kw)


def run_cycle(once=True):
    os.makedirs(STATE_DIR, exist_ok=True)
    print(f"Cycle trainer — target {TARGET_GEN} gens/skill, {len(SKILLS)} skills")

    while True:
        for skill in SKILLS:
            name = skill["name"]
            theta, gen, mean_r, max_r = load_state(name)
            print(f"\n=== {name} (resuming at gen {gen}/{TARGET_GEN}) ===", flush=True)

            tr = build_trainer(skill)
            if theta is not None:
                # guard against dim mismatch (e.g. skill def changed)
                if tr.n_params == len(theta):
                    tr.theta = theta
                    tr.gen = gen
                    tr.mean_r = mean_r
                    tr.max_r = max_r
                else:
                    print(f"  (state dim mismatch {len(theta)} vs {tr.n_params}, starting fresh)")

            t0 = time.time()
            tr = train_to(tr, TARGET_GEN)
            save_state(name, tr)
            dt = time.time() - t0
            print(f"  {name}: gen {tr.gen}, mean_r {tr.mean_r:.2f}, max_r {tr.max_r:.2f} "
                  f"({dt:.1f}s, {TARGET_GEN - tr.gen} remaining was 0)", flush=True)

            # free the two MuJoCo envs before the next skill
            del tr
            gc.collect()

        print("\n--- full cycle complete ---", flush=True)
        if once:
            return


def show_status():
    if not os.path.isdir(STATE_DIR):
        print("No cycle state yet.")
        return
    print(f"{'skill':14} {'gen':>5} {'mean_r':>8} {'max_r':>8}")
    for skill in SKILLS:
        name = skill["name"]
        _, gen, mean_r, max_r = load_state(name)
        print(f"{name:14} {gen:5} {mean_r:8.2f} {max_r:8.2f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forever", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    if args.status:
        show_status()
        return
    run_cycle(once=not args.forever)


if __name__ == "__main__":
    main()
