#!/usr/bin/env python3
"""Daily Queue Report — 2026-10-16 (live data)."""
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

Key stats (live @ {ts}):
- Uptime 150d 2h47m | Load 2.02/2.29/2.33 🟢 back to baseline (~2.2) | Mem 10Gi/15Gi (5.0Gi avail) 🟢 | Disk 76%
- Swap 2.4Gi/29Gi
- Email queue (email_queue table): 207 "ready" (capton_hospitality_202607), 0 sent all-time 🔴 STILL STALLED since July 2026
- DepotChaos enrichment_queue: 1000 available, 0 pending (no SendGrid configured)
- PENDING_TASKS: 4,050 (all CA_SOS_Scraper mock leads — do NOT send); lastUpdated 10-16 11:15 UTC ✅ fresh (was 4,000 — +50 new)
- Active unified.db (data/depot_chaos/unified.db, 94.3MB): unified_leads 1,460 | leads 32,588 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 501 | psd_customer_sales 503 | datadepot_intelligence 74,518 | address_crossref 3,535 | email_queue 207 | verified_leads 1
- ⚠️ datadepot/unified.db still 0 bytes (truncated Oct 3) — active DB at data/depot_chaos/unified.db
- 3 FAILED services: aos-ternary, certbot, dailyaidecheck

Action items:
1. 🔴 Email queue still stalled — 207 ready (capton_hospitality_202607) never sent. Needs a decision: send or clear.
2. 🟡 Load back to normal (2.02) after being elevated (~4.4) earlier this week.
3. 3 failed services (aos-ternary, certbot, dailyaidecheck) still down.
4. Confirm intended location of unified.db — datadepot/ copy truncated to 0 bytes since Oct 3.

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
