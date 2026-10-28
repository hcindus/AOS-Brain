# Vascular Warmth — Circulatory Thermal System ("Warm-Blooded" Body)

**Status:** DESIGN DIRECTION — Captain's vision, 2026-10-28
**Applies to:** Myl2Ssa.R0s — §C Materials (thermal layer) + §3 Electrical (thermal management)
**Related:** `structural-battery-design-hypothesis.md` (power = the heat source = the "heart")

> Captain's words: *"To circulate the warmth, these need to be these silicone vessels — I envision the circulatory systems in mammals that circulate blood."*

---

## The idea

Distribute warmth the way mammals do: a **vascular system** — flexible silicone vessels embedded through the body, circulating warm fluid — instead of a static resistive heating web.

This reframes the "35°C warmth" lesson from *heating the surface* to *warming the body from within*. A warm-blooded body, not a heated object.

---

## Why it beats a resistive web

| | Resistive web | Vascular system |
|---|---|---|
| Heat distribution | Hot spots / cold patches at elements | **Uniform** — fluid reaches everywhere |
| Heat source | N scattered elements | **One core** (the "heart") + vessel network |
| Thermoregulation | Heat only | **Dual-mode** — warm fluid *or* coolant (shiver/sweat analog) |
| Integration | Standalone | **Carrier layer** — thermal fluid + sensor fibers ("nervous system") + potential hydraulic actuation in one vessel network |
| Efficiency | Poor (many elements) | **One source, many sinks** — beats the efficiency enemy |

---

## Architecture (mammal analog)

| Element | Mammal | Myl2Ssa |
|---|---|---|
| Heart | Pumps blood | **Core heat source + pump** (the chest-core — see below) |
| Blood | Carries O₂/heat | **Thermal fluid** (water/glycol, or a specialized medium) |
| Vessels | Arteries/veins/capillaries | **Silicone channels** — macro vessels in the chassis, micro-capillaries in the skin layer |
| Capillaries | Exchange at the surface | **Skin-level micro-channels** — the 35°C at the surface |
| Thermoregulation | Sweat/shiver | **Fluid temp + flow rate** modulated by the control node |

---

## The unification — power + warmth = one system

This snaps directly into **body-as-battery** (`structural-battery-design-hypothesis.md`):

- Xiao's teardown: **"a battery hidden inside her bones"** + **"something at the very center of her chest."**
- That **chest-core is the heart** — the core battery *is* the heat source.
- The vessels are how the battery's heat reaches every part of the body.

**Power and warmth collapse into one system:** the battery heats the "blood," the "blood" warms the body. This is the *integration* principle (Captain, 2026-10-28) made physical — one network doing thermal + (optionally) sensing + actuation.

---

## Honest constraints

- **Fluid adds mass + failure modes** (leaks, pump wear, fluid degradation) — must be sealed and serviceable. This is real engineering, not free.
- **Micro-capillary fabrication** in silicone is non-trivial (soft-lithography / 3D-printed vascular networks exist in research, e.g. vascularized soft robots, but production-grade is early).
- **Efficiency trade-off:** a fluid loop has pump + thermal-mass overhead vs. a simple resistive web. The win is *uniformity + integration*, not raw simplicity.
- **Path:** start with a **macro vessel loop** (core → spine/limb arteries → skin manifold) for the physical build; micro-capillaries in the skin are the maturity target.

---

## Where it lands in the build

- **§C Materials** — thermal layer becomes "silicone vascular system (circulatory warmth)," not a resistive web.
- **§3 Electrical / §G** — thermal management = core heat source (the body-as-battery "heart") + vessel network + pump + control-node thermoregulation.
- **Build order** — the silicone step now includes casting vessels, not just a flat heating web (see `body-inventory.md` / `build-order-list.md` fold-ins).

---

*Design direction, not yet built. The next physical proof is a single silicone vessel loop held at 35°C — the "warm-blooded patch" test.*
