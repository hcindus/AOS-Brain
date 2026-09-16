#!/usr/bin/env python3
"""Corrected reconciliation of Performance POS past-due accounts."""
import json, re, sqlite3

records = json.load(open("/root/.openclaw/workspace/data/ppos_pastdue_parsed.json"))

def norm(s):
    if not s:
        return ""
    s = s.upper()
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def tokens(s):
    return set(norm(s).split())

# Generic words that should NOT drive a match on their own
GENERIC = {"MARKET","TAVERN","BAR","KITCHEN","CAFE","CAFÉ","RESTAURANT","DELI",
           "GRILL","STEAKHOUSE","CORNER","HOUSE","GROCERY","DINER","PIZZA",
           "STORAGE","BREWPUB","SALOON","SELF","WAGON","OLD","THE","AND","E","CORP",
           "INC","LLC","CUISINE","INDIAN","PARILLA","TAQUERIA","VINTAGE","COUNTRY",
           "GABLES","ROADHOUSE","ITALIANA","RIVERVIEW","SALT","PEPPER","TIBURON",
           "STAR","MADNESS","TERIYAKI","BROTHERS","GRILL","THREE","GROUP","LA"}

def sig(s):
    """Meaningful tokens (drop generic)."""
    return {t for t in tokens(s) if t not in GENERIC and len(t) > 1}

# Load backfill clients
bf = json.load(open("/root/.openclaw/workspace/data/backfill_clients.json"))

# Load leads (exact-name candidates only, filter empties)
con = sqlite3.connect("/root/.openclaw/workspace/data/depot_chaos/unified.db")
con.row_factory = sqlite3.Row
leads = con.execute(
    "SELECT business_name, city, state, email, phone, id, status, is_customer "
    "FROM leads WHERE deleted=0 AND business_name IS NOT NULL AND TRIM(business_name) != ''"
).fetchall()
lead_by_norm = {}
for l in leads:
    lead_by_norm.setdefault(norm(l["business_name"]), []).append(l)

def match_backfill(name):
    n = norm(name)
    ns = sig(name)
    exact = bf_by_norm.get(n)
    if exact:
        return ("exact", exact[0])
    # signature overlap
    best = None
    best_score = 0
    for c in bf:
        cs = sig(c["vendor_name"])
        if not ns or not cs:
            continue
        inter = ns & cs
        union = ns | cs
        score = len(inter) / len(union) if union else 0
        if score > best_score and score >= 0.5:
            best_score = score
            best = c
    if best:
        return ("fuzzy", best)
    return None

bf_by_norm = {}
for c in bf:
    bf_by_norm.setdefault(norm(c["vendor_name"]), []).append(c)

print("=== RECONCILIATION (backfill-first) ===\n")
print(f"{'#':3} {'CUSTOMER':30} {'INV':9} {'TOTAL':>9}  {'CITY/REG':12} {'CONTACT (from backfill)':40}")
print("-"*120)

results = []
for i, r in enumerate(records, 1):
    m = match_backfill(r["name"])
    email = phone = ""
    source = ""
    if m:
        c = m[1]
        email = c.get("email", "") or ""
        phone = c.get("phone", "") or ""
        source = "BF:" + m[0]
        match_name = c["vendor_name"]
    else:
        # leads exact
        lmatches = lead_by_norm.get(norm(r["name"]), [])
        if lmatches:
            l = lmatches[0]
            email = l["email"] or ""
            phone = l["phone"] or ""
            source = "LEADS#%s" % l["id"]
            match_name = l["business_name"]
        else:
            source = "MISSING"
            match_name = ""
    contact = f"{phone} {email}".strip()
    results.append((r, source, match_name, email, phone))
    print(f"{i:3} {r['name'][:30]:30} {r['invoice'] or '':9} {r['total']:>9,.2f}  {r['region_city'][:12]:12} {contact[:40]}")

# totals by source
from collections import Counter
c = Counter(src for _, src, *_ in results)
print("\n=== SUMMARY ===")
print(f"Total accounts: {len(records)}")
print(f"Total outstanding: ${sum(r['total'] for r in records):,.2f}")
for src, cnt in c.items():
    amt = sum(r['total'] for r, s, *_ in results if s == src)
    print(f"  {src:12}: {cnt} accounts, ${amt:,.2f}")

print("\n=== MISSING (not in backfill, no exact leads match) ===")
for r, src, *_ in results:
    if src == "MISSING":
        print(f"  {r['name']:34} {r['invoice']:10} {r['region_city']:14} ${r['total']:,.2f}")

# save full results
out = []
for r, src, match_name, email, phone in results:
    out.append({**r, "match_source": src, "matched_name": match_name,
                "email": email, "phone": phone})
json.dump(out, open("/root/.openclaw/workspace/data/ppos_pastdue_reconciled.json", "w"), indent=2, ensure_ascii=False)
print(f"\nSaved reconciled results to data/ppos_pastdue_reconciled.json")
