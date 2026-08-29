#!/usr/bin/env python3
"""Inspect DepotChaos leads table schema + existing YellowPages rows."""
import sqlite3, os

DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("PRAGMA table_info(leads)")
cols = cur.fetchall()
print("=== leads columns ===")
for c in cols:
    print(c[1], "|", c[2], "| nullable=", "YES" if c[3]==0 else "NO", "| default=", c[4])

# any existing source=YellowPages?
for src in ["YellowPages", "yp_directory", "Santa_Rosa_Yelp"]:
    try:
        n = cur.execute("SELECT COUNT(*) FROM leads WHERE source = ?", (src,)).fetchone()[0]
        print(f"source={src}: {n}")
    except Exception as e:
        print(f"source={src}: ERR {e}")

# dedupe check query works
try:
    n = cur.execute("SELECT COUNT(*) FROM leads WHERE business_name = ? AND city=? AND state=?", ("Cucina Paradiso","Petaluma","CA")).fetchone()[0]
    print("Cucina Paradiso/Petaluma/CA existing count:", n)
except Exception as e:
    print("dedupe query ERR:", e)

conn.close()
print("ok")
