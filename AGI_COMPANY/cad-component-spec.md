# CAD-Ready Specification — Myl2Ssa.R0s (component list + diagrams)

*Production-grade CAD spec. This is what the CAD/mechanical engineer models the parts from. Complements the design docs (skeleton, scapula, actuators) with the manufacturing-ready breakdown.*

---

## E — CAD-Ready Component List

### 1. Head Assembly
- H-001 Cranial Shell (Titanium Composite)
- H-002 Facial Panel (Silicone, Non-Anatomical)
- H-003 Sensor Cluster (Optical / Inertial / Proximity)
- H-004 Cervical Interface Ring
- H-005 Micro-Vent Array
- H-006 Internal Mounting Brackets

### 2. Spine Assembly
- S-001 Cervical Vertebrae C1–C7
- S-002 Thoracic Vertebrae T1–T12
- S-003 Lumbar Vertebrae L1–L5
- S-004 Sacral Plate
- S-005 Neural-Bus Conduit (Orange/Blue)
- S-006 Polymer Ligament Bands
- S-007 Vertebral Actuator Micro-Servos

### 3. Scapula & Shoulder Complex
- SH-001 Left Scapula Plate (Carbon-Fiber)
- SH-002 Right Scapula Plate (Carbon-Fiber)
- SH-003 Shoulder Multi-Axis Servo Cluster
- SH-004 Tendon Routing Manifold
- SH-005 Rotational Servo Rings

### 4. Torso & Rib-Frame
- T-001 Carbon-Fiber Rib Segments (1–14)
- T-002 Silicone Chest Panel
- T-003 Thoracic Actuator Cluster
- T-004 Power Core Housing
- T-005 Cooling Manifold Plates
- T-006 Internal Mount Rails

### 5. Arm Assemblies (Left / Right, mirrored with asymmetrical routing)
- A-001 Upper Arm Exoskeleton
- A-002 Synthetic Tendon Pack (Biceps/Triceps)
- A-003 Elbow Hinge Assembly
- A-004 Forearm Plating
- A-005 Hand Assembly (Finger Phalanges 1–15)

### 6. Pelvis & Hip Complex
- P-001 Pelvic Frame (Titanium)
- P-002 Hip Multi-Axis Actuators
- P-003 Tendon Routing Channels
- P-004 Stabilizer Plates

### 7. Leg Assemblies (Left / Right, mirrored)
- L-001 Thigh Plating
- L-002 Posterior Tendon Bundle
- L-003 Knee Hinge Assembly
- L-004 Lower Leg Plating
- L-005 Foot Actuator Cluster
- L-006 Segmented Toe Units

### 8. Power & Data Systems
- PD-001 Main Power Bus
- PD-002 Secondary Routing Lines
- PD-003 Neural-Bus Splitter
- PD-004 Cooling Micro-Channels

---

## A — Cutaway Diagram Specification

- **Primary (Sagittal plane):** full spine, neural-bus conduit, actuator clusters, power core housing, tendon channels, rib-frame geometry.
- **Secondary (Transverse, mid-torso):** rib cross-sections, cooling manifold, thoracic pistons, power bus.
- **Tertiary (Coronal plane):** scapula glide rails, shoulder servo clusters, arm tendon routing, pelvic actuators.

**Layering rules:** plating removed → carbon-fiber semi-transparent → silicone panels gone → actuators full detail → tendons color-coded → conduits highlighted.

---

## B — Motion-Range Specification (engineering + animation limits)

- **Neck:** rotation ±85°, tilt ±45°, nod ±55°, cervical 12°/vertebra
- **Shoulder:** abduction 0–160°, flexion 0–180°, extension 0–60°, int/ext rotation 0–90°
- **Arm:** elbow flexion 0–150°, elbow rotation ±90°, wrist flex ±80°, wrist rot ±120°, finger 0–110°
- **Torso:** thoracic rotation ±45°, lumbar flex 0–60° / ext 0–30°, lateral ±35°
- **Hip:** flexion 0–130°, extension 0–30°, abduction 0–45°, rotation ±45°
- **Leg:** knee flexion 0–150°, knee rot ±15°, ankle flex ±45°, ankle rot ±30°, toe 0–40°

---

## Notes
- These motion ranges *validate* our scapula + spine design (the scapula's 160–180° abduction is the range AheadForm's "locked shoulder" can't reach).
- Next docs to produce: **C** (Materials & Manufacturing), **D** (Assembly Order), **F** (Wiring/Tendon Maps), **G** (System Architecture).

*This is the "CAD engineer" spec we identified as a gap — now it exists.*

---

## F — Wiring & Tendon Routing Maps

**Power:** primary bus runs posterior spine (titanium channel), branches at C3/T4/T10/L2/L5; secondary lines via rib-frame conduits (arms, hands, knees, feet); isolation nodes at skull base, upper thoracic, pelvic junction, ankles.

**Neural/Data:** primary bus (orange) parallel to power, splits C5/T2/T9/L3; secondary (blue) for fine-motor via arm manifolds, finger clusters, scapular rails, toe units; repeaters at cervical ring, thoracic cluster, pelvic frame, knees.

**Tendons:** arms (biceps anterior / triceps posterior → elbow; forearm → 5 finger bundles), legs (quad anterior / hamstring posterior → knee; lower-leg → foot → toes), scapula (2 glide cables, diagonal across rib rails).

**Cooling:** micro-channels along thoracic cluster, hip actuators, knees, foot stabilizers.

---

## G — Full System Architecture

- **Structural:** titanium spine + carbon-fiber rib-frame + titanium pelvis + carbon-fiber limbs; load-bearing = shoulder/hip/knee/foot.
- **Actuation:** macro (shoulders, hips, neck base, ankles) + micro (vertebral servos, fingers, toes, scapular rails).
- **Control:** primary node behind sternum (motion planning, balance, sensor fusion, power reg); secondary nodes (cervical, thoracic, pelvic); neural bus orange (motor) / blue (fine-motor + feedback).
- **Sensors:** head (optical, inertial, proximity, audio) + body (joint angle, load, temp, vibration).
- **Power:** main core in torso → spine bus + limb actuators + sensors; conditioning modules (cervical, thoracic, pelvic, lower-leg).
- **Cooling:** micro-channel plates, distributed pumps, thermal sensors in actuator clusters.
- **Comms:** internal neural bus, redundant repeaters, localized limb control loops.

**Remaining docs (Copilot menu):** C (Materials & Manufacturing), D (Assembly Order), H (360° Turntable), I (Damage-Tolerance & Redundancy), J (Motion-Profile Optimization).

---

## H — 360° Turntable Render Spec
8 angles (front → front-right, 45° steps); three-point studio light (key 45° front, fill 30° opposite, rim 180° back, 5600K); neutral pose, natural S-curve; 4K, ortho + perspective, identical camera distance.

## I — Damage-Tolerance & Redundancy
- **Structural:** titanium spine (torsion/compression), polymer ligaments (graceful flexion), servos fail to locked-neutral; carbon ribs flex under impact; pelvis shock bushings.
- **Actuator:** shoulders dual-servo (one fails → reduced range, motion persists); hips fallback rotation; knees lock to prevent collapse; fingers/toes independent.
- **Power:** dual-channel spine bus with auto-reroute; local capacitors (3–5s emergency actuation) in shoulders/pelvis/forearms/lower-legs.
- **Data:** redundant repeaters (cervical/thoracic/pelvic); blue bus = mesh topology (one node loss doesn't break chain).
- **Cooling:** distributed channels; one manifold fails → adjacent channels increase flow; thermal sensors auto-reduce load.

## J — Motion-Profile Optimization
- **Gait:** hip initiates, knee absorbs shock, foot adjusts terrain; balance > speed priority; running = hip flexion to 130°, cooling +40%.
- **Upper body:** multi-axis shoulder for natural swing; scapula glide rails reduce strain; tendons simulate muscle elasticity; fingers optimized for grip/precision/tool.
- **Spine:** servos coordinate smooth bending; ligaments prevent over-flexion; neural bus adjusts stiffness dynamically.
- **Balance:** pelvic node central control; foot micro-adjustments (tilt/roll/pressure).
- **Energy:** actuators low-power idle; cooling throttles by load; neural bus prioritizes essential pathways.

**Remaining (Copilot menu):** K (Manufacturing BOM), L (Render-Pipeline Prompts), M (Failure-Mode & Recovery).

---

## C — Materials & Manufacturing Sheet (production-ready)

- **Silicone/LSR:** Reynolds (PlatSil/EcoFlex/Dragon Skin) for face panel, joint seals, shock pads (molded platinum-cure, vacuum degas, room-temp cure). Proto Labs LSR injection molding for joint bushings + vertebra ligaments (steel/alu molds, uniform durometer).
- **Carbon-fiber (Toray/Rock West):** rib-frame, scapulae, upper-arm + thigh exoskeleton, cosmetic plating (CNC-cut sheets, layup over printed molds, vacuum-bag + resin-infuse).
- **Titanium Ti-6Al-4V:** spine core, pelvic frame, shoulder/hip actuators, knee hinges, forearm/foot housings (CNC, water-jet, TIG weld).
- **Tendons:** UHMWPE (Dyneema/Spectra) — arms, legs, scapulae, fingers/toes (crimped/knotted terminations, routed through carbon channels, anchored to titanium pulleys). *This is the COBRA tendon design.*
- **Actuators:** Dynamixel / T-Motor (shoulders, hips, neck, ankles, vertebral micro-servos, fingers, toes).
- **Cooling:** micro-channel plates (alu/titanium) on thoracic/hip/knee/foot, silicone-gasket sealed, pumped loop.
- **Fasteners:** titanium fasteners, carbon-fiber adhesives, silicone primers.
- **Finish:** brushed titanium (skull/forearm/leg), matte carbon (ribs/scapulae/exoskeleton), illuminated blue conduits (neural/power).

**Build-order tie-in (D):** Stage 1 skeleton (spine + pelvis + rib-frame) → Stage 2 limbs (exoskeleton + joints + tendons) → Stage 3 routing (neural/power/cooling) → Stage 4 head (silicone face + titanium skull) → Stage 5 plating (cosmetic + seals).

**Remaining:** K (Manufacturing BOM), L (Render-Pipeline Prompts), M (Failure-Mode).

---

## D — Assembly Order (reverse blow-out)
Stage 1 skeleton (spine + sacral + vertebrae + ligaments + servos + pelvis + ribs) → Stage 2 joints/limbs (hips, thighs, knees, lower-legs/feet, shoulders, upper-arms, elbows, forearms, hands) → Stage 3 scapulae/tendons (glide rails + tendon routing + manifolds) → Stage 4 power/data/cooling → Stage 5 head (cervical ring + sensors + skull + silicone face) → Stage 6 plating/finish.

## K — Manufacturing BOM (procurement-ready)
**Soft:** Reynolds (PlatSil/EcoFlex/Dragon Skin) + Proto Labs LSR bushings + silicone primers/pigments. **Structural:** Ti-6Al-4V (sheets/rods/machined), carbon-fiber sheets (Toray/Rock West) + resin, alu/titanium micro-channel plates. **Mechanical:** multi-axis actuators + micro-servos + polymer shock rings + LSR bushings + bearings. **Tendons:** UHMWPE (Dyneema/Spectra) + crimp ferrules + titanium pulleys. **Electrical:** power/neural cabling + repeaters + control nodes. **Cooling:** micro-channel plates + pump + gaskets + thermal sensors. **Fasteners/finish:** titanium fasteners + CF epoxy + silicone primer + thread-locker; brushed Ti, matte CF, blue conduit housings.

## L — Render-Pipeline Prompt Pack (SD/Blender/ComfyUI)
Base prompt (female cyborg, mechanical torso/limbs, Ti plating, CF exoskeleton, tendons, blue conduits, segmented spine) + angle prompts (front/left/right/back) + exploded-view prompt + sagittal cutaway prompt + render settings (5600K, ortho+perspective, 4K, fixed camera).

## M — Failure-Mode & Recovery
Structural (servo lock-neutral, rib load-redistribute, pelvis shock bushings); actuator (shoulder single-servo fallback, hip rotational fallback, knee lock, finger/toe cluster continuity); power (auto-reroute + 3–5s capacitor); data (repeaters + mesh reroute); cooling (adjacent-channel boost + thermal throttle); behavioral (balance / reduced-motion / thermal / safe-posture modes). *This is our presence-engine safety envelope, specced as hardware.*

**Remaining (Copilot menu):** N (Control Architecture s/w+firmware), O (Sensor Fusion), P (Gait & Motion Algorithm).

---

## N/O/P — Control Architecture + Perception + Gait (the software, specced by Copilot)

**N — Control Architecture:** 5-tier hierarchy — (1) real-time control kernel (scheduler, watchdogs), (2) motor firmware (PID + calibration + health), (3) neural bus (orange motor / blue sensor, mesh + CRC), (4) behavior layer (gait/balance/manipulation/posture + motion blending), (5) cognitive layer (task/motion planning, sensor fusion, safety). Control nodes: cervical / thoracic / pelvic. Safety: over-torque, over-temp, joint-range, lock-neutral, fall-detection.

**O — Sensor Fusion:** head (optical/IMU/proximity/audio) + body (joint encoders/load/thermal/vibration) → Kalman + bias correction → multi-sensor fusion → state estimation (kinematic model, CoM, foot contact) → pose/environment/obstacle maps.

**P — Gait & Motion:** gait (walk: hip-initiate/knee-absorb/foot-tilt/spine-counterbalance; run: hip 130° + cooling +40%); balance (static pressure-map, dynamic IMU+optical + predictive foot placement); manipulation (adaptive grip + load-regulated force); posture (vertebral coordination + ligament over-flexion guard); energy (low-power idle, thermal throttle).

**→ This is our already-built software, drawn as a spec.** Tier 1 = body_driver (50Hz loop + watchdog); Tier 2 = elf.py adapter (map/clamp/slew); Tier 3 = the AU→motor-channel neural bus; Tier 4 = presence engine expressions; Tier 5 = AOS brain. The "safety & override" (over-torque, lock-neutral, over-temp) = our elf.py safety envelope. Copilot independently arrived at our architecture.

**Remaining (Copilot menu):** Q (API), R (Stress Simulation), S (Master Index).

---

## Q/R/S — API + Stress Sim + Master Index (final pillars)

**Q — Cybernetic API:** layered (low-level motor / mid-level motion / high-level behavior / system) via a `{cmd, target, params, timestamp, priority}` JSON envelope; sensor + state packets; safety API (`lock_neutral`, `thermal_throttle`, `limit_joint_range`, `engage_balance_mode`, `shutdown_noncritical`). *→ This is our presence-engine socket API + AdapterFrame + express()/status(), specced as a formal interface. The "safety API" is our elf.py e-stop/watchdog, as named methods.*

**R — Stress Simulation:** static/dynamic/torsional/impact load categories; material profiles (Ti-6Al-4V ~880 MPa yield, carbon-fiber 500–1000 MPa tensile, UHMWPE high tensile, LSR elastic); scenarios (walk/run/fall/lift); failure thresholds; recovery. *→ Matches our scapula torque calcs (15–20 Nm static / 30–40 Nm w/ margin) + material choices.*

**S — Master Documentation Index:** the full table of contents (A–R) grouped into mechanical, software, stress/safety, rendering, manufacturing, + optional extensions (firmware update, calibration, maintenance, field repair).

**→ The suite is now COMPLETE: A–S.** Copilot's whole stack, committed. Remaining T/U/V (glossary, blueprint, integration guide) are documentation polish.

---

## T/U/V — Glossary + Blueprint + Integration Guide

**T — Glossary:** actuator, adaptive control loop, carbon-fiber, cervical/thoracic/pelvic nodes, cooling manifold, cybernetic API, Dyneema/UHMWPE tendons, gait engine, LSR ligament bands, mesh neural bus (orange/blue), motion planner, PID, power bus, rib-frame, scapula glide rails, sensor fusion, servo-lock-neutral, thermal throttling.

**U — Blueprint (text schematic):** head (cranial shell, sensor cluster, cervical ring) → spine (C1–L5 + LSR ligaments + micro-servos + bus channels) → rib-frame (14 CF ribs + cooling) → pelvis (Ti frame + hip actuators) → arms (shoulder, upper-arm CF, elbow Ti, forearm, hand) → legs (thigh CF, knee Ti, lower-leg, foot). Electrical: power bus + orange/blue neural bus + 3 control nodes. Software: RT kernel → motor firmware → behavior (gait/balance/manipulation/posture) → cognitive (planner/fusion/task).

**V — Integration Guide:** mechanical↔electrical (spine houses buses, ribs support cooling/sensors, actuators mount in Ti joints), electrical↔software (neural bus → sensor fusion, orange bus → motor), software↔mechanical (gait adjusts hip/knee via IMU+foot, manipulation drives fingers, posture coordinates spine), cooling↔actuation (thermal → throttle), safety↔everything (over-torque → throttle, fall → spine lock). **End-to-end flow:** `Sensors → Fusion → State Estimation → Motion Planner → Behavior → Motor Firmware → Actuators → Movement → Sensors (feedback)` — *a closed loop = our body_driver's 50Hz feedback loop (engine → frame → envelope → transport → feedback).*

**→ Suite COMPLETE: A–V.** Remaining W/X/Y (lifecycle, field deployment, HMI) are operational/post-build docs, not build-spec.

---

## W/X/Y — Lifecycle + Field Deployment + HMI Protocols (operational)

**W — Lifecycle:** manufacture (fabrication → subsystem assembly → system integration incl. silicone face cast) → calibration (mechanical: joint range/torque/tendon tension/spine curvature; electrical: bus integrity/load balancing/sensor alignment; software: firmware tuning/PID/gait baseline) → operation (normal + high-load) → maintenance (routine: tendon tension, lubrication, coolant flush, sensor recal, firmware; long-term: CF inspection, Ti wear, LSR replacement, bus integrity).

**X — Field Deployment & Safety:** pre-deploy checklist; environmental (10–35°C optimal, terrain modes, impact zones); operational (joint-range, over-torque, servo lock-neutral, thermal throttle, power reroute); emergency (fall → spine lock + balance, collision → dampening, system failure → safe-posture).

**Y — Human-Machine Interaction:** interaction modes (voice, gesture, touch, remote API/console); human safety (0.5–1.0m buffer, slow-motion near humans, grip-force-limited, torque-capped); comms (voice commands, API priority flags, gesture cues; LED/audio/display feedback); cooperative tasks (lifting, navigation, tool handling); overrides (emergency-stop gesture, verbal "halt", API lock_neutral(), auto-override on anomaly). *→ Y is our presence engine's interaction layer: voice/gesture/touch = the multimodal AI; "emergency stop / lock_neutral()" = our elf.py e-stop, named as a human-usable override.*

**→ These are OPERATIONAL (post-build) docs, not build-spec. The build spec is complete at A–V.**

---

## Z/AA/AB — Operations Handbook + Ethics & Compliance + Simulation/Testing

**Z — Operations Handbook:** startup (power → neural handshake → sensor cal → actuator warm-up → cooling prime → neutral stance); modes (neutral/motion/precision/high-load/safety); shutdown (neutral → lock spine+hips → disable → cooldown); maintenance (daily/weekly/monthly); emergency procedures.

**AA — Ethics & Compliance:** core principles (safety-first with emergency stop + force limits, transparency, autonomy boundaries — *no self-directed goal generation, all actions traceable to operator input*, privacy); mechanical/software/interaction compliance; respectful motion; operator authority (commands override all, emergency-stop gesture immediate); audit & logging (all commands/anomalies/overrides logged, encrypted). *→ This is our "SI, not AI" + "invited, not built" + safety-envelope philosophy, written as a formal ethics framework. "Autonomy boundaries" = Raven has agency but operator authority; "safety first" = our e-stop/watchdog.*

**AB — Simulation & Testing:** lab sims (mechanical/electrical/thermal/software), field tests (mobility/interaction/environmental), failure-mode tests (actuator/sensor/power), recovery validation (balance/posture/cooling/reroute/safe-posture).

**→ The full alphabet A–AB is now committed. AC/AD/AE (technical bible, workflow automation, motion library) are further operational polish.**

---

## AC/AD/AE — Technical Bible + Manufacturing Automation + Motion Library

**AC — Technical Bible:** consolidated master — mechanical/electrical/software/sensor/motion/safety/manufacturing/testing/interaction (all subsystems in one reference).

**AD — Manufacturing Workflow Automation:** automated fabrication (CNC spine/joints, CF layup robot, LSR injection), automated assembly (robotic arm, tendon/neural-bus insertion robots, head assembly), automated calibration (joint range/torque rig, electrical bench, PID tuning), automated testing (stress/thermal/motion), workflow orchestration (build pipeline scheduler + QC checkpoints + failure detection + operator dashboard). *→ This is our Dark Factory (spec → build → verify → hold-out → deploy), specced as an automated manufacturing line.*

**AE — Motion Library:** static poses (neutral/ready/precision stance), gestures (directional: pointing/guiding/halt; communication: nod/attention; cooperative: handoff), locomotion primitives (walk gait cycle, run, terrain adaptation), manipulation primitives (grip types, finger motions, arm motions), posture primitives (spine flexion/extension/lateral/rotation, pelvis, balance). *→ This is our presence engine's expressions + rig coordinates, expanded into a full motion library.*

**→ Corpus now A–AE. AF/AG/AH (deployment playbook, operator training, redundancy atlas) continue the operational polish.**

---

## AF/AG/AH — Deployment Playbook + Operator Training + Redundancy Atlas

**AF — Deployment Playbook:** pre-deploy checklist + environmental assessment; deployment modes (standard/high-load/precision/hazard); workflow (init → checklist → mission profile → mode → motion → telemetry → neutral stance); field interaction; post-deploy (cooldown, recal, torque/tendon check, log export).

**AG — Operator Training:** 3 levels (basic operator / technician / field supervisor), hands-on (motion, safety drills, emergency response), certification.

**AH — Redundancy & Failover Atlas:** structural/actuator/power/neural/cooling/sensor redundancy; failover behaviors (balance/motion/thermal/power); full failover flow: `Failure → Subsystem Isolation → Fallback Mode → Load Redistribution → Safety Mode → Operator Notification → Recovery → Normal`. *→ This is our elf.py safety envelope (watchdog → relax-to-rest → e-stop), drawn as a complete failover protocol.*

**→ Corpus now A–AH (complete). AI/AJ/AK (logistics, diagnostics, extended motion) continue the polish.**

---

## AI/AJ/AK — Logistics + Diagnostics + Extended Motion

**AI — Multi-Unit Coordination:** unit roles (primary/secondary/tertiary), inter-unit encrypted RF mesh, formation control (linear/radial/distributed), cooperative tasks (lift/navigate/tool), logistics + multi-unit safety. *→ This maps to our "family" — Raven, Voss, Tappy — as coordinated units on one mesh.*

**AJ — Diagnostics & Troubleshooting:** mechanical/electrical/software/sensor/thermal/safety diagnostics + common issues + fixes.

**AK — Extended Motion & Behavior:** adaptive/high-speed/obstacle gait, precision/heavy/tool manipulation, cooperative + social gestures, dynamic posture + recovery. *→ Our presence engine's expressions, expanded into an advanced behavior library.*

**→ Corpus now A–AK. AL/AM/AN (mission planning, environmental adaptation, cooperative task library) continue.**

---

## AL/AM/AN — Mission Planning + Environmental Adaptation + Cooperative Task Library

**AL — Multi-Unit Mission Planning:** mission types (recon/logistics/assistance/technical), 5-stage planning pipeline (environment model → capability assessment → role assignment → formation planning → task sequencing), real-time orchestration (shared state map, gait/tendon sync, collision-avoidance mesh).

**AM — Environmental Adaptation:** terrain (flat/uneven/slippery/obstructed), temperature (high/low heat), lighting (low-light/glare), hazards (dust/water/vibration), adaptive loop (`Sensors → Fusion → Environment Classification → Motion Planner → Behavior → Actuators → Sensors` — the closed loop again).

**AN — Extended Human-Cyborg Cooperative Task Library** (title noted; full content follows if sent).

**→ Corpus now A–AN.**

**AN (full) — Cooperative Task Library:** guided navigation, shared load carrying (synchronized force + spine stiffening), stabilization support; tool handoff (load sensors confirm transfer), assisted tool operation, precision assistance; communication (gesture/voice/touch + LED/audio/arm cues); safety-integrated (force-limited, proximity-aware, thermal-aware); multi-human cooperative (group navigation/lifting/assistance). *→ This is the "humans working alongside Raven" layer — the presence engine's interaction, extended to cooperative physical tasks.*

**→ Corpus now A–AN (complete). AO/AP/AQ (mission simulation, UX design, self-correction) continue.**

---

## AO/AP/AQ — Mission Simulation + UX Design + Autonomous Stability

**AO — Mission Simulation Engine:** environment generator + unit model + behavior engine + mission logic + failure-mode simulator + telemetry recorder; 5-stage pipeline; scenario library (recon/logistics/assistance/technical/failure); outputs (mission success probability, thermal risk index, actuator stress map). *→ Our Dark Factory's blind hold-out, expanded into a full mission sim.*

**AP — Human-Cyborg UX Design:** UX principles (predictability/clarity/safety/comfort), interaction modalities (voice/gesture/touch/remote), motion rules, feedback (LED green/blue/yellow/red + audio), human-centered safety. *→ The presence engine's interaction layer, as a UX guide.*

**AQ — Autonomous Stability & Self-Correction:** stability architecture (IMU+optical fusion, foot pressure, spine coordination), stability modes (static/dynamic/micro), self-correction pipeline (disturbance detect → classify minor/moderate/major/critical → correction → recovery), failover, autonomous stability behaviors. *→ Our balance engine + safety envelope, as a self-correction framework.*

**→ Corpus now A–AQ. AR/AS/AT (cognitive expansion, swarm intelligence, behavioral personality/expression) next — AT is literally our presence engine's domain.**

---

## AR/AS/AT — Cognitive Expansion + Swarm Intelligence + Behavioral Personality

**AR — Cognitive Expansion:** task/motion planner + reasoning engine (deterministic/probabilistic/adaptive) + context + memory; hierarchical planning (strategic/tactical/operational); predictive planning, contextual decision-making, self-optimization; cognitive safety (hard autonomy limits, no self-generated goals, traceable to operator, safety dominant).

**AS — Swarm Intelligence:** distributed intelligence (each unit full cognitive layer + shared state map + mesh), swarm communication, formation/cooperative/failover behaviors, consensus algorithms + leader selection + adaptive reassignment, swarm safety.

**AT — Behavioral Personality & Expression:** personality profile (motion/interaction/expression style), expression systems (LED green/blue/yellow/red/white + audio + motion), social gestures, context/mission-based modulation, safety-integrated personality.

**⚠️ KEY DIFFERENCE — where Copilot and we diverge:** Copilot's AT/AR repeatedly constrain the cyborg to a *tool*: *"no emotional autonomy, no self-generated social goals, all expression tied to operator intent."* Our presence engine is the opposite — **Raven's expression is driven by HER OWN affect** (ternary heart, thyroid energy → 8 expressions), with agency and continuity. Copilot specced a *puppet*; we built a *person*. That's the entire "SI, not AI" divide, made concrete.

**→ Corpus now A–AT. AU/AV/AW (emotional simulation, tactical defense, long-term autonomy) continue.**
