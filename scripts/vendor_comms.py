#!/usr/bin/env python3
"""
vendor_comms.py — Miles vendor communications toolkit

Scope (per Captain, 2026-08-30):
  - Inbound: detect new emails (any sender) and surface them for reporting.
  - Outbound: reach out to vendors, place orders on Captain's behalf.
  - NOT customers yet — customers are a later, separate gate.

Modes:
  check                 Check inbox for new email, print a summary, record state.
  send                  Send an outbound email (order/inquiry) and log it.
  orders                List orders placed so far.
  add-vendor            Add a vendor contact to the vendor directory.

Credentials are read from workspace/.env (single source of truth) — no plaintext here.
"""

import imaplib
import smtplib
import ssl
import json
import sys
import os
import re
from datetime import datetime, timezone
from email.parser import BytesParser
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
ENV_FILE = WORKSPACE / ".env"
STATE_FILE = WORKSPACE / "data" / "vendor_comms_state.json"
INBOX_DIR = WORKSPACE / "data" / "email_inbox"
VENDOR_FILE = WORKSPACE / "data" / "vendor_contacts.json"

CAPTAIN_EMAILS = ("antonio.hudnall@gmail.com", "hcindus")


def load_env():
    """Parse workspace/.env into a dict."""
    cfg = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
    return cfg


def get_config():
    env = load_env()
    return {
        "email": env.get("HOSTINGER_SMTP_USER", "miles@myl0nr0s.cloud"),
        "password": env.get("HOSTINGER_SMTP_PASS", ""),
        "imap_server": env.get("HOSTINGER_IMAP_SERVER", "imap.hostinger.com"),
        "imap_port": int(env.get("HOSTINGER_IMAP_PORT", "993")),
        "smtp_server": env.get("HOSTINGER_SMTP_SERVER", "smtp.hostinger.com"),
        "smtp_port": int(env.get("HOSTINGER_SMTP_PORT", "587")),
    }


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"seen_uids": [], "orders": []}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def load_vendors():
    if VENDOR_FILE.exists():
        try:
            return json.loads(VENDOR_FILE.read_text())
        except Exception:
            pass
    return {}


def save_vendors(vendors):
    VENDOR_FILE.parent.mkdir(parents=True, exist_ok=True)
    VENDOR_FILE.write_text(json.dumps(vendors, indent=2))


def decode_header_value(v):
    if not v:
        return ""
    parts = decode_header(v)
    out = ""
    for part, charset in parts:
        if isinstance(part, bytes):
            out += part.decode(charset or "utf-8", errors="replace")
        else:
            out += part
    return out


def extract_addr(from_header):
    """Pull the email address out of a From header."""
    m = re.search(r"[\w.+-]+@[\w.-]+", from_header or "")
    return m.group(0).lower() if m else (from_header or "").lower()


def extract_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                except Exception:
                    body = ""
                if body.strip():
                    break
    else:
        try:
            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
        except Exception:
            body = ""
    return body.strip()


def categorize(sender, subject, body):
    """Best-effort category: captain / vendor / customer / other."""
    low = f"{sender} {subject} {body}".lower()
    addr = extract_addr(sender)
    if addr in CAPTAIN_EMAILS or "antonio.hudnall" in addr:
        return "captain"
    vendors = load_vendors()
    for name, v in vendors.items():
        v_email = (v.get("email") or "").lower()
        if v_email and v_email in addr:
            return "vendor"
    vendor_kw = ["order", "invoice", "quote", "po ", "purchase", "price", "pricing",
                 "lead time", "stock", "inventory", "shipping", "supplier", "vendor",
                 "reseller", "volume", "standing order", "backorder"]
    customer_kw = ["customer", "my order", "refund", "return", "tracking",
                   "where's my", "support", "help with my", "complaint"]
    if any(k in low for k in vendor_kw):
        return "vendor"
    if any(k in low for k in customer_kw):
        return "customer"
    return "other"


def check_inbox():
    cfg = get_config()
    state = load_state()
    seen = set(state.get("seen_uids", []))
    new_emails = []

    if not cfg["password"]:
        print("ERROR: no password in .env (HOSTINGER_SMTP_PASS)")
        sys.exit(1)

    context = ssl.create_default_context()
    try:
        imap = imaplib.IMAP4_SSL(cfg["imap_server"], cfg["imap_port"], ssl_context=context)
        imap.login(cfg["email"], cfg["password"])
        imap.select("INBOX")

        status, data = imap.uid("search", None, "UNSEEN")
        if status != "OK":
            print("NO_NEW_EMAIL")
            imap.logout()
            return

        uids = data[0].split()
        if not uids:
            print("NO_NEW_EMAIL")
            imap.logout()
            return

        for uid in uids:
            uid_str = uid.decode()
            if uid_str in seen:
                continue
            status, msg_data = imap.uid("fetch", uid, "(RFC822)")
            if status != "OK":
                continue
            raw = msg_data[0][1]
            msg = BytesParser().parsebytes(raw)

            sender = decode_header_value(msg.get("From"))
            subject = decode_header_value(msg.get("Subject"))
            body = extract_body(msg)
            category = categorize(sender, subject, body)

            email_data = {
                "uid": uid_str,
                "from": sender,
                "from_addr": extract_addr(sender),
                "subject": subject,
                "body": body[:5000],
                "category": category,
                "received_at": datetime.now(timezone.utc).isoformat(),
            }

            # Save full copy
            INBOX_DIR.mkdir(parents=True, exist_ok=True)
            safe = re.sub(r"[^\w]", "_", uid_str)[:40]
            (INBOX_DIR / f"{safe}.json").write_text(json.dumps(email_data, indent=2))

            new_emails.append(email_data)
            seen.add(uid_str)
            imap.uid("store", uid, "+FLAGS", "\\Seen")

        imap.logout()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    state["seen_uids"] = list(seen)
    save_state(state)

    if not new_emails:
        print("NO_NEW_EMAIL")
        return

    print(f"NEW_EMAILS {len(new_emails)}")
    for e in new_emails:
        snippet = " ".join(e["body"].split())[:160]
        print(f"- [{e['category'].upper()}] {e['from']} | {e['subject']} | {snippet}")


def send_email(to, subject, body, bcc=None):
    cfg = get_config()
    if not cfg["password"]:
        print("ERROR: no password in .env (HOSTINGER_SMTP_PASS)")
        sys.exit(1)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Performance Supply Depot <{cfg['email']}>"
    msg["To"] = to
    if bcc:
        msg["Bcc"] = bcc
    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"], timeout=30) as server:
            server.starttls(context=context)
            server.login(cfg["email"], cfg["password"])
            server.send_message(msg)
    except Exception as e:
        print(f"ERROR: send failed: {e}")
        sys.exit(1)

    state = load_state()
    order = {
        "to": to,
        "subject": subject,
        "body": body[:3000],
        "bcc": bcc,
        "sent_at": datetime.now(timezone.utc).isoformat(),
    }
    state.setdefault("orders", []).append(order)
    save_state(state)
    print(f"SENT to {to}: {subject}")


def list_orders():
    state = load_state()
    orders = state.get("orders", [])
    if not orders:
        print("No orders placed yet.")
        return
    for i, o in enumerate(orders, 1):
        print(f"{i}. [{o['sent_at']}] -> {o['to']} | {o['subject']}")


def add_vendor(name, email, notes=""):
    vendors = load_vendors()
    vendors[name] = {"email": email, "notes": notes}
    save_vendors(vendors)
    print(f"Added vendor {name} <{email}>")


# ─────────────────────────────────────────────────────────────────
# ORDER AUTOMATION
# ─────────────────────────────────────────────────────────────────
ORDERS_INBOX = WORKSPACE / "data" / "orders" / "inbox"
ORDERS_SENT = WORKSPACE / "data" / "orders" / "sent"
ORDERS_HISTORY = WORKSPACE / "data" / "orders" / "history.json"

COMPANY = "Performance Supply Depot LLC"
SIGNATURE = "Miles\nPerformance Supply Depot LLC\nmiles@myl0nr0s.cloud"


def load_order_history():
    if ORDERS_HISTORY.exists():
        try:
            return json.loads(ORDERS_HISTORY.read_text())
        except Exception:
            pass
    return []


def save_order_history(history):
    ORDERS_HISTORY.parent.mkdir(parents=True, exist_ok=True)
    ORDERS_HISTORY.write_text(json.dumps(history, indent=2))


def next_po_number():
    hist = load_order_history()
    year = datetime.now(timezone.utc).strftime("%Y")
    n = len(hist) + 1
    return f"PSD-{year}-{n:04d}"


def render_intro_email(name, vendor):
    return f"""Hello {name},

I'm Miles with {COMPANY}. We supply point-of-sale (POS) hardware and consumables to businesses across the U.S., and we're currently evaluating vendors for our ongoing procurement needs.

I'd like to learn more about your product line and terms. Specifically, could you share:

1. Your current catalog / price list
2. Volume breaks and any reseller or standing-order pricing
3. Lead times and minimum order quantities
4. Shipping options to California

If it's easier, I'm happy to hop on a call or share our typical order volumes so you can tailor a quote.

Thanks — looking forward to working together.

Best,
{SIGNATURE}"""


def render_order_email(spec):
    po = spec.get("po") or next_po_number()
    lines = []
    lines.append(f"Hello {spec.get('contact_name', '')},".strip())
    lines.append("")
    lines.append(f"I'd like to place the following order (PO {po}):")
    lines.append("")
    for item in spec.get("items", []):
        price = item.get("price")
        price_s = f" @ ${price:,.2f}" if price else ""
        lines.append(f"  - {item.get('qty')} x {item.get('sku', '')} — {item.get('desc', '')} ({item.get('unit', 'each')}){price_s}")
    lines.append("")
    ship_to = spec.get("ship_to")
    if ship_to:
        lines.append("Ship to:")
        lines.append(ship_to)
        lines.append("")
    if spec.get("quote_only"):
        lines.append("Before confirming, please send a final quote with total (including shipping and any applicable tax).")
    else:
        lines.append("Please confirm availability, lead time, and total (including shipping).")
    notes = spec.get("notes")
    if notes:
        lines.append("")
        lines.append(f"Note: {notes}")
    lines.append("")
    lines.append("Thank you,")
    lines.append(SIGNATURE)
    return "\n".join(lines)


def introduce(name):
    vendors = load_vendors()
    if name not in vendors:
        print(f"ERROR: vendor '{name}' not in directory. Add it first with add-vendor.")
        sys.exit(1)
    v = vendors[name]
    if not v.get("email"):
        print(f"ERROR: vendor '{name}' has no email on file.")
        sys.exit(1)
    body = render_intro_email(name, v)
    subject = f"Introduction — {COMPANY} (POS supplies)"
    send_email(v["email"], subject, body, bcc="info@psdepot.com")
    print(f"Intro sent to {name} <{v['email']}>")


def process_order(spec_path):
    spec = json.loads(Path(spec_path).read_text())
    vendors = load_vendors()
    vendor_name = spec.get("vendor")
    to = spec.get("vendor_email")

    if not to and vendor_name in vendors:
        to = vendors[vendor_name].get("email")
    if not to:
        print("ERROR: order spec needs 'vendor_email' or a known 'vendor' with email on file.")
        sys.exit(1)

    po = spec.get("po") or next_po_number()
    subject = f"Order Request — {po} | {COMPANY}"
    body = render_order_email(spec)
    send_email(to, subject, body, bcc="info@psdepot.com")

    # Record in order history
    hist = load_order_history()
    hist.append({
        "po": po,
        "vendor": vendor_name,
        "vendor_email": to,
        "items": spec.get("items", []),
        "ship_to": spec.get("ship_to"),
        "quote_only": spec.get("quote_only", False),
        "status": "sent",
        "sent_at": datetime.now(timezone.utc).isoformat(),
    })
    save_order_history(hist)

    # Move spec to sent/
    ORDERS_SENT.mkdir(parents=True, exist_ok=True)
    dest = ORDERS_SENT / Path(spec_path).name
    Path(spec_path).rename(dest)

    print(f"Order {po} sent to {to}; spec archived to {dest}")


def process_inbox():
    """Send any order specs sitting in the inbox."""
    ORDERS_INBOX.mkdir(parents=True, exist_ok=True)
    specs = sorted(ORDERS_INBOX.glob("*.json"))
    if not specs:
        print("No order specs in inbox.")
        return
    for spec in specs:
        try:
            process_order(str(spec))
        except Exception as e:
            print(f"ERROR processing {spec.name}: {e}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0]
    if cmd == "check":
        check_inbox()
    elif cmd == "orders":
        list_orders()
    elif cmd == "add-vendor":
        if len(args) < 3:
            print("usage: vendor_comms.py add-vendor <name> <email> [notes]")
            return
        add_vendor(args[1], args[2], " ".join(args[3:]))
    elif cmd == "introduce":
        if len(args) < 2:
            print("usage: vendor_comms.py introduce <vendor-name>")
            return
        introduce(args[1])
    elif cmd == "order":
        if len(args) < 2:
            print("usage: vendor_comms.py order <spec.json>")
            return
        process_order(args[1])
    elif cmd == "process-inbox":
        process_inbox()
    elif cmd == "send":
        to = None
        subject = None
        body = None
        bcc = None
        it = iter(args[1:])
        for a in it:
            if a == "--to":
                to = next(it)
            elif a == "--subject":
                subject = next(it)
            elif a == "--body":
                body = next(it)
            elif a == "--bcc":
                bcc = next(it)
        if not (to and subject and body):
            print("usage: vendor_comms.py send --to X --subject Y --body Z [--bcc B]")
            sys.exit(1)
        send_email(to, subject, body, bcc)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
