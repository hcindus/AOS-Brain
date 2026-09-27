#!/usr/bin/env python3
"""Daily Queue Email Report - September 27, 2026 (live data @ 11:38 UTC)."""
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
• Uptime:   131 days, 2h46m
• CPU Load: 0.73 / 0.99 / 0.99  🟢 healthy, settled
• Memory:   8.9 Gi used / 15 Gi total  🟡 up from 8.0 Gi (09-26)
• Available: 6.7 Gi
• Swap:     1.5 Gi / 29 Gi
• Disk:     140G / 193G (73%)  🟢 stable

Core services: ✅ aos-brain-v4, aos-bhsi-v4, aos-mission-control, ollama
all ACTIVE. ⚠️ depotchaos still "activating" (NINTH consecutive day).

⚠️ 4 services in FAILED state — aos-ternary, certbot, dailyaidecheck,
and minecraft. society-agents.service remains disabled/inactive.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db → email_queue):  207 emails — ALL status "ready"
    - campaign_id: capton_hospitality_202607  (207)
    - sent_at ALL NULL  → 0 sent all-time  🔴 STILL STALLED

• PENDING_TASKS.json:  3,450 tasks (up 50 from 3,400 on 09-26)
    - source: CA_SOS_Scraper  (100% — synthetic/mock leads, do not send)
    - task_type: outreach_email (100%)
    - lastUpdated: 2026-09-27 11:15 UTC  ✅ REFRESHED today

• Patricia's Factory (data/factory/dark_factory.db):
    - production_orders: 48 — ALL completed ✅, 0 active/queued
    - No open build orders; factory idle this week (+0 new / +0 completed)

• DepotChaos DB (data/depot_chaos/unified.db):  89 MB (unchanged)
    - unified_leads:  1,460
    - leads:         32,587
    - ca_abc_licenses: 77,390
    - enriched_leads:   919
    - verified_leads:     1
    - psd_customers:    501

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
  2. depotchaos stuck in "activating" for a NINTH day — worth a
     `systemctl restart depotchaos` (or check its journal) to see if it
     recovers to ACTIVE.
  3. Four services still FAILED — aos-ternary, certbot, dailyaidecheck,
     and minecraft. A restart (or explicit decision to leave disabled)
     would confirm they come back clean.

🟢 NOTE
  4. PENDING_TASKS refresher RAN — lastUpdated 09-27 11:15 UTC and count
     ticked up 3,400 → 3,450. Scraper/refresher remains on schedule. ✅
  5. Load settled (0.73) — no resource pressure. Memory ticked up
     8.0 → 8.9 Gi but well within headroom. ✅
  6. Factory clear — all 48 production orders completed, nothing queued.
  7. Disk stable at 73% — no OOM/disk/CPU risk.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection). Secondary: depotchaos
"activating" for a ninth day and the four failed services. Standing by.

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
