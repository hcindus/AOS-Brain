#!/usr/bin/env python3
"""
Daily Queue Email Report - August 8, 2026
Sends comprehensive queue and system status report to Captain
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

    body = f"""Good afternoon, Captain!

Here is your daily queue and system status report for {current_date}.

═══════════════════════════════════════════════════════════════════════════
                           SYSTEM HEALTH STATUS
═══════════════════════════════════════════════════════════════════════════

Generated: {current_time}
Uptime: 81 days, 4+ hours

COMPONENT STATUS:
┌──────────────────────────┬───────────┬──────────────────────────────────┐
│ Component                │ Status    │ Details                          │
├──────────────────────────┼───────────┼──────────────────────────────────┤
│ Brain Core v4.5          │ 🟢 ACTIVE │ python3 complete_brain_v45.py    │
│ Ollama Model Server      │ 🟢 ONLINE  │ 11 models loaded, responsive    │
│ Agent Network            │ 🟢 ONLINE  │ 1,305 agent files in workspace  │
│ Minecraft Server         │ 🟢 ACTIVE  │ Paper 1.20.4, Chelios connected │
│ Security (auditd)        │ 🟢 SECURED │ Active and monitoring           │
│ DepotChaos Email Engine  │ 🔴 STUCK   │ SendGrid API key NOT configured │
│ Cron Scheduler           │ 🟡 DEGRADED│ 13 of 38 jobs in error state    │
└──────────────────────────┴───────────┴──────────────────────────────────┘

SYSTEM RESOURCES:
• CPU Load:     9.52 / 8.21 / 8.06  ⚠️ ELEVATED
• Memory:       10Gi used / 15Gi total (67%)
• Memory Avail: 5.5Gi
• Swap:         4.5Gi used / 29Gi total
• Disk:         133G used / 193G total (69%)

TOP PROCESSES BY MEMORY:
  • Java (Minecraft): 3.2 GiB  — Paper 1.20.4
  • Ollama Runner:    2.0 GiB  — qwen2.5:14b model
  • OpenClaw Gateway: 1.9 GiB  — main session
  • Ollama Runner #2: 334 MiB  — active model

═══════════════════════════════════════════════════════════════════════════
                           QUEUE STATUS
═══════════════════════════════════════════════════════════════════════════

DARK FACTORY (Patricia's Production):
• Total Orders:     3
• Completed:        0
• Active/Pending:   3

FACTORY QUEUE ITEMS:
  • DF-REG-004 — Patricia v2 Registration
  • DF-RS80-001 — Forge Task (ReggieStarr RS80)
  • Various urgent builds (CREAM Mobile, NogNog Mobile, Brain v4 restoration)

EMAIL QUEUE (DepotChaos):
• ~100 campaign emails stuck (since June 5, 2026 — 64+ days)
• 99x Teriyaki Madness thermal paper outreach
• 1x DNS setup reminder
• ROOT CAUSE: SENDGRID_API_KEY not configured in environment
• Auth system also needs SendGrid for password resets

═══════════════════════════════════════════════════════════════════════════
                           CRON JOB HEALTH
═══════════════════════════════════════════════════════════════════════════

Total Jobs: 38 | Healthy: 25 | Error: 13

🔴 FAILING JOBS (13):
  • aos-layer-feeder (every 5m) — 218 consecutive errors
    → Telegram delivery: @heartbeat chat not found
  • Git Push 8hr — 3 duplicate jobs failing (ac7b, b681, c4b8)
    → Telegram delivery target missing
  • Daily Patricia + Jordan Standup (9AM UTC) — 6 errors
  • datadepot-daily-collection (6AM PT) — 57 errors
  • datadepot-weekly-sales-sprint (Mon 9AM PT) — 9 errors
  • Weekly Competitor Report (Mon 9AM) — 1 error
  • Monthly Legal Compliance Check — 1 error
  • Monthly GitHub Audit — 1 error
  • Monthly Document Review — 2 errors
  • Monthly VPS Audit — 1 error

🟢 HEALTHY JOBS (25):
  • Unified AOS Health Check (every 10m) ✅
  • Auto GitHub Push (every 30m) ✅
  • Ollama Model Keepalive (every 30m) ✅
  • Miles Waste Emailer (every 30m) ✅
  • SendGrid Auth System Reminder (daily) ✅
  • Minecraft Agent Rotation (12h) ✅
  • Lead Piping Scraper (daily) ✅
  • Daily Email Check - Miles ✅
  • PSDepot Price Sync (daily) ✅
  • AGI Company Daily Report (midnight) ✅
  • CREAM Realtor Lead Scraper (daily) ✅
  • Daily Lead Scraper (6AM) ✅
  • Daily SFX Generation (5AM) ✅
  • Daily Data Scraper (2AM) ✅
  • Daily DepotChaos Lead Import (3AM) ✅
  • Git Push - Midnight/Morning/Evening systemEvents ✅

═══════════════════════════════════════════════════════════════════════════
                           ACTION ITEMS
═══════════════════════════════════════════════════════════════════════════

🔴 CRITICAL:
  1. CONFIGURE SENDGRID API KEY
     → 100 emails stuck for 64+ days across 2 systems
     → Set SENDGRID_API_KEY env var + restart services
     → Also needed for auth-system password resets

  2. CLEAN UP STALE CRON JOBS
     → 13 jobs in error — many are duplicates or have delivery issues
     → Remove duplicate Git Push jobs (keep f9a8ba22 + delivery-targeted ones)
     → Fix Telegram delivery targets (@heartbeat → numeric chat IDs)
     → Disable failing monthly jobs until fixed

🟡 IMPORTANT:
  3. FACTORY QUEUE BACKLOG
     → 3 active orders pending — no completions recently
     → Review with Patricia during next standup

  4. SYSTEM LOAD ELEVATED
     → CPU load 9.52 — Minecraft + Ollama are top consumers
     → Memory at 67% — within acceptable range
     → Monitor for OOM risk if load increases

  5. AGENT FILES AT 1,305
     → Down from previous 6,589 — verify no data loss
     → May reflect cleanup/consolidation

═══════════════════════════════════════════════════════════════════════════

All core services operational. Primary concern remains the 100-email
DepotChaos backlog stuck behind missing SendGrid config, plus 13 cron
jobs needing triage (mostly delivery/target issues).

Report auto-generated. Standing by for Captain's directives.

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
    return current_time, recipient

if __name__ == "__main__":
    send_daily_queue_report()
