#!/usr/bin/env python3
"""Daily Queue Email Report - November 21, 2026 (live data @ 09:40 UTC)."""
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
• Uptime:   13 days, 8h53m
• CPU Load: 1.10 / 0.91 / 0.94  🟢 stable
• Memory:   6.0 Gi used / 15 Gi total  🟢
• Available: 9.6 Gi  🟢
• Swap:     5.7 Gi / 29 Gi  🟡 up from 2.7 Gi (11-20)
• Disk:     157G / 193G (82%)  🟡 (was 81% on 11-20)

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control,
aos-vision, depotchaos, depotchaos-tasks, ollama, receptionist,
psd-sales-automation — all ACTIVE.

⚠️ 2 services FAILED — certbot, dailyaidecheck (unchanged, multi-week).

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

• PENDING_TASKS.json:  4,850 tasks
    - source: CA_SOS_Scraper (100% — synthetic/mock leads, do not send)
    - lastUpdated: 2026-11-19 12:24 UTC  🔴 2 days stale (was fresh 11-19)

• DepotChaos DB (data/depot_chaos/unified.db, 122 MB — SHRANK from 715 MB on 11-20):
    - unified_leads:         1,460
    - leads:                33,575
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           636
    - datadepot_intelligence: 77,390  🟢 RESOLVED — down from 1.39M (11-20)

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🟢 RESOLVED
  1. datadepot_intelligence dropped from ~1.39M rows back to 77,390, and
     the DB shrank 715 MB → 122 MB. The unique license_number index
     deduplicated the table (77,390 = exact match to ca_abc_licenses).
     The "runaway growth" flagged in prior reports is cleared — no action
     needed unless you expected a different final count.

🟡 IMPORTANT
  2. Swap climbed to 5.7 Gi (was 2.7 Gi on 11-20). Worth a glance if it
     keeps rising — may just be transient.

  3. Email queue status still "synthetic" for the 148 remaining
     capton_hospitality records. If correct, those stay unsent — please
     confirm intent (no new sends since 11-11).

  4. PENDING_TASKS refresher now 2 days stale (lastUpdated 11-19 12:24).
     Count 4,850 (mock CA_SOS leads; do not send).

  5. 2 services still FAILED — certbot (SSL renewals) + dailyaidecheck.
     Worth a restart/renew pass before certs expire.

  6. Disk at 82% (was 81%). The DB shrink freed ~590 MB, but watch the
     trend.

🟢 NOTE
  7. Load/memory healthy and stable. Sender path working but idle —
     nothing queued to push right now.

All core systems operational. Headline: healthy and stable — the big
datadepot_intelligence growth from the last two weeks has self-resolved
(deduplicated to 77,390 unique records). Standing by.

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
