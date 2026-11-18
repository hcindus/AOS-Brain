#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-18 (live data @ 06:00 UTC)."""
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
- 🟡 Uptime 10d 5h13m (no reboot). Load 2.60/1.96/1.59 🟡 (UP from 1.41 yesterday) | Mem 9.0Gi/15Gi (6.6Gi avail) 🟡 (up from 6.4Gi) | Disk 81% 🟢 (flat) | Swap 2.1Gi/29Gi 🟢 (DOWN from 3.0Gi).
- 🟡 Vision daemons STILL hot: continuous_vision_daemon.py ~29.7% + vision_service.py ~23.1% CPU (combined ~52.8%). Unchanged — worth confirming they should run hot.
- 🟡 Top CPU: continuous_vision_daemon.py 29.7%, vision_service.py 23.1%, openclaw-gateway 17.9%, ollama 9.2%, temporal-server 2.5%.
- 🔴 Email queue STILL STALLED: 59 sent / 148 "synthetic" — UNCHANGED. Last send still Nov 08 19:30:24 UTC (now ~10 days, no sends). Campaign capton_hospitality_202607 frozen.
- 🟡 unified.db 583MB (flat vs 11-17) — last written Nov 17 06:30 UTC (~24h ago; resumed briefly on 11-17 then went stale again).
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL absent (only idx_enrichment index remains).
- Table counts (ALL FLAT vs 11-17): unified_leads 1,460 | leads 33,086 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 | psd_customer_sales 235 | verified_leads 1 | scrape_runs 4 | email_queue 207

Datadepot queue (separate JSON store):
- Pending 0 | Sent 170 (all-time) | Failed 54 | Sent last 24h: 0 | Sent last 7 days: 0

Action items:
1. 🔴 Email queue stalled ~10 days — no sends since Nov 08 19:30. Confirm whether the drain stopped (rate limit, daemon down, or intentional pause) and whether to resume the remaining 148.
2. 🟡 Vision daemons (continuous_vision_daemon.py + vision_service.py) still ~52.8% CPU combined — confirm they should run hot, or throttle.
3. 🟡 Load ticked up 1.41 → 2.60 and memory 6.4Gi → 9.0Gi — mild, but watch alongside the hot vision daemons.
4. 🟡 unified.db went stale again (last write Nov 17 06:30, ~24h). Track whether the scraper/enrichment chain has stalled upstream.
5. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
6. ✅ Swap improved 3.0Gi → 2.1Gi; disk stable at 81%. No immediate action.

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
