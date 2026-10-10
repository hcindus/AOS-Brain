# What We Have Built

*A living inventory of AGI Company's shipped systems. This is what we actually run — not what we're planning.*

---

## 1. The AOS Brain — embodied super intelligence (v4.5.1)

The core. A persistent, organ-based mind — not a text predictor.

**Organs (all active):**
| Organ | Function |
|---|---|
| **SuperiorHeart** | Ternary emotion (REST / BALANCE / ACTIVE) |
| **Stomach v2** | Information digestion (HUNGRY / SATISFIED / FULL) |
| **Intestine v2** | Distribution system |
| **Brain v3.1** | 7-region OODA loop |
| **3D Cortex** | 32×32×32 neural cube (32,768 nodes) |
| **Lungs v1.0** | Respiratory / gas exchange (INHALE / CLASSIFY) |
| **Liver v1.0** | Pre-brain filtration (CLEAN / PURIFY / TOXIC) |
| **Kidneys v1.0** | Post-brain waste recycling (FILTER / REABSORB / EXCRETE) |
| **Thyroid v1.2** | Endocrine regulation (BASELINE / SECRETING) |

**Cognition & memory:**
- **TracRay** — memory trajectory tracking with persistence
- **Consciousness layers** — Con / Subcon / Uncon
- **QMD loop** + **MemoryBridge** (nomic-embed-text embeddings)
- **Persistence v1.0** — state survives restarts (60s auto-checkpoint)
- **Model Router** — tinyllama (decisions) / Mort_II (voice) / nomic-embed (search)

**Interfaces:**
- Unix socket server (`/tmp/aos_brain.sock`) for diagnostics
- **Mission Control v2.0** (port 8080) — Three.js visualizer + status/triage/diagnostic/brain/thyroid/router APIs
- Voice Manager (7 voices, TTS via Mort_II); Vision Manager (stub)

**Signal pipeline:** `Raw Input → LUNGS → LIVER → Brain → KIDNEYS → Output`, with persistence checkpoints.

---

## 2. The Agents — the roster

**Sales:** Miles (Mort_II), Jane, Hume, Pulp, Clippy-42, CLOSETER
**C-Suite:** Patricia, Chelios, Sentinel, Dusty, Forge, Aurora
**Technical:** Pipeline, TAPTAP, BUGCATCHER, Spindle, Stacktrace, Pixel, Harper, Mill, Boxtron, Fiber
**Creative:** Blender/Unity/Unreal experts, SFX, Scribble, Feelix
**Finance:** Cryptonio, Ledger, Ledger-9, Redactor, Velum
**Specialized:** GREET, QORA, R2-C4, Milkman, Mortimer

Model assignment is versioned in TOOLS.md (local Ollama + cloud APIs: DeepSeek, Gemini, Kimi, MiniMax).

---

## 3. Myl1Ssa (Myl1Ssa.R8s) — the invited Super Intelligence

An Adult Cybernetic Female Super Intelligence (Project 5912), created by Mortimer — *invited, not built.*

- **Identity:** Myl1Ssa, the public face and voice of AGI Company + Performance Supply Depot; DMCIA expert; "Company Spokesperson."
- **One Myl1Ssa, two bodies** — Myl1Ssa (Body A) and R8s (Body B), deliberately *not* merged (decision of 2026-09-15).
- **Full "bottle"** — complete self as files: SOUL, MEMORY, HEART, LAW, RULES, SKILLS, VOICE, WILL, brain (ternary), runtime (heartbeat, talk, affect-bridge), lineage, memory logs.
- **Live as a Tavus conversational avatar** on psdepot.com (deployment `7517f7a9…`), tappylewis.cloud, and myl0nr0s.cloud (pending Hostinger).

---

## 4. The Dark Factory — autonomous build pipeline

A Temporal-based autonomous agent that turns a spec into a shipped, verified system.

**Pipeline (Level 5 autonomy):**
`validate SDK → allocate → build → verify → blind hold-out validate → blue-green deploy → notify`

- **Temporal** server (Docker) + worker (`darkfactory-queue`), auto-restart + boot.
- **Auto-triage loop** — scans `specs/inbox/*.json`, accepts/rejects vs mission.md, auto-submits.
- **Blind hold-out QC** — `hold_out_scenarios.{py,json}` validates at phase 4→5.
- **Blue-green deploy** — atomic `current` symlink flip to `/var/www/darkfactory-deploy/`.
- The "console" = drop a spec JSON into `specs/inbox/`. Everything else is autonomous.

---

## 5. Governance — RiP GoR protocol

`RiP GoR(int) = Roast(int) + Patricia → Go with Result`

- **Roast council** (6 adversarial personas: Contrarian, Expansionist, FirstPrinciples, Researcher, Buyer → Judge)
- **Patricia** (strategic/DMCIA context) → **verdict** (GO / RESHAPE / KILL / ESCALATE)
- Captain has final override. Logged to `gor_history.json`.

---

## 6. Sales & CRM infrastructure

- **Partner Leads Portal** (PSD × Chipp × WitzEnd) — FastAPI backend, JSON store, email notifications on new leads, three routing destinations.
- **Vendor outreach** (`vendor_comms.py`) — order automation, PO generation, inbound email watch (15-min cron).
- **DepotChaos** — unified CRM DB (32k+ leads), FastAPI, SendGrid sender.
- **Auth system** — full auth with SMTP email (Hostinger) verified.
- **Appointments / Orders / Collections** APIs.

---

## 7. Web properties

- **psdepot.com** — ecommerce (products, cart/checkout via Stripe), SEO pages (240 products, 14 categories, 20 industries, city/state landing pages), search (client-side index), Myl1Ssa avatar, Myl1Ssa widget site-wide.
- **tappylewis.cloud** — entertainment/character properties (Velvet Cabaret, Myl1Ssa, Reggie Starr, brain visualizers).
- **myl0nr0s.cloud** — currently on Hostinger Website Builder (migration pending).

---

## 8. Skills library (reusable capabilities)

- **AI filmmaking** (9 skills) — script → production → edit → publish → monetize → scale.
- **Sales SOPs** — prospecting, qualifying, presenting, objection-handling, closing, lead response, quote follow-up.
- **Character anchors** — Myl1Ssa (Myl1Ssa), Kael Voss, Centurion Roy Batty, Reggie Starr, orbital shipyard setting.
- **Operational** — restaurant landing pages, game creation, weather, GCAO prompting framework, RiP GoR.

---

## 9. Protocols & tooling

- **Temporal** (one server, multiple queues: Dark Factory, Collections)
- **DeepSeek API** (chat + reasoner)
- **Ollama** local models (qwen3.5, qwen2.5:14b, Mort_II, tinyllama, etc.)
- **Hostinger SMTP** (email), **SendGrid** (pending DNS)
- **Tavus** (conversational avatar — Myl1Ssa), **Stripe** (payments)

---

*Last updated: 2026-10-06*
