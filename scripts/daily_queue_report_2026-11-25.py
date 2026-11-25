#!/usr/bin/env python3
"""Daily Queue Email Report - November 25, 2026 (live data @ 06:00 UTC)."""
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
subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')} (06:00 UTC)"

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')} (06:00 UTC).

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   17 days, 5h12m
• CPU Load: 1.77 / 1.39 / 1.25  🟢 back to normal (was 3.28/2.01/1.60 on 11-23)
• Memory:   7.8 Gi used / 15 Gi total  🟢
• Available: 7.8 Gi  🟢
• Swap:     5.6 Gi / 29 Gi  🟢 steady
• Disk:     158G / 193G (82%)  🟡 unchanged

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
    - failed_emails:         54  ⚠️ (bounced/undeliverable backlog)

• PENDING_TASKS.json:  5,050 tasks  (was 4,950 on 11-23)
    - source: CA_SOS_Scraper (synthetic/mock leads, do not send)
    - lastUpdated: 2026-11-24 12:23 UTC  🟢 fresh (yesterday)

════════════════════════════════════════════
  DepotChaos — LIVE vs DEMO split (active since 11-22 18:58 UTC)
════════════════════════════════════════════
LIVE data/depot_chaos/unified.db:
    - unified_leads:         1,460
    - leads:                12,204  (was 11,009 on 11-23 → +1,195 real)
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           636
    - datadepot_intelligence: 77,390  🟢 (deduped, holding)

LIVE DepotChaos/depot_chaos.db (canonical CRM):
    - vendors:               33,530  (was 32,634 → +896)
    - sales_contacts:            32  (was 30 → +2)
    - psd_clients:              848
    - psd_client_products:    1,542

DEMO (synthetic, kept for demos):
    - depot_chaos_demo.db vendors:       120,966
    - unified_demo.db leads:              23,533
    - datadepot_intelligence_demo:        79,060

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🟢 RECOVERED
  1. CPU load back to normal (1.77/1.39/1.25) after the 11-23 spike. No
     sustained load — the earlier blip was transient.

  2. Live leads grew +1,195 (11,009 → 12,204) and vendors +896 (32,634 →
     33,530) — real ingestion continuing cleanly post-split.

🟡 WATCH
  3. PENDING_TASKS ticked 4,950 → 5,050 (+100, still CA_SOS mock, do not
     send). Refresher ran 11-24 — source stays active.

  4. failed_emails = 54 (bounced/undeliverable). Same one-time cleanup
     question as before — real contacts needing correction, or dead leads?

  5. Disk holding at 82% (stable). No immediate action; watch trend.

  6. 2 services still FAILED (unchanged, multi-week) — certbot (SSL
     renewals) + dailyaidecheck. certbot is the priority: renew before
     certs lapse.

🟢 NOTE
  7. Email queue "synthetic" 148 records unchanged; no new sends since
     11-11. Sender path working but idle — nothing queued to push.

All core systems operational. Headline: healthy and quiet — load recovered,
live leads/vendors growing on real ingestion, and only routine watch items
(failed certbot, failed_emails backlog, mock PENDING_TASKS drift). Standing by.

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
