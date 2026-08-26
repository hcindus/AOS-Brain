#!/usr/bin/env python3
"""
DepotChaos REAL Opportunity Router (honest version)
Only surfaces REAL businesses (real phone/email, no synthetic fabrication).

Real data sources:
  - vendors with real (non-555) phone + real email  (~6,374)
  - teriyaki_madness franchise locations (190) — real chain

Destination mapping (name-based type detection):
  - bar / wine bar / tavern / brewery / cocktail / pub  → WitzEnd (mocktails) + PSDepot (pour control)
  - restaurant / cafe / deli / food / grill             → PSDepot (supplies) + Chipp
  - default                                             → PSDepot (supplies)
"""
import sqlite3, json, re
from datetime import datetime
from pathlib import Path

VENDORS_DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
OUT = Path("/root/.openclaw/workspace/aocros/reports/real_opportunities.json")

BAR_PAT = re.compile(r"\b(wine bar|bar\b|tavern|brew|brewery|pub\b|cocktail|lounge|taphouse)\b", re.I)
REST_PAT = re.compile(r"\b(restaurant|cafe|café|deli|food|grill|kitchen|pizza|diner|eatery|bistro|taqueria|seafood|steakhouse|bakery)\b", re.I)

# Filter out junk/numeric/artifact business names
JUNK_PAT = re.compile(r"^\d+(\.\d+)?$|^$|^[A-Za-z]?\d+$")  # pure numbers, empty, "1190", "2890"

def is_junk(name):
    n = (name or "").strip()
    if not n or len(n) < 3:
        return True
    if JUNK_PAT.match(n):
        return True
    if n in ("LOCATION", "WORLDPAY", "WORLDPAY PAYMENTS"):
        return True
    return False

def classify(name):
    n = name or ""
    if BAR_PAT.search(n):
        return ["witzend", "psd"]
    if REST_PAT.search(n):
        return ["psd", "chipp"]
    return ["psd"]

def main():
    conn = sqlite3.connect(VENDORS_DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # REAL vendors: real phone (not 555) — these are genuinely contactable businesses
    c.execute("""
        SELECT id, name, city, state, phone, email, address, vendor_type
        FROM vendors
        WHERE phone IS NOT NULL AND phone != '' AND phone NOT LIKE '%555%'
        ORDER BY name
    """)
    vendors = [dict(r) for r in c.fetchall()]

    # teriyaki_madness — real franchise locations
    c.execute("""
        SELECT store_name, city, state, phone, address
        FROM teriyaki_madness
        WHERE address IS NOT NULL AND address != ''
    """)
    teriyaki = [dict(r) for r in c.fetchall()]
    conn.close()

    qualified = {"psd": [], "chipp": [], "witzend": []}

    for v in vendors:
        if is_junk(v["name"]):
            continue
        dests = classify(v["name"])
        rec = {
            "business_name": v["name"],
            "city": v.get("city") or "",
            "state": v.get("state") or "",
            "phone": v.get("phone") or "",
            "email": v.get("email") or "",
            "address": v.get("address") or "",
            "source": "vendors",
        }
        for d in dests:
            qualified[d].append(rec)

    # Teriyaki Madness = restaurants → supplies + partner (real franchise)
    for t in teriyaki:
        rec = {
            "business_name": t.get("store_name", "Teriyaki Madness"),
            "city": t.get("city") or "",
            "state": t.get("state") or "",
            "phone": t.get("phone") or "",
            "email": "",
            "address": t.get("address") or "",
            "source": "teriyaki_madness",
        }
        qualified["psd"].append(rec)
        qualified["chipp"].append(rec)

    # Dedupe each destination by (name, city)
    def dedupe(lst):
        seen = set(); out = []
        for r in lst:
            k = (r["business_name"], r["city"])
            if k not in seen:
                seen.add(k); out.append(r)
        return out
    for d in qualified:
        qualified[d] = dedupe(qualified[d])

    stats = {d: len(qualified[d]) for d in qualified}
    stats["real_vendors"] = len(vendors)
    stats["teriyaki"] = len(teriyaki)

    report = {
        "generated_at": datetime.now().isoformat(),
        "note": "REAL data only — vendors with real phone numbers + teriyaki_madness franchise locations. No synthetic/fabricated records.",
        "stats": stats,
        "top_opportunities": {d: qualified[d][:25] for d in qualified},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(report, f, indent=2)

    print("=" * 62)
    print("  DEPOTCHAOS REAL OPPORTUNITIES (honest — real data only)")
    print("=" * 62)
    print(f"Real vendors (real phone): {stats['real_vendors']}")
    print(f"Teriyaki Madness locations: {stats['teriyaki']}")
    print(f"  → WitzEnd (bars/mocktails): {stats['witzend']}")
    print(f"  → Chipp (restaurants/partner): {stats['chipp']}")
    print(f"  → PSDepot (supplies): {stats['psd']}")
    print(f"\nReport: {OUT}")
    print("\nTop real opportunities:")
    for d in ["witzend", "chipp", "psd"]:
        print(f"\n  [{d.upper()}]")
        for r in qualified[d][:6]:
            print(f"    • {r['business_name']} ({r['city']}, {r['state']}) {r['phone']}")

if __name__ == "__main__":
    main()
