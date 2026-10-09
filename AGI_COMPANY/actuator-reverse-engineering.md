# Actuator Reverse-Engineering — the principles

*We don't buy muscles. We understand the principle, then the parts are all on a shelf.*

---

## 1. McKibben muscle (1950s — the base)

**Principle:** a rubber/silicone tube inside a **braided sleeve**. Pressurize → the tube inflates radially → the braid's helix angle changes → axial **contraction** (20–30% strain). It's just geometry: radial bulge → longitudinal pull.

**Parts (all off-the-shelf):** silicone tubing (Smooth-On), braided polyester/nylon sleeving, barb fittings, a pressure source.

**Reverse-engineer difficulty:** trivial. The braid angle (≈54.7° "neutral angle") is the whole trick — above it contracts, below it extends.

---

## 2. EHD pump (MIT 2026 — the new part)

**Principle:** an electric field between two electrodes acts on a **dielectric fluid**, dragging it along (ion-drag / conduction pumping). **No moving parts, silent.**

**Parts:** a dielectric fluid (HFE or similar), two mm-scale electrodes, a kV voltage source. That's it.

**Reverse-engineer difficulty:** the *hardest*. The phenomenon (electrohydrodynamics) is 50-year-old physics, but MIT's contribution is **miniaturizing it into a closed loop with the McKibben** so the whole thing is electric + untethered. The principle is documented; the integration is the craft.

---

## 3. TCPA (twisted-and-coiled polymer — the DIY darling)

**Principle:** twist a polymer fiber (nylon fishing line or silver-plated thread) + coil it into a spring. **Heat → the coil tightens and contracts; cool → relaxes.** Joule heating through the conductive coating makes it electric.

**Parts:** nylon fishing line (~$5/spool) or silver-plated nylon thread, a drill to twist it, current for heat.

**Reverse-engineer difficulty:** *easiest.* There are open DIY tutorials. Fully electric, no compressor. The best first muscle to build — it's literally fishing line you twist and it becomes a muscle.

---

## 4. SMA (Nitinol)

**Principle:** Nitinol (Ni-Ti alloy) has two crystal phases. Heating flips martensite → austenite and **contracts 4–8%**; cooling reverses. Silent, electric.

**Parts:** Nitinol wire (off-the-shelf, cheap), current for Joule heating.

**Reverse-engineer difficulty:** easy. Low strain (4–8%) but high force and silent — good for hands, face micro-motion.

---

## The build order (reverse-engineer path)

| Order | Actuator | Why first |
|---|---|---|
| **1** | **TCPA** | cheapest, fully electric, DIY — proves the concept in a weekend |
| **2** | **McKibben** | off-the-shelf parts, higher force |
| **3** | **SMA (Nitinol)** | silent micro-motion (hands/face) |
| **4** | **EHD pump** | the last mile — untethered electrofluidic fibers (v2) |

**The insight:** three of the four are *already* DIY with off-the-shelf parts. TCPA is fishing line. McKibben is tubing + braid. Nitinol is wire. Only the EHD pump is genuinely novel — and its principle (electrohydrodynamics) is textbook, just not yet commoditized.

So the path is: **build a TCPA muscle first** (this week, ~$20 in parts), confirm the force/strain numbers, then stack the others. Once we've got TCPA + McKibben + Nitinol working, we understand 80% of "soft actuation" — and the EHD pump becomes a targeted reverse-engineering project, not a mystery.

---

## Next step (concrete)

Order a **TCPA kit's worth of parts**: nylon fishing line + silver-plated thread + a cheap drill + a bench power supply. Twist a fiber, coil it, run current, watch it contract. That single experiment teaches the principle that all the fancier muscles are built on.

*The muscle is just a twisted string that remembers heat. Everything fancier is that, with better plumbing.*
