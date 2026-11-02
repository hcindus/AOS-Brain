#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-02 (live data @ 06:00 UTC)."""
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

Key stats (live @ 06:00 UTC):
- Uptime 15d 9h23m. Load 22.93/27.63/31.71 🔴 (spiked sharply from yesterday's ~4.7/5.5/5.5 — see action #2). Eased to ~9.6/20.4/28.1 by 06:02 (partial spike from the health-check itself, but sustained 15-min still ~28). Mem 10Gi/15Gi (4.8Gi avail) 🟡 | Disk 79% flat | Swap 11Gi/29Gi 🟡 (climbed 10Gi→11Gi — still creeping)
- 🔴 Load driver identified: robotics/training_room train_server.py (RP1 CPU-first training) at ~60% CPU, running 2d 10h. openclaw-gateway ~93% CPU (14h50m uptime).
- Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026 (unchanged)
- 🔴 PENDING_TASKS table NO LONGER EXISTS in unified.db — yesterday it held 4,450 rows (stale since 10-28). New discrepancy: table dropped/moved, not just stale. Verify CA_SOS scraper DB source.
- Active unified.db (data/depot_chaos/unified.db, ~131MB, mtime Oct 28 10:06 — unchanged): unified_leads 1,460 | leads 32,590 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | email_queue 207
- ⚠️ enrichment_queue table still not found in unified.db (unchanged) — verify enrichment daemon/DB source.
- 2 FAILED services: certbot, dailyaidecheck (unchanged)

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time. Needs a decision: set a real SendGrid key, send via verified Hostinger SMTP, or clear.
2. 🔴 Load spike + swap creep — train_server.py (RP1 training room) has run ~60% CPU for 2.4 days and swap is now 11Gi/29Gi. Confirm intended CPU-first training is OK, or throttle/pause to free headroom. This is the biggest change from yesterday.
3. 🔴 PENDING_TASKS table vanished from unified.db (was 4,450 rows) — confirm the CA_SOS scraper chain's intended DB and whether the drop was deliberate.
4. 🟡 Swap climbing 10Gi→11Gi across days — watch for a memory-hungry process beyond the training server.
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
