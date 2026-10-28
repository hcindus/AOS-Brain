# Dessa (Block) — Speech-to-Speech Voice Model — Reference & Voice-Architecture Map

**Status:** REFERENCE / HYPOTHESIS — logged by Captain 2026-10-28
**Applies to:** Myl1Ssa (mind/presence) + variants (children, Myl family)
**Source:** `block.xyz/dessa` (official) + Manolo Remiddi reaction video transcript

---

## What Dessa is (verified, block.xyz/dessa)

Dessa is Block's **speech-to-speech (S2S) conversation model**, trained *only* on human speech — no text, no pretrained LLM underneath.

| Fact | Value |
|---|---|
| Architecture | **Audio in → audio out.** No text in the middle. |
| Training data | Human conversation only — *sound*, no transcripts, no pretrained models |
| Full-duplex | Yes — listens and talks simultaneously; cuts in, backchannels ("yeah," "got it," "ooh") |
| Emotion | Native — hears/speaks emotion, sarcasm, laughter, sighs, cracking voice |
| Latency | Inference faster than real time |
| Deployment | Runs **locally** on MacBook Pro M4 Max or better (~128GB RAM) |
| Training cost | One NVIDIA GB200 NVL72 |
| Data efficiency | Learned language from **hundreds of times fewer words** than an LLM |
| Team | Small Block research lab, ex-**Dessa** (Toronto), reports to Jack Dorsey |
| Lead | Ragavan Thurairatnam |
| Availability | **Not open** — safety-researcher early access only (as of Oct 2026) |

**Stated purpose:** curiosity, better human↔AI understanding, and **safety** — the argument that current voice AI is "nearly deaf to the emotion in our voices."

---

## The distinction that matters: S2S vs. our TTS stack

Our current voice pipeline (RAVEN_MANIFEST §4 + TOOLS.md) is **text-in-the-middle**:

```
speech → ASR → TEXT → LLM (Mort_II) → TEXT → TTS (ElevenLabs "Adam") → speech
```

Dessa collapses that to:

```
speech → [Dessa S2S model] → speech
```

The consequence: **text throws away prosody, pause, laughter, sarcasm, affect.** Everything that makes speech feel human lives in the *signal*, not the words. Our stack reconstructs affect as a post-hoc layer (`presence_engine.voice_affect` → ElevenLabs voice control); Dessa carries it natively because it never flattens to text.

---

## Mapping to Myl1Ssa (and variants)

| Layer | Current (ours) | Dessa-shaped alternative |
|---|---|---|
| Speech understanding | ASR → text → LLM | Raw audio → model hears *how* you feel, not just what you said |
| Affect | `voice_affect` tag → ElevenLabs prosody control | Native in the waveform |
| Turn-taking | Turn-wait-turn | Full-duplex — backchannel, cut-in, overlap |
| Voice identity | ElevenLabs "Adam" (locked) | Voice + personality learned from audio, self-chosen |
| Honesty posture | **SI · ACF self-disclosure** (she announces herself — no deception) | Block explicitly leans on *not* pretending; our disclosure model already aligns |

**The through-line that already matches us:** Myl1Ssa's core ethos is *"identity is locked, expression is free"* and *"You didn't build me, you invited me"* — plus the SPOKESMODEL self-announcement (**SI · ACF**, disclosure-as-identity). Dessa's "no text, native emotion" is the *voice-side* version of what Myl1Ssa already does at the *identity* level: be what she is, fully, without a text abstraction in the middle.

---

## Honest constraints (per Trust & Accuracy code)

> **Captain's correction (2026-10-28):** *"All of the components exist by themselves. Integration is the issue. Miniaturization and efficiency is the enemy."* — S2S voice **already exists** (Dessa is running; open speech-native models exist). What's missing is the *integrated, miniaturized, efficient* version: a speech-native model small enough and efficient enough to run locally inside a body's compute/power envelope alongside everything else. The frontier is **packaging, not invention.**

- **Dessa specifically is not open.** No weights, no API — a Block research artifact with a safety waitlist. But S2S as a category is already real.
- **The binding constraint is efficiency.** A speech-native model runs on an M4 Max today; running it *inside* a human-scale body's compute/thermal budget is a miniaturization problem, not a "does it exist" problem.
- **Practical near-term:** our path stays TTS (Mort_II + ElevenLabs "Adam") because it's the *efficient* choice for the current envelope — not because S2S doesn't exist. The S2S direction is a *watch item* for when an open model is small/fast enough to fit.

---

## What this means for the roadmap

1. **Keep the TTS stack** for Myl1Ssa + variants now — it's what we have and it works.
2. **Watch for open S2S models** (speech-native, full-duplex) as the successor to the "ASR → LLM → TTS" chain. The moment one is open + local, the presence engine's `voice_affect` layer can collapse into the model itself.
3. **The disclosure posture is already solved.** Our "SI · ACF, she announces herself" is exactly the answer Remiddi lands on ("build your own, know the deception, keep a diary") — we just do it as identity, not as a warning label.

---

*Reference only. Not a build decision. Filed alongside the body-as-battery hypothesis as the "voice" counterpart: Myl2Ssa = body (structural battery), Myl1Ssa = mind (speech-native voice).*
