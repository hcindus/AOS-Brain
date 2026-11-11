#!/usr/bin/env python3
"""
Ingest a canvass CSV into DepotChaos vendors, with automatic cross-reference dedup
against existing customers (exact + substring name match).

Usage:
  python3 ingest_canvass.py <csv_path> --source mortimer-hwy4-680

CSV columns (Mortimer schema): business_name, address, city, county, state, zip,
phone, email, website, cuisine, status, tier, source.
"""
import csv, sqlite3, re, argparse
from datetime import datetime, timezone

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"


def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--source", required=True, help="e.g. mortimer-hwy4-680")
    args = ap.parse_args()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    # existing customers (anything already in the system)
    cur.execute("SELECT name FROM vendors WHERE status != 'new'")
    existing = {}
    for (name,) in cur.fetchall():
        n = norm(name)
        if n and n not in existing:
            existing[n] = name

    rows = list(csv.DictReader(open(args.csv_path)))
    inserted = dupes = skipped = 0

    for r in rows:
        name = (r.get('business_name') or '').strip()
        if not name:
            skipped += 1
            continue
        n = norm(name)

        is_dupe = False
        if n in existing:
            is_dupe = True
        else:
            for en in existing:
                if n and en and len(n) >= 5 and len(en) >= 5 and (n in en or en in n):
                    is_dupe = True
                    break

        status = 'duplicate' if is_dupe else 'new'
        note = ("dup-of-existing-customer; website=" if is_dupe else "website=") + \
               f"{r.get('website') or ''}; tier={r.get('tier') or ''}"

        cur.execute('''INSERT INTO vendors
            (name, phone, email, address, city, state, zip, territory, vendor_type,
             status, source_file, imported_at, notes, data_class)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (name, r.get('phone') or '', r.get('email') or '', r.get('address') or '',
             r.get('city') or '', r.get('state') or '', r.get('zip') or '', r.get('county') or '',
             r.get('cuisine') or 'Restaurant', status, args.source,
             datetime.now(timezone.utc).isoformat(), note, 'real'))

        if is_dupe:
            dupes += 1
        else:
            inserted += 1
            existing[n] = name  # also dedupe within the same CSV

    con.commit()
    con.close()
    print(f"CSV={len(rows)} INSERTED={inserted} DUPLICATES={dupes} SKIPPED={skipped}")


if __name__ == "__main__":
    main()
