#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-17 (live data @ 06:00 UTC)."""
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
- 🟢 Uptime 9d 5h12m (no reboot). Load 1.41/1.35/1.27 🟢 | Mem 6.4Gi/15Gi (9.2Gi avail) 🟢 | Disk 81% 🟢 (DOWN from 85% on 11-16 — freed ~5G this morning) | Swap 3.0Gi/29Gi 🟡 (up from 1.6Gi on 11-16).
- 🟡 Vision daemons STILL hot: continuous_vision_daemon.py ~29.5% + vision_service.py ~22.9% CPU (combined ~52.4%). Unchanged from prior days; worth confirming they should be running hot.
- 🟢 Top CPU: continuous_vision_daemon.py 29.5%, vision_service.py 22.9%, openclaw-gateway 12.0%, ollama 7.4%, complete_brain_v45.py 6.0%.
- 🔴 Email queue STILL STALLED: 59 sent / 148 "synthetic" — UNCHANGED. Last send still Nov 08 19:30:24 UTC (now ~8.5 days, no sends). Campaign capton_hospitality_202607 frozen.
- 🟡 unified.db 577MB (flat vs 11-16) — last written Nov 16 06:30 UTC (~24h ago; went stale again after 11-15's brief resume).
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL absent (only idx_enrichment index remains).
- Table counts (ALL FLAT vs 11-16): unified_leads 1,460 | leads 33,086 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 | psd_customer_sales 235 | verified_leads 1 | scrape_runs 4 | email_queue 207

Datadepot queue (separate JSON store):
- Pending 0 | Sent 170 (all-time) | Failed 54 | Follow-up 100
- Sent last 24h: 0 | Sent last 7 days: 0

Action items:
1. 🔴 Email queue stalled ~8.5 days — no sends since Nov 08 19:30. Confirm whether the drain stopped (rate limit, daemon down, or intentional pause) and whether to resume the remaining 148.
2. 🟡 Vision daemons (continuous_vision_daemon.py + vision_service.py) still ~52.4% CPU combined — confirm they should be running hot, or throttle.
3. 🟡 Swap climbed 1.6Gi → 3.0Gi — mild, still healthy, but trending up; watch alongside memory pressure.
4. 🟡 unified.db went stale again (last write Nov 16 06:30, ~24h). Track whether the scraper/enrichment chain has stalled upstream.
5. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
6. ✅ Disk improved 85% → 81% (cleanup done 11-17 ~04:10: journal vacuum + BHSI/Intestines/enrichment log truncation + pip cache purge). No immediate action, but keep an eye on log growth (BHSI/Intestines logs regrow ~1G+/week).

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
