#!/usr/bin/env python3
"""Daily Queue Email Report - November 23, 2026 (live data @ 09:40 UTC)."""
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
• Uptime:   15 days, 8h52m
• CPU Load: 1.14 / 1.37 / 1.42  🟢 stable (was 1.24/1.43/1.39 on 11-22)
• Memory:   4.4 Gi used / 15 Gi total  🟢
• Available: 11 Gi  🟢
• Swap:     5.8 Gi / 29 Gi  🟡 steady (unchanged from 11-22)
• Disk:     158G / 193G (82%)  🟡 +1G vs yesterday

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

• PENDING_TASKS.json:  4,950 tasks (was 4,900 — +50)
    - source: CA_SOS_Scraper (synthetic/mock leads, do not send)
    - lastUpdated: 2026-11-22 12:23 UTC  🟢 fresh (yesterday)

• DepotChaos DB (data/depot_chaos/unified.db, 78 MB — was 122 MB):
    - unified_leads:         1,460
    - leads:                11,009  ⚠️ was 34,059 on 11-22 (see Action #1)
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           636
    - datadepot_intelligence: 77,390  🟢 (deduped, holding)

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 REVIEW
  1. leads table dropped 34,059 → 11,009 overnight (~-23k) and the DB
     file shrank 122 MB → 78 MB. A split/re-import ran at 2026-11-23
     03:00 UTC (daily_stats: 10,526 total / 10,506 "new", 234 cream).
     Data is preserved in backups:
       • unified.db.bak_pre_split     (127 MB, 11-22 19:01)
       • unified.db.bak_20261120      (711 MB, 11-20 18:08)
     → Please confirm this reset was intentional (dedupe/clean re-import)
     vs. accidental loss. No data is gone — it's in the .bak files.

🟡 WATCH
  2. Swap steady at 5.8 Gi (leveled off since 11-20's 2.7 Gi). Not
     climbing. Glance if it trends up again.

  3. Email queue still "synthetic" for the 148 remaining
     capton_hospitality records. If correct, they stay unsent — please
     confirm intent (no new sends since 11-11).

  4. Disk at 82% (158G, +1G vs yesterday). Watch trend; the two DB
     backups now on disk add ~838 MB. No immediate action.

  5. 2 services still FAILED (unchanged, multi-week) — certbot
     (SSL renewals) + dailyaidecheck. Worth a restart/renew pass before
     certs expire.

🟢 NOTE
  6. PENDING_TASKS refresher back to fresh (11-22 12:23), +50 tasks.
     Load/memory healthy. Sender path working but idle — nothing queued
     to push.

All core systems operational. Headline: healthy and stable, but the
leads table took a ~23k drop overnight via a 03:00 UTC split/re-import —
data is safe in backups, but I need you to confirm that was the plan.
Swap has leveled off; disk crept up 1G. Standing by.

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
