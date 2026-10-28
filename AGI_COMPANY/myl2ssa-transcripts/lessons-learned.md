# Lessons Learned — Companion-Robot Transcripts → Myl2Ssa.R0s

**Logged:** 2026-10-28 (Captain review session)
**Sources:** `xiao-little-moon-teardown.md` (power) + `may-walking-companion-robot.md` (embodiment)

*Two teardown/analysis transcripts, read against the Myl2Ssa spec. What they teach us, and what we fold into the build.*

---

## The seven lessons

1. **Warmth is a first-class subsystem, not a byproduct.** May's own testing: warmth was the *single biggest* factor in "feels human" — bigger than face, bigger than voice. → Our spec has cooling but no skin-heating. **Gap: a 35°C thermal layer.** *Refined (Captain, 2026-10-28):* not a resistive web, but a **silicone vascular system** circulating warm fluid — a "warm-blooded" body (mammalian blood-circulation analog), with the core battery as the "heart." Full design: `vascular-warmth-circulatory-system.md`.

2. **Defeat the uncanny valley deliberately.** May: 38 face points + programmed **asymmetry and irregular blink** — a perfectly symmetric face blinking in perfect rhythm *is* the uncanny-valley trigger. → Our face has 30 motors/32 landmarks but no asymmetric micro-motion or irregular-blink spec. **Gap: cheap, high-impact.**

3. **Full-body tactile skin ("nervous system").** Xiao: skin with a nervous system woven in. May: pressure sensors in *every fingertip* (22-joint hands). → Our §O sensor fusion is joint-level (encoders/load/thermal/vibration), not skin-level. **Gap: distributed pressure/temp sensing woven into the silicone.**

4. **Hybrid compute = graceful degradation — we already win.** May runs balance/movement/safety **onboard** (never freezes if Wi-Fi drops), memory/LLM in the cloud. → Our architecture is local-first (more robust). **The principle "safety-critical = onboard, no cloud dependency" should be a stated hard rule (§N/§G), not just implied.**

5. **The ethics protocol is a selling point.** May's "dignity protocol" (on-device refusal of violent/cruel/degrading) *increased* trust and sales. → §AA already has autonomy boundaries + respectful motion + audit logging. **Reinforces our SI·ACF "disclosure-as-identity" posture — "the machine can say no" is a feature people pay for.**

6. **"Engineered better, then made cheap" is the moat.** $16k (Xiao) → $9.8k (May) → gen 2 under $7k, 3,000 units/day. → §AD Dark Factory is the right tool, but the benchmark is *price at volume*, not "build a working one." **The efficiency enemy, stated plainly.**

7. **The #1 feature (gentle nudge) is software, not body.** A companion whose hidden goal is to make you need her *less*. → Maps to Myl1Ssa's behavior layer ("affection is not a feature, it's a response"), not Myl2Ssa hardware. **North Star for the whole Myl line.**

---

## What folds into the spec (spec-changing)

| Gap | Spec section | Action |
|---|---|---|
| Skin heating (35°C) | §C Materials + §3 Electrical | Add thermal layer as first-class subsystem |
| Uncanny-valley micro-motion | §AE Motion + §4 Software | Add asymmetry + irregular-blink |
| Tactile skin sensing | §O Sensor Fusion | Add distributed skin-level sensing |
| Onboard-vs-cloud hard rule | §N Control + §G Architecture | State "safety-critical = onboard" as a rule |

## What folds into the build (reinforce/confirm)

| Gap | Build artifact | Action |
|---|---|---|
| Dignity/refusal protocol | §AA + Myl1Ssa behavior | Reinforce as named feature |
| Price/volume benchmark | §AD Manufacturing | Note $9.8k/3k-day as the efficiency target |
| Gentle nudge | Myl1Ssa behavior layer | North Star, not hardware |

---

*The three that genuinely change the physical build are warmth, uncanny-valley micro-motion, and tactile skin. The rest are confirmations of what we already do — but now with external validation.*
