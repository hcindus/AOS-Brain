#!/usr/bin/env python3
"""Daily Queue Email Report - September 15, 2026 (live data @ 06:00 UTC)."""
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
• Uptime:   118 days, 21h08m
• CPU Load: 1.76 / 1.59 / 1.46  🟡 slightly elevated but stable
• Memory:   3.4 Gi used / 15 Gi total (23%)  🟢 healthy
• Available: 12 Gi
• Swap:     5.4 Gi / 29 Gi
• Disk:     136G / 193G (71%)  🟢 healthy

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control, ollama (ACTIVE).

⚠️ depotchaos is currently "activating" (still not ACTIVE).

⚠️ 4 services in FAILED state — aos-ternary, certbot, dailyaidecheck,
and minecraft. mission-control remains "inactive".
society-agents.service remains disabled/inactive.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db → email_queue):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - scheduled_at present, sent_at ALL NULL
• Sent last 24h / 7d / all-time:  0 / 0 / 0  🔴 still stalled

• PENDING_TASKS.json:  3,150 tasks (unchanged)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - lastUpdated: 2026-09-11 11:15 UTC (NOT refreshed today)

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
     campaign), 0 sent all-time. Root cause remains the Hostinger SMTP
     sender-address rejection (info@psdepot.com not owned by
     miles@myl0nr0s.cloud). Fix: verify info@psdepot.com as a sender
     in Hostinger, or switch the engine to send from
     miles@myl0nr0s.cloud. Confirm DKIM/SPF/DMARC for myl0nr0s.cloud.

🟡 IMPORTANT
  2. Four services in FAILED state — aos-ternary, certbot,
     dailyaidecheck, and minecraft. Worth a `systemctl restart` (or a
     decision to leave them disabled) to confirm they come back clean.
  3. mission-control remains "inactive" — re-check whether it should be
     enabled (note: aos-mission-control is ACTIVE).
  4. depotchaos is "activating" — confirm it reaches ACTIVE and isn't
     stuck mid-restart.
  5. society-agents.service remains disabled/inactive.

🟢 NOTE
  6. PENDING_TASKS at 3,150 are all CA_SOS_Scraper mock leads — no real
     outreach needed; do not inject more synthetic leads.
     (lastUpdated unchanged since 2026-09-11 — scraper did not run.)
  7. System otherwise healthy: memory 23%, disk 71%, load settled
     ~1.5-1.8 — no OOM/disk/CPU risk.

All core systems operational. Primary concerns remain the stalled
207-email queue (sender-address rejection), the four failed services,
and mission-control/depotchaos not in ACTIVE state. Standing by for
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
