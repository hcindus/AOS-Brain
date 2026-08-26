#!/usr/bin/env python3
"""Daily Queue Email Report - August 26, 2026 (live data)."""
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
• Uptime:   99 days (14 weeks, 1 day)
• CPU Load: 0.88 / 1.12 / 1.26  🟢 healthy
• Memory:   9.5 Gi used / 15 Gi total (63%)  🟢 acceptable
• Available: 6.1 Gi
• Swap:     3.5 Gi / 29 Gi
• Disk:     130G / 193G (68%)  🟢 healthy

Top processes (mem):
  ollama runner       23.8%   ~3.9 Gi
  openclaw-gateway    23.6%   ~3.9 Gi
  ollama runner #2     2.2%
  systemd-journald     1.3%
  whatsapp-bridge      1.3%
  complete_brain_v45   0.9%

Core services: ✅ depotchaos, roblox-bridge active.

⚠️ Service flags:
  • society-agents.service — inactive (should auto-restart)
  • minecraft.service      — failed (needs restart)

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Pending emails:        99  (unchanged)
    - teriyaki_thermal_paper_q2_2026: 98
    - outreach:                      1
• Failed emails:         29
• Follow-up queue:       100
• Sent last 24h / 7d:    0 / 0  ⚠️ still stalled
• Sent all-time:         170

• DepotChaos DB:         22 MB, populated
    - vendors:            113,592  (up from 112,247, +1,345)
    - teriyaki_madness:   190
    - vendor_interactions: 0

════════════════════════════════════════════
  CRON / AUTOMATION HEALTH
════════════════════════════════════════════

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
  1. 99 emails still stuck — 0 sent in 7+ days. Root cause remains
     the Hostinger SMTP sender-address rejection:
     `info@psdepot.com` is "not owned by user miles@myl0nr0s.cloud".
     Fix: verify info@psdepot.com as a sender in Hostinger, or switch
     the DepotChaos engine to send from miles@myl0nr0s.cloud.
     Confirm DKIM/SPF/DMARC records are live for myl0nr0s.cloud.

🟡 IMPORTANT
  2. Fix Telegram @heartbeat delivery — 2 jobs failing because the
     recipient resolves to no numeric chat ID.
  3. Restart minecraft.service and society-agents.service.
  4. Monthly Document Review still hitting the Telegram 400-char
     limit — apply the "write-to-file + 2-line summary" fix.

🟢 NOTE
  5. DepotChaos vendors grew to 113,592 (+1,345) — lead DB healthy.
  6. Memory steady at 63%, disk at 68% — no immediate OOM/disk risk.

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
