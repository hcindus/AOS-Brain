#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-28 (live data @ 11:41 UTC)."""
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

Key stats (live @ 11:41 UTC):
- Uptime 10d 15h02m. Load 13.71/13.06/11.60 🔴 (5/15-min RISING 11.46→13.06 / 9.99→11.60 vs this morning — sustained load climbing; 1-min dipped slightly 14.06→13.71). Mem 9.8Gi/15Gi (5.9Gi avail) 🟡 (up from 8.8Gi this AM) | Disk 79% | Swap 8.7Gi/29Gi 🟡 (up from 8.0Gi)
- Email queue (email_queue): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026
- DepotChaos enrichment_queue (DepotChaos/enrichment_queue/queue.db): 1,000 "available", 0 claimed/completed ⚠️ enrichment daemon idle
- ⚠️ SendGrid still NOT truly configured — api_key field holds literal "${{SENDGRID_API_KEY}}" placeholder, never resolved. 0 sent today.
- ⚠️ PENDING_TASKS table is now GONE from unified.db (was 4,400 CA_SOS mock). Replaced by scrape_runs table (4 old rows, last 2026-05-07). CA_SOS v3 log at /var/log/aos/ca_sos_scraper_v3.log does NOT exist — scraper has not been producing.
- Active unified.db (data/depot_chaos/unified.db, 125MB, mtime Oct 28 10:06): unified_leads 1,460 | leads 32,590 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 502 | psd_customer_sales 503 | datadepot_intelligence 77,390 | address_crossref 3,535 | verified_leads 1 | email_queue 207
- ⚠️ datadepot/unified.db + root unified.db still 0 bytes (truncated) — active DB lives at data/depot_chaos/unified.db
- 2 FAILED services: certbot, dailyaidecheck (unchanged)

Action items:
1. 🔴 Email queue STILL stalled — 207 ready (capton_hospitality_202607), 0 sent all-time. Needs a decision: set a real SendGrid key, send, or clear.
2. ⚠️ SendGrid key is a false positive — holds literal "${{SENDGRID_API_KEY}}" placeholder. Blocked on Captain for a real key.
3. 🔴 Load average climbing — 5/15-min now ~13.06/11.60 and memory up to 9.8Gi. Check `top`/`htop` for a sustained load source before it saturates.
4. ⚠️ DepotChaos enrichment_queue: 1,000 "available", 0 claimed — daemon appears idle; restart/verify the enrichment worker.
5. ⚠️ CA_SOS scraper chain broken — pending_tasks table removed and v3 log missing. Confirm intended state or restore the 6:00 UTC cron (scripts/ca_sos_daily.sh → AGI_COMPANY/.../ca_sos_scraper_v3.py).

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
