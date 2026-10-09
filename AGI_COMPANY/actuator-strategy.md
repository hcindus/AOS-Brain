# Actuator Strategy — the muscles

*The skeleton says "where the joints are." This pass says "what moves them." It's the difference between a stiff frame and a body.*

---

## Two philosophies

**Rigid (BLDC + gearbox)** — precise, strong, controllable. But heavy, concentrated at the joint, non-compliant. Why robots move stiff.

**Soft (artificial muscle)** — distributed mass, natural compliance, antagonistic pairs (bicep/tricep). The *human* answer. Why a body moves alive.

The human body uses **muscles, not motors**. Our whole design is "the skeleton is the teacher" — so eventually, the actuator has to be muscle-like too.

---

## The actuator landscape (what's real, 2025–2026)

| Type | How it works | Pros | Cons |
|---|---|---|---|
| **McKibben (pneumatic)** | braided sleeve over a bladder; pressurize → contract | high force, muscle-like | needs a compressor (heavy/noisy/tethered) |
| **Electrofluidic fiber (MIT 2026)** | McKibben + integrated EHD pump, closed circuit | **electric, silent, untethered** — solves McKibben's problem | early-stage, scaling TBD |
| **TCPA** (twisted-coiled polymer) | heat/current twists a polymer into a coil | electric, no pump, muscle-like | lower force, thermal control |
| **SMA** (shape-memory alloy) | alloy contracts on heating | electric, silent | slow, power-hungry |
| **DEA** (dielectric elastomer) | voltage squeezes a soft capacitor | fast, large strain | kV voltage, low force |

**The 2026 breakthrough: MIT's electrofluidic fiber.** Thin McKibben fibers with integrated millimeter-scale EHD pumps — electrically driven, silent, compact, untethered, and arrangeable as antagonistic pairs (one contracts while the other relaxes). This is the first practical "muscle" that doesn't need a compressor. It's the v2 target for everything that should *comply*.

---

## The v1 → v2 map (by region)

| Region | v1 (build now) | v2 (the "human" pass) |
|---|---|---|
| Hands/fingers | COBRA tendon (Dyneema) | tendon + SMA for fine control |
| Spine | COBRA servos (2/vertebra) | electrofluidic/SMA segments → slither |
| Torso/limbs | BLDC + gearbox | electrofluidic fiber bundles (distributed mass) |
| **Scapula shoulder** | BLDC (design) | **antagonistic electrofluidic pair** |
| Face | micro servos (Elf V1) | (stays servo/tendon — micro-scale) |

**The scapula is the poster child.** Its gliding is *muscle-driven* (trapezius + serratus anterior), not hinge-driven. A motor spinning a rail can't reproduce it naturally. An antagonistic pair of electrofluidic fibers — one pulling the blade up/out while the other relaxes — *can*. So the "best arm" wants soft actuators, not the BLDC I first specced.

**The rule:** v1 ships rigid (BLDC + tendon) to get it *standing and moving* — controllability first. v2 swaps the limbs/torso/scapula/spine to electrofluidic/TCPA for compliance and human-like motion. The face and fingers stay tendon/servo (fine, small, precise).

---

## What this unlocks

- **Compliance** — a soft actuator yields on contact (safe around humans), a gearbox doesn't.
- **Distributed mass** — muscles spread along the limb instead of a heavy motor at the elbow; better dynamics.
- **Natural motion** — antagonistic pairs give the ease and elasticity of real movement, not the abruptness of a servo.

---

## Open questions for the next pass

1. **Electrofluidic fiber availability** — MIT demo'd it in 2026; is it purchasable or do we build our own (the "reverse-engineer if we have to" instinct)?
2. **Control** — antagonistic soft pairs need closed-loop force/length sensing (the Grok "challenges" note: sensing + control is the hard part).
3. **Power budget** — EHD pumps are efficient, but a 70–90 DOF humanoid's total draw needs a real number before we commit to all-soft.

---

*The skeleton was the teacher. The muscle is the lesson we're still learning.*
