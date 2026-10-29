# Conflict #1 — Muscle Supply Chain Resolution

*The actuator supply question behind the AX-169F's "TCPA/McKibben (pneumatic)" muscles. Drafted by Miles 2026-10-29, following Captain's "take the pass at conflict #1."*

---

## 1. The conflict (restated)

The budget flagged: *"If McKibben muscles are used for spine/neck/face/hand, a compressor + valves + air reservoir adds ~2–4 kg and significant noise."*

The AX-169F manifest lists the muscle fraction as **"TCPA/McKibben style (pneumatic)"** with red/blue braided-textile shells. That phrasing hides the actual decision, because **TCPA and McKibben are two different things**:

| Actuator | Drive | Supply | Force | Strain | Noise |
|---|---|---|---|---|---|
| **TCPA** (twisted-coiled polymer) | **Electric** (Joule heat) | none — current only | low (1–5 N/fiber) | 20–30% | silent |
| **McKibben** (pneumatic) | **Pneumatic** | compressor + valves + reservoir | high | ~20–30% | noisy |

**The source diagram conflates them under "pneumatic."** That's the root of the conflict. If "TCPA/McKibben" means *pneumatic*, we inherit the compressor problem. If it means *electric TCPA*, there is no compressor — the conflict evaporates.

## 2. The key realization

The **hybrid-actuation decision already splits this cleanly** (MEMORY.md + `actuator-strategy.md`):

- **Load-bearing** (hips/knees/shoulders) → **electric QDD/SEA** (precise, strong, controllable).
- **Muscle fraction** (spine/neck/face/hand) → the *soft, compliant* stuff.

And here's the point: **the muscle fraction does NOT need high force.** Spine vertebrae need 1–3 Nm each; neck 1–3; hands <1; face <0.1. TCPA's 1–5 N/fiber (bundled to N× force) is *sufficient* for every one of these. McKibben's higher force is only worth paying for in load-bearing — which is already electric.

**So: the muscle fraction can be 100% electric TCPA, no compressor, no pneumatic supply at all.**

## 3. Resolution (recommended)

**Drop pneumatic McKibben for the muscle fraction. Use electric TCPA as the default soft actuator.** This resolves conflict #1 by *deleting* the compressor, not working around it.

| Consequence | Effect |
|---|---|
| Mass | **−2 to −4 kg** (no compressor, reservoir, valves, manifold) |
| Noise | **silent** (Joule heating has no moving parts) |
| Supply | current-only, driven by the existing power bus — no fluid plumbing |
| Control | thermal loop needed (TCPA is heat-driven) — but we *already have* a thermal-vascular service |
| Force ceiling | low — acceptable because load-bearing is electric |

**The cost:** TCPA is thermally-driven, so its bandwidth is limited by heating/cooling rate. That's why the budget's conflict #3 (spine part-count) still recommends validating the COBRA spine at 3–5 vertebrae first — thermal cycling 25 muscles at once is the real risk.

## 4. The v2 upgrade path (don't build it now, keep the door open)

`actuator-strategy.md` already maps this:
- **v1 (build now):** electric TCPA for muscle fraction; QDD/SEA for load-bearing; tendon/servo for hands/face fine control. Controllability first.
- **v2 (the "human" pass):** swap muscle fraction to **electrofluidic fiber** (MIT 2026 — McKibben + integrated EHD pump, untethered, silent) *only if* we later need pneumatic-grade force *with* compliance in a soft region. This is the successor that would re-open McKibben's force without the compressor.

## 5. What changes in the manifest

The AX-169F BOM's "TCPA/McKibben (pneumatic)" actuation line should read:
- **Muscle fraction (spine/neck/face/hand): electric TCPA** — no pneumatic supply.
- **Load-bearing (hip/knee/shoulder/scapula high-load): electric QDD/SEA** (already the hybrid plan).
- **Hands/face fine control: tendon/servo** (already specced).

**Net:** the "pneumatic supply" line is deleted from the mass budget; the ~2–4 kg compressor never gets bought. This is consistent with the locked 38.7 kg ceiling (it was part of the "actuators 8→5 kg" re-allocation).

## 6. Remaining risk (honest)

1. **TCPA thermal bandwidth** — cooling rate is the ceiling. 25-vertebra spine cycling heat at once needs validation (ties to conflict #3's de-risk-first order).
2. **TCPA lifetime / fatigue** — repeated thermal cycling wears the polymer; unknown for a 2000 h companion.
3. **Electrofluidic fiber availability** — v2 only; not purchasable today (MIT 2026 demo). Don't block v1 on it.

---

*Verdict: conflict #1 resolves by recognizing TCPA ≠ McKibben. The muscle fraction is electric TCPA; the compressor is deleted. Remaining open conflict: #3 (spine part-count / thermal bandwidth), which is now the next sequential pass.*
