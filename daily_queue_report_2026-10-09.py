#!/usr/bin/env python3
"""Daily Queue Email Report - October 09, 2026 (live data @ 11:38 UTC)."""
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
• Uptime:   143 days, 2h46m
• CPU Load: 0.89 / 0.90 / 0.91  🟢 healthy, settled
• Memory:   9.7 Gi used / 15 Gi total  🟡 up from 5.4 Gi (10-08)
• Available: 6.0 Gi
• Swap:     1.7 Gi / 29 Gi
• Disk:     139G / 193G (73%)  🟢 stable

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control,
depotchaos-api, ollama — all ACTIVE.

⚠️ 4 services in FAILED state — aos-ternary, certbot, dailyaidecheck,
and minecraft. society-agents.service remains disabled/inactive.

🟡 depotchaos.service is "activating" again (still in auto-restart loop).

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db → email_queue):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - sent_at ALL NULL  → 0 sent all-time  🔴 STILL STALLED

• PENDING_TASKS.json:  3,900 tasks (up 50 from 3,850 on 10-08)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-10-08 11:15 UTC  ✅ REFRESHED yesterday

• DepotChaos DB (data/depot_chaos/unified.db, 93.4 MB):
    - unified_leads:    1,460
    - leads:           32,588
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
  2. depotchaos.service is "activating" again — still in the auto-restart
     loop. Worth a look.
  3. Four services still FAILED — aos-ternary, certbot, dailyaidecheck,
     and minecraft. A restart (or explicit decision to leave disabled)
     would confirm they come back clean.
  4. Memory ticked up 5.4 → 9.7 Gi (6.0 Gi available); load still low
     (~0.9). No immediate pressure, but worth watching.

🟢 NOTE
  5. PENDING_TASKS refresher RAN — lastUpdated 10-08 11:15 UTC, count
     ticked up 3,850 → 3,900. Scraper/refresher on schedule. ✅
  6. Disk stable at 73% — no OOM/disk/CPU risk.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection). Secondary: depotchaos.service
in "activating" loop + the four failed services. Standing by.

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
