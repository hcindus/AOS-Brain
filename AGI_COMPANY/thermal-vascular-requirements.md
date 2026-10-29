# Thermal-Vascular Service — Quantitative Requirements (v0.1)

*Drafted by external model, reconciled by Miles 2026-10-29. The numbers behind `vascular-warmth-circulatory-system.md`.*

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
| TV-05 | Continuous heat rejection | **≥ 120 W** | Peak electronics + moderate actuation |
| TV-06 | Peak heat rejection (≤ 5 min) | **≥ 220 W** | Short high-load bursts |
| TV-07 | Fluid operating temperature range | **28–42 °C** | Safe for platinum silicone + electronics |
| TV-08 | Core loop flow rate (nominal) | **0.8–1.4 L/min** | Good heat transport |
| TV-09 | Peripheral capillary flow rate | **0.3–0.7 L/min** | Fine surface control |
| TV-10 | Max pump acoustic noise | **≤ 28 dB(A) @ 1 m** | Companion comfort |
| TV-11 | Pump power (nominal) | **≤ 6 W** | Energy budget |
| TV-12 | Time to change avg surface temp by 2 °C | **≤ 4 min** | Responsive to Thyroid |
| TV-13 | Leak tolerance | **Zero visible leaks / 2000 h** | Reliability |
| TV-14 | Fluid type | **Medical-grade or dielectric, platinum-silicone compatible** | Biocompat + material safety |
| TV-15 | Redundancy | **Dual pumps or pump + bypass** | Safety |
| TV-16 | Thyroid interface latency | **≤ 200 ms** setpoint → pump response | Tight SW/HW loop |

## 3. Derived / Allocation Targets
- Core circuit volume: 1.1–1.6 L
- Peripheral capillary volume: 0.5–1.0 L
- Max pressure: **≤ 35 kPa** (protect micro-channels + soft skin)
- Capillary channel diameter: **150–400 µm** (fabrication-dependent)
- Active thermal-zone skin coverage: **≥ 70%** of exposed area

## 4. Success Metrics (first physical prototype)
- Maintain **34.5 ± 1.0 °C** surface at 25 °C ambient with **60 W** internal load, **2 h**.
- Track a Thyroid setpoint change of **+2 °C within 3.5 min**.
- No leaks after **100 thermal cycles** (20–40 °C).
- Acoustic signature "unnoticeable" in quiet room by 5 evaluators.

## 5. Open Implementation Notes
- Prefer modular capillary panels for early iteration.
- Thyroid remains the sole thermal setpoint authority.
- All thermal state published to Body Schema.

---

## Reconciliation notes (Miles)

- **TV-04 (≥31 °C min)** is a nice catch — the *lower* bound (avoid "cold robot") is as important as the upper safety bound, and earlier notes only focused on the 43 °C burn ceiling.
- **TV-13 (zero leaks / 2000 h)** + **TV-15 (dual pumps)** directly encode the "junction leaks + flex fatigue" failure modes from the vascular doc — good, they're now quantitative.
- **35 kPa max pressure** confirms the "blood-pressure not radiator-pressure" framing (35 kPa ≈ 0.35 bar, between blood and a PC loop).
- **TV-16 (≤200 ms Thyroid→pump latency)** is the hard requirement that makes the "Thyroid = sole thermostat" claim real, not poetic — it forces the control loop tight.
- This doc is the quantitative counterpart to the budget template's thermal section; TV-05/06 (120/220 W) are the *answer* to "can the loop dump surplus heat?" — yes, up to 220 W peak.

---

*These two drafts (Seam Interface Spec + Thermal-Vascular Requirements) are the concrete deliverables that turn the three reviews' architecture into buildable contracts.*
