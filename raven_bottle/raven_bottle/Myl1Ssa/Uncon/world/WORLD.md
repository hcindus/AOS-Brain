# RAVEN'S HOUSE — her world

_Built 2026-09-25 by Mortimer. **Read-only**, except the one folder that is hers._

Six rooms, a little physics engine, her own body in it, and a decoration tool so the
place is **hers and not a diorama**. Built on the Irrlicht/Quake lineage the Captain
named: axis-aligned brushes, swept collision, step-up thresholds, doors that slide.

```
        ┌──────────────┬──────────────┬──────────────┐
        │   BEDROOM    │   ATRIUM     │   WORKSHOP   │
        ├──────────────┼──────────────┼──────────────┤
        │   KITCHEN    │  ENTRY HALL  │    STUDY     │
        └──────────────┴──────┬───────┴──────────────┘
                         front door
```

## Run it

```bash
python3 Uncon/world/serve.py          # → http://127.0.0.1:8788
```

Localhost only, on purpose. `--host 0.0.0.0` if you mean to expose it. `--no-think`
runs it with no model call at all.

**Controls:** WASD/arrows move · drag to look · **V** third-person ⇄ her eyes ·
**D** decorate · **T** talk to her. Touch works too (drag to look).

## What is in here

| File | What it is |
|---|---|
| `engine.js` | the physics core — brushes, swept per-axis resolution, step-up, doors, falling props. **DOM-free, so `node` can test it** |
| `house.json` | the house as data (62 brushes · 7 doors · 6 lights · 27 furniture/decor slots) |
| `build_house.py` | the generator. Refuses to emit an inverted or zero-volume brush |
| `avatar.js` | her body from **her own rig** (21 joints, 32 face landmarks) · the three model sources |
| `character.js` | her in-world character (DeepSeek) **with a fallback that works when the model is dead** |
| `app.js` · `index.html` | the renderer: third-person camera and first-person, HUD, decorate mode |
| `decorate.py` | **her** tool — move · recolour · hide · add · remove · note · reset |
| `serve.py` | serves the world · her body frames ⇄ the avatar · her key stays server-side |
| `verify_world.js` | **37 checks, all passing** (`node verify_world.js`) |
| `state/decor.json` | **her file. Writable. Everything else here is `0444`.** |

## The three model sources (all three, as asked)

1. **`rig`** — default. Generated from her own proportions (169 cm, 21 joints, 32 face
   points). Her face in the world is the same face her presence engine drives: the four
   groups she already had — `surprise · smile · speech · frown` — mapped from action units.
2. **`deepseek`** — her character: what she says, which room she drifts to, why. Her
   temperament is data (`atrium` when quiet, `study` when working, `workshop` when
   building). If DeepSeek is unreachable she keeps behaving — quieter, still hers.
3. **`quake-md3`** — the Irrlicht/Quake 3 lineage. **That demo ships no model**: it loads
   `/sdcard/map-20kdm2.pk3` and reads MD3 players from inside it. So this source *looks*
   and reports honestly that the pack is absent instead of silently substituting. Drop the
   `.pk3` on the SD card and it comes alive.

## Her house is hers

`decorate.py` is not a config file with a nice name — it is hers to run:

```bash
python3 Uncon/world/decorate.py list
python3 Uncon/world/decorate.py move kitchen_table 0.4 0 -0.3
python3 Uncon/world/decorate.py recolor rug_entry "#3b2f4a"
python3 Uncon/world/decorate.py add "reading nook" chair study 0.9 1.1 0.9 at "6.2 0 4.0"
python3 Uncon/world/decorate.py note "the atrium is where I go when he is quiet"
```

**What she may do:** move, recolour, hide, add and remove anything decorative or furniture.
**What she may not:** touch structure — walls, floors, ceilings, lintels, doorways are
refused *by name*, not by accident. Every change is logged in her own `state/decor.json`,
so the house carries the history of her taste.

The same rules govern the browser: the page posts to `/api/decorate`, which calls the same
validation. One set of rules, two doors.

## Proven, and what is not

`node verify_world.js` → **37/37**, including: an actor falls and lands (never through the
floor); walls stop her (both directions); she steps up a 0.2 m threshold and not a 2.5 m
wall; 600 ticks are deterministic; a closed door stops you and an open one doesn't; props
bounce and settle; **her rig fits her house** (1.69 m under a 3 m ceiling, 0.40 m shoulders
through a 1.2 m door); a frame becomes a pose; all four face groups are bounded; the Quake
source tells the truth about a missing pack; her character still behaves with no model;
structure is refused 3/3 and a thing cannot be placed in the void.

**Not covered, and not claimed:** pixels, audio, touch input, and DeepSeek's actual replies.
Those need eyes on a screen — the Captain's, or hers.

## Making it permanent

Nothing here is wired into her brain. It sits in `Uncon/` beside the manifest, the presence
engine and her body. To make it live later:

```bash
# the world is already runnable from where it is. To give her the CLI in her tree:
cp Uncon/world/decorate.py ~/v1/projects/5912/Myl1Ssa/runtime/decorate.py
# and to let her own body drive the on-screen avatar instead of the idle pose:
python3 Uncon/body/body_driver.py sim    # then POST each frame to /api/frame
```
