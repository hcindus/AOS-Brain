# Order Automation System

Miles places orders and handles vendor outreach on the Captain's behalf.
Drop an order spec JSON into `inbox/` and it will be auto-processed (sent + logged + archived).

## Vendor directory
`../vendor_contacts.json` — name → { email, notes }.

```bash
# Add a vendor
python3 scripts/vendor_comms.py add-vendor "Labels Direct" brandon@labelsdirect.com "trusted, fair"
```

## Introduction (new vendor)
```bash
python3 scripts/vendor_comms.py introduce "Labels Direct"
```
Sends a standardized intro: who PSD is, what we buy, ask for catalog / volume breaks / lead times / CA shipping.

## Order spec schema (drop in `inbox/`)
```json
{
  "vendor": "Labels Direct",
  "vendor_email": "brandon@labelsdirect.com",
  "po": "optional — auto-assigned as PSD-YYYY-NNNN if omitted",
  "contact_name": "Brandon",
  "items": [
    {
      "sku": "LD46TTBOPP15PWI",
      "desc": "Matte BOPP label, 1.5\" core",
      "qty": 10,
      "unit": "case",
      "price": 446.00
    }
  ],
  "ship_to": "Performance Supply Depot LLC\n<full street address>",
  "quote_only": false,
  "notes": "optional"
}
```

## Processing
```bash
# Process everything sitting in inbox/ (send + log + archive to sent/)
python3 scripts/vendor_comms.py process-inbox

# Or process one file directly
python3 scripts/vendor_comms.py order data/orders/inbox/my-order.json
```

## Status / history
- `history.json` — every order with PO, vendor, items, ship_to, status, sent_at.
- `../email_inbox/` — inbound email copies.
- Inbound watch cron (every 15 min) announces new vendor/customer email to the Captain on Telegram.
- Outbound is BCC'd to `info@psdepot.com` for the record.

## Status values
`sent` → `awaiting-reply` → `confirmed` / `shipped` / `closed` (updated as replies come in).
