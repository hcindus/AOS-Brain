#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-04."""
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
- Uptime 137d 21h08m | Load 1.28/0.88/0.89 🟢 | Mem 10Gi/15Gi (67%) 🟡 | Disk 73%
- Swap 1.3Gi/29Gi
- Email delivery queue: 99 pending (98 teriyaki_thermal_paper_q2_2026 + 1 outreach); 170 sent all-time, last sent 2026-06-15 🔴 STALLED since June
- unified.db email_queue table: 207 (capton_hospitality_202607, still queued)
- PENDING_TASKS: 3,700 (all Active; lastUpdated 2026-10-02)
- DepotChaos unified.db 89.1MB: unified_leads 1,460 | leads 32,587 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 501 | psd_customer_sales 503
- 4 FAILED services (aos-ternary, certbot, dailyaidecheck, minecraft); mission-control + brain v4.5 + BHSI active

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
