---
name: scale-film-to-series
description: Turn a short film into a full episodic series using an AI studio — writing stages (logline → outline → cliffhanger chain → scripts), cast/world locking, scene-per-render shooting, and autopilot. Use when scaling a finished short into a season.
---

# Scale Film → Series (the "pilot" play)

**KPI:** Turn one short film into a coherent season — one story cut at deliberate cliffhanger points, not ten short films in a row.

## Writing stages (run in order; re-run any stage you dislike)

**What you feed it (one of):**
- A single line — the premise/logline.
- An existing script — paste it and skip straight to casting.
- A longer text — up to 24,000 chars (treatment or short story).

Then set the writing voice + content guidelines (same decisions as module 1, but straight into the studio).

**The positioning interview:** at most 6 questions on genre, setting, dramatic situation. Answer, or press "Let AI decide the rest."

**What comes back:**
- A series logline — one sentence that must carry ten episodes, not three minutes.
- Per-episode outline with a stage goal + emotional beat each.
- A **cliffhanger chain** — each episode ends where the next begins.
- Full scripts, generated in batches across scenes.

### Read the cliffhanger chain closely
A season is one story cut at nine deliberate points. If episode four ends somewhere comfortable, the viewer stops there. The outline is cheap to regenerate (a language-model turn, not a render) — get the arc right *before* generating frames, because frames are where the credits go.

## Cast once, shoot every episode
- A project holds up to **12 characters, 30 environments, 30 props**. Each gets a reference image generated in-studio (Nano Banana 2, GPT Image 2, Seedream, Z-Image). Once approved, that reference is **locked for the whole season**.
- The character-reference-sheet idea, extended to sets/objects: save a location in ep 1, reuse it in ep 9 — same room, light, window.

## Shooting scenes
- Each scene renders as **one complete generation**, not shot-by-shot. The cinematography prompt asks the model for shot variation *inside* the render (wide, closer angle, insert).
- Engine per project: Seedance 2.0 / 2.5, MiniMax H3, HappyHorse 1.1, Gemini Omni. Output 9:16 vertical, or 16:9 / 1:1.
- Before rendering, read every scene prompt + which reference images it uses. Edit the prompt there — far cheaper than regenerating after.

## Autopilot
- Scripts + shoots one episode at a time, unattended. Pauses when credits run out; resumes at the first unfinished item on top-up. Nothing generated is lost or repeated.
- **Autopilot is not a reason to skip the outline** — it will faithfully shoot a weak arc to episode twelve. Read the outline + cliffhangers first, then let it run.

## Chaining vs. one-render-per-scene
- Chaining (6s clips) = frame-level control → right for a *short film*.
- One render per scene = volume → right for a *series*. You trade some control for scale and ask the model to vary shots inside the render.

## Rules
- Re-run the outline until the arc is right — it's cheap; frames are not.
- Lock references before shooting; consistency across episodes is the product.
- Edit scene prompts pre-render, never post.
- Feed your existing film's script as episode one — it already has a working first act.
