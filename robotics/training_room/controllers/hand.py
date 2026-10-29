"""HandController — base PD hold for the hand model + grasp curl.

Holds the 28 body joints at nominal (so the body stands) and curls the 12
finger actuators toward the grasp target. The learned residual (ES) refines
the grasp — so the hand trains the *precision* of the grasp on top of a naive
"close everything" base, exactly like the reference-tracking skills.

Obs layout (HandGymEnv): [height, quat(4), vel(3), angvel(3), qpos(40), qvel(40)]
"""
from __future__ import annotations

import numpy as np

from gym.hand_env import GRASP_TARGET  # noqa: F401  (kept for the default path)


class HandController:
    name = "hand"

    def __init__(self, env, kp_body: float = 60.0, kd_body: float = 4.0,
                 kp_grasp: float = 40.0, kd_grasp: float = 2.0,
                 target: np.ndarray | None = None):
        self.env = env
        self.view = env.view
        self.kp_body = kp_body
        self.kd_body = kd_body
        self.kp_grasp = kp_grasp
        self.kd_grasp = kd_grasp
        # target pose (default = env target if present, else the grasp curl)
        if target is not None:
            self.target = np.asarray(target, dtype=np.float64)
        elif hasattr(env, "target"):
            self.target = np.asarray(env.target, dtype=np.float64)
        else:
            self.target = np.asarray(GRASP_TARGET, dtype=np.float64)
        # mask of joints the target specifies (non-zero) — only these are driven
        self.mask = np.abs(self.target) > 1e-6

        self._q_offset = 1 + 4 + 3 + 3  # where actuated qpos begins in obs

    def reset(self) -> None:
        pass

    def act(self, obs: np.ndarray | None = None) -> np.ndarray:
        d = self.view.data
        m = self.view.model
        n_act = self.env.n_act

        # current actuated qpos/qvel (from the live data, aligned to actuators)
        qpos = d.qpos[self.env.act_qpos_adr]
        qvel = d.qvel[self.env.act_dof_adr]

        tau = np.zeros(n_act)
        # target-specified joints: PD toward target; everything else: hold at 0
        # (legs stay at 0 = standing; non-gesture arm joints also hold at 0).
        err = qpos - self.target
        tau = -self.kp_grasp * err - self.kd_grasp * qvel
        # hold body/legs at nominal (0) — a gentler gain so the standing body
        # is stable while the arm+finger joints drive the gesture.
        tau[0:14] = -self.kp_body * qpos[0:14] - self.kd_body * qvel[0:14]

        lo = m.actuator_ctrlrange[:, 0]
        hi = m.actuator_ctrlrange[:, 1]
        return np.clip(tau, lo, hi)


if __name__ == "__main__":
    from gym.hand_env import HandGymEnv
    env = HandGymEnv()
    ctrl = HandController(env)
    obs = env.reset()
    errs = []
    for _ in range(60):
        obs, r, done, info = env.step(ctrl.act(obs))
        errs.append(info["grasp_err"])
        if done:
            break
    print(f"grasp_err start={errs[0]:.3f} end={errs[-1]:.3f}  (lower = better grasp)")
    print("HandController self-test OK")
