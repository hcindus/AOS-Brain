#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-29 (live data @ 06:01 UTC)."""
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
- Uptime 11d 09h23m. Load 8.74/7.89/7.53 🟡 (elevated but easing vs yesterday's ~13.7; 1-min above 5/15-min — watch for a sustained source). Mem 9.0Gi/15Gi (6.7Gi avail) 🟡 | Disk 79% | Swap 7.9Gi/29Gi 🟡 (down from 8.7Gi yesterday)
- Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026
- DepotChaos enrichment_queue (DepotChaos/enrichment_queue/queue.db): 1,000 "available", 0 claimed/completed ⚠️ enrichment daemon idle
- ⚠️ SendGrid still NOT truly configured — systemd depotchaos.service holds literal "${{SENDGRID_API_KEY}}" placeholder; auth-system .env notes "EXPIRED — SendGrid account closed". 0 sent today.
- ⚠️ PENDING_TASKS table absent from unified.db (replaced by scrape_runs: 4 old rows, last 2026-05-07). CA_SOS v3 log not producing — scraper chain idle.
- Active unified.db (data/depot_chaos/unified.db, ~125MB, mtime Oct 28 10:06 — unchanged since yesterday): unified_leads 1,460 | leads 32,590 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | datadepot_intelligence 77,390 | address_crossref 3,535 | verified_leads 1 | email_queue 207
- ⚠️ datadepot/unified.db + root unified.db still 0 bytes (truncated) — active DB lives at data/depot_chaos/unified.db
- 2 FAILED services: certbot, dailyaidecheck (unchanged)

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time. Needs a decision: set a real SendGrid key, send, or clear.
2. ⚠️ SendGrid key is a false positive — placeholder "${{SENDGRID_API_KEY}}" (account closed). Blocked on Captain for a real key (or switch to verified Hostinger SMTP path already working for auth emails).
3. 🟡 Load average elevated (~8.7) though easing from yesterday. Check `top`/`htop` for a sustained load source if it climbs again.
4. ⚠️ DepotChaos enrichment_queue: 1,000 "available", 0 claimed — daemon idle; restart/verify the enrichment worker.
5. ⚠️ CA_SOS scraper chain idle — scrape_runs last 2026-05-07, v3 log missing. Confirm intended state or restore the 6:00 UTC cron.

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
