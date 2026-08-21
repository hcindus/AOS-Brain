#!/usr/bin/env python3
"""Daily Queue Email Report - August 21, 2026 (live data)."""
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
• Uptime:   94 days, 2h 46m
• CPU Load: 1.01 / 1.25 / 1.14  🟢 healthy
• Memory:   5.9 Gi used / 15 Gi total (39%)
• Available: 9.7 Gi  🟢 ample headroom
• Swap:     1.5 Gi / 29 Gi
• Disk:     143G / 193G (74%)

Top processes (mem):
  openclaw-gateway           20.2%
  ollama runner (active)      2.6%
  openclaw-tui                2.2%
  systemd-journald            1.6%
  complete_brain_v45.py       1.1%

Core services: ✅ Brain v4.5, Ollama serve + runner, n8n, gateway.
Load steady and low (was 0.92 yesterday, now 1.01) — system is calm.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Pending emails:        99  (down 1 from 100)
    - teriyaki_thermal_paper_q2_2026: 98
    - outreach:            1
• Follow-up queue:       100
• Sent last 24h / 7d:    0 / 0  ⚠️ stalled
• Sent all-time:         170
• DepotChaos DB:         22.07 MB, populated
    - vendors:            111,349  (up from 110,900)
    - teriyaki_madness:   190
    - vendor_interactions: 0

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. 99 emails still stuck in the queue — 0 sent in 7 days.
     Root cause remains SendGrid API key / SMTP auth for the
     DepotChaos engine. Confirm SENDGRID_API_KEY is set and DNS
     (DKIM/SPF/DMARC) is live in Hostinger for myl0nr0s.cloud.

🟡 IMPORTANT
  2. CREAM Realtor Lead Scraper keeps timing out (300s cap) —
     bump timeout to 900s or chunk the 1000-prospect generation.
  3. Monthly Document Review fails on Telegram message length —
     3 consecutive failures; confirm file-output + 2-line summary
     fix is applied.

🟢 NOTE
  4. DepotChaos vendors grew to 111,349 (+449) — lead DB healthy.
  5. 3 duplicate/stale "Git Push Schedule" cron jobs (disabled)
     still carry errors — safe to delete to reduce registry noise.

All core systems operational. Load and memory are in great shape.
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
