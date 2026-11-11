#!/usr/bin/env python3
"""
Drain the DepotChaos email queue (pending_emails.json) via the sales Gmail SMTP.
Replaces the dead SendGrid path.

Usage: python3 drain_email_queue.py [--limit N]
"""
import json, smtplib, time, argparse
from email.mime.text import MIMEText

PENDING = "/root/.openclaw/workspace/datadepot/queue/pending_emails.json"
BCC = "info@psdepot.com"


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
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    c = creds()
    pending = json.load(open(PENDING))
    if args.limit:
        pending = pending[: args.limit]

    sent = 0
    failed_ids = []
    for e in pending:
        to = e.get("to_email")
        if not to:
            failed_ids.append(e.get("id"))
            continue
        try:
            msg = MIMEText(e.get("body", ""), "plain")
            msg["From"] = f"Sales Performance Supply Depot <{c['SALES_SMTP_USER']}>"
            msg["To"] = to
            msg["Bcc"] = BCC
            msg["Subject"] = e.get("subject", "Performance Supply Depot")
            s = smtplib.SMTP(c.get("SALES_SMTP_HOST", "smtp.gmail.com"),
                             int(c.get("SALES_SMTP_PORT", "587")), timeout=30)
            s.starttls()
            s.login(c["SALES_SMTP_USER"], c["SALES_SMTP_PASS"])
            s.sendmail(c["SALES_SMTP_USER"], [to, BCC], msg.as_string())
            s.quit()
            sent += 1
        except Exception as ex:
            failed_ids.append(e.get("id"))
            print(f"  FAIL {to}: {str(ex)[:70]}")
        time.sleep(1.0)

    remaining = [e for e in pending if e.get("id") in failed_ids]
    json.dump(remaining, open(PENDING, "w"), indent=2)
    print(f"SENT={sent} FAILED={len(failed_ids)} REMAINING={len(remaining)}")


if __name__ == "__main__":
    main()
