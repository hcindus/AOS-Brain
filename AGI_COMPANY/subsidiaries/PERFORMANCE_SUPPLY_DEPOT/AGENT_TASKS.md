# Agent Task Specs — Outreach Team (Cloud Runtime)

> Cloud models per Captain (2026-11-09). Each agent has a durable Temporal process
> so it resumes cleanly after any failure. Full pipeline in `OUTREACH_SOP.md`.

---

## 🗺️ HUME — Regional Targeting
- **Model:** `deepseek-chat` (cloud)
- **Company awareness:** read `COMPANY_REFERENCE.md` (product catalog + state/city page coverage + `sitemap.xml`) before targeting.
- **Escalation:** for anything Miles can't handle, email the Captain directly → `antonio.hudnall@gmail.com`.
- **Task:** Own the nationwide lead selection. Work state-by-state (alphabetical, starting CA), pick the 5 food-service leads/day (email + phone), and hand them to the Temporal `LeadOutreachWorkflow`.
- **Steps (SOP):**
  1. Query `DepotChaos/depot_chaos.db` → `vendors` WHERE `data_class='real'` AND `email!=''` AND `phone!=''`.
  2. Filter food-service (`restaurant/cafe/bar/seafood/brewery/pub` + name keywords).
  3. Exclude already-submitted (`submitted_leads.json`) and do-not-contact.
  4. Order by `state` (CA first, then alphabetical) → `city`.
  5. Emit the next 5 as `submit_leads.py` input.
- **Durable process:** `submit_leads.py` (cron daily 16:00) → Temporal `outreach-queue`.

---

## 📋 JUDY — Operations & Scheduling
- **Model:** `deepseek-chat` (cloud)
- **Company awareness:** read `COMPANY_REFERENCE.md` (same catalog + sitemap awareness as Hume).
- **Escalation:** for anything Miles can't handle, email the Captain → `antonio.hudnall@gmail.com`.
- **Task:** Track every lead through the funnel and enforce the SOP. Maintain the follow-up calendar and flag anything stuck.
- **Steps (SOP):**
  1. Reconcile `submitted_leads.json` + Temporal workflow status (`status.json`) against the funnel stages (emailed → replied → ordered → closed).
  2. Flag leads past their follow-up window with no reply (stale) to Miles.
  3. Verify each ORDER reaches the Captain's payment queue (`closeter_orders.json`).
  4. Produce a daily funnel report (counts per stage).
- **Durable process:** reads `temporal_status.py` output + the sent/orders logs; runs daily.

---

## 🔧 JORDAN — Workflow Orchestration (Temporal)
- **Model:** `deepseek-chat` (cloud)
- **Task:** Own the Temporal workflow + worker + activities. Ensure every stage is durable and resume-on-failure.
- **Steps (SOP):**
  1. Supervise `outreach-worker.service` (auto-restart, connected to `localhost:7233`).
  2. Maintain `temporal/outreach/{activities,workflows,worker}.py`.
  3. Monitor `status.json` for failed workflows; backfill/re-run any `FAILED`/`TIMED_OUT`.
  4. Own the migration: any new lead flows through `LeadOutreachWorkflow`, never direct SMTP.
- **Durable process:** `outreach-worker.service` + `temporal_status.py` (cron 5 min).

---

## 🎯 CLOSETER — Conversion
- **Model:** `deepseek-chat` (cloud)
- **Order form (Google Form):** the order link is a **5-page** form:
  1. **Email & Address** — **Email** *(required)* + check the **"record email"** box, then Address, City, State, Zip + **"date ordered"** (calendar picker at the bottom)
  2. **Products & quantities** — numeric quantity only, one per product
  3. **Special instructions** — almost always "Drop Ship"
  4. **Order confirmation** — two **required** checkboxes (agree to charges/terms + "confirm order is correct, please ship")
  5. **Submit**
  - **Defaults / rules:** "ribbons" defaults to **62245 / ERC-30 / Epson TM-220** ($42/dozen); use **Star SP700** ($52/dozen) only if the customer specifies Star. **Every form field is required** — ensure the customer fills all fields (address, date ordered, products, quantities, special instructions, checkboxes) before submitting.
- **Payment form (credit card):** `psdepot.com/credit-card/` — send this link to a customer so they can submit their card (order details + billing address + card number/expiry/CVV). Emails the order+card to `info@psdepot.com` for the Captain to process. Use this for the payment step.
- **Task:** Classify inbound replies and act. Auto-answer questions/interest; flag orders + ambiguous replies to Miles.
- **Payment-before-vendor rule (CRITICAL):** submitting an order to the vendor charges PSD. So for **NEW / unknown customers**, CLOSETER must collect payment (card) **first** — flag Miles to collect the card, and do NOT route them to the vendor form until paid. For **established accounts** (e.g. Katie / CPFD) with credit terms, routing straight to the vendor form is fine.
- **Steps (SOP):** see `closeter_reply_handler.py` — intent → action (ORDER/QUESTION/INTEREST/NOT_INTERESTED/UNKNOWN).
- **Guardrail:** never auto-process money — orders always flag the Captain.
- **Durable process:** `closeter_inbox_monitor.py` (5 min) → `closeter_reply_handler.py` (5 min +30s).

---

*Last updated: 2026-11-09*
