#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-18 (live data)."""
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

Key stats (live @ 06:00 UTC):
- ⚠️ SYSTEM REBOOTED — uptime 9h22m (was 150d+ yesterday). Load 0.92/0.94/1.06 🟢 | Mem 7.7Gi/15Gi (7.9Gi avail) 🟢 | Disk 76% | Swap 512Ki/29Gi 🟢 — all healthy post-reboot.
- Email queue (email_queue table): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026
- DepotChaos queue API: 99 pending (teriyaki thermal + outreach), sent_today 0, failed_today 0
- 🔴 SendGrid REGRESSED — api_key_configured now FALSE (was true yesterday). Key was unset/reverted. Queue still not sending.
- PENDING_TASKS: 4,050 (all CA_SOS_Scraper mock — do NOT send); lastUpdated 10-16 11:15 UTC 🔴 2 days stale (scraper did not run 10-17 or 10-18)
- Active unified.db (data/depot_chaos/unified.db, 94.3MB): unified_leads 1,460 | leads 32,590 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | datadepot_intelligence 74,518 | address_crossref 3,535 | email_queue 207 | verified_leads 1
- ⚠️ datadepot/unified.db still 0 bytes (truncated Oct 3) — active DB at data/depot_chaos/unified.db
- 2 FAILED services: certbot, dailyaidecheck (aos-ternary recovered since yesterday)

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607) + 99 pending (teriyaki), 0 sent all-time. SendGrid key was reverted to unset; needs a decision: re-set key, send, or clear.
2. 🔴 PENDING_TASKS scraper stale 2 days (last ran 10-16) — check ca_sos_scraper cron.
3. ⚠️ System rebooted overnight — verify all services came back (only 2 failed now, good).
4. Confirm intended location of unified.db — datadepot/ copy truncated to 0 bytes since Oct 3.

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
