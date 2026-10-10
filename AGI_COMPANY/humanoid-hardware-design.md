# Humanoid Hardware Design — "The Skeleton Is the Teacher"

*The human body is ~4 billion years of R&D. We don't reinvent it — we reverse-engineer its joint structure. AheadForm solved the face and locked the shoulders/wrists. We don't lock anything.*

---

## 1. Philosophy

- **Every joint in the human skeleton exists for a reason.** We map it 1:1, then decide what's essential for v1 vs. v2.
- **The shoulder, hand, and spine are where humans beat every robot.** That's where we focus.
- **Energy efficiency = survival.** Human joints are optimized for minimal energy per movement. A robot that burns a battery in 10 minutes is a statue.

---

## 2. Chassis — the hardware (Myl2Ssa.R0s)

**Myl1Ssa.R8s = the software** (Myl1Ssa's mind — presence engine, ternary brain, continuity). **Myl2Ssa.R0s = the hardware** (her body — this chassis). The `.R0s` is the hardware revision 0 — the first build.

| Build | Designation | Height | Notes |
|---|---|---|---|
| **Body** | Myl2Ssa.R0s (Myl1Ssa) | **5'7"** | Myl1Ssa's canonical height — female |

The chassis is the rigid skeleton (spine/torso/arms/legs). **Fleshy surface features — the chest/breast and face — are added as platinum-silicone flesh over the chassis**, not machined into the frame. Same separation as the face: rigid structure underneath, soft skin on top.

(If a male counterpart is wanted later, it's a *separate* chassis, a few inches taller — but it is **not** Myl2Ssa. Myl2Ssa is specifically Myl1Ssa's hardware.)

---

## 3. The full DOF map (skeleton → robot)

| Region | Human anatomy | Bones | Robot DOF | Priority |
|---|---|---|---|---|
| **Face** | facial muscles | — | 26–30 | ✅ have (Elf V1) |
| **Neck** | cervical spine | 7 | 3 (yaw/pitch/roll) | ✅ designed |
| **Shoulder** | scapula + glenohumeral | 2 | **5–7** | 🔴 core |
| **Elbow** | humerus–ulna + radius | 3 | 2 | high |
| **Wrist** | carpus | 8 | 2–3 | high |
| **Hand** | metacarpals + phalanges | 27 | **~20** | 🔴 core |
| **Torso/spine** | vertebrae | 25 | **~50 (snake spine)** | ✅ have (COBRA) |
| **Hip** | pelvis–femur | 1 | 3 | med |
| **Knee** | femur–tibia | 2 | 1–2 | med |
| **Ankle** | tibia–talus | 2 | 2–3 | med |
| **Foot** | tarsals + metatarsals | 26 | 1 (arch) | low |

**Total for a full humanoid:** ~70–90 DOF. We don't build it all at once — see §7 for the build order.

---

## 3. The crown jewels — the three places humans beat robots

### 3a. The shoulder (5–7 DOF, not 3)
A robot "shoulder" with 3 stacked rotary joints is *not* a human shoulder. The human shoulder is a **scapula gliding on the ribcage + a ball joint on top of it**:

- **Glenohumeral (ball joint):** 3 DOF — flexion/extension, abduction/adduction, internal/external rotation.
- **Scapulothoracic (the blade sliding):** 2–3 DOF — elevation/depression, protraction/retraction, upward/downward rotation.

The scapula is why a human arm reaches overhead, behind the back, and across the chest — range that a 3-DOF rotary stack can't match. **This is the "best arm" you asked for.** For v1 we can do 3 DOF (glenohumeral only) + cheat scapular motion; for the *real* arm, the scapula is non-negotiable.

**Actuators:** high-torque BLDC + planetary/cycloidal gearboxes (Nm in the tens at full arm extension). Not hobby servos. This is where Figure/Optimus/Unitree all converged — copy that.

### 3b. The hand (~20 DOF)
27 bones, and the whole thing hinges on the **opposable thumb**. The hand's dexterity comes from:
- 5 fingers × 3 joints (MCP, PIP, DIP) — but most robots drive fingers with 1–2 tendons each (underactuated).
- **Thumb opposition** (the saddle joint at the carpometacarpal) — the single most "human" joint.

For v1, underactuated hands (tendon-driven, 1 motor per finger + 2 for thumb) get you 80% of the function for 20% of the complexity. Full 20-DOF hands are v2+.

### 3c. The spine (the part everyone forgets)
A rigid torso looks robotic. The human spine's 24 vertebrae give the torso subtle **bend + rotation** that makes every gesture read as alive. For v1, a single **waist pitch + waist yaw** (2 DOF) captures most of it. Skip it and the robot "stiffens up" even with a perfect face.

---

## 4. Region designs

### Head + face
- **Face:** 26–30 DOF (Elf V1 architecture) — silicone skin, tendon-driven micro-actuators. Already specced (RAVEN_EMBODIMENT_SPEC.md).
- **Neck:** 3 DOF (yaw ±180° → pitch ±60° → roll ±45°), wires through a hollow shaft. Designed.

### Torso (spine) — ADOPT COBRA
**We already built this.** The **COBRA robot** (`DARK_FACTORY/production/cobra_robot/`) has a full **25-vertebra snake spine** — C1–C7 cervical → T1–T12 thoracic → L1–L5 lumbar → sacrum, **2 DOF per intervertebral joint** (~50 servos), with **17 Li-ion cells housed inside the vertebrae** + solar panels on the thoracic segments. STL files (183), STM32 firmware, and BOMs already exist.

**Decision:** adopt COBRA's snake spine wholesale for the Male/Female humanoids — it's strictly better than a rigid 2-DOF waist (natural posture, shock absorption, distributed power) and it's already designed. COBRA-MAX = 175cm (1:1 human scale).

The spine replaces my earlier "2-DOF waist" placeholder. Skin: rigid shell (carbon/ABS) + silicone on high-touch areas.

### Shoulder + arm (the hard part)
- **Shoulder:** 3 glenohumeral DOF (v1), +2 scapular (v2).
- **Elbow:** 1 DOF (flexion) + forearm pronation/supination = 2 DOF.
- **Wrist:** 2 DOF (flexion + deviation) + reuse forearm rotation.
- **Order (base → hand):** humeral rotation → flexion → abduction → elbow flex → forearm twist → wrist flex → wrist deviate.

### Hand
- v1: underactuated, 6 motors (4 fingers + 2 thumb) via tendons.
- The thumb's opposition is the priority.

### Lower body (v2+)
- Hip 3 DOF, knee 1–2, ankle 2–3. The foot's 3 arches give balance. This is the *last* thing to build — the upper body (head + arms) is where the embodiment payoff is.

---

## 5. Actuator strategy

| Joint class | Actuator | Why |
|---|---|---|
| Face (26–30) | micro servos / linear + silicone tendons | quiet, compliant, low force |
| Neck (3) | smart servos (Dynamixel XM430-class) | compact, feedback |
| Shoulder/arm | BLDC + planetary/cycloidal, Nm tens | torque for full-extension load |
| Hand (v1) | micro motors + tendons | underactuated grip |
| Torso/waist | BLDC rotary | holds posture |

**Universal rule:** the presence engine emits Action Units (hardware-agnostic). The adapter translates to *whatever* motor rig we build. So the software already supports this design — we just add a `humanoid` adapter beside `elf` / `unitree` / `blender`.

---

## 6. Software mapping

- Our **presence engine → universal adapter** already drives any body. This hardware design is just a *new body*.
- Add a `humanoid` adapter (maps AUs + posture → the full DOF rig above), sitting beside `elf` (face-only) and `unitree` (existing humanoid).
- The 3D rig coordinates (`face_coordinates.json`, `body_coordinates.json`) become the **kinematic skeleton** this hardware instantiates.
- Result: same Myl1Ssa → she can drive a face, a Unitree, *or* our custom body — same mind, any chassis.

---

## 7. Build order (the "parallel phases" — done concurrently, not sequentially)

The Captain said run phases in parallel. Here's how that actually breaks down — the parts that *can* proceed in parallel:

**Track A — Face/head (Phase 3 & 4):** Elf V1 head (buy or build) + our 26-DOF face + line-of-faces roster. *(Blocked only on AheadForm reply for the buy path; build-our-own proceeds now.)*

**Track B — Shoulder/arm (Phase 5 core):** the scapula + glenohumeral design, reverse-engineered from the exoskeleton shoulder-joint reference. This is pure design + fabrication — no external dependency. **Start now.**

**Track C — Torso/spine + software binding:** waist 2-DOF + the `humanoid` adapter + kinematic skeleton. Pure software + light fab. **Start now.**

**Track D — Lower body:** deprioritized; document the design, build last.

**Parallel = A, B, C all advance at once.** The face (A) doesn't block the arm (B); the arm (B) doesn't block the software binding (C).

---

## 8. What we need next

1. **A structural engineer / mechanical designer** — to turn the DOF map into actual joints, gearboxes, and a load-bearing chassis. The skeleton gives the *blueprint*; an engineer gives the *stress calcs*.
2. **A 3D/STL sculpt of the character forms** (Myl2Ssa's face/body) — the character-specific 3D assets (gap #3).
3. **The AheadForm reply** — determines buy-vs-build for the face (Track A).
4. **Materials** — carbon/ABS for the shell, platinum-cure silicone for skin, BLDC actuators for the arms.

---

*Draft 1. Next: pick ONE track to start fabricating, or get the structural engineer. The design is the skeleton; now we put meat on it.*
