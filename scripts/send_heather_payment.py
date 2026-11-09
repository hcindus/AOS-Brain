#!/usr/bin/env python3
"""
Payment-link email to Heather (Kitchen Door Restaurant).
Retries on rate-limit (waits for hour boundary). BCC info@psdepot.com.
"""
import smtplib, time
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

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

TO = "info@kitchendoornapa.com"
BCC = "info@psdepot.com"
SUBJECT = "Open invoice — Performance Supply Depot"

LINK = "https://app.squareup.com/pay-invoice/invtmp:bc8b7e29-a91a-4879-8d92-773ee734c1f3"

body = ("Hi Heather,\n\n"
        "I hope you're doing well! We have an open invoice on file for Kitchen "
        "Door that we wanted to make sure you saw.\n\n"
        "Whenever you have a moment, you can view and pay it here:\n\n"
        f"{LINK}\n\n"
        "No rush — and if anything looks off or you have any questions, just "
        "let us know.\n\n"
        "Warmly,\n\n"
        "Miles\n"
        "Performance Supply Depot\n"
        "psdepot.com | 1-888-881-6834")

msg = MIMEText(body)
msg["From"] = f"Performance Supply Depot <{FROM}>"
msg["To"] = TO
msg["Bcc"] = BCC
msg["Subject"] = SUBJECT

for attempt in range(12):
    try:
        s = smtplib.SMTP(HOST, PORT, timeout=30)
        s.starttls()
        s.login(FROM, PASSWORD)
        s.sendmail(FROM, [TO, BCC], msg.as_string())
        s.quit()
        print("SENT_TO_HEATHER_OK")
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
