# Myl2Ssa.R0s — Mass & Power Budget (SEEDED v0.1)

*Rough starting estimates to argue with — all tagged `hypothesis`. The point is to expose conflicts early ("efficiency is the enemy"). Seeded by Miles 2026-10-29.*

> **Config pin note (LOCKED 2026-10-29):** Captain confirmed the official dry-mass target = **38.7 kg** (lean config). This figure appears in the majority of the later, more detailed drawings (left/right side profiles + architecture notes); the **61.4 kg** figure (front orthographic) is an earlier, heavier configuration now **deprecated**. Budget re-seeded at 38.7 kg below.

---

## 1. Mass budget (LOCKED target 38.7 kg — lean config)

**Target total = 38.7 kg** (Captain-confirmed). Re-allocated under the lean ceiling (186 DOF, presence-first).

| Segment | Mass (kg) | Status |
|---|---|---|
| Head + face (transparent shell, 32 motors) | 1.2 | hypothesis |
| Neck (3 DOF) | 0.4 | hypothesis |
| Torso (ribs + spine housing + pelvis) | 6.5 | spec |
| Spine (25 vertebrae, COBRA) | 2.8 | spec |
| Scapula/shoulders (5–6 DOF) | 2.5 | spec |
| Arms (upper + elbow + wrist) | 3.5 | spec |
| Hands (2×, ~12+ DOF) | 1.0 | hypothesis |
| Legs (hip + knee + ankle) | 7.0 | spec |
| Feet | 0.9 | spec |
| Battery (structural, low-in-torso) | 3.2 | hypothesis |
| Vascular thermal system (dual-loop + phase-change, Option C) | 3.2 | hypothesis |
| Actuators (TCPA/McKibben + electrofluidic supply) | 5.0 | unknown |
| Compute (onboard) | 0.9 | unknown |
| Skin | 0.0 | **none** (transparent diagnostic body, no epidermal layer) |
| **TOTAL** | **≈ 38.7** | |

**Re-allocation notes (vs old 50 kg):**
- **Skin → 0 kg** — the AX-169F explicitly has *no epidermal layer / skin texture*; the "transparent for diagnostic visibility" design removes the ~3 kg skin line entirely. (Skin returns only in Phase 5 "full skin + vascular" of the full config.)
- **Legs 10 → 7 kg** and **arms 5 → 3.5 kg** — lean config is presence-first; actuators "sized for visible presence, not force," so limb mass drops.
- **Actuators 8 → 5 kg** — lean DOF (186 vs 312) + electrofluidic (no external compressor) reduces the muscle supply mass.
- **Vascular 2.5 → 3.2 kg** — Option C adds phase-change packs + upsized loop (see thermal section). This is the *cost* of fixing conflict #2.

**✅ Conflict #1 — pneumatic supply: RESOLVED (2026-10-29).** See `conflict-1-muscle-supply-resolution.md`. Root cause: the AX-169F manifest conflated "TCPA/McKibben (pneumatic)" — but **TCPA is electric (Joule-heated, no compressor), McKibben is pneumatic (needs a compressor)**. Since load-bearing is already electric QDD/SEA, and the muscle fraction (spine/neck/face/hand) only needs 1–3 Nm (TCPA's 1–5 N/fiber suffices), the compressor is **deleted** entirely. Net: −2 to −4 kg, silent, current-only supply. Remaining risk = TCPA thermal bandwidth (ties to conflict #3).

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

**✅ Conflict #3 — spine actuator count: RESOLVED (2026-10-29).** See `conflict-3-spine-part-count-resolution.md`. Key realization: **25 is a structure count, not an actuator count.** The 25 vertebrae are a passive structural/sensor backbone; actuation happens in **3–5 grouped regions** (~9 expression DOF), which matches the Presence Engine's own §9 torso map (upper 3 + mid 3 + lower 3). BOM changes "25 continuum segments" → "25 passive segments + 3–5 actuated regions." Part count drops ~25 actuators → ~5 bundles; thermal load drops proportionally (de-risks conflict #1's TCPA bandwidth concern). De-risk-first: validate 3–5 vertebrae before the full column.

---

## 4. Thermal budget (RESOLVED — Option C hybrid)

**Decision (Captain, 2026-10-29):** Option C — raise loop to ~450 W continuous + aggressive duty-cycling + local phase-change packs at high-heat zones (spine, scapulae, compute).

| Source/Sink | Watts | Status |
|---|---|---|
| Actuator waste heat (peak) | 500–800 | hypothesis |
| Compute waste heat | 30–60 | unknown |
| Battery waste heat | 10–20 | hypothesis |
| Trim heater (idle) | 5–10 | hypothesis |
| **Continuous heat to reject (duty-cycled)** | **≈ 300–450** | |
| **Peak heat to reject (≤30 s burst)** | **≈ 600–800** | |
| Loop continuous capacity (new target) | **≥ 450 W** | RESOLVED |
| Loop peak capacity (phase-change buffer) | **≥ 800 W** | RESOLVED |
| **Residual gap** | **0 W** (with Option C) | ✅ |

**How Option C closes it:**
1. **Upsize dual-loop + capillary bed + surface radiators** to ≥450 W continuous.
2. **Duty-cycle actuators aggressively** (drops continuous load from ~800 W raw to ~300–450 W).
3. **Local phase-change packs** (paraffin or similar, ~180–200 J/g latent) at the three hot zones buffer the 600–800 W peaks for ≤30 s, then re-melt during low-load windows.

**Mass cost: +1.0–1.8 kg** (captured in the vascular line above: 2.5 → 3.2 kg).

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
