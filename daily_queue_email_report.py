#!/usr/bin/env python3
"""
Daily Queue Email Report - August 7, 2026
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

    subject = f"📊 Daily Queue Report - {datetime.now().strftime('%B %d, %Y')}"

    body = f"""Good afternoon, Captain!

Here is your daily queue and system status report for {current_date}.

═══════════════════════════════════════════════════════════════════════════
                           SYSTEM HEALTH STATUS
═══════════════════════════════════════════════════════════════════════════

Generated: {current_time}
Uptime: 80 days, 4+ hours

COMPONENT STATUS:
┌──────────────────────────┬───────────┬──────────────────────────────────┐
│ Component                │ Status    │ Details                          │
├──────────────────────────┼───────────┼──────────────────────────────────┤
│ Brain Core v4.5          │ 🟢 ACTIVE │ 2 processes running              │
│ Ollama Model Server      │ 🟢 ONLINE  │ 11 models loaded, responsive    │
│ Agent Network            │ 🟢 ONLINE  │ 6,589 files / 1,305 agents      │
│ Security (auditd)        │ 🟢 SECURED │ Active and monitoring           │
│ DepotChaos Email Engine  │ 🔴 STUCK   │ SendGrid API key NOT configured │
│ Cron Scheduler           │ 🟡 DEGRADED│ 12 of 39 jobs in error state    │
└──────────────────────────┴───────────┴──────────────────────────────────┘

SYSTEM RESOURCES:
• CPU Load:     10.86 / 9.02 / 9.55  ⚠️ HIGH
• Memory:       12.0 Gi used / 15 Gi total (80%)
• Memory Avail: 3.4 Gi
• Swap:         4.2 Gi used / 29 Gi total
• Disk:         132G used / 193G total (69%)

═══════════════════════════════════════════════════════════════════════════
                           QUEUE STATUS
═══════════════════════════════════════════════════════════════════════════

DEPOTCHAOS TASKS:
• Total Pending: 13 tasks
• Priority Tasks: 2 (PECAN-001, DINER-001—both overdue since July 7)
• Status: All 13 tasks stuck in "pending" state

TOP PRIORITY TASKS:
  1. PECAN-001 — Contact Pecan POS West Coast Dealer (overdue)
  2. DINER-001 — Diner Daddy Lead Program Signup (overdue)
  3. PECAN-002 — Request Pecan POS Demo (due July 10, overdue)

EMAIL QUEUE (DepotChaos):
• 100 campaign emails stuck since June 5, 2026 (63 days)
• 99x Teriyaki Madness thermal paper outreach
• 1x DNS setup reminder to Captain
• ROOT CAUSE: SENDGRID_API_KEY not configured in environment

═══════════════════════════════════════════════════════════════════════════
                           CRON JOB HEALTH
═══════════════════════════════════════════════════════════════════════════

Total Jobs: 39 | OK: 24 | ERROR: 12 | RUNNING: 1 | IDLE: 2

🔴 FAILING JOBS:
  • aos-layer-feeder (every 5m) — error 45m ago
  • Git Push Schedule — 3 jobs failing (ac7b, b681, c4b8)
  • Daily Patricia + Jordan (9AM UTC) — error
  • datadepot-daily-collection — error
  • datadepot-weekly-sales-report — error
  • Weekly Competitor Report — error
  • Monthly Legal Compliance — error (last run 6 days ago)
  • Monthly GitHub Audit — error
  • Monthly Document Review — error
  • Monthly VPS Audit — error

🟢 HEALTHY JOBS:
  • Unified AOS Health Check (every 10m) ✅
  • Auto GitHub Push (every 30m) ✅
  • Ollama Model Keepalive (every 30m) ✅
  • Miles Waste Emailer (every 30m) ✅
  • SendGrid Auth System (daily) ✅
  • Minecraft Agent Rotation (12h) ✅
  • Lead Piping Scraper (daily) ✅
  • Daily Email Check - Miles ✅

═══════════════════════════════════════════════════════════════════════════
                           ACTION ITEMS
═══════════════════════════════════════════════════════════════════════════

🔴 CRITICAL:
  1. CONFIGURE SENDGRID API KEY
     → 100 emails stuck for 63 days
     → Set SENDGRID_API_KEY env var + restart depotchaos service
     → DNS: Add SendGrid DKIM/SPF records in Hostinger for myl0nr0s.cloud

🟡 IMPORTANT:
  2. Review 12 failing cron jobs
     → Monthly jobs likely failing due to missing API keys/configs
     → Git Push schedule has 3 stale error jobs (duplicates?)

  3. Clear DepotChaos backlog
     → 13 tasks all pending, 2 overdue since July 7
     → PECAN & DINER lead programs need Captain's attention

  4. Monitor system load
     → CPU load 10.86 — elevated, check for runaway processes
     → Memory at 80% — monitor for OOM risk

═══════════════════════════════════════════════════════════════════════════

All core systems operational. Main concern is the 100-email DepotChaos
backlog requiring SendGrid API key, plus 12 errant cron jobs needing triage.

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

if __name__ == "__main__":
    send_daily_queue_report()
