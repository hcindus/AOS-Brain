#!/usr/bin/env python3
"""
DepotChaos Lead Qualification — Real Opportunities Router
Maps REAL CA ABC license data (74K records from actual ABC export) to 3 destinations:
  - Type 48 (Bar/Tavern)  → WitzEnd (mocktails) + PSDepot (pour control)
  - Type 47/41 (Restaurant) → PSDepot (supplies) + Chipp
  - Type 20/21 (Off-sale)   → PSDepot (supplies)
  - Type 58 (Caterer)       → PSDepot + Chipp

Honest: only REAL data. No fabrication. Flags data-quality gaps clearly.
"""
import sqlite3, json
from datetime import datetime
from pathlib import Path

DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
OUT = Path("/root/.openclaw/workspace/aocros/reports/qualified_opportunities.json")

# License type → destination mapping
TYPE_MAP = {
    "48": ["witzend", "psd"],   # Bar/Tavern → mocktails + pour control
    "47": ["psd", "chipp"],     # Restaurant → supplies + partner
    "41": ["psd", "chipp"],     # Eating place → supplies + partner
    "20": ["psd"],              # Off-sale beer/wine → supplies
    "21": ["psd"],              # Off-sale general → supplies
    "58": ["psd", "chipp"],     # Caterer → supplies + partner
}

# Opportunity scoring: full contact info = higher value
def score(rec):
    s = 0
    if rec.get("address") and rec["address"].strip(): s += 1
    if rec.get("city") and rec["city"].strip(): s += 1
    if rec.get("zip") and rec["zip"].strip(): s += 1
    if rec.get("owner_name") and rec["owner_name"].strip(): s += 1
    if rec.get("phone") and rec["phone"].strip(): s += 1
    return s

def main():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Pull ACTIVE licenses only (real, current businesses)
    c.execute("""
        SELECT license_number, license_type, license_type_name, status,
               business_name, owner_name, address, city, county, zip, phone
        FROM ca_abc_licenses
        WHERE status = 'ACTIVE'
          AND business_name IS NOT NULL AND business_name != ''
        ORDER BY license_type, city
    """)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    qualified = {"psd": [], "chipp": [], "witzend": []}
    stats = {"psd": 0, "chipp": 0, "witzend": 0, "total_active": len(rows)}

    for r in rows:
        lt = r.get("license_type", "")
        dests = TYPE_MAP.get(lt, ["psd"])
        opp_score = score(r)
        for d in dests:
            qualified[d].append({
                "business_name": r["business_name"],
                "license_type": lt,
                "license_type_name": r.get("license_type_name", ""),
                "city": r.get("city", ""),
                "county": r.get("county", ""),
                "owner_name": r.get("owner_name", ""),
                "phone": r.get("phone", ""),
                "address": r.get("address", ""),
                "zip": r.get("zip", ""),
                "opportunity_score": opp_score,  # 0-5, higher = more complete/ready
                "license_number": r["license_number"],
            })
            stats[d] += 1

    # Sort each destination's leads by opportunity score (best first)
    for d in qualified:
        qualified[d].sort(key=lambda x: -x["opportunity_score"])

    # Build report
    report = {
        "generated_at": datetime.now().isoformat(),
        "source": "ca_abc_licenses (REAL ABC export, ACTIVE only)",
        "stats": stats,
        "top_opportunities": {
            d: qualified[d][:20] for d in qualified
        },
        "total_qualified": {d: len(qualified[d]) for d in qualified},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(report, f, indent=2)

    # Print summary for Captain
    print("=" * 60)
    print("  DEPOTCHAOS REAL OPPORTUNITY QUALIFICATION")
    print("=" * 60)
    print(f"Active ABC licenses: {stats['total_active']}")
    print(f"  → PSDepot (supplies):   {stats['psd']}")
    print(f"  → Chipp (partner):      {stats['chipp']}")
    print(f"  → WitzEnd (mocktails):  {stats['witzend']}")
    print(f"\nReport written to: {OUT}")
    print("\nTop 5 by destination (highest opportunity score):")
    for d in ["witzend", "chipp", "psd"]:
        print(f"\n  [{d.upper()}]")
        for lead in qualified[d][:5]:
            print(f"    • {lead['business_name']} ({lead['city']}) — {lead['license_type_name']} — score {lead['opportunity_score']}/5")

if __name__ == "__main__":
    main()
