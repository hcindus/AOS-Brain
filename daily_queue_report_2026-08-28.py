#!/usr/bin/env python3
"""Daily Queue Email Report - August 28, 2026 (live data)."""
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
• Uptime:   101 days, 2h46m
• CPU Load: 0.55 / 0.74 / 0.88  🟢 healthy
• Memory:   3.9 Gi used / 15 Gi total (26%)  🟢 healthy
• Available: 11 Gi
• Swap:     5.3 Gi / 29 Gi
• Disk:     132G / 193G (69%)  🟢 healthy

Top processes (mem):
  openclaw-gateway      8.4%   ~1.3 Gi
  ollama runner         2.0%
  ollama serve          1.6%
  whatsapp-bridge       1.5%
  systemd-journald      1.2%
  complete_brain_v45    1.1%
  n8n                   1.0%
  temporal-server       0.7%

Note: memory usage dropped markedly (26% vs 63% on prior runs) —
buff/cache now ~9.3 Gi with 11 Gi available. No OOM pressure.

Core services: ✅ depotchaos, temporal, n8n, brain v4.5 active.

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

• DepotChaos DB:         22.7 MB, populated
    - vendors:            114,488  (up from 113,592, +896)
    - teriyaki_madness:   190
    - vendor_interactions: 0

════════════════════════════════════════════
  CRON / AUTOMATION HEALTH
════════════════════════════════════════════

🔴 FAILING JOBS
  1. Mirror Audit (Weekly) — Telegram recipient @heartbeat
     could not be resolved to a numeric chat ID
     (getChat 400: chat not found)
  2. Weekly Blog Post (Hospitality) — same @heartbeat error
  3. Monthly Document Review (Jordan + Redactor)
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
  5. DepotChaos vendors grew to 114,488 (+896) — lead DB healthy.
  6. Memory dropped to 26% used, disk steady at 69% — no immediate
     OOM/disk risk.

All core systems operational. Primary concern remains the stalled
99-email queue (sender-address rejection) plus 3 errant cron jobs.
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
