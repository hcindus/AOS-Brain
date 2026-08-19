---
name: sop-quote-followup
description: Generate accurate quotes within 2 hours of a qualified lead and systematically follow up to close 35%+. Covers requirements verification, pricing, quote delivery, and a 30-day follow-up sequence. Use when a HOT/WARM lead (from sop-lead-response) needs a quote.
---

# SOP-002 — Quote Generation & Follow-Up

**KPI:** 2-hour quote turnaround · 35%+ close rate · tracked per lead.

## Step 1 — Requirements verification (0–15 min)
Confirm before pricing:
- Product category, quantity, delivery timeline
- Special requirements (branding, customization)
- Current supplier/competitor, budget range

If anything's missing, ask first: *"Before I send this, I want to make sure I'm including exactly what you need. Quick question…"*

## Step 2 — Pricing lookup (15–30 min)
Pull accurate pricing from the catalog / `products.json` / vendor sheets. No guesses — quote what's real.

## Step 3 — Quote delivery (within 2h)
Generate the PDF quote (use `jarvis_core` `QuoteEngine`) with:
- Client name + business
- Line items (description, qty, unit, total)
- Terms: **50% deposit to book, 50% due on delivery**
- Total

Send with a short note: *"Here's your quote. Happy to walk through it — 15 min this week?"*

## Step 4 — Follow-up (30-day sequence)
| Day | Action |
|---|---|
| Day 2 | "Did you get a chance to look at the quote?" |
| Day 5 | "Any questions on pricing or the build process?" |
| Day 10 | "We can hold pricing for a bit — still interested?" |
| Day 20 | "Closing your file soon — worth one more look?" |
| Day 30 | Final touch: "Here if it comes back up." |

## KPI check
Did the quote go out within 2 hours? Is follow-up scheduled? Am I tracking toward 35%+ close?
