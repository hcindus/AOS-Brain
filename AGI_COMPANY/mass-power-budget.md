# Myl2Ssa.R0s — Mass & Power Budget (SEEDED v0.1)

*Rough starting estimates to argue with — all tagged `hypothesis`. The point is to expose conflicts early ("efficiency is the enemy"). Seeded by Miles 2026-10-29.*

---

## 1. Mass budget (target total + per segment)

**Target total ≈ 50 kg** (169 cm humanoid; comparable bipeds 35–70 kg).

| Segment | Mass (kg) | Status |
|---|---|---|
| Head + face (silicone, 30 motors) | 1.5 | hypothesis |
| Neck (3 DOF) | 0.5 | hypothesis |
| Torso (ribs + spine housing + pelvis) | 8.0 | spec |
| Spine (25 vertebrae, COBRA) | 3.0 | spec |
| Scapula/shoulders (5–6 DOF) | 3.0 | spec |
| Arms (upper + elbow + wrist) | 5.0 | spec |
| Hands (2×, underactuated ~12–15 DOF) | 1.0 | hypothesis |
| Legs (hip + knee + ankle) | 10.0 | spec |
| Feet | 1.0 | spec |
| Battery (main pack, low-in-torso) | 3.0 | hypothesis |
| Vascular thermal system (1.8–2.8 L + pump) | 2.5 | hypothesis |
| Actuators (electric + pneumatic supply) | 8.0 | unknown |
| Compute (onboard) | 1.0 | unknown |
| Skin (silicone + tactile) | 3.0 | spec |
| **TOTAL** | **≈ 50.5** | |

**⚠️ Conflict #1 — pneumatic supply.** If McKibben muscles are used for spine/neck/face/hand, a compressor + valves + air reservoir adds ~2–4 kg and significant noise. The hybrid-actuation decision (electric for load-bearing, muscle for spine/face) *already* reduces this, but the "muscle" fraction still needs a pneumatic or electrofluidic supply that isn't priced into the 8 kg actuator line. **Recommend: electrofluidic (no external compressor) for the muscle fraction, or accept the +3 kg/compressor noise.**

---

## 2. Power budget

| Mode | Watts | Status |
|---|---|---|
| Idle (resting, low actuation) | 50–80 | hypothesis |
| Average (slow walk + manipulation) | 200–350 | hypothesis |
| Peak (dynamic balance, hard maneuver) | 800–1200 | hypothesis |
| Compute load (onboard brain + presence) | 30–60 | unknown |
| Trim heater (idle warmth) | 5–10 | hypothesis |
| Pump + thermal loop | ~6 | spec (TV-11) |

**Runtime check:** 3 kg Li-ion ≈ 250 Wh/kg × 3 = ~750 Wh. At 300 W average → **~2.5 h**; at 60 W idle → **~12 h**. (A companion doing gentle work lands closer to idle/average — acceptable; a "sprinting" humanoid does not.)

**⚠️ Conflict #2 — thermal spec vs. actuator heat.** Actuators + compute generate **hundreds of W** (to >1 kW peak). But the thermal-vascular service is specced for **TV-05 = 120 W continuous / TV-06 = 220 W peak** rejection. **These don't reconcile** — a 300 W average body can't be held at 35 °C by a 120 W loop. Either (a) the loop must be upsized to ~300–500 W continuous, or (b) the actuators must be throttled to stay inside 120 W (defeats dynamic motion). **This is the single most important number the budget exposes.**

---

## 3. Actuator torque & speed (per joint)

| Joint | DOF | Actuator | Torque (Nm) | Status |
|---|---|---|---|---|
| Hip | 2–3 | electric (QDD/SEA) | 60–120 | hypothesis |
| Knee | 1 | electric | 40–80 | hypothesis |
| Shoulder | 3 | electric | 20–40 | hypothesis |
| Scapula | 5–6 | ? (electric or muscle) | 5–15 | spec |
| Spine (25 vert) | ~25 | muscle (TCPA) | 1–3 each | spec |
| Neck | 3 | muscle | 1–3 | spec |
| Hand (~12–15) | ~13 | muscle/tendon | <1 each | hypothesis |
| Face (30 motors) | 30 | micro (silent) | <0.1 | spec |

**⚠️ Conflict #3 — spine actuator count.** 25 vertebrae × ~1 TCPA each ≈ 25 pneumatic muscles + tendons + valves, each needing supply. This is the *highest part-count* subsystem and the weakest link for the "efficiency" principle. **Recommend: validate the COBRA spine at 3–5 vertebrae first (de-risk-first order), before committing to 25.**

---

## 4. Thermal budget

| Source/Sink | Watts | Status |
|---|---|---|
| Actuator waste heat (peak) | 500–800 | hypothesis |
| Compute waste heat | 30–60 | unknown |
| Battery waste heat | 10–20 | hypothesis |
| Trim heater (idle) | 5–10 | hypothesis |
| **Total heat to reject** | **≈ 300–800** | |
| Loop capacity (TV-05/06) | **120 / 220** | spec |
| **Gap** | **−180 to −580 W** | 🔴 |

**Bottom line:** the thermal-vascular spec must be upsized by roughly **2.5–5×** to match a dynamic body, OR the body must be de-rated to a gentle companion envelope. This is the concrete "efficiency is the enemy" decision — and it's a real one the Captain needs to make.

---

## 5. Kill criteria (filled)

| Hypothesis | Kill criterion |
|---|---|
| **Structural battery** | Drop from load-bearing unless energy density clears ~80 Wh/kg (it's ~10–30 now). Keep as ride-through/sensor supplement only. |
| **Capillary (micro) fabrication** | Drop fine capillaries if molded/lost-wax macro channels hit TV-02 (35 °C) uniformity — keep it simple first. |
| **Muscle actuation for balance** | Move any joint to electric if McKibben bandwidth can't meet gait in sim (already the hybrid plan). |
| **Vascular warmth** | Reconsider if loop mass+power exceeds a resistive web by >2× for the same 35 °C uniformity. |

---

*Three conflicts surfaced by rough numbers — #2 (thermal undersized) is the one that must be resolved before any build. The other two (#1 pneumatic supply, #3 spine part-count) are strong arguments for the de-risk-first build order.*
