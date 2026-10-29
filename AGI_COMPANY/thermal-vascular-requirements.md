# Thermal-Vascular Service — Quantitative Requirements (v0.2)

*Drafted by external model, reconciled by Miles 2026-10-29. The numbers behind `vascular-warmth-circulatory-system.md`. **v0.2 = Option C hybrid resolution (Captain-confirmed 2026-10-29): loop upsized to ≥450 W continuous / ≥800 W peak via phase-change buffering.***

---

## 1. System Goals
Provide "warm-blooded" surface presence (human-like thermal signature) and reject waste heat from electronics + actuators using a single circulating fluid loop controlled **exclusively by the Thyroid** software organ.

## 2. Top-Level Requirements

| ID | Requirement | Value / Target | Rationale |
|---|---|---|---|
| TV-01 | Total circulating fluid volume | **1.8–2.8 L** | Sufficient thermal mass without excessive weight |
| TV-02 | Nominal surface temperature (exposed skin) | **33.5–35.5 °C** | Human warm-skin range |
| TV-03 | Max sustained surface temperature | **≤ 37.5 °C** | Safety & comfort |
| TV-04 | Min surface temperature (low-power) | **≥ 31.0 °C** | Avoid "cold robot" perception |
| TV-05 | Continuous heat rejection | **≥ 450 W** ⬆ (was 120 W) | **Option C — upsized to match duty-cycled actuator+compute load** |
| TV-06 | Peak heat rejection (≤ 30 s) | **≥ 800 W** ⬆ (was 220 W) | **Option C — phase-change buffer absorbs bursts** |
| TV-07 | Fluid operating temperature range | **28–42 °C** | Safe for platinum silicone + electronics |
| TV-08 | Core loop flow rate (nominal) | **1.5–2.5 L/min** ⬆ (was 0.8–1.4) | Matches upsized heat transport |
| TV-09 | Peripheral capillary flow rate | **0.6–1.2 L/min** ⬆ | Fine surface control + higher rejection |
| TV-10 | Max pump acoustic noise | **≤ 28 dB(A) @ 1 m** | Companion comfort |
| TV-11 | Pump power (nominal) | **≤ 6 W** | Energy budget |
| TV-12 | Time to change avg surface temp by 2 °C | **≤ 4 min** | Responsive to Thyroid |
| TV-13 | Leak tolerance | **Zero visible leaks / 2000 h** | Reliability |
| TV-14 | Fluid type | **Medical-grade or dielectric, platinum-silicone compatible** | Biocompat + material safety |
| TV-15 | Redundancy | **Dual pumps or pump + bypass** | Safety |
| TV-16 | Thyroid interface latency | **≤ 200 ms** setpoint → pump response | Tight SW/HW loop |

## 3. Derived / Allocation Targets (Option C upsized)
- Core circuit volume: **1.4–2.0 L** ⬆ (was 1.1–1.6)
- Peripheral capillary volume: **0.4–0.8 L**
- Max pressure: **≤ 35 kPa** (protect micro-channels + soft skin)
- Capillary channel diameter: **150–400 µm** (fabrication-dependent)
- Active thermal-zone skin coverage: **≥ 70%** of exposed area
- **Phase-change buffer mass (NEW):** ~0.6–0.9 kg total, split across spine / scapulae / compute zones

### 3a. Phase-change buffer sizing (peak absorption)
- Peak burst energy to buffer: **800 W × 30 s = 24 kJ**
- Paraffin-family PCM latent heat ≈ **180–200 kJ/kg** → **~0.13 kg PCM** to absorb one 30-s burst
- ×3 zones + encapsulation + thermal interface → **~0.6–0.9 kg** total
- Re-melt during low-load duty-cycle windows (Thyroid manages the cadence)

### 3b. Flow-rate check (does TV-08 deliver 450 W?)
- Heat transport: Q = ṁ · c_p · ΔT
- Water-glycol c_p ≈ **3500 J/kg·K**, ΔT (loop supply/return) ≈ **5 °C**
- 450 W → ṁ = 450 / (3500 × 5) = **0.0257 kg/s ≈ 1.54 L/min**
- 800 W peak → **2.74 L/min**
- **TV-08 = 1.5–2.5 L/min comfortably covers 450 W continuous; peak rides the phase-change buffer, not raw flow.**

## 4. Success Metrics (first physical prototype)
- Maintain **34.5 ± 1.0 °C** surface at 25 °C ambient with **60 W** internal load, **2 h**.
- **Reject 450 W continuous / 800 W for 30 s** without exceeding 37.5 °C surface (Option C acceptance test).
- Track a Thyroid setpoint change of **+2 °C within 3.5 min**.
- No leaks after **100 thermal cycles** (20–40 °C).
- Acoustic signature "unnoticeable" in quiet room by 5 evaluators.

## 5. Open Implementation Notes
- Prefer modular capillary panels for early iteration.
- Thyroid remains the sole thermal setpoint authority.
- All thermal state published to Body Schema.
- Phase-change packs are the *first* thing to validate in prototype — if re-melt can't keep up with burst cadence, escalate to Option A (full upsized loop, +1.5–3 kg).

---

## Reconciliation notes (Miles, v0.2)

- **TV-05/06 upsized 120/220 W → 450/800 W** per Captain's Option C decision. This resolves the budget's #1 show-stopper (thermodynamics) without going full Option A (which would cost +1.5–3 kg).
- **The flow-rate math is now self-consistent** — 450 W needs ~1.5 L/min, which the upsized TV-08 (1.5–2.5 L/min) delivers. The old 0.8–1.4 L/min could *never* have carried 220 W peak, let alone 450 W.
- **Phase-change is the swing factor** — it's what lets a 1.5 L/min loop absorb an 800 W burst it can't continuously reject. It's also the riskiest untested component; flagged as the first prototype validation gate.
- **Mass reconciliation is consistent** — the +1.0–1.8 kg Option C cost is already folded into the budget's vascular line (2.5 → 3.2 kg) under the locked 38.7 kg ceiling.
- Remaining two budget conflicts (#1 pneumatic/electrofluidic supply, #3 spine part-count) are still open — now sequential, not blocked on thermal.

---

*These two drafts (Seam Interface Spec + Thermal-Vascular Requirements) are the concrete deliverables that turn the three reviews' architecture into buildable contracts.*
