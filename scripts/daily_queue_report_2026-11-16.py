#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-16 (live data @ 09:40 UTC)."""
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
- 🟢 Uptime 8d 8h53m (no reboot). Load 0.76/0.95/1.02 🟢 | Mem 8.4Gi/15Gi (7.2Gi avail) 🟢 | Disk 85% 🟡 (UP from 80% on 11-15 — 5% in a day) | Swap 1.6Gi/29Gi 🟡 (up from 715Mi on 11-15).
- 🟡 Vision daemons STILL hot: continuous_vision_daemon.py ~29.5% + vision_service.py ~23.0% CPU (combined ~52.5%). Same as prior days; worth confirming they should be running hot.
- 🟢 Top CPU: continuous_vision_daemon.py 29.5%, vision_service.py 23.0%, openclaw-gateway 12.6%, ollama 7.2%, complete_brain_v45.py 4.4%.
- 🔴 Email queue STILL STALLED: 59 sent / 148 "synthetic" — UNCHANGED. Last send still Nov 08 19:30:24 UTC (now ~8 days, no sends). Campaign capton_hospitality_202607 frozen.
- 🟢 unified.db 577MB (up from 508MB on 11-15) — last written Nov 16 06:30 UTC (~3h ago; writes resumed vs. 11-15's stale state).
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL absent (only idx_enrichment index remains).
- Table counts (ALL FLAT vs 11-15): unified_leads 1,460 | leads 33,086 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 | psd_customer_sales 235 | verified_leads 1 | scrape_runs 4 | email_queue 207

Datadepot queue (separate JSON store):
- Pending 0 | Sent 170 (all-time) | Failed 54 | Follow-up 100
- Sent last 24h: 0 | Sent last 7 days: 0

Action items:
1. 🔴 Email queue stalled ~8 days — no sends since Nov 08 19:30. Confirm whether the drain stopped (rate limit, daemon down, or intentional pause) and whether to resume the remaining 148.
2. 🟡 Disk jumped 80% → 85% in a day (now 163G/193G used). Identify what's consuming space before it hits critical; unified.db alone is 577MB.
3. 🟡 Vision daemons (continuous_vision_daemon.py + vision_service.py) still ~52.5% CPU combined — confirm they should be running hot, or throttle.
4. 🟡 Swap climbed 715Mi → 1.6Gi — mild, still healthy, but trending up; watch alongside memory pressure.
5. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.

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
