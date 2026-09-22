#!/usr/bin/env python3
"""Daily Queue Email Report - September 22, 2026 (live data @ 06:00 UTC)."""
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
subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')} (06:00 UTC)"

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')} (06:00 UTC refresh).

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   125 days, 21h08m
• CPU Load: 1.35 / 1.03 / 0.93  🟢 healthy, settled
• Memory:   8.1 Gi used / 15 Gi total (54%)  🟡 slightly up from 50% yesterday
• Available: 7.5 Gi
• Swap:     1.7 Gi / 29 Gi
• Disk:     138G / 193G (72%)  🟢 healthy

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control, ollama
all ACTIVE. ⚠️ depotchaos still "activating" (fourth consecutive day).

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

• PENDING_TASKS.json:  3,250 tasks (unchanged)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-09-19 11:16 UTC (3 days stale — NOT refreshed)
    - scraped_at: 2026-06-16 11:13 UTC (underlying leads NOT refreshed)

• DepotChaos DB (data/depot_chaos/unified.db):  93.4 MB (unchanged)
    - unified_leads:           1,460
    - leads:                  32,587
    - ca_abc_licenses:        77,390  (unchanged)
    - enriched_leads:            919
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
  2. depotchaos stuck in "activating" for a FOURTH day — worth a
     `systemctl restart depotchaos` (or check its journal) to see if
     it recovers to ACTIVE.
  3. Four services still FAILED — aos-ternary, certbot, dailyaidecheck,
     and minecraft. A restart (or explicit decision to leave disabled)
     would confirm they come back clean.
  4. PENDING_TASKS lastUpdated still has not refreshed (still 09-19
     11:16 UTC — now 3 days stale). The scraper/refresher is not
     running on schedule — check that job.

🟢 NOTE
  5. Memory ticked back up slightly — 50% → 54% (7.5 Gi → 8.1 Gi used).
     Still healthy, not a concern, just noting the reversal of
     yesterday's improvement.
  6. DB size and all table counts unchanged from yesterday — no new
     ingest, no growth concern.
  7. Load improved further — 2.09 → 1.35 (settled). No CPU pressure.
  8. System otherwise healthy: disk 72% — no OOM/disk/CPU risk.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection). Secondary: depotchaos
"activating" for a fourth day, the four failed services, and
PENDING_TASKS now 3 days stale. Standing by.

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
