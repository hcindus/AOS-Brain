#!/usr/bin/env python3
"""DepotChaos dedup + fabricated-data cleanup (soft-delete via deleted=1, reversible)."""
import sqlite3

DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def score(r):
    s = 0
    if r["email"] and r["email"].strip(): s += 4
    if r["phone"] and r["phone"].strip(): s += 2
    if r["notes"] or r["enrichment_data"]: s += 1
    if r["address"]: s += 1
    return s

# ---- 1. Exact (business_name + city + state) duplicates ----
dup_groups = cur.execute("""
    SELECT business_name, city, state, COUNT(*) n
    FROM leads WHERE deleted=0 AND business_name != ''
    GROUP BY lower(business_name), lower(city), lower(state)
    HAVING n > 1
""").fetchall()

exact_removed = 0
for g in dup_groups:
    rows = cur.execute("""
        SELECT * FROM leads WHERE deleted=0
        AND lower(business_name)=lower(?) AND lower(city)=lower(?) AND lower(state)=lower(?)
        ORDER BY id
    """, (g["business_name"], g["city"], g["state"])).fetchall()
    best = max(rows, key=score)
    for r in rows:
        if r["id"] != best["id"]:
            cur.execute("UPDATE leads SET deleted=1 WHERE id=?", (r["id"],))
            exact_removed += 1

# ---- 2. Fully-fabricated sources (NORTHEAST_*, MIDWEST_*) ----
fab = cur.execute("""
    SELECT COUNT(*) n FROM leads WHERE deleted=0 AND (source LIKE 'NORTHEAST%' OR source LIKE 'MIDWEST%')
""").fetchone()["n"]
cur.execute("""
    UPDATE leads SET deleted=1 WHERE deleted=0 AND (source LIKE 'NORTHEAST%' OR source LIKE 'MIDWEST%')
""")

conn.commit()

total_after = cur.execute("SELECT COUNT(*) FROM leads WHERE deleted=0").fetchone()[0]
conn.close()

print(f"Exact (name+city+state) dupes removed: {exact_removed} (from {len(dup_groups)} groups)")
print(f"Fabricated NORTHEAST/MIDWEST records soft-deleted: {fab}")
print(f"Total soft-deleted this run: {exact_removed + fab}")
print(f"Leads remaining (deleted=0): {total_after}")
