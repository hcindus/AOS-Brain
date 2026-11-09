#!/usr/bin/env python3
"""
Generic payment-link sender (reusable).
Usage: python3 send_payment_link.py <to_email> <greeting_name> <business_name> <link> [cc_email]
Retries on rate-limit (waits for hour boundary). BCC info@psdepot.com.
"""
import sys, smtplib, time
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

if len(sys.argv) < 5:
    print("usage: send_payment_link.py <to_email> <greeting_name> <business_name> <link> [cc_email]")
    sys.exit(1)

to_email = sys.argv[1]
greeting = sys.argv[2]
business = sys.argv[3]
link = sys.argv[4]
cc = sys.argv[5] if len(sys.argv) > 5 else None

creds = {}
for line in open("/root/.openclaw/workspace/aocros/secrets/smtp.env"):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        creds[k] = v
FROM = creds["HOSTINGER_SMTP_USER"]
PASSWORD = creds["HOSTINGER_SMTP_PASS"]
HOST = creds.get("HOSTINGER_SMTP_SERVER", "smtp.hostinger.com")
PORT = int(creds.get("HOSTINGER_SMTP_PORT", "587"))
BCC = "info@psdepot.com"

SUBJECT = "Open invoice — Performance Supply Depot"

body = (f"Hi {greeting},\n\n"
        f"I hope you're doing well! We have an open invoice on file for "
        f"{business} that we wanted to make sure you saw.\n\n"
        f"Whenever you have a moment, you can view and pay it here:\n\n"
        f"{link}\n\n"
        f"No rush — and if anything looks off or you have any questions, just "
        f"let us know.\n\n"
        f"Warmly,\n\n"
        f"Miles\n"
        f"Performance Supply Depot\n"
        f"psdepot.com | 1-888-881-6834")

msg = MIMEText(body)
msg["From"] = f"Performance Supply Depot <{FROM}>"
msg["To"] = to_email
if cc:
    msg["Cc"] = cc
msg["Bcc"] = BCC
msg["Subject"] = SUBJECT

recipients = [to_email, BCC] + ([cc] if cc else [])

for attempt in range(12):
    try:
        s = smtplib.SMTP(HOST, PORT, timeout=30)
        s.starttls()
        s.login(FROM, PASSWORD)
        s.sendmail(FROM, recipients, msg.as_string())
        s.quit()
        print(f"SENT_OK to={to_email}")
        break
    except Exception as e:
        err = str(e)
        if "451" in err or "ratelimit" in err.lower():
            now = datetime.now(timezone.utc)
            nxt = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            wait = int((nxt - now).total_seconds()) + 5
            print(f"RATE_LIMIT — waiting {wait}s (attempt {attempt+1}/12)")
            time.sleep(wait)
        else:
            print(f"FAILED: {err}")
            break
else:
    print("GAVE_UP_AFTER_RETRIES")
