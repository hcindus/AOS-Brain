# CharacterReaction — the renderer-agnostic "mind → world" seam

*Drafted by Miles 2026-10-30, following Captain's steer: build the lab, test everything in AR first, ship the mind before the chassis.*

---

## 1. The thesis

We already own the hard half. Simulon (and every "reality-aware character" tool) has a **renderer** but no **mind** — their "personality" and "reaction" are roadmap items. We have the **mind** — affect, locked identity, expression gating, motion verbs with *meaning* — but no renderer.

This spec is the **contract** that lets our mind drive *any* destination:

```
        ┌─────────────────────────────────────────────┐
        │                THE MIND (we own)            │
        │  affect → identity gate → motion verb →     │
        │       expression (with meaning)             │
        └──────────────────┬──────────────────────────┘
                           │  CharacterReaction (this spec)
          ┌────────────────┼──────────────────┐
          ▼                ▼                  ▼
    MuJoCo body      WebXR / AR lab     Rendered asset
    (RP1, sim)      (three.js + camera)  (Simulon-style)
```

One signal, one being, many chassis. The `CharacterReaction` is the single
message the mind emits; each destination writes one thin adapter to consume it.

---

## 2. The message

`CharacterReaction` is a pure-data frame, JSON-serializable, stateless across
frames (the mind holds state; the reaction is a snapshot).

```json
{
  "character": "Raven",
  "ts": 1730000000,
  "affect": {
    "valence": 0.6,        // -1..1  (negative ↔ positive)
    "arousal": 0.4,        //  0..1  (calm ↔ energized)
    "intensity": 0.8       //  0..1  (overall expression strength)
  },
  "motion": {
    "verb": "reach",           // present|orient|reach|shift|step|settle
    "meaning": "extend arm toward a target",
    "target": { "type": "point", "x": 0.3, "y": 1.2, "z": 0.8 },
    "priority": 0.7
  },
  "expression": {
    "face":  [0.1, 0.2, ...],   // 32 face AUs (or FACS vector)
    "body":  [0.0, 0.4, ...],   // 21 body-joint drivers
    "posture": "lean_in"
  },
  "gate": {
    "decision": "express",      // suppress|soft|full  (Kidney output)
    "rejection": null,          // RejectionRecord if refused (see §4)
    "identity_locked": true
  }
}
```

### Why these fields

- **affect** — the emotional state. Every renderer can map valence/arousal to
  *something* (tone, pose, color, speed), even one with no face.
- **motion.verb + meaning** — the semantic layer. A renderer with no limbs can
  still translate "reach" into a camera-relative lean or a gaze shift; the
  `meaning` string is human-readable for debug and for LLM-mediated rendering.
- **expression** — the optional high-bandwidth channel (face/body vectors) for
  destinations that have a full rig; empty for destinations that don't.
- **gate** — the Kidney's decision. This is what makes a character *refuse*
  authentically ("my no is a complete sentence") rather than always comply.

---

## 3. The lifecycle (what the mind does, not what the renderer does)

1. **Stimulus** — an event enters (voice, a poke, a gaze, a scheduled cue).
2. **Affect update** — Cortex/Ternary/T thyroid adjust valence/arousal/energy.
3. **Intent** — the mind selects a motion verb + meaning (semantic grounding).
4. **Identity gate** — the Kidney decides suppress/soft/full; may reject.
5. **Emit** — a `CharacterReaction` frame goes out on the seam.

The renderer's only job: *consume the frame and realize it in its medium.*
A MuJoCo body turns `motion.verb` into torques; a WebXR scene turns it into a
camera-relative transform; a neural-asset renderer turns it into a clip.

---

## 4. Rejection → presence (the part that makes it alive)

Refusals are never silent. The `gate.rejection` carries the 12-code taxonomy
from `seam-interface-spec.md` (`SAFE_LIMIT`, `IDENTITY_MACHINE_NO`,
`IDENTITY_LOCKED`, …). A renderer that honors rejection renders the *refusal*
as presence — the character stiffens, turns away, says no — instead of
happily complying.

This is the single most differentiating behavior vs. a dumb reference-to-video
tool: **our characters have a boundary, and the boundary is visible.**

---

## 5. The lab (AR first)

Phase 1 — **WebXR + three.js** (runs in a phone browser, no app-store wait):

- A camera feed + a rigged 3D character (we already have three.js experience:
  `orbital-shipyard.html`, the `digital_world` adapter).
- The mind runs *locally* (we already have Mort_II/qwen on Ollama), emits
  `CharacterReaction` frames over the existing seam (the organs we built tonight).
- A thin `ar` adapter consumes the frame → moves the rigged character in the
  camera view, gated by the Kidney.

Phase 2 — plug the *same* frames into a neural-asset renderer when one with an
API lands (or build our own on an open image/video model).

Phase 3 — the *same* frames drive the physical humanoid (AX-169F / HopeJR),
unchanged.

The point: we write the mind **once**, and the lab is where we prove it reacts
correctly — long before a servo exists.

---

## 6. What already exists (build on it, don't rebuild)

| Piece | Status | Where |
|---|---|---|
| Presence Engine (affect → expression) | ✅ built + tested | `presence_engine.py` |
| Motion Verb Layer (validate/reject) | ✅ built + tested | `motion_verb_layer.py` |
| Kidney (identity gate / expression) | ✅ built + tested | `kidney_expression.py` |
| Body Schema (proprioception) | ✅ built + tested | `body_schema_anatomy.py` |
| Semantic grounding (meaning of motion) | ✅ built | `dispatch/motion_semantics.py` |
| Seam integration (the full loop) | ✅ built + tested | `seam_integration.py` |
| Character identities (assignable personalities) | ✅ data | `characters/*/SOUL.md` etc. |

**Missing (the actual next build):** the `CharacterReaction` emitter + one
`ar` adapter. That's it — the mind side is done.

---

*This is the document that makes "look at this news" into "we already built the hard half."*
