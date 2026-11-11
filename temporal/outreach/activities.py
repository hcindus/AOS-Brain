"""Outreach activities — the actual work each Temporal workflow step does."""
import json, smtplib, os, re
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from temporalio import activity

INBOX = "/root/.openclaw/workspace/datadepot/data/closeter_inbox.json"
ORDERS = "/root/.openclaw/workspace/datadepot/data/closeter_orders.json"
FORM_URL = ("https://docs.google.com/forms/d/e/1FAIpQLSf_MpGmbwkrZm2nVsL-"
            "RYiVHCsEqEMpjZ6eHKTQ8rr1KUx2Cw/viewform")

def _smtp():
    c = {}
    for line in open("/root/.openclaw/workspace/aocros/secrets/smtp.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1); c[k] = v
    return c

def _send(to_email, subject, body_html):
    c = _smtp()
    msg = MIMEText(body_html, "html")
    msg["From"] = f"Performance Supply Depot <{c['HOSTINGER_SMTP_USER']}>"
    msg["To"] = to_email
    msg["Bcc"] = "info@psdepot.com"
    msg["Subject"] = subject
    s = smtplib.SMTP(c.get("HOSTINGER_SMTP_SERVER", "smtp.hostinger.com"),
                     int(c.get("HOSTINGER_SMTP_PORT", "587")), timeout=30)
    s.starttls(); s.login(c["HOSTINGER_SMTP_USER"], c["HOSTINGER_SMTP_PASS"])
    s.sendmail(c["HOSTINGER_SMTP_USER"], [to_email, "info@psdepot.com"], msg.as_string())
    s.quit()

COLD_BODY = (
    "<p>Hi there,</p>"
    "<p>I know you're busy, so I'll keep this quick. I'm Miles with Performance "
    "Supply Depot — we supply thermal paper and printer ribbons to restaurants "
    "and cafes across California.</p>"
    "<p>Below are our prices:</p>"
    "<p><strong>Paper</strong> (per case of 50 rolls):</p>"
    "<ul>"
    "<li>PF-230 Epson Thermal 3 1/8\" x 230' (phenol-free) — $124.10</li>"
    "<li>18-333 3\" three-ply (white/canary/pink) — $89.40</li>"
    "<li>CC-235 3\" two-ply Epson TMU-220 — $76.00</li>"
    "<li>13-305 Epson Impact 3\" one-ply x 165 — $59.00</li>"
    "</ul>"
    "<p><strong>Ink / Ribbons</strong> (per dozen):</p>"
    "<ul>"
    "<li>62245 black/red (Epson TM-220) — $42.00</li>"
    "<li>67240 black/red (Star SP700) — $52.00</li>"
    "</ul>"
    "<p>All prices are subject to tax and shipping.</p>"
    "<p>Feel free to compare — we'd love the chance to earn your business.</p>"
    "<p>Thank you,<br>Miles<br>Performance Supply Depot<br>psdepot.com | 1-888-881-6834</p>"
)

FOLLOWUP_BODY = (
    "<p>Hi there,</p>"
    "<p>Just following up on my note from earlier this week — wanted to make sure "
    "it didn't get buried. If you need thermal paper or printer ribbons, we'd love "
    "to earn your business.</p>"
    "<p>You can see our prices and order here: "
    f"<a href=\"{FORM_URL}\">order supplies</a></p>"
    "<p>Thanks!<br>Miles<br>Performance Supply Depot<br>psdepot.com | 1-888-881-6834</p>"
)

@activity.defn
async def send_cold_email(lead: dict) -> str:
    email = lead.get("email")
    if not email or "@" not in email:
        return "SKIP_NO_EMAIL"
    _send(email, "POS supplies — quick quote?", COLD_BODY)
    return "SENT"

@activity.defn
async def send_followup(lead: dict) -> str:
    email = lead.get("email")
    if not email or "@" not in email:
        return "SKIP_NO_EMAIL"
    _send(email, "Following up — POS supplies", FOLLOWUP_BODY)
    return "SENT_FOLLOWUP"

@activity.defn
async def check_reply(lead: dict) -> bool:
    """True if the lead has replied (a message from their email in the inbox log)."""
    email = (lead.get("email") or "").lower()
    try:
        inbox = json.load(open(INBOX))
    except Exception:
        return False
    for m in inbox.values():
        if email and email in (m.get("from") or "").lower():
            return True
    return False

@activity.defn
async def handle_reply(lead: dict) -> str:
    """CLOSETER classifies the lead's reply. Returns ORDER / QUESTION / INTEREST / NOT_INTERESTED / UNKNOWN."""
    email = (lead.get("email") or "").lower()
    try:
        inbox = json.load(open(INBOX))
    except Exception:
        return "UNKNOWN"
    body = ""
    for m in inbox.values():
        if email and email in (m.get("from") or "").lower():
            body = m.get("body", ""); break
    t = body or ""
    if re.search(r"not interested|no thanks|remove|unsubscribe|stop|don't need|pass", t, re.I):
        return "NOT_INTERESTED"
    if re.search(r"\?|how much|price|pricing|cost|shipping|tax|do you|what|which|available|in stock", t, re.I):
        return "QUESTION"
    if re.search(r"\border|buy|purchase|need|want|case|roll|dozen|pf-230|13-305|cc-235|18-333|62245|67240", t, re.I):
        return "ORDER"
    if re.search(r"interested|quote|info|more|thanks|tell me|yes", t, re.I):
        return "INTEREST"
    return "UNKNOWN"

@activity.defn
async def flag_order(lead: dict) -> str:
    """Flag an order to the Captain (payment is human-in-the-loop)."""
    try:
        orders = json.load(open(ORDERS))
    except Exception:
        orders = []
    orders.append({
        "lead": lead.get("name"), "email": lead.get("email"),
        "flagged_at": datetime.now(timezone.utc).isoformat(),
        "note": "ORDER — collect card (Captain in the loop).",
    })
    json.dump(orders, open(ORDERS, "w"), indent=2)
    return "FLAGGED"

@activity.defn
async def mark_closed(lead: dict) -> str:
    return "CLOSED"


@activity.defn
async def process_order(lead: dict) -> str:
    """Process a structured order (items) -> compute summary + vendor block + flag Captain."""
    items = lead.get("items") or []
    if not items:
        return "NO_ITEMS"
    import sys, json
    sys.path.insert(0, "/root/.openclaw/workspace/scripts")
    import order_processor
    summary = order_processor.process_order(items)
    vendor = order_processor.vendor_lines(summary)
    rec = {
        "lead": lead.get("name"), "email": lead.get("email"),
        "summary": summary, "vendor_lines": vendor,
        "flagged_at": datetime.now(timezone.utc).isoformat(),
        "note": "ORDER processed — collect card (Captain in the loop).",
    }
    try:
        orders = json.load(open(ORDERS))
    except Exception:
        orders = []
    orders.append(rec)
    json.dump(orders, open(ORDERS, "w"), indent=2)
    # email Captain with the full summary
    try:
        c = _smtp()
        body = (f"New order (processed):\n\n"
                f"Business: {lead.get('name','')}\nEmail: {lead.get('email','')}\n\n"
                f"--- SUMMARY ---\n")
        for l in summary["lines"]:
            body += f"  {l['qty']} x {l['sku']} {l['name']} = ${l['sell']:.2f}\n"
        body += (f"Subtotal ${summary['subtotal']:.2f} + tax ${summary['tax']:.2f} = "
                 f"${summary['total']:.2f}\nProfit ${summary['margin']:.2f} ({summary['margin_pct']}%)\n\n"
                 f"--- VENDOR ---\n{vendor}\n")
        msg = MIMEText(body)
        msg["From"] = f"Performance Supply Depot <{c['SALES_SMTP_USER']}>" if 'SALES_SMTP_USER' in c else f"Performance Supply Depot <{c['HOSTINGER_SMTP_USER']}>"
        msg["To"] = "info@psdepot.com"
        msg["Subject"] = f"New order — {lead.get('name')}"
        s = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
        s.starttls()
        s.login(c["SALES_SMTP_USER"], c["SALES_SMTP_PASS"])
        s.sendmail(c["SALES_SMTP_USER"], ["info@psdepot.com"], msg.as_string())
        s.quit()
    except Exception:
        pass
    return "PROCESSED"
