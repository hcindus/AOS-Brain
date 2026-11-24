#!/usr/bin/env python3
"""
PSD Phone Pivot Dialer — cold-calls the staged restaurant queue via Twilio.

Uses the LIVE TwiML endpoint (psdepot.com/twiml/outbound, served by twilio_voice.py
on :8099) and the ACTIVE Twilio creds (aocros/secrets/twilio.env), NOT the stale
vault token.

Usage:
  python3 phone_pivot_dialer.py --test                 # call Captain's number once
  python3 phone_pivot_dialer.py --limit 5              # dial first 5 queue entries
  python3 phone_pivot_dialer.py                        # dial the whole queue
  python3 phone_pivot_dialer.py --dry-run              # show plan, dial nothing
"""
import json
import os
import sys
import time
import argparse
import requests
from datetime import datetime, timezone
from pathlib import Path

BASE = "/root/.openclaw/workspace"
QUEUE = f"{BASE}/datadepot/data/phone_call_queue.json"
RESULTS = f"{BASE}/datadepot/data/pivot_call_log.json"
DB = f"{BASE}/data/depot_chaos/unified.db"

TWILIO_FROM = "+18557899606"
TWIML_URL = "https://psdepot.com/twiml/outbound"
OWNER_NUMBERS = ["+14155326834", "+14155719724"]  # Captain


def load_creds():
    creds = {}
    for line in open(f"{BASE}/aocros/secrets/twilio.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            creds[k] = v
    return creds


def load_queue():
    q = json.load(open(QUEUE))
    if not isinstance(q, list):
        return []
    # filter to dialable entries
    out = []
    for e in q:
        phone = (e.get("phone") or "").strip()
        if not phone:
            continue
        phone = "".join(ch for ch in phone if ch.isdigit())
        if len(phone) == 10:
            out.append({"name": e.get("name", ""), "phone": "+1" + phone,
                        "city": e.get("city", ""), "email": e.get("email", "")})
    return out


def log_result(entry):
    path = Path(RESULTS)
    data = []
    if path.exists():
        try:
            data = json.load(open(path))
        except Exception:
            data = []
    data.append(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, open(path, "w"), indent=2)


def dial(creds, to, name):
    """Place a call via Twilio REST API (requests, no twilio lib)."""
    sid = creds["TWILIO_ACCOUNT_SID"]
    token = creds["TWILIO_AUTH_TOKEN"]
    try:
        r = requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Calls.json",
            data={"To": to, "From": TWILIO_FROM, "Url": TWIML_URL},
            auth=(sid, token),
            timeout=30,
        )
        if r.status_code in (200, 201):
            j = r.json()
            return {"status": j.get("status", "queued"), "sid": j.get("sid")}
        else:
            return {"status": "error", "error": f"HTTP {r.status_code}: {r.text[:200]}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="test call to Captain")
    ap.add_argument("--limit", type=int, default=0, help="max calls (0 = all)")
    ap.add_argument("--delay", type=int, default=3, help="seconds between calls")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    creds = load_creds()

    if args.test:
        print("🧪 Test call to Captain:", OWNER_NUMBERS[0])
        if not args.dry_run:
            r = dial(creds, OWNER_NUMBERS[0], "Captain (test)")
            print("  ->", r)
        return

    queue = load_queue()
    print(f"📞 Queue: {len(queue)} dialable numbers")
    if args.limit:
        queue = queue[: args.limit]
        print(f"   (limited to {args.limit})")

    if args.dry_run:
        for e in queue[:10]:
            print(f"   [dry-run] {e['name'][:30]:30s} {e['phone']} ({e['city']})")
        return

    for i, e in enumerate(queue):
        now = datetime.now(timezone.utc).isoformat()
        r = dial(creds, e["phone"], e["name"])
        print(f"[{i+1}/{len(queue)}] {e['name'][:30]:30s} {e['phone']} -> {r['status']}")
        log_result({
            "name": e["name"], "phone": e["phone"], "city": e["city"],
            "sid": r.get("sid"), "status": r["status"],
            "error": r.get("error", ""), "dialed_at": now,
        })
        if r["status"] == "error" and "21212" in r.get("error", ""):
            print("   ⚠️ Toll-free verification needed — stopping.")
            break
        if i < len(queue) - 1:
            time.sleep(args.delay)


if __name__ == "__main__":
    main()
