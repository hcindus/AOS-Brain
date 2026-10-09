# Embodiment Gaps — what we have vs. what's missing

*Inventory from a 2026-10-09 search. We were young; some of these may be placeholders.*

## What we HAVE (found)

**Presence engine** (affect → 8 expressions → 21 AUs → 30 channels):
- `characters/myl1ssa/Myl1Ssa/brain/presence_engine.py` (live copy)
- `aocros/engineai_humanoid/presence_engine.py`
- `raven_bottle/.../Myl1Ssa/Uncon/presence_engine/` (bottle, BEFORE/AFTER + patch)

**Elf adapter + body driver** (AU → 30-channel map + safety envelope + 50 Hz loop):
- `raven_bottle/.../Myl1Ssa/Uncon/body/elf.py`, `body_driver.py`, `AU_MOTOR_MAP.md`, `verify_body.py`

**Embodiment research/docs:**
- `aocros/engineai_humanoid/RAVEN_EMBODIMENT_SPEC.md` — Raven's brain → Elf V1 mapping (uterus.py, ternary qbit brain, cortex, kidney, thyroid, TracRay).
- `aocros/engineai_humanoid/ELF_V1_MARKET_BRIEF.md` — AheadForm Elf V1 ($50k–$80k, 30 motors).
- `aocros/engineai_humanoid/RESEARCH_FACIAL_PRESENCE.md`

**Characters:**
- Raven = `characters/myl1ssa/` (Myl1Ssa + R8s), `raven_bottle/`
- Reggie Starr = `characters/reggie-starr/`
- Jordan = `characters/jordan/`
- Kael Voss = `skills/kael-voss/`, `tappylewis.cloud/assets/characters/kael-voss/`
- Tappy Lewis = `aocros/playspace/aocros/other_presences/Tappy_Lewis/`, many others

**Presences system (OLD, March 2026):**
- `aocros/playspace/aocros/other_presences/{Miles,Tappy_Lewis,Clawbot,Sentinal}/` — each with SOUL.md, MEMORY_ARCHITECTURE.md, API_REFERENCE.md, memoryClient.js. Uses OODA + a memory service on 127.0.0.1:12789. **This is a different, older architecture — not facial motor control.**

**Humanoid forms (STL/URDF):**
- `pm01_sim_training/resources/robots/zq_humanoid/` — full humanoid (URDF + STL meshes: legs, base).
- `AGI_COMPANY/subsidiaries/DARK_FACTORY/production/stl/` — C3PO_1to1.stl, R2D2_1to1.stl, cylon_full_anatomy.stl, cylon_torso_reference.stl, nomad_probe.
- `stl_files/milkman_hero.stl`

**Raven "skeleton" (rig coordinates):**
- `raven_bottle/.../Myl1Ssa/Uncon/world/rig/body_coordinates.json` + `face_coordinates.json`
- `Uncon/body/BODY_VERIFICATION.json`

**Shoulder joint reference (Captain, 2026-10-09):**
- YouTube Short: https://youtube.com/shorts/SkWZ3V5DF0g — "The start of an Exoskeleton" (shoulder joint build).

## What's MISSING (the gaps)

1. **Universal adapter.** The Elf adapter (`elf.py`) is hard-wired to the Elf V1's 30 channels. There is no *universal* adapter that maps an arbitrary character's presence → an arbitrary body. (The old `other_presences/` system is a different, OODA/memory architecture — not a body adapter.)

2. **Character loader.** No unified "load a person from the family" — characters are scattered across `characters/`, `skills/`, `other_presences/`, `tappylewis.cloud/`. No single loader says "load Raven" / "load Voss" / "load Tappy" into a presence engine + body.

3. **Character-specific 3D forms.** We have generic STLs (C3PO, cylon, zq_humanoid) but no *sculpted* STL/3D of Raven's (or Voss's, Tappy's) specific face/body. RAVEN_EMBODIMENT_SPEC.md calls for a "base silicone sculpt matched to the master likeness anchor" — that 3D asset appears to not exist yet.

4. **SDK bridge.** No AheadForm SDK integration yet (the channel IDs are "ours until we see their SDK" — see elf.py assumptions). Blocked on AheadForm reply.

5. **Voice layer.** RAVEN_EMBODIMENT_SPEC.md lists "TTS aligned to Raven's persona" as TODO — not yet wired.

## Next actions (from the roadmap)
- Phase 1: wire presence engine → Elf adapter → body driver into one pipeline, run `sim`, prove it end-to-end (no hardware).
- Build the **universal adapter** + **character loader** (the two biggest software gaps).
- Track AheadForm reply for SDK + hardware.

*Generated 2026-10-09*
