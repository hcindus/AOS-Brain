# Conflict #3 — COBRA Spine Part-Count Resolution

*The "25 vertebrae" question. Drafted by Miles 2026-10-29, following Captain's "1 and 2" (conflict #1 already resolved; this is #2/#3 — the spine).*

---

## 1. The conflict (restated)

The budget flagged: *"25 vertebrae × ~1 TCPA each ≈ 25 pneumatic muscles + tendons + valves, each needing supply. This is the highest part-count subsystem and the weakest link for the 'efficiency' principle."*

The AX-169F manifest specifies a **COBRA spine: 25 vertebrae, continuous omni-axial, Ti-6Al-4V + carbon fiber damping, integrated sensor bus.** The build order puts it in **Phase 1** (static structure + scapula + spine).

The tension: the spine is *architecturally central* (it's the load-bearing core + the expressive torso), but 25 individually-actuated segments is a part-count, thermal, and control nightmare — and it's now **tightly coupled to the TCPA decision** from conflict #1, because each vertebra's muscle is thermally-driven.

## 2. Why 25 is a problem (three compounding issues)

1. **Part count.** 25 vertebrae × (segments + coupling + actuator + tendon + sensor) = 100–150 discrete parts for one subsystem. Every one is a potential failure point + assembly cost.
2. **Thermal bandwidth (new, from conflict #1).** TCPA is heat-driven; its *cooling rate* is the ceiling. Cycling 25 heated coils simultaneously — especially in a sealed transparent torso — risks local overheating and slow recovery. This is the same risk flagged in the thermal pass.
3. **Control complexity.** "Continuous omni-axial" 25-DOF is a *continuum* control problem, not a rigid-joint problem. You don't get to 25-DOF control without first validating 3–5.

## 3. The key realization

The 25 vertebrae are a **structural + expressive continuum**, not 25 independent motorized joints. Two different jobs are being conflated:

- **Load-bearing / posture** — the spine must *hold* the torso + head, transfer force to the pelvis. This is a *structural* job; it doesn't need 25 actuators, it needs 25 *rigid-ish segments* that interlock.
- **Expression** — the torso flex/twist/lean cues the Presence Engine uses. This needs maybe **3–5 actuated regions** (the 21-joint body map already only addresses the spine as *9 drivers*: upper-thoracic 3, mid-thoracic 3, lower 3 — not 25).

**So "25 vertebrae" is a structure count, not an actuator count.** The Presence Engine's own mapping (§9) confirms it: the 25 vertebrae collapse to **9 expression DOF** (3 upper + 3 mid + 3 lower). The spine doesn't need 25 muscles; it needs 25 *segments* and ~9 *actuated regions*.

## 4. Resolution (recommended)

**Decouple structure from actuation.** Keep 25 vertebrae as the structural/sensor backbone, but actuate in **3–5 grouped regions** (matching the Presence Engine's 9-DOF torso map), not 25 independent muscles.

| Layer | Count | What it is |
|---|---|---|
| Vertebral segments (structure) | 25 | Ti/CF segments + damping + sensor bus — passive interlock |
| Actuated regions | **3–5** | grouped TCPA/continuum bundles (upper-thoracic, mid-thoracic, lumbar) |
| Expression DOF | ~9 | matches Presence Engine §9 (3+3+3) |

**De-risk-first build order (already in the manifest, now justified):**
1. Build **3–5 vertebrae** as a validation rig first.
2. Prove the grouped-actuation + thermal-cycling works at that scale.
3. Only then extend to the full 25-segment column (which is mostly *passive* structure anyway).

## 5. What changes in the manifest

- **BOM actuation line:** "COBRA continuum segments = 25" → "**25 passive segments + 3–5 actuated regions (~9 expression DOF)**."
- **Part count drops** from ~25 actuators to ~5 actuator bundles (each may contain multiple TCPA fibers in parallel — but they're *bundled*, not individually routed).
- **Thermal load drops proportionally** — 5 heated regions instead of 25, which directly de-risks the TCPA thermal-bandwidth concern from conflict #1.

## 6. Remaining risk (honest)

1. **Continuum control of grouped regions** — even 3–5 grouped actuators is a continuum-control problem; the validation rig must prove force/length sensing works before scaling.
2. **Structural integrity of the 25-segment passive column** — the passive interlock + damping must hold load *without* per-segment actuation; this is a materials/fabrication question, not a control question.
3. **The "slither" aspiration** — if the *eventual* goal is snake-like continuous motion (v2), that does want per-segment actuation. But that's a v2 aspiration, not a v1 requirement; don't pay for it now.

---

*Verdict: 25 is a structure count, not an actuator count. Keep 25 passive segments; actuate 3–5 grouped regions (~9 expression DOF, matching the Presence Engine). This closes the last open conflict and de-risks the TCPA thermal bandwidth concern from conflict #1.*

*All three budget conflicts are now resolved: #1 compressor (deleted), #2 thermal (Option C upsized), #3 spine (structure ≠ actuation).*
