#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-24 (live data @ 11:39 UTC)."""
import smtplib, ssl, os, sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
FROM = "miles@myl0nr0s.cloud"
TO = "antonio.hudnall@gmail.com"
PASS = os.environ.get("HOSTINGER_SMTP_PASS") or os.environ.get("SMTP_PASS") or "Myl0n.R0s"

now = datetime.utcnow()
date_str = now.strftime("%B %d, %Y")
ts = now.strftime("%Y-%m-%d %H:%M UTC")

report = f"""📊 Daily Queue Report — {date_str}
Generated: {ts}

Key stats (live @ 11:39 UTC):
- Uptime 6d 15h00m. Load 2.45/3.10/3.33 🟡 (elevated — was ~0.7 on prior days; likely transient cron burst). Mem 12Gi/15Gi (3.5Gi avail) 🟡 | Disk 79% | Swap 4.8Gi/29Gi 🟢
- Email queue (email_queue table): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026
- DepotChaos enrichment_queue: 1,000 "available", 0 claimed/completed
- ⚠️ SendGrid still NOT truly configured — api_key field holds the literal "${{SENDGRID_API_KEY}}" placeholder, never resolved to a real key. 0 sent today.
- PENDING_TASKS: 4,300 (all CA_SOS_Scraper mock — do NOT send); lastUpdated 2026-10-22T11:16 UTC ⚠️ scraper did NOT run 10-23 or 10-24 (2 days stale; last lead file still ca_leads_2026-10-22.json)
- Active unified.db (data/depot_chaos/unified.db, 90MB): unified_leads 1,460 | leads 32,590 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | datadepot_intelligence 74,518 | address_crossref 3,535 | email_queue 207 | verified_leads 1
- ⚠️ datadepot/unified.db + root unified.db still 0 bytes (truncated Oct 3 / Oct 19) — active DB lives at data/depot_chaos/unified.db
- 2 FAILED services: certbot, dailyaidecheck (unchanged; timers still active)

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time. Needs a decision: re-set a real SendGrid key, send, or clear.
2. ⚠️ SendGrid key is a false positive — api key field holds the literal "${{SENDGRID_API_KEY}}" placeholder, never expanded. Blocked on Captain for a real SendGrid API key.
3. ⚠️ CA_SOS_Scraper stale 2 days (lastUpdated 10-22 11:16). Cron may have stopped; investigate if it stays stale.
4. ⚠️ Load average elevated (~2.5-3.3) — likely transient, but worth a glance if it persists.
5. ⚠️ DepotChaos enrichment_queue has 1,000 "available" but 0 claimed — enrichment daemon may be idle.

—
Miles 🚀 (automated)
miles@myl0nr0s.cloud
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = f"📊 Daily Queue Report — {date_str}"
msg["From"] = FROM
msg["To"] = TO
msg.attach(MIMEText(report, "plain", "utf-8"))

try:
    ctx = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
        s.starttls(context=ctx)
        s.login(FROM, PASS)
        s.send_message(msg)
    print("SENT")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
