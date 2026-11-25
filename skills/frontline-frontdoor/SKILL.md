---
name: frontline-frontdoor
description: Bottled engineering patterns from the Frontline SOA voice receptionist (n8n × Twilio × gateway) — the two-phase "answer-fast / compute-in-background" latency fix, deterministic-before-LLM routing, and the front-door hygiene rules. Use when wiring any synchronous inbound trigger (voice, email, chat, webhook) to a slow AI backend, or when designing an n8n/agent intake workflow.
---

# Frontline Front-Door Patterns

**KPI:** A synchronous inbound trigger that never times out and never hard-fails — it
answers in <1s, computes in the background, and degrades gracefully. One model call per
turn, no secrets in the workflow, and onboarding a new client = fill a form, not edit code.

**Source (Frontline SOA, 2026-11-25):** Two n8n voice-receptionist workflows — a
single-phase and a two-phase version — surfaced these patterns. They are channel-agnostic
and reusable.

---

## 1 · The two-phase pattern (the crown jewel)

**Problem:** Twilio (and most webhooks) drops a request that doesn't answer in ~15s. A
CPU agent turn takes ~28s. A synchronous `trigger → AI → reply` chain therefore dies in
production.

**Fix — split the turn in two phases:**

1. **Phase one** answers *instantly* with a placeholder + a redirect/hold:
   `<Say>One moment…</Say><Redirect>…-reply?n=1</Redirect>` — and *the same execution
   keeps running* to compute the real answer in the background.
2. **Phase two** is a lightweight poller: read the session store; if the answer is
   ready → `<Say>` + next step; if not → `<Pause length="2"/>` + redirect with `n+1`;
   if out of budget (n ≥ 20, ~40s) → take a message + leave a callback task.

**The background answer is written to a durable session store** (`/session/<callSid>`),
not to in-memory n8n state — so a restart doesn't lose it, and multiple pollers see the
same truth.

**Rule of thumb:** any synchronous trigger + slow AI = answer fast with a placeholder,
compute in the background, poll (or webhook-back). Never block the trigger on the model.

---

## 2 · Deterministic routing before the LLM

**Problem:** a classifier LLM call is slow and expensive. Don't spend a model call when a
regex can route.

**Fix — keyword rules first, sticky ownership:**

```js
const rules = [
  { agent: 'concierge', re: /\b(book|appointment|schedule|reserve)\b/ },
  { agent: 'closeter', re: /\b(price|quote|cost|buy|order)\b/ },
  { agent: 'clerk',    re: /\b(invoice|receipt|billing|account)\b/ },
];
let agent = previousAgent || 'greet';   // sticky: keep the specialist once assigned
for (const r of rules) if (r.re.test(text)) { agent = r.agent; break; }
```

- **One model call per turn** — the LLM only writes the *reply*, never re-classifies.
- **Sticky ownership** — once a specialist owns the call, keep them unless a new rule
  fires. This preserves context and avoids flip-flopping.

This is the "20% of the code" leverage: cheap, instant, explainable routing up front.

---

## 3 · Front-door hygiene rules

1. **Read the raw payload once.** Flatten the webhook body into one flat item
   (`Read Call`) so no later HTTP node can shadow the call facts (`$json` gets replaced
   by every HTTP node).
2. **Every external call is `neverError: true`** + a graceful fallback reply
   ("I'm sorry, I didn't catch that"). The workflow must never hard-fail on a gateway
   hiccup.
3. **No secrets in the file.** Tokens, numbers, ngrok hosts — all env-referenced
   (`$env.FOO`). Safe to version and share.
4. **Ack callbacks.** Return an empty `<Response></Response>` to Twilio
   transcript/recording callbacks so it stops retrying.
5. **Node names are a contract.** `$('Read Call').first().json` cross-references mean
   renaming a node silently breaks the flow. Keep names stable, or pass values forward.
6. **Config-driven, not code-driven.** Greeting, hours, voice, forward number all come
   from the client's profile (`/questionnaire`), so one workflow serves N clients.

---

## 4 · n8n specifics that bite

- Set `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` — n8n 2.x blocks `$env` by default.
- `$getWorkflowStaticData('global')` is volatile (lost on restart, not shared across
  instances). Use a real session store for anything production.
- Twilio voice webhook timeout is ~15s; a `<Gather input="speech" speechTimeout="auto">`
  is the idiomatic way to capture the next utterance in the same call.
- `respondToWebhook` sends the response *and the execution continues* — that's what makes
  phase one of the two-phase pattern possible.

---

## 5 · Webhook authentication (do not skip)

An unauthenticated voice webhook is an injection hole: anyone who finds the URL can POST
forged call payloads and write tasks/notes/CRM entries.

- **Correct fix:** validate the Twilio `X-Twilio-Signature` header
  (HMAC-SHA1 of `fullUrl + sorted(postParams)`, keyed by the auth token). Must use the
  *exact* URL Twilio called, including scheme and query string.
- **Lighter fix:** a shared secret in the webhook URL query string, checked in a code
  node right after `Read Call`.
- **Safe default:** if the auth token is unset, pass through with a warning rather than
  hard-rejecting — so enabling auth can't accidentally drop every real call.

---

## 6 · When to use each phase

| | Single-phase | Two-phase |
|---|---|---|
| Turn latency budget | must finish < 15s | caller hears ~2s hold, answer streams in |
| History storage | n8n static data (volatile) | durable session store |
| Round-trips per turn | none | 3–4 (reset / load / store / poll) |
| Verdict | dev / demo only | **the live design** |

Use single-phase only when you've *proven* every turn is sub-15s (GPU, cached, short).
