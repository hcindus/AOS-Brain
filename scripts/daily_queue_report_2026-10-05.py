#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-05 (live data)."""
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

Key stats (live):
- Uptime 139d 2h46m | Load 0.97/1.01/1.11 🟢 | Mem 9.0Gi/15Gi (6.6Gi avail) 🟡 | Disk 73%
- Swap 1.9Gi/29Gi
- Email delivery queue: 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STALLED since July 2026
- Scraper queue: 78 items | 144 reports (lastUpdated 2026-10-05 11:30 UTC)
- DepotChaos unified.db 93.4MB: unified_leads 1,460 | leads 32,587 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 501 | psd_customer_sales 503
- 4 FAILED services: aos-ternary, certbot, dailyaidecheck, minecraft (mission-control + brain v4.5 + BHSI active)

Action items:
1. 🔴 Email queue still stalled — 207 ready emails (capton_hospitality_202607) never sent. Needs decision: send or clear.
2. 4 failed services (aos-ternary, certbot, dailyaidecheck, minecraft) awaiting attention.

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
