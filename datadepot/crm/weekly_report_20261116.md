# DataDepot Weekly Sales Sprint Report
**Week Ending:** Monday, November 16, 2026
**Reporting:** Pulp (Head of Sales)
**Status:** Week 29 — outbound email RESTARTED; now throttled by Hostinger rate-limit. First material movement since June.

---

## ⚡ Material Change This Week

For the first time since ~June 15, outbound email campaigns are **attempting to send** — not zero. The hard `553 sender-not-owned` rejection from prior weeks is resolved. What remains is a **soft throttle**: the Hostinger outbound relay is rate-limiting bulk sends with `451 4.7.1 Ratelimit "hostinger_out_ratelimit" exceeded` (key `RLnxigg46w84qqxnok68pwkzh4`).

Three campaigns fired this week (Nov 9–15):

| Campaign | Attempted | Delivered | Bounced (451) |
|----------|-----------|-----------|---------------|
| Thanksgiving (seasonal) | 134 | ~most | subset |
| Ribbon / toner | 131 | ~most | subset |
| Reorder (existing customers) | 23 | ✓ | 0 (reminder loop) |

Bounce logs record **88 × 451 rate-limit** + 1 × 421 across `reorder_bounces.log` (10) and `courtesy_bounces.log` (79). Net: sends are going out, but bulk volume is being clamped by the shared Hostinger relay.

---

## 🎯 Performance Summary vs. Targets

| Metric | Target | Actual | % |
|--------|--------|--------|---|
| Demos Booked | 8/week | 0 | 0% 🔴 |
| Closes | 2/week | 0 | 0% 🔴 |
| MRR Growth | $1,000 | $0 | 0% 🔴 |
| Emails Sent (attempted) | 145/week | ~288 | 199% 🟢 |
| Calls Made | 125/week | 0 (49 queued) | 0% 🔴 |

Email volume finally broke zero — but it's *attempted* sends, with a meaningful bounce tail. No demos, no closes, no MRR yet.

---

## 📬 Email Layer — actual state (re-verified Nov 16)

- **Sender verification:** ✅ Fixed (553 "sender not owned" no longer appearing).
- **New blocker:** 🔴 Hostinger outbound rate-limit (451) throttling bulk sends. Single-shared-relay key.
- **Inbound (CLOSETER):** ✅ Live — processing order-intent emails, flagging card-collection to Captain. 5 orders this week (all `test@example.com` = test fixtures, not real revenue).
- **Mortimer relay:** 🔴 84 failed / 0 done in `mortimer_email_state.json`.
- **vendor_email_switch:** disabled.

---

## 📊 Pipeline (Tier-1 POS-tech list still frozen)

- Enriched leads: 100 (52 Tier 1 / 35 Tier 2 / 13 Tier 3), 0 contacted. ~$27,100 potential.
- The POS-tech SaaS pipeline remains untouched — this week's volume was **thermal-paper / ribbon / reorder** (physical supplies), not the SaaS Tier-1 list.
- No response-rate analysis possible on the SaaS list — still 0 SaaS sends.

---

## 🚨 Infrastructure Status

| System | Status | Detail |
|--------|--------|--------|
| Email relay (Hostinger) | 🟡 **THROTTLED** | 451 outbound rate-limit on bulk sends. Sender ownership fixed. |
| Email campaigns | 🟢 FIRING | Thanksgiving 134, ribbon/toner 131, reorder 23 (attempted). |
| CLOSETER (inbound orders) | 🟢 ACTIVE | Order intent → card collection flagged to Captain. |
| Phone pivot | 🟡 PREPPED | 49 restaurants queued (`phone_call_queue.json`), 0 dials yet. |
| Multi-state scraper | 🟢 ACTIVE | 158 biz / 13 states daily (12-per-state sample). |
| Temporal workflows | 🟡 STUCK | 3 RUNNING, 0 completed. |
| submit_leads.py | 🔴 BROKEN | `ImportError: WorkflowHandle` from `temporalio.workflow`. |
| Hume territory intel | 🔴 STALE | ~201 days (Apr 29). No refresh. |
| ABC licenses | 🔴 CORRUPTED | 4-schema concat; cleanup pending Captain. |

---

## 🎯 Decision Required (updated)

1. **Lift the 451 rate-limit** — the sender is fixed; now the shared Hostinger relay throttles bulk volume. Options: (a) raise/wait out the Hostinger outbound quota, (b) move bulk sends off the shared relay (dedicated SMTP / SendGrid / SES), or (c) pace sends under the hourly limit. This is the next unblock to reach clean delivery at volume.
2. **Start dialing the 49-phone queue** — the phone pivot is staged and needs no email infra. This is the fastest path to actual demos/closes right now.
3. **Fix submit_leads.py** (`temporalio.workflow.WorkflowHandle` → `ChildWorkflowHandle`) — Temporal lead-submission is dead.

---

## 🎯 Next Week

- **Pace email sends** under the Hostinger hourly cap to cut the 451 tail (serialize bursts; respect rate-limit rather than hammering).
- **Activate the phone queue** — 49 staged restaurants are the nearest real demos/closes.
- **Hold Tier-1 SaaS list at ready** — the 52 top leads remain the highest-value asset the moment clean email delivery is confirmed.
- **Recommendation to Captain:** prioritize (a) phone pivot activation and (b) a dedicated/bulk mail relay to escape the shared Hostinger throttle.

---

*Report Generated:* Monday, November 16, 2026 17:05 UTC
*Report Owner:* Pulp (Head of Sales)
*Territory Intel:* Hume (~201 days stale)
*Infrastructure:* Forge (scraper active; submit_leads.py broken)
*Blocker Owner:* Captain (rate-limit lift / phone pivot approval / dedicated mail relay)
