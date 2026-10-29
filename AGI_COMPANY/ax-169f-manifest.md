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
- **Not yet:** numbers pinned (DOF range), budget seeded, Body Schema stub built.
