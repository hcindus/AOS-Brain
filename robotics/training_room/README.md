# RP1 Skill Gym — training humanoid skills in simulation

A parallel training system where 12 humanoid motor skills (walk, run, jump,
get-up, roll, squat, …) each learn in their own MuJoCo lane, share knowledge,
and are visualized live at **https://tappylewis.cloud/train.html**.

Built around the open-source **RoboParty RP1** (28-DoF) humanoid, which Myl1Ssa
(the brain) drives through the `BodyAdapter` HAL as Myl2Ssa (the body).

## Architecture

Each skill = **base controller + learned residual**, trained by an evolution
strategy (ES) on CPU:

```
combined_torque(obs) = base_controller(env) + residual(theta, obs)
```

- **base controller** — model-based warm start (a hand-built controller, or a
  `ReferenceTrackingController` that PD-tracks real mocap).
- **residual** — a *small* learned additive torque (linear or a 64-tanh MLP),
  trained by ES to maximize a dense, per-skill reward.
- **reward** — skill-specific: forward progress (walk/run), height gain
  (jump/get-up), squat depth, roll-over progress, or mocap *tracking error*.

Two threads per skill (train + live display), each with its own env.

## The skills (12)

| Tier | Skills | Note |
|------|--------|------|
| 300 (foundation) | balance, recover | MLP residual; shared widest |
| 200 (intermediate) | walk, squat, kneel, sit, climb | |
| 100 (specific) | run, jump, crawl, roll, getup | |

## Knowledge sharing

**Dynamic, maturity-based:** every skill inherits the learned residual of every
skill that has trained *more generations* than it (`_shared_residual`). So the
fast-training skills become the teachers, and improvements cascade down
automatically — no static labels.

## Motion imitation

Real human motion capture is retargeted onto the RP1 and tracked:

1. **Data** — `xuewang/UFO-MotionData` (HuggingFace), the RP1-retargeted LaFAN
   set: 55 clips, 50 Hz, already in RP1 joint space (`robotics/motion_data/ufo/`).
2. **Retarget** — `reference.py` maps the 24-DoF mocap onto our 28-DoF robot
   (single wrist → wrist_pitch).
3. **Track** — `ReferenceTrackingController` PD-tracks the reference; the
   residual + tracking reward (`-‖qpos - ref‖²`) close the dynamics gap.

Skills → reference clips: walk (15 clips), run/sprint (6), jump (3),
fallAndGetUp/ground (6 → get-up/roll), pushAndStumble (recover), etc.

## Running it

```bash
cd robotics/training_room && source .venv/bin/activate
python3 train_server.py        # WebSocket server (served at :8096, proxied by nginx)
```

Dashboard: **https://tappylewis.cloud/train.html** (nginx serves the page,
proxies `/train-ws/` → the server). Deployed as `rp1-training-server.service`.

## Layout

```
robotics/
  rp1/                # 16 cloned RoboParty repos (gitignored)
  training_room/
    gym/              # RP1GymEnv (MuJoCo sandbox)
    controllers/      # base controllers (balance, walk, squat, jump, getup, roll, crawl, ref_track, ik)
    dispatch/         # SkillTrainer, residual (linear/MLP), ES trainer
    train_server.py   # the live server
    train.html        # the dashboard
  motion_data/
    ufo/              # downloaded mocap (gitignored, ~1.2GB)
    reference.py      # loader + skill→clip mapping + 24→28 retarget
    retarget.py       # human keypoints → RP1 legs (IK)
```

## Key findings (hard-won)

- **Tiny feet** (4 contact points, ±5.7° ankle roll) cap static balance — the
  RP1 must *step* to balance; the ZMP/CoP planner is the real answer.
- **Lateral weight-shift** (CoM onto stance foot before lifting the swing foot)
  is what makes walking move forward, not backward.
- **Squat/kneel/sit are dynamic** (free joint drops under gravity), not static poses.
- **Roll/get-up can't be hand-scripted** — they need mocap reference (now solved).
- **Linear residual plateaus**; a 64-tanh MLP breaks the ceiling.

## Next levers

- MLP residual for the per-skill (not just foundation) residuals.
- Graduation gate (blind hold-out + GoR council) wired to auto-promote skills.
- GPU dispatch (UFO/Isaac Lab) for deeper policies.
