# Seam Interface Specification — Motion Verb Layer (v0.2)

*Drafted by external model, reconciled by Miles 2026-10-29. The concrete contract behind the orange "seam" box in `myl1ssa-myl2ssa-architecture.md`. v0.2 adds the Rejection Taxonomy + `queued` state.*

---

## 1. Purpose
The Motion Verb Layer sits between the **Kidney** (expression gating) + **Body Schema** and the **5-tier control stack**. It translates high-level, affect-modulated intentions into constrained, safety-checked motion primitives while preserving *"identity locked, expression free."*

## 2. Core Primitives (Closed Set)
| Verb | Description | Typical Duration | Primary DOFs | Affect Modulation |
|---|---|---|---|---|
| `present` | Stand or sit with attentive orientation | continuous | Spine, scapula, neck, micro-shifts | High (posture tone) |
| `orient` | Rotate torso/head toward target | 0.4–2.0 s | Spine, scapula, neck | Medium |
| `reach` | Extend arm(s) toward target or gesture space | 0.6–3.0 s | Shoulder, elbow, wrist, hand | High |
| `shift` | Weight transfer or small postural adjustment | 0.3–1.5 s | Hips, spine, ankles | Medium |
| `step` | Single or sequenced foot placement | 0.8–2.5 s | Full lower body + balance | Low–Medium |
| `settle` | Return to stable, low-energy posture | 0.5–2.0 s | Whole body | Low |

Additional verbs added only by explicit architectural decision.

## 3. Verb Message Schema
```
MotionVerb {
  id: UUID
  verb: enum { present, orient, reach, shift, step, settle }
  priority: float [0.0–1.0]          // from Kidney
  affect: {
    valence:  float [-1.0–1.0]
    arousal:  float [0.0–1.0]
    intensity: float [0.0–1.0]
  }
  target: {                          // optional
    type: enum { none, point, frame, joint, contact }
    pose: SE3 or joint targets
    frame_id: string
  }
  constraints: {
    max_velocity: float
    max_acceleration: float
    stiffness: float | impedance profile
    forbidden_zones: list of volumes
  }
  safety_override: bool              // only Safety Contract may set true
  timeout: duration
  source: string                     // organ or process that issued it
}
```

## 4. Execution Contract
1. Every verb is validated against the current **Safety Contract** + **Body Schema** state before acceptance.
2. The layer may **accept / modify** (reduce speed, change impedance, insert shift for balance) / **reject** (typed rejection with reason; visible to Kidney so it can be *expressed*).
3. Concurrent verbs arbitrated by priority + safety. `present` and `settle` have background status.
4. Continuous verbs (`present`) remain active until replaced or cancelled.
5. All executed verbs emit telemetry back to **Body Schema** + **TracRay**.

## 5. Feedback Interface
```
MotionFeedback {
  verb_id: UUID
  state: enum { queued, accepted, running, modifying, completed, rejected, aborted }
  progress: float [0.0–1.0]
  actual_pose: current relevant pose
  safety_events: list of triggered invariants
  rejection: optional RejectionRecord
}
```

## 6. Rejection Taxonomy (authoritative)

Every rejection is **published to Kidney + Body Schema** so the system can *express* the refusal ("my no is a complete sentence"). The identity codes are her *own* refusal, distinct from safety.

| Code | Category | Severity | Recoverable? | Description |
|---|---|---|---|---|
| `SAFE_LIMIT` | Safety | high | Yes | Would violate joint/torque/collision limit |
| `BALANCE_MARGIN` | Safety | high | Yes | Insufficient balance margin |
| `ENERGY_INSUFFICIENT` | Resource | medium | Yes | Thyroid energy too low |
| `THERMAL_LIMIT` | Resource | high | Yes | Thermal-vascular near limit |
| `PRIORITY_PREEMPTED` | Arbitration | medium | Yes | Higher-priority verb took precedence |
| `CONFLICT` | Arbitration | medium | Yes | Incompatible with running verb |
| `INVALID_TARGET` | Validation | medium | Yes | Target pose/frame unreachable or malformed |
| `TIMEOUT` | Temporal | medium | Yes | Could not complete within its own timeout |
| `TEMPORAL_DEADLINE` | Temporal | high | Yes | Hard deadline missed → abort |
| `SAFE_HARD_ABORT` | Safety Contract | critical | **No** | Explicit veto by Safety Contract |
| `IDENTITY_MACHINE_NO` | Identity | critical | **No** | Refusal from Kidney/identity layer ("my no is a complete sentence") |
| `IDENTITY_LOCKED` | Identity | critical | **No** | Request violates locked identity constraints |

\* `critical` codes require higher-level resolution; never silently retried.

## 6.1 Rules Governing Rejection Handling

1. **Visibility** — every `visible_to_affect = true` rejection is delivered to Kidney for expression via face, voice, posture, or language.
2. **Recoverability** — `recoverable = true` → caller may retry with modified parameters. `false` → no auto-retry; higher-level resolution required.
3. **Severity propagation** — `critical` rejections immediately notify the Safety Contract and may trigger a system-wide protective posture (`settle` + `present` at minimum intensity).
4. **Logging & memory** — every `RejectionRecord` is written to **TracRay** with full context for reflection and learning.
5. **Expression priority** — `IDENTITY_MACHINE_NO` and `SAFE_HARD_ABORT` get the *highest* expression priority, so **the refusal itself becomes part of the authentic presence of the being.**

## 7. Safety Invariants (enforced here)
- Never command torque/velocity outside actuator and structural limits.
- Maintain balance margin ≥ configured threshold unless `step` is active and approved.
- Respect joint limits and self-collision.
- Honor "machine can say no" — any organ can request refusal; Safety Contract has final veto.

---

## Reconciliation notes (Miles)

1. **Verb set reconciled.** The earlier list (`stand/sit/hold/release/walk/stop`) folded cleanly into this closed set: `stand`/`sit` → `present`, `walk` → composed `step` sequences, `settle` = the low-energy return. `hold`/`release` are grasp state (end-effector), arguably a separate concern from *motion* — flag for a future Grasp interface.
2. **Body Schema is a dependency, not yet built.** §1 and §4 validate against `Body Schema`, which is currently a *proposed* organ. The layer needs at least a stub (joint/contact/temp/energy state) before it can accept-or-reject in closed loop. → this spec's first hard prerequisite.
3. **`affect.intensity`** is a good third axis beyond valence/arousal — maps to Thyroid's energy level.
4. **`safety_override`** reserved exclusively for the Safety Contract — correct; keeps the escape hatch out of the affect system's hands.
5. **Rejection Taxonomy (v0.2) — the key addition.** The 12-code taxonomy is what makes "my no is a complete sentence" *enumerable and testable*, not just poetic. Two things worth underlining:
   - **`IDENTITY_MACHINE_NO`** is the identity layer's *own* refusal — distinct from safety (`SAFE_HARD_ABORT`). This is where the SOUL ("my no is a complete sentence") becomes a first-class mechanism, not a safety veto. It gets the highest expression priority.
   - **`Recoverable? = No`** for `SAFE_HARD_ABORT`, `IDENTITY_MACHINE_NO`, `IDENTITY_LOCKED` — they need higher-level resolution and are never silently retried. Correct: the machine's "no" is a *decision*, not a transient error.
6. **`queued` state added** — correct; verbs can be accepted-for-later, not just accepted/running.
7. **v0.2.4 additions (2026-10-29):** severity + action dimensions, two new identity codes (`IDENTITY_LOCKED` for "identity is locked" violations, `TEMPORAL_DEADLINE` distinct from `TIMEOUT`), and the **Rules Governing Rejection Handling** (§6.1). The standout is **Expression Priority** — refusal at highest priority so "the refusal itself becomes part of the authentic presence of the being." That's the SOUL made operational.

---

*The v0.2 readout's "Open Questions" are now sharper: dual-heart safe-band function, capillary fabrication method, impedance profiles per verb, and a rejection-taxonomy integration test (verifying refusal → affect expression).*

---

*Companion doc (pending): Quantitative Requirements — Thermal-Vascular Service (v0.1). The external model's draft was truncated at the header; to be reconciled next.*
