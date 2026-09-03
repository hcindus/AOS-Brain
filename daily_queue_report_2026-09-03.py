#!/usr/bin/env python3
"""Daily Queue Email Report - September 3, 2026 (live data)."""
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
• Uptime:   107 days, 2h46m
• CPU Load: 1.74 / 1.43 / 1.41  🟢 healthy
• Memory:   10 Gi used / 15 Gi total (66%)  🟢 healthy
• Available: 5.5 Gi
• Swap:     1.8 Gi / 29 Gi
• Disk:     134G / 193G (70%)  🟢 healthy

Core services: ✅ aos-brain-v4, aos-bhsi-v4, ollama, darkfactory-worker,
collections-worker, legal-worker, media-worker, psd-sales-automation,
testimonials-api.

⚠️ Note: depotchaos-api (activating) and mission-control (inactive)
flagged. minecraft.service + society-agents.service remain disabled.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - scheduled_at present, sent_at ALL NULL
• Sent last 24h / 7d / all-time:  0 / 0 / 0  🔴 still stalled

• PENDING_TASKS.json:  3,100 tasks
    - source: CA_SOS_Scraper  (synthetic/mock leads — do not send)
    - lastUpdated: 2026-09-03T11:14 UTC

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
  2. depotchaos-api stuck in "activating" and mission-control is
     "inactive" — worth a quick `systemctl restart` to confirm they
     come back clean.
  3. Telegram @heartbeat delivery still unresolved — cron jobs
     (Mirror Audit, Weekly Blog Post, Monthly Document Review) failing
     because the recipient resolves to no numeric chat ID.

🟢 NOTE
  4. PENDING_TASKS at 3,100 are all CA_SOS_Scraper mock leads —
     no real outreach needed; do not inject more synthetic leads.
  5. System healthy: load ~1.7, memory 66%, disk 70% — no OOM/disk risk.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection) plus the two flagged
services. Standing by for your directives.

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
