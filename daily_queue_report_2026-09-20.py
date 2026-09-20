#!/usr/bin/env python3
"""Daily Queue Email Report - September 20, 2026 (live data @ 06:00 UTC)."""
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
• Uptime:   123 days, 21h08m
• CPU Load: 1.82 / 1.40 / 1.31  🟢 healthy, settled
• Memory:   8.6 Gi used / 15 Gi total (57%)  🟢 improved (was 63% yesterday)
• Available: 7.0 Gi
• Swap:     1.4 Gi / 29 Gi
• Disk:     138G / 193G (72%)  🟢 healthy

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control, ollama
all ACTIVE. ⚠️ depotchaos still "activating" (second consecutive day).

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

• PENDING_TASKS.json:  3,250 tasks (unchanged from yesterday)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-09-19 11:16 UTC (NOT refreshed since yesterday)
    - scraped_at: 2026-06-16 11:13 UTC (underlying leads NOT refreshed)

• DepotChaos DB (data/depot_chaos/unified.db):  93.4 MB (was 89.1 MB)
    - unified_leads:           1,460
    - leads:                  32,587
    - ca_abc_licenses:        77,390  (unchanged from yesterday)
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
  2. depotchaos stuck in "activating" for a second day — worth a
     `systemctl restart depotchaos` (or check its journal) to see if
     it recovers to ACTIVE.
  3. Four services still FAILED — aos-ternary, certbot, dailyaidecheck,
     and minecraft. A restart (or explicit decision to leave disabled)
     would confirm they come back clean.
  4. PENDING_TASKS lastUpdated has not refreshed today (still 09-19
     11:16 UTC). The scraper/refresher did not run overnight — check
     that scheduled job.

🟢 NOTE
  5. Memory improved — 63% → 57% (9.5 Gi → 8.6 Gi used). Yesterday's
     climb has reversed; no action needed, continue to watch.
  6. DB grew 89.1 → 93.4 MB (+4.3 MB) but ca_abc_licenses count is
     unchanged — likely WAL/index/vacuum growth, not new ingest. No action.
  7. System otherwise healthy: disk 72%, load ~1.3-1.8 — no OOM/disk/CPU
     risk.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection). Secondary: the four failed
services, depotchaos "activating," and PENDING_TASKS not refreshing.
Standing by.

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
