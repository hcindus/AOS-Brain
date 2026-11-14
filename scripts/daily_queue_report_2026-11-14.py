#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-14 (live data @ 09:41 UTC)."""
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

Key stats (live @ 09:41 UTC):
- 🟢 Uptime 6d 8h53m (no reboot). Load 1.72/1.48/1.24 🟡 | Mem 10Gi/15Gi (5.1Gi avail) 🟡 | Disk 80% | Swap 184Mi/29Gi 🟢 (down sharply from 4.1Gi on 11-13 — swap cleared).
- 🟡 Vision daemons STILL hot: continuous_vision_daemon.py ~30.5% + vision_service.py ~23.7% CPU (combined ~54%). Same as 11-13; worth confirming they should be running hot.
- 🟢 Top CPU: continuous_vision_daemon.py 30.5%, vision_service.py 23.7%, ollama 21.8%, openclaw-gateway 14.4%, temporal-server 2.5%.
- 🔴 Email queue STILL STALLED: 59 sent / 148 "synthetic" — UNCHANGED. Last send still Nov 08 19:30:24 UTC (now ~5.5 days, no sends). Campaign capton_hospitality_202607 frozen.
- 🟡 unified.db 508MB (was 419MB on 11-13) — last written Nov 14 06:30 UTC (~3h ago; still writing).
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL absent (only idx_enrichment index remains).
- Table counts (ALL FLAT vs 11-13): unified_leads 1,460 | leads 33,086 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 | psd_customer_sales 235 | verified_leads 1 | scrape_runs 4 | email_queue 207

Datadepot queue (separate JSON store):
- Pending 0 | Sent 170 (all-time) | Failed 54 | Follow-up 100
- Sent last 24h: 0 | Sent last 7 days: 0

Action items:
1. 🔴 Email queue stalled 5.5+ days — no sends since Nov 08 19:30. Confirm whether the drain stopped (rate limit, daemon down, or intentional pause) and whether to resume the remaining 148.
2. 🟡 Vision daemons (continuous_vision_daemon.py + vision_service.py) still consuming ~54% CPU combined — confirm they should be running hot, or throttle.
3. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
4. 🟡 unified.db grew 419→508MB in ~2 days while lead counts stayed flat — worth checking what's writing (last write Nov 14 06:30).

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
