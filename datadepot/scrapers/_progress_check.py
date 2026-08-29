#!/usr/bin/env python3
import sqlite3
conn = sqlite3.connect("/root/.openclaw/workspace/data/depot_chaos/unified.db")
cur = conn.cursor()
n = cur.execute("SELECT COUNT(*) FROM leads WHERE source='YellowPages'").fetchone()[0]
print("YellowPages leads total:", n)
rows = cur.execute("SELECT city, COUNT(*) FROM leads WHERE source='YellowPages' GROUP BY city ORDER BY city").fetchall()
for r in rows:
    print(" ", r)
conn.close()
