# DepotChaos Email Configuration

**Last Updated:** 2026-06-08 10:30 UTC
**Updated By:** Miles

## From Email Address
- **Primary:** info@psdepot.com
- **Previous:** miles@psdepot.com (migrated 2026-06-08)

## Note
- `miles@myl0nr0s.cloud` in email signatures is preserved (this is Miles' actual contact email)
- Only `miles@psdepot.com` → `info@psdepot.com` was changed

## Mailgun Settings
- Domain: psdepot.com
- Test Mode: True (default)
- BCC: info@psdepot.com on all emails

## Files Using info@psdepot.com
- queue_followups.py
- outreach_launcher.py
- queue/followup_queue_20260429.json
- queue/sent_emails.json
- web/depotchaos_fastapi.py
- web/depotchaos_api.py
- cron/process_email_queue.py
- cron/stripe_enrichment.py
- MAILGUN_INTEGRATION.md
- crm/weekly_report_20260518.md

## Queue Files
- pending_emails.json
- calling_blitz_may5_2026.json
- email_sequence_may5_2026.json
- linkedin_sequence_may5_2026.json
