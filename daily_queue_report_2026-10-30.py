#!/usr/bin/env python3
"""Daily Queue Email Report - October 30, 2026 (live data @ 11:40 UTC)."""
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
• Uptime:   12 days, 15h03m
• CPU Load: 10.69 / 6.31 / 6.64  🔴 CRITICAL SPIKE (was 5.29/8.22/7.93 on 10-29)
• Memory:   11 Gi used / 15 Gi total  🔴 (was 8.3 Gi on 10-29)
• Available: 4.4 Gi  🔴 dropping (was 7.3 Gi)
• Swap:     7.6 Gi / 29 Gi  🟡 (was 7.9 Gi)
• Disk:     152G / 193G (79%)  🟡 flat vs 10-29

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control,
depotchaos, ollama — all ACTIVE.

⚠️ 2 services FAILED — certbot, dailyaidecheck (unchanged for multiple days).

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (data/depot_chaos/unified.db → email_queue):
    207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - sent_at ALL NULL  → 0 sent all-time  🔴 STILL STALLED (since July)

• PENDING_TASKS.json:  4,450 tasks (unchanged from 10-29)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-10-28 11:16 UTC  🔴 2 days stale (was 1 day on 10-29)

• DepotChaos DB (data/depot_chaos/unified.db, ~131 MB — flat vs 10-29):
    - unified_leads:         1,460
    - leads:                32,590
    - ca_abc_licenses:      77,390
    - enriched_leads:          919
    - verified_leads:            1
    - psd_customers:           502
    - psd_customer_sales:      503
    - datadepot_intelligence: 77,390

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. CPU load spiked AGAIN — 1-min load 10.69 (was 5.29 yesterday), memory
     now 11 Gi used with only 4.4 Gi available. This is an accelerating
     climb (1.7 → 5.3 → 10.7 over 3 days). Recommend immediate triage of
     load/memory drivers before swap pressure forces a stall.
  2. Email queue STILL stalled — 207 ready emails (capton_hospitality
     campaign), 0 sent all-time. Root cause unchanged: Hostinger SMTP
     sender-address rejection (info@psdepot.com not owned by
     miles@myl0nr0s.cloud). Fix: verify info@psdepot.com as a sender, or
     switch engine to send from miles@myl0nr0s.cloud; confirm
     DKIM/SPF/DMARC for myl0nr0s.cloud.

🟡 IMPORTANT
  3. Disk stable at 79% — no growth this cycle (was +3% prior cycle).
  4. PENDING_TASKS refresher now 2 days stale (10-28 11:16 UTC) — count
     flat at 4,450 (mock CA_SOS leads). Refresher cron has not fired.
  5. Two services FAILED — certbot, dailyaidecheck (unchanged).

🟢 NOTE
  6. Core services + vision daemons all healthy.
  7. No new overnight work on my side; AX-169F/Myl1Ssa seam build remains
     complete and tested (memory 10-28/10-29).

All core systems still operational, but the CPU/memory climb has gone
critical (load 10.7, 4.4 Gi free) and needs a look today. The standing
sender-address fix is still the only thing blocking the 207-email backlog.
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
