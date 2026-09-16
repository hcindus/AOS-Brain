#!/usr/bin/env python3
"""Add missing past-due accounts to the Performance POS client list."""
import json, shutil, csv, datetime, re

BF = "/root/.openclaw/workspace/data/backfill_clients.json"
BF_CSV = "/root/.openclaw/workspace/data/backfill_clients.csv"
RECON = "/root/.openclaw/workspace/data/ppos_pastdue_reconciled.json"

# O/S city inference from name
OS_CITY = {
    "TERIYAKI MADNESS HELENA": ("Helena", "MT"),
    "TERIYAKI MADNESS BILLINGS": ("Billings", "MT"),
    "THREE BROTHERS GRILL POTTSTOWN": ("Pottstown", "PA"),
}

ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
shutil.copy(BF, BF + f".bak_{ts}")
shutil.copy(BF_CSV, BF_CSV + f".bak_{ts}")

clients = json.load(open(BF))
recon = json.load(open(RECON))

# existing normalized names to avoid dupes
def norm(s):
    return re.sub(r"[^A-Z0-9 ]", " ", (s or "").upper())
    # collapse
def norm2(s):
    return re.sub(r"\s+", " ", norm(s)).strip()

existing = {norm2(c["vendor_name"]) for c in clients}

added = []
for r in recon:
    if r.get("match_source") != "MISSING":
        continue
    n = norm2(r["name"])
    if n in existing:
        continue  # already present under some name
    city = r.get("region_city", "")
    state = "CA"
    if r["region"] == "O/S":
        city, state = OS_CITY.get(r["name"].upper(), ("Out of State", ""))
    # title-case client name
    client_name = r["name"].title()
    entry = {
        "vendor_id": None,
        "vendor_name": r["name"].upper(),
        "client_name": client_name,
        "email": "",
        "phone": "",
        "city": city,
        "state": state,
        "region_code": r["region"],
        "invoice": r.get("invoice", ""),
        "amount_due": r.get("total", 0.0),
        "source": "ppos_pastdue_2026",
    }
    clients.append(entry)
    added.append(entry)
    existing.add(n)

json.dump(clients, open(BF, "w"), indent=2, ensure_ascii=False)

# regenerate CSV with union of keys
keys = ["vendor_id", "vendor_name", "client_name", "email", "phone",
        "city", "state", "region_code", "invoice", "amount_due", "source"]
with open(BF_CSV, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys)
    w.writeheader()
    for c in clients:
        w.writerow({k: c.get(k, "") for k in keys})

print(f"Backed up to .bak_{ts}")
print(f"Added {len(added)} accounts to client list (now {len(clients)} total)")
print(f"\n--- Added ---")
for a in added:
    print(f"  {a['client_name']:32} {a['city']:16} ${a['amount_due']:>9,.2f}  inv={a['invoice']}")
