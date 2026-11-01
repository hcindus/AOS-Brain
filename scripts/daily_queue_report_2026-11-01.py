#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-01 (live data @ 06:00 UTC)."""
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
- Uptime 14d 09h22m. Load 4.74/5.55/5.52 🟡 (eased from yesterday's ~10.4 1-min spike; 5/15-min stable ~5.5). Mem 11Gi/15Gi (3.7Gi avail) 🟡 | Disk 79% flat | Swap 10Gi/29Gi 🟡 (up from 7.5Gi — watch)
- Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026
- PENDING_TASKS: 4,450 (flat; CA_SOS_Scraper mock — do not send); lastUpdated 2026-10-28T11:16 UTC 🔴 4 days stale
- Active unified.db (data/depot_chaos/unified.db, ~131MB, mtime Oct 28 10:06 — unchanged): unified_leads 1,460 | leads 32,590 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | email_queue 207
- ⚠️ enrichment_queue table not found in unified.db (differs from prior reports) — verify enrichment daemon/DB source.
- 2 FAILED services: certbot, dailyaidecheck (unchanged)

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time. Needs a decision: set a real SendGrid key, send via verified Hostinger SMTP, or clear.
2. ⚠️ SendGrid key is a false positive (account closed). Blocked on Captain for a real key — or switch fully to the Hostinger SMTP path already verified for auth emails.
3. 🟡 Swap climbed 7.5Gi → 10Gi. Memory 11Gi/15Gi. Watch for a memory-hungry process; consider pruning idle agents.
4. ⚠️ PENDING_TASKS lastUpdated 4 days stale (10-28) — CA_SOS scraper chain idle; confirm intended state or restore the 6:00 UTC cron.
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
