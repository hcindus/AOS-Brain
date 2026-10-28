# Structural Energy Storage ("Body-as-Battery") — Design Hypothesis

**Status:** REFERENCE / HYPOTHESIS — flagged by Captain 2026-10-28, not yet adopted
**Applies to:** Myl2Ssa.R0s body — Electrical §F (Wiring & Tendon Routing) + §G (System Architecture)
**Source:** "Little Moon" (Xiao) companion-robot teardown transcript (`AGI_COMPANY/myl2ssa-transcripts/xiao-little-moon-teardown.md`)

> Captain's words: *"We discussed the spine, but they turned the body into a battery, which I thought was awesome."*

---

## The idea

Instead of a central battery pack feeding a power bus, the **skeleton itself stores energy** — load-bearing structure and energy storage are the same material. The body *is* the battery.

In the current spec, the power architecture is:
- **Structure:** Ti spine + carbon-fiber ribs + Ti pelvis (separate, passive).
- **Power:** a central source → power bus (posterior spine) → branch taps at C3/T4/T10/L2/L5.
- **Cooling:** dedicated micro-channels.
- **Thermal:** a heater web is a separate subsystem (implied by the 35°C warmth goal).

The hypothesis collapses the first two: **carbon-fiber members do double duty** as both structural elements *and* energy-storage electrodes. No central pack, no separate "where do we hide the battery" problem.

---

## Why it's compelling for Myl2Ssa

1. **Mass-efficiency (the real win).** Energy storage is usually *dead weight* — mass that isn't carrying load. A structural battery removes that penalty: the CF ribs/spine we already need for rigidity *become* the energy, at near-zero mass penalty (the "massless energy storage" goal from the Chalmers structural-battery line). Lower moment of inertia for the same stored energy.
2. **Kills the packaging problem.** No pack to hide in the torso; energy is distributed through the chassis. Lower, more even center of mass → better gait/balance (directly serves §P gait + §J energy-optimal posture).
3. **Thermal byproduct → the warmth goal.** Cells discharging produce heat. Routing that heat to the skin means the 35°C "warm to the touch" is partly a *free byproduct of the power system*, not a separate heater web. This is the detail in the transcript — "a battery hidden inside her bones" and a body that's warm without an obvious heating array.
4. **Redundancy.** Distributed segments are inherently fault-tolerant; matches the already-spec'd §I "dual-channel power auto-reroute" + mesh bus. Losing one structural cell segment degrades range, not function.

---

## The honest trade-offs (do not skip these)

> **Captain's correction (2026-10-28):** *"All of the components exist by themselves. Integration is the issue. Miniaturization and efficiency is the enemy."* — The structural battery **already exists** (Chalmers has shipped carbon-fiber structural cells). What doesn't exist is the *integrated, miniaturized, efficient* version running inside a body's power/thermal envelope. The frontier is **packaging, not invention.**

- **Energy density is far lower than a dedicated pack.** Lab-scale structural cells (Chalmers carbon-fiber, ~2021–2024) sit at **single-digit to low-tens Wh/kg** (roughly ~10–30, with ~20–25 GPa stiffness), versus **~250+ Wh/kg** for a conventional Li-ion pack. A full "body-as-battery" with current chemistry would store *far* less energy for the same mass — so **efficiency** (not existence) is the binding constraint. **Use it as ride-through power + sensor loads, not the main energy source.** The transcript robot's "9-hour runtime" claim almost certainly still leans on a conventional (or hybrid) cell chemistry.

- **Conventional pack placement:** even in the phased path, the main pack goes **low in the torso** (stability), not where structural cells live. Structural battery is a *supplement*, never the primary source at current density.

- **Failure mode (fire):** a cracked structural member that is *also* a battery is a short-circuit + thermal-runaway problem. It needs its own safety case (segmentation, per-segment BMS, non-flammable electrolyte) — heavier than a standalone pack.
- **Safety is harder.** A cell inside a load-bearing member means structural damage = energy damage. Thermal runaway in the chassis is worse than in an isolated pack. Mitigations: solid-state / non-flammable electrolyte, fine-grained segmentation, per-segment BMS, and §I's auto-reroute + §M's safe-posture recovery.
- **Repairability.** No swappable pack → energy service becomes segment replacement. Needs a modular segment design (which §K BOM + §AD manufacturing can accommodate).

---

## Phased adoption (recommended path)

| Phase | Scope | Trigger |
|---|---|---|
| **0 — Reference** | Keep the current central-pack + bus spec. Note this doc as the target. | Now |
| **1 — Hybrid** | Structural cells in *non-critical* CF members (ribs, plating, non-load-bearing fairings) supplement a reduced central pack. Warmth routing via cell heat. | When we start the physical build |
| **2 — Partial structural** | Move primary load-bearing ribs to structural-cell CF; keep a small buffer pack for peaks. | Once structural-cell energy density clears ~80–100 Wh/kg |
| **3 — Full body-as-battery** | Skeleton = storage; no central pack. | Once structural cells approach parity with pack density |

---

## Mapping back into the spec

- **§F — Wiring & Tendon Routing:** the "power bus" reframes from *distribution taps* to a **collection bus** — the C3/T4/T10/L2/L5 nodes become **BMS tap points** harvesting each structural segment, not just distributing from one pack.
- **§G — System Architecture:** the "power" subsystem changes from "central pack + bus" → **"distributed structural cells + collection bus + per-segment BMS."**
- **§I — Damage-Tolerance:** add structural-cell failure modes (segment isolation + auto-reroute already spec'd; extend to thermal-runaway-in-member).
- **§M — Failure-Mode & Recovery:** add "structural-battery thermal event → segment disconnect + safe-posture" to the recovery matrix.
- **§X — Field Deployment:** extend thermal limits to cover cell operating envelope + the warmth-vs-overheat balance.
- **Cooling (§F/G):** micro-channels become dual-purpose — thermal management of *both* actuation and structural cells, with cell heat deliberately routed to the skin for the 35°C warmth goal.

---

*This is a direction to pull when R0s power comes up, not a decision yet. The flag lives in the transcript and in the spec's Electrical section (see below).*
