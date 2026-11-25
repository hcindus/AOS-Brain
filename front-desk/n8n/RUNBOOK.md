# Frontline Receptionist — Voice (n8n × Twilio × Frontline SOA)

**Corrected runbook** · prepared by Miles · 2026-11-25

Two n8n workflows act as the Twilio "front door" to the Frontline SOA gateway. They
turn an inbound phone call into: a greeting, an agent-routed conversational turn, or a
voicemail/recording that lands as tasks + notes + a CRM contact.

- `frontline-receptionist-voice-soa.json` — **single-phase** (`id: fL1nR3c3pt10nV01`)
- `frontline-receptionist-voice-two-phase-soa.json` — **two-phase** (`id: fL1n2Ph4s3RcpV02`)

---

## 1 · The one decision that matters: single-phase vs two-phase

Twilio drops a voice webhook that does not answer within **~15 seconds**. A Frontline
agent turn on CPU takes **~28 seconds**. That single fact decides which workflow is
safe to run live.

| | Single-phase | Two-phase |
|---|---|---|
| Turn latency budget | must finish **< 15s** | caller hears ~2s hold, answer streams in |
| Where the reply is built | synchronously, in the webhook response | background, written to gateway `/session/<sid>` |
| Call history location | n8n static data (volatile) | gateway session store (durable) |
| Extra round-trips | none | 3–4 per turn (reset / load / store / poll) |
| Survives a 28s CPU turn | ❌ drops the call | ✅ holds + polls |
| Verdict | **dev / demo only** | **the live design** |

**Correction #1 (the critical one):** do **not** activate the single-phase workflow for
real traffic. It will drop every call whose agent turn exceeds ~15s. The two-phase
workflow exists precisely to solve this. If the agent turns end up <15s in practice
(GPU, cached, short replies), single-phase is simpler — but that is a latency
assumption you must prove, not assume.

---

## 2 · Gateway contract the workflows expect (the spec)

Every model call in both workflows goes to the **Frontline gateway**, never to a model
directly. n8n is only Twilio-in / TwiML-out + call state. The gateway owns the skills,
the business profile, tools, and memory.

| Method | Path | Body → Response |
|---|---|---|
| `GET` | `/questionnaire` | → `{ "profile": { business_name, hours, days_open, … } }` |
| `POST` | `/soa/agent/<agent>` | `{ input, caller_id, channel, agent, context, history }` → `{ reply, ok, mode, error }` |
| `GET` | `/session/<callSid>` | → `{ "session": { reply, history, agent, forward, forward_to } }` |
| `POST` | `/session/<callSid>` | `{ reply, history, agent, from, forward, … }` (patch) → `{ ok }` |
| `POST` | `/tool/task_add` | `{ title, due, priority }` |
| `POST` | `/tool/note_add` | `{ text, topic }` |
| `POST` | `/directory` | `{ name, channel, address, preferred, meta }` |
| `GET` | `/admin` | admin UI (referenced in sticky notes, not called by nodes) |

**Default gateway base URL:** `http://127.0.0.1:8800` (override with `FRONTLINE_URL`).

> ⚠️ **Open question — this contract does not match what is currently deployed.**
> The live receptionist scaffold (`front-desk/server.py`, port **8120**) exposes a
> different, simpler surface: `POST /api/inbound` (one-shot classify → store → alert),
> `POST /api/classify`, `GET /api/inbound`, `GET /api/stats`, `GET /api/suites`,
> `GET /health`, and `GET /questionnaire` returns an **HTML form**, not JSON. None of
> `/soa/agent/*`, `/session/*`, `/tool/*`, `/directory`, or `/admin` exist there, and
> nothing is listening on 8800. These workflows target the *next* gateway build — which
> is the thing to confirm before these can run end-to-end.

---

## 3 · Corrections required before activation

**#2 — CRM endpoint inconsistency.** Both `Add Caller to CRM` nodes `POST` to
`/directory`, but the single-phase sticky note documents CRM as `/tool/contact_add`.
One is wrong. Confirm which route the gateway actually exposes and make the node match.

**#3 — No webhook authentication.** Neither workflow validates the Twilio signature
(`X-Twilio-Signature`). Anyone who discovers the public URL can `POST` forged call
payloads and inject tasks / notes / CRM entries into the gateway. Add Twilio signature
verification (or a shared secret header check) in a code node right after `Read Call`.

**#4 — `/questionnaire` shape.** `Build Greeting` reads `$('Load Profile (greeting)').first().json.profile`.
If the gateway returns HTML (as `front-desk` does today), this is `undefined` and every
greeting falls back to "our office" defaults. The gateway must return JSON `{ profile }`.

**#5 — Fragile cross-node reads.** `Save Turn` / `Prepare Session` / `Build Reply` reach
back with `$('Read Call').first().json` and `$('Pick Agent').first().json`. This is
correct n8n, but it breaks silently if a node is renamed. Keep those names stable (they
are a contract), or switch to passing values forward explicitly.

**#6 — Single-phase history is volatile.** `$getWorkflowStaticData('global')` is lost on
n8n restart and is not shared across instances / workers. Fine for a demo; use the
two-phase gateway `/session` store for anything production.

---

## 4 · Environment variables (on the n8n host)

| Var | Meaning | Default |
|---|---|---|
| `FRONTLINE_PUBLIC_URL` | public URL of this n8n, no trailing slash (ngrok / tunnel / domain) | — (required) |
| `FRONTLINE_URL` | gateway base URL | `http://127.0.0.1:8800` |
| `FRONTLINE_FORWARD_TO` | transfer number; empty = never transfer | — |
| `FRONTLINE_TZ` | timezone for open/closed hours | `America/Los_Angeles` |
| `FRONTLINE_VOICE` | Twilio `<Say>` voice | `Polly.Joanna-Neural` |

Also set `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` (n8n 2.x blocks `$env` by default).

---

## 5 · Twilio console + activation

- **Voice URL** (single-phase): `{FRONTLINE_PUBLIC_URL}/webhook/frontline-receptionist`
- **Voice URL** (two-phase): `{FRONTLINE_PUBLIC_URL}/webhook/frontline-voice-2p`
- The transcript callback (`transcribeCallback`) points at the same path; the
  `Is Transcript Callback?` node tells the two payload shapes apart.
- Activate **one** workflow only. The two-phase workflow is shipped `inactive` on
  purpose — flip it on only after deactivating single-phase or re-pointing Twilio.

**No secrets** live in these files — no tokens, numbers, or ngrok hosts.

---

## 6 · What I still need from you

1. The **real gateway contract** — confirm the endpoint set + response shapes (is it
   the `/soa/agent/*` + `/session/*` + `/tool/*` + `/directory` spec above, and on what
   port/host?).
2. **`/directory` vs `/tool/contact_add`** — which is the actual CRM route?
3. **`/questionnaire`** — JSON `{ profile }` or HTML form?
4. Whether the gateway is a **separate service** from `front-desk/` (port 8120), so I
   know not to touch my desk while wiring these up.
