# Wuji Tech — Raw Reference Dump (for Beets compilation)

Captured by Miles on 2026-10-21 for Project Thing. Sources:
- https://docs.wuji.tech/docs/en/wuji-hand/latest/overview
- https://docs.wuji.tech/docs/en/wuji-glove/latest/
- https://docs.wuji.tech/docs/en/release-notes
- https://wuji.tech/en/

## Wuji Hand 2 (2.2 Beta, non-tactile prototype)
- 20 active DoF (4 per finger), full opposition + lateral abduction
- Back-drivable direct-drive rotary joints, FOC vector control
- MIT force-position hybrid control, user-tunable params
- Control: 1000 Hz × 20 axes
- Communication: RJ45 Ethernet 100BASE-TX
- Power: 11-13V DC (12V nominal), 12V 20A adapter (>=200W), XT30 + RJ45
- Weight: 800g curb (650g bare hand, 70g base separately), 180×80×40mm
- SDK: Python + C, joint-level; device discovery, state read, command output
- Sim models: URDF, MJCF, USD (MuJoCo, Isaac Sim), incl. fingertip soft-pad model
- Teleop demo via Wuji Glove (cross-product)
- Three layers: Skeleton (load-bearing) / Soft pad (compliance) / Skin (protection, no sensing)
  - SKIN is user-removable and replaceable; NEVER run without skin fitted
- Back-of-hand RGB status light (breathes when idle: white breathing=ready, blue=powering up, white solid=running, yellow/red=warning/fault)
- Fingertip soft-pad hardness still being tuned; skin design not finalized (2.2 Beta)
- Min grasp diameter 0mm; thumb supports opposition
- Finger lengths: index/middle/ring ~137mm, little ~134mm, thumb ~140mm
- 300K cycle lifespan, 80cm drop test, impact-resistant (twist-lock + slot locking)

## Wuji Glove (teleoperation / data glove)
- Intelligent data glove for robotic teleoperation + HCI
- 526 touch points, 120 FPS real-time tactile + pose capture
- IMU + hand tracking
- MCAP recording; offline pipeline (recompute hand products + IMU fusion)
- Calibration: hand-model + tactile contact
- SDK: data subscription, merge, rate-limit; Python + C
- Firmware v0.12.0 (teleop glove)

## Release notes (Oct 2026) key facts
- 2026-10-12: Wuji Description → Hand 2.1 + 2.2 ROS2 packages (wuji_hand2_1_description / wuji_hand2_2_description)
- SDK/CLI support Ubuntu 20.04+ x86_64 + arm64; Python 3.8+
- Hand 2 firmware v2.12.0; Glove firmware v1.0.3; SDK v2026.10.12 (`pip install wuji-sdk`)
- Default SDK port 50001 (was 7447) since firmware v2.7.0 / Sept 2026
- Feed-forward compensation enabled by default (units shipped Oct 2026+, firmware v2.10.0)
- kd default 0.1, kp = 5.0 (MIT impedance)

## Wuji company
- sales@wuji.tech (pricing/purchase), support@wuji.tech
- HQ Shenzhen (Bao'an COFCO Chuangxin R&D Center) + Beijing (Haidian Tsinghua Tongfang)
- Products: Wuji Hand, Hand 2, Glove

## Related: ETH Zurich walking hand (prior art, Oct 2026)
- Soft Robotics Lab (Robert Katzschmann; PhD candidate Amirhossein Kazemipour)
- Off-the-shelf Wuji Technology hand + 80g backpack (battery + IMU + Raspberry Pi Zero)
- Reinforcement learning in simulation → fingertip walking, turning, pushing, righting, 14 surfaces
- "Virtual springs" gait (each finger custom target position)
- Hand asymmetry (finger lengths, opposable thumb) = key challenge
- Earlier attempts: EPFL LASA + Nature paper s41467-025-67675-8
