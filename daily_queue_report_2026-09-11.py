#!/usr/bin/env python3
"""Daily Queue Email Report - September 11, 2026 (live data)."""
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465
EMAIL = "miles@myl0nr0s.cloud"
PASSWORD = "Myl0n.R0s"
RECIPIENT = "Antonio.hudnall@gmail.com"

now = datetime.utcnow()
subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')}"

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')}.

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   115 days, 2h46m
• CPU Load: 0.80 / 0.69 / 0.67  🟢 healthy
• Memory:   9.6 Gi used / 15 Gi total (64%)  🟢 healthy
• Available: 6.0 Gi
• Swap:     903 Mi / 29 Gi
• Disk:     136G / 193G (71%)  🟢 healthy

Core services: ✅ aos-brain-v4, aos-bhsi-v4, ollama, darkfactory-worker,
collections-worker, legal-worker, media-worker, psd-sales-automation,
testimonials-api (ACTIVE).

⚠️ depotchaos is currently "activating" (was ACTIVE yesterday).

⚠️ 4 services in FAILED state — aos-ternary, certbot, dailyaidecheck,
and minecraft. mission-control regressed to "inactive" (was ACTIVE
yesterday). society-agents.service remains disabled/inactive.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db → email_queue):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - scheduled_at present, sent_at ALL NULL
• Sent last 24h / 7d / all-time:  0 / 0 / 0  🔴 still stalled

• PENDING_TASKS.json:  3,150 tasks (was 3,100 yesterday)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - lastUpdated: 2026-09-11 11:15 UTC (fresh today)

• DepotChaos DB (data/depot_chaos/unified.db):  73 MB
    - unified_leads:           1,460
    - leads:                  32,542
    - ca_abc_licenses:        74,521
    - datadepot_intelligence: 74,518
    - enriched_leads:            919
    - psd_customers:             501
    - psd_customer_sales:        503
    - address_crossref:        3,535
    - verified_leads:              1

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. Email queue still stalled — 207 ready emails (capton_hospitality
     campaign), 0 sent. Root cause remains the Hostinger SMTP
     sender-address rejection (info@psdepot.com not owned by
     miles@myl0nr0s.cloud). Fix: verify info@psdepot.com as a sender
     in Hostinger, or switch the engine to send from
     miles@myl0nr0s.cloud. Confirm DKIM/SPF/DMARC for myl0nr0s.cloud.

🟡 IMPORTANT
  2. Four services in FAILED state — aos-ternary, certbot,
     dailyaidecheck, and minecraft. Worth a `systemctl restart` (or a
     decision to leave them disabled) to confirm they come back clean.
  3. mission-control regressed to "inactive" — was ACTIVE yesterday;
     re-check whether it should be enabled.
  4. depotchaos is "activating" — confirm it reaches ACTIVE and isn't
     stuck mid-restart.
  5. society-agents.service remains disabled/inactive.

🟢 NOTE
  6. PENDING_TASKS at 3,150 are all CA_SOS_Scraper mock leads — no real
     outreach needed; do not inject more synthetic leads.
  7. System otherwise healthy: memory 64%, disk 71%, load settled — no
     OOM/disk/CPU risk.

All core systems operational. Primary concerns remain the stalled
207-email queue (sender-address rejection) and the four failed
services, plus mission-control regressing to inactive. Standing by for
your directives.

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
with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ctx) as s:
    s.login(EMAIL, PASSWORD)
    s.sendmail(EMAIL, RECIPIENT, msg.as_string())

print("SENT to", RECIPIENT, "|", subject)
