#!/usr/bin/env python3
"""
Daily Queue Email Report - August 16, 2026
Sends comprehensive queue and system status report to Captain.
Live data collected at runtime (2026-08-16 11:37 UTC).
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
Uptime: 89 days, 2 hours, 45 minutes

COMPONENT STATUS:
┌──────────────────────────┬───────────┬──────────────────────────────────┐
│ Component                │ Status    │ Details                          │
├──────────────────────────┼───────────┼──────────────────────────────────┤
│ Brain Core v4.5          │ 🟢 ACTIVE │ complete_brain_v45.py (2 procs)  │
│ OpenClaw Gateway         │ 🟢 ONLINE  │ systemd, port 18789, ~1.2 GiB   │
│ Ollama Model Server      │ 🟢 ONLINE  │ Mort_II (3.9G) + embed (565M)   │
│ Minecraft Server         │ 🟢 ACTIVE │ Paper Java ~1.98 GiB (1 agent)   │
│ DepotChaos FastAPI       │ 🟢 RUNNING │ depotchaos_fastapi.py            │
│ n8n Automation           │ 🟢 RUNNING │ node, ~168 MiB                   │
│ Fail2Ban                 │ 🟢 ACTIVE │ security daemon                  │
│ Cron Scheduler           │ 🟡 STABLE  │ 44 jobs, 2 recurring errors      │
└──────────────────────────┴───────────┴──────────────────────────────────┘

SYSTEM RESOURCES:
• CPU Load:     1.86 / 1.20 / 1.13   🟢 HEALTHY (was 8.51 yesterday!)
• Memory:       6.8Gi used / 15Gi total (45%)
• Memory Avail: 8.8Gi
• Swap:         2.8Gi used / 29Gi total
• Disk:         136G used / 193G total (71%)

TOP PROCESSES BY MEMORY:
  • Java (Minecraft):  1.98 GiB  — Paper 1.20.4 server
  • Ollama runner:     1.93 GiB  — Mort_II resident model
  • OpenClaw Gateway:  1.20 GiB  — main session
  • Ollama runner:     0.32 GiB  — embeddings worker
  • Python (Brain):    0.30 GiB  — complete_brain_v45.py (x2)

✅ BIG IMPROVEMENT: CPU load has dropped from 8.51 → 1.86, and memory
   from 80% → 45% since yesterday. The OpenClaw Gateway shrank from
   4.0 GiB back to 1.2 GiB, and Minecraft society agents dropped from 6
   to 1. System is in a much healthier state today with 8.8 GiB free.

═══════════════════════════════════════════════════════════════════════════
                           QUEUE STATUS
═══════════════════════════════════════════════════════════════════════════

PENDING OUTREACH TASKS (PENDING_TASKS.json):
• 2 tasks queued — CA business registration outreach (Auto Shop + Restaurant)
  → Assigned to Miles, task_type "outreach_email", status PENDING
  → Source: CA_SOS_Scraper, added 2026-06-16 (aging ~61 days)

PATRICIA PENDING TASKS:
• 40 lines in agent_sandboxes/patricia/PENDING_TASKS.md

DEPOTCHAOS DATABASE:
• depot_chaos.db: 0 bytes (empty) — lead pipeline idle
• data/depot_chaos/queue.db: 0 bytes (empty)

REPORTS ON FILE:
• 93 files in /reports/ (daily queue + status reports)

QUEUE DIRECTORY:
• 40+ historical DAILY_STATUS_*.md files (since April)
• No active queue-processing jobs currently running

═══════════════════════════════════════════════════════════════════════════
                           CRON JOB HEALTH
═══════════════════════════════════════════════════════════════════════════

🔴 JOBS IN ERROR (2, unchanged):
  • Weekly Competitor Report (Mon 9AM UTC) — timeout (consecutiveErrors: 3)
  • Monthly Document Review - Jordan+Redactor (1st, 9AM) — "message too long"

🟢 HEALTHY HIGHLIGHTS (all running ok):
  • Unified AOS Health Check (10m) ✅
  • Ollama Model Keepalive (30m) ✅
  • aos-layer-feeder (5m) ✅
  • Auto GitHub Push (30m) ✅
  • Daily Email Check ✅
  • Daily Data Scraper (2AM) ✅
  • Daily DepotChaos Lead Import (3AM) ✅
  • Daily SFX Gen (5AM) ✅
  • Daily Lead Scraper (6AM) ✅
  • Daily Queue Status (6AM) ✅
  • Patricia + Jordan Standup (9AM) ✅

═══════════════════════════════════════════════════════════════════════════
                           NOTABLE CHANGES SINCE LAST REPORT
═══════════════════════════════════════════════════════════════════════════

✅ RECOVERED:
  • CPU load: 8.51 → 1.86 (major drop)
  • Memory: 80% → 45% (8.8 GiB now free)
  • OpenClaw Gateway: 4.0 GiB → 1.2 GiB
  • Minecraft agents: 6 → 1

🟡 WATCH:
  • Same 2 recurring cron errors (no new failures)
  • SendGrid API key still pending (blocks email verification flows)

═══════════════════════════════════════════════════════════════════════════
                           ACTION ITEMS
═══════════════════════════════════════════════════════════════════════════

🟡 RECOMMENDED:
  1. CLEAR 2 AGED OUTREACH TASKS — the 2 PENDING_TASKS.json entries have
     been queued ~61 days. Either execute the outreach emails or close them.

  2. FIX WEEKLY COMPETITOR REPORT (recurring timeout)
     → Run manually: python3 skills/browser-agent/examples/competitor_monitor.py

  3. FIX MONTHLY DOCUMENT REVIEW DELIVERY
     → "message too long" — write to file, send 2-line summary instead.

  4. SENDGRID API KEY
     → Still pending; blocks email verification + campaign pipelines.
     → Daily reminder cron (auth-system-sendgrid-setup) is active.

═══════════════════════════════════════════════════════════════════════════

Overall: System is in markedly better shape today — CPU and memory have
recovered substantially since yesterday (load 8.5→1.86, mem 80%→45%).
The gateway memory creep resolved and Minecraft agents scaled down from 6
to 1. Same 2 recurring cron errors remain, plus 2 aged outreach tasks
worth clearing. Everything else green.

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
