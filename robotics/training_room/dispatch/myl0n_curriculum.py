"""Myl0nCurriculumTrainer — Myl0n.r0s advances through a skill ladder.

Myl0n is embodied with a presence-engine head, but he also needs a *body
curriculum*: a sequence of skills he masters in order, advancing to the next
when he passes the current one. This trainer wraps a SkillTrainer per skill and
swaps it when the pass condition is met, so Myl0n's tile always shows the skill
he's currently learning and auto-progresses him.

The pass condition is simple + observable: after a minimum number of generations,
if mean reward clears a per-skill threshold, advance to the next skill. The
current skill name + threshold are surfaced to the tile so progress is visible.

His presence engine is the "head" that stays constant across skills (posture +
affect); the curriculum changes the *body controller* he trains against.
"""
from __future__ import annotations

import threading
import time

from dispatch.skill_trainer import SkillTrainer
from controllers.balance import BalanceController
from controllers.getup import GetUpController
from controllers.ref_track import ReferenceTrackingController
from controllers.squat import SquatController
from controllers.walk_controller import WalkController


# The ladder Myl0n climbs. Each entry: skill name, base-controller factory,
# and the pass threshold (mean reward) + min generations before he can advance.
#
# getup comes BEFORE balance: he must learn to stand up (recover from a fall)
# before he can balance. balance (static) → squat → walk had no recovery step,
# so a fall was unrecoverable — the exact "he's fallen and can't get up" state.
CURRICULUM = [
    {"skill": "getup",   "min_gen": 20, "pass_r": 50.0,
     "factory": lambda env: GetUpController(env),
     "gate_reward": True, "start_lying": True},
    {"skill": "balance", "min_gen": 15, "pass_r": 250.0,
     "factory": lambda env: BalanceController(env), "gate_reward": True},
    {"skill": "squat",   "min_gen": 15, "pass_r": 0.0,
     "factory": lambda env: ReferenceTrackingController(env, "squat"),
     "gate_reward": False, "ignore_done": True, "reference": "squat"},
    {"skill": "walk",    "min_gen": 15, "pass_r": 0.0,
     "factory": lambda env: ReferenceTrackingController(env, "walk"),
     "gate_reward": False, "ignore_done": True, "reference": "walk"},
]


class Myl0nCurriculumTrainer:
    """A meta-trainer that swaps SkillTrainer instances as Myl0n passes skills."""

    def __init__(self, name: str = "myl0n", curriculum: list | None = None):
        self.name = name
        self.curriculum = curriculum or CURRICULUM
        self.cur_idx = 0
        self.skill_name = self.curriculum[0]["skill"]
        self.pass_r = self.curriculum[0]["pass_r"]
        self.min_gen = self.curriculum[0]["min_gen"]
        self.completed: list[str] = []

        self.current = self._make_trainer(0)
        self.all_trainers = []  # Myl0n does not share residuals with body skills

        self._running = False
        self._advance_thread = None

    def _make_trainer(self, idx: int) -> SkillTrainer:
        entry = self.curriculum[idx]
        kw = {k: v for k, v in entry.items() if k not in ("skill", "min_gen", "pass_r", "factory")}
        return SkillTrainer(entry["skill"], entry["factory"], **kw)

    # -- proxy the SkillTrainer interface the server expects -----------------
    @property
    def gen(self):
        return self.current.gen

    @property
    def mean_r(self):
        return self.current.mean_r

    @property
    def max_r(self):
        return self.current.max_r

    @property
    def history(self):
        return self.current.history

    @property
    def live(self):
        return self.current.live

    @property
    def train_env(self):
        return self.current.train_env

    def start(self):
        self.current.start()
        self._running = True
        self._advance_thread = threading.Thread(target=self._watch, daemon=True)
        self._advance_thread.start()

    def _watch(self):
        """Check the pass condition and advance Myl0n when he passes."""
        while self._running:
            time.sleep(5)
            if self.cur_idx >= len(self.curriculum) - 1:
                continue  # last skill — no further advance
            with self.current.lock:
                gen = self.current.gen
                mean_r = self.current.mean_r
            if gen >= self.min_gen and mean_r >= self.pass_r:
                self._advance()

    def _advance(self):
        prev = self.skill_name
        self.completed.append(prev)
        self.cur_idx += 1
        entry = self.curriculum[self.cur_idx]
        self.skill_name = entry["skill"]
        self.pass_r = entry["pass_r"]
        self.min_gen = entry["min_gen"]
        # stop the old trainer's loops (daemon threads; set a flag)
        self.current._running = getattr(self.current, "_running", None)
        self.current = self._make_trainer(self.cur_idx)
        self.current.start()
        print(f"[myl0n] ✅ PASSED {prev} → now learning {self.skill_name}", flush=True)

    def status(self) -> dict:
        return {
            "name": self.name,
            "skill": self.skill_name,
            "curriculum": [c["skill"] for c in self.curriculum],
            "cur_idx": self.cur_idx,
            "completed": self.completed,
            "pass_r": self.pass_r,
            "min_gen": self.min_gen,
            "gen": self.gen,
            "mean_r": round(self.mean_r, 2),
        }


if __name__ == "__main__":
    t = Myl0nCurriculumTrainer()
    print("curriculum:", [c["skill"] for c in t.curriculum])
    print("starting skill:", t.skill_name, "pass_r:", t.pass_r, "min_gen:", t.min_gen)
    print("status:", t.status())
    print("Myl0nCurriculumTrainer self-test OK")
