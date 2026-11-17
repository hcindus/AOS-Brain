#!/usr/bin/env python3
"""Daily Queue Email Report - November 17, 2026 (live data @ 09:40 UTC)."""
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
• Uptime:   9 days, 8h53m
• CPU Load: 1.40 / 1.41 / 1.39  🟢 stable
• Memory:   7.6 Gi used / 15 Gi total  🟢
• Available: 8.0 Gi  🟢
• Swap:     3.2 Gi / 29 Gi  🟢
• Disk:     155G / 193G (81%)  🟡 climbing (was 79% on 10-30)

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control,
depotchaos, ollama — all ACTIVE.

⚠️ 2 services FAILED — certbot, dailyaidecheck (unchanged, multi-week).

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (data/depot_chaos/unified.db → email_queue):
    207 total — capton_hospitality_202607
    - 59 SENT 🟢 (unchanged since 11-11)
    - 148 "synthetic"  ⚠️ NOTE: status flipped from "ready" → "synthetic"
      (were labeled "ready" for months; now flagged synthetic. Do not send.)

• datadepot queue:
    - pending_emails.json:   0 (drained)
    - followup_queue:      100
    - sent_emails (all-time): 170

• PENDING_TASKS.json:  4,750 tasks
    - source: CA_SOS_Scraper (100% — synthetic/mock leads, do not send)
    - lastUpdated: 2026-11-14 12:23 UTC  🔴 3 days stale

• DepotChaos DB (data/depot_chaos/unified.db, 612 MB — grew from 405 MB):
    - unified_leads:         1,460
    - leads:                33,086
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           636
    - psd_customer_sales:      235
    - datadepot_intelligence: 1,160,850  🔴 up from 696,510 (11-11)

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🟡 IMPORTANT
  1. datadepot_intelligence jumped to ~1.16M rows (was 696K on 11-11, 77K
     in Oct). Confirm the ingestion is intentional, not a runaway scraper
     — DB now 612 MB and disk at 81%.

  2. Email queue status changed from "ready" to "synthetic" for the 148
     remaining capton_hospitality records. If that re-label is correct,
     those should NOT be sent — please confirm intent.

  3. PENDING_TASKS refresher stale again — lastUpdated 11-14 12:23 UTC
     (3 days). Count 4,750 (mock CA_SOS leads; do not send).

  4. 2 services still FAILED — certbot (SSL renewals) + dailyaidecheck.
     Worth a restart/renew pass before certs expire.

  5. Disk creeping up (79% → 81%) — driven by DB growth. Watch it.

🟢 NOTE
  6. Load/memory/swap all healthy and stable. 59 of 207 email-queue
     records remain sent (no new sends since 11-11) — sender path is
     working but idle; nothing queued to push right now.

All core systems operational. Headline: system is healthy and stable, but
two data-growth items (datadepot_intelligence 1.16M rows, disk 81%) and
the "synthetic" re-label deserve a Captain's look. Standing by.

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
