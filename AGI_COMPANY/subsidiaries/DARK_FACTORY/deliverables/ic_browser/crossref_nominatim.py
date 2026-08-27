#!/usr/bin/env python3
"""
Cross-reference every address through Nominatim vs stored business name.
Flags mismatches (our data stale/wrong) — honest verification at scale.

Rate-limited (Nominatim 1 req/sec), resumable (skips already-processed IDs),
writes results to a SQLite table + progress log.

Usage:
  python3 crossref_nominatim.py --limit 20    # sample
  python3 crossref_nominatim.py               # full run (resumable)
"""
import sqlite3, json, time, sys, os
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sources import nominatim

VENDORS_DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
RESULT_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def ensure_table():
    conn = sqlite3.connect(RESULT_DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS address_crossref (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        src_table TEXT, src_id INTEGER,
        stored_name TEXT, addr TEXT,
        nominatim_name TEXT, nominatim_category TEXT,
        match TEXT,           -- 'match' | 'mismatch' | 'no_business' | 'error'
        checked_at TIMESTAMP
    )""")
    conn.commit(); conn.close()

def load_addresses(limit=None):
    """Real addresses with a stored business name, ordered for resumability."""
    conn = sqlite3.connect(VENDORS_DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # vendors with real phone + address (the verified subset)
    q = """SELECT id, name, address FROM vendors
           WHERE phone IS NOT NULL AND phone != '' AND phone NOT LIKE '%555%'
             AND address IS NOT NULL AND address != '' AND address != ','
           ORDER BY id"""
    rows = [dict(r) for r in c.execute(q).fetchall()]
    # teriyaki_madness (real franchise addresses)
    trows = [dict(r) for r in c.execute("SELECT id, store_name AS name, address FROM teriyaki_madness WHERE address != ''").fetchall()]
    conn.close()
    # tag source table
    out = [("vendors", r) for r in rows] + [("teriyaki", r) for r in trows]
    if limit:
        out = out[:limit]
    return out

def already_done(src_table, src_id):
    conn = sqlite3.connect(RESULT_DB)
    c = conn.cursor()
    c.execute("SELECT 1 FROM address_crossref WHERE src_table=? AND src_id=?", (src_table, src_id))
    r = c.fetchone()
    conn.close()
    return r is not None

def record(src_table, src_id, stored_name, addr, nm_name, nm_cat, match):
    conn = sqlite3.connect(RESULT_DB)
    c = conn.cursor()
    c.execute("""INSERT INTO address_crossref
        (src_table, src_id, stored_name, addr, nominatim_name, nominatim_category, match, checked_at)
        VALUES (?,?,?,?,?,?,?,?)""",
        (src_table, src_id, stored_name, addr, nm_name, nm_cat, match, datetime.now(timezone.utc).isoformat()))
    conn.commit(); conn.close()

def compare(stored, nom):
    """Compare stored name vs nominatim name → match/mismatch/no_business."""
    if not nom:
        return "no_business"
    # normalize: lowercase, strip punctuation, compare token overlap
    def norm(s):
        return set(c.lower() for c in s.replace("'","").replace("&","and").split() if c.isalnum())
    s, n = norm(stored), norm(nom)
    if not s or not n:
        return "no_business"
    if s & n:  # any shared significant token
        return "match"
    return "mismatch"

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    ensure_table()
    items = load_addresses(args.limit)
    print(f"Addresses to cross-reference: {len(items)}")

    stats = {"match": 0, "mismatch": 0, "no_business": 0, "error": 0, "skipped": 0}
    t0 = time.time()
    for i, (src_table, r) in enumerate(items):
        src_id = r["id"]
        stored = r["name"] or ""
        addr = r["address"] or ""
        if already_done(src_table, src_id):
            stats["skipped"] += 1
            continue
        try:
            res = nominatim.lookup_by_address(addr)
            nm_name = res.get("business_name", "") if res else ""
            nm_cat = res.get("category", "") if res else ""
            m = compare(stored, nm_name)
        except Exception as e:
            m, nm_name, nm_cat = "error", "", str(e)[:60]
        record(src_table, src_id, stored, addr, nm_name, nm_cat, m)
        stats[m] = stats.get(m, 0) + 1
        # progress every 25
        if (i + 1) % 25 == 0:
            el = time.time() - t0
            rate = (i + 1) / el
            eta = (len(items) - i - 1) / rate
            print(f"  [{i+1}/{len(items)}] match={stats['match']} mismatch={stats['mismatch']} "
                  f"no_biz={stats['no_business']} err={stats['error']} | ETA {eta/60:.0f}m")
        time.sleep(1.05)  # Nominatim 1 req/sec

    print(f"\nDone. {stats}")

if __name__ == "__main__":
    main()
