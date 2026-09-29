#!/usr/bin/env python3
"""Daily Queue Email Report - September 29, 2026 (live data @ 11:38 UTC)."""
import smtplib, ssl, os
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
• Uptime:   133 days, 2h46m
• CPU Load: 1.20 / 0.99 / 0.92  🟢 healthy, settled
• Memory:   8.7 Gi used / 15 Gi total  🟡 up from 7.7 Gi (09-28)
• Available: 6.9 Gi
• Swap:     2.2 Gi / 29 Gi
• Disk:     140G / 193G (73%)  🟢 stable

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control, aos-vision,
depotchaos-api, ollama, ollama-bonsai-bridge — all ACTIVE.
✅ depotchaos.service now ACTIVE — recovered from the "activating"
auto-restart loop that persisted for 11 straight days. Good news.

⚠️ 4 services in FAILED state — aos-ternary, certbot, dailyaidecheck,
and minecraft. society-agents.service remains disabled/inactive.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db → email_queue):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - sent_at ALL NULL  → 0 sent all-time  🔴 STILL STALLED

• PENDING_TASKS.json:  3,550 tasks (up 50 from 3,500 on 09-28)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-09-29 11:15 UTC  ✅ REFRESHED today

• DepotChaos DB (data/depot_chaos/unified.db):
    - unified_leads:    1,460
    - leads:           32,587
    - ca_abc_licenses: 77,390
    - enriched_leads:     919
    - verified_leads:       1
    - psd_customers:      501

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

🟡 IMPORTANT
  2. Four services still FAILED — aos-ternary, certbot, dailyaidecheck,
     and minecraft. A restart (or explicit decision to leave disabled)
     would confirm they come back clean.

🟢 NOTE
  3. ✅ depotchaos.service RECOVERED — now ACTIVE after 11 days of
     "activating" auto-restart loops. No action needed unless it flaps.
  4. PENDING_TASKS refresher RAN — lastUpdated 09-29 11:15 UTC, count
     ticked up 3,500 → 3,550. Scraper/refresher on schedule. ✅
  5. Memory ticked UP 7.7 → 8.7 Gi (6.9 Gi available); load still settled
     (~1.20). No resource pressure. ✅
  6. Disk stable at 73% — no OOM/disk/CPU risk.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection). Secondary: the four failed
services. Standing by.

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
