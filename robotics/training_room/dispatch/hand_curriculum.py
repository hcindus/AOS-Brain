"""HandCurriculumTrainer — the hand learns grasp then universal gestures.

The hand climbs a ladder: grasp (curl fingers) → universal gestures that use
the arm + hand together (point, stop, come, go_away, wave_hello, wave_help).
Each step is a HandSkillTrainer with a different target pose; the trainer
swaps to the next gesture when the current one passes.

Gestures use the full arm (root_locked so raising an arm doesn't tip the body)
and a target pose the ES learns to reach. The pass condition is pose error:
once the mean pose error drops below a threshold, the gesture is "reached."
"""
from __future__ import annotations

import threading
import time

import numpy as np

from gym.hand_env import HandGymEnv, GRASP_TARGET
from gym.gestures import target as gesture_target, gesture_names
from controllers.hand import HandController
from dispatch.hand_trainer import HandSkillTrainer


# The hand's ladder: (name, target-pose, pass threshold on mean pose error).
# grasp uses the curl target (12 finger values) mapped into the 40-dim space;
# gestures use arm+finger targets (root_locked).
def _grasp_target_40() -> np.ndarray:
    """Map the 12 finger curl values (GRASP_TARGET) onto the 40 actuator indices.

    Finger actuators are 28..39 (12 of them); the GRASP_TARGET is a 12-element
    vector in that order. Everything else (legs/arms) stays 0 = standing/neutral.
    """
    v = np.zeros(40, dtype=np.float64)
    v[28:40] = np.asarray(GRASP_TARGET, dtype=np.float64)
    return v


def _ladder():
    steps = [("grasp", _grasp_target_40(), 0.05)]
    for g in gesture_names():
        steps.append((g, gesture_target(g), 0.08))
    return steps


class HandCurriculumTrainer:
    def __init__(self, name: str = "hand"):
        self.name = name
        self.ladder = _ladder()
        self.idx = 0
        self.skill_name = self.ladder[0][0]
        self.pass_err = self.ladder[0][2]
        self.completed: list[str] = []
        self.current = self._make(0)
        self.all_trainers = []
        self._running = False

    def _make(self, idx: int) -> HandSkillTrainer:
        gname, tgt, pass_err = self.ladder[idx]
        # root_locked for gestures (arms move), not for grasp (fingers only)
        root_locked = (gname != "grasp")
        t = HandSkillTrainer(name=gname)
        t.hand_env = HandGymEnv(target=tgt, root_locked=root_locked)
        t.hand_disp = HandGymEnv(target=tgt, root_locked=root_locked)
        t.train_env = t.hand_env
        t.disp_env = t.hand_disp
        t.base_train = HandController(t.train_env, target=tgt)
        t.base_disp = HandController(t.disp_env, target=tgt)
        t.obs_dim = t.train_env.obs_dim
        t.n_act = t.train_env.n_act
        t.n_params = t.n_act * t.obs_dim
        t.theta = np.zeros(t.n_params)
        t._stop = False
        # track the pose error live so the pass condition can read it
        t.pose_err = 1.0
        return t

    # -- proxy the trainer interface ----------------------------------------
    @property
    def gen(self): return self.current.gen

    @property
    def mean_r(self): return self.current.mean_r

    @property
    def max_r(self): return self.current.max_r

    @property
    def history(self): return self.current.history

    @property
    def live(self): return self.current.live

    @property
    def train_env(self): return self.current.train_env

    def start(self):
        self.current.start()
        self._running = True
        threading.Thread(target=self._watch, daemon=True).start()

    def _watch(self):
        while self._running:
            time.sleep(5)
            if self.idx >= len(self.ladder) - 1:
                continue
            with self.current.lock:
                gen = self.current.gen
                pose_err = getattr(self.current, "pose_err", 1.0)
            # pass when the pose is reached (low error) after a min gen floor
            if gen >= 10 and pose_err <= self.pass_err:
                self._advance()

    def _advance(self):
        prev = self.skill_name
        self.completed.append(prev)
        self.idx += 1
        gname, _, pass_err = self.ladder[self.idx]
        self.skill_name = gname
        self.pass_err = pass_err
        self.current._stop = True
        self.current = self._make(self.idx)
        self.current.start()
        print(f"[hand] ✅ mastered {prev} → now learning {self.skill_name}", flush=True)

    def status(self) -> dict:
        return {
            "name": self.name,
            "skill": self.skill_name,
            "curriculum": [s[0] for s in self.ladder],
            "idx": self.idx,
            "completed": self.completed,
            "pass_err": self.pass_err,
            "gen": self.gen,
            "mean_r": round(self.mean_r, 2),
        }


if __name__ == "__main__":
    t = HandCurriculumTrainer()
    print("curriculum:", [s[0] for s in t.ladder])
    print("starting:", t.skill_name, "pass_err:", t.pass_err)
    print("status:", t.status())
    print("OK")
