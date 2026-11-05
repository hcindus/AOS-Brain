#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-05 (live data @ 09:40 UTC)."""
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

Key stats (live @ 09:40 UTC):
- Uptime 1d 2h24m. Load 3.01/3.27/3.31 🟢 (post-reboot, down from ~34). Mem 10Gi/15Gi (4.8Gi avail) 🟡 | Disk 79% flat | Swap 8.0Gi/29Gi 🟡 (reset after reboot)
- 🔴 Top CPU: robotics/training_room train_server.py ~147% CPU (RP1 CPU-first training), continuous_vision_daemon.py ~33%, vision_service.py ~24%, ollama runner ~16%, openclaw-gateway ~11.8%
- 🔴 2 FAILED services: certbot, dailyaidecheck (unchanged)
- ✅ unified.db (197MB) updated to Nov 05 06:30 UTC — scraper/daemon writing again (was stuck at Oct 28)
- 🔴 Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time — STILL STALLED since July 2026 (scheduled_at range 2026-07-10 → 07-16, unchanged)
- 🔴 PENDING_TASKS table STILL absent from unified.db (unchanged). Verify CA_SOS scraper DB source.
- ⚠️ enrichment_queue table STILL not found in unified.db (unchanged) — verify enrichment daemon/DB source.
- Table counts: unified_leads 1,460 | leads 32,591 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | verified_leads 1 | scrape_runs 4

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time since July. Needs a decision: set a real SendGrid key, send via verified Hostinger SMTP, or clear.
2. 🟡 train_server.py still ~147% CPU post-reboot. Confirm training run is still intended, or throttle it — biggest CPU headroom candidate.
3. 🔴 PENDING_TASKS table still missing from unified.db — confirm the CA_SOS scraper chain's intended DB and whether the drop was deliberate.
4. ⚠️ enrichment_queue discrepancy — verify which DB/daemon backs DepotChaos enrichment.
5. 🟢 Watch swap: reset to 8.0Gi after reboot; monitor whether it re-creeps toward 12Gi as processes re-ramp.

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
