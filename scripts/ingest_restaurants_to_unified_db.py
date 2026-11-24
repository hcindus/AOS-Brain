#!/usr/bin/env python3
"""
Fold restaurant corridor reports into the DepotChaos LIVE unified DB (`leads` table).

Sources:
  1. Hwy 4/680  -> /tmp/mortimer_canvass/restaurants_hwy4_680_depotchaos.csv (84 rows)
  2. Highway 116 -> data/email_inbox/highway116_restaurants.md (~260 spots)

Target: data/depot_chaos/unified.db -> `leads` (UNIQUE(business_name, city, state))

Run: python3 ingest_restaurants_to_unified_db.py [--dry-run]
"""
import csv
import json
import re
import sys
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
CSV = "/tmp/mortimer_canvass/restaurants_hwy4_680_depotchaos.csv"
MD = "/root/.openclaw/workspace/data/email_inbox/highway116_restaurants.md"

PHONE_RE = re.compile(r"\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})")
WEB_RE = re.compile(r"[\w-]+\.(com|net|org|co|io|us|biz|info)(?:/\S*)?", re.I)

# Highway 116 town -> county
TOWN_COUNTY = {
    "Jenner": "Sonoma", "Guerneville": "Sonoma", "Forestville": "Sonoma",
    "Graton": "Sonoma", "Sebastopol": "Sonoma", "Cotati": "Sonoma",
    "Rohnert Park": "Sonoma", "Petaluma": "Sonoma",
}
TOWN_ALIASES = {
    "jenner": "Jenner", "guerneville": "Guerneville", "forestville": "Forestville",
    "graton": "Graton", "sebastopol": "Sebastopol", "cotati": "Cotati",
    "rohnert": "Rohnert Park", "petaluma": "Petaluma",
}


def norm_phone(s):
    m = PHONE_RE.search(s or "")
    return "".join(m.groups()) if m else ""


def norm_website(s):
    if not s:
        return ""
    s = s.strip()
    if not s.startswith("http"):
        s = "http://" + s
    return s


def parse_hwy4_680():
    rows = []
    with open(CSV) as f:
        for r in csv.DictReader(f):
            name = (r.get("business_name") or "").strip()
            if not name:
                continue
            rows.append({
                "business_name": name,
                "address": (r.get("address") or "").strip(),
                "city": (r.get("city") or "").strip(),
                "county": (r.get("county") or "").strip(),
                "state": "CA",
                "zip": (r.get("zip") or "").strip(),
                "phone": norm_phone(r.get("phone") or ""),
                "email": (r.get("email") or "").strip(),
                "website": norm_website(r.get("website") or ""),
                "business_type": (r.get("cuisine") or "").strip() or "Restaurant",
                "tier": (r.get("tier") or "Tier 3").strip(),
                "source": "mortimer-hwy4-680",
            })
    return rows


def town_from_line(line):
    low = line.lower()
    for slug, city in TOWN_ALIASES.items():
        if slug in low:
            return city
    return None


def parse_hwy116():
    lines = Path(MD).read_text().splitlines()
    city = None
    sub_city = None
    # track current table columns
    cols = None
    seen = set()
    rows = []

    def add(name, phone="", website="", address="", cuisine=""):
        name = name.strip()
        if not name or len(name) < 2:
            return
        c = sub_city or city or ""
        key = (name.lower(), c)
        if key in seen:
            return
        seen.add(key)
        rows.append({
            "business_name": name,
            "address": address.strip(),
            "city": c,
            "county": TOWN_COUNTY.get(c, "Sonoma"),
            "state": "CA",
            "zip": "",
            "phone": norm_phone(phone),
            "email": "",
            "website": norm_website(website),
            "business_type": cuisine.strip() or "Restaurant",
            "tier": "Tier 3",
            "source": "highway116",
        })

    for raw in lines:
        line = raw.strip()

        # town header
        if line.startswith("## "):
            city = town_from_line(line)
            sub_city = None
            cols = None
            continue

        # subsection header
        if line.startswith("### "):
            t = town_from_line(line)
            sub_city = t if t else None
            cols = None
            continue

        # table header row (defines columns)
        if line.startswith("|") and "---" not in line and line.endswith("|"):
            hdr = [c.strip().lower() for c in line.strip("|").split("|")]
            if hdr and hdr[0] in ("name", "business_name"):
                cols = hdr
                continue

        # table data row
        if line.startswith("|") and line.endswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not cells or not cells[0]:
                continue
            if cols:
                row = dict(zip(cols, cells))
                name = row.get("name", "")
                phone = row.get("phone", "")
                website = row.get("website", "")
                address = row.get("address", "")
                cuisine = row.get("cuisine", "")
                add(name, phone, website, address, cuisine)
            else:
                # fallback: first cell name, scan rest for phone/website
                name = cells[0]
                phone = website = ""
                for c in cells[1:]:
                    if not phone and PHONE_RE.search(c):
                        phone = c
                    elif not website and WEB_RE.search(c):
                        website = c
                add(name, phone, website)
            continue

        # bullet line
        if line.startswith("- "):
            mname = re.search(r"\*\*(.+?)\*\*", line)
            if not mname:
                continue
            name = mname.group(1).strip()
            phone = ""
            website = ""
            mph = PHONE_RE.search(line)
            if mph:
                phone = line[mph.start():mph.end()]
            mweb = WEB_RE.search(line)
            if mweb:
                website = mweb.group(0)
            add(name, phone, website)

    return rows


def insert_leads(rows):
    now = datetime.now(timezone.utc).isoformat()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    added = 0
    skipped = 0
    for r in rows:
        try:
            cur.execute("""
                INSERT OR IGNORE INTO leads
                (business_name, address, city, state, zip, phone, email, website,
                 business_type, county, tier, source, status, created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                r["business_name"], r["address"], r["city"], r["state"], r["zip"],
                r["phone"], r["email"], r["website"], r["business_type"], r["county"],
                r["tier"], r["source"], "new", now,
            ))
            if cur.rowcount > 0:
                added += 1
            else:
                skipped += 1
        except Exception as e:
            print("  ERROR:", r["business_name"], e)
    con.commit()
    con.close()
    return added, skipped


def main():
    dry = "--dry-run" in sys.argv
    hw4 = parse_hwy4_680()
    hw116 = parse_hwy116()
    print(f"Hwy 4/680 rows: {len(hw4)}")
    print(f"Highway 116 rows: {len(hw116)}")
    print(f"  hw116 cities: {dict(Counter(r['city'] for r in hw116))}")

    all_rows = hw4 + hw116
    print(f"total to attempt: {len(all_rows)}")

    if dry:
        # show dedup preview
        con = sqlite3.connect(DB)
        cur = con.cursor()
        new = 0
        for r in all_rows:
            cur.execute("SELECT 1 FROM leads WHERE business_name=? AND city=? AND state=?",
                        (r["business_name"], r["city"], r["state"]))
            if cur.fetchone() is None:
                new += 1
        con.close()
        print(f"would add (net new): {new}, dup-skipped: {len(all_rows)-new}")
        return

    added, skipped = insert_leads(all_rows)
    print(f"INSERTED: {added}, skipped(dup): {skipped}")


if __name__ == "__main__":
    main()
