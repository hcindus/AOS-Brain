# DepotChaos Email Queue Update Summary

**Date:** 2026-06-08 10:40 UTC
**Updated By:** Miles

## Changes Made

### From Address Updated
- **Old:** miles@psdepot.com
- **New:** info@psdepot.com

### Files Modified

| File | Change |
|------|--------|
| queue_followups.py | from: miles@psdepot.com → info@psdepot.com |
| outreach_launcher.py | from: miles@psdepot.com → info@psdepot.com |
| cron/process_email_queue.py | default from_email: miles@psdepot.com → info@psdepot.com |
| cron/stripe_enrichment.py | from: miles@psdepot.com → info@psdepot.com |
| web/depotchaos_fastapi.py | from: miles@psdepot.com → info@psdepot.com |
| web/depotchaos_api.py | from: miles@psdepot.com → info@psdepot.com |
| MAILGUN_INTEGRATION.md | FROM_EMAIL: miles@psdepot.com → info@psdepot.com |
| crm/weekly_report_20260518.md | from: miles@psdepot.com → info@psdepot.com |
| queue/followup_queue_20260429.json | from: miles@psdepot.com → info@psdepot.com |
| queue/sent_emails.json | from: miles@psdepot.com → info@psdepot.com |

### Queue Data Updated

| Queue File | Records Updated |
|------------|-----------------|
| pending_emails.json | All from_email fields (info@psdepot.com) |

### Preserved
- miles@myl0nr0s.cloud in email signatures (Miles' personal contact)

## Verification
```bash
# Check for old addresses
grep -r "miles@psdepot.com" /root/.openclaw/workspace/datadepot/
# Result: 0 matches

# Check for new addresses
grep -r "info@psdepot.com" /root/.openclaw/workspace/datadepot/ | wc -l
# Result: 200+ matches
```

## Status
✅ All outgoing emails now use info@psdepot.com
