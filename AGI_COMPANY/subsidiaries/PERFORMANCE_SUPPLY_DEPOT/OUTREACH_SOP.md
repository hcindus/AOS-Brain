# PSD Supply Canvas — Outreach SOP

**Owner:** Performance Supply Depot LLC
**Goal:** Nationwide cold outreach to food-service businesses (restaurants, cafés, taquerias, bakeries, coffee shops) for thermal paper + printer ribbons.
**Cadence:** 5 leads/day, state-by-state (alphabetical), durable/resumable via Temporal.

---

## Team & Roles

| Agent | Runtime | Role |
|---|---|---|
| **Beets** | Hermes (external) | Enrichment — `name + address → email + phone` |
| **Hume** | Ollama Mort_II | Regional targeting — pick the next state + prioritize leads |
| **CLOSETER** | Ollama Mort_II | Conversion — classify replies + respond / flag orders |
| **Judy** | Ollama Mort_II | Operations — track the pipeline + schedule follow-ups + enforce SOP |
| **Jordan** | Ollama qwen3.5 | Workflow — own the Temporal orchestration + glue |
| **Miles** | (overseer) | Oversight — monitor, approve edge cases, handle payments |

---

## The Pipeline (one durable Temporal workflow per lead)

```
1. ENRICH    Beets: name+address -> email+phone  (write to DepotChaos vendors)
2. SELECT    Hume: state-by-state, 5/day, food-service + email + phone
3. SEND      cold email (Miles copy: 5/day, BCC info@psdepot.com)
4. FOLLOWUP  timer +4 days -> if no reply, send follow-up
5. REPLY     CLOSETER: classify (ORDER / QUESTION / INTEREST / NOT-INTERESTED / UNKNOWN)
6. ACT       CLOSETER: respond (question/info) OR flag Captain (order/unknown)
7. ORDER     Captain collects card -> mark converted -> vendors ship
8. CLOSE     no reply after N days -> mark lost/closed
```

---

## Each Agent's SOP

### Beets (Enrichment)
1. Query `DepotChaos/depot_chaos.db` → `vendors` WHERE `data_class='real'` AND `email=''`.
2. For each lead: search `name+address` → find website → extract contact email + phone.
3. **Never guess-pattern emails** (no `firstname@domain`). Only record high-confidence finds.
4. `UPDATE vendors SET email=?, phone=?` for enriched leads.
5. Report yield (processed / email-found / phone-found).

### Hume (Regional Targeting)
1. Work state-by-state (alphabetical, starting CA).
2. For the current state, pull food-service leads (`restaurant/cafe/bar/seafood/brewery/pub` + name keywords) with `email + phone`.
3. Select the next 5 for the day (skip already-emailed via sent-log).
4. Hand the 5 to the `send_cold_email` activity.
5. Advance to the next city/state when exhausted.

### CLOSETER (Conversion)
1. Read `closeter_inbox.json` (new replies).
2. Classify intent: ORDER / QUESTION / INTEREST / NOT-INTERESTED / UNKNOWN.
3. Act: auto-answer (question/info), confirm + flag (order), close (not-interested), flag (unknown).
4. **Never auto-process money** — orders always flag the Captain.

### Judy (Operations)
1. Track every lead through the funnel (emailed → replied → ordered → closed).
2. Maintain the follow-up calendar (who's due, who's gone cold).
3. Enforce the SOP checklist per stage.
4. Flag anomalies (stuck leads, missed follow-ups) to Miles.

### Jordan (Workflow / Temporal)
1. Own the Temporal workflow + worker + activities.
2. Ensure every stage is durable (timer + activity results persist across restarts).
3. Register + supervise the `outreach-queue`.
4. Re-run/backfill any workflow that failed.

### Miles (Oversight)
1. Review flagged orders + unknown intents.
2. Collect cards (Option A) — the one human-in-the-loop money step.
3. Approve copy/pricing changes.

---

## Failure & Resume (Temporal durability)

Every lead runs as a **Temporal workflow**. If any activity fails or the worker restarts:
- Timers (follow-up waits) and activity results persist in the Temporal server.
- The workflow **resumes from where it left off** — no lead is dropped, no follow-up is lost.

---

## Handoff Rules
- **Order / money** → always Miles (Captain in the loop) until a Square API key is added.
- **Ambiguous reply** → flag Miles, don't guess.
- **Escalation** (custom deal / enterprise) → Miles → Jane (enterprise sales).

---

*Last updated: 2026-11-09*
