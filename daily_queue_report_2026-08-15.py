#!/usr/bin/env python3
"""
Daily Queue Email Report - August 15, 2026
Sends comprehensive queue and system status report to Captain.
Live data collected at runtime (2026-08-15 06:05 UTC).
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_daily_queue_report():
    smtp_server = "smtp.hostinger.com"
    smtp_port = 465
    email = "miles@myl0nr0s.cloud"
    password = "Myl0n.R0s"
    recipient = "Antonio.hudnall@gmail.com"

    current_date = datetime.now().strftime("%A, %B %d, %Y")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    subject = f"📊 Daily Queue Report — {datetime.now().strftime('%B %d, %Y')}"

    body = f"""Good morning, Captain!

Here is your daily queue and system status report for {current_date}.

═══════════════════════════════════════════════════════════════════════════
                           SYSTEM HEALTH STATUS
═══════════════════════════════════════════════════════════════════════════

Generated: {current_time}
Uptime: 87 days, 21 hours

COMPONENT STATUS:
┌──────────────────────────┬───────────┬──────────────────────────────────┐
│ Component                │ Status    │ Details                          │
├──────────────────────────┼───────────┼──────────────────────────────────┤
│ Brain Core v4.5          │ 🟢 ACTIVE │ tick 103,939, signal 0.895      │
│ BHSI v4                  │ 🟢 ACTIVE │ systemd active, 72 BPM           │
│ Mission Control v2       │ 🟢 RUNNING │ port 8080                       │
│ Ollama Model Server      │ 🟢 ONLINE  │ Mortimer resident (3.7 GiB)     │
│ Roblox Bridge            │ 🟢 ACTIVE │ PID 289318                       │
│ Minecraft Server         │ 🟢 ACTIVE │ Java ~3.4 GiB                    │
│ OpenClaw Gateway         │ 🟢 ONLINE  │ ~4.0 GiB RAM (grown since yday) │
│ DepotChaos DB            │ 🟢 HEALTHY │ lead pipeline active             │
│ Cron Scheduler           │ 🟡 STABLE  │ ~34 jobs, 2 recurring errors     │
└──────────────────────────┴───────────┴──────────────────────────────────┘

SYSTEM RESOURCES:
• CPU Load:     8.51 / 8.78 / 8.43   🟡 ELEVATED (was 3.67 yesterday)
• Memory:       12Gi used / 15Gi total (80%)
• Memory Avail: 3.2Gi
• Swap:         3.1Gi used / 29Gi total
• Disk:         137G used / 193G total (71%)

TOP PROCESSES BY MEMORY:
  • OpenClaw Gateway: 4.0 GiB  — main session (grown from 1.3 GiB)
  • Java (Minecraft): 3.4 GiB  — Paper server
  • Ollama:           2.0 GiB  — Mortimer resident + embeddings
  • Python (Brain):   ~195 MiB — complete_brain_v45.py

NOTE: CPU load has risen back to ~8.5 after yesterday's recovery to 3.67.
      Memory is also up — 80% (vs 67% yesterday). Primary driver is the
      OpenClaw Gateway, which has grown to ~4.0 GiB (was ~1.3 GiB). 6
      Minecraft society agents are running. Memory is holding at the 80%
      warning threshold; no OOM yet, 3.2 GiB still available.

═══════════════════════════════════════════════════════════════════════════
                           QUEUE STATUS
═══════════════════════════════════════════════════════════════════════════

DARK FACTORY:
• 48 production orders — all completed, factory idle (unchanged)

DEPOTCHAOS DATABASE:
• Lead import/enrichment pipeline active

PATRICIA REPORTS:
• 384 reports on file

QUEUE DIRECTORY:
• 74 files in /queue/ (historical daily status reports)
• No active queue-processing jobs detected

MILES INBOX:
• Daily email check cron healthy

═══════════════════════════════════════════════════════════════════════════
                           CRON JOB HEALTH
═══════════════════════════════════════════════════════════════════════════

🔴 JOBS IN ERROR (2, unchanged from yesterday):
  • Weekly Competitor Report (Mon 9AM UTC) — timeout (300s limit)
  • Monthly Document Review (1st, 9AM) — "message is too long"

🟢 HEALTHY HIGHLIGHTS:
  • Unified AOS Health Check (10m) ✅
  • Ollama Model Keepalive (30m) ✅
  • miles-waste-emailer (30m) ✅ (script disabled per orders)
  • Auto GitHub Push (30m) ✅
  • Daily Email Check ✅
  • Daily Data Scraper (2AM) ✅
  • Daily DepotChaos Lead Import (3AM) ✅
  • Daily SFX Gen (5AM) ✅
  • Daily Queue Status (6AM) ✅
  • Patricia + Jordan Standup (9AM) ✅

═══════════════════════════════════════════════════════════════════════════
                           NOTABLE CHANGES SINCE LAST REPORT
═══════════════════════════════════════════════════════════════════════════

⚠️ WATCH:
  • CPU load back up: 3.67 → 8.5 (Minecraft agents 6, OpenClaw growth)
  • Memory up: 67% → 80% — OpenClaw Gateway grew 1.3 GiB → 4.0 GiB
  • Swap up: 934Mi → 3.1Gi (still comfortable vs 29Gi total)

✅ STABLE:
  • Disk steady at 71% (137G/193G)
  • Same 2 recurring cron errors (no new failures)
  • Brain/BHSI/Mission Control all active and healthy
  • Factory idle (48 orders complete)

═══════════════════════════════════════════════════════════════════════════
                           ACTION ITEMS
═══════════════════════════════════════════════════════════════════════════

🟡 WATCH:
  1. MEMORY CREEP — OpenClaw Gateway now 4.0 GiB (from 1.3 GiB).
     Consider restarting the gateway session if it keeps growing;
     currently holding at 80% with 3.2 GiB free.

  2. FIX WEEKLY COMPETITOR REPORT (recurring timeout)
     → Run manually: python3 skills/browser-agent/examples/competitor_monitor.py

  3. FIX MONTHLY DOCUMENT REVIEW DELIVERY
     → "message too long" — switch to email or chunk output

  4. SENDGRID API KEY
     → Still pending; blocks email verification + campaign pipelines

═══════════════════════════════════════════════════════════════════════════

Overall: System is healthy but memory and CPU load have climbed since
yesterday. The OpenClaw Gateway is the main new memory consumer (grown to
4 GiB). Still 3.2 GiB free with 29 GiB swap headroom, so no immediate risk,
but worth watching if the trend continues. Same 2 recurring cron errors
remain. Everything else green.

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
    print(f"   Timestamp: {current_time}")
    return True

if __name__ == "__main__":
    send_daily_queue_report()
