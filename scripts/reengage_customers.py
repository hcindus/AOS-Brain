#!/usr/bin/env python3
"""
Existing-customer re-engagement — nurture/reorder existing 'active' customers on a
cadence, and log every touch to DepotChaos (sales_contacts + vendor).

Usage:
  python3 reengage_customers.py --dry-run            # preview who's due
  python3 reengage_customers.py --limit 20            # re-engage 20
"""
import json, re, sqlite3, smtplib, argparse
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
SENT = "/root/.openclaw/workspace/datadepot/data/reengage_sent.json"
SKIP = {"info@psdepot.com", "antonio.hudnall@gmail.com", "miles@myl0nr0s.cloud",
        "performancesupplydepotsales@gmail.com", "terrychico@sbcglobal.net", "coldpop.billing@gmail.com"}


def creds():
    c = {}
    for line in open("/root/.openclaw/workspace/aocros/secrets/sales_smtp.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            c[k] = v
    return c


def load(p, d):
    try:
        return json.load(open(p))
    except Exception:
        return d


def log_contact(vid, lead_name, outcome, want_prices, note):
    now = datetime.now(timezone.utc).isoformat()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO sales_contacts (vendor_id, lead_name, contact_type, channel, outcome, want_prices, notes, contacted_at) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (vid, lead_name, "email", "outbound", outcome, want_prices, note, now))
    if vid:
        cur.execute("UPDATE vendors SET last_contact_at=?, last_outcome=?, contact_preference=? WHERE id=?",
                    (now, outcome, "email", vid))
    con.commit()
    con.close()


def body(name):
    first = (name or "there").split()[0]
    return (f"<p>Hi {first},</p>"
            f"<p>Just a quick check-in from Performance Supply Depot &mdash; we wanted to make sure "
            f"you're stocked up on thermal paper and printer ribbons for the season.</p>"
            f"<p>Would it be okay if I email you our current prices so you can consider us in the future? "
            f"No pressure at all.</p>"
            f"<p>Thanks so much for your time.</p>"
            f"<p>Warmly,<br>Miles<br>Performance Supply Depot<br>psdepot.com | (888) 881-6834</p>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    con = sqlite3.connect(DB)
    cur = con.cursor()
    # existing customers: active + has email, not contacted recently
    cur.execute("""SELECT id, name, email FROM vendors
                   WHERE status='active' AND email IS NOT NULL AND email != ''""")
    rows = cur.fetchall()
    con.close()

    sent = load(SENT, [])
    sent_set = set(sent)
    todo = [r for r in rows if r[2] not in SKIP and r[2] not in sent_set]
    if args.limit:
        todo = todo[: args.limit]

    print(f"active_customers={len(rows)} already_sent={len(sent_set)} todo={len(todo)}")

    if args.dry_run:
        for vid, name, email in todo[:20]:
            print(f"  [DRY] {name[:30]} <{email}>")
        return

    c = creds()
    count = 0
    for vid, name, email in todo:
        try:
            msg = MIMEText(body(name), "html")
            msg["From"] = f"Sales Performance Supply Depot <{c['SALES_SMTP_USER']}>"
            msg["To"] = email
            msg["Bcc"] = "info@psdepot.com"
            msg["Subject"] = "Quick check-in — Performance Supply Depot"
            s = smtplib.SMTP(c.get("SALES_SMTP_HOST", "smtp.gmail.com"),
                             int(c.get("SALES_SMTP_PORT", "587")), timeout=30)
            s.starttls(); s.login(c["SALES_SMTP_USER"], c["SALES_SMTP_PASS"])
            s.sendmail(c["SALES_SMTP_USER"], [email, "info@psdepot.com"], msg.as_string())
            s.quit()
            log_contact(vid, name, "reengage", None, "existing-customer nurture")
            sent.append(email)
            count += 1
        except Exception as e:
            print("FAIL", email, str(e)[:50])

    json.dump(sorted(sent), open(SENT, "w"), indent=2)
    print(f"DONE sent={count}")


if __name__ == "__main__":
    main()
