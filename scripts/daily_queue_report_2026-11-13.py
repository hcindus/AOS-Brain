#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-13 (live data @ 06:00 UTC)."""
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
- 🟢 Uptime 5d 5h13m (no reboot overnight). Load 1.64/1.16/1.00 🟢 | Mem 4.1Gi/15Gi (11Gi avail) 🟢 | Disk 80% | Swap 4.1Gi/29Gi 🟡 (up from 2.2Gi on 11-12).
- 🟡 Vision daemons REAPPEARED: continuous_vision_daemon.py ~31% CPU + vision_service.py ~24% CPU (combined ~55%). Both running since boot 5d ago; 11-12 report had noted these as "dropped off." Worth confirming they should be hot.
- 🟢 Top CPU: continuous_vision_daemon.py 31.4%, vision_service.py 23.8%, ollama 11.8%, openclaw-gateway 11.3%, temporal-server 2.5%.
- 🟡 2 FAILED services: certbot, dailyaidecheck (same as prior days; both recovered/safe but still marked failed).
- 🔴 Email queue STILL STALLED: 59 sent / 148 "synthetic" — UNCHANGED. Last send still Nov 08 19:30:24 UTC (now 4+ days, no sends). Campaign capton_hospitality_202607 frozen.
- 🟡 unified.db 419MB (was 405MB on 11-11) — last written Nov 12 06:30 UTC (~23h ago).
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL absent (only idx_enrichment index remains).
- Table counts (ALL FLAT vs 11-12): unified_leads 1,460 | leads 33,086 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 | psd_customer_sales 235 | verified_leads 1 | scrape_runs 4 | email_queue 207

Action items:
1. 🔴 Email queue stalled 4+ days — no sends since Nov 08 19:30. Confirm whether the drain stopped (rate limit, daemon down, or intentional pause) and whether to resume the remaining 148.
2. 🟡 Vision daemons (continuous_vision_daemon.py + vision_service.py) are consuming ~55% CPU combined — confirm they should be running hot, or they may need throttling.
3. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
4. 🟡 unified.db grew 405→419MB while lead counts flat; last write Nov 12 06:30 — worth a glance at what's writing (and whether it stopped).

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
