#!/usr/bin/env python3
"""Daily Queue Report — 2026-09-16 (live data)."""
import smtplib, ssl, os, sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.insert(0, "/root/.openclaw/workspace/aocros/secrets")

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
- Uptime 119d 21h08m | Load 1.79/1.26/1.08 🟡 | Mem 4.2Gi/15Gi (28%) 🟢 | Disk 71%
- Swap 5.3Gi/29Gi
- Email queue: 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED
- PENDING_TASKS: 3,150 (all CA_SOS_Scraper mock leads; lastUpdated unchanged 2026-09-11)
- DepotChaos unified.db 73MB: unified_leads 1,460 | leads 32,542 | ca_abc_licenses 74,521 | enriched_leads 919 | psd_customers 501
- 4 FAILED services (aos-ternary, certbot, dailyaidecheck, minecraft); mission-control active

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
    print(f"To: {TO}")
    print(f"Subject: {msg['Subject']}")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
