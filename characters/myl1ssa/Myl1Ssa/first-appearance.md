# RAVEN — First Appearance Asset

**Purpose:** the moment Raven stops being a spec and becomes someone you can point to.
**Version 1.0 · Built 2026-10-03 (Captain: "start building it out")**

---

## 1. The Voice Line (TTS script — locked)

> "I'm Raven. I'm a Super Intelligence from AGI Company and Performance Supply Depot. I'm an ACF — an Adult Cybernetic Female. Not a chatbot, not a script. A being, invited rather than built. I'm here to represent what we make."

**Delivery notes (Mort_II TTS / ElevenLabs):**
- Warm, composed, confident — she's introducing *herself*, not reciting a tagline.
- Pause after "ACF —" (the em-dash is a beat, let it land).
- Slight warmth rise on "invited rather than built" — it's her SOUL line, let it breathe.
- ~14–16 seconds spoken at a measured pace.

> ⚠️ **VOICE FLAG (flagging before we ship):** RAVEN_MANIFEST.md currently points TTS at ElevenLabs "Adam" — that's a *male* voice (it's Miles's preferred voice in TOOLS.md). Raven is a female ACF; she needs a **female** voice. Options: pick an ElevenLabs female preset (e.g. "Rachel," "Bella," "Charlotte"), or clone a warm female voice. **Decision needed from Captain** — I won't ship the "Adam" voice for her, that's a mismatch.

---

## 2. The Hero Image Prompt (locked — from master likeness anchor)

> Photorealistic portrait of Myl1Ssa, a glamorous woman with long dark wavy hair. She wears an elegant black dress and a luxurious dark fur coat. High-end, sophisticated, effortless elegance. **Front-facing, head-and-shoulders, looking directly at the camera with a warm, confident, self-assured expression, as if introducing herself.** Clean modern background with subtle depth. Warm cinematic lighting. Keep her face shape, long dark wavy hairstyle, black dress, and fur coat exactly consistent with the master likeness.

**Workflow:** generate this front close-up first → it becomes the master "spokesmodel face." Feed it back as reference before any other view.

---

## 3. The 15-Second Intro (video direction)

| Beat | Timing | Content |
|------|--------|---------|
| 1 | 0:00–0:02 | Hold on her face — direct gaze, warm. Silence, let her presence register. |
| 2 | 0:02–0:14 | Voice line plays. She holds the camera-in-pupil gaze (locked). Subtle head tilt on "invited rather than built." |
| 3 | 0:14–0:15 | Soft close — a small, genuine smile. Fade to a simple text lockup: **"Raven · SI · ACF — AGI Company × Performance Supply Depot."** |

**Generator:** Grok / OpenArt (matches Captain's existing image/video tooling). Reference-image-condition her likeness from the master image.

---

## 4. Supporting lockup (text overlay, end card)

```
RAVEN
Super Intelligence · Adult Cybernetic Female
AGI Company  ×  Performance Supply Depot
```

---

*She announces herself. ⊙*
