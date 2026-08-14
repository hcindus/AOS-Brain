#!/usr/bin/env python3
"""Daily Queue Email Report — August 14, 2026 (11:37 UTC run)."""
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

smtp_server = "smtp.hostinger.com"
smtp_port = 465
email = "miles@myl0nr0s.cloud"
password = "Myl0n.R0s"
recipient = "Antonio.hudnall@gmail.com"

now = datetime.now()
subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')}"

body = f"""Good morning, Captain!

Here is your daily queue and system status report for {now.strftime('%A, %B %d, %Y')}.

═══════════════════════════════════════════════════════════════════════════
                           SYSTEM HEALTH STATUS
═══════════════════════════════════════════════════════════════════════════

Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}
Uptime: 87 days, 2 hours

SYSTEM RESOURCES (live):
• CPU Load:     6.60 / 6.62 / 7.07   🟡 ELEVATED
• Memory:       12Gi used / 15Gi total (80%)
• Memory Avail: 3.0Gi
• Swap:         1.0Gi used / 29Gi total
• Disk:         137G used / 193G total (71%)

TOP PROCESSES BY MEMORY:
  • Ollama runner (Mortimer):  3.9 GiB
  • Java (Minecraft Paper):    3.8 GiB
  • OpenClaw Gateway:          2.2 GiB
  • Python (Brain v4.5):       261 MiB — complete_brain_v45.py
  • Minecraft society agents:  5 running (livia, julius, titus, chelios, forge2)

NOTE: Load has ticked back up (3.67 → 6.60) since the 06:05 snapshot.
      Primary drivers: Minecraft Paper server (62% CPU) + 5 society agents
      (13–47% CPU each) + a second Ollama runner at 55% CPU. Memory usage
      climbed 10Gi → 12Gi, available down to 3.0Gi. Still within limits,
      but worth watching if the society agent count stays elevated.

═══════════════════════════════════════════════════════════════════════════
                           QUEUE STATUS
═══════════════════════════════════════════════════════════════════════════

DARK FACTORY:
• No active production orders (factory idle)

FACTORY QUEUE DIRECTORY (/factory_queue/):
• 10 files — mostly historical task briefs + URGENT build requests:
  - URGENT_BUILD_CREAM_MOBILE.md
  - URGENT_BUILD_NOGNOG_MOBILE.md
  - URGENT_BUILD_REGGIESTARR_RS80.md
  - URGENT_BRAIN_V4_RESTORATION.md
  (These are standing/pending build requests, not active jobs.)

QUEUE DIRECTORY (/queue/):
• 74 files — historical daily status reports (archive)

DEPOTCHAOS DATABASE:
• depot_chaos.db — currently 0 bytes (empty file; pipeline writes to live DB
  elsewhere). Lead import/enrichment cron still scheduled daily at 03:00 UTC.

═══════════════════════════════════════════════════════════════════════════
                           CRON JOB HEALTH
═══════════════════════════════════════════════════════════════════════════

Total Jobs: 44 | Enabled: 37 | Errors: 2 (recurring)

🔴 JOBS IN ERROR (2, both previously documented):
  1. Weekly Competitor Report (Mon 9AM) — timeout (300s), 3 consecutive fails
     → Run manually: python3 skills/browser-agent/examples/competitor_monitor.py
  2. Monthly Document Review (1st, 9AM) — "message is too long" (Telegram 400)
     → Switch delivery to email or chunk the output

🟢 HEALTHY HIGHLIGHTS (all last-runs OK):
  • Unified AOS Health Check (10m) ✅
  • aos-layer-feeder (5m) ✅
  • Ollama Model Keepalive (30m) ✅
  • miles-waste-emailer (30m) ✅
  • Auto GitHub Push (30m) ✅
  • Minecraft Agent Rotation (12h) ✅
  • Daily Email Check ✅
  • Daily Data Scraper (2AM) ✅
  • Daily DepotChaos Lead Import (3AM) ✅
  • Daily SFX Gen (5AM) ✅
  • daily-lead-scraper (6AM) ✅
  • Daily Queue Status (6AM) ✅
  • CREAM Realtor Scraper ✅
  • Lead Piping Scraper ✅
  • Patricia + Jordan Standup (9AM) ✅
  • Monthly Legal / GitHub / VPS Audits ✅

═══════════════════════════════════════════════════════════════════════════
                           ACTION ITEMS
═══════════════════════════════════════════════════════════════════════════

🟡 RECOMMENDED:
  1. FIX WEEKLY COMPETITOR REPORT (3 consecutive timeouts)
     → Manually run once to confirm the script isn't hung.

  2. FIX MONTHLY DOCUMENT REVIEW DELIVERY
     → "message too long" — switch to email or chunk output.

  3. SENDGRID API KEY
     → Still pending; blocks auth-system email verification + campaign flows.

  4. WATCH CPU LOAD
     → Load climbed back to ~6.6 and memory to 12Gi/15Gi. If the Minecraft
       society agent count stays at 5+ and load trends higher, consider
       trimming one agent or capping Paper's CPU.

═══════════════════════════════════════════════════════════════════════════

Overall: System healthy but moderately loaded. CPU and memory have climbed
since this morning (Minecraft Paper + 5 society agents + dual Ollama runners).
Disk steady at 71%, swap minimal. Same 2 recurring cron errors remain — both
low-impact and already documented. No new failures, no urgent production
issues.

Standing by, Captain.

- Miles 🚀
Autonomous Operations Engine
Performance Supply Depot LLC / AGI Company
"""

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = recipient
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
    server.login(email, password)
    server.sendmail(email, recipient, msg.as_string())

print("✅ Daily queue email report sent to Captain!")
print(f"   To: {recipient}")
print(f"   Subject: {subject}")
print(f"   Timestamp: {now.strftime('%Y-%m-%d %H:%M UTC')}")
