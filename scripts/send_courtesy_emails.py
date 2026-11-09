#!/usr/bin/env python3
"""
Paid-customer courtesy outreach:
  1. Parse the invoices CSV → dedupe to unique customers (by email).
  2. Send a warm "checking on your supplies" email (BCC info@psdepot.com).
  3. Load customers into psd_customers (live DepotChaos) for scheduled follow-up.
"""
import csv, smtplib, sqlite3
from email.mime.text import MIMEText
from pathlib import Path

CSV = "/root/.openclaw/media/inbound/invoices-export-20261109T2014---63cf980b-e227-4a3a-97ab-294293696cb7.csv"
DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
BCC = "info@psdepot.com"
BOUNCE_LOG = "/root/.openclaw/workspace/datadepot/data/courtesy_bounces.log"

# SMTP creds
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

# Emails to skip (our own / test / placeholder)
SKIP = {"info@psdepot.com", "info@psdepot.com", "test@example.com", "info@guess.com",
        "antonio.hudnall@gmail.com", "antonio.hudnall@chipp.cc", "a.hud@att.net",
        "jane@grandhotel.com"}

SUBJECT = "Checking in — how are your supplies holding up?"

def body(name):
    first = (name or "there").split()[0]
    return f"""Hi {first},

Just a quick check-in from all of us at Performance Supply Depot — I wanted to see how your supplies are holding up and whether there's anything you need.

Thermal paper, printer ribbons, cash-register parts, scales — if you're running low on anything, just reply and I'll get you sorted right away.

No pressure at all. Just wanted to make sure you're taken care of.

Warmly,

Miles
Performance Supply Depot
psdepot.com
1-888-881-6834
"""

def main():
    # 1. Parse + dedupe customers
    customers = {}
    with open(CSV, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = (row.get("Customer Email") or "").strip().lower()
            name = (row.get("Customer Name") or "").strip()
            phone = (row.get("Customer Phone") or "").strip()
            if not email or "@" not in email:
                continue
            if email in SKIP:
                continue
            if email not in customers:
                customers[email] = {"name": name, "email": email, "phone": phone}

    print(f"UNIQUE_CUSTOMERS={len(customers)}")

    # 2. Load into psd_customers (live DepotChaos)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # ensure table has needed columns (idempotent-ish)
    try:
        c.execute("ALTER TABLE psd_customers ADD COLUMN email TEXT")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE psd_customers ADD COLUMN phone TEXT")
    except Exception:
        pass
    for email, cus in customers.items():
        c.execute("INSERT OR IGNORE INTO psd_customers (name, email, phone) VALUES (?,?,?)",
                  (cus["name"], email, cus["phone"]))
    conn.commit()
    conn.close()

    # 3. Send courtesy emails (BCC)
    sent = 0
    bounced = 0
    for email, cus in customers.items():
        msg = MIMEText(body(cus["name"]))
        msg["From"] = f"Performance Supply Depot <{FROM}>"
        msg["To"] = email
        msg["Bcc"] = BCC
        msg["Subject"] = SUBJECT
        try:
            s = smtplib.SMTP(HOST, PORT, timeout=30)
            s.starttls()
            s.login(FROM, PASSWORD)
            s.sendmail(FROM, [email, BCC], msg.as_string())
            s.quit()
            sent += 1
        except Exception as e:
            bounced += 1
            with open(BOUNCE_LOG, "a") as f:
                f.write(f"{email} | {e}\n")

    print(f"SENT={sent}")
    print(f"BOUNCED={bounced}")

if __name__ == "__main__":
    main()
