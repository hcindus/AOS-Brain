#!/usr/bin/env python3
"""
Reusable CALL-BACK skill — any department can call back any customer/lead via Twilio
and log the outcome to DepotChaos (sales_contacts + vendor).

Usage:
  # call back a single number (logs outcome to DepotChaos)
  python3 call_back.py --to +14155552671 --name "Via Piccola" --channel outbound

  # mark the outcome after you (or a rep) dialed
  python3 call_back.py --to +14155552671 --name "Via Piccola" \
      --outcome reached --want_prices yes --note "wants pricing, reorder soon"

  # work a queue (e.g. courtesy_callbacks.json)
  python3 call_back.py --queue datadepot/data/courtesy_callbacks.json
"""
import argparse, json, os, sqlite3, sys
from datetime import datetime, timezone

sys.path.insert(0, "/root/.openclaw/workspace/scripts")

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
TWILIO_ENV = "/root/.openclaw/workspace/aocros/secrets/twilio.env"

OUTCOMES = {"reached", "voicemail", "no_answer", "interested", "not_interested",
            "order", "question", "opted_out", "reengage"}


def twilio_creds():
    c = {}
    for line in open(TWILIO_ENV):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            c[k.strip()] = v.strip()
    return c


def find_vendor_by_phone(phone):
    import re
    con = sqlite3.connect(DB)
    cur = con.cursor()
    d = re.sub(r"\D", "", phone or "")[-10:]
    cur.execute("SELECT id, name, phone FROM vendors WHERE phone IS NOT NULL AND phone != ''")
    for vid, name, p in cur.fetchall():
        pd = re.sub(r"\D", "", p or "")[-10:]
        if d and pd == d:
            con.close()
            return vid, name
    con.close()
    return None, None


def log_contact(phone, name, channel, outcome, want_prices, note, contact_type="phone"):
    now = datetime.now(timezone.utc).isoformat()
    vid, vend_name = find_vendor_by_phone(phone)
    lead_name = vend_name or name or phone
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO sales_contacts (vendor_id, lead_name, contact_type, channel, outcome, want_prices, notes, contacted_at) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (vid, lead_name, contact_type, channel, outcome, want_prices, note, now))
    if vid:
        cur.execute("UPDATE vendors SET last_contact_at=?, last_outcome=?, contact_preference=? WHERE id=?",
                    (now, outcome, "phone", vid))
    con.commit()
    con.close()
    return lead_name


def twilio_dial(to_number):
    """Place an outbound call via Twilio (returns the call SID or None)."""
    c = twilio_creds()
    sid = c.get("TWILIO_ACCOUNT_SID")
    token = c.get("TWILIO_AUTH_TOKEN")
    if not sid or not token:
        return None
    try:
        from twilio.rest import Client
        client = Client(sid, token)
        from_num = c.get("TWILIO_FROM_NUMBER") or "+18557899606"
        # TwiML URL for the voice script (set via env, or leave a stub)
        twiml_url = c.get("TWILIO_TWIML_URL")
        if not twiml_url:
            return None  # no voice script URL configured yet — just log
        call = client.calls.create(to=to_number, from_=from_num, url=twiml_url)
        return call.sid
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to")
    ap.add_argument("--name", default="")
    ap.add_argument("--channel", default="outbound", choices=["inbound", "outbound"])
    ap.add_argument("--outcome", default="reengage", choices=sorted(OUTCOMES))
    ap.add_argument("--want_prices", default=None, choices=["yes", "no"])
    ap.add_argument("--note", default="")
    ap.add_argument("--dial", action="store_true", help="actually place a Twilio call")
    ap.add_argument("--queue", help="JSON file of {number, script} entries")
    args = ap.parse_args()

    if args.queue:
        q = json.load(open(args.queue))
        for entry in q:
            num = entry.get("number")
            if not num:
                continue
            if args.dial:
                twilio_dial(num)
            lead = log_contact(num, entry.get("name", ""), args.channel,
                               "reengage", None, "queued call-back")
            print(f"LOGGED {lead} ({num})")
        return

    if not args.to:
        ap.error("--to or --queue is required")

    if args.dial:
        sid = twilio_dial(args.to)
        print(f"TWILIO_CALL={sid or 'not-placed (no TwiML URL)'}")

    lead = log_contact(args.to, args.name, args.channel, args.outcome,
                       args.want_prices, args.note)
    print(f"LOGGED {lead} ({args.to}) -> outcome={args.outcome} want_prices={args.want_prices}")


if __name__ == "__main__":
    main()
