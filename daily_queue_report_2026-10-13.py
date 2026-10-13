#!/usr/bin/env python3
"""Daily Queue Email Report - October 13, 2026 (live data @ 11:38 UTC)."""
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
• Uptime:   147 days, 2h46m
• CPU Load: 2.31 / 2.21 / 2.36  🟡 elevated (held ~2.2-2.6 since 10-11)
• Memory:   8.7 Gi used / 15 Gi total  🟢 normal
• Available: 6.9 Gi
• Swap:     4.4 Gi / 29 Gi  🟡 creeping up (was 3.1 Gi on 10-11)
• Disk:     142G / 193G (74%)  🟢 stable

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control,
depotchaos-api, ollama — all ACTIVE.

⚠️ 3 services in FAILED state — aos-ternary, certbot, dailyaidecheck.
(minecraft.service still dropped off the failed list.)

🟡 depotchaos.service is "activating" (still in auto-restart loop).

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db → email_queue):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - sent_at ALL NULL  → 0 sent all-time  🔴 STILL STALLED

• PENDING_TASKS.json:  3,900 tasks (unchanged)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-10-08 11:15 UTC  🔴 5 DAYS STALE (no refresh)

• DepotChaos DB (data/depot_chaos/unified.db, 93.4 MB):
    - unified_leads:         1,460
    - leads:                32,588
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           501
    - psd_customer_sales:      503
    - datadepot_intelligence: 74,518
    - address_crossref:       3,535

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. Email queue STILL stalled — 207 ready emails (capton_hospitality
     campaign), 0 sent all-time. Root cause remains the Hostinger SMTP
     sender-address rejection (info@psdepot.com not owned by
     miles@myl0nr0s.cloud). Fix: verify info@psdepot.com as a sender in
     Hostinger, or switch the engine to send from miles@myl0nr0s.cloud.
     Confirm DKIM/SPF/DMARC for myl0nr0s.cloud.

  2. PENDING_TASKS refresher now 5 DAYS silent — lastUpdated 10-08 11:15
     UTC. Confirm the scraper/refresher cron is still scheduled and
     running (was 3 days stale on 10-11, now 5).

🟡 IMPORTANT
  3. Load still elevated to ~2.2-2.4 (vs ~0.5-0.9 baseline). Worth a
     look at what's consuming CPU — this is now a multi-day trend.
  4. Swap climbing — 4.4 Gi now (3.1 Gi two days ago). Keep an eye on it.
  5. depotchaos.service is "activating" — still in auto-restart loop.
  6. Three services still FAILED — aos-ternary, certbot, dailyaidecheck.

🟢 NOTE
  7. Disk stable at 74% — no OOM/disk risk.
  8. All DepotChaos DB counts unchanged — pipeline idle.

All core systems operational. Top concerns remain the stalled 207-email
queue (sender-address rejection) and the now-5-day-silent PENDING_TASKS
refresher. Secondary: sustained elevated load (~2.2-2.4), rising swap
(4.4 Gi), depotchaos "activating" loop, and three failed services.
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
