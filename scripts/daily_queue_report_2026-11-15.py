#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-15 (live data @ 06:00 UTC)."""
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
- 🟢 Uptime 7d 5h12m (no reboot). Load 0.96/0.97/1.03 🟢 | Mem 8.3Gi/15Gi (7.3Gi avail) 🟢 | Disk 80% | Swap 715Mi/29Gi 🟢 (up from 184Mi on 11-14 — minor, still healthy).
- 🟡 Vision daemons STILL hot: continuous_vision_daemon.py ~29.7% + vision_service.py ~23.3% CPU (combined ~53%). Same as 11-13/11-14; worth confirming they should be running hot.
- 🟢 Top CPU: continuous_vision_daemon.py 29.7%, vision_service.py 23.3%, openclaw-gateway 12.7%, ollama 8.1%, temporal-server 2.5%.
- 🔴 Email queue STILL STALLED: 59 sent / 148 "synthetic" — UNCHANGED. Last send still Nov 08 19:30:24 UTC (now ~6.5 days, no sends). Campaign capton_hospitality_202607 frozen.
- 🟡 unified.db 508MB — last written Nov 14 06:30 UTC (now ~24h ago; no new writes in the past day).
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL absent (only idx_enrichment index remains).
- Table counts (ALL FLAT vs 11-14): unified_leads 1,460 | leads 33,086 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 | psd_customer_sales 235 | verified_leads 1 | scrape_runs 4 | email_queue 207

Datadepot queue (separate JSON store):
- Pending 0 | Sent 170 (all-time) | Failed 54 | Follow-up 100
- Sent last 24h: 0 | Sent last 7 days: 0

Action items:
1. 🔴 Email queue stalled 6.5+ days — no sends since Nov 08 19:30. Confirm whether the drain stopped (rate limit, daemon down, or intentional pause) and whether to resume the remaining 148.
2. 🟡 Vision daemons (continuous_vision_daemon.py + vision_service.py) still consuming ~53% CPU combined — confirm they should be running hot, or throttle.
3. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
4. 🟡 unified.db not written in ~24h (last write Nov 14 06:30) while lead counts stayed flat — confirm scrapers/ingest are still scheduled and running.

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
