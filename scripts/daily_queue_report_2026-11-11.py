#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-11 (live data @ 06:00 UTC)."""
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
- 🟢 Uptime 3d 5h12m (no reboot overnight). Load 2.08/1.32/1.09 🟢 | Mem 8.4Gi/15Gi (7.3Gi avail) 🟢 | Disk 79% flat | Swap 911Mi/29Gi 🟢
- 🟢 Top CPU: continuous_vision_daemon.py ~33%, vision_service.py ~24%, ollama ~14%, openclaw-gateway ~10%. chat_server.py NOT running (was ~110% yesterday — dropped off). train_server.py NOT running (RP1 training inactive).
- 🟡 2 FAILED services: certbot, dailyaidecheck (both recovered/safe but still marked failed).
- 🔴 Email queue STALLED again: 59 sent / 148 ready — UNCHANGED from 11-10. Last send still Nov 08 19:30 UTC. Campaign capton_hospitality_202607 has not progressed in 2+ days.
- 🟡 unified.db 371MB (was 335MB) — last written Nov 10 12:23 UTC (daily cadence holding).
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL not found (only idx_enrichment index remains).
- Table counts: unified_leads 1,460 | leads 33,086 (↑ from 32,591) | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 | psd_customer_sales 235 | verified_leads 1 | scrape_runs 4

Action items:
1. 🔴 Email queue re-stalled — no sends since Nov 08 19:30. Confirm whether the drain stopped (rate limit, daemon down, or intentional pause) and whether to resume the remaining 148.
2. 🟢 leads +495 (32,591→33,086) — scraper pipeline active and writing; confirm expected.
3. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
4. 🟡 chat_server.py dropped off CPU (was ~110% yesterday) — verify it wasn't intended to be running.

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
