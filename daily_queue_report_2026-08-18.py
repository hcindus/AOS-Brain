#!/usr/bin/env python3
"""
Daily Queue Email Report - August 18, 2026
Live data collected at runtime (2026-08-18 11:38 UTC).
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
Uptime: 91 days, 2 hours, 46 minutes

COMPONENT STATUS:
┌──────────────────────────┬───────────┬──────────────────────────────────┐
│ Component                │ Status    │ Details                          │
├──────────────────────────┼───────────┼──────────────────────────────────┤
│ Brain Core v4.5          │ 🟢 ACTIVE │ complete_brain_v45.py (x2, 0.4G) │
│ OpenClaw Gateway         │ 🟢 ONLINE  │ 4.2 GiB resident                 │
│ Ollama Model Server      │ 🟢 ONLINE  │ 2 runners, ~47% CPU active       │
│ Minecraft Server         │ 🟢 ACTIVE │ Java 2.2 GiB @ 47.6% CPU         │
│ Minecraft Society Agents │ 🟢 RUNNING │ 3 node agents @ 25-41% CPU each │
│ n8n Automation           │ 🟢 RUNNING │ node, ~0.2 GiB                   │
│ Cron Scheduler           │ 🟡 STABLE  │ 34 jobs, 1 recurring error       │
└──────────────────────────┴───────────┴──────────────────────────────────┘

SYSTEM RESOURCES:
• CPU Load:     5.80 / 5.24 / 5.03   🟡 ELEVATED
• Memory:       9.7 GiB used / 15 GiB total (65%)
• Memory Avail: 5.9 GiB
• Swap:         4.5 GiB used / 29 GiB total
• Disk:         137G used / 193G total (71%)

TOP PROCESSES BY MEMORY:
  • OpenClaw Gateway:   4.2 GiB  — main session (up from 1.2 GiB)
  • Java (Minecraft):   2.2 GiB  — Paper 1.20.4, 47.6% CPU
  • Ollama runner:      0.3 GiB  — Mort_II inference, 47.4% CPU
  • Brain v4.5 (x2):    0.4 GiB  — complete_brain_v45.py
  • Minecraft agents:   0.6 GiB  — 3 node agents (25-41% CPU)

🟡 NOTE: Load back up to ~5.8 after yesterday's recovery (1.86). Driven by
   Minecraft society agents (3x node @ 25-41% CPU) + Ollama inference +
   Java server. Gateway grew 1.2 → 4.2 GiB again. Worth watching for the
   memory-creep cycle observed in prior days.

═══════════════════════════════════════════════════════════════════════════
                           QUEUE STATUS
═══════════════════════════════════════════════════════════════════════════

PENDING OUTREACH TASKS (PENDING_TASKS.json):
• 0 tasks currently queued — file empty (prior 2 CA outreach tasks cleared)

PATRICIA PENDING TASKS:
• 40 lines in agent_sandboxes/patricia/PENDING_TASKS.md (unchanged)

DEPOTCHAOS DATABASE:
• depot_chaos.db: 0 bytes (empty)
• data/depot_chaos/queue.db: 0 bytes (empty) — lead pipeline idle

REPORTS ON FILE:
• 95 files in /reports/ (daily queue + status reports)

QUEUE DIRECTORY:
• Historical DAILY_STATUS_*.md + research/security task files present
• No active queue-processing jobs currently running

═══════════════════════════════════════════════════════════════════════════
                           CRON JOB HEALTH
═══════════════════════════════════════════════════════════════════════════

Total Jobs: 34 | OK: 33 | ERROR: 1

🔴 JOB IN ERROR (1):
  • Monthly Document Review — Jordan+Redactor (1st, 9AM)
    → "message too long" (consecutiveErrors: 3)

✅ RECOVERED:
  • Weekly Competitor Report (Mon 9AM) — now "ok" (was timeout/3 errors)

🟢 HEALTHY HIGHLIGHTS:
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
                           ACTION ITEMS
═══════════════════════════════════════════════════════════════════════════

🟡 RECOMMENDED:
  1. FIX MONTHLY DOCUMENT REVIEW (recurring "message too long")
     → Payload already instructs writing full report to file and sending
       only a 2-line summary, yet job still exceeds Telegram's 400-char
       limit. Force a rerun and confirm the reply is truncated.

  2. WATCH GATEWAY MEMORY CREEP
     → Gateway grew 1.2 → 4.2 GiB again overnight (same cycle as before).
       If it hits 4+ GiB consistently, consider a periodic gateway restart.

  3. MONITOR SYSTEM LOAD
     → Load 5.80, driven by 3 Minecraft agents + Ollama + Java. Acceptable
       but elevated; consider throttling agent count if it climbs past 8.

  4. SENDGRID API KEY (still pending)
     → Blocks email verification + campaign pipelines. Reminder cron
       (auth-system-sendgrid-setup) remains active.

═══════════════════════════════════════════════════════════════════════════

Overall: Core systems healthy. Queue is clear (0 pending outreach, DBs
empty/idle). Two watch items: system load climbed back to ~5.8 after
yesterday's dip, and the OpenClaw Gateway is again creeping up in memory
(1.2 → 4.2 GiB). One recurring cron error remains (Monthly Document
Review — message too long); Weekly Competitor Report has recovered.

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
