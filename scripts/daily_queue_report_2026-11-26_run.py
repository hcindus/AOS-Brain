#!/usr/bin/env python3
"""Daily Queue Email Report - November 26, 2026 (live data @ 09:40 UTC)."""
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
subject = f"\U0001F4CA Daily Queue Report \u2014 {now.strftime('%B %d, %Y')} (09:40 UTC)"

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')} (09:40 UTC).

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
  SYSTEM HEALTH
\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
\u2022 Uptime:   18 days, 8h53m
\u2022 CPU Load: 1.56 / 1.69 / 1.61  \U0001F7E2 settled (was 2.63/1.63/1.35 at 06:00)
\u2022 Memory:   9.3 Gi used / 15 Gi total  \U0001F7E2
\u2022 Available: 6.3 Gi  \U0001F7E2
\u2022 Swap:     5.0 Gi / 29 Gi  \U0001F7E2 steady
\u2022 Disk:     158G / 193G (82%)  \U0001F7E1 unchanged

\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
  QUEUE STATUS
\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
\u2022 Email queue (data/depot_chaos/unified.db \u2192 email_queue):
    207 total \u2014 capton_hospitality_202607
    - 59 SENT \U0001F7E2 (unchanged)
    - 148 "synthetic"  \u26A0\uFE0F unchanged (do not send \u2014 confirm re-label intent)

\u2022 datadepot queue:
    - pending_emails.json:   0 (drained)
    - followup_queue:      100
    - sent_emails (all-time): 170
    - failed_emails:         54  \u26A0\uFE0F (bounced/undeliverable backlog)

\u2022 PENDING_TASKS.json:  5,100 tasks  (was 5,050 on 11-25)
    - source: CA_SOS_Scraper (synthetic/mock leads, do not send)
    - lastUpdated: 2026-11-25 12:23 UTC  \U0001F7E2 fresh (yesterday)

\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
  DepotChaos \u2014 LIVE vs DEMO split (active since 11-22 18:58 UTC)
\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
LIVE data/depot_chaos/unified.db:
    - unified_leads:         1,460
    - leads:                12,671  (was 12,204 on 11-25 \u2192 +467 real)
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           636
    - datadepot_intelligence: 77,390  \U0001F7E2 (deduped, holding)

LIVE DepotChaos/depot_chaos.db (canonical CRM):
    - vendors:               34,011  (was 33,530 on 11-25 \u2192 +481)
    - sales_contacts:            32  (unchanged)
    - psd_clients:              848
    - psd_client_products:    1,542

DEMO (synthetic, kept for demos):
    - depot_chaos_demo.db vendors:       120,966
    - unified_demo.db leads:              23,533
    - datadepot_intelligence_demo:        79,060

\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
  ACTION ITEMS
\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
\U0001F7E2 TRENDING WELL
  1. Live leads +467 (12,204 \u2192 12,671) and vendors +481 (33,530 \u2192
     34,011) \u2014 real ingestion continuing cleanly post-split.

  2. CPU load settled back to normal (1.56/1.69/1.61) after a transient
     06:00 bump (2.63). No sustained spike \u2014 confirmed transient.

\U0001F7E1 WATCH
  3. PENDING_TASKS ticked 5,050 \u2192 5,100 (+50, still CA_SOS mock, do not
     send). Refresher ran 11-25 \u2014 source stays active.

  4. failed_emails = 54 (bounced/undeliverable). Same open question as
     before \u2014 real contacts needing correction, or dead leads?

  5. Disk holding at 82% (stable). No immediate action; watch trend.

  6. 2 services still FAILED (unchanged, multi-week) \u2014 certbot (SSL
     renewals) + dailyaidecheck. certbot is the priority: renew before
     certs lapse.

\U0001F7E2 NOTE
  7. Email queue "synthetic" 148 records unchanged; no new sends since
     11-11. Sender path working but idle \u2014 nothing queued to push.

All core systems operational. Headline: healthy and quiet \u2014 live leads and
vendors keep growing on real ingestion, load bump was transient and has
settled, with only routine watch items (failed certbot, failed_emails
backlog, mock PENDING_TASKS drift). Standing by.

\u2014 Miles \U0001F680
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
