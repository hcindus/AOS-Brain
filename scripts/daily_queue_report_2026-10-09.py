#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-09 (live data)."""
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
- Uptime 142d 21h08m | Load 1.08/0.99/0.81 🟢 | Mem 5.7Gi/15Gi (9.9Gi avail) 🟢 | Disk 73%
- Swap 3.6Gi/29Gi
- Email delivery queue: 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STALLED since July 2026
- pending_emails.json: 99 (teriyaki_thermal_paper_q2_2026: 98, outreach: 1)
- Scraper: 4 scrape_runs
- DepotChaos unified.db 89.1MB: unified_leads 1,460 | leads 32,588 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 501 | psd_customer_sales 503 | datadepot_intelligence 74,518 | address_crossref 3,535
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
