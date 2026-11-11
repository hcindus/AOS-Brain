#!/usr/bin/env python3
"""
Ribbon & Toner Division — outreach email to the existing customer funnel.

Reads the reorder-frequency list (existing customers) + sends a "we now carry
toners/inkjets/copiers" announcement. BCC info@psdepot.com. Uses the sales Gmail.
"""
import json, smtplib, time, argparse
from datetime import datetime, timezone
from email.mime.text import MIMEText

FUNNEL = "/root/.openclaw/workspace/datadepot/data/reorder_frequency.json"
SENT = "/root/.openclaw/workspace/datadepot/data/ribbon_toner_sent.json"
BCC = "info@psdepot.com"
SKIP = {"info@psdepot.com", "antonio.hudnall@gmail.com", "miles@myl0nr0s.cloud",
        "performancesupplydepotsales@gmail.com", "terrychico@sbcglobal.net",
        "coldpop.billing@gmail.com"}  # do-not-contact


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


def save(p, o):
    json.dump(o, open(p, "w"), indent=2)


def email_html(name):
    return f"""<html><body style="font-family:Arial,sans-serif;color:#111;font-size:14px;line-height:1.6">
<p>Hi {name},</p>

<p>Good news — <strong>Performance Supply Depot has expanded</strong>. We now stock a full
<strong>Ribbon &amp; Toner</strong> line alongside our thermal paper and POS ribbons.</p>

<p>We carry compatible and remanufactured <strong>toner, inkjet, and copier supplies</strong> from the
brands you already trust — HP, Brother, Canon, Epson, Kyocera, Lexmark, and more.</p>

<p>A few popular items (all in stock, plus shipping &amp; tax):</p>

<table cellpadding="8" cellspacing="0" style="border-collapse:collapse">
<tr style="background:#0A1A2F;color:#fff">
  <th style="text-align:left">Item</th><th>Price</th></tr>
<tr><td>Brother TN760 toner (3K yield)</td><td align="right">$20.25</td></tr>
<tr style="background:#f5f7fa"><td>HP 26X toner (9K high-yield)</td><td align="right">$33.00</td></tr>
<tr><td>Kyocera TK-3432 copier toner (21K)</td><td align="right">$52.92</td></tr>
<tr style="background:#f5f7fa"><td>HP 952XL inkjet (black)</td><td align="right">$10.88</td></tr>
<tr><td>Epson TM-220 ribbon (dozen)</td><td align="right">$42.00</td></tr>
</table>

<p>Already ordering paper from us? <strong>Add toners to the same order</strong> — one invoice, one
shipment, one supplier.</p>

<p>Reply to this email or call <strong>(888) 881-6834</strong> and we'll get you a quote.</p>

<p>Thanks,<br>
<strong>Miles</strong><br>
Performance Supply Depot LLC<br>
psdepot.com &bull; (888) 881-6834</p>
</body></html>"""


def send(to, name):
    c = creds()
    msg = MIMEText(email_html(name), "html")
    msg["From"] = f"Sales Performance Supply Depot <{c['SALES_SMTP_USER']}>"
    msg["To"] = to
    msg["Bcc"] = BCC
    msg["Subject"] = "Now stocking — Ribbon & Toner supplies"
    s = smtplib.SMTP(c.get("SALES_SMTP_HOST", "smtp.gmail.com"),
                     int(c.get("SALES_SMTP_PORT", "587")), timeout=30)
    s.starttls()
    s.login(c["SALES_SMTP_USER"], c["SALES_SMTP_PASS"])
    s.sendmail(c["SALES_SMTP_USER"], [to, BCC], msg.as_string())
    s.quit()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true", help="Preview only, no send")
    args = ap.parse_args()

    funnel = load(FUNNEL, [])
    sent = load(SENT, [])
    sent_set = set(sent)

    targets = [f for f in funnel if f.get("email") and f["email"] not in SKIP and f["email"] not in sent_set]
    if args.limit:
        targets = targets[: args.limit]

    print(f"funnel={len(funnel)} already_sent={len(sent_set)} targets={len(targets)}")

    for f in targets:
        to = f["email"]
        name = f.get("name") or "there"
        if args.dry_run:
            print(f"  [DRY] {name} <{to}>")
            continue
        try:
            send(to, name)
            sent.append(to)
            save(SENT, sent)
            print(f"  SENT {name} <{to}>")
            time.sleep(1.2)  # pace
        except Exception as e:
            print(f"  FAIL {to}: {e}")

    save(SENT, sent)
    print(f"DONE: sent={len(sent)}")


if __name__ == "__main__":
    main()
