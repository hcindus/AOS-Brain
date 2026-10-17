#!/usr/bin/env python3
"""Daily Queue Email Report - October 17, 2026 (live data @ 11:38 UTC)."""
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
• Uptime:   151 days, 2h46m
• CPU Load: 3.38 / 2.72 / 2.43  🟡 elevated (1-min spike to 3.38)
• Memory:   9.5 Gi used / 15 Gi total  🟡 climbing (was 8.7 Gi)
• Available: 6.1 Gi
• Swap:     3.0 Gi / 29 Gi  🟢 dropped back (was 4.4 Gi on 10-13)
• Disk:     147G / 193G (76%)  🟡 creeping up (was 74%)

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control,
depotchaos-api, ollama — all ACTIVE.

⚠️ 3 services in FAILED state — aos-ternary, certbot, dailyaidecheck.

🟡 depotchaos-api.service is "activating" (auto-restart loop).
   depotchaos.service is ACTIVE.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db → email_queue):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - sent_at ALL NULL  → 0 sent all-time  🔴 STILL STALLED

• PENDING_TASKS.json:  4,050 tasks (up from 3,900)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-10-16 11:15 UTC  🟢 REFRESHED (was 5 days stale!)

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
  1. PENDING_TASKS refresher is BACK — lastUpdated 2026-10-16 11:15 UTC
     (was 5 days silent on 10-13). Count ticked up to 4,050.

🔴 CRITICAL
  2. Email queue STILL stalled — 207 ready emails (capton_hospitality
     campaign), 0 sent all-time. Root cause remains the Hostinger SMTP
     sender-address rejection (info@psdepot.com not owned by
     miles@myl0nr0s.cloud). Fix: verify info@psdepot.com as a sender in
     Hostinger, or switch the engine to send from miles@myl0nr0s.cloud.
     Confirm DKIM/SPF/DMARC for myl0nr0s.cloud.

🟡 IMPORTANT
  3. Load elevated — 3.38 / 2.72 / 2.43 (1-min spiked above 3). Multi-day
     trend, worth a look at CPU consumers.
  4. Memory climbing — 9.5 Gi used (was 8.7 Gi); available down to 6.1 Gi.
  5. Disk up to 76% (was 74%) — creeping, keep an eye on it.
  6. Three services still FAILED — aos-ternary, certbot, dailyaidecheck.
  7. depotchaos-api.service still "activating" (auto-restart loop).

🟢 NOTE
  8. Swap dropped back to 3.0 Gi (was 4.4 Gi) — pressure eased.
  9. DepotChaos DB counts essentially flat — pipeline idle.

All core systems operational. Good news: the PENDING_TASKS refresher is
running again and swap pressure eased. Top remaining concern is the
stalled 207-email queue (sender-address rejection, 0 sent all-time).
Secondary: sustained elevated load/memory, disk at 76%, three failed
services, and the depotchaos-api "activating" loop.
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
