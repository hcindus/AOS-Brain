#!/usr/bin/env python3
"""Daily Queue Email Report - September 19, 2026 (live data @ 11:38 UTC)."""
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

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')} (midday refresh).

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   123 days, 2h46m
• CPU Load: 0.98 / 1.25 / 1.37  🟢 healthy, settled
• Memory:   9.5 Gi used / 15 Gi total (63%)  🟡 rising (was 55% yesterday)
• Available: 6.1 Gi
• Swap:     1.4 Gi / 29 Gi
• Disk:     138G / 193G (72%)  🟢 healthy

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control, ollama
all ACTIVE. ⚠️ depotchaos is "activating" (was active yesterday).

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

• PENDING_TASKS.json:  3,250 tasks (was 3,200 yesterday — +50)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-09-19 11:16 UTC (refreshed today)
    - scraped_at: 2026-06-16 11:13 UTC (underlying leads NOT refreshed)

• DepotChaos DB (data/depot_chaos/unified.db):  89.1 MB (was 77.2 MB)
    - unified_leads:           1,460
    - leads:                  32,587
    - ca_abc_licenses:        77,390  (was 74,521 — +2,869 new)
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
  2. Memory climbing — 19% → 55% → 63% over three days (9.5 Gi used).
     Worth identifying the top consumers before it nears the ceiling.
  3. depotchaos dropped to "activating" (was active yesterday). Watch
     whether it returns to ACTIVE or needs a restart.
  4. Four services still FAILED — aos-ternary, certbot, dailyaidecheck,
     and minecraft. A `systemctl restart` (or a decision to leave them
     disabled) would confirm they come back clean.
  5. PENDING_TASKS crept 3,200 → 3,250 (+50 CA_SOS_Scraper mock leads).
     These are synthetic — do not inject or send.

🟢 NOTE
  6. ca_abc_licenses grew +2,869 (74,521 → 77,390) — new ABC license
     records ingested; DB up ~12 MB to 89.1 MB. Normal ingest, no action.
  7. System otherwise healthy: disk 72%, load ~1.0-1.4 — no OOM/disk/CPU
     risk. Memory trend is the primary new flag to watch.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection). Secondary: the failed
services, depotchaos "activating," and the three-day memory climb.
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
