#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-15 (live data)."""
import smtplib, ssl, os, sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
FROM = "miles@myl0nr0s.cloud"
TO = "antonio.hudnall@gmail.com"
PASS = os.environ.get("HOSTINGER_SMTP_PASS", "Myl0n.R0s")

now = datetime.utcnow()
date_str = now.strftime("%B %d, %Y")
ts = now.strftime("%Y-%m-%d %H:%M UTC")

report = f"""📊 Daily Queue Report — {date_str}
Generated: {ts}

Key stats (live @ 06:00 UTC):
- Uptime 148d 21h08m | Load 3.51/2.88/2.96 🟡 elevated (baseline ~2.2) | Mem 4.4Gi/15Gi (11Gi avail) | Disk 75%
- Swap 6.7Gi/29Gi
- Email queue (email_queue table): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026
- DepotChaos queue API: 99 pending (teriyaki thermal + outreach), sent_today 0, failed_today 0
- PENDING_TASKS: 3,950 (all CA_SOS_Scraper mock leads — do NOT send); lastUpdated 10-14 11:16 UTC ✅ refreshed (freshness checker ran)
- Active unified.db (data/depot_chaos/unified.db, 93.4MB): unified_leads 1,460 | leads 32,588 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 501 | psd_customer_sales 503 | datadepot_intelligence 74,518 | address_crossref 3,535 | email_queue 207 | verified_leads 1
- ⚠️ datadepot/unified.db still 0 bytes (truncated Oct 3) — active DB at data/depot_chaos/unified.db
- 3 FAILED services: aos-ternary, certbot, dailyaidecheck

Action items:
1. 🔴 Email queue still stalled — 207 ready (capton_hospitality_202607) + 99 pending (teriyaki) never sent. Needs a decision: send or clear.
2. 🟡 Load elevated at 3.51 (baseline ~2.2) — worth a quick look at CPU consumers.
3. 3 failed services (aos-ternary, certbot, dailyaidecheck) still down.
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
