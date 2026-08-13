#!/usr/bin/env python3
"""
Daily Queue Email Report - August 13, 2026
Sends comprehensive queue and system status report to Captain.
Live data collected at runtime (2026-08-13 11:37 UTC).
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
Uptime: 86 days, 2+ hours

COMPONENT STATUS:
┌──────────────────────────┬───────────┬──────────────────────────────────┐
│ Component                │ Status    │ Details                          │
├──────────────────────────┼───────────┼──────────────────────────────────┤
│ Brain Core v4.5          │ 🟢 ACTIVE │ complete_brain_v45.py running   │
│ Ollama Model Server      │ 🟢 ONLINE  │ runner active, model resident   │
│ Agent Network            │ 🟢 ONLINE  │ 315 agent files, heart 72 BPM   │
│ Minecraft Server         │ 🟢 ACTIVE  │ Paper 1.20.4, Java ~2.4GiB      │
│ OpenClaw Gateway         │ 🟢 ONLINE  │ ~2.5 GiB RAM, stable            │
│ Security (auditd)        │ 🟢 SECURED │ Active and monitoring           │
│ DepotChaos DB            │ 🟢 HEALTHY │ 20MB, updated today 11:13 UTC   │
│ Cron Scheduler           │ 🟡 STABLE  │ 34/44 enabled, 2 with errors    │
│ Git Working Tree         │ 🟡 DIRTY   │ 5 modified files (data/scraper) │
└──────────────────────────┴───────────┴──────────────────────────────────┘

SYSTEM RESOURCES:
• CPU Load:     13.89 / 11.06 / 9.86  🔴 HIGH
• Memory:       7.9Gi used / 15Gi total (51%)
• Memory Avail: 7.7Gi
• Swap:         4.6Gi used / 29Gi total
• Disk:         137G used / 193G total (71%)

TOP PROCESSES BY MEMORY:
  • OpenClaw Gateway:    2.5 GiB  — main session
  • Java (Minecraft):    2.4 GiB  — Paper 1.20.4
  • Ollama Runner:        325 MiB  — active model
  • Brain v4.5 (AOS):     313 MiB  — complete_brain_v45.py
  • Minecraft agents:    ~1.0 GiB each — chelios, livia, julius, titus,
                          forge2, patricia2 (6 agents, ~24-40% CPU each)

NOTE: Load jumped sharply (5.86 → 13.89). Root cause is 6 active Minecraft
      society agents running concurrently (simple_agent.js + simple_society_agent.js),
      plus the Ollama runner. CPU load is elevated but not yet critical;
      memory is fine at 51%.

═══════════════════════════════════════════════════════════════════════════
                           QUEUE STATUS
═══════════════════════════════════════════════════════════════════════════

DARK FACTORY:
• factory_queue/ contains only diagnostic .md files — no active orders
• No JSON order files detected; factory remains idle

DEPOTCHAOS DATABASE:
• DepotChaos/depot_chaos.db — 20MB (21.4 MB), updated today 11:13 UTC
• yelp_cache.json — 2.2MB, updated today 06:02 UTC
• Root-level depot_chaos.db = 0 bytes (stale artifact — ignore)

QUEUE DIRECTORY:
• 74 files in /queue/ (historical daily status reports)
• Scraper queue_status.json: 74 queue items, 85 reports
• No active queue-processing jobs detected

MILES INBOX:
• Daily email check cron healthy (last run: OK)

═══════════════════════════════════════════════════════════════════════════
                           CRON JOB HEALTH
═══════════════════════════════════════════════════════════════════════════

Total Jobs: 44 | Enabled: 34 | Disabled: 10
Healthy: 32 | Error: 2 | Pending: 1 (Sept 1)

🔴 ENABLED JOBS IN ERROR (2):
  • Weekly Competitor Report (Mon 9AM UTC) — 3 consecutive timeouts
    → Last run timed out at 300s — script may be hung
  • Monthly Document Review (1st, 9AM) — 3 consecutive errors
    → "message is too long" (Telegram 400 delivery limit)
    → Needs output chunking or email delivery instead

🟡 DISABLED JOBS ACCUMULATING ERRORS (cleanup candidates):
  • Git Push (c4b8d7c0) — 97 errors, bad Telegram target
  • Git Push (b681b610) — 53 errors, @heartbeat chat not found
  • Git Push (ac7b1569) — 33 errors, bad Telegram target
  • Miles-Mortimer Daily Report (ee4868ac) — 1 error, @heartbeat
  • Old Daily Queue Report (5bb713dd) — superseded by this job
  → Recommend: delete these 5 disabled jobs to clear error logs

🟢 HEALTHY HIGHLIGHTS (32):
  • Unified AOS Health Check (10m) ✅
  • aos-layer-feeder (5m) ✅
  • Auto GitHub Push (30m) ✅
  • miles-waste-emailer (30m) ✅
  • Ollama Keepalive (30m) ✅
  • Daily Email Check ✅
  • Git Push 8hr Chunks ✅
  • Minecraft Rotation (12h) ✅
  • PSDepot Price Sync ✅
  • AGI Company Daily Report (midnight) ✅
  • Daily Data Scraper (2AM) ✅
  • DepotChaos Lead Import (3AM) ✅
  • Daily SFX Gen (5AM) ✅
  • daily-lead-scraper (6AM) ✅
  • Daily Queue Status (6AM) ✅
  • CREAM Realtor Scraper ✅
  • Lead Piping Scraper ✅
  • Patricia + Jordan Standup (9AM) ✅
  • Monthly Legal Compliance ✅
  • Monthly GitHub Audit ✅
  • Monthly VPS Audit ✅

═══════════════════════════════════════════════════════════════════════════
                           NOTABLE CHANGES SINCE LAST REPORT
═══════════════════════════════════════════════════════════════════════════

⚠️ CHANGES TO NOTE:
  • CPU load spiked: 5.86 → 13.89 (6 Minecraft agents active + Ollama)
  • Git tree now dirty: 5 modified files in data/scraper/ (auto-generated
    metrics JSON — expected, will be committed by Auto GitHub Push)
  • DepotChaos DB touched today (11:13) — lead import/enrichment active
  • Cron error count steady at 2 (same 2 jobs as yesterday)

✅ STABLE:
  • Memory healthy at 51% (down from 58% yesterday)
  • 32 cron jobs healthy — same strong baseline
  • DepotChaos DB healthy, no new corruption

═══════════════════════════════════════════════════════════════════════════
                           ACTION ITEMS
═══════════════════════════════════════════════════════════════════════════

🔴 IMPORTANT:
  1. INVESTIGATE HIGH CPU LOAD (13.89)
     → 6 Minecraft society agents running concurrently (24-40% CPU each)
     → Consider throttling/capping concurrent agents or pausing extras
     → Confirm this is intended vs. runaway process leak

  2. FIX WEEKLY COMPETITOR REPORT
     → 3 consecutive timeouts (300s limit)
     → Run manually: python3 skills/browser-agent/examples/competitor_monitor.py

  3. FIX MONTHLY DOCUMENT REVIEW DELIVERY
     → "message too long" — Telegram 400 limit
     → Switch delivery to email or chunk the output

🟡 NICE-TO-HAVE:
  4. CLEAN UP 5 DISABLED CRON JOBS
     → c4b8d7c0, b681b610, ac7b1569, ee4868ac, 5bb713dd
     → All disabled but accumulating error logs

  5. SENDGRID API KEY
     → Still flagged by daily auth-system reminder
     → Blocks email verification + campaign pipelines

═══════════════════════════════════════════════════════════════════════════

Overall: System stable with 32 healthy cron jobs and healthy DepotChaos DB.
Primary new concern is the CPU load spike to ~13.89 driven by 6 concurrent
Minecraft agents — worth a quick review to confirm intended. Same 2 cron
jobs remain in error (Weekly Competitor timeout + Monthly Doc Review
message-length). Everything else green.

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
