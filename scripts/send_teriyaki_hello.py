#!/usr/bin/env python3
"""
Send a generic "hello" email to Teriyaki Madness locations.
- Dedupes by email (send once per unique address)
- Handles bounces gracefully (logs SMTP failures, doesn't crash)
- Uses the verified sender (miles@myl0nr0s.cloud)
"""
import smtplib
from email.mime.text import MIMEText
import sqlite3

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
BOUNCE_LOG = "/root/.openclaw/workspace/datadepot/data/teriyaki_bounces.log"

# Load SMTP creds
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

SUBJECT = "A quick hello from Performance Supply Depot"

BODY = """Hi there,

Just a quick hello from all of us at Performance Supply Depot.

We're a California-based supplier of point-of-sale supplies — thermal receipt paper, printer ribbons, cash registers, and scales. We work with restaurants and food-service businesses like yours, and I wanted to reach out and introduce ourselves.

No hard sell here — just wanted to say hello and let you know we're here if you ever need a dependable source for the everyday supplies that keep a restaurant running.

If you'd like, I can send over a quick list of what we carry. Or if now's not a good time, no worries at all.

Either way, hope business is treating you well.

Warmly,

Miles
Performance Supply Depot
psdepot.com
1-888-881-6834
"""


def send():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # Distinct emails (dedupe — currently the corporate email covers all stores)
    c.execute("SELECT DISTINCT email FROM teriyaki_madness WHERE email IS NOT NULL AND email != ''")
    emails = [r[0] for r in c.fetchall()]
    conn.close()

    print(f"Recipients (distinct emails): {len(emails)}")
    for e in emails:
        print(f"  → {e}")

    sent = 0
    bounced = 0
    for to in emails:
        msg = MIMEText(BODY)
        msg["From"] = f"Performance Supply Depot <{FROM}>"
        msg["To"] = to
        msg["Subject"] = SUBJECT

        try:
            s = smtplib.SMTP(HOST, PORT, timeout=30)
            s.starttls()
            s.login(FROM, PASSWORD)
            s.sendmail(FROM, [to], msg.as_string())
            s.quit()
            sent += 1
            print(f"  ✅ sent → {to}")
        except Exception as e:
            bounced += 1
            with open(BOUNCE_LOG, "a") as f:
                f.write(f"{to} | {e}\n")
            print(f"  ❌ bounced → {to} ({e})")

    print(f"\n=== RESULT ===")
    print(f"  Sent: {sent} | Bounced: {bounced}")
    if bounced:
        print(f"  Bounce log: {BOUNCE_LOG}")


if __name__ == "__main__":
    send()
