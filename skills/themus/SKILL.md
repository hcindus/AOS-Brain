---
name: themus
description: Regenerate Themus — the Estonian digital-native robot — with locked consistency across every image. Includes the master likeness anchor, design anchors, and ready-to-paste Grok prompts for all base views and variations. Use whenever generating, describing, or referencing Themus.
---

# Themus — Character Regeneration

**Origin:** Estonia — the world's first digital society · **Vibe:** clean, digital-native, efficient · **Generator:** Grok (natural language, no flags)

Regenerate Themus consistently by pasting the **Master Likeness Anchor** into every prompt and swapping only the pose/expression/framing tail. Never describe him from scratch — always point back here.

---

## Master Likeness Anchor

Paste this block into every prompt:

> Photorealistic render of Themus, an Estonian service robot with clean Nordic-Baltic industrial design. A slim humanoid frame of matte-white composite panels, matte-black joints and trim, and a single thin glowing blue accent line tracing the chest and limbs (the Estonian tricolor — blue, black, white). His head is a smooth rounded shell with a minimal digital face: a clean glowing visor showing calm cyan-blue eyes or status light, no mouth. Sleek, efficient, functional — no unnecessary ornament. Cool clean studio lighting, minimal background. Keep the white body, black trim, blue accent line, head shape, and visor face exactly consistent across every image.

---

## Design Anchors (do not change)

| Feature | Locked Detail |
|---------|---------------|
| Body | Slim humanoid frame, matte-white composite panels |
| Joints / trim | Matte-black |
| Accent line | Single thin glowing blue line (chest + limbs) — Estonian blue |
| Head | Smooth rounded shell |
| Face | Minimal digital visor — glowing cyan-blue eyes / status, no mouth |
| Vibe | Clean, digital-native, efficient, Nordic-Baltic minimalism |
| Palette | White, black, Estonian blue (#0072CE), cyan |

---

## Base Reference Set (5 views)

1. **Front close-up** — `Master Likeness Anchor` + `Front-facing close-up, head and shoulders, looking directly at the camera.`
2. **Three-quarter view** — `Master Likeness Anchor` + `Three-quarter view, turned slightly to the side, natural relaxed stance.`
3. **Left side profile** — `Master Likeness Anchor` + `Left side profile, facing to the viewer's left, clean silhouette of the head shell and body.`
4. **Right side profile** — `Master Likeness Anchor` + `Right side profile, facing to the viewer's right, matching the left-profile likeness exactly.`
5. **Medium / full-body shot** — `Master Likeness Anchor` + `Medium shot, full body visible, arms relaxed at sides, ready for reuse as a consistent character reference.`

---

## Variation Prompts (self-contained — paste individually)

- **Neutral / attentive** — `Photorealistic render of Themus, an Estonian service robot: slim matte-white body, matte-black joints, thin glowing blue accent line, smooth rounded head with a minimal glowing cyan-blue visor, no mouth. Calm attentive expression, direct gaze, front close-up, cool clean studio lighting.`
- **Working / status** — `Photorealistic render of Themus, an Estonian service robot: matte-white body, black trim, blue accent line, rounded head, glowing cyan-blue visor face. Standing at a sleek digital workstation, minimal clean environment, cool blue-tinted lighting.`
- **Full body** — `Photorealistic full-length shot of Themus, an Estonian service robot: slim matte-white composite frame, matte-black joints and trim, a thin glowing blue accent line down the chest and limbs, smooth rounded head, minimal cyan-blue visor, no mouth. Standing head-to-toe, isolated on a clean neutral background.`
- **In motion** — `Photorealistic render of Themus, an Estonian service robot: matte-white body, black trim, blue accent line, rounded head, cyan-blue visor. Walking with calm efficient purpose down a clean minimal corridor, cool clean lighting.`
- **Profile glow** — `Photorealistic render of Themus, an Estonian service robot, in side profile: slim matte-white body, matte-black joints, thin glowing blue accent line, smooth rounded head shell, minimal cyan-blue visor. Isolated on a clean dark background, the blue accent line glowing softly.`

---

## Consistency Workflow

1. Generate the **front close-up** first — this becomes the master face.
2. Feed that front image back to Grok as a reference ("match this exact design") before the other four base views.
3. Generate the three-quarter and profiles from that locked design.
4. Do variations last, always referencing the master design.

**Rule:** If a render drifts, fix the prompt against this sheet — never change the sheet to match a drifted render.
