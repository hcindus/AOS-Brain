#!/usr/bin/env python3
"""Daily Queue Email Report - November 27, 2026 (live data @ 09:41 UTC)."""
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
subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')} (09:41 UTC)"

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')} (09:41 UTC).

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════════
• Uptime:   19 days, 8h53m
• CPU Load: 1.06 / 1.28 / 1.25  🟢 settled (was 1.56/1.69/1.61 on 11-26)
• Memory:   7.2 Gi used / 15 Gi total  🟢
• Available: 8.4 Gi  🟢
• Swap:     5.0 Gi / 29 Gi  🟢 steady
• Disk:     158G / 193G (82%)  🟡 unchanged

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
    - failed_emails:         54  ⚠️ (bounced/undeliverable backlog)

• PENDING_TASKS.json:  5,150 tasks  (was 5,100 on 11-26 — +50)
    - source: CA_SOS_Scraper (synthetic/mock leads, do not send)
    - lastUpdated: 2026-11-26 12:23 UTC  🟢 fresh (yesterday)

════════════════════════════════════════════════
  DepotChaos — LIVE vs DEMO split (active since 11-22 18:58 UTC)
════════════════════════════════════════════════
LIVE data/depot_chaos/unified.db:
    - unified_leads:         1,460
    - leads:                13,142  (was 12,671 on 11-26 → +471 real)
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           636
    - datadepot_intelligence: 77,390  🟢 (deduped, holding)

LIVE DepotChaos/depot_chaos.db (canonical CRM):
    - vendors:               34,459  (was 34,011 on 11-26 → +448)
    - sales_contacts:            33  (was 32 → +1)
    - psd_clients:              848
    - psd_client_products:    1,542

════════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════════
🟢 TRENDING WELL
  1. Live leads +471 (12,671 → 13,142) and vendors +448 (34,011 →
     34,459) — real ingestion continuing cleanly post-split.

  2. CPU load settled to normal (1.06/1.28/1.25) after yesterday's
     transient 06:00 bump. No sustained spike.

🟡 WATCH
  3. PENDING_TASKS ticked 5,100 → 5,150 (+50, still CA_SOS mock, do not
     send). Refresher ran 11-26 — source stays active.

  4. failed_emails = 54 (bounced/undeliverable). Same open question —
     real contacts needing correction, or dead leads?

  5. Disk holding at 82% (stable). No immediate action; watch trend.

  6. 2 services still FAILED (unchanged, multi-week) — certbot (SSL
     renewals) + dailyaidecheck. certbot is the priority: renew before
     certs lapse.

🟢 NOTE
  7. Email queue "synthetic" 148 records unchanged; no new sends since
     11-11. Sender path working but idle — nothing queued to push.

All core systems operational. Headline: healthy and quiet — live leads and
vendors keep climbing on real ingestion, load is settled, and the only
standing items are routine watch flags (failed certbot, failed_emails
backlog, mock PENDING_TASKS drift). Standing by.

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
