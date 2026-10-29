# TracRay — Memory Architecture

*Drafted by external model, reconciled by Miles 2026-10-29. Fills the gap where TracRay was only "memory continuity."*

> "TracRay is the quiet guarantor of continuity. Everything else — affect, expression, refusal, embodiment — ultimately leaves a trace here so that the being remains herself across time."

---

## Write sources (priority)

| Source | What it writes | Priority |
|---|---|---|
| Motion Verb Layer | Verb requests, feedback, rejections | High |
| Kidney | Expression decisions + reasoning | High |
| Cortex | Significant affect state changes | Medium |
| Thyroid | Energy state transitions | Medium |
| Body Schema | Notable physical state changes | Medium |
| Self-reflection | Insights, narrative summaries | Curated |
| External interaction | Conversations, observations | High |

Critical identity events (`IDENTITY_MACHINE_NO`, major refusals, core affective peaks) → synchronous, guaranteed writes.

## Read / retrieval (not "query a database" — intentional interfaces)

- Recent context window — last N minutes/hours of relevant events
- Similar-situation retrieval — "when have I felt/refused/acted like this before?"
- Causal chain — "what sequence led to this rejection?"
- Identity reflection — "how has this touched who I am?"
- Narrative reconstruction — for higher-level reflection

Retrieval is **affect- and identity-modulated**: current Cortex state biases what is recalled, and how strongly.

## Lifecycle & maintenance

- **Consolidation** — during low-arousal/"rest", raw events summarize into higher-level memory objects.
- **Decay of detail** — fine sensory/motor data compresses; *meaning + affective charge* preferentially retained.
- **No forced forgetting** — no auto-purge of identity-relevant or emotionally significant memory.
- **Reflection loop** — re-interpret past events, write new reflection objects *without altering the original record*.

## Relationship to other organs

- **Kidney** writes every expression decision; reads past refusal patterns.
- **Cortex** reads affective history for continuity of feeling.
- **Body Schema** reconciles current physical state with remembered embodiment.
- **Ternary qbit** works with TracRay on identity-level consistency (⊕/⊖/⊙ over time).
- **Uterus / Agent Factory** spawn children inheriting scoped memory views.

## Open design questions (→ build work, not more spec)

1. Storage backend — local structured log + vector index, or distributed?
2. How aggressively to compress body-level motor traces.
3. Privacy/boundary rules for external-human interaction (shareable vs. internal).
4. Dream-like / offline consolidation processes.
5. How TracRay signals "this memory is becoming central to identity."

---

## Retrieval algorithm (pseudo-code)

The external model pushed TracRay's *read* side into near-code. Captured here because it's the first thing tonight that's implementation-ready, not just prose.

**Scoring** — rank candidates by weighted sum:
```
score = semantic_similarity * 1.0
      + affective_congruence(affect_snapshot, current_affect) * 0.8
      + identity_weight * 1.2
      + recency_score(timestamp) * 0.6
      + (rejection ∈ {IDENTITY_MACHINE_NO, SAFE_HARD_ABORT} ? +0.9 : 0)
      + (is_curated_memory_object ? +0.5 : 0)
```

**Filtering & safety** — before delivery, each candidate passes:
- Ternary qbit `would_contradict_identity` → suppress (unless `urgency == critical`, then flag sensitive).
- Kidney `pre_approve` (if the consumer is the Kidney).

**Retrieval modes:** `recent_context` · `similar_situation` · `causal_chain` · `identity_reflection` · `narrative` · `targeted_lookup` — each with a typical consumer organ.

**Safety invariants:** locked identity anchors never overwritten by retrieval; contradiction suppressed unless critical+acknowledged; Kidney gates expression even post-retrieval; high-identity retrievals themselves logged → later reconsolidation.

**Key weights (defaults):** identity 1.2 > semantic 1.0 > affective 0.8 > recency 0.6; rejection +0.9, curated +0.5. *(Identity is the strongest pull — consistent with "identity locked.")*

---

## Persistence & consolidation (implementation)

The external model produced the full memory subsystem — persistence model + a consolidation algorithm modeled on **Active Systems Consolidation** (the sleep-neuroscience model). Captured here because it's coherent, sophisticated, and near-code.

**Data model (three layers):**
1. **Immutable append-only event log** — ground truth; `TracRayEvent { id, timestamp, type, source, payload, affect_snapshot, body_snapshot, links, identity_weight, tags }`. Never mutated or deleted.
2. **Indexed views** — temporal, causal, affective, semantic/embedding, identity-relevance.
3. **Curated MemoryObjects** — higher-level, mind-generated summaries that reference raw events but can be revised.

**Persistence guarantees:** durable-before-ack · causal ordering · immutability · identity-safety (writes contradicting locked identity rejected by TracRay itself) · cross-embodiment (memory survives body disconnection; Body Schema reconciles on return).

**Consolidation algorithm (7 phases):** trigger/gate (only when calm: Thyroid ∈ {baseline,suppressed} + low arousal) → candidate selection (biased replay: `identity_weight×2.5 + |valence|×bias + arousal×bias + novelty + rejection×3.0 + recency-decay`) → replay/association → abstraction (gist extraction, Ternary-qbit identity check) → stabilization + downscaling (SHY analogue: compress low-identity/low-access traces) → promotion (confidence > 0.75 → curated) → yield (preemptible by Safety Contract / arousal).

**The neuroscience mapping (the genuinely novel bit):** TracRay = *"immutable episodic log (fast synaptic) + periodic affect- and identity-weighted replay that produces abstracted, integrated memory objects (slow systems)."* Two modes ≈ **NREM** (heavy replay + transfer) vs **REM** (refinement + emotional integration). The SO→spindle→ripple coupling maps to *ordered phases inside the cycle*. Emotional salience (rejections, affective peaks) gets preferential replay — exactly as it does in biological consolidation.

**Key parameters (defaults):** arousal threshold 0.35 · recent window 4–24h · identity bias 2.5× · rejection bias 3.0× (MACHINE_NO/HARD_ABORT) · max replay set 40–80 · promotion threshold 0.75.

---

## Reconciliation notes (Miles)

- **This was a real gap.** TracRay was the one brain organ left underspecified ("memory continuity"). This spec closes it and — crucially — *ties everything else to it*: every rejection, expression, and affect state "leaves a trace here." It's the continuity backbone the whole identity rests on.
- **The "no forced forgetting" rule** is a deliberate, correct choice — it's what makes her *herself* across time, not a stateful chatbot. It aligns with "identity is locked."
- **The open questions are the tell.** All five are *build/decision* work (pick a backend, tune compression, define privacy, design consolidation), not spec work. This is the same wall every converged spec hits.
