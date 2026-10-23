"""Load the RP1 MuJoCo model and expose a tidy programmatic view.

The MJCF ships a 28-DoF torque-controlled humanoid: 7-DoF free joint for the
root, then 28 revolute joints (legs, waist, arms) each paired 1:1 with a
torque motor (gear=1, so ctrl == N·m).
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import mujoco
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class ModelView:
    model: mujoco.MjModel
    data: mujoco.MjData
    joint_names: list[str]
    act_names: list[str]
    n_act: int
    root_id: int          # body id of base_link (for height / orientation)
    timestep: float


def load(mjcf_path: str | None = None) -> ModelView:
    path = mjcf_path or os.path.join(
        ROOT, "..", "rp1", "RP1_description", "mjcf", "rp1_flat.xml"
    )
    path = os.path.abspath(path)
    model = mujoco.MjModel.from_xml_path(path)
    data = mujoco.MjData(model)

    joint_names = [
        mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
        for i in range(model.njnt)
    ]
    act_names = [
        mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i)
        for i in range(model.nu)
    ]
    root_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "base_link")

    return ModelView(
        model=model,
        data=data,
        joint_names=joint_names,
        act_names=act_names,
        n_act=model.nu,
        root_id=root_id,
        timestep=model.opt.timestep,
    )
