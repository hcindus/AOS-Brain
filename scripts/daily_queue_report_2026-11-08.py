#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-08 (live data @ 06:00 UTC)."""
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
- ⚠️ SYSTEM REBOOTED overnight — uptime 5h12m (was 3d 2h24m yesterday). Load 2.06/1.33/1.11 🟢 (DOWN from 3.87/5.59/7.66). Mem 9.4Gi/15Gi (6.3Gi avail) 🟡 | Disk 79% flat | Swap 472Mi/29Gi 🟢 (reset by reboot; was 9.3Gi)
- 🔴 Top CPU (changed after reboot): ollama runner ~103% (now top), continuous_vision_daemon ~62%, vision_service ~40%, openclaw-gateway ~29%. train_server.py NO LONGER running (RP1 training stopped after reboot).
- 🟡 1 FAILED service: dailyaidecheck (certbot now recovered)
- 🟡 unified.db 265MB (flat) — last written Nov 07 06:30 UTC, single-cycle-then-stop pattern persists
- 🔴 Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time — STILL STALLED since July 2026
- 🔴 PENDING_TASKS table STILL absent from unified.db (unchanged) — verify CA_SOS scraper DB source.
- ⚠️ enrichment_queue table STILL not found (only idx_enrichment index remains).
- Table counts: unified_leads 1,460 | leads 32,591 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | verified_leads 1 | scrape_runs 4

Action items:
1. 🔴 Email queue STILL stalled — 207 ready, 0 sent all-time since July. Needs a decision: set a real SendGrid key, send via verified Hostinger SMTP sender, or clear.
2. 🟡 Post-reboot verification — confirm the reboot was intentional and that train_server.py (RP1 training) not restarting is expected.
3. 🟡 unified.db write pattern = ~once/day then stall. Investigate cron/loop schedule for the scraper/daemon.
4. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.

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
