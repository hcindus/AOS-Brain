#!/usr/bin/env python3
"""
Mark an order as "paid" and auto-send the customer a payment thank-you email
(with the pre-filled thank-you-payment.html link, ref = PO number).

Usage:
  python3 mark_payment_received.py --po SLS-110526001 --email cust@x.com \
      --name "David Dearstyne" --amount 315.26 --method "Credit Card"

This records the payment in payments.json and emails the thank-you.
"""
import argparse, json, os, sys, datetime
sys.path.insert(0, '/root/.openclaw/workspace/scripts')
import order_processor as op

PAYMENTS = "/root/.openclaw/workspace/datadepot/data/payments.json"


def load(p, d):
    try:
        return json.load(open(p))
    except Exception:
        return d


def save(p, o):
    json.dump(o, open(p, "w"), indent=2)


def send_thankyou(to_email, date, ref, amount, method, name):
    from email.mime.text import MIMEText
    import smtplib
    c = {}
    for line in open("/root/.openclaw/workspace/aocros/secrets/sales_smtp.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            c[k] = v
    body = op.payment_thank_you_email_html(date, ref, amount, method, name)
    msg = MIMEText(body, "html")
    msg["From"] = f"Sales Performance Supply Depot <{c['SALES_SMTP_USER']}>"
    msg["To"] = to_email
    msg["Bcc"] = "info@psdepot.com"
    msg["Subject"] = "Thank you for your payment — Performance Supply Depot"
    s = smtplib.SMTP(c.get("SALES_SMTP_HOST", "smtp.gmail.com"),
                     int(c.get("SALES_SMTP_PORT", "587")), timeout=30)
    s.starttls()
    s.login(c["SALES_SMTP_USER"], c["SALES_SMTP_PASS"])
    s.sendmail(c["SALES_SMTP_USER"], [to_email, "info@psdepot.com"], msg.as_string())
    s.quit()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--po", required=True, help="PO / invoice number (SLS-...)")
    p.add_argument("--email", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--amount", required=True)
    p.add_argument("--method", required=True)
    p.add_argument("--date", default=datetime.datetime.now().strftime("%Y-%m-%d"))
    a = p.parse_args()

    payments = load(PAYMENTS, [])
    rec = {
        "po": a.po, "email": a.email, "name": a.name,
        "amount": float(a.amount), "method": a.method, "date": a.date,
        "collected_at": datetime.datetime.now().isoformat(),
    }
    payments.append(rec)
    save(PAYMENTS, payments)

    send_thankyou(a.email, a.date, a.po, a.amount, a.method, a.name)
    link = op.payment_thank_you_link(a.date, a.po, a.amount, a.method, a.name)
    print(f"PAID {a.po} recorded + thank-you sent to {a.email}")
    print(f"LINK: {link}")


if __name__ == "__main__":
    main()
