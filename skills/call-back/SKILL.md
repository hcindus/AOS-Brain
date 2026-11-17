---
name: call-back
description: Call back any customer or lead via Twilio and log the outcome to DepotChaos (sales_contacts + vendor). Reusable by any department — pass a single number or a queue, and record reached/voicemail/no-answer/outcome so sales results flow back into the CRM.
---

# Call-Back Skill

Re-engage any customer/lead by phone and log the result, so the whole company (sales, support, any department) has a consistent call-back + logging flow.

## Usage

```bash
# Call back a single number (log the attempt to DepotChaos)
python3 call_back.py --to +14155552671 --name "Via Piccola" --channel outbound

# Log the outcome after you/rep dialed
python3 call_back.py --to +14155552671 --name "Via Piccola" \
    --outcome reached --want_prices yes --note "wants pricing"

# Work a queue (e.g. courtesy_callbacks.json)
python3 call_back.py --queue datadepot/data/courtesy_callbacks.json

# Actually place a Twilio call (needs TWILIO_TWIML_URL set)
python3 call_back.py --to +14155552671 --dial
```

## Flags

| Flag | Values | Purpose |
|---|---|---|
| `--to` | phone number | who to call |
| `--name` | text | lead/customer name |
| `--channel` | inbound / outbound | direction |
| `--outcome` | reached, voicemail, no_answer, interested, not_interested, order, question, opted_out, reengage | result |
| `--want_prices` | yes / no | did they want pricing emailed? |
| `--note` | text | free-form note |
| `--dial` | (flag) | actually place a Twilio call |
| `--queue` | JSON file | batch from `{number, name}` list |

## What it writes (DepotChaos)

- `sales_contacts` row: vendor_id, lead_name, contact_type, channel, outcome, want_prices, notes, contacted_at
- `vendors` update: last_contact_at, last_outcome, contact_preference

## ⛔ Call-time rule (hard constraint)

**Never call a restaurant during a meal rush.** The skill blocks dialing during:
- Breakfast rush — 7–10 AM
- Lunch rush — 11 AM–2 PM
- Dinner rush — 5–9 PM

Safe windows: **10–11 AM** and **2–5 PM** (Pacific). `--force` bypasses for testing only.

## Call scripts (canonical tone)

See `datadepot/data/call_scripts.json`:
- **Outgoing (60s):** "did I catch you at a bad time?" → pitch → "can I email you our prices?" → yes/no → "hope we earn your business"
- **Incoming (8min):** "we saw a missed call from this number…" → learn → capture order/follow-up → close politely

## To enable live dialing

Set `TWILIO_TWIML_URL` in `aocros/secrets/twilio.env` to a TwiML endpoint that speaks the call script. Until then, `--dial` won't place the call — it logs the touch (which is the durable record).
