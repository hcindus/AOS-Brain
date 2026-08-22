#!/usr/bin/env python3
"""Daily Queue Email Report - August 22, 2026 (live data)."""
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
• Uptime:   95 days, 2h 46m
• CPU Load: 0.99 / 1.03 / 0.99  🟢 healthy
• Memory:   12 Gi used / 15 Gi total (80%)  ⚠️ elevated
• Available: 3.1 Gi  ⚠️ watch OOM risk
• Swap:     6.6 Gi / 29 Gi
• Disk:     144G / 193G (75%)

Top processes (mem):
  ollama runner (48.0%)    7.87 Gi  ⚠️ largest consumer
  openclaw-gateway (19.7%) 3.23 Gi
  ollama runner #2  (2.0%)
  complete_brain_v45.py x2 (1.0% ea)
  systemd-journald (0.9%)

Core services: ✅ Brain v4.5, Ollama serve + runner, n8n, gateway.
Load is low and steady. Note: memory climbed to 80% (was 39% yesterday)
driven by an Ollama runner holding ~7.9 Gi — monitor for OOM risk.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Pending emails:        99  (unchanged)
    - teriyaki_thermal_paper_q2_2026: 98
    - outreach:            1
• Follow-up queue:       100
• Sent last 24h / 7d:    0 / 0  ⚠️ still stalled
• Sent all-time:         170
• DepotChaos DB:         22.16 MB, populated
    - vendors:            111,797  (up from 111,349, +448)
    - teriyaki_madness:   190
    - vendor_interactions: 0

════════════════════════════════════════════
  CRON / AUTOMATION HEALTH
════════════════════════════════════════════
• Total jobs: 37 | OK: 36 | ERROR: 1

🔴 FAILING JOB
  1. Monthly Document Review (Jordan + Redactor)
     — 3 consecutive errors, last: GrammyError 400
       "message is too long" (Telegram 400-char limit).
     — Fix: write full report to file, send 2-line summary only.

🟢 All other jobs healthy (Git pushes, health checks, keepalive,
   lead scrapers, standups, price sync, waste emailer, etc.).

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. 99 emails stuck — 0 sent in 7+ days. Root cause remains
     SendGrid API key / SMTP auth for the DepotChaos engine.
     Confirm SENDGRID_API_KEY is set and DNS (DKIM/SPF/DMARC)
     is live in Hostinger for myl0nr0s.cloud.

🟡 IMPORTANT
  2. Memory at 80% — an Ollama runner is holding ~7.9 Gi.
     If load spikes, consider unloading idle models or restarting
     the runner to reclaim RAM before OOM.
  3. Monthly Document Review failing (Telegram length). Apply the
     "write-to-file + 2-line summary" fix — same as the legal
     compliance job which already has it.

🟢 NOTE
  4. DepotChaos vendors grew to 111,797 (+448) — lead DB healthy.
  5. Core services + 36/37 cron jobs operational.

All core systems operational. Primary concerns: the stalled 99-email
queue (SendGrid auth) and elevated memory usage. Standing by.

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
