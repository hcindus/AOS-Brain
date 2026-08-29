#!/usr/bin/env python3
"""Daily Queue Email Report - August 29, 2026 (live data)."""
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

body = f"""Good morning, Captain!

Daily queue & system status report for {now.strftime('%A, %B %d, %Y')}.

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

════════════════════════════════════════════
  SYSTEM HEALTH
════════════════════════════════════════════
• Uptime:   102 days, 2h46m
• CPU Load: 1.04 / 0.92 / 0.96  🟢 healthy
• Memory:   3.9 Gi used / 15 Gi total (26%)  🟢 healthy
• Available: 11 Gi
• Swap:     5.3 Gi / 29 Gi
• Disk:     133G / 193G (69%)  🟢 healthy

Core services: ✅ depotchaos-api, aos-brain-v4.5, aos-bhsi-v4,
mission-control, ollama, darkfactory-worker, collections-worker,
legal-worker, media-worker, psd-sales-automation, testimonials-api.

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• Email queue (unified.db):  207 emails — ALL status "ready"
    - campaign: capton_hospitality_202607  (207)
• Sent last 24h / 7d / all-time:  0 / 0 / 0  🔴 still stalled

• PENDING_TASKS.json:  2,950 tasks
    - source: CA_SOS_Scraper  (2,950)
    - ⚠️ NOTE: these are MOCK leads (per established guidance,
      the CA_SOS_Scraper source generates synthetic records —
      not real prospects; do not send).

• DepotChaos DB (data/depot_chaos/unified.db):  75.5 MB
    - unified_leads:      1,460
    - leads:             31,090
    - ca_abc_licenses:   74,521
    - enriched_leads:       919

════════════════════════════════════════════
  CRON / AUTOMATION HEALTH
════════════════════════════════════════════

🔴 FAILING JOBS
  1. Mirror Audit (Weekly) — Telegram recipient @heartbeat
     unresolved (getChat 400: chat not found) — 1 consecutive error
  2. Weekly Blog Post (Hospitality) — same @heartbeat error — 1 error
  3. Monthly Document Review (Jordan + Redactor)
     — GrammyError 400 "message is too long" — 3 consecutive errors

🟢 All other jobs healthy (Git pushes, health checks, keepalive,
   lead scrapers, standups, price sync, waste emailer, SFX, etc.).

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. Email queue still stalled — 207 ready emails (capton_hospitality
     campaign), 0 sent. Root cause remains the Hostinger SMTP
     sender-address rejection (info@psdepot.com not owned by
     miles@myl0nr0s.cloud). Fix: verify info@psdepot.com as a sender
     in Hostinger, or switch the engine to send from
     miles@myl0nr0s.cloud. Confirm DKIM/SPF/DMARC for myl0nr0s.cloud.

🟡 IMPORTANT
  2. Fix Telegram @heartbeat delivery — 2 jobs failing because the
     recipient resolves to no numeric chat ID.
  3. Monthly Document Review still hitting Telegram 400-char limit —
     apply the "write-to-file + 2-line summary" fix (3 consecutive).

🟢 NOTE
  4. PENDING_TASKS at 2,950 are all CA_SOS_Scraper mock leads —
     no real outreach needed; do not inject more synthetic leads.
  5. System healthy: load ~1.0, memory 26%, disk 69% — no OOM/disk risk.

All core systems operational. Primary concern remains the stalled
207-email queue (sender-address rejection) plus 3 errant cron jobs.
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
