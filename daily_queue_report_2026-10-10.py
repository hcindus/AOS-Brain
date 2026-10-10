#!/usr/bin/env python3
"""Daily Queue Email Report - October 10, 2026 (live data @ 11:38 UTC)."""
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
• Uptime:   144 days, 2h46m
• CPU Load: 0.54 / 0.72 / 0.96  🟢 healthy, settled
• Memory:   8.1 Gi used / 15 Gi total  🟢 back to normal (was 9.7 Gi on 10-09)
• Available: 7.5 Gi
• Swap:     2.3 Gi / 29 Gi
• Disk:     139G / 193G (73%)  🟢 stable

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control,
depotchaos-api, ollama — all ACTIVE.

⚠️ 4 services in FAILED state — aos-ternary, certbot, dailyaidecheck,
and minecraft. society-agents.service remains disabled/inactive.

🟡 depotchaos.service is "activating" (still in auto-restart loop).

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db → email_queue):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - sent_at ALL NULL  → 0 sent all-time  🔴 STILL STALLED

• PENDING_TASKS.json:  3,900 tasks (unchanged from 10-08/10-09)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-10-08 11:15 UTC  🟡 UNCHANGED (no refresh in 2 days)

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

🟡 IMPORTANT
  2. depotchaos.service is "activating" again — still in the auto-restart
     loop. Worth a look.
  3. Four services still FAILED — aos-ternary, certbot, dailyaidecheck,
     and minecraft. A restart (or explicit decision to leave disabled)
     would confirm they come back clean.
  4. Memory eased 9.7 → 8.1 Gi (7.5 Gi available); load low (~0.5-0.9).
     No pressure, just the normal daily ebb.

🟢 NOTE
  5. PENDING_TASKS unchanged at 3,900 — refresher last ran 10-08 11:15
     UTC (no refresh in ~2 days). Worth confirming the scraper/refresher
     cron is still scheduled.
  6. Disk stable at 73% — no OOM/disk/CPU risk.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection). Secondary: depotchaos.service
in "activating" loop + the four failed services, and the PENDING_TASKS
refresher now 2 days silent. Standing by.

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
