#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-07 (live data @ 09:41 UTC)."""
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

Key stats (live @ 09:41 UTC):
- Uptime 3d 2h24m. Load 3.87/5.59/7.66 🟡 (DOWN from 9.01 yesterday — good). Mem 8.2Gi/15Gi (7.4Gi avail) 🟢 improved | Disk 79% flat | Swap 9.3Gi/29Gi 🟡 (still creeping: 8.0 → 8.8 → 9.3)
- 🔴 Top CPU: robotics/training_room train_server.py ~110% CPU (unchanged), ollama runner ~54%, continuous_vision_daemon ~46%, openclaw-gateway ~39%, vision_service ~31%
- 🔴 2 FAILED services: certbot, dailyaidecheck (unchanged)
- 🟡 unified.db now 265MB (was 231MB yesterday) — wrote again ~once/day (last Nov 07 06:30 UTC) then stalled; single-cycle-then-stop pattern persists
- 🔴 Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time — STILL STALLED since July 2026
- 🔴 PENDING_TASKS table STILL absent from unified.db (unchanged) — verify CA_SOS scraper DB source.
- ⚠️ enrichment_queue table STILL not found in unified.db (unchanged).
- Table counts: unified_leads 1,460 | leads 32,591 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | verified_leads 1 | scrape_runs 4

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time since July. Needs a decision: set a real SendGrid key, send via verified Hostinger SMTP sender, or clear.
2. 🔴 train_server.py (~110%) remains the top CPU driver — confirm RP1 training is still intended or throttle it.
3. 🟡 unified.db write pattern = ~once/day then stall (now 265MB). Investigate cron/loop schedule for the scraper/daemon.
4. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
5. 🟡 Swap creeping (9.3Gi) — monitor re-creep toward 12Gi despite improved CPU load.

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
