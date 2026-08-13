# Daily Queue Status Report — 2026-08-13 06:00 UTC

## Email Queue (DepotChaos / port 8082)

| Metric | Value |
|--------|-------|
| Pending | 100 |
| Sent (lifetime) | 170 |
| Failed (lifetime) | 28 |
| Sent today | 0 |
| Failed today | 0 |
| Can send now | true |
| Wait seconds | 0 |
| SendGrid API key | ❌ NOT configured |

### ⚠️ Action Required
SendGrid API key is **not configured** (`api_key_configured: false`). The 100 pending
emails are stuck and cannot be delivered. This is a known, open TODO (see
MEMORY.md "SendGrid Integration for DepotChaos" and "TODO: Auth System SendGrid Setup").

To resolve:
1. Obtain/set `SENDGRID_API_KEY`
2. Add DNS records (CNAME + DKIM + DMARC) for psdepot.com
3. Restart `depotchaos` service and process the queue

## Waste Queue (Feedback-to-Curriculum)
- Empty — no pending waste events.

## GoR Delegation Queue
- No live socket command (`gor` returns "Unknown command") — protocol not loaded in
  the currently running brain instance. History file has 2 test entries on disk.

## Brain Status
- v4.5 running, tick 186026, phase "Orient", signal quality 0.895 — healthy.

## Summary
- **1 blocker:** SendGrid unconfigured → 100 stuck emails.
- All other queues clear/nominal.
