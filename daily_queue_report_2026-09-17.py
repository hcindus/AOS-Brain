#!/usr/bin/env python3
"""Daily Queue Email Report - September 17, 2026 (live data @ 06:00 UTC)."""
import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load SMTP credentials from secrets file (not hardcoded)
def load_env(filepath):
    if os.path.exists(filepath):
        for line in open(filepath):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env('/root/.openclaw/workspace/aocros/secrets/smtp.env')

SMTP_SERVER = os.getenv("HOSTINGER_SMTP_SERVER", "smtp.hostinger.com")
SMTP_PORT = int(os.getenv("HOSTINGER_SMTP_PORT", "587"))
EMAIL = os.getenv("HOSTINGER_SMTP_USER", "miles@myl0nr0s.cloud")
PASSWORD = os.getenv("HOSTINGER_SMTP_PASS", "")
RECIPIENT = "Antonio.hudnall@gmail.com"

now = datetime.utcnow()
subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')}"

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')}.

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   120 days, 21h08m
• CPU Load: 2.03 / 1.20 / 1.01  🟢 healthy, settled
• Memory:   5.1 Gi used / 15 Gi total (34%)  🟢 healthy
• Available: 10 Gi
• Swap:     5.4 Gi / 29 Gi
• Disk:     137G / 193G (71%)  🟢 healthy

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control, ollama
— ALL ACTIVE. ⚠️ depotchaos = "activating" (was ACTIVE yesterday —
re-check whether it fully came up).

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
    - scraped_at: 2026-06-16 11:13 UTC (NOT refreshed today)

• DepotChaos DB (data/depot_chaos/unified.db):  73.7 MB
    - unified_leads:           1,460
    - leads:                  32,542
    - ca_abc_licenses:        74,521
    - datadepot_intelligence: 74,518
    - enriched_leads:            919
    - psd_customers:             501
    - psd_customer_sales:        503
    - address_crossref:        3,535
    - verified_leads:              1
    - scrape_runs:                 4

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
  2. Four services still in FAILED state — aos-ternary, certbot,
     dailyaidecheck, and minecraft. Worth a `systemctl restart` (or a
     decision to leave them disabled) to confirm they come back clean.
  3. mission-control remains "inactive" — re-check whether it should be
     enabled (note: aos-mission-control is ACTIVE).
  4. society-agents.service remains disabled/inactive.
  5. depotchaos reverted to "activating" (was ACTIVE yesterday) —
     monitor to confirm it settles back to ACTIVE.

🟢 NOTE
  6. PENDING_TASKS at 3,150 are all CA_SOS_Scraper mock leads — no real
     outreach needed; do not inject more synthetic leads.
     (scraped_at unchanged since 2026-06-16 — scraper did not run.)
  7. System otherwise healthy: memory 34%, disk 71%, load settled
     ~1.0-2.0 — no OOM/disk/CPU risk.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection). Secondary: the four failed
services, mission-control not in ACTIVE state, and depotchaos reverting
to "activating". Standing by for your directives.

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
