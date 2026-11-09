#!/usr/bin/env python3
"""
Daily supply-canvas outreach — email 5 new food-service leads/day.
Reads the LIVE DepotChaos vendors table for real leads that now have BOTH
email + phone (enriched by Beets), selects 5 food-service businesses not yet
emailed, and sends a supply-intro email. BCC info@psdepot.com.
"""
import sqlite3, smtplib, time, json
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
SENT_LOG = "/root/.openclaw/workspace/datadepot/data/canvas_sent.json"
FORM_URL = ("https://docs.google.com/forms/d/e/1FAIpQLSf_MpGmbwkrZm2nVsL-"
            "RYiVHCsEqEMpjZ6eHKTQ8rr1KUx2Cw/viewform")

PER_DAY = 5
SEND_INTERVAL = 90
BCC = "info@psdepot.com"

# food-service vendor types (exclude existing "customer" + supplier/County Lead)
FOOD_TYPES = ("restaurant", "cafe", "bar", "seafood", "brewery", "pub", "coffee shop", "bakery", "taqueria")

SKIP_EMAILS = {"info@psdepot.com", "antonio.hudnall@gmail.com", "miles@myl0nr0s.cloud",
               "terrychico@sbcglobal.net", "coldpop.billing@gmail.com",  # Travis do-not-contact
               }

def load_json(p, d):
    try: return json.load(open(p))
    except Exception: return d

def save_json(p, o):
    json.dump(o, open(p, "w"), indent=2)

def main():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # enriched food-service leads: real + has email + has phone
    q = ("SELECT id, name, email, phone, city, state, vendor_type FROM vendors "
         "WHERE data_class='real' AND email IS NOT NULL AND email != '' "
         "AND phone IS NOT NULL AND phone != '' "
         "AND (vendor_type IN (%s) OR lower(name) LIKE '%%cafe%%' OR lower(name) LIKE '%%coffee%%' "
         "OR lower(name) LIKE '%%taquer%%' OR lower(name) LIKE '%%baker%%') "
         "AND lower(email) NOT LIKE '%%example.com%%' "
         "ORDER BY state='CA' DESC, state, city" % ",".join("?"*len(FOOD_TYPES)))
    rows = c.execute(q, FOOD_TYPES).fetchall()
    conn.close()

    sent = load_json(SENT_LOG, {})
    today = datetime.now(timezone.utc).date()

    # pick PER_DAY not-yet-emailed (skip do-not-contact + already-sent)
    picks = []
    for r in rows:
        email = r["email"].strip().lower()
        if not email or "@" not in email or email in SKIP_EMAILS:
            continue
        if sent.get(email):
            continue
        picks.append(r)
        if len(picks) >= PER_DAY:
            break

    if not picks:
        print("NO_NEW_LEADS")
        return

    creds = {}
    for line in open("/root/.openclaw/workspace/aocros/secrets/smtp.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            creds[k] = v
    FROM = creds["HOSTINGER_SMTP_USER"]; PASSWORD = creds["HOSTINGER_SMTP_PASS"]
    HOST = creds.get("HOSTINGER_SMTP_SERVER","smtp.hostinger.com"); PORT = int(creds.get("HOSTINGER_SMTP_PORT","587"))

    SUBJECT = "POS supplies — quick quote?"

    def body(r):
        name = (r["name"] or "there")
        return (f"<p>Hi there,</p>"
                f"<p>I'm Miles with Performance Supply Depot — thermal paper and printer "
                f"ribbons for restaurants and cafes across California.</p>"
                f"<p>Thermal paper from $59/case, ribbons from $42/dozen (plus shipping &amp; tax).</p>"
                f"<p>Want a quick quote? Just reply and I'll send pricing.</p>"
                f"<p>Thanks!<br>Miles<br>Performance Supply Depot<br>psdepot.com | 1-888-881-6834</p>")

    count = 0
    for r in picks:
        email = r["email"].strip().lower()
        msg = MIMEText(body(r), "html")
        msg["From"] = f"Performance Supply Depot <{FROM}>"
        msg["To"] = email
        msg["Bcc"] = BCC
        msg["Subject"] = SUBJECT
        ok = False
        for attempt in range(6):
            try:
                s = smtplib.SMTP(HOST, PORT, timeout=30); s.starttls(); s.login(FROM, PASSWORD)
                s.sendmail(FROM, [email, BCC], msg.as_string()); s.quit()
                ok = True; break
            except Exception as e:
                err = str(e)
                if "451" in err or "ratelimit" in err.lower():
                    now = datetime.now(timezone.utc)
                    nxt = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
                    time.sleep(int((nxt-now).total_seconds()) + 5)
                else:
                    break
        if ok:
            sent[email] = today.strftime("%Y-%m-%d")
            count += 1
            save_json(SENT_LOG, sent)
            print(f"SENT {r['name'][:30]} | {email}")
        time.sleep(SEND_INTERVAL)

    print(f"SENT_TODAY={count}")

if __name__ == "__main__":
    main()
