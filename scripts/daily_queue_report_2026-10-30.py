#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-30 (live data @ 06:01 UTC)."""
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

Key stats (live @ 06:01 UTC):
- Uptime 12d 09h22m. Load 10.36/6.69/6.40 🟡 (1-min spiked to ~10.4, but 5/15-min easing ~6.4-6.7 — watch for a sustained source). Mem 12Gi/15Gi (3.5Gi avail) 🟡 | Disk 79% | Swap 7.5Gi/29Gi 🟡 (down from 7.9Gi yesterday)
- Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026
- DepotChaos enrichment_queue (enrichment_queue table): 1,000 "available", 0 claimed/completed ⚠️ enrichment daemon idle
- ⚠️ SendGrid still NOT truly configured — placeholder key / account closed. 0 sent today.
- ⚠️ CA_SOS scraper chain idle — scrape_runs last 2026-05-07 (4 old rows, all WA/OR/TX).
- Active unified.db (data/depot_chaos/unified.db, ~125MB, mtime Oct 28 10:06 — unchanged): unified_leads 1,460 | leads 32,590 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | email_queue 207
- 2 FAILED services: certbot, dailyaidecheck (unchanged)

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time. Needs a decision: set a real SendGrid key, send via verified Hostinger SMTP, or clear.
2. ⚠️ SendGrid key is a false positive (account closed). Blocked on Captain for a real key — or switch fully to the Hostinger SMTP path already verified for auth emails.
3. 🟡 Load 1-min spike ~10.4 (easing on 5/15-min). Check `top`/`htop` for a sustained source if it climbs again.
4. ⚠️ DepotChaos enrichment_queue: 1,000 "available", 0 claimed — daemon idle; restart/verify the enrichment worker.
5. ⚠️ CA_SOS scraper chain idle — scrape_runs last 2026-05-07. Confirm intended state or restore the 6:00 UTC cron.

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
