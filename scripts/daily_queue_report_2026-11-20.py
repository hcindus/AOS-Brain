#!/usr/bin/env python3
"""Daily Queue Report — 2026-11-20 (live data @ 06:00 UTC)."""
import smtplib, ssl, os, sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.environ.get("HOSTINGER_SMTP_SERVER", "smtp.hostinger.com")
SMTP_PORT = int(os.environ.get("HOSTINGER_SMTP_PORT", "587"))
FROM = os.environ.get("HOSTINGER_SMTP_USER", "miles@myl0nr0s.cloud")
TO = "antonio.hudnall@gmail.com"
PASS = os.environ.get("HOSTINGER_SMTP_PASS") or os.environ.get("SMTP_PASS") or "Myl0n.R0s"

now = datetime.utcnow()
date_str = now.strftime("%B %d, %Y")
ts = now.strftime("%Y-%m-%d %H:%M UTC")

report = f"""📊 Daily Queue Report — {date_str}
Generated: {ts}

Key stats (live @ 06:00 UTC):
- 🟢 Uptime 12d 5h12m (no reboot). Load 3.13/1.67/1.28 🟡 (1m spike from report-gen; 5m/15m steady at 1.67/1.28) | Mem 9.3Gi/15Gi (6.3Gi avail) 🟢 (flat) | Disk 81% 🟢 (flat) | Swap 2.5Gi/29Gi 🟢 (slightly up from 2.1Gi).
- 🟡 Vision daemons STILL hot: continuous_vision_daemon.py ~30.0% + vision_service.py ~23.2% CPU (combined ~53.2%). Unchanged — worth confirming they should run hot.
- 🟡 Top CPU: python3 (vision daemon) 30.0%, python3 (vision_service) 23.2%, openclaw-gateway 13.6%, ollama runner 7.5%, temporal-server 2.5%, complete_brain_v45 2.5%.
- 🔴 Email queue STILL STALLED: 59 sent / 148 "synthetic" — UNCHANGED. Last send still Nov 08 19:30:24 UTC (~12 days, no sends). Campaign capton_hospitality_202607 frozen.
- 🔴 unified.db 680MB (was 646MB) — last written Nov 19 06:30 UTC. STALE AGAIN (~24h, no writes since yesterday morning). The chain is stalled again; yesterday's recovery did not hold.
- 🔴 PENDING_TASKS table STILL absent from unified.db — confirm intended DB for CA_SOS scraper chain.
- 🟡 enrichment_queue table STILL absent (only idx_enrichment index remains).
- Table counts (ALL FLAT vs 11-19): unified_leads 1,460 | leads 33,086 | ca_abc_licenses 77,390 | enriched_leads 919 | psd_customers 636 | psd_customer_sales 235 | verified_leads 1 | scrape_runs 4 | email_queue 207

Datadepot queue (separate JSON store):
- Pending 0 | Sent 170 (all-time) | Failed 54 | Sent last 24h: 0 | Sent last 7 days: 0

Action items:
1. 🔴 Email queue stalled ~12 days — no sends since Nov 08 19:30. Confirm whether the drain stopped (rate limit, daemon down, or intentional pause) and whether to resume the remaining 148.
2. 🔴 unified.db went stale AGAIN (last write Nov 19 06:30) — the scraper/enrichment chain is NOT flowing. This regressed from yesterday's recovery.
3. 🟡 Vision daemons (continuous_vision_daemon.py + vision_service.py) still ~53% CPU combined — confirm they should run hot, or throttle.
4. 🟢 Memory flat at 9.3Gi used (6.3Gi avail). Swap ticked up slightly to 2.5Gi. Load steady at 1.67 (5m). No concern.
5. 🔴 PENDING_TASKS table still missing — confirm intended DB for the CA_SOS scraper chain.
6. 🟢 Disk stable at 81%; no immediate action.

—
Miles 🚀 (automated)
miles@myl0nr0s.cloud
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = f"📊 Daily Queue Report — {date_str}"
msg["From"] = FROM
msg["To"] = TO
msg.attach(MIMEText(report, "plain", "utf-8"))

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
