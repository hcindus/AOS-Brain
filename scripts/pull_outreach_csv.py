#!/usr/bin/env python3
"""
Pull the REAL (data_class='real') records into an outreach-ready CSV.
Merges vendors + leads, dedupes, sorts by contact completeness.
"""
import sqlite3, csv
from datetime import datetime

VENDORS_DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
UNIFIED_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
OUT = "/root/.openclaw/workspace/data/outreach_real_leads.csv"

def norm_phone(p):
    return "".join(ch for ch in (p or "") if ch.isdigit())

def main():
    records = {}

    # vendors (real)
    conn = sqlite3.connect(VENDORS_DB)
    conn.row_factory = sqlite3.Row
    for r in conn.execute("""
        SELECT name, phone, email, address, city, state, zip, vendor_type, source_file
        FROM vendors WHERE data_class='real'"""):
        name = (r["name"] or "").strip()
        if not name:
            continue
        key = (name.lower(), norm_phone(r["phone"]))
        rec = {
            "name": name, "phone": (r["phone"] or "").strip(),
            "email": (r["email"] or "").strip().lower(),
            "address": (r["address"] or "").strip(), "city": (r["city"] or "").strip(),
            "state": (r["state"] or "").strip(), "zip": (r["zip"] or "").strip(),
            "type": (r["vendor_type"] or "").strip(), "source": "vendors:" + (r["source_file"] or ""),
        }
        records[key] = rec
    conn.close()

    # leads (real)
    conn = sqlite3.connect(UNIFIED_DB)
    conn.row_factory = sqlite3.Row
    for r in conn.execute("""
        SELECT business_name, phone, email, address, city, state, zip, business_type, source_type
        FROM leads WHERE data_class='real' AND deleted=0"""):
        name = (r["business_name"] or "").strip()
        if not name:
            continue
        key = (name.lower(), norm_phone(r["phone"]))
        if key in records:
            # enrich existing with email if missing
            if not records[key]["email"] and r["email"]:
                records[key]["email"] = (r["email"] or "").strip().lower()
            continue
        records[key] = {
            "name": name, "phone": (r["phone"] or "").strip(),
            "email": (r["email"] or "").strip().lower(),
            "address": (r["address"] or "").strip(), "city": (r["city"] or "").strip(),
            "state": (r["state"] or "").strip(), "zip": (r["zip"] or "").strip(),
            "type": (r["business_type"] or "").strip(), "source": "leads:" + (r["source_type"] or ""),
        }
    conn.close()

    # sort by completeness: phone+email > phone > email > name-only
    def score(r):
        s = 0
        if r["phone"]: s += 3
        if r["email"]: s += 2
        if r["city"] or r["state"]: s += 1
        return s

    rows = sorted(records.values(), key=lambda r: (-score(r), r["name"].lower()))

    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name","phone","email","address","city","state","zip","type","source"])
        w.writeheader()
        w.writerows(rows)

    phone = sum(1 for r in rows if r["phone"])
    email = sum(1 for r in rows if r["email"])
    both = sum(1 for r in rows if r["phone"] and r["email"])
    print(f"✅ Outreach CSV: {len(rows)} real businesses → {OUT}")
    print(f"   with phone: {phone} | with email: {email} | phone+email: {both}")

if __name__ == "__main__":
    main()
