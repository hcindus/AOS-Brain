#!/usr/bin/env python3
"""Daily Queue Email Report - October 29, 2026 (live data @ 11:40 UTC)."""
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
subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')} (11:40 UTC)"

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')} (11:40 UTC refresh).

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   11 days, 15h02m
• CPU Load: 5.29 / 8.22 / 7.93  🔴 ELEVATED (was 1.72/1.33/1.23 on 10-21)
• Memory:   8.3 Gi used / 15 Gi total  🟡 (was 4.6 Gi on 10-21)
• Available: 7.3 Gi
• Swap:     7.9 Gi / 29 Gi  🟡 climbing (was 3.9 Gi)
• Disk:     151G / 193G (79%)  🟡 +3% since 10-17

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control,
depotchaos, ollama — all ACTIVE. Vision daemons also up.

⚠️ 2 services FAILED — certbot, dailyaidecheck (same two as prior days).

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (data/depot_chaos/unified.db → email_queue):
    207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - sent_at ALL NULL  → 0 sent all-time  🔴 STILL STALLED (since July)

• PENDING_TASKS.json:  4,450 tasks (up from 4,250 on 10-21)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-10-28 11:16 UTC  🟡 1 day stale (was fresh 10-21)

• DepotChaos DB (data/depot_chaos/unified.db, 131 MB — grew from 94 MB):
    - unified_leads:         1,460
    - leads:                32,590
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           502
    - psd_customer_sales:      503
    - datadepot_intelligence: 77,390 (now mirrors ca_abc_licenses)

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. CPU load spiked — 5.29 / 8.22 / 7.93 (was ~1.7 on 10-21). Worth a
     look at what's driving it; memory (8.3 Gi) and swap (7.9 Gi) are also
     climbing in step.
  2. Email queue STILL stalled — 207 ready emails (capton_hospitality
     campaign), 0 sent all-time. Root cause unchanged: Hostinger SMTP
     sender-address rejection (info@psdepot.com not owned by
     miles@myl0nr0s.cloud). Fix: verify info@psdepot.com as a sender, or
     switch engine to send from miles@myl0nr0s.cloud; confirm
     DKIM/SPF/DMARC for myl0nr0s.cloud.

🟡 IMPORTANT
  3. Disk up to 79% (was 76%) — +3% growth this cycle; DepotChaos DB grew
     94→131 MB. Worth watching.
  4. PENDING_TASKS refresher slipped to 1 day stale (10-28 11:16 UTC) —
     count still climbing (4,250 → 4,450, mock CA_SOS leads).
  5. Two services FAILED — certbot, dailyaidecheck (unchanged).

🟢 NOTE
  6. Core services + vision daemons all healthy.
  7. No overnight embodiment/robotics work on my side beyond the
     AX-169F/Myl1Ssa seam build (see memory 10-28/10-29); the seam is now
     a complete, tested end-to-end loop.

All core systems operational. Top concerns this cycle are the sharp CPU
load/memory/swap climb and the still-stalled 207-email queue. Recommend a
quick look at load drivers, plus the standing sender-address fix to finally
clear the email backlog.
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
