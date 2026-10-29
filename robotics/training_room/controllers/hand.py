"""HandController — base PD hold for the hand model + grasp curl.

Holds the 28 body joints at nominal (so the body stands) and curls the 12
finger actuators toward the grasp target. The learned residual (ES) refines
the grasp — so the hand trains the *precision* of the grasp on top of a naive
"close everything" base, exactly like the reference-tracking skills.

Obs layout (HandGymEnv): [height, quat(4), vel(3), angvel(3), qpos(40), qvel(40)]
"""
from __future__ import annotations

import numpy as np

from gym.hand_env import GRASP_TARGET, FINGER_ACT


class HandController:
    name = "hand"

    def __init__(self, env, kp_body: float = 60.0, kd_body: float = 4.0,
                 kp_grasp: float = 40.0, kd_grasp: float = 2.0):
        self.env = env
        self.view = env.view
        self.kp_body = kp_body
        self.kd_body = kd_body
        self.kp_grasp = kp_grasp
        self.kd_grasp = kd_grasp

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
        # body joints (0..27): PD hold toward nominal (0)
        tau[0:28] = -self.kp_body * qpos[0:28] - self.kd_body * qvel[0:28]
        # finger joints (28..39): PD toward grasp target
        finger_err = qpos[28:40] - GRASP_TARGET
        tau[28:40] = -self.kp_grasp * finger_err - self.kd_grasp * qvel[28:40]

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
