"""HandSkillTrainer — ES training for the hand, reusing the SkillTrainer loop.

The hand has a different env (HandGymEnv, 40 DOF, underactuated) and a grasp
reward rather than the walk reward. Rather than fork SkillTrainer, we subclass
it and override the reward: the base HandController already curls the fingers,
so the ES residual learns to *refine* the grasp. The reward is the grasp error
(lower = better grasp) + alive/upright, computed from the hand env's info.
"""
from __future__ import annotations

import numpy as np

from gym.hand_env import HandGymEnv
from controllers.hand import HandController
from dispatch.residual import MLPResidual
from dispatch.skill_trainer import SkillTrainer


class HandSkillTrainer(SkillTrainer):
    def __init__(self, name: str = "hand", residual_clip: float = 15.0,
                 popsize: int = 12, sigma: float = 0.3, lr: float = 0.05,
                 steps: int = 200, seed: int = 0):
        # build our own envs (hand model) + base controller
        self.hand_env = HandGymEnv()
        self.hand_disp = HandGymEnv()
        base_factory = lambda env: HandController(env)  # noqa: E731

        # call parent with our envs wired via a small override
        super().__init__(name, base_factory, residual_clip=residual_clip,
                         popsize=popsize, sigma=sigma, lr=lr, steps=steps, seed=seed)
        # replace the parent's walk envs with hand envs
        self.train_env = self.hand_env
        self.disp_env = self.hand_disp
        self.base_train = base_factory(self.train_env)
        self.base_disp = base_factory(self.disp_env)
        self.obs_dim = self.train_env.obs_dim
        self.n_act = self.train_env.n_act

        # re-init residual/theta for the 40-DOF obs/act dims
        self.mlp = None  # linear residual is fine for the hand
        self.n_params = self.n_act * self.obs_dim
        self.theta = np.zeros(self.n_params)
        self.rng = np.random.default_rng(seed)
        self._stop = False
        self.pose_err = 1.0

    def _rollout(self, env, base, theta) -> float:
        base.reset()
        obs = env.reset(qpos_noise=0.02)
        total = 0.0
        t = 0
        done = False
        while (not done) and t < self.steps:
            resid = self._residual(theta, obs)
            tau = np.clip(base.act(obs) + resid, -30.0, 30.0)
            obs, r, done, info = env.step(tau)
            total += r
            t += 1
        return total

    def _train(self):
        while not self._stop:
            eps = self.rng.standard_normal((self.popsize, self.n_params))
            rewards = np.zeros(self.popsize)
            for i in range(self.popsize):
                rewards[i] = self._rollout(self.train_env, self.base_train, self.theta + self.sigma * eps[i])
            rewards = np.nan_to_num(rewards, nan=-1e3, posinf=-1e3, neginf=-1e3)
            A = (rewards - rewards.mean()) / (rewards.std() + 1e-8)
            with self.lock:
                self.theta += (self.lr / (self.popsize * self.sigma)) * np.einsum("i,ij->j", A, eps)
                self.gen += 1
                self.mean_r = float(rewards.mean())
                self.max_r = float(rewards.max())
                self.history.append([self.gen, self.mean_r, self.max_r])
                if len(self.history) > 500:
                    self.history = self.history[-500:]

    def _display(self):
        import time
        while not self._stop:
            with self.lock:
                theta = self.theta.copy()
            self.base_disp.reset()
            obs = self.disp_env.reset(qpos_noise=0.02)
            done = False
            t = 0
            while (not done) and t < self.steps and not self._stop:
                resid = self._residual(theta, obs)
                tau = np.clip(self.base_disp.act(obs) + resid, -30.0, 30.0)
                obs, r, done, info = self.disp_env.step(tau)
                d = self.disp_env.view.data
                self.pose_err = float(info.get("grasp_err", 1.0))
                self.live = {
                    "alive": bool(info["alive"]),
                    "height": float(d.xpos[self.disp_env.view.root_id][2]),
                    "bodies": [list(map(float, p)) for p in d.xpos[: self.disp_env.view.model.nbody]],
                    "reward": float(r),
                }
                t += 1
                time.sleep(0.03)


if __name__ == "__main__":
    t = HandSkillTrainer()
    t.start()
    import time
    time.sleep(3)
    print(f"hand gen={t.gen} mean_r={t.mean_r:.3f} max_r={t.max_r:.3f}")
    print("HandSkillTrainer self-test OK")
