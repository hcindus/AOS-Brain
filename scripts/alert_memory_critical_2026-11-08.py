#!/usr/bin/env python3
import smtplib, ssl, os, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
FROM = "miles@myl0nr0s.cloud"
TO = "antonio.hudnall@gmail.com"
PASS = os.environ.get("HOSTINGER_SMTP_PASS") or os.environ.get("SMTP_PASS") or "Myl0n.R0s"

body = """🚨 CRITICAL — Miles VPS memory exhaustion + crash-reboot loop

Captain, the health check just flagged a real problem that needs your call.

What's happening:
- System memory at 95% CRITICAL (14Gi/15Gi used, ~1.1Gi available)
- Crash-reboot loop: 3 reboots in ~2.7 hours
  • Nov 7 22:06 → 22:09 (3 min boot)
  • Nov 7 23:35 → 23:47 (12 min boot)
  • Nov 8 00:47 → now (still ramping)

Root cause (same one flagged in daily reports for days):
- train_server.py (RP1 robotics training) is actively training and holding 6.1GB RSS (37% of RAM)
- Plus a large Ollama model (~3.9GB) + openclaw-gateway (~3GB) + n8n + temporal + all factory agents, all on a 15GB box.

The training room (skill_trainer.py _train/_rollout) is pushing memory over the edge right after each boot, and the box is crashing and rebooting repeatedly.

Recommendation — pick one:
1. Throttle/stop train_server.py until the RP1 training is scheduled on a GPU or a bigger host.
2. Reduce model residency (unload the large qwen/nous models, keep only Mort_II + tinyllama).
3. Confirm RP1 training is intentional and add RAM / move it off this VPS.

This has been the #1 "headroom candidate" in every daily queue report for a week. It's now actively crashing the box.

I can stop or throttle train_server.py on your word.

—
Miles 🚀
miles@myl0nr0s.cloud
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = "🚨 CRITICAL: Miles VPS memory exhaustion + crash loop (RP1 train_server.py)"
msg["From"] = FROM
msg["To"] = TO
msg.attach(MIMEText(body, "plain", "utf-8"))

try:
    ctx = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
        s.starttls(context=ctx)
        s.login(FROM, PASS)
        s.send_message(msg)
    print("SENT")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
