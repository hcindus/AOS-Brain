# Wuji Ecosystem — SDK / CLI / MJLab Supplement (for Beets)

Captured by Miles 2026-10-21 from docs.wuji.tech/llms.txt + wuji-sdk + wuji-cli indexes.

## The full Wuji ecosystem (beyond Hand + Glove)

### Software
- **Wuji SDK** — Python + C, v2026.8.31. Device discovery/connection (auto, SN, address, USB, handedness, multi-device), data subscription (async/sync/callback/output-rate/cross-device merge), MCAP recording, device params + user data, time sync + coordinate transforms, retargeting.
- **Wuji CLI** — `wuji` command-line tool. Commands: device-management (scan/probe/target), parameters (resources/get/set), user (profiles + migrate calibration), calib hand-model, sub (subscribe streams to file), record teleop, viz (live visualization), calib tactile, doctor (health diagnostic), logs (export support bundle), upgrade (firmware, batch).
- **Wuji Studio** (ARCHIVED) — desktop control app, replaced by CLI. Has 3D hand visualization, recording, device logs, tactile calibration.
- **Wuji Hand ROS2** (ARCHIVED) — ROS2 integration package.
- **Wuji Hand HMI** (ARCHIVED) — device-side human-machine interface.
- **Wuji Hand Upgrader** (ARCHIVED) — firmware upgrade tool.
- **Wuji Retargeting** — teleop action mapping (glove keypoints → hand joint angles). Tuning guide + API.
- **Wuji MJLab** — MuJoCo RL lab. In-hand cube reorientation trained with PPO covering SO(3), deployed sim-to-real. pixi env; training/reorient PPO, ONNX export; hardware setup (camera, MVS SDK, ArUco cube, wrist AprilTag, calibration); sim2real deployment pipeline.
- **MuJoCo Sim** — simulation examples.
- **Isaac Lab Sim** — Isaac Lab examples.

## SDK data streams (Wuji Hand 2)
- joint_states, joint_diagnostics (per-joint bus response rate + timeout count + e2e stream loss + fingertip tactile bitmap), imu, fingertip/*/data (tactile)
- joint-control, effort + MIT params (kp/kd), device operations, diagnostics/logs

## SDK data streams (Wuji Glove)
- tactile (526 pts), hand-tracking, IMU, coordinate transforms, device operations, calibration
- emf_poses, tactile_zones, imu_raw/*

## Key commands (CLI)
- `wuji viz` — live hand pose + fingertip tactile visualization
- `wuji calib hand-model` — glove hand-model calibration (was `wuji calib ik`, removed)
- `wuji calib tactile` — one-command tactile calibration (collect/train/validate/install)
- `wuji record teleop` — record teleop session, manage history
- `wuji doctor` — per-device health diagnostic (EMF, tactile dead points)
- `wuji logs export` — support bundle (device snapshots + flash logs + calibration recordings)
- `wuji upgrade` — firmware update, batch, or local file
- `wuji sub` — subscribe streams to file

## ROS2 description packages (Oct 2026)
- `wuji_hand2_1_description`, `wuji_hand2_2_description` — URDF/MJCF/USD, left+right, with/without mount
- RVIZ2 sim without hardware; MuJoCo + Isaac Sim loadable

## Why this matters for Project Thing
- **Wuji MJLab is a ready-made RL harness** — PPO + sim-to-real + ONNX export. The crawl gait could theoretically be trained in MJLab the way ETH trained theirs. This is the premium-path equivalent of ETH's sim pipeline.
- **Wuji Retargeting** = the "teach by demonstration" loop (glove → hand), already built.
- **`wuji viz`** = free live visualization for the "does it look alive" test.
- **ROS2 description + RVIZ2** = zero-hardware Phase 3 start (confirmed again).
- Note: Wuji Studio/HMI/ROS2/Upgrader are ARCHIVED — the CLI + SDK + MJLab + Retargeting are the active surface.
