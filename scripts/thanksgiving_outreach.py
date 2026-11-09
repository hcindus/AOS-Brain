#!/usr/bin/env python3
"""
Thanksgiving supplies outreach — send a courtesy email to ALL active customers.
Builds deduped list from all invoice CSVs, excludes closed businesses + own
addresses, rate-limited (90s spacing), deduped against thanksgiving_sent.json.
BCC info@psdepot.com.
"""
import csv, glob, json, smtplib, time, os
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

MEDIA = "/root/.openclaw/media/inbound"
SENT_LOG = "/root/.openclaw/workspace/datadepot/data/thanksgiving_sent.json"
FORM_URL = ("https://docs.google.com/forms/d/e/1FAIpQLSf_MpGmbwkrZm2nVsL-"
            "RYiVHCsEqEMpjZ6eHKTQ8rr1KUx2Cw/viewform")

SEND_INTERVAL = 90
MAX_PER_RUN = 40
MAX_RATE_WAITS = 6
BCC = "info@psdepot.com"

# own / closed addresses to skip
SKIP = {"info@psdepot.com", "antonio.hudnall@gmail.com", "miles@myl0nr0s.cloud",
        "kvance@leftbank.com", "bthompson@leftbank.com",  # Left Bank (closed)
        "terrychico@sbcglobal.net", "coldpop.billing@gmail.com",  # Travis (do-not-contact)
        }

# multi-email identity merge (canonical -> keep one)
ALIASES = {
    "coldpop.billing@gmail.com": "terrychico@sbcglobal.net",   # Travis
    "delfierro@coastside.net": "betsy@itsitaliarestaurant.com",  # Betsy
    "leslie@bungalow44.com": "tiffany@realrestaurants.com",   # Leslie (Bungalow 44)
    "sepillo78@hotmail.com": "samuelhm502@gmail.com",          # Mario ECR
    "beriekidane@gmail.com": "harjitgandham@yahoo.com",        # Harry
}

def clean_name(name):
    if not name:
        return ""
    for s in ("SUPPLY ONLY","NCC","ECR","MAITRE'D","GM","Owner","Manager",
              "General Manager","left msg","open","Cd @ 2 months","call back",
              "open store","Manager Manager","(415) 652-6550"):
        name = name.replace(s, " ")
    parts = [p for p in name.replace(",", " ").split() if p]
    return " ".join(parts).strip()

def load_json(path, default):
    try:
        return json.load(open(path))
    except Exception:
        return default

def save_json(path, obj):
    json.dump(obj, open(path, "w"), indent=2)

# build deduped customer list
cust = {}
for fn in sorted(glob.glob(os.path.join(MEDIA, "invoices-export-*.csv"))):
    with open(fn, newline="", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            email = (r.get("Customer Email") or "").strip().lower()
            name = (r.get("Customer Name") or "").strip()
            if not email or "@" not in email or email in SKIP:
                continue
            email = ALIASES.get(email, email)
            if email in SKIP:
                continue
            cname = clean_name(name)
            if email not in cust or (cname and len(cname) < len(cust[email])):
                cust[email] = cname or name

print(f"UNIQUE_TARGETS={len(cust)}")

# SMTP creds
creds = {}
for line in open("/root/.openclaw/workspace/aocros/secrets/smtp.env"):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        creds[k] = v
FROM = creds["HOSTINGER_SMTP_USER"]; PASSWORD = creds["HOSTINGER_SMTP_PASS"]
HOST = creds.get("HOSTINGER_SMTP_SERVER","smtp.hostinger.com"); PORT = int(creds.get("HOSTINGER_SMTP_PORT","587"))

SUBJECT = "Thanksgiving supplies — are you stocked up?"

def body(name):
    first = (name or "there").split()[0]
    return (f"Hi {first},\n\n"
            f"Thanksgiving is right around the corner! Just wanted to check in — "
            f"are you stocked up on supplies for the holiday rush? We've got thermal "
            f"paper, printer ribbons, and everything else to keep your POS running "
            f"smooth through the busy season.\n\n"
            f"To order supplies on your schedule:\n{FORM_URL}\n\n"
            f"Let me know if you need anything — happy to help you get ready!\n\n"
            f"Warmly,\n\nMiles\nPerformance Supply Depot\npsdepot.com | 1-888-881-6834")

sent = load_json(SENT_LOG, {})
today = datetime.now(timezone.utc).date()
todo = [(e, n) for e, n in cust.items()
        if not sent.get(e) or (datetime.strptime(sent[e], "%Y-%m-%d").date() < today)]
todo = sorted(todo, key=lambda x: x[1].lower())[:MAX_PER_RUN]

print(f"TO_SEND_THIS_RUN={len(todo)}")

count = 0
for email, name in todo:
    msg = MIMEText(body(name))
    msg["From"] = f"Performance Supply Depot <{FROM}>"
    msg["To"] = email
    msg["Bcc"] = BCC
    msg["Subject"] = SUBJECT
    ok = False
    err = ""
    for attempt in range(MAX_RATE_WAITS):
        try:
            s = smtplib.SMTP(HOST, PORT, timeout=30); s.starttls(); s.login(FROM, PASSWORD)
            s.sendmail(FROM, [email, BCC], msg.as_string()); s.quit()
            ok = True; break
        except Exception as e:
            err = str(e)
            if "451" in err or "ratelimit" in err.lower():
                now = datetime.now(timezone.utc)
                nxt = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
                wait = int((nxt - now).total_seconds()) + 5
                print(f"RATE_LIMIT waiting {wait}s"); time.sleep(wait)
            else:
                break
    if ok:
        sent[email] = today.strftime("%Y-%m-%d")
        count += 1
        save_json(SENT_LOG, sent)
    else:
        print(f"FAIL {email}: {err}")
    time.sleep(SEND_INTERVAL)

print(f"SENT={count}")
