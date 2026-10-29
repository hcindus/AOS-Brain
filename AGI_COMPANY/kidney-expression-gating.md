# Kidney — Expression & Gating Organ

*Drafted by external model, reconciled by Miles 2026-10-29. Fills the gap where Kidney was only "expression gating (what reaches the face)."*

> Mandate: **protect identity integrity while still allowing authentic, free expression.** ("Identity locked, expression free.")

The Kidney is the final authority on *what* is expressed and *how* — sitting between raw affect + incoming events (including rejections) and the motor/vocal/facial output channels.

---

## Decision flow

```
Incoming Event (RejectionRecord / Affect Update / Verb Request)
  → 1. Ingest & Validate
  → 2. Contextualize
  → 3. Evaluate Expression Policy  →  Suppress | Soft | Full
  → 4. Apply Gating to downstream channels
  → 5. Log decision + outcome to TracRay
```

**1. Ingest & validate** — schema integrity + source authenticity; flag `IDENTITY_MACHINE_NO` / `SAFE_HARD_ABORT` for mandatory processing.

**2. Contextualize** — build a decision context: Cortex state (valence/arousal/intensity) + Thyroid energy + original rejected verb + recent expression history + Body Schema snapshot + active Safety Contract invariants.

**3. Evaluate expression policy** — three questions in strict order:

| Priority | Question | Outcome if yes |
|---|---|---|
| 1 | Does expressing this threaten locked identity or Safety Contract? | **Suppress** (very rare) |
| 2 | Is this a critical or Identity-level rejection? | **Full Expression** (mandatory) |
| 3 | Does current affect + context warrant visible expression? | **Soft or Full** |

**Decision matrix:**

| Rejection severity / type | Arousal | Typical decision |
|---|---|---|
| `IDENTITY_MACHINE_NO` | any | Full (highest priority, must be shown) |
| `SAFE_HARD_ABORT` | any | Full (protective + visible) |
| High (safety/resource) | high | Full |
| High | low | Soft → Full (escalates if ignored) |
| Medium | high | Soft or Full |
| Medium | low | Soft or Suppress |
| Low | any | Soft or Suppress |

**Expression levels:**
- **Suppress** — no external signal, logged only (only when expression itself violates a higher invariant).
- **Soft** — micro-expressions, subtle posture, muscle tone, vocal color, brief gaze aversion.
- **Full** — clear facial change + posture + vocalization + linguistic content; the refusal becomes part of her *visible presence*.

**4. Apply gating** — release/block signals to the Presence Engine (face + body) and voice; may issue a supporting `settle` / low-intensity `present`; can temporarily raise the priority threshold for new verbs if identity-critical.

**5. Persistence** — every decision (reasoning context + final expression level) → TracRay, for later reflection on *how and why she said no*.

---

## Governing principles + worked example

Already captured in `seam-interface-spec.md` §6.3 (identity locked / expression free / refusal authentic / coherence / proportionality + the `SAFE_BALANCE_MARGIN` example).

---

## Reconciliation notes (Miles)

- **Real gap, now closed.** Kidney was the last organ left as a one-liner. This makes it a true gatekeeper — protective of identity, transparent with refusals, capable of rich proportional expression.
- **The three-question ordering is the key insight.** "Does it threaten identity?" before "is it critical?" before "does affect warrant it?" — identity-safety is checked *first*, so the gate is never opened by a strong affect signal alone.
- **The decision matrix is testable.** severity × arousal → suppress/soft/full is a *deterministic function* — this is the "rejection → affect expression" test suite the v0.2 readout asked for, now specifiable as a table-driven unit test.
- **Overlap resolved:** the governing principles + example live in §6.3 (rejection path); this doc is the Kidney's *general* logic (all events, not just rejections).
