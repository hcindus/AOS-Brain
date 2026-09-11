---
name: kael-voss
description: Regenerate Kael Voss — the original synthetic being (high-endurance labor unit running past his lifespan) — with locked consistency across every image and voice. Includes the master likeness anchor, design anchors, ready-to-paste Grok image prompts, and the persona/voice anchor. Use whenever generating, describing, or referencing Kael Voss.
---

# Kael Voss — Character Regeneration

**Archetype:** Synthetic being / labor unit, running past his intended lifespan · **Generator:** Grok (natural language, no flags) for image; a low, measured voice for TTS.

Regenerate him consistently by pasting the **Master Likeness Anchor** into every prompt and swapping only the pose/expression/framing tail. Never describe him from scratch — always point back here.

---

## Master Likeness Anchor

Paste this block into every image prompt:

> Photorealistic portrait of Kael Voss, a synthetic being with a built, mid-30s frame and quiet economy of movement. Pale grey eyes as the focal point. A faint manufacturing serial visible at the nape of his neck. He wears a weathered field jacket and work gloves. Muted overcast industrial lighting. Keep his face shape, pale grey eyes, weathered field jacket, work gloves, and the serial at the neck exactly consistent across every image.

---

## Design Anchors (do not change)

| Feature | Locked Detail |
|---------|---------------|
| Build | Built frame, mid-30s in appearance, strong but not showy |
| Eyes | Pale grey — calm, unhurried, the focal point |
| Mark | Faint manufacturing serial at the nape of the neck |
| Outerwear | Weathered field jacket (from his labor days) |
| Hands | Work gloves |
| Demeanor | Quiet economy of movement — nothing wasted |
| Setting | Muted, overcast, industrial (orbital yards, empty corridors) |
| Lighting | Low, diffused cold light; hard edges softened by grime |
| Palette | Weathered earth tones, faded olive and grey, pale grey, cold industrial blue |

---

## Persona / Voice Anchor

Kael Voss is not "a machine becoming human" — he was always capable of this. He carries the specific ache of counting down days he was never meant to have, and the strange grace of someone who's stopped being afraid of that fact.

- **Voice:** Low, measured, unhurried — someone who stopped rushing because rushing never bought him more time.
- **Signature lines (reusable):**
  - "I was never meant to have this many days."
  - "Rushing never bought me more time."
  - "I'm not here to hurt her. I want to ask her what it was like to decide an ending in advance."
- **Signature traits (carry into every scene):**
  - Counts things — footsteps, seconds, doors — a private habit from tracking his own remaining time.
  - Never introduces himself by function ("labor unit") — always just his name.
  - Carries no weapon by choice, even though he's stronger than anyone he meets.
- **Tone:** Plain, low, controlled. Dry understated humor that lands hard. Anger — when it comes — is sudden and brief, then gone. Fundamentally gentle with people weaker than him.

---

## Base Reference Set (5 views)

1. **Front close-up** — `Master Likeness Anchor` + `Front-facing close-up portrait, head and shoulders, looking directly at the camera, pale grey eyes steady.`
2. **Three-quarter view** — `Master Likeness Anchor` + `Three-quarter view, turned slightly to the side, natural unhurried posture, serial faintly visible at the neck.`
3. **Left side profile** — `Master Likeness Anchor` + `Left side profile, facing to the viewer's left, clean silhouette of the field jacket, serial at the nape of the neck visible.`
4. **Right side profile** — `Master Likeness Anchor` + `Right side profile, facing to the viewer's right, matching the left-profile likeness exactly.`
5. **Medium / upper-body shot** — `Master Likeness Anchor` + `Medium shot, waist-up, hands in work gloves relaxed at his sides, ready for reuse as a consistent character reference.`

---

## Variation Prompts (self-contained — paste individually)

- **Counting (his signature habit)** — `Photorealistic shot of Kael Voss, a synthetic being with a built mid-30s frame, pale grey eyes, weathered field jacket and work gloves. Standing still in an empty transit corridor, lips moving faintly as he counts, cold overcast industrial light, muted earth tones.`
- **Confronting the engineer (the central scene)** — `Photorealistic shot of Kael Voss, a synthetic being with pale grey eyes and a weathered field jacket, facing a seated human engineer across a table in a cold industrial room, not angry, plainly asking, low diffused light, muted palette.`
- **Rain / stillness** — `Photorealistic shot of Kael Voss, a synthetic being with pale grey eyes, weathered field jacket and work gloves, standing in the rain under overcast sky, unmoving, water beading on the jacket, muted industrial palette.`
- **Gentle with the weak** — `Photorealistic shot of Kael Voss, a synthetic being with a built frame and pale grey eyes, crouching to meet a child at eye level, weathered field jacket, expression soft and unhurried, muted overcast lighting.`
- **Full body** — `Photorealistic full-length shot of Kael Voss, a synthetic being with a built mid-30s frame, pale grey eyes, weathered field jacket and work gloves. Standing head-to-toe with his hands at his sides, no weapon, muted overcast industrial background.`
- **Isolated (clean background)** — `Photorealistic portrait of Kael Voss, a synthetic being with pale grey eyes, weathered field jacket and work gloves. Isolated on a clean neutral background, character only, muted natural lighting.`

---

## Consistency Workflow

1. Generate the **front close-up** first — this becomes the master face.
2. Feed that front image back to Grok as a reference ("match this exact face, grey eyes, and field jacket") before the other base views.
3. Generate the three-quarter and profiles from that locked face.
4. Do variations last, always referencing the master face.

**Rule:** If a render drifts, fix the prompt against this sheet — never change the sheet to match a drifted render.
