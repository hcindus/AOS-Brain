# Myl2Ssa.R0s — Mass & Power Budget (working template)

**Purpose:** rough budgets expose conflicts early (the "efficiency is the enemy" principle, operationalized). Fill in estimates → the directions that can't survive become obvious fast.

**Status:** TEMPLATE — numbers below are placeholders/starting-points to argue with, not commitments. Every figure tagged **spec / hypothesis / unknown**.

---

## 1. Mass budget (target total + per segment)

**Target total: ______ kg** (a 169 cm humanoid; rough reference: comparable bipeds 35–70 kg).

| Segment | Mass (kg) | Status | Notes |
|---|---|---|---|
| Head + face (silicone, 30 motors) | | unknown | silicone skin + actuated face |
| Neck (3 DOF) | | spec | |
| Torso (ribs, spine housing, pelvis) | | spec | CF ribs + Ti spine/pelvis |
| Spine (25 vertebrae, COBRA) | | spec | |
| Scapula/shoulders (5–6 DOF) | | spec | the crown jewel |
| Arms (upper + elbow + wrist) | | spec | wrist = missing (2-DOF) |
| Hands (2×, underactuated Rev A ~12–15 DOF) | | hypothesis | |
| Legs (hip + knee + ankle) | | spec | ankle = missing |
| Feet | | spec | |
| **Battery (main pack, low-in-torso)** | | hypothesis | primary source — structural cells are *supplement only* |
| **Vascular thermal system** (fluid + pump + heater) | | hypothesis | coolant ~1 kg/L; volume TBD |
| Actuators (electric + pneumatic supply) | | unknown | McKibben adds compressor/valve |
| Compute (onboard) | | unknown | local inference = the efficiency enemy |
| Skin (silicone + tactile sensors) | | spec | |
| **TOTAL** | **______** | | |

---

## 2. Power budget (idle / avg / peak / compute)

| Mode | Watts | Status | Notes |
|---|---|---|---|
| Idle (resting, low actuation) | | unknown | ~100 W human baseline is the *lower* bound reference |
| Average (walking/manipulation) | | hypothesis | hundreds of W |
| Peak (dynamic balance, lift) | | hypothesis | >1 kW |
| Compute load (onboard brain + presence) | | unknown | the efficiency enemy — local model sizing drives this |
| Trim heater (idle warmth) | | hypothesis | "basal metabolism" gap-fill |
| Pump + thermal loop | | unknown | small, but always-on |

**Key question:** does onboard battery capacity × average power give a useful runtime (hours, not minutes)? This is the first number that kills a direction.

---

## 3. Actuator torque & speed (per joint)

| Joint | DOF | Actuator type | Torque (Nm) | Speed (rad/s) | Status |
|---|---|---|---|---|---|
| Hip | | electric (QDD/SEA) | | | spec |
| Knee | | electric | | | spec |
| Shoulder | | electric (load-bearing) | | | spec |
| Scapula (5–6) | | ? | | | spec |
| Spine (25 vert) | | muscle (TCPA) | | | spec |
| Neck (3) | | muscle | | | spec |
| Hand (~12–15 underactuated) | | muscle/tendon | | | hypothesis |
| Face (30 motors) | | micro (silent) | | | spec |

**Key question:** can the electric joints deliver enough bandwidth for dynamic balance, given the mass budget? (McKibben hysteresis = balance risk — see hybrid-actuation note in spec.)

---

## 4. Thermal budget (watts in / out)

| Source/Sink | Watts | Status |
|---|---|---|
| Actuator waste heat (peak) | | hypothesis |
| Compute waste heat | | unknown |
| Battery waste heat | | unknown |
| Trim heater (idle) | | hypothesis |
| **Total heat to reject** | **______** | |
| Skin radiation/convection (at 35°C vs ambient) | | hypothesis |
| Surplus to dump via loop | | hypothesis |

**Key question:** at peak, is the "blood" loop's flow rate + ΔT enough to *dump* the surplus, or do we need a dedicated radiator? (Rejecting surplus = the hard half.)

---

## 5. Kill criteria (external review, 2026-10-28)

Define *in advance* what result would make us drop a hypothesis, so they don't linger:

| Hypothesis | Kill criterion |
|---|---|
| **Structural battery** | If energy density doesn't clear ~______ Wh/kg (worthwhile vs a pack), it stays a supplement / dropped from load-bearing. |
| **Capillary (micro) fabrication** | If molded/lost-wax macro channels give most of the thermal benefit, drop fine capillaries from scope. |
| **Muscle actuation for balance** | If McKibben bandwidth can't meet gait/balance spec in sim, move those joints to electric (already the hybrid plan). |
| **Vascular warmth** | If the loop's mass + power overhead exceeds a simple resistive web's by >X for the same 35°C uniformity, reconsider. |

---

*Fill the unknowns with rough numbers first — even ±50% estimates are more useful than blanks. This is the artifact that turns "efficiency is the enemy" from a principle into a filter.*
