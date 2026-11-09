#!/usr/bin/env python3
"""
Load paid customers + Tomatina GMs into the LIVE DepotChaos DB.

Target: DepotChaos/depot_chaos.db -> vendors table
  data_class = 'real', vendor_type = 'customer'
Upsert by email (lowercased). Source provenance tracked in source_file.
"""
import json, sqlite3

FREQ = "/root/.openclaw/workspace/datadepot/data/reorder_frequency.json"
LIVE_DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
SOURCE = "invoices-export-20261109"

SKIP_EMAILS = {"info@psdepot.com", "antonio.hudnall@gmail.com", "miles@myl0nr0s.cloud"}

freq = json.load(open(FREQ))
conn = sqlite3.connect(LIVE_DB)
c = conn.cursor()

cols = [r[1] for r in c.execute("PRAGMA table_info(vendors)").fetchall()]

def upsert(name, email, phone):
    email = (email or "").strip().lower()
    if not email or "@" not in email or email in SKIP_EMAILS:
        return False
    c.execute("SELECT id FROM vendors WHERE lower(email)=? AND email!=''", (email,))
    row = c.fetchone()
    if row:
        c.execute("UPDATE vendors SET name=?, phone=?, vendor_type='customer', "
                  "data_class='real', status='active', source_file=? WHERE id=?",
                  (name, phone, SOURCE, row[0]))
    else:
        c.execute("INSERT INTO vendors (name,email,phone,vendor_type,data_class,status,source_file) "
                  "VALUES (?,?,?,'customer','real','active',?)",
                  (name, email, phone, SOURCE))
    return True

loaded = 0
updated = 0
inserted = 0
for x in freq:
    email = (x.get("email") or "").strip().lower()
    name = x.get("name") or ""
    phone = x.get("phone") or ""
    if not email or "@" not in email or email in SKIP_EMAILS:
        continue
    c.execute("SELECT id FROM vendors WHERE lower(email)=? AND email!=''", (email,))
    row = c.fetchone()
    if row:
        c.execute("UPDATE vendors SET name=?, phone=?, vendor_type='customer', "
                  "data_class='real', status='active', source_file=? WHERE id=?",
                  (name, phone, SOURCE, row[0]))
        updated += 1
    else:
        c.execute("INSERT INTO vendors (name,email,phone,vendor_type,data_class,status,source_file) "
                  "VALUES (?,?,?,'customer','real','active',?)",
                  (name, email, phone, SOURCE))
        inserted += 1
    loaded += 1

conn.commit()

# report
tot_real = c.execute("SELECT COUNT(*) FROM vendors WHERE data_class='real'").fetchone()[0]
tot_cust = c.execute("SELECT COUNT(*) FROM vendors WHERE vendor_type='customer'").fetchone()[0]
conn.close()

print(f"LOADED={loaded} (inserted={inserted}, updated={updated})")
print(f"vendors.data_class='real' total={tot_real}")
print(f"vendors.vendor_type='customer' total={tot_cust}")
