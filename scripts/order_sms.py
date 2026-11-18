#!/usr/bin/env python3
"""
ORDER SMS — visual order confirmation + reply-to-confirm, fully wired into the
courtesy-invoice pipeline.

Flow:
  1. Customer places an order. Send them a visual SMS (line items + total).
  2. Customer replies "YES" to confirm (or texts a correction).
  3. On "YES" -> FIRE the invoice:
       - assign PO + build internal profit summary (order_processor.order_email)
       - generate courtesy-invoice PDF + email customer (attached)
       - flag Captain via email AND Telegram
       - SMS Captain
       - log to datadepot/data/closeter_orders.json

Order dict (caller supplies):
  {
    "business": "Bungalow 44",          # business_name
    "name": "Peter Schumacher",         # manager/contact
    "phone": "+14153812500",
    "email": "peterschumacher2@gmail.com",
    "address": "3068 Claremont Ave",
    "city": "Berkeley", "state": "CA", "zip": "94705",
    "items": [{"sku": "62245", "qty": 6}, {"sku": "13-305", "qty": 3}],
    "special_instructions": "",         # optional
  }
"""
import os, re, json, smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

BASE = "/root/.openclaw/workspace"
STATE_FILE = f"{BASE}/data/order_sms_state.json"
LOG_FILE = f"{BASE}/data/order_sms_log.json"
ORDERS_LOG = f"{BASE}/datadepot/data/closeter_orders.json"
FROM_NUMBER = "+18557899606"

# SMTP (matches voice_server.py GREET — gmail app password)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "performancesupplydepotsales@gmail.com"
SMTP_PASS = "nlelxrhbxinxklnp"
NOTIFY_TO = ["info@psdepot.com", "antonio.hudnall@gmail.com"]
CAPTAIN_SMS = "+14155326834"   # Captain's cell (415-532-6834)

TELEGRAM_ENV = f"{BASE}/aocros/secrets/telegram.env"


# ---------- notify helpers (email + telegram + sms) ----------
def _telegram_creds():
    c = {}
    try:
        for line in open(TELEGRAM_ENV):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                c[k] = v
    except FileNotFoundError:
        pass
    return c


def _telegram_send(text):
    import requests
    c = _telegram_creds()
    token = c.get("TELEGRAM_BOT_TOKEN", "")
    chat = c.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat:
        return False
    try:
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json={"chat_id": chat, "text": text}, timeout=10)
        return bool(r.json().get("ok"))
    except Exception:
        return False


def _send_sms(to, body, from_=None):
    import sys
    if f"{BASE}/scripts" not in sys.path:
        sys.path.insert(0, f"{BASE}/scripts")
    from sms import send_sms
    return send_sms(to, body, from_=from_)


def _send_email(to, subject, body_html, attachments=None):
    if attachments:
        msg = MIMEMultipart("mixed")
        msg.attach(MIMEText(body_html, "html"))
        for p in attachments:
            if not os.path.exists(p):
                continue
            part = MIMEBase("application", "octet-stream")
            part.set_payload(open(p, "rb").read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                            f'attachment; filename="{os.path.basename(p)}"')
            msg.attach(part)
    else:
        msg = MIMEText(body_html, "html")
    msg["From"] = f"Performance Supply Depot <{SMTP_USER}>"
    msg["To"] = to
    msg["Bcc"] = "info@psdepot.com"
    msg["Subject"] = subject
    rcpts = [to, "info@psdepot.com"]
    s = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
    s.starttls()
    s.login(SMTP_USER, SMTP_PASS)
    s.sendmail(SMTP_USER, rcpts, msg.as_string())
    s.quit()
    return True


def _notify_captain(subject, body_html):
    """Flag Captain via email AND Telegram."""
    try:
        _send_email("info@psdepot.com", subject, body_html)
    except Exception as e:
        print("[notify] email failed:", e)
    try:
        _telegram_send(f"📦 {subject}\n{body_html}")
    except Exception as e:
        print("[notify] telegram failed:", e)


# ---------- order summary ----------
def _build_summ(order):
    import sys
    if f"{BASE}/scripts" not in sys.path:
        sys.path.insert(0, f"{BASE}/scripts")
    import order_processor as op
    items = order.get("items") or []
    summ = op.process_order(items)
    summ.update({
        "business_name": order.get("business", ""),
        "manager_name": order.get("name", ""),
        "email": order.get("email", ""),
        "address": order.get("address", ""),
        "city": order.get("city", ""),
        "state": order.get("state", ""),
        "zip": order.get("zip", ""),
        "phone": order.get("phone", ""),
        "date": datetime.now().strftime("%m/%d/%Y"),
        "special_instructions": order.get("special_instructions", ""),
    })
    return summ


# ---------- formatting ----------
def format_order_sms(summ, ask_confirm=True):
    lines = ["PERFORMANCE SUPPLY DEPOT"]
    biz = summ.get("business_name")
    if biz:
        lines.append(biz)
    lines.append("")
    for l in summ.get("lines", []):
        lines.append(f"{l['sku']} x{l['qty']}  ${l['sell']:,.2f}")
    lines.append(f"Total: ${summ['total']:,.2f}")
    if ask_confirm:
        lines.append("")
        lines.append("Reply YES to confirm, or text any correction.")
    return "\n".join(lines)


# ---------- reply parsing ----------
def parse_reply(body):
    t = (body or "").strip().lower()
    t = re.sub(r"^[\s:;,\-]+", "", t)
    yes_pat = r"\b(yes|yep|yeah|correct|ok|okay|confirmed|confirm|approve|good|looks good|y)\b"
    no_pat = r"\b(no|nope|incorrect|wrong|not right|reject)\b"
    if re.search(no_pat, t) and not re.search(yes_pat, t):
        return {"action": "reject", "text": t}
    if re.search(yes_pat, t) and len(t) <= 40:
        return {"action": "confirm", "text": t}
    return {"action": "correction", "text": t}


# ---------- state store ----------
def _load_state():
    try:
        return json.load(open(STATE_FILE))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    json.dump(s, open(STATE_FILE, "w"), indent=2)


def _append_log(entry):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    try:
        log = json.load(open(LOG_FILE))
    except (FileNotFoundError, json.JSONDecodeError):
        log = []
    log.append(entry)
    json.dump(log, open(LOG_FILE, "w"), indent=2)


def _normalize_phone(p):
    return re.sub(r"\D", "", p or "")[-10:]


# ---------- fire the invoice (on "YES") ----------
def fire_invoice(summ):
    """Run the full courtesy-invoice pipeline. Returns dict with po + status."""
    import sys
    if f"{BASE}/scripts" not in sys.path:
        sys.path.insert(0, f"{BASE}/scripts")
    import order_processor as op

    # 1. Assign PO + build internal profit summary (also sets summ['po'])
    body = op.order_email(summ)
    po = summ.get("po")

    # 2. Flag Captain (internal summary) — email + Telegram
    _notify_captain(f"✅ Order {po} CONFIRMED", body.replace("\n", "<br>"))

    # 3. Email customer with courtesy invoice (PDF attached)
    if summ.get("email"):
        try:
            pdf = f"/tmp/invoice_{po}.pdf"
            op.courtesy_invoice_pdf(summ, pdf)
            cust = op.customer_email(summ).replace("\n", "<br>")
            inv = op.courtesy_invoice_html(summ)
            _send_email(summ["email"], f"Your order {po} — Performance Supply Depot",
                        cust + "<hr>" + inv, attachments=[pdf])
        except Exception as e:
            print("[fire] customer email failed:", e)

    # 4. SMS Captain
    try:
        _send_sms(CAPTAIN_SMS, f"Order {po} confirmed: {summ['business_name'] or ''} — total ${summ['total']:.2f}")
    except Exception as e:
        print("[fire] sms failed:", e)

    # 5. Log order
    _log_order(summ, po)

    return {"po": po, "total": summ["total"], "status": "fired"}


def _log_order(summ, po):
    os.makedirs(os.path.dirname(ORDERS_LOG), exist_ok=True)
    try:
        orders = json.load(open(ORDERS_LOG))
    except Exception:
        orders = []
    orders.append({
        "source": "sms", "po": po, "business": summ.get("business_name", ""),
        "name": summ.get("manager_name", ""), "phone": summ.get("phone", ""),
        "email": summ.get("email", ""), "address": summ.get("address", ""),
        "city": summ.get("city", ""), "state": summ.get("state", ""),
        "zip": summ.get("zip", ""), "items": summ.get("lines", []),
        "quote": summ,
        "flagged_at": datetime.now(timezone.utc).isoformat(),
        "note": "SMS order — customer confirmed YES. Courtesy invoice emailed.",
    })
    json.dump(orders, open(ORDERS_LOG, "w"), indent=2)


# ---------- high-level API ----------
def send_order_confirmation(to_number, order, from_=None):
    """Send a confirmation SMS + store the full order pending customer reply.

    Returns (sid, summ). summ is cached in state so the reply can fire the invoice.
    """
    summ = _build_summ(order)
    body = format_order_sms(summ, ask_confirm=True)
    sid = _send_sms(to_number, body, from_=from_)
    now = datetime.now(timezone.utc).isoformat()
    state = _load_state()
    key = _normalize_phone(to_number)
    state[key] = {
        "status": "pending",
        "sent_at": now,
        "message_sid": sid,
        "order": order,          # full original order (for re-building)
        "summ": summ,            # cached summary (for firing)
    }
    _save_state(state)
    _append_log({
        "ts": now, "direction": "outbound", "to": to_number,
        "business": order.get("business"), "sid": sid, "status": "pending",
    })
    return sid, summ


def handle_reply(from_number, body):
    """Process a customer reply. On confirm -> fire the invoice. Returns result dict."""
    now = datetime.now(timezone.utc).isoformat()
    parsed = parse_reply(body)
    state = _load_state()
    key = _normalize_phone(from_number)
    pending = state.get(key)

    result = {
        "action": parsed["action"], "text": parsed["text"],
        "matched": bool(pending),
        "business": (pending or {}).get("order", {}).get("business"),
    }

    if pending:
        summ = pending.get("summ")
        if parsed["action"] == "confirm":
            pending["status"] = "confirmed"
            pending["confirmed_at"] = now
            _save_state(state)
            if summ:
                fired = fire_invoice(summ)
                result["fired"] = fired
                result["po"] = fired.get("po")
            # Thank the customer for confirming
            _send_sms(from_number,
                      "Thank you for confirming your order! Your courtesy invoice is on its way. - Performance Supply Depot")
        elif parsed["action"] == "reject":
            pending["status"] = "rejected"
            pending["rejected_at"] = now
            _save_state(state)
            _notify_captain(
                f"❌ Order rejected via SMS — {result['business'] or from_number}",
                f"Customer {from_number} replied: \"{body}\"")
        else:
            pending["status"] = "correction"
            pending["correction"] = parsed["text"]
            _save_state(state)
            _notify_captain(
                f"✏️ Order correction via SMS — {result['business'] or from_number}",
                f"Customer {from_number} replied: \"{body}\"")

    _append_log({
        "ts": now, "direction": "inbound", "from": from_number,
        "body": body, "action": parsed["action"], "matched": bool(pending),
        "po": result.get("po"),
    })
    return result


# ---------- CLI ----------
def main():
    import argparse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("send")
    sp.add_argument("--to", required=True)
    sp.add_argument("--order", required=True, help="path to order JSON")

    pp = sub.add_parser("parse")
    pp.add_argument("--body", required=True)

    args = ap.parse_args()

    if args.cmd == "send":
        order = json.load(open(args.order))
        sid, summ = send_order_confirmation(args.to, order)
        print(f"SID={sid}")
        print(format_order_sms(summ))
    elif args.cmd == "parse":
        print(json.dumps(parse_reply(args.body), indent=2))


if __name__ == "__main__":
    main()
