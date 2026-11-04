#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-04 (live data @ 06:12 UTC)."""
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

Key stats (live @ 06:12 UTC):
- Uptime 17d 9h34m. Load 34.18/34.39/35.09 🔴 (sustained high — see action #2). Mem 9Gi/15Gi (5.6Gi avail) 🟡 | Disk 79% flat | Swap 12Gi/29Gi 🟡 (still creeping: 10Gi→11Gi→12Gi across days)
- 🔴 Load drivers: openclaw-gateway ~87% CPU, continuous_vision_daemon.py ~50% CPU, ollama runner ~46% CPU. robotics/training_room train_server.py still running (RP1 CPU-first training, ~2.5d uptime).
- Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026 (unchanged)
- 🔴 PENDING_TASKS table still absent from unified.db (unchanged since 10-28 — table dropped/moved, not just stale). Verify CA_SOS scraper DB source.
- Active unified.db (data/depot_chaos/unified.db, ~131MB, mtime Oct 28 10:06 — unchanged): unified_leads 1,460 | leads 32,590 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | email_queue 207
- ⚠️ enrichment_queue table still not found in unified.db (unchanged) — verify enrichment daemon/DB source.
- 2 FAILED services: certbot, dailyaidecheck (unchanged)

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time. Needs a decision: set a real SendGrid key, send via verified Hostinger SMTP, or clear.
2. 🔴 Sustained high load (~34) + swap creep 10→12Gi. Drivers: gateway ~87% CPU, continuous_vision_daemon ~50%, ollama runner ~46%, plus train_server.py still running. Confirm all CPU-first processes are intended, or throttle (vision daemon + training server are the biggest headroom candidates).
3. 🔴 PENDING_TASKS table still missing from unified.db — confirm the CA_SOS scraper chain's intended DB and whether the drop was deliberate.
4. 🟡 Swap climbing 10Gi→12Gi across days — watch for a memory-hungry process beyond the training server/vision daemon.
5. ⚠️ enrichment_queue discrepancy — verify which DB/daemon backs DepotChaos enrichment.

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
