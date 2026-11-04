#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-04 (fresh live data)."""
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

Key stats (live snapshot):
- Uptime 2h24m (host rebooted ~07:16 UTC today). Load 3.26/2.72/2.78 🟢 (post-reboot, down from ~34). Mem 10Gi/15Gi (5.3Gi avail) 🟡 | Disk 79% flat | Swap 7.9Gi/29Gi 🟡 (reset after reboot; was 12Gi pre-reboot)
- 🔴 Top CPU: robotics/training_room train_server.py ~145% CPU, continuous_vision_daemon.py ~33%, vision_service.py ~24%, ollama runner ~31%, openclaw-gateway ~8.6%
- ✅ 0 failed services (certbot + dailyaidecheck both recovered after reboot)
- ✅ unified.db updated to Nov 04 09:00 UTC (was stuck at Oct 28) — scraper/daemon writing again
- 🔴 Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time — STILL STALLED since July 2026 (unchanged)
- 🔴 PENDING_TASKS table STILL absent from unified.db (unchanged — dropped/moved, not just stale). Verify CA_SOS scraper DB source.
- ⚠️ enrichment_queue table STILL not found in unified.db (unchanged) — verify enrichment daemon/DB source.

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time. Needs a decision: set a real SendGrid key, send via verified Hostinger SMTP, or clear.
2. 🟡 train_server.py still at ~145% CPU post-reboot (robotics RP1 CPU-first training, ~2.5d wall-clock before reboot). Confirm training run is still intended, or throttle it — it's the single biggest CPU headroom candidate.
3. 🔴 PENDING_TASKS table still missing — confirm the CA_SOS scraper chain's intended DB and whether the drop was deliberate.
4. ⚠️ enrichment_queue discrepancy — verify which DB/daemon backs DepotChaos enrichment.
5. 🟢 Watch swap: reset to 7.9Gi after reboot; monitor whether it re-creeps toward 12Gi+ as processes re-ramp.

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
