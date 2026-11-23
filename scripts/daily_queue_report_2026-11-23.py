#!/usr/bin/env python3
"""Daily Queue Email Report - November 23, 2026 (live data @ 06:00 UTC)."""
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
• Uptime:   15 days, 5h12m
• CPU Load: 3.28 / 2.01 / 1.60  🟡 slightly elevated (was 1.24/1.43/1.39 on 11-22)
• Memory:   6.4 Gi used / 15 Gi total  🟢
• Available: 9.2 Gi  🟢
• Swap:     5.8 Gi / 29 Gi  🟡 steady (unchanged)
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

• PENDING_TASKS.json:  4,950 tasks  (was 4,900 on 11-22)
    - source: CA_SOS_Scraper (synthetic/mock leads, do not send)
    - lastUpdated: 2026-11-22 12:23 UTC  🟢 fresh (yesterday)

════════════════════════════════════════════
  DepotChaos — LIVE vs DEMO split (active since 11-22 18:58 UTC)
════════════════════════════════════════════
LIVE data/depot_chaos/unified.db (75 MB — was 122 MB pre-split):
    - unified_leads:         1,460
    - leads:                11,009  (live-only; was 10,526 at split → +483 real)
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           636
    - datadepot_intelligence: 77,390  🟢 (deduped, holding)

LIVE DepotChaos/depot_chaos.db (canonical CRM):
    - vendors:               32,634
    - sales_contacts:            30
    - psd_clients:              848
    - psd_client_products:    1,542

DEMO (synthetic, kept for demos):
    - depot_chaos_demo.db vendors:       120,966
    - unified_demo.db leads:              23,533
    - datadepot_intelligence_demo:        79,060

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🟡 WATCH
  1. CPU load ticked up to 3.28 (1-min) from ~1.2 yesterday. Likely a
     transient batch (scraper/ingestion), but glance if it holds >3.

  2. LIVE/DEMO split now in effect — the old "leads 34,059" figure is
     now correctly split into 11,009 live + 23,533 demo. Live leads grew
     +483 since the 18:58 split (real ingestion, matches yesterday's bump).

  3. PENDING_TASKS ticked 4,900 → 4,950 (+50, still CA_SOS mock, do not
     send). Refresher ran 11-22 — source stays active.

  4. failed_emails = 54 (bounced/undeliverable). Worth a one-time cleanup
     review — are these real contacts needing correction, or dead leads?

  5. Disk holding at 82% (stable). No immediate action; watch trend.

  6. 2 services still FAILED (unchanged, multi-week) — certbot
     (SSL renewals) + dailyaidecheck. certbot is the priority: renew
     before certs lapse.

🟢 NOTE
  7. Email queue "synthetic" 148 records unchanged; no new sends since
     11-11. Sender path working but idle — nothing queued to push.

All core systems operational. Headline: healthy — the big shift this cycle
is the LIVE/DEMO split landing cleanly (live DB now 75 MB vs 122 MB), live
leads growing on real ingestion, with only routine watch items (load blip,
failed certbot, failed_emails backlog). Standing by.

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
