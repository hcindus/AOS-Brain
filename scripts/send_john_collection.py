#!/usr/bin/env python3
"""
Nice collection email to John (omersidick@yahoo.com), CC accountant Amy.
4 Square payment links. BCC info@psdepot.com.
Retries on rate-limit (waits for hour boundary).
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

TO = "omersidick@yahoo.com"
CC = "amy@slaterandassoc.net"
BCC = "info@psdepot.com"
SUBJECT = "Quick check-in — a few open invoices"

links = [
    "https://app.squareup.com/pay-invoice/invtmp:0ba8d276-cd5b-4a6e-948f-897ad7150edd",
    "https://app.squareup.com/pay-invoice/invtmp:5f54f0b5-f897-472d-9a8d-0679417fd95d",
    "https://app.squareup.com/pay-invoice/invtmp:625116a9-e4b3-4187-9ef9-4d92f1ec4531",
    "https://app.squareup.com/pay-invoice/invtmp:b164315a-5813-484a-9e9f-0187bdc69ed0",
]

body = ("Hi John,\n\n"
        "I hope you're doing well! Just a friendly note — we're showing a few "
        "invoices open on our end and wanted to make sure they didn't get lost "
        "in the shuffle.\n\n"
        "Whenever you have a moment, you can view and pay them here:\n\n"
        + "\n".join(f"{i+1}. {l}" for i, l in enumerate(links)) +
        "\n\nNo rush at all — and if anything looks off or you have any questions, "
        "just let us know.\n\n"
        "Warmly,\n\n"
        "Miles\n"
        "Performance Supply Depot\n"
        "psdepot.com | 1-888-881-6834")

msg = MIMEText(body)
msg["From"] = f"Performance Supply Depot <{FROM}>"
msg["To"] = TO
msg["Cc"] = CC
msg["Bcc"] = BCC
msg["Subject"] = SUBJECT

for attempt in range(12):
    try:
        s = smtplib.SMTP(HOST, PORT, timeout=30)
        s.starttls()
        s.login(FROM, PASSWORD)
        s.sendmail(FROM, [TO, CC, BCC], msg.as_string())
        s.quit()
        print("SENT_TO_JOHN_OK")
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
