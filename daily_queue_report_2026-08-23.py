#!/usr/bin/env python3
"""Daily Queue Email Report - August 23, 2026 (live data)."""
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
• Uptime:   96 days, 2h 46m
• CPU Load: 0.97 / 1.07 / 1.04  🟢 healthy
• Memory:   9.5 Gi used / 15 Gi total (63%)  🟢 acceptable
• Available: 6.1 Gi
• Swap:     3.7 Gi / 29 Gi
• Disk:     115G / 193G (60%)  🟢 healthy

Top processes (mem):
  ollama runner       23.8%   ~3.9 Gi
  openclaw-gateway    22.7%   ~3.7 Gi
  ollama runner #2     2.1%
  systemd-journald     1.0%
  n8n                  1.0%

Core services: ✅ depotchaos, roblox-bridge active.
Load steady and healthy. Memory down from yesterday's 80% peak.

⚠️ Service flags:
  • society-agents.service — inactive (should auto-restart)
  • minecraft.service      — failed (needs restart)

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Pending emails:        99  (unchanged)
    - teriyaki_thermal_paper_q2_2026: 99
• Failed emails:         29
• Follow-up queue:       100
• Sent last 24h / 7d:    0 / 0  ⚠️ still stalled
• Sent all-time:         170

• DepotChaos DB:         22.2 MB, populated
    - vendors:            112,247  (up from 111,797, +450)
    - teriyaki_madness:   190
    - vendor_interactions: 0

════════════════════════════════════════════
  CRON / AUTOMATION HEALTH
════════════════════════════════════════════
• Total jobs: 37 | OK: 33 | ERROR: 4

🔴 FAILING JOBS
  1. CREAM Realtor Lead Scraper — timed out (300s limit)
  2. Mirror Audit (Weekly) — Telegram recipient @heartbeat
     could not be resolved to a numeric chat ID
  3. Weekly Blog Post (Hospitality) — same @heartbeat error
  4. Monthly Document Review (Jordan + Redactor)
     — GrammyError 400 "message is too long" (3 consecutive)

🟢 All other jobs healthy (Git pushes, health checks, keepalive,
   lead scrapers, standups, price sync, waste emailer, etc.).

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. 99 emails stuck — 0 sent in 7+ days. Root cause is now a
     Hostinger SMTP sender-address rejection:
     `info@psdepot.com` is "not owned by user miles@myl0nr0s.cloud".
     Fix: either verify info@psdepot.com as a sender in Hostinger,
     or switch the DepotChaos engine to send from miles@myl0nr0s.cloud.
     Confirm DKIM/SPF/DMARC records are live for myl0nr0s.cloud.

🟡 IMPORTANT
  2. Fix Telegram @heartbeat delivery — 2 jobs failing because the
     recipient resolves to no numeric chat ID. Point them at a real
     chat ID or disable their announce delivery.
  3. Restart minecraft.service and society-agents.service.
  4. Monthly Document Review still hitting the Telegram 400-char
     limit — apply the "write-to-file + 2-line summary" fix.

🟢 NOTE
  5. DepotChaos vendors grew to 112,247 (+450) — lead DB healthy.
  6. Memory eased to 63% (was 80% yesterday) — no immediate OOM risk.

All core systems operational. Primary concern remains the stalled
99-email queue (sender-address rejection) plus 4 errant cron jobs.
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
