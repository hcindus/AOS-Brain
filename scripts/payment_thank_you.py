#!/usr/bin/env python3
"""
Send a "thank you for your payment" email to a customer, with the pre-filled
thank-you-payment.html link.

Usage:
  python3 payment_thank_you.py --email cust@x.com --date 2026-07-22 \
      --ref INV-061326-045 --amount 315.26 --method "Credit Card" --name "David Dearstyne"
"""
import argparse, smtplib, sys, os
sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from email.mime.text import MIMEText
import order_processor as op


def creds():
    c = {}
    for line in open("/root/.openclaw/workspace/aocros/secrets/sales_smtp.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            c[k] = v
    return c


def send(to_email, subject, body_html):
    c = creds()
    msg = MIMEText(body_html, "html")
    msg["From"] = f"Sales Performance Supply Depot <{c['SALES_SMTP_USER']}>"
    msg["To"] = to_email
    msg["Bcc"] = "info@psdepot.com"
    msg["Subject"] = subject
    s = smtplib.SMTP(c.get("SALES_SMTP_HOST", "smtp.gmail.com"),
                     int(c.get("SALES_SMTP_PORT", "587")), timeout=30)
    s.starttls()
    s.login(c["SALES_SMTP_USER"], c["SALES_SMTP_PASS"])
    s.sendmail(c["SALES_SMTP_USER"], [to_email, "info@psdepot.com"], msg.as_string())
    s.quit()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--email", required=True)
    p.add_argument("--date", required=True)
    p.add_argument("--ref", required=True)
    p.add_argument("--amount", required=True)
    p.add_argument("--method", required=True)
    p.add_argument("--name", required=True)
    a = p.parse_args()

    link = op.payment_thank_you_link(a.date, a.ref, a.amount, a.method, a.name)
    body = op.payment_thank_you_email_html(a.date, a.ref, a.amount, a.method, a.name)
    send(a.email, "Thank you for your payment — Performance Supply Depot", body)
    print(f"SENT to {a.email}\nLINK: {link}")


if __name__ == "__main__":
    main()
