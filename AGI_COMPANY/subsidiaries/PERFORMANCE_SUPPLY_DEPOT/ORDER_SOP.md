# Order Process SOP — Performance Supply Depot

Canonical end-to-end order flow. Every step logs to `sales_contacts` + the orders ledger.

## The 8 steps

| # | Step | Owner | Trigger | Tool |
|---|---|---|---|---|
| 1 | **Capture** | Miles (voice) · CLOSETER (email) | inbound order intent | receptionist / reply handler |
| 2 | **Parse** | Miles | free-text → `{sku, qty}` | `order_processor.parse_order` |
| 3 | **Quote** | Miles | subtotal + shipping + tax → price | `order_processor.process_order` |
| 4 | **Confirm** | Captain (human) | customer approves + gives payment method | manual (card on file / Square / check) |
| 5 | **Payment** | Captain | card collected → mark paid | `mark_payment_received` |
| 6 | **Vendor** | Miles | place order → Domtar (email) / ACM (SOAP) | `vendor_order_email` (switch-gated) |
| 7 | **Fulfill** | Captain | vendor ships → customer receives → tracking | manual + note |
| 8 | **Log** | (auto) | every touch | `sales_contacts` + orders ledger |

## Rules (hard)

1. **Agents never auto-process money.** Step 4–5 (confirm + charge) are always the Captain (human). CLOSETER/Miles collect + flag, never charge.
2. **Payment before vendor.** New customers pay before we place the Domtar/ACM order (step 5 → step 6 order).
3. **Vendor switch gated.** Domtar email fires only when `vendor_email_switches.json` = on. ACM stays manual until SOAP auth is fixed.
4. **Every step logged.** No silent order — each touch writes to `sales_contacts` (outcome: order / paid / vendor / fulfilled).

## The "nailed down" flow

```
voice/email order → parse → quote
   → Captain confirms + collects payment (steps 4–5, human)
   → mark paid → thank-you receipt
   → vendor order (Domtar email, switch-gated)
   → fulfill + tracking note
   → logged end-to-end
```

## Current status

- ✅ 1 Capture, 2 Parse, 3 Quote, 5 Payment, 8 Log — built
- ⚠️ 4 Confirm — human, needs the "approve + payment method" step made explicit
- ⚠️ 6 Vendor — Domtar switch OFF (safety), ACM SOAP 403
- ❌ 7 Fulfill — not yet tracked (manual note only)
