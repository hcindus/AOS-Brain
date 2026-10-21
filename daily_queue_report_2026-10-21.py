#!/usr/bin/env python3
"""Daily Queue Email Report - October 21, 2026 (live data @ 11:38 UTC)."""
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
subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')} (11:38 UTC)"

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')} (11:38 UTC refresh).

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   3 days, 15h00m
• CPU Load: 1.72 / 1.33 / 1.23  🟢 normalized (was 3.38 on 10-17)
• Memory:   4.6 Gi used / 15 Gi total  🟢 dropped (was 9.5 Gi)
• Available: 10 Gi
• Swap:     3.9 Gi / 29 Gi  🟢 stable
• Disk:     146G / 193G (76%)  🟡 flat (unchanged from 10-17)

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control,
depotchaos, ollama — all ACTIVE.

⚠️ 2 services FAILED — certbot, dailyaidecheck (same two as prior day).

🟡 depotchaos-api.service is "activating" (auto-restart loop, unchanged).
🟡 aos-ternary.service is inactive.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db → email_queue):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - sent_at ALL NULL  → 0 sent all-time  🔴 STILL STALLED (since July)

• PENDING_TASKS.json:  4,250 tasks (up from 4,050)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-10-21 11:15 UTC  🟢 FRESH (refreshed today)

• DepotChaos DB (data/depot_chaos/unified.db, 94.3 MB):
    - unified_leads:         1,460
    - leads:                32,590
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           502
    - psd_customer_sales:      503
    - datadepot_intelligence: 74,518
    - address_crossref:       3,535

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🟢 RESOLVED
  1. System load normalized — 1.72 / 1.33 / 1.23 (was 3.38 spike on 10-17).
  2. Memory pressure eased — 4.6 Gi used (was 9.5 Gi); 10 Gi available.
  3. PENDING_TASKS refresher running clean — lastUpdated TODAY 11:15 UTC,
     count ticked up to 4,250.

🔴 CRITICAL
  4. Email queue STILL stalled — 207 ready emails (capton_hospitality
     campaign), 0 sent all-time. Root cause remains the Hostinger SMTP
     sender-address rejection (info@psdepot.com not owned by
     miles@myl0nr0s.cloud). Fix: verify info@psdepot.com as a sender in
     Hostinger, or switch the engine to send from miles@myl0nr0s.cloud.
     Confirm DKIM/SPF/DMARC for myl0nr0s.cloud.

🟡 IMPORTANT
  5. Disk flat at 76% — no growth since 10-17, but still worth watching.
  6. Two services FAILED — certbot, dailyaidecheck.
  7. depotchaos-api.service still "activating" (auto-restart loop).
  8. aos-ternary.service inactive.

🟢 NOTE
  9. DepotChaos DB counts essentially flat — pipeline idle.

All core systems operational. Good news: load and memory have both
normalized, and the PENDING_TASKS refresher is back on a same-day cadence.
Top remaining concern is still the stalled 207-email queue (sender-address
rejection, 0 sent all-time). Secondary: the usual two failed services and
the depotchaos-api "activating" loop.
Standing by.

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
