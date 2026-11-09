#!/usr/bin/env python3
"""
Load paid customers + Tomatina GMs into DepotChaos (psd_customers / psd_customer_sales).

Reads reorder_frequency.json (clean, deduped, incl. 8 Tomatina GMs) and upserts
each identity into psd_customers by email. Also loads per-invoice sales history
into psd_customer_sales (year/month/amount). Skips synthetic "Sample"/"20 *" rows.
"""
import json, csv, sqlite3
from datetime import datetime

FREQ = "/root/.openclaw/workspace/datadepot/data/reorder_frequency.json"
CSV = "/root/.openclaw/media/inbound/invoices-export-20261109T2014---63cf980b-e227-4a3a-97ab-294293696cb7.csv"
DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

SKIP_EMAILS = {"info@psdepot.com", "antonio.hudnall@gmail.com", "miles@myl0nr0s.cloud"}
ALIASES = {
    "terrychico@sbcglobal.net": "travis_hauffman",
    "coldpop.billing@gmail.com": "travis_hauffman",
    "betsy@itsitaliarestaurant.com": "betsy_delfiero",
    "delfierro@coastside.net": "betsy_delfiero",
    "accountspayable@150pelican.com": "pelican_150",
}

def tier(total):
    if total >= 3000:
        return "gold"
    if total >= 800:
        return "silver"
    return "bronze"

def category(name):
    n = (name or "").lower()
    if any(k in n for k in ("market", "grocery", "mart", "supermercado")):
        return "market"
    if any(k in n for k in ("inn", "hotel")):
        return "lodging"
    if any(k in n for k in ("bar", "wine", "tavern", "pub")):
        return "bar"
    if any(k in n for k in ("cafe", "coffee")):
        return "coffee shop"
    return "restaurant"

freq = json.load(open(FREQ))

conn = sqlite3.connect(DB)
c = conn.cursor()

# ensure email column exists
cols = [r[1] for r in c.execute("PRAGMA table_info(psd_customers)").fetchall()]
for col in ("email", "phone", "category", "tier"):
    if col not in cols:
        c.execute(f"ALTER TABLE psd_customers ADD COLUMN {col} TEXT")
        conn.commit()

email_to_id = {}

def upsert_customer(name, email, phone, total, cat):
    if email in email_to_id:
        return email_to_id[email]
    # find existing by email
    c.execute("SELECT id FROM psd_customers WHERE email=? AND email!=''", (email,))
    row = c.fetchone()
    if row:
        cid = row[0]
        c.execute("UPDATE psd_customers SET name=?, phone=?, category=?, tier=? WHERE id=?",
                  (name, phone, cat, tier(total), cid))
    else:
        c.execute("INSERT INTO psd_customers (name,email,phone,category,tier,status) "
                  "VALUES (?,?,?,?,?,'active')", (name, email, phone, cat, tier(total)))
        cid = c.lastrowid
    email_to_id[email] = cid
    return cid

loaded = 0
for x in freq:
    email = (x.get("email") or "").strip().lower()
    name = x.get("name") or ""
    phone = x.get("phone") or ""
    total = x.get("total_spent") or 0.0
    if not email or "@" not in email or email in SKIP_EMAILS:
        continue
    upsert_customer(name, email, phone, total, category(name))
    loaded += 1

conn.commit()
print(f"CUSTOMERS_LOADED={loaded}")

# load sales history (per invoice -> year/month/amount)
# clear prior synthetic sales to avoid mixing
c.execute("DELETE FROM psd_customer_sales")
sales = 0
with open(CSV, newline="", encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        email = (r.get("Customer Email") or "").strip().lower()
        if not email or "@" not in email or email in SKIP_EMAILS:
            continue
        cid = email_to_id.get(ALIASES.get(email, email))
        if not cid:
            continue
        date_s = (r.get("Invoice Date") or "").strip()
        amt_s = (r.get("Amount Paid") or "").strip().replace("$", "").replace(",", "")
        try:
            d = datetime.strptime(date_s, "%Y-%m-%d")
            amt = float(amt_s) if amt_s else 0.0
        except Exception:
            continue
        c.execute("INSERT INTO psd_customer_sales (customer_id,year,month,amount) "
                  "VALUES (?,?,?,?)", (cid, d.year, d.strftime("%B"), amt))
        sales += 1

conn.commit()
conn.close()
print(f"SALES_ROWS_LOADED={sales}")
