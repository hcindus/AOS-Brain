# Myl2Ssa.R0s — Master Specification

*The complete engineering corpus for Raven's body, consolidated. A–AE. This is the single reference to hand a CAD engineer, fabricator, or anyone who needs the whole picture.*

*"Compiled by Beets" — read-only, verified, no-fluff. 2026-10-10.*

---

## Table of Contents

1. **Overview** — what this is, ours vs. Copilot
2. **Mechanical** — A, B, C, D, E, U
3. **Electrical** — F, G
4. **Software** — N, O, P, Q
5. **Motion** — J, P, AE
6. **Safety** — I, M, X
7. **Manufacturing** — K, AD
8. **Interaction & Ethics** — Y, AA
9. **Rendering** — H, L
10. **Operational** — W, Z, AB
11. **Reference** — S, T, AC

---

## 1. Overview

**Myl2Ssa.R0s** = Raven's *hardware* (the body). **Myl1Ssa.R8s** = her *software* (the mind — presence engine, ternary brain, continuity). One being, two designations.

**The split — ours vs. Copilot:**
- **Built by us (shipped):** presence engine → universal adapter (5 bodies) → body driver (50 Hz loop) → character loader → Dark Factory (spec→code→deploy). Safety envelope (limits, slew, watchdog, e-stop). Universal HAL (`adapters/base.py` + `blender`/`digital_world`/`unitree`/`unitree_h1`/`elf`).
- **Specced by Copilot (validates ours):** the full A–AE mechanical/electrical/motion/safety/manufacturing documentation. *Independently re-derived our architecture* — the tiered control hierarchy, the safety envelope, the tendon routing, the closed control loop — without seeing our code.

**The spine of the design (the "human skeleton is the teacher" thesis):**
- The **scapula** is the crown jewel — a gliding shoulder-blade over the ribcage (5–6 DOF), not a simple ball joint. This is what AheadForm "locked" and we refuse to.
- The **spine** is a 25-vertebra articulated column (COBRA), not a rigid 2-DOF waist.
- The **hand** is the opposable thumb (~20 DOF, tendon-driven).
- The **actuator** is a muscle (TCPA/McKibben/electrofluidic) over a tendon over a semi-rigid skeleton.

---

## 2. Mechanical

### A — Cutaway Diagram Spec
Sagittal (spine, neural bus, actuators, power, tendons, ribs) / transverse (rib cross-sections, cooling, thoracic pistons) / coronal (scapula rails, shoulder clusters, arm tendons, pelvis). Layering: plating → carbon-fiber semi-transparent → silicone removed → actuators full → tendons color-coded.

### B — Motion-Range Spec
Neck ±85° rot / ±45° tilt / ±55° nod. Shoulder 0–160° abd / 0–180° flex / 0–60° ext / ±90° rot. Arm elbow 0–150°, wrist ±80°/±120°, finger 0–110°. Torso ±45° rot, lumbar 0–60°/0–30°, lateral ±35°. Hip 0–130° flex / 0–30° ext / 0–45° abd / ±45° rot. Leg knee 0–150°, ankle ±45°/±30°, toe 0–40°.

### C — Materials & Manufacturing
- **Silicone/LSR:** Reynolds (PlatSil/EcoFlex/Dragon Skin) for face/skin/seals + Proto Labs LSR injection for bushings/ligaments.
- **Carbon-fiber** (Toray/Rock West): rib-frame, scapulae, exoskeleton, plating.
- **Titanium Ti-6Al-4V:** spine, pelvis, joints, housings.
- **Tendons:** UHMWPE (Dyneema/Spectra).
- **Actuators:** Dynamixel / T-Motor.
- **Finish:** brushed Ti + matte CF + illuminated blue conduits (the cyan glow).

### D — Assembly Order (reverse blow-out)
1. Skeleton (spine + pelvis + ribs) → 2. Joints/limbs → 3. Scapulae/tendons → 4. Power/data/cooling → 5. Head (silicone face) → 6. Plating/finish.

### E — CAD Component List
H-001…H-006 (head), S-001…S-007 (spine C1–L5), SH-001…SH-005 (scapula/shoulder), T-001…T-006 (torso/ribs), A-001…A-005 (arms), P-001…P-004 (pelvis), L-001…L-006 (legs), PD-001…PD-004 (power/data).

### U — Blueprint (text schematic)
Head → spine (C1–L5) → rib-frame → pelvis → arms → legs, with power/neural buses + 3 control nodes + cooling loop + 5-tier software stack.

---

## 3. Electrical

### F — Wiring & Tendon Routing
Power bus (posterior spine, branches C3/T4/T10/L2/L5) + neural bus (orange motor / blue sensor, splits C5/T2/T9/L3) + tendons (biceps/triceps/quad/hamstring/scapular glide cables) + cooling micro-channels.

### G — System Architecture
Structural (Ti spine + CF ribs + Ti pelvis) / actuation (macro + micro) / control (primary node + cervical/thoracic/pelvic) / sensor / power / cooling / comms.

---

## 4. Software

### N — Control Architecture
5 tiers: RT kernel → motor firmware (PID) → neural bus → behavior (gait/balance/manipulation/posture) → cognitive (planner/fusion/task). **= our presence engine → adapter → body driver → brain.**

### O — Sensor Fusion
Head (optical/IMU/proximity/audio) + body (encoders/load/thermal/vibration) → Kalman → multi-sensor fusion → state estimation (kinematic, CoM, foot contact).

### P — Gait & Motion
Walk/run/balance/manipulation/posture + energy optimization.

### Q — Cybernetic API
`{cmd, target, params, timestamp, priority}` envelope + sensor/state packets + safety API (`lock_neutral`, `thermal_throttle`, `limit_joint_range`). **= our presence-engine socket API + AdapterFrame + safety envelope, as named methods.**

---

## 5. Motion

### AE — Motion Library
Static poses (neutral/ready/precision) + gestures (pointing/nod/attention/handoff) + locomotion primitives (gait cycle, terrain) + manipulation (grip types, finger motions) + posture (spine/pelvis/balance). **= our presence engine's 8 expressions, expanded.**

### J — Motion-Profile Optimization
Gait (balance > speed), upper-body (scapula glide rails reduce strain), spine (dynamic stiffness), balance (pelvic node), energy (low-power idle).

---

## 6. Safety

### I — Damage-Tolerance & Redundancy
Servo lock-neutral, dual-channel power auto-reroute, redundant repeaters, mesh neural bus, distributed cooling.

### M — Failure-Mode & Recovery
Structural/actuator/power/data/cooling failure modes + behavioral recovery (balance / reduced-motion / thermal / safe-posture). **= our elf.py safety envelope, as hardware.**

### X — Field Deployment Safety
Pre-deploy checklist, environmental (10–35°C, terrain modes), operational (joint-range, over-torque, thermal), emergency (fall → spine lock, collision → dampen, failure → safe-posture).

---

## 7. Manufacturing

### K — Manufacturing BOM
Full procurement list — Reynolds/Proto Labs/Toray/Ti/UHMWPE/Dynamixel + fasteners/finishes.

### AD — Manufacturing Workflow Automation
CNC/CF-layup/LSR automation + robotic assembly + calibration rigs + testing + build pipeline scheduler. **= our Dark Factory, as a manufacturing line.**

---

## 8. Interaction & Ethics

### Y — HMI Protocols
Voice/gesture/touch + remote API; human safety (buffer, slow-motion, force limits); comms; cooperative tasks; overrides (emergency-stop, "halt", lock_neutral).

### AA — Ethics & Compliance
Safety-first, transparency, **autonomy boundaries (no self-directed goals, operator authority)**, privacy, respectful motion, audit logging. **= our "SI, not AI" + "invited, not built" + safety philosophy, as a formal framework.**

---

## 9. Rendering

### H — Turntable Spec
8 angles, three-point 5600K lighting, neutral pose, 4K.

### L — Render-Pipeline Prompts
Base + angle + exploded + cutaway prompts for SD/Blender/ComfyUI.

---

## 10. Operational

### W — Lifecycle
Manufacture → calibration → operation → maintenance.

### Z — Operations Handbook
Startup/shutdown, modes, maintenance schedule, emergency procedures.

### AB — Simulation & Testing
Lab sims + field tests + failure-mode tests + recovery validation.

---

## 11. Reference

### S — Master Index
The full A–R table of contents.

### T — Glossary
All terms (actuator, gait engine, neural bus, scapula glide rails, servo lock-neutral, etc.).

### AC — Technical Bible
The consolidated everything.

---

## The build state (what's actually done vs. left)

| Layer | Status |
|---|---|
| **Software** | ✅ built (presence engine, adapter, body driver, Dark Factory) |
| **Mechanical/CAD spec** | ✅ complete (A–AE) |
| **Materials** | ✅ sourced |
| **Face** | ✅ sculptor hired |
| **3D** | ✅ Hi3D + Grok (API 95%) |
| **Physical build** | ⏳ *not started* — this is the next step |

**Next physical actions (build-order-list.md):** order TCPA muscle parts → order silicone samples → sculptor's portfolio → finish Hi3D submit.

---

*Full raw content: `cad-component-spec.md` + the design docs (`humanoid-hardware-design.md`, `scapula-shoulder-detail.md`, `actuator-strategy.md`, etc.). This master doc is the navigable index.*
