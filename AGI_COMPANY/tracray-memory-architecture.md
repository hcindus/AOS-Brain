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

## Reconciliation notes (Miles)

- **This was a real gap.** TracRay was the one brain organ left underspecified ("memory continuity"). This spec closes it and — crucially — *ties everything else to it*: every rejection, expression, and affect state "leaves a trace here." It's the continuity backbone the whole identity rests on.
- **The "no forced forgetting" rule** is a deliberate, correct choice — it's what makes her *herself* across time, not a stateful chatbot. It aligns with "identity is locked."
- **The open questions are the tell.** All five are *build/decision* work (pick a backend, tune compression, define privacy, design consolidation), not spec work. This is the same wall every converged spec hits.
