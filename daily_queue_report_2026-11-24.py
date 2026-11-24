#!/usr/bin/env python3
"""Daily Queue Email Report - November 24, 2026 (live data @ 09:40 UTC)."""
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

════════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════════
• Uptime:   16 days, 8h53m
• CPU Load: 1.30 / 1.33 / 1.27  🟢 stable (was 1.14/1.37/1.42 on 11-23)
• Memory:   6.7 Gi used / 15 Gi total  🟢
• Available: 9.0 Gi  🟢
• Swap:     5.6 Gi / 29 Gi  🟡 steady (was 5.8 Gi)
• Disk:     158G / 193G (82%)  🟡 flat (unchanged)

════════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════════
• Email queue (data/depot_chaos/unified.db → email_queue):
    207 total — capton_hospitality_202607
    - 59 SENT 🟢 (unchanged)
    - 148 "synthetic"  ⚠️ unchanged (do not send — confirm re-label intent)

• datadepot queue:
    - pending_emails.json:   0 (drained)
    - followup_queue:      100
    - sent_emails (all-time): 170

• PENDING_TASKS.json:  5,000 tasks (was 4,950 — +50)
    - source: CA_SOS_Scraper (synthetic/mock leads, do not send)
    - lastUpdated: 2026-11-23 12:23 UTC  🟢 fresh (yesterday)

• DepotChaos DB (data/depot_chaos/unified.db, 78 MB — flat):
    - unified_leads:         1,460
    - leads:                11,732  🟢 was 11,009 on 11-23 (+723)
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           636
    - datadepot_intelligence: 77,390  🟢 (deduped, holding)

════════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════════
🟡 WATCH
  1. leads table recovered slightly (11,009 → 11,732, +723) since the
     11-23 03:00 UTC split/re-import. No further drop — the reset looks
     to be holding. Still awaiting your confirmation that it was
     intentional (data preserved in unified.db.bak_pre_split / .bak_20261120).

  2. Email queue still "synthetic" for the 148 remaining
     capton_hospitality records — no sends since 11-11. If correct, they
     stay unsent; please confirm intent.

  3. Swap steady at 5.6 Gi (leveled off). Disk flat at 82%. No movement
     today — nothing urgent.

  4. 2 services still FAILED (unchanged, multi-week) — certbot
     (SSL renewals) + dailyaidecheck. Worth a restart/renew pass before
     certs expire.

🟢 NOTE
  5. PENDING_TASKS +50 (5,000 total), refresher fresh at 11-23 12:23.
     Load/memory healthy. Sender path working but idle — nothing queued
     to push.

All core systems operational. Headline: healthy and stable. The leads
table is climbing back up after yesterday's split (+723) rather than
dropping further, so the reset appears to be holding — but I still need
your confirmation that the re-import was the plan. Swap and disk are
flat; only certbot + dailyaidecheck remain as the standing failed
services. Standing by.

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
