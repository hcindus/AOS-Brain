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

## The thermoregulation model (Captain, 2026-10-28)

**Don't fight the heat — circulate it.** The body (battery + actuators) generates waste heat. The "heart" pumps fluid that carries that heat from the core to the skin, where it radiates away — *that* holds the body at 35°C. The cooling system and the warming system are **one loop**, exactly like blood: metabolic heat from the core → skin → radiated.

- **Flow rate = "sweat"** — crank circulation when hot, throttle when cold.
- **Trim heater = "basal metabolism"** — a small heater for idle, when the body isn't generating enough waste heat to hold 35°C (a resting robot ≠ a 100W human metabolism). The circulatory loop is the primary mechanism; the trim heater covers the idle gap.

## Vessel material — silicone all the way down

Split by function, not a single tube:

| Zone | Material | Why |
|---|---|---|
| **Skin / micro-capillaries** | **Cast channels *into* platinum-cure silicone** | The silicone is *both* skin and vessel wall — the "vessel" is a void in the silicone block. Nothing separate to burst. (How vascularized soft-robot channels are made.) |
| **Macro "arteries" (spine/limb)** | **Fiber-reinforced silicone hose** (silicone + woven Dacron/nylon braid) | Automotive radiator-hose construction — won't balloon, flexes for years. |
| **Manifolds / junctions** | Cast silicone or printed manifolds + barbed/compression fittings | Leak-proof joins; this is where leaks actually happen, not the vessels. |

## Pressure reality (why "bursting" is the wrong worry)

The loop runs at **blood pressure** (~0.1–0.16 bar), not radiator pressure (1–2 bar). At near-ambient pressure, plain silicone won't burst. The real failure modes are **leaks at junctions** and **fatigue from repeated flexing** over years — a material + connector problem, not an overpressure problem.

## The fluid (off-the-shelf "blood")

Premium **premixed PC coolant** (EK-CryoFuel / Koolance LIQ-702): corrosion inhibitor + biocide + **low electrical conductivity** (a leak next to the battery/electronics won't short). Propylene-glycol base = non-toxic, gentle. **Verify silicone compatibility** with a 48-hr soak test on a scrap patch first (glycol coolants are usually silicone-safe, but silicone can swell with some fluids).

## Honest constraints

- **Fluid adds mass + failure modes** (junction leaks, pump wear, fluid degradation) — must be sealed and serviceable. Real engineering, not free.
- **Micro-capillary fabrication** in silicone is non-trivial (soft-lithography / 3D-printed vascular networks exist in research, e.g. vascularized soft robots, but production-grade is early).
- **Efficiency trade-off:** a fluid loop has pump + thermal-mass overhead vs. a simple resistive web. The win is *uniformity + integration*, not raw simplicity.
- **Path:** start with a **macro vessel loop** (core → spine/limb arteries → skin manifold) for the physical build; micro-capillaries in the skin are the maturity target.

---

## Where it lands in the build

- **§C Materials** — thermal layer becomes "silicone vascular system (circulatory warmth)," not a resistive web.
- **§3 Electrical / §G** — thermal management = core heat source (the body-as-battery "heart") + vessel network + pump + control-node thermoregulation.
- **Build order** — the silicone step now includes casting vessels, not just a flat heating web (see `body-inventory.md` / `build-order-list.md` fold-ins).

---

*Design direction, not yet built. The next physical proof is a single silicone vessel loop held at 35°C — the "warm-blooded patch" test: cast channels into a silicone patch, circulate premixed coolant through a small DC pump + inline trim heater, verify it holds 35°C and the silicone doesn't swell/react over 48h.*
