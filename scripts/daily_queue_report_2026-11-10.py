#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-10 (live data @ 06:00 UTC)."""
import smtplib, ssl, os, sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.environ.get("HOSTINGER_SMTP_SERVER", "smtp.hostinger.com")
SMTP_PORT = int(os.environ.get("HOSTINGER_SMTP_PORT", "587"))
FROM = os.environ.get("HOSTINGER_SMTP_USER", "miles@myl0nr0s.cloud")
TO = "antonio.hudnall@gmail.com"
PASS = os.environ.get("HOSTINGER_SMTP_PASS") or os.environ.get("SMTP_PASS") or "Myl0n.R0s"

now = datetime.utcnow()
date_str = now.strftime("%B %d, %Y")
ts = now.strftime("%Y-%m-%d %H:%M UTC")

report = f"""📊 Daily Queue Report — {date_str}
Generated: {ts}

Key stats (live @ 06:00 UTC):
- 🟢 Uptime 2d 5h13m (no reboot overnight). Load 2.20/1.89/1.68 🟢 | Mem 10Gi/15Gi (5.5Gi avail) 🟡 | Disk 79% flat | Swap 894Mi/29Gi 🟢
- 🔴 Top CPU: chat_server.py ~110% (myl0nr0s.cloud API), continuous_vision_daemon ~35%, vision_service ~26%, openclaw-gateway ~18%, ollama runner ~17%. train_server.py NOT running (RP1 training inactive).
- 🟡 2 FAILED services: certbot, dailyaidecheck (both recovered/safe but still marked failed).
- 🟢 Email queue (email_queue) PROGRESS: 59 sent, 148 ready (was 207 ready / 0 sent on 11-08). Last send Nov 08 19:30 UTC. Campaign capton_hospitality_202607 no longer fully stalled.
- 🟡 unified.db 335MB (was 265MB) — last written Nov 09 20:38 UTC (was Nov 07 06:30). Write frequency improved.
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL not found (only idx_enrichment index remains).
- Table counts: unified_leads 1,460 | leads 32,591 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 (↑ from 502) | psd_customer_sales 235 (↓ from 503) | verified_leads 1 | scrape_runs 4

Action items:
1. ✅ Email queue un-stalled — 59 sent. Confirm the sender path (Hostinger SMTP vs SendGrid) and whether to continue draining remaining 148.
2. 🟡 psd_customer_sales dropped 503→235 — verify whether this is a re-import, dedup, or data loss.
3. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
4. 🟡 unified.db now writes ~daily (Nov 09) — confirm scraper/daemon cron schedule is intentional.

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
