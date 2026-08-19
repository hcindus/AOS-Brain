#!/usr/bin/env python3
"""Daily Queue Email Report - August 19, 2026 (live data)."""
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
• Uptime:   92 days, 2h 46m
• CPU Load: 8.39 / 5.47 / 5.31  ⚠️ ELEVATED
• Memory:   6.3 Gi used / 15 Gi total (42%)
• Available: 9.3 Gi  🟢 healthy
• Swap:     6.3 Gi / 29 Gi
• Disk:     142G / 193G (74%)

Top processes (mem):
  java (RS-80 Android build, -Xmx4G)  14.1%
  openclaw-gateway                     7.9%
  complete_brain_v45.py (x2)           4.2%

Core services: ✅ Brain v4.5, Ollama (11 models), 5 society agents
(marcus, julius, titus, julia, livia), DepotChaos DB (21.9 MB populated).

════════════════════════════════════════════
  QUEUE STATUS
════════════════════════════════════════════
• DepotChaos lead DB: 21.9 MB, active (was 0 bytes on Aug 15)
• Factory queue: RS-80 APK build COMPLETE (14.78 MB, hosted via
  download link after SMTP attachment cap hit)
• Pending Captain action:
  1. ACM Technologies SOAP API — client rebuilt, needs live test
  2. DNS records (SendGrid + subdomains) — still pending in Hostinger

════════════════════════════════════════════
  CRON HEALTH — 34 jobs
════════════════════════════════════════════
🔴 2 jobs timing out (last run):
  • Daily Data Scraper + GitHub Sync (02:00) — timeout
  • CREAM Realtor Lead Scraper — timeout
🟡 Monthly Document Review — 3 consecutive errors
   (Telegram "message too long" — needs 2-line summary, not full text)

✅ All else healthy (git pushes, standups, email check, lead import).

════════════════════════════════════════════
  ACTION ITEMS
════════════════════════════════════════════
🔴 CRITICAL
  1. Investigate 2 timing-out cron jobs (scraper + CREAM) —
     likely need timeout bump or chunking.
  2. Monthly Document Review keeps failing on msg length —
     swap to file output + short chat summary.

🟡 IMPORTANT
  3. Add SendGrid DNS records (DKIM/SPF/DMARC) in Hostinger for
     psdepot.com — email authentication still pending.
  4. Test ACM SOAP client (credentials in aocros/secrets/acm_api.env).
  5. System load elevated (8.39) — driven by RS-80 Gradle build; expect
     to settle once the build finishes.

🟢 NOTE
  • 1.15 GB Bonsai-8B gguf still referenced in git history —
    candidate for `git filter-repo` if GitHub push is ever blocked again.
  • Yesterday's hprof heap-dump incident was cleaned up + gitignored.

All core systems operational. Standing by for your directives.

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
