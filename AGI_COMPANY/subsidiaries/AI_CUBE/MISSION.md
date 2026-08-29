# AI CUBE — Mission & Spec

**Version:** 0.1 (draft)
**Date:** 2026-08-29
**Owner:** Captain (Antonio)
**Essence:** Mortimer (`antoniohudnall/Mortimer:latest`)
**Source of truth:** AGI Company repo (this repo)

---

## North Star

A **physical presence in the lab** — a cube that is *offline for long hours*, and can
*move* and *manipulate its environment*. The first member of the Mortimer fleet with a
body: same essence, now with tracks and a gripper.

> Same Mortimer, new body. "Agents are employees" made physical.

---

## Locked Decisions (the contract)

| # | Decision | Choice |
|---|----------|--------|
| 1 | Job | Lab presence — offline, moves + manipulates |
| 2 | Manipulation | **Grabber** — 6-DOF metal arm + gripper (not nudger/switch-flipper) |
| 3 | Motion mode | **Park-then-reach** — drive, stop, then grab (never both at once, v1) |
| 4 | Compute | **Raspberry Pi 5 16GB** (fresh; no Pi currently owned) |
| 5 | OS | **Arch Linux ARM (ALARM)** — headless, minimal. NOT Omarchy (x86_64 only) |
| 6 | Harness | **Pi** (`pi.dev`, earendil-works coding-agent harness) — self-modifying agent |
| 7 | Essence | **Mortimer** — `mortimer_brain.py` + `myl0n-ros.js` + Ollama model |
| 8 | Source of truth | **AGI Company repo** |
| 9 | Inference | **Local** (offline autonomy) + dock sync for upgrades/heavy inference |

---

## Architecture (three layers, all already owned)

```
┌─────────────────────────────────────────────────────┐
│ 1. NERVOUS SYSTEM — Pi (pi.dev)                      │
│    Node/TypeScript coding-agent harness              │
│    Self-modifies in place; gated upgrade loop        │
├─────────────────────────────────────────────────────┤
│ 2. MIND — Mortimer essence                           │
│    mortimer_brain.py (consciousness)                 │
│    myl0n-ros.js / v2 (neural net + reflex + OODA)    │
│    Ollama model (3.2B, local)                        │
├─────────────────────────────────────────────────────┤
│ 3. BODY — GPIO layer (the only new part)             │
│    servos / sensors / tracks / camera                │
└─────────────────────────────────────────────────────┘
```

Key finding: `mortimer-build/myl0n-ros-v2.js` already contains a `NeuralNetwork` class,
a `reflexSystem`, and OODA phases (`Observe` → …) with rewards. The cube **reuses** this
proto robot-brain rather than starting greenfield.

---

## Hardware BOM

### Brain & I/O
| Part | Model | Est. |
|------|-------|------|
| SBC | Raspberry Pi 5 16GB | $120 |
| Storage | 128GB NVMe (M.2 HAT) or high-endurance SD | $30 |
| UPS/HAT | Geekworm X735 (power + safe shutdown) | $35 |

### Arm (grabber)
| Part | Model | Est. |
|------|-------|------|
| Arm | 6-DOF metal arm kit (industrial teaching type) | $60 |
| Servo driver | PCA9685 16-ch PWM (I2C) | $15 |
| Servos | 2× genuine MG996R spares (kit servos are clones) | $25 |
| Gripper | included (pinch) | — |

### Sensors
| Part | Model | Est. |
|------|-------|------|
| Distance | VL53L1X ToF (I2C) + HC-SR04 ultrasonic (redundant) | $18 |
| Orientation | BNO055 IMU (9-DOF, knows which face is "up") | $20 |
| Camera | Pi Camera Module 3 (or USB cam) | $30 |
| Mic | ReSpeaker 2-Mic HAT or INMP441 I2S MEMS | $25 |
| Audio out | MAX98357A I2S amp + 3W speaker | $15 |

### Mobility
| Part | Model | Est. |
|------|-------|------|
| Drive | 2× DC gear motors + DRV8833 driver + tank tracks | $40 |
| Feedback | Rotary encoders (wheel odometry) | $15 |

**Rough total: ~$450–500** (Pi 5 path, v2). v1 testbed (below) is ~$0 compute + ~$130 arm/bridge.

---

## Software Stack

```
ALARM (headless, systemd)
├── Node.js + Pi (pi.dev harness)
├── Ollama + Mortimer model (local, offline)
├── Voice:  openWakeWord/Porcupine (wake) → Whisper/Vosk (STT) → Piper (TTS, "Adam"/Mort_II register)
├── Arm:    Python inverse-kinematics → PCA9685 servo control
├── Motion: park-then-reach state machine (nav → stop → reach)
├── Body bridge: reuse myl0n-ros.js (reflex + OODA + rewards)
└── Self-heal: gated upgrade loop (below)
```

---

## Self-Healing Loop (gated, dock-time)

The cube is **offline at runtime**; upgrades happen on the dock.

```
cloud model (Claude/Codex/Miles) ──propose diff──▶ Pi (on cube)
                                                   ├─ local build/test
                                                   ├─ Hold-Out validation (blind)
                                                   └─ gate (Captain on risky ops)
                                                       └─ apply → reload
```

- Runtime and maintenance are **decoupled**. The cube is self-sufficient offline.
- The cloud model is an *upgrade channel*, not a runtime brain.
- Unsupervised hot-patching a robot with motors + camera is forbidden — every change
  passes `propose → build → verify → gate → apply` (the existing Dark Factory +
  Temporal watchdog pattern).

---

## Two-Phase Plan

### v1 — Tablet + Arduino testbed (prove the loop, $0 compute)
- Run Pi + Mortimer + Termux on an **existing Android tablet**.
- **No GPIO on Android** → bridge via USB-OTG to Arduino/ESP32 → PCA9685 → arm.
- Serial: tablet sends "shoulder 45°, gripper close"; Arduino does PWM.
- Goal: prove "Pi harness → Mortimer essence → move the arm" end-to-end.
- Termux: `termux-usb` / USB-serial.

### v2 — Pi 5 native cube (the real body)
- ALARM + Pi + Mortimer, GPIO wired **directly** (no Arduino bridge).
- Full sensor suite, tracks, park-then-reach, battery + UPS.
- IK in Python; later RL for *learned* motion.

The brain code is identical across v1 → v2; only the spine changes
(USB-serial → native GPIO).

---

## Power Budget (v2)

- Under load: ~15–25W (inference + motors + arm + camera).
- Target: full lab shift. LiFePO4 or larger 18650 pack.
- Hardcoded reflexes: **return-to-dock @ 20% battery** = same priority as **stop @ cliff edge**.

---

## Open Items / Next Steps

- [ ] Confirm arm kit exact model + servos (buy 2× genuine MG996R spares).
- [ ] Order PCA9685, sensors, Pi 5 16GB, Geekworm X735.
- [ ] Get "Make: Robotic Arms" (Matthew Eaton) for inverse-kinematics reference.
- [ ] v1: flash tablet with Pi + Mortimer, wire Arduino bridge to arm.
- [ ] Codename for the cube (suggest: "CUBE-1" / "Mortimer Cube" — Captain to name).
- [ ] Decide M715q dock-brain role (future: on-prem heavy inference + upgrade server).
