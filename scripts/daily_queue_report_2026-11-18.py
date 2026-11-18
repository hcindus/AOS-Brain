#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-18 (live data @ 09:40 UTC)."""
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

Key stats (live @ 09:40 UTC):
- 🟢 Uptime 10d 8h53m (no reboot). Load 1.35/1.14/1.11 🟢 (DOWN from 2.60 yesterday) | Mem 10Gi/15Gi (5.6Gi avail) 🟡 (up from 6.6Gi) | Disk 81% 🟢 (flat) | Swap 2.1Gi/29Gi 🟢 (flat).
- 🟡 Vision daemons STILL hot: python3 ~29.8% + python3 ~23.1% CPU (combined ~52.9%). Unchanged — worth confirming they should run hot.
- 🟡 Top CPU: python3 (vision daemon) 29.8%, python3 (vision_service) 23.1%, openclaw-gateway 16.8%, docker-entrypoint 9.3%, ollama 6.9%.
- 🔴 Email queue STILL STALLED: 59 sent / 148 "synthetic" — UNCHANGED. Last send still Nov 08 19:30:24 UTC (~10 days, no sends). Campaign capton_hospitality_202607 frozen.
- 🟢 unified.db 646MB — last written Nov 18 06:30 UTC (fresh this morning; recovered from yesterday's ~24h stale state).
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL absent (only idx_enrichment index remains).
- Table counts (ALL FLAT vs 11-17): unified_leads 1,460 | leads 33,086 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 | psd_customer_sales 235 | verified_leads 1 | scrape_runs 4 | email_queue 207

Datadepot queue (separate JSON store):
- Pending 0 | Sent 170 (all-time) | Failed 54 | Sent last 24h: 0 | Sent last 7 days: 0

Action items:
1. 🔴 Email queue stalled ~10 days — no sends since Nov 08 19:30. Confirm whether the drain stopped (rate limit, daemon down, or intentional pause) and whether to resume the remaining 148.
2. 🟡 Vision daemons (continuous_vision_daemon.py + vision_service.py) still ~52.9% CPU combined — confirm they should run hot, or throttle.
3. 🟢 Load improved 2.60 → 1.35; memory ticked up to 10Gi (5.6Gi avail). Swap stable at 2.1Gi. No immediate concern.
4. 🟢 unified.db resumed writes this morning (Nov 18 06:30) after going stale yesterday — confirm the scraper/enrichment chain is flowing again.
5. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
6. 🟢 Disk stable at 81%; swap flat. No immediate action.

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
