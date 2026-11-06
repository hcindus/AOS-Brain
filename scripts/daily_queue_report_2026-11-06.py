#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-06 (live data @ 06:02 UTC)."""
import smtplib, ssl, os, sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
FROM = "miles@myl0nr0s.cloud"
TO = "antonio.hudnall@gmail.com"
PASS = os.environ.get("HOSTINGER_SMTP_PASS") or os.environ.get("SMTP_PASS") or "Myl0n.R0s"

now = datetime.utcnow()
date_str = now.strftime("%B %d, %Y")
ts = now.strftime("%Y-%m-%d %H:%M UTC")

report = f"""📊 Daily Queue Report — {date_str}
Generated: {ts}

Key stats (live @ 06:02 UTC):
- Uptime 1d 22h45m. Load 10.58/7.22/6.65 🔴 (re-ramping, was ~3 post-reboot). Mem 11Gi/15Gi (4.2Gi avail) 🟡 | Disk 79% flat | Swap 8.0Gi/29Gi 🟡 (stable since reboot)
- 🔴 Top CPU: robotics/training_room train_server.py ~132% CPU, continuous_vision_daemon.py ~39%, openclaw-gateway ~36%, ollama runner ~31%, vision_service.py ~27.6%
- 🔴 2 FAILED services: certbot, dailyaidecheck (unchanged)
- 🔴 unified.db (197MB) NOT updated since Nov 05 06:30 UTC — scraper/daemon stalled again after a single write cycle (was stuck at Oct 28 before)
- 🔴 Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time — STILL STALLED since July 2026 (scheduled_at range 2026-07-10 → 07-16, unchanged)
- 🔴 PENDING_TASKS table STILL absent from unified.db (unchanged). Verify CA_SOS scraper DB source.
- ⚠️ enrichment_queue table STILL not found in unified.db (unchanged) — verify enrichment daemon/DB source.
- Table counts: unified_leads 1,460 | leads 32,591 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | verified_leads 1 | scrape_runs 4

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time since July. Needs a decision: set a real SendGrid key, send via verified Hostinger SMTP, or clear.
2. 🔴 CPU load re-ramping 3 → 10.6 in ~1 day post-reboot. train_server.py (~132%) is the biggest headroom candidate — confirm RP1 training is still intended or throttle it.
3. 🔴 unified.db write stalled again (last write Nov 05 06:30). Confirm CA_SOS scraper/daemon health — it wrote once then stopped.
4. 🔴 PENDING_TASKS table still missing from unified.db — confirm the CA_SOS scraper chain's intended DB.
5. 🟡 Watch swap (8.0Gi) — monitor re-creep toward 12Gi as processes ramp.

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
