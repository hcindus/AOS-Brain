#!/usr/bin/env python3
"""Daily Queue Email Report - November 20, 2026 (live data @ 09:40 UTC)."""
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
• Uptime:   12 days, 8h52m
• CPU Load: 1.87 / 1.64 / 1.46  🟢 stable
• Memory:   7.2 Gi used / 15 Gi total  🟢
• Available: 8.4 Gi  🟢
• Swap:     2.7 Gi / 29 Gi  🟢
• Disk:     156G / 193G (81%)  🟡 climbing (was 79% on 10-30)

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control,
aos-vision, depotchaos, depotchaos-tasks, ollama, receptionist,
psd-sales-automation — all ACTIVE.

⚠️ 2 services FAILED — certbot, dailyaidecheck (unchanged, multi-week).

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (data/depot_chaos/unified.db → email_queue):
    207 total — capton_hospitality_202607
    - 59 SENT 🟢 (unchanged since 11-11)
    - 148 "synthetic"  ⚠️ unchanged (do not send — confirm re-label intent)

• datadepot queue:
    - pending_emails.json:   0 (drained)
    - followup_queue:      100
    - sent_emails (all-time): 170

• PENDING_TASKS.json:  4,850 tasks
    - source: CA_SOS_Scraper (100% — synthetic/mock leads, do not send)
    - lastUpdated: 2026-11-19 12:24 UTC  ✅ fresh again (was stale 11-14)

• DepotChaos DB (data/depot_chaos/unified.db, 715 MB — grew from 612 MB on 11-17):
    - unified_leads:         1,460
    - leads:                33,086
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           636
    - datadepot_intelligence: 1,393,020  🔴 up from 1.16M (11-17), 696K (11-11)

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🟡 IMPORTANT
  1. datadepot_intelligence now ~1.39M rows (was 1.16M on 11-17, 696K on
     11-11). Still climbing — DB now 715 MB and disk at 81%. Confirm this
     ingestion is intentional, not a runaway scraper.

  2. Email queue status still "synthetic" for the 148 remaining
     capton_hospitality records. If correct, those stay unsent — please
     confirm intent (no new sends since 11-11).

  3. PENDING_TASKS refresher recovered — lastUpdated 11-19 12:24 UTC
     (was stale 11-14). Count 4,850 (mock CA_SOS leads; do not send).

  4. 2 services still FAILED — certbot (SSL renewals) + dailyaidecheck.
     Worth a restart/renew pass before certs expire.

  5. Disk holding at 81% — driven by DB growth. Watch it.

🟢 NOTE
  6. Load/memory/swap all healthy and stable. Sender path is working but
     idle — nothing queued to push right now.

All core systems operational. Headline: system healthy and stable, but
datadepot_intelligence continues to grow (~1.39M rows) and the "synthetic"
re-label still deserves a Captain's confirmation. Standing by.

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
