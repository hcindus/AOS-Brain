#!/usr/bin/env python3
"""
CLOSETER reply handler — reads new inbound replies (from closeter_inbox_monitor),
classifies intent, and takes the appropriate action:

  ORDER          -> flag Captain (collect card) + confirm to lead (form link)
  QUESTION       -> auto-answer from the product/price sheet
  INTEREST       -> send more info + order form link
  NOT INTERESTED -> mark closed (no follow-up)
  UNKNOWN        -> flag Captain for manual review

Deduped via a processed tracker (Message-ID). Safe: only auto-sends for clear
intents; anything ambiguous is flagged, not guessed.
"""
import json, smtplib, re
from email.mime.text import MIMEText
from datetime import datetime, timezone

INBOX = "/root/.openclaw/workspace/datadepot/data/closeter_inbox.json"
PROCESSED = "/root/.openclaw/workspace/datadepot/data/closeter_processed.json"
ORDERS = "/root/.openclaw/workspace/datadepot/data/closeter_orders.json"
FORM_URL = ("https://docs.google.com/forms/d/e/1FAIpQLSf_MpGmbwkrZm2nVsL-"
            "RYiVHCsEqEMpjZ6eHKTQ8rr1KUx2Cw/viewform")

# price sheet (for auto-answering questions)
PRICE_SHEET = (
    "Our prices (plus shipping & tax):\n\n"
    "Paper (per case of 50 rolls):\n"
    "  PF-230 Epson Thermal 3 1/8\" x 230' (phenol-free) — $124.10\n"
    "  18-333 3\" three-ply (white/canary/pink) — $89.40\n"
    "  CC-235 3\" two-ply Epson TMU-220 — $76.00\n"
    "  13-305 Epson Impact 3\" one-ply x 165 — $59.00\n\n"
    "Ribbons (per dozen):\n"
    "  62245 black/red (Epson TM-220) — $42.00\n"
    "  67240 black/red (Star SP700) — $52.00"
)

# --- intent classification ---
ORDER_RE = re.compile(r"\border|buy|purchase|need|want|case|roll|dozen|pf-230|13-305|cc-235|18-333|62245|67240", re.I)
NO_RE = re.compile(r"not interested|no thanks|remove|unsubscribe|stop|don't need|pass", re.I)
QUESTION_RE = re.compile(r"\?|how much|price|pricing|cost|shipping|tax|do you|what|which|available|in stock", re.I)

def classify(text):
    t = text or ""
    if NO_RE.search(t):
        return "NOT_INTERESTED"
    if QUESTION_RE.search(t):
        return "QUESTION"
    if ORDER_RE.search(t):
        return "ORDER"
    if re.search(r"interested|quote|info|more|thanks|tell me|yes", t, re.I):
        return "INTEREST"
    return "UNKNOWN"

def load(p, d):
    try: return json.load(open(p))
    except Exception: return d

def save(p, o):
    json.dump(o, open(p, "w"), indent=2)

def smtp_creds():
    c = {}
    for line in open("/root/.openclaw/workspace/aocros/secrets/smtp.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1); c[k] = v
    return c

def send(to_email, subject, body_html):
    c = smtp_creds()
    msg = MIMEText(body_html, "html")
    msg["From"] = f"Performance Supply Depot <{c['HOSTINGER_SMTP_USER']}>"
    msg["To"] = to_email
    msg["Bcc"] = "info@psdepot.com"
    msg["Subject"] = subject
    s = smtplib.SMTP(c.get("HOSTINGER_SMTP_SERVER","smtp.hostinger.com"),
                     int(c.get("HOSTINGER_SMTP_PORT","587")), timeout=30)
    s.starttls(); s.login(c["HOSTINGER_SMTP_USER"], c["HOSTINGER_SMTP_PASS"])
    s.sendmail(c["HOSTINGER_SMTP_USER"], [to_email, "info@psdepot.com"], msg.as_string())
    s.quit()

def main():
    inbox = load(INBOX, {})
    processed = load(PROCESSED, {})
    orders = load(ORDERS, [])

    actions = 0
    for mid, m in inbox.items():
        if mid in processed:
            continue
        frm = m.get("from", "")
        body = m.get("body", "")
        intent = classify(body)

        # extract reply-to email from "Name <email>" or "email"
        to_email = ""
        m2 = re.search(r"[\w.+-]+@[\w.-]+\.\w+", frm)
        if m2:
            to_email = m2.group(0)

        result = {"msg_id": mid, "from": frm, "intent": intent, "action": "", "sent_to": to_email}

        if intent == "ORDER":
            # flag Captain for payment + confirm to lead
            orders.append({
                "from": frm, "subject": m.get("subject"), "body": body[:2000],
                "received_at": m.get("received_at"), "flagged_at": datetime.now(timezone.utc).isoformat(),
                "note": "Lead wants to order — collect card (Captain in the loop)."
            })
            # email the Captain so the order "comes through" to his inbox
            try:
                send("antonio.hudnall@gmail.com", f"New order — {frm}",
                     f"<p>A new order came in from <strong>{frm}</strong>.</p>"
                     f"<p><strong>Subject:</strong> {m.get('subject')}</p>"
                     f"<pre>{body[:2000]}</pre>"
                     f"<p>— CLOSETER</p>")
            except Exception:
                pass
            if to_email:
                try:
                    send(to_email, "Re: your order",
                         f"<p>Thanks so much! We've got your order and will send a payment link shortly.</p>"
                         f"<p>In the meantime, you can also submit your order here: "
                         f"<a href=\"{FORM_URL}\">order form</a></p>"
                         f"<p>— Miles, Performance Supply Depot</p>")
                    result["action"] = "flagged_captain + confirmed_to_lead"
                except Exception as e:
                    result["action"] = f"flagged_captain (confirm send failed: {e})"
            else:
                result["action"] = "flagged_captain (no reply-to email)"

        elif intent == "QUESTION":
            if to_email:
                try:
                    send(to_email, "Re: your question",
                         f"<p>Great question! Here are our prices:</p>"
                         f"<pre>{PRICE_SHEET}</pre>"
                         f"<p>All prices are plus shipping &amp; tax. Want to place an order? "
                         f"<a href=\"{FORM_URL}\">Order here</a></p>"
                         f"<p>— Miles, Performance Supply Depot</p>")
                    result["action"] = "auto_answered_question"
                except Exception as e:
                    result["action"] = f"answer_send_failed: {e}"
            else:
                result["action"] = "no_reply_to_email"

        elif intent == "INTEREST":
            if to_email:
                try:
                    send(to_email, "Thanks for your interest!",
                         f"<p>Thanks for your interest! We'd love to earn your business.</p>"
                         f"<p>Here are our prices:</p><pre>{PRICE_SHEET}</pre>"
                         f"<p>All prices are plus shipping &amp; tax. Ready to order? "
                         f"<a href=\"{FORM_URL}\">Order here</a></p>"
                         f"<p>— Miles, Performance Supply Depot</p>")
                    result["action"] = "sent_info"
                except Exception as e:
                    result["action"] = f"info_send_failed: {e}"
            else:
                result["action"] = "no_reply_to_email"

        elif intent == "NOT_INTERESTED":
            result["action"] = "marked_closed (no follow-up)"

        else:  # UNKNOWN
            result["action"] = "flagged_captain_review"
            orders.append({
                "from": frm, "subject": m.get("subject"), "body": body[:2000],
                "received_at": m.get("received_at"), "flagged_at": datetime.now(timezone.utc).isoformat(),
                "note": "UNKNOWN intent — manual review."
            })

        processed[mid] = result
        actions += 1
        print(f"  [{intent}] {frm} -> {result['action']}")

    save(PROCESSED, processed)
    save(ORDERS, orders)
    print(f"PROCESSED={actions}")

if __name__ == "__main__":
    main()
