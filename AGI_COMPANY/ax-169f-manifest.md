# AX-169F — Cybernetic Mannequin (Female Profile / Hourglass 37-27-39)

**Compiled from:** orthographic views + MyI1Ssa.R8s / MyI2Ssa.R0s architecture diagrams.
**Scale:** orthographic 1:5.
**Transparency:** all systems transparent for diagnostic visibility — no epidermal layer / skin texture.

## Headline targets
- **Dry mass target:** ≈ 38.7–61.4 kg (config-dependent).
- **Total DOF:** ≈ 186–312 (architecture-dependent).
- **Identity/Mind:** locked identity (TracRay + Ternary Qbit).

---

## 1. High-Level System Manifest

| Layer | Component / Module | Key Specs / Notes | Status |
|-------|--------------------|-------------------|--------|
| Identity / Mind (Software) | Core Identity & Memory | TracRay + Ternary Qbit | Locked identity |
| | Affect & Energy | Cortex + Thyroid | Energy/affect modulation |
| | Expression & Gating | Kidney | Expression control |
| | Generation | Uterus / Agent Factory | — |
| | Body Schema Organ (NEW) | Real-time joint, contact, temp, energy model | Bridges Mind ↔️ Seam |
| Seam / Interfaces | Motion Verb Layer (NEW) | present \| orient \| reach \| shift \| step \| settle; Affect-modulated + Safety-constrained | — |
| | Safety Contract (NEW) | Living invariants; Machine can say no; visible to affect system | — |
| | Dual-Heart Arbitration (NEW) | Physical pump (hard real-time) ↔️ Affect cadence (within safe band) | — |
| Body / Hardware | 5-Tier Control Stack + Impedance / whole-body OSC | — | — |
| | Skeleton + Actuators | Scapula 5–6 DOF • COBRA Spine • Hands TCPA/McKibben + UHMWPE | Primary structure |
| | Presence Engine | Affect → 30-motor expression; 32 face + 21 body joints | — |
| | Unified Thermal-Vascular Service Core (NEW) | Loop + peripheral capillary bed • Thyroid sole thermostat • 33–36 °C surface | Dual-loop |
| | Structural Battery — Phased (NEW) | P1 conventional pack • P2 hybrid embedded • P3 load-bearing | — |

### Recommended Build Order (Risk-Reduced)
1. Static structure + Scapula + COBRA spine
2. Single arm + hand (full DOF)
3. Presence controller + Dual-heart + Thermal loop (fixed torso)
4. Bipedal locomotion
5. Full skin + vascular

---

## 2. Bill of Materials

### Structural Frame & Skeleton
- **Primary structure:** Ti-6Al-4V (titanium alloy) + carbon fiber hybrid
- **Cranial Shell:** smooth mannequin head, no facial detail, structural transparency
- **Scapula (Articulated):** 5–6 DOF, Ti-6Al-4V / carbon fiber, ball socket + glenoid actuation (×2)
- **COBRA Spine:** 25 vertebrae, Ti-6Al-4V segments, carbon fiber damping, integrated sensor bus (continuous omni-axial bio-inspired robotic actuator)
- **Pelvis / Hip:** articulated, 3 DOF
- **Lower limb frames:** femur, tibia/fibula equivalents (Ti-6Al-4V / CF)
- **Foot:** Ti-6Al-4V frame, carbon fiber sole plate, articulated toes (14 DOF total)
- **Articulations:** ballistic-grade, all joints

### Actuation System
- **Muscle actuators:** TCPA / McKibben style (pneumatic)
  - Red: Extensor / Flexor (or Flexor / Warm)
  - Blue: Adduction / Rotation (or Extensor / Cool)
  - Braided textile shell
- **Tendons:** UHMWPE (Dyneema® equivalent) — high strength / low stretch, over muscle bundles
- **Hand actuators:** full TCPA/McKibben + UHMWPE (12+ DOF per hand)

### DOF Summary (approximate)
| Joint | DOF |
|-------|-----|
| Shoulder (Scapula) | 5–6 |
| Elbow | 2 |
| Wrist | 3 |
| Hand | 12+ |
| Hip | 3 |
| Knee | 1 |
| Ankle | 2 |
| Spine | continuous / multi-DOF (25 vert.) |
| Toes | 14 total |
| Face/expression | ~32 motors (Presence Engine) |

### Thermal-Vascular & Power
- **Dual-Heart Module / Pump:** parallel circulatory assist (×1–2), hard real-time physical pump
- **Thermal-Vascular Tubing:** micro-channel / dual-loop for heat exchange + nutrient/thermoregulatory fluid; orange/yellow in diagrams
- **Thyroid:** sole thermostat (33–36 °C surface target)
- **Power/Data:** distributed, redundant; Structural Battery (phased)
- **Sensors:** integrated sensor bus (spine), contact/temp/joint/energy (Body Schema), cyan points

### Dimensions & Mass Targets
- **Height:** 169 cm (5 ft 6.5 in)
- **Bust:** 37 in (94.0 cm) @ nipple line
- **Waist:** 27 in (68.6 cm) @ narrowest
- **Hips:** 39 in (99.1 cm) @ widest
- **Mass (dry):** 38.7 kg (base) → 61.4 kg (full)
- **Proportions:** Hourglass 37-27-39
- **Tolerance:** all dims ±0.5 cm

### Control & Software Interfaces
- 5-Tier Control Stack + Impedance / whole-body OSC
- Presence Engine (Affect → expression mapping)
- Motion Verb Layer primitives + Safety Contract
- Dual-Heart Arbitration layer

### Legend / Color Coding
- **Red:** muscle actuator (extensor/flexor OR flexor/warm)
- **Blue:** muscle actuator (adduction/rotation OR extensor/cool)
- **White/Gray:** UHMWPE tendon (tension)
- **Orange/Yellow dashed:** thermal-vascular tubing
- **Hatched:** titanium / carbon fiber structure
- **Cyan:** sensor / data / rotation points

### Notes & Constraints
- All systems transparent for diagnostic visibility.
- Zero organic tissue; biomimetic mobility, strength, thermoregulation.
- **Identity Locked, Expression Free** architecture.
- Drawn refs: Axion Dynamics Engineering (2024-05-20), Rev A1 (2024-05-18).

---

---

## 2b. Exploded Sub-Assemblies (hierarchical)

### 1. Single Arm Sub-Assembly (Full DOF) — ≈ 22–23 DOF
Shoulder 5–6 + Elbow 2 + Wrist 3 + Hand 12+.
- **1.1 Scapula / Shoulder Complex (5–6 DOF):** articulated scapula plate (Ti/CF), ball-socket + glenoid, primary actuator cluster (red flexor/extensor + blue adduction/rotation), UHMWPE anchors, sensor bus node, thoracic/cobra-spine attachment.
- **1.2 Upper Arm (humerus):** Ti/CF structural tube, embedded muscle bundles (braided shell), parallel UHMWPE tension members, thermal micro-channel routing, proximal/distal joint interfaces.
- **1.3 Elbow (2 DOF):** ballistic hinge/pivot, flexor/extensor pair (red), tendon pass-through, encoder/position sensor.
- **1.4 Forearm (radius/ulna):** dual Ti/CF members, rotation + fine-control actuator bundles, UHMWPE conduits, thermal loop continuation.
- **1.5 Wrist (3 DOF):** multi-axis (flex/ext + deviation + rotation), compact actuator set, sensor cluster.
- **1.6 Hand (12+ DOF):** CF/Ti palm plate, digit assemblies (fingers+thumb) w/ individual TCPA/McKibben, per-digit UHMWPE tendon network, articulated phalanges (ballistic joints), fingertip contact/force sensors, optional micro-vascular loops.
- **Note:** mount scapula first, cascade distal; full arm buildable/testable standalone (Phase 2).

### 2. COBRA Spine Segment (25 vertebrae, modular 3–5 groups)
- **2.1 Vertebral body:** Ti-6Al-4V segment, central canal (sensor bus/thermal lines).
- **2.2 Intervertebral coupling:** CF damping/compliance, ball/multi-axis surfaces, optional UHMWPE straps.
- **2.3 Actuation:** localized TCPA/McKibben or continuum actuators (omni-axial).
- **2.4 Sensor bus:** continuous data/power backbone, local joint-angle/load/temp sensors per level.
- **2.5 Thermal-vascular pass-through:** micro-channel segments, quick-connect fittings.
- **2.6 End interfaces:** cervical plate, thoracic/lumbar transition plates, rib/scapula hardpoints.
- **Note:** build lumbar-upward or modular stacks; continuous bus + thermal continuity (Phase 1).

### 3. Dual-Heart Module + Thermal-Vascular Core
- **3.1 Dual-Heart pump:** primary (hard real-time) + secondary parallel assist, drive electronics, Ti/CF thoracic cradle, redundant valving manifolds.
- **3.2 Thermal-vascular loop:** main dual-loop orange/yellow micro-channel network, peripheral capillary bed, heat-exchange sections, quick-disconnect + isolation valves.
- **3.3 Thermostat & control:** Thyroid (sole thermostat), temp/flow sensors, local node → Dual-Heart Arbitration.
- **3.4 Fluid management:** reservoir/expansion, filtration/conditioning, charge ports.
- **3.5 Integration:** thoracic/spine mounts, redundant power/data, Body Schema sensor feed, arbitration (pump ↔ affect cadence).
- **Note:** install after structure+scapulae, before full limb population (Phase 3).

### 4. Hand Only (Full DOF) — 12+ DOF per hand
- **4.1 Palm plate:** Ti/CF base, actuator bosses, tendon channels, thermal feed ports, 3-DOF wrist flange.
- **4.2 Thumb:** metacarpal + 2–3 phalanges, red flexor / blue abductor-rotator, UHMWPE pairs, tip contact sensor.
- **4.3 Fingers ×4 (index/middle/ring/little):** metacarpal stub + 3 phalanges each, red flexor/extensor pair, UHMWPE tension members, lateral compliance, fingertip sensor.
- **4.4 Shared:** central tendon plate, micro-channel loop, sensor bus node, optional capillary extensions.

### 5. Foot Structure — 14 DOF (toes) + 2 DOF ankle
- **5.1 Ankle/talus:** 2-DOF ballistic (dorsi/plantar + inversion/eversion), tibia load-path, force/angle/contact sensors.
- **5.2 Main foot frame:** Ti-6Al-4V chassis, arch reinforcement, tendon/actuator pass-throughs.
- **5.3 Sole plate:** CF high-stiffness/low-weight, traction texture (no skin), thermal channels.
- **5.4 Toes (14 DOF):** hallux multi-segment + 4 lesser toes (2–3 phalanges each), compact TCPA/continuum, UHMWPE, tip sensors.
- **5.5 Shared:** sensor bus extension, thermal loop termination, redundant sole load sensors.

### 6. Cranial Shell
- **6.1 Outer shell:** smooth mannequin-form, no facial features, structural transparency, cervical/COBRA flange.
- **6.2 Internal reinforcement:** Ti/CF lattice/ribs, Presence Engine motor mounts, sensor bus entry.
- **6.3 Pass-throughs:** power/data bulkheads, thermal-vascular feed, alignment pins/quick-lock.
- **6.4 Optional mounts:** Presence Engine 32-motor bases, local processing/sensor nodes.

### 7. Presence Engine (32 face motors + 21 body joints)
- **7.1 Central Presence Controller:** affect-input processing node, Safety Contract visibility, power/data distribution.
- **7.2 Facial Motor Array (≈32):** micro-actuators/compact TCPA on cranial lattice, tendon/direct-drive, local encoders.
- **7.3 Body Joint Expression Drivers (21):** distributed driver modules for selected spine/scapula/limb DOF, impedance control, affect-modulated.
- **7.4 Sensor/feedback:** joint angle/torque, affect-state monitoring, cyan → Body Schema.
- **7.5 Integration:** Dual-Heart Arbitration link, Motion Verb Layer input, cranial/spine hardpoints.
- **Note:** install after cranial shell + skeleton (Phase 3). Motors sized for visible presence, not force.

### 8. Presence Engine — 32-Motor Face Map
| Group | Motors | Function |
|-------|--------|----------|
| Forehead / Brow | 1–6 | brow elevation, frown, surprise |
| Eye / Eyelid / Orbicularis | 7–14 | open/close, squint, gaze accent |
| Nose / Cheek | 15–20 | nose wrinkle, cheek raise, sneer |
| Mouth / Lips | 21–28 | smile, pursing, frown, mouth shape |
| Jaw / Temporal | 29–32 | jaw drop, lateral shift, tension |

### 9. Presence Engine — 21 Body-Joint Expression Drivers (actuator mapping)
| # | Segment | DOF | Role |
|---|---------|-----|------|
| 1 | Upper Cervical C1–C2 | 2 (nod+tilt) | head nod/tilt |
| 2 | Mid-Cervical | 1 (yaw) | head turn |
| 3–5 | Upper Thoracic COBRA | 3 (flex/ext/lat) | upper-torso lean, shoulder-set |
| 6–8 | Mid-Thoracic COBRA | 3 (flex/ext/twist) | torso twist, breathing cue |
| 9 | Lower Thoracic/Lumbar | 1 (flex) | posture shift |
| 10–11 | Left Scapula | 2 (elev+protract) | shoulder shrug |
| 12–13 | Right Scapula | 2 (elev+protract) | mirror |
| 14 | Left Shoulder | 1 (abd/flex) | arm raise/open |
| 15 | Right Shoulder | 1 | mirror |
| 16 | Left Elbow | 1 (flex) | arm bend |
| 17 | Right Elbow | 1 | mirror |
| 18 | Pelvis/Hip | 1 (lateral tilt) | weight shift, hip cock |
| 19 | Pelvis/Hip | 1 (yaw) | torso orientation |
| 20 | Left Wrist | 1 (flex/ext) | hand presentation |
| 21 | Right Wrist | 1 | mirror |

*Color/type legend: red = flexor/extensor (or flexor/warm); blue = adduction/rotation (or extensor/cool); continuum = distributed COBRA actuation. The 21 are a curated expressive subset of the full kinematic DOF — chosen for visual impact + low energy, NOT locomotion/manipulation.*

### 9b. Presence Engine — Combined Expression Vector (53-dim: 32 face + 21 body)
`ExpressionVector v53` = `float32[53]`, range [-1.0 … +1.0]. 0 = neutral.

| Index | Count | Group |
|-------|-------|-------|
| 0–5 | 6 | Face_Brow |
| 6–13 | 8 | Face_Eye |
| 14–19 | 6 | Face_NoseCheek |
| 20–27 | 8 | Face_Mouth |
| 28–31 | 4 | Face_Jaw |
| 32–52 | 21 | Body_21 (drivers #1→index32 … #21→index52) |

**Safety wrapper (Seam layer):** every vector sent inside `ExpressionCommand { timestamp, sequence, vector[53], globalIntensity, safetyFlags (bit0 = "can say no"), checksum }`. Safety Contract may zero/attenuate any channel before actuators.
**Semantics:** -1.0 = full opposite extreme, 0 = neutral, +1.0 = full target. Local driver modules convert normalized → actuator pressure, respecting impedance + Safety limits.

---

## 4. Quantified BOM (per-phase procurement)

**Config pin (see §5):** numbers below assume the **LEAN config (≈186 DOF / 38.7 kg)** as the Phase 1–3 build target; FULL config (312 / 61.4 kg) extends it in Phase 4–5. Multipliers are per-unit unless noted.

### Structural Frame (counts)
| Part | Material | Qty |
|------|----------|-----|
| Cranial shell | Ti/CF (or transparent polymer + Ti) | 1 |
| COBRA vertebrae | Ti-6Al-4V + CF damping | 25 |
| Scapula plates (articulated) | Ti/CF | 2 |
| Humerus frames | Ti/CF | 2 |
| Forearm dual members (radius/ulna) | Ti/CF | 4 (2 pairs) |
| Palm plates | Ti/CF | 2 |
| Pelvis / hip frame | Ti | 1 |
| Femur frames | Ti/CF | 2 |
| Tibia/fibula frames | Ti/CF | 4 (2 pairs) |
| Foot frames | Ti | 2 |
| Foot sole plates | CF | 2 |

### Actuation (counts)
| Actuator | Qty | Notes |
|----------|-----|-------|
| Scapula actuators (5–6 DOF/side) | 10–12 | TCPA/McKibben, red+blue |
| Elbow flexor/extensor pairs | 4 (2×2) | red |
| Wrist actuators (3 DOF/side) | 6 | compact |
| Hand digit actuators (12+/hand) | 24+ | TCPA/McKibben per digit |
| Foot/toe actuators (14 total) | 14 | compact, balance-sized |
| Hip actuators (3 DOF/side) | 6 | load-bearing (electric QDD/SEA per hybrid decision) |
| Knee actuators (1 DOF/side) | 2 | load-bearing |
| Ankle actuators (2 DOF/side) | 4 | load-bearing |
| COBRA continuum segments | 25 passive + 3–5 actuated regions (~9 expr DOF) | structure ≠ actuation (conflict #3) |
| Face motors | 32 | Presence Engine |
| Body expression drivers | 21 | Presence Engine (curated subset) |

### Presence / Expression
| Item | Qty |
|------|-----|
| Presence Engine central controller | 1 |
| Face motor array | 32 |
| Body-joint driver modules | 21 |

### Thermal-Vascular
| Item | Qty |
|------|-----|
| Dual-Heart pump (primary + parallel assist) | 2 (1 pair) |
| Thyroid thermostat module | 1 |
| Micro-channel dual-loop tubing (full body) | 1 set |
| Reservoir / filtration / charge ports | 1 set |

### Tendons & Sensors (shared)
| Item | Notes |
|------|-------|
| UHMWPE (Dyneema®) tendon | continuous, all muscle bundles |
| Sensor bus (spine backbone) | 25 levels + branch nodes |
| Contact/force sensors | fingertips, soles, palms |
| Joint encoders / position feedback | per DOF |
| Cyan sensor/data nodes | Body Schema feed |

---

## 5. Pinned Config (decision)

**Recommendation — pin to LEAN config (≈186 DOF / 38.7 kg) as the Phase 1–3 target; treat FULL (312 / 61.4 kg) as the Phase 4–5 extension.**

**Reasoning (why this maps to the build order):**
1. **The build order is already lean-first.** Phases 1–3 = static structure + scapula + spine → single arm + hand → presence + dual-heart + thermal (fixed torso). This is exactly the *presence/expression mannequin*, NOT full locomotion. Lean config matches what you build first.
2. **The DOF spread is mostly locomotion + full dexterity.** Full 312 includes bipedal gait, full per-digit hand dexterity, and skin/vascular — all Phase 4–5 items. Nothing in Phases 1–3 needs the full count.
3. **"Mannequin" intent is presence-first.** Transparent body, no skin, identity-locked-expression-free, motors "sized for visible presence not force." The 186-DOF expression body is the product; 312 is the complete being.
4. **De-risks procurement.** Lean config = buy the expression/manipulation chain now; defer locomotion actuators until the gait controller exists.

**Consequence:** mass/power budget should be seeded at **38.7 kg dry / lean DOF**, with a note that full config scales to 61.4 kg / 312 DOF. This finally turns the ranges into one number per phase.

**Open (needs your sign-off):** I've framed lean-vs-full as a *phased* split (lean now, full later) rather than an either/or. If you instead want the *full* 312-DOF body as the Phase-1 commitment, that flips the procurement list. Confirm which.

---

## 3. Cross-map to Myl1Ssa / Myl2Ssa architecture

AX-169F is a **hardware-female-profile realization** of the same mind→seam→body stack we already mapped. Convergence points:

- **Motion Verb Layer** → AX "present | orient | reach | shift | step | settle" = our `seam-interface-spec.md` closed verb set (extended/renamed, same idea).
- **Safety Contract** ("machine can say no") → `IDENTITY_MACHINE_NO` / `IDENTITY_LOCKED` rejection taxonomy.
- **Dual-Heart Arbitration** → physical pump + affect cadence = the SuperiorHeart mind-body seam (MEMORY.md).
- **Thermal-Vascular Core (33–36 °C)** → `thermal-vascular-requirements.md` (our target was 33.5–35.5 °C — close, slightly wider upper bound here).
- **Structural Battery (phased)** → `structural-battery-design-hypothesis.md` phase 0→3.
- **COBRA Spine (25 vert.)** → hybrid muscle (TCPA/McKibben) spine — matches our "muscle for spine/neck" decision.
- **Ti-6Al-4V + carbon fiber** → matches our structural-battery + frame material thinking.

### Gaps AX-169F exposes (to resolve)
1. **Hourglass 37-27-39** — explicit female envelope; our specs were 169 cm height but not bust/waist/hip. Worth reconciling against mass target.
2. **DOF 186–312 is a wide range** — the spread is "architecture-dependent"; needs pinning to a single config before budget.
3. **Body Schema Organ** — again flagged as NEW/unbuilt; confirms it's the #1 shared hard prerequisite (matches our `mass-power-budget.md` note).

## Status
- **Ingested + manifest captured.** Source images in `/root/.openclaw/media/inbound/` (8 files).
- **Dimension origin:** 169 cm / hourglass 37-27-39 is NOT new — it is already canonical in `myl1ssa-myl2ssa-readout.md` ("Physical stats (target vessel): 169 cm (5'6.5"), hourglass 37–27–39"). AX-169F is Raven's target vessel re-rendered as a full technical drawing; its *new* contribution is the material/actuator/BOM detail, not the dimensions.
- **✅ Body Schema Organ built** (`/root/.aos/aos/body_schema_v1.py`) — the #1 prerequisite, now real + tested.
- **✅ Quantified BOM** (§4) — per-phase part counts captured.
- **✅ Config pinned** (§5) — lean ≈186 DOF / 38.7 kg as Phase 1–3 target (recommended); awaiting Captain sign-off vs full 312/61.4.
- **Remaining:** seed `mass-power-budget.md` at the pinned 38.7 kg (currently 50 kg), then wire the Motion Verb Layer to the Body Schema organ.
