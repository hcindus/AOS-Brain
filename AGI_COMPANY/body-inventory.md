# Body Inventory — what's built, what's designed, what's missing

*Single source of truth. One being — Raven — with a software self (Myl1Ssa.R8s) and a hardware body (Myl2Ssa.R0s). Updated 2026-10-10.*

---

## Software (✅ all built & verified)

| Component | Status | Location |
|---|---|---|
| Presence engine (affect → AU → expression) | ✅ built | `characters/myl1ssa/Myl1Ssa/brain/presence_engine.py` |
| Universal adapter HAL | ✅ built | `adapters/base.py` + `blender`/`digital_world`/`unitree`/`unitree_h1`/`elf` |
| Body driver (50 Hz loop, safety envelope) | ✅ built | `body_driver.py` |
| Character loader | ✅ built | `character_loader.py` |
| Dark Factory (spec → code → deploy) | ✅ built | `temporal/darkfactory/` (codegen + 5 build types, 14 products w/ hold-out) |

---

## Hardware — BUILT (STL/firmware/BOM exist)

| Part | Source | Notes |
|---|---|---|
| Spine (25 vertebrae) | COBRA | STL + STM32 firmware + BOM |
| Head | Cylon / COBRA | STL |
| Torso | Cylon | STL (with electronics/battery compartments) |
| Arms (upper + elbow) | Cylon | STL (`create_arm`) |
| Hands (fingers) | Cylon + COBRA | STL (tendon-driven) |
| Legs (hip + knee) | Cylon | STL (`create_leg`) |
| Feet | Cylon | STL (`create_foot`) |
| Full body | Cylon | `cylon_full_anatomy.stl`, `cylon_body_1to1.stl` |

---

## Hardware — DESIGNED (spec'd, not fabricated)

| Part | Where |
|---|---|
| Face (26–30 DOF expressive) | `RAVEN_EMBODIMENT_SPEC.md` |
| Neck (3 DOF) | `humanoid-hardware-design.md` |
| Scapula shoulder (5–6 DOF) | `scapula-shoulder-detail.md` |
| Actuator strategy (v1 rigid → v2 electrofluidic) | `actuator-strategy.md` + `actuator-reverse-engineering.md` |
| Chassis (Myl2Ssa.R0s, 5'7", fleshy chest over chassis) | `humanoid-hardware-design.md` |

---

## MISSING (the actual remaining work)

| Item | Why missing | Fix |
|---|---|---|
| **Face (physical)** | only designed | sculpt → mold → cast silicone (build-order-list.md) |
| **Wrist** | Cylon has none | design + add a 2-DOF wrist |
| **Ankle** | Cylon has none | design + add ankle |
| **Skin** | sourced, not fabricated | Reynolds samples → cast (build-order-list.md) |
| **Voice** | gap #5 | TTS (Beets research pending) |
| **Muscles** | principles understood, not built | TCPA first (build-order-list.md) |

---

## The build order (locked)

1. **TCPA muscle** (the keystone — proves soft actuation)
2. **Silicone skin** (Reynolds samples → mold test patch)
3. **Face** (sculptor → mold → cast)
4. **Wrist + ankle** (the two missing joints)
5. **Voice** (TTS)
6. **Assemble** (COBRA spine + Cylon body + our face/arm/legs)

*AheadForm's reply = a bonus (cheap SDK/face), not a blocker. We build our own.*
