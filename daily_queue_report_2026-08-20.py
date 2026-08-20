#!/usr/bin/env python3
"""Daily Queue Email Report - August 20, 2026 (live data)."""
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

body = f"""Good afternoon, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')}.

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   93 days, 2h 46m
• CPU Load: 0.92 / 1.03 / 1.07  🟢 healthy
• Memory:   3.5 Gi used / 15 Gi total (23%)
• Available: 12 Gi  🟢 ample headroom
• Swap:     1.6 Gi / 29 Gi
• Disk:     142G / 193G (74%)

Top processes (mem):
  openclaw-gateway            7.9%
  ollama runner (active model) 2.2%
  openclaw-tui                1.6%
  n8n                         1.0%
  complete_brain_v45.py       0.7%

Core services: ✅ Brain v4.5, Ollama serve + runner, n8n, gateway.
Load has dropped dramatically vs. yesterday (was 8.39, now 0.92) —
RS-80 build activity has settled.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Pending emails:        100  (unchanged)
    - teriyaki_thermal_paper_q2_2026: 99
    - outreach:            1
• Sent last 24h / 7d:    0 / 0  ⚠️ stalled
• Sent all-time:         170
• DepotChaos DB:         21.99 MB, populated
    - vendors:            110,900  (up from 109,969)
    - teriyaki_madness:   190
    - vendor_interactions: 0

════════════════════════════════════════════
  CRON HEALTH — 44 jobs (35 enabled)
════════════════════════════════════════════
🔴 2 active jobs in error state:
  • CREAM Realtor Lead Scraper — timeout (2 consecutive errors)
  • Monthly Document Review — 3 consecutive errors
    (Telegram "message is too long")

🟡 Stale/disabled jobs flagged for cleanup (not firing):
  • 3 duplicate "Git Push Schedule" jobs (33/53/97 errors) — disabled
  • 1 disabled "Daily Queue Email Report" (5bb713dd) — superseded by
    this active job (6bffa2fa)

✅ All else healthy: git pushes, standups, email check, lead import,
   SFX generation, price sync, scraper, competitor report.

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. 100 emails still stuck in the queue — 0 sent in 7 days.
     Root cause remains SendGrid API key / SMTP auth for the
     DepotChaos engine. Confirm SENDGRID_API_KEY is set and DNS
     (DKIM/SPF/DMARC) is live in Hostinger for myl0nr0s.cloud.

🟡 IMPORTANT
  2. CREAM Realtor Lead Scraper keeps timing out (300s cap) —
     bump timeout to 900s or chunk the 1000-prospect generation.
  3. Monthly Document Review fails on Telegram message length —
     script already instructs file output + 2-line summary; confirm
     the fix is applied (3 consecutive failures now).

🟢 NOTE
  4. 3 duplicate/stale "Git Push Schedule" cron jobs carry 183
     combined errors and are disabled — safe to delete to reduce
     noise in the cron registry.
  5. DepotChaos vendors grew to 110,900 (+931) — lead DB healthy.

All core systems operational. Load and memory are in great shape today.
Standing by for your directives.

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
