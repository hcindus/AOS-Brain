#!/usr/bin/env python3
"""
Reorder-reminder scheduler (cadence-timed, not a blast).

Reads reorder_frequency.json (customer -> next_due), and each day emails only the
customers whose reorder window has arrived (next_due - LEAD_TIME <= today).
Uses Captain's template, BCC info@psdepot.com, rate-limited, deduped via sent-log.

Run daily via cron. Safe to run manually to "catch up" overdue customers.
"""
import json, smtplib, time, sys
from datetime import datetime, timedelta
from email.mime.text import MIMEText

FREQ = "/root/.openclaw/workspace/datadepot/data/reorder_frequency.json"
SENT_LOG = "/root/.openclaw/workspace/datadepot/data/reorder_sent.json"
BOUNCE_LOG = "/root/.openclaw/workspace/datadepot/data/reorder_bounces.log"

LEAD_TIME_DAYS = 4          # email this many days before predicted reorder
RESEND_SUPPRESS_DAYS = 30   # don't re-email a customer within this window
SEND_INTERVAL = 8           # seconds between sends (Hostinger outbound rate limit)
BCC = "info@psdepot.com"

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

SUBJECT = "Checking in on your POS supplies"

def body(name):
    first = (name or "there").split()[0]
    return (f"Hi {first},\n\n"
            f"This is Performance Supply Depot. We just wanted to check with you "
            f"on your POS supplies. Please let me know if you need anything.\n\n"
            f"- Performance Supply Depot\n"
            f"psdepot.com | 1-888-881-6834")

def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

def main():
    today = datetime.utcnow().date()
    freq = load_json(FREQ, [])
    sent = load_json(SENT_LOG, {})  # email -> "YYYY-MM-DD"

    due = []
    for c in freq:
        email = (c.get("email") or "").strip().lower()
        next_due = c.get("next_due")
        if not email or "@" not in email or not next_due:
            continue
        try:
            due_date = datetime.strptime(next_due, "%Y-%m-%d").date()
        except Exception:
            continue
        # skip if already emailed recently
        last_sent = sent.get(email)
        if last_sent:
            last = datetime.strptime(last_sent, "%Y-%m-%d").date()
            if (today - last).days < RESEND_SUPPRESS_DAYS:
                continue
        # due if reorder window (next_due - lead) has arrived
        if due_date - timedelta(days=LEAD_TIME_DAYS) <= today:
            due.append(c)

    if not due:
        print("NONE_DUE")
        return

    print(f"DUE_TODAY={len(due)}")

    sent_count = 0
    bounced = 0
    for c in due:
        email = c["email"].strip().lower()
        name = c.get("name") or "there"
        msg = MIMEText(body(name))
        msg["From"] = f"Performance Supply Depot <{FROM}>"
        msg["To"] = email
        msg["Bcc"] = BCC
        msg["Subject"] = SUBJECT
        ok = False
        for attempt in (1, 2):
            try:
                s = smtplib.SMTP(HOST, PORT, timeout=30)
                s.starttls()
                s.login(FROM, PASSWORD)
                s.sendmail(FROM, [email, BCC], msg.as_string())
                s.quit()
                ok = True
                break
            except Exception as e:
                err = str(e)
                # on rate-limit, back off and retry once
                if "451" in err or "ratelimit" in err.lower():
                    time.sleep(60)
                else:
                    break
        if ok:
            sent[email] = today.strftime("%Y-%m-%d")
            sent_count += 1
        else:
            bounced += 1
            with open(BOUNCE_LOG, "a") as f:
                f.write(f"{email} | {err}\n")
        time.sleep(SEND_INTERVAL)

    save_json(SENT_LOG, sent)
    print(f"SENT={sent_count}")
    print(f"BOUNCED={bounced}")

if __name__ == "__main__":
    main()
