#!/usr/bin/env python3
"""Sync Performance POS past-due accounts into DepotChaos (unified.db leads table)."""
import json, sqlite3, re, datetime

DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
GEO = "/root/.openclaw/workspace/data/ppos_pastdue_geocoded.json"

def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^A-Z0-9 ]", " ", (s or "").upper())).strip()

STATE = {"CA": "CA", "MT": "MT", "PA": "PA"}

records = json.load(open(GEO))
con = sqlite3.connect(DB)
c = con.cursor()

# existing leads index
rows = c.execute(
    "SELECT id, business_name, city, state FROM leads WHERE deleted=0 AND business_name IS NOT NULL AND TRIM(business_name)!=''"
).fetchall()
idx = {}
for lid, bn, city, st in rows:
    idx.setdefault(norm(bn), []).append((lid, city, st))

today = "2026-09-17"
updated = 0
inserted = 0
skipped = set()

for r in records:
    n = norm(r["name"])
    key = n
    # dedup within this batch (e.g., two Mi Casa invoices)
    city = r.get("region_city") or (r.get("geocode") or {}).get("city") or ""
    state = "CA"
    if r.get("region") == "O/S":
        state = {"TERIYAKI MADNESS HELENA": "MT",
                 "TERIYAKI MADNESS BILLINGS": "MT",
                 "THREE BROTHERS GRILL POTTSTOWN": "PA"}.get(r["name"].upper(), "CA")
    geo = r.get("geocode") or {}
    address = geo.get("street") or ""
    if address and geo.get("housenumber"):
        address = f"{geo['housenumber']} {address}"
    zipcode = geo.get("postcode") or ""
    phone = r.get("phone") or ""
    email = r.get("email") or ""
    amount = r.get("total") or r.get("amount_due") or 0
    invoice = r.get("invoice") or ""
    status = "contacted" if r.get("status") == "contacted" else "new"
    notes = f"Past due ${amount:,.2f} (inv {invoice})" if amount else ""

    existing = idx.get(n)
    if existing:
        # update the first matching lead
        lid = existing[0][0]
        c.execute("""UPDATE leads SET
            is_customer=1, source_type=COALESCE(source_type,'ppos_pastdue'),
            data_class='ppos_pastdue', status=?, notes=?, assigned_agent='Miles',
            city=COALESCE(NULLIF(city,''), ?), state=?,
            phone=COALESCE(NULLIF(phone,''), ?), email=COALESCE(NULLIF(email,''), ?)
            WHERE id=?""", (status, notes, city, state, phone, email, lid))
        updated += 1
    else:
        try:
            c.execute("""INSERT INTO leads
                (business_name, city, state, zip, phone, email, address, status,
                 is_customer, source_type, data_class, notes, assigned_agent, created_at, last_contact)
                VALUES (?,?,?,?,?,?,?,?,1,'ppos_pastdue','ppos_pastdue',?,'Miles',?,?)""",
                (r["name"], city, state, zipcode, phone, email, address, status, notes, today, today))
            inserted += 1
        except sqlite3.IntegrityError as e:
            # likely UNIQUE(business_name, city, state) collision — fall back to update
            c.execute("""UPDATE leads SET is_customer=1, data_class='ppos_pastdue',
                status=?, notes=?, assigned_agent='Miles' WHERE business_name=?""",
                (status, notes, r["name"]))
            updated += 1

con.commit()
print(f"Synced to DepotChaos: {inserted} inserted, {updated} updated")
print(f"Total leads now: {c.execute('SELECT COUNT(*) FROM leads').fetchone()[0]}")
print(f"Customers (is_customer=1): {c.execute('SELECT COUNT(*) FROM leads WHERE is_customer=1').fetchone()[0]}")
