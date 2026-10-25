#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-25 (live data @ 06:01 UTC)."""
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

Key stats (live @ 06:01 UTC):
- Uptime 7d 9h22m. Load 14.14/9.02/5.55 🔴 HIGH (was ~2.5-3.3 yesterday; 1-min spike to 14 — investigate if sustained). Mem 11Gi/15Gi (4.6Gi avail) 🟡 | Disk 79% | Swap 6.4Gi/29Gi 🟢
- Email queue (email_queue table): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026
- DepotChaos enrichment_queue (DepotChaos/enrichment_queue/queue.db): 1,000 "available", 0 claimed/completed
- ⚠️ SendGrid still NOT truly configured — api_key field holds the literal "${{SENDGRID_API_KEY}}" placeholder, never resolved to a real key. 0 sent today.
- PENDING_TASKS: 4,300 (all CA_SOS_Scraper mock — do NOT send); lastUpdated 2026-10-22T11:16 UTC ⚠️ scraper did NOT run 10-23, 10-24, or 10-25 (3 days stale)
- Active unified.db (data/depot_chaos/unified.db, 90MB): unified_leads 1,460 | leads 32,590 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | datadepot_intelligence 74,518 | address_crossref 3,535 | email_queue 207 | verified_leads 1
- ⚠️ datadepot/unified.db + root unified.db still 0 bytes (truncated Oct 3 / Oct 19) — active DB lives at data/depot_chaos/unified.db
- 2 FAILED services: certbot, dailyaidecheck (unchanged; timers still active)

Action items:
1. 🔴 Load average spiked to 14.14 (1-min) — highest observed in weeks. Check `top`/`htop` for a runaway process; likely a transient cron burst but confirm it returns to baseline.
2. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time. Needs a decision: re-set a real SendGrid key, send, or clear.
3. ⚠️ SendGrid key is a false positive — api key field holds the literal "${{SENDGRID_API_KEY}}" placeholder, never expanded. Blocked on Captain for a real SendGrid API key.
4. ⚠️ CA_SOS_Scraper stale 3 days (lastUpdated 10-22 11:16). Cron may have stopped; investigate if it stays stale.
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
