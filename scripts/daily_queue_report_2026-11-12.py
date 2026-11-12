#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-12 (live data @ 06:00 UTC)."""
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
- 🟢 Uptime 4d 5h12m (no reboot overnight). Load 1.61/1.20/1.01 🟢 | Mem 7.3Gi/15Gi (8.3Gi avail) 🟢 | Disk 80% | Swap 2.2Gi/29Gi 🟢
- 🟢 Top CPU: openclaw-gateway ~13%, ollama ~13%, temporal-server ~2.5%. No chat_server.py, no train_server.py, no continuous_vision_daemon.py this window (all dropped off since 11-11).
- 🟡 2 FAILED services: certbot, dailyaidecheck (same as 11-11; both recovered/safe but still marked failed).
- 🔴 Email queue STILL STALLED: 59 sent / 148 ready (status now labeled "synthetic") — UNCHANGED from 11-11. Last send still Nov 08 19:30:24 UTC (3+ days, no sends). Campaign capton_hospitality_202607 frozen.
- 🟡 unified.db 405MB (was 371MB on 11-11) — last written Nov 11 18:30 UTC.
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL absent (only idx_enrichment index remains).
- Table counts: unified_leads 1,460 | leads 33,086 (FLAT vs 11-11; scraper pipeline no longer adding) | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 | psd_customer_sales 235 | verified_leads 1 | scrape_runs 4 | email_queue 207

Action items:
1. 🔴 Email queue stalled 3+ days — no sends since Nov 08 19:30. Confirm whether the drain stopped (rate limit, daemon down, or intentional pause) and whether to resume the remaining 148.
2. 🟡 leads flat at 33,086 (was +495/day on 11-11) — scraper pipeline appears to have halted; confirm expected.
3. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
4. 🟡 unified.db grew 371→405MB while lead counts flat — worth a glance at what's writing.

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
