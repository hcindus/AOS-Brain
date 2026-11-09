#!/usr/bin/env python3
"""
Reorder-reminder scheduler (cadence-timed, not a blast).

Reads reorder_frequency.json (customer -> next_due), and each day emails only the
customers whose reorder window has arrived (next_due - LEAD_TIME <= today).
Uses Captain's template, BCC info@psdepot.com, rate-limited, deduped via sent-log.

Run daily via cron. Safe to run manually to "catch up" overdue customers.
"""
import json, smtplib, time
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

FREQ = "/root/.openclaw/workspace/datadepot/data/reorder_frequency.json"
SENT_LOG = "/root/.openclaw/workspace/datadepot/data/reorder_sent.json"
BOUNCE_LOG = "/root/.openclaw/workspace/datadepot/data/reorder_bounces.log"

LEAD_TIME_DAYS = 4          # email this many days before predicted reorder
RESEND_SUPPRESS_DAYS = 30   # don't re-email a customer within this window
SEND_INTERVAL = 90          # seconds between sends (~40/hr, under Hostinger ~50/hr)
MAX_PER_RUN = 40            # hard cap per run to stay under hourly limit
BCC = "info@psdepot.com"

# never email our own / test addresses
SKIP = {"info@psdepot.com", "antonio.hudnall@gmail.com", "miles@myl0nr0s.cloud"}

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
    today = datetime.now(timezone.utc).date()
    freq = load_json(FREQ, [])
    sent = load_json(SENT_LOG, {})

    due = []
    for c in freq:
        email = (c.get("email") or "").strip().lower()
        if not email or "@" not in email or email in SKIP:
            continue
        last_sent = sent.get(email)
        if last_sent:
            last = datetime.strptime(last_sent, "%Y-%m-%d").date()
            if (today - last).days < RESEND_SUPPRESS_DAYS:
                continue
        # new contacts (no order history) get a one-time check-in
        if c.get("new_contact"):
            due.append(c)
            continue
        next_due = c.get("next_due")
        if not next_due:
            continue
        try:
            due_date = datetime.strptime(next_due, "%Y-%m-%d").date()
        except Exception:
            continue
        if due_date - timedelta(days=LEAD_TIME_DAYS) <= today:
            due.append(c)

    if not due:
        print("NONE_DUE")
        return

    # sort most-overdue first, cap per run
    due.sort(key=lambda c: c.get("days_overdue") or 0, reverse=True)
    due = due[:MAX_PER_RUN]

    print(f"DUE_TODAY={len(due)}")

    sent_count = 0
    bounced = 0
    ratelimited = False
    for c in due:
        email = c["email"].strip().lower()
        name = c.get("name") or "there"
        msg = MIMEText(body(name))
        msg["From"] = f"Performance Supply Depot <{FROM}>"
        msg["To"] = email
        msg["Bcc"] = BCC
        msg["Subject"] = SUBJECT
        ok = False
        last_err = ""
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
                last_err = str(e)
                if "451" in last_err or "ratelimit" in last_err.lower():
                    ratelimited = True
                    time.sleep(60)
                else:
                    break
        if ok:
            sent[email] = today.strftime("%Y-%m-%d")
            sent_count += 1
            save_json(SENT_LOG, sent)  # incremental, survive crash
        else:
            bounced += 1
            with open(BOUNCE_LOG, "a") as f:
                f.write(f"{email} | {last_err}\n")
        if ratelimited:
            # stop this run; remaining will be picked up next cron tick
            print("RATE_LIMIT_HIT_STOPPING")
            break
        time.sleep(SEND_INTERVAL)

    save_json(SENT_LOG, sent)
    print(f"SENT={sent_count}")
    print(f"BOUNCED={bounced}")

if __name__ == "__main__":
    main()
