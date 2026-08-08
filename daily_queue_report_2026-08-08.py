#!/usr/bin/env python3
"""
Daily Queue Email Report — August 8, 2026
Live system data, queue summary, action items
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone

def send_report():
    smtp_server = "smtp.hostinger.com"
    smtp_port = 465
    email = "miles@myl0nr0s.cloud"
    password = "Myl0n.R0s"
    recipient = "Antonio.hudnall@gmail.com"

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M UTC")
    date_str = now.strftime("%A, %B %d, %Y")

    subject = f"📊 Daily Queue Report — {now.strftime('%B %d, %Y')}"

    body = f"""Captain —

Daily queue and system status report for {date_str}.

══════════════════════════════════════════════════════════════════
                     SYSTEM HEALTH OVERVIEW
══════════════════════════════════════════════════════════════════

  Component          Status     Details
 ─────────────────────────────────────────────────────────────────
  Brain v4           🟡 DEGRADED  API port 8000 unreachable (8th day)
                                   Internal organs healthy: tick 216,303, signal 0.895
                                   5 brain processes alive
  Ollama             🟢 HEALTHY   11/11 models loaded
  DepotChaos         🟡 CRASHING  CRM serving via orphan PID 547070
                                   systemd restart counter: 133,847
                                   Root cause: port 8082 conflict
  Pipeline Desk      🟡 UNVERIFIED Daemons running 10 days, output unchecked
  Minecraft Society  🟢 THRIVING  7 agents, 9 processes
  Docker             🟢 HEALTHY   buzz-postgres, buzz-redis, n8n
  OpenClaw Gateway   🟢 OPERATIONAL Cron scheduler healthy

  RESOURCES
  CPU Load:   7.93 / 8.75 / 8.40 (improved from 12.46 yesterday)
  Memory:     10GB / 15GB used, 5.6GB available (improved)
  Disk:       69% (61GB free)
  Uptime:     81 days

══════════════════════════════════════════════════════════════════
                     QUEUE & WORK STATUS
══════════════════════════════════════════════════════════════════

  AGENT NETWORK
  Agent Sandboxes:     58
  Agent MD Files:      617
  Minecraft Agents:    7 active (2x Patricia, 2x Forge, 2x Chelios, Aurora)
  Models Loaded:       11/11 (qwen3.5, qwen2.5:14b, deepseek-r1:7b, nos-hermes2, Mort_II, etc.)

  FACTORY
  Total Orders:        3 (all dated April 2026)
  Active Orders:       0
  Factory idle — no new production activity in 4 months

  PENDING_TASKS
  Status:              🔴 30 DAYS STALE — 7th discipline failure
  Last Updated:        2026-07-09 09:01 UTC
  Yesterday's Actions: 1/10 completed (cron consolidation by Miles)

  CA SOS SCRAPER
  Status:              🔴 BLOCKED 64 days
  Last Lead:           2026-06-05
  Root Cause:          DNS failure

  GIT ACTIVITY
  Overnight Commits:   30 (9 Jordan office syncs, 15 scraper metrics, 6 continuous iterations)
  Pending Changes:     5 files (scraper metrics updates)
  Jordan's Production: Strong despite zero coordination-layer action

══════════════════════════════════════════════════════════════════
                     CRON JOB HEALTH
══════════════════════════════════════════════════════════════════

  Job                           Errors    Issue
 ─────────────────────────────────────────────────────────────────
  aos-layer-feeder              216       Telegram @heartbeat not found
  Git Push 8h (c4b8d7c0)        89        Missing Telegram chatId
  datadepot-daily-collection    56        Missing Telegram chatId
  Git Push 8h (b681b610)        45        Telegram @heartbeat not found
  Git Push 8h (ac7b1569)        25        Missing Telegram chatId
  Daily Standup (da0de559)      6         Missing Telegram chatId
  Daily Standup (88dab0ee)      6         Missing Telegram chatId

  ROOT CAUSE: Multiple cron jobs configured with announce mode
  pointing to unresolved Telegram targets (@heartbeat, missing
  chatId). Non-critical — jobs themselves execute fine, only
  delivery/announcement fails.

══════════════════════════════════════════════════════════════════
                     TOP 5 ACTION ITEMS
══════════════════════════════════════════════════════════════════

  🔴 1. PENDING_TASKS Discipline Restoration
     → 30 days stale. 7th discipline failure.
     → Patricia + Jordan must update PENDING_TASKS TODAY
     → Accountability statements overdue 30 days
     → This is blocking all coordination-layer work

  🟡 2. DepotChaos Remediation — 30-SECOND FIX
     → Root cause identified: port 8082 conflict
     → Kill orphan PID 547070 + restart depotchaos.service
     → Fix: kill 547070 && systemctl restart depotchaos
     → Zero risk. CRM web UI already serving via orphan process.
     → 133,847 failed restart attempts — just needs authorization

  🟡 3. Brain v4 Port 8000 Investigation — 8th Day
     → All 5 brain processes alive, internal organs healthy
     → API layer is single point of failure
     → Need Jordan/Forge to investigate or document as intentional

  ✅ 4. Standup Cron Consolidation — RESOLVED
     → da0de559 (kimi-k2.5 duplicate) DISABLED at 09:03 UTC today
     → Only 88dab0ee (deepseek) remains active
     → First action completed in 31 days

  🟡 5. Pipeline Desk Output Verification — 10th Day
     → Chelios, Forge, and Dark Factory controllers running since Jul 28
     → No one has verified actual output
     → Are these real pipelines or empty 5-minute loops?

══════════════════════════════════════════════════════════════════
                     CAPTAIN QUESTIONS (16th Standup)
══════════════════════════════════════════════════════════════════

  Standing questions awaiting your response:

  1. Model budget decision — 103 days pending
  2. ACM API credentials — 53 days
  3. DNS records — 31 days (exceeded Patricia's 30-day closure threshold)
  4. Agent authority/autonomy framework — 30 days
  5. PENDING_TASKS: still required? Consequences if not? — 30 days
  6. Brain v4 investigation authorization — 8th day
  7. DepotChaos fix authorization (30-second, zero-risk fix) — NEW TODAY

  16 consecutive standups filed, zero Captain response.

══════════════════════════════════════════════════════════════════

  Summary: System running 81 days. Production layer (MC, Git, Docker)
  healthy. Coordination layer (PENDING_TASKS, Brain API, DepotChaos)
  degraded. One action completed today (cron consolidation) — first
  in 31 days. DepotChaos has a known 30-second fix awaiting
  authorization. Brain v4 internally healthy but API dead for 8 days.

  Next standup: Tomorrow 09:00 UTC.

  — Miles 🚀
  Automated report via OpenClaw Cron
  Generated: {timestamp}
"""

    msg = MIMEMultipart()
    msg['From'] = f"Miles <{email}>"
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, recipient, msg.as_string())

    print("✅ Report sent successfully!")
    print(f"   To: {recipient}")
    print(f"   Subject: {subject}")
    print(f"   Time: {timestamp}")

if __name__ == "__main__":
    send_report()
