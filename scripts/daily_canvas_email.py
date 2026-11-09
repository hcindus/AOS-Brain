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
        th = "border:1px solid #ddd;padding:6px 8px;text-align:left;background:#f5f5f5;"
        td = "border:1px solid #ddd;padding:6px 8px;text-align:left;"
        def table(headers, rows):
            h = "".join(f"<th style='{th}'>{c}</th>" for c in headers)
            b = ""
            for row in rows:
                b += "<tr>" + "".join(f"<td style='{td}'>{c}</td>" for c in row) + "</tr>"
            return f"<table style='border-collapse:collapse;width:100%;margin:6px 0 12px;'><tr>{h}</tr>{b}</table>"

        paper = [
            ("PF-230", "Epson Thermal Rolls", "3 1/8\" × 230', Phenol-Free", "50 rolls", "$124.10"),
            ("18-333", "Three-Ply Paper", "3\" White/Canary/Pink", "50 rolls", "$89.40"),
            ("CC-235", "Epson Two-Ply", "3\" Epson TMU-220", "50 rolls", "$76.00"),
            ("13-305", "Epson Impact Bond", "3\" One-Ply × 165'", "50 rolls", "$59.00"),
        ]
        ribbons = [
            ("62245", "Black/Red Ribbon", "Epson TM-220 Series", "Per Dozen", "$42.00"),
            ("67240", "Black/Red Ribbon", "Star SP700 Series", "Per Dozen", "$52.00"),
        ]
        paper_html = table(["Item #", "Description", "Specs", "Pack Size", "Price"], paper)
        ribbon_html = table(["Item #", "Description", "Printer Model", "Pack Size", "Price"], ribbons)

        return (f"<p>Hi there,</p>"
                f"<p>I know you're busy, so I'll keep this quick. I'm Miles with Performance "
                f"Supply Depot — we supply thermal paper and printer ribbons to restaurants "
                f"and cafes across California.</p>"
                f"<p>Below are our prices:</p>"
                f"<p><strong>Paper</strong></p>{paper_html}"
                f"<p><strong>Ink / Ribbons</strong></p>{ribbon_html}"
                f"<p>All prices are subject to tax and shipping.</p>"
                f"<p>Feel free to compare — we'd love the chance to earn your business.</p>"
                f"<p>Thank you,<br>Miles<br>Performance Supply Depot<br>psdepot.com | 1-888-881-6834</p>")

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
