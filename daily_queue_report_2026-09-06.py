#!/usr/bin/env python3
"""Daily Queue Email Report - September 6, 2026 (live data)."""
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
• Uptime:   109 days, 21h08m
• CPU Load: 1.62 / 0.98 / 0.93  🟢 healthy (no spike)
• Memory:   8.1 Gi used / 15 Gi total (54%)  🟢 healthy
• Available: 7.6 Gi
• Swap:     2.9 Gi / 29 Gi
• Disk:     133G / 193G (69%)  🟢 healthy

Core services: ✅ aos-brain-v4, aos-bhsi-v4, depotchaos, ollama,
darkfactory-worker, collections-worker, legal-worker, media-worker,
psd-sales-automation, testimonials-api (10 active).

⚠️ Note: 4 services in FAILED state — aos-ternary, certbot,
dailyaidecheck, and minecraft. mission-control is INACTIVE.
society-agents.service remains disabled.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - scheduled_at present, sent_at ALL NULL
• Sent last 24h / 7d / all-time:  0 / 0 / 0  🔴 still stalled

• PENDING_TASKS.json:  3,100 tasks
    - source: CA_SOS_Scraper  (synthetic/mock leads — do not send)
    - lastUpdated: 2026-09-03

• DepotChaos DB (data/depot_chaos/unified.db):  76.3 MB
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
  2. mission-control remains INACTIVE (persistent across recent days).
     Likely needs a systemd enable/restart to stay up.
  3. Four services in FAILED state — aos-ternary, certbot,
     dailyaidecheck, and minecraft. Worth a `systemctl restart` (or a
     decision to leave them disabled) to confirm they come back clean.
  4. Telegram @heartbeat delivery still unresolved — cron jobs
     (Mirror Audit, Weekly Blog Post, Monthly Document Review) failing
     because the recipient resolves to no numeric chat ID.

🟢 NOTE
  5. PENDING_TASKS at 3,100 are all CA_SOS_Scraper mock leads —
     no real outreach needed; do not inject more synthetic leads.
  6. System otherwise healthy: memory 54%, disk 69%, load settled —
     no OOM/disk/CPU risk.

All core systems operational. Primary concerns remain the stalled
207-email queue (sender-address rejection), mission-control staying
inactive, and the four failed services. Standing by for your
directives.

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
