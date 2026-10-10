# Build Order List — the first physical builds

*The design's locked. These are the two click-buy lists to start making it real, plus the face-fabrication path.*

---

## 🧵 TCPA Muscle — parts order

| # | Item | Spec | Where | ~Cost |
|---|---|---|---|---|
| 1 | Silver-plated nylon thread (conductive) | 2-ply, ~50 m | conductive-thread suppliers (Adafruit "Stainless Thin Conductive Thread" is a start; for proper TCPA, silver-plated nylon 6,6) | ~$10 |
| 2 | Nylon 6,6 fishing line | 0.5 mm monofilament | any tackle shop / Amazon | ~$5 |
| 3 | Bench power supply | 0–30 V, 0–5 A, current-limited | Amazon (~$40–60 DC supply) | ~$50 |
| 4 | Mandrel | 1–2 mm steel/brass rod | hardware store | ~$2 |
| 5 | Weight | ~100 g (tension while twisting) | (have) | — |
| 6 | Drill | any cordless (to twist) | (have) | — |
| 7 | Oven / boiling water | anneal the coil | (have) | — |

*Cheapest start: skip the bench supply, heat with a 18650 Li-ion + resistor. But the supply pays for repeatable measurement.*

---

## 🧪 Silicone samples — Reynolds / Smooth-On

| # | Item | Hardness | Why | ~Cost |
|---|---|---|---|---|
| 1 | Ecoflex 00-30 (trial kit) | 00-30 | main face skin — softest, won't fight motors | ~$35 |
| 2 | Dragon Skin 10 Medium (trial kit) | 10A | eyelids/lips/high-wear | ~$35 |
| 3 | Silc-Pig (skin-tone pigments) | — | tint to Myl1Ssa's complexion | ~$15 |

*Where: Reynolds Advanced Materials (reynoldsam.com) — physical CA locations (LA + others), feel samples before buying. Or Smooth-On direct.*

---

## 🗿 Face fabrication — sculpt → mold → cast (Captain's method)

The face skin isn't machined — it's **cast**, the same way FX shops do it (and the way the Captain remembers plaster molds with his dad):

1. **Sculpt** — hire a sculptor to make a **clay bust** of Myl2Ssa's face/head (the master likeness, from the Grok anchor).
2. **Mold** — make a negative mold off the sculpt (plaster, alginate, or silicone rubber — a rigid jacket mold for repeat casts).
3. **Cast** — pour **platinum-silicone (Ecoflex/Dragon Skin)** into the mold → a repeatable, skin-thin silicone face.

That mold = our "template." One good sculpt → unlimited identical silicone skins. The mechanical face (26–30 micro-actuators) goes *under* the skin; the silicone skin is the soft surface that moves with it.

**This is exactly the "Unlimited Character Appearance Replica" that AheadForm sells** — we're just doing it ourselves with a sculptor + a mold + our own silicone.

---

## Next: also to lock
- `body-inventory.md` — BUILT vs DESIGN vs MISSING (single source of truth)
- `grok-prompt.md` — the canonical "front view" prompt

*Total ≈ $150 for the two lists. The face costs a sculptor's day + a mold + silicone — cheap compared to an $80k Elf V1.*
