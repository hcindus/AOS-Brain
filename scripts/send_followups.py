#!/usr/bin/env python3
"""
Send the drafted "nice" follow-up reminders (followup_drafts.json).
Usage:
  python3 send_followups.py --dry-run    # preview only
  python3 send_followups.py              # send all
  python3 send_followups.py --only Ross  # send one (by name)
"""
import json, smtplib, argparse
from email.mime.text import MIMEText

DRAFTS = "/root/.openclaw/workspace/datadepot/data/followup_drafts.json"


def creds():
    c = {}
    for line in open("/root/.openclaw/workspace/aocros/secrets/sales_smtp.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            c[k] = v
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()

    drafts = json.load(open(DRAFTS))
    if args.only:
        drafts = [d for d in drafts if d["name"].lower() == args.only.lower()]

    c = creds()
    for d in drafts:
        if args.dry_run:
            print(f"[DRY] {d['name']} <{d['to']}> — {d['subject']}")
            continue
        msg = MIMEText(d["body"])
        msg["From"] = f"Sales Performance Supply Depot <{c['SALES_SMTP_USER']}>"
        msg["To"] = d["to"]
        msg["Bcc"] = "info@psdepot.com"
        msg["Subject"] = d["subject"]
        s = smtplib.SMTP(c.get("SALES_SMTP_HOST", "smtp.gmail.com"),
                         int(c.get("SALES_SMTP_PORT", "587")), timeout=30)
        s.starttls()
        s.login(c["SALES_SMTP_USER"], c["SALES_SMTP_PASS"])
        s.sendmail(c["SALES_SMTP_USER"], [d["to"], "info@psdepot.com"], msg.as_string())
        s.quit()
        print(f"SENT {d['name']} <{d['to']}>")

    print(f"DONE ({len(drafts)} emails)")


if __name__ == "__main__":
    main()
