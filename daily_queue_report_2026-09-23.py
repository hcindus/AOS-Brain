#!/usr/bin/env python3
"""Daily Queue Email Report - September 23, 2026 (live data @ 11:38 UTC)."""
import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

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
subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')} (11:38 UTC)"

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')} (11:38 UTC refresh).

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   127 days, 2h46m
• CPU Load: 1.11 / 1.00 / 1.01  🟢 healthy, settled
• Memory:   10 Gi used / 15 Gi total (67%)  🟡 up from 54% yesterday
• Available: 5.6 Gi
• Swap:     1.5 Gi / 29 Gi
• Disk:     139G / 193G (72%)  🟢 unchanged

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control, ollama
all ACTIVE. ⚠️ depotchaos still "activating" (fifth consecutive day).

⚠️ 4 services in FAILED state — aos-ternary, certbot, dailyaidecheck,
and minecraft. society-agents.service remains disabled/inactive.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db → email_queue):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - sent_at ALL NULL
• Sent last 24h / 7d / all-time (this engine):  0 / 0 / 0  🔴 still stalled

• datadepot/queue (separate engine):
    - pending_emails.json:  99  (teriyaki_thermal_paper_q2_2026 = 98, outreach = 1)
    - followup_queue:       100
    - failed_emails.json:    29
    - sent (all-time):      170

• PENDING_TASKS.json:  3,300 tasks (up 50 from 3,250 yesterday)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-09-23 11:15 UTC  ✅ REFRESHED (was stale since 09-19)

• DepotChaos DB (data/depot_chaos/unified.db):  93.4 MB (unchanged)
    - unified_leads:           1,460
    - leads:                  32,587
    - ca_abc_licenses:        77,390  (unchanged)
    - enriched_leads:            919
    - verified_leads:              1
    - psd_customers:             501

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. Email queue STILL stalled — 207 ready emails (capton_hospitality
     campaign), 0 sent all-time. Root cause remains the Hostinger SMTP
     sender-address rejection (info@psdepot.com not owned by
     miles@myl0nr0s.cloud). Fix: verify info@psdepot.com as a sender
     in Hostinger, or switch the engine to send from
     miles@myl0nr0s.cloud. Confirm DKIM/SPF/DMARC for myl0nr0s.cloud.

🟡 IMPORTANT
  2. depotchaos stuck in "activating" for a FIFTH day — worth a
     `systemctl restart depotchaos` (or check its journal) to see if
     it recovers to ACTIVE.
  3. Four services still FAILED — aos-ternary, certbot, dailyaidecheck,
     and minecraft. A restart (or explicit decision to leave disabled)
     would confirm they come back clean.
  4. Memory climbed 54% → 67% (8.1 → 10 Gi used). Still not critical,
     but it's the largest single-day jump in weeks — worth a glance at
     `top`/`ps` for any runaway process before it tightens.

🟢 NOTE
  5. PENDING_TASKS refresher RAN — lastUpdated moved 09-19 → 09-23
     11:15 UTC and count ticked up 3,250 → 3,300. Scraper/refresher is
     back on schedule. ✅
  6. DB size and all table counts unchanged from yesterday — no new
     ingest, no growth concern.
  7. Load settled nicely (1.11) — no CPU pressure.
  8. Disk stable at 72% — no OOM/disk/CPU risk.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection). Secondary: depotchaos
"activating" for a fifth day, the four failed services, and this
week's memory creep (67%). Standing by.

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
