#!/usr/bin/env python3
"""Daily Queue Email Report - November 22, 2026 (live data @ 09:40 UTC)."""
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
EMAIL = "miles@myl0nr0s.cloud"
PASSWORD = "Myl0n.R0s"
RECIPIENT = "Antonio.hudnall@gmail.com"

now = datetime.utcnow()
subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')} (09:40 UTC)"

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')} (09:40 UTC).

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   14 days, 8h52m
• CPU Load: 1.24 / 1.43 / 1.39  🟢 stable (was 1.10/0.91/0.94 on 11-21)
• Memory:   4.5 Gi used / 15 Gi total  🟢
• Available: 11 Gi  🟢
• Swap:     5.8 Gi / 29 Gi  🟡 steady (was 5.7 Gi on 11-21)
• Disk:     157G / 193G (82%)  🟡 unchanged

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (data/depot_chaos/unified.db → email_queue):
    207 total — capton_hospitality_202607
    - 59 SENT 🟢 (unchanged)
    - 148 "synthetic"  ⚠️ unchanged (do not send — confirm re-label intent)

• datadepot queue:
    - pending_emails.json:   0 (drained)
    - followup_queue:      100
    - sent_emails (all-time): 170

• PENDING_TASKS.json:  4,900 tasks
    - source: CA_SOS_Scraper (synthetic/mock leads, do not send)
    - lastUpdated: 2026-11-21 12:23 UTC  🟢 fresh (yesterday)

• DepotChaos DB (data/depot_chaos/unified.db, 122 MB — unchanged):
    - unified_leads:         1,460
    - leads:                34,059  (was 33,575 on 11-21)
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           636
    - datadepot_intelligence: 77,390  🟢 (deduped, holding)

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🟡 WATCH
  1. Swap holding at 5.8 Gi (was 2.7 Gi on 11-20, now steady 5.7→5.8).
     Not climbing — likely stabilized. Glance if it trends up again.

  2. leads table ticked up 33,575 → 34,059 (+484 since 11-21). Confirm
     the source is expected (new lead ingestion) vs. stray duplication.

  3. Email queue still "synthetic" for the 148 remaining
     capton_hospitality records. If correct, they stay unsent — please
     confirm intent (no new sends since 11-11).

  4. Disk holding at 82% (stable after last week's DB shrink). Watch
     trend; no immediate action.

  5. 2 services still FAILED (unchanged, multi-week) — certbot
     (SSL renewals) + dailyaidecheck. Worth a restart/renew pass before
     certs expire.

🟢 NOTE
  6. PENDING_TASKS refresher back to fresh (11-21 12:23). Load/memory
     healthy. Sender path working but idle — nothing queued to push.

All core systems operational. Headline: healthy and stable — datadepot
dedupe has held, swap has leveled off, and the only real movement is a
+484 bump in the leads table worth a quick source check. Standing by.

— Miles 🚀
Autonomous Operations Engine
Performance Supply Depot LLC / AGI Company
"""

msg = MIMEMultipart()
msg['From'] = EMAIL
msg['To'] = RECIPIENT
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

ctx = ssl.create_default_context()
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as s:
    s.ehlo()
    s.starttls(context=ctx)
    s.ehlo()
    s.login(EMAIL, PASSWORD)
    s.sendmail(EMAIL, RECIPIENT, msg.as_string())

print("SENT to", RECIPIENT, "|", subject)
