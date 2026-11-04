#!/usr/bin/env python3
"""
Sync the LIVE DepotChaos table (datadepot_intelligence) from the source of truth
(ca_abc_licenses). Runs daily AFTER the scraper + ETL bridge.

Funnels REAL scraped data → the LIVE table only. NEVER touches the DEMO table
(datadepot_intelligence_demo), which stays synthetic for show/sell.
"""
import sqlite3, json
from datetime import datetime, timezone

DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
LIVE_TABLE = "datadepot_intelligence"      # ← the LIVE page (depotchaos_live/)
# DEMO table = datadepot_intelligence_demo (deliberately NOT touched here)

TYPE_NAMES = {"20":"Off-Sale Beer & Wine","21":"Off-Sale General","40":"On-Sale Beer",
              "41":"On-Sale Beer & Wine - Eating Place","42":"On-Sale Beer & Wine - Public Premises",
              "47":"On-Sale General - Restaurant","48":"On-Sale General - Bar/Tavern",
              "58":"Caterer's Permit","75":"Event Permit"}


def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Pull all real ABC licenses (the source of truth)
    rows = c.execute("""
        SELECT license_number, license_type, license_type_name, status, business_name,
               owner_name, address, city, state, zip, county, phone, issue_date, expiration_date
        FROM ca_abc_licenses
    """).fetchall()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    synced = 0
    for r in rows:
        ln, lt, ltn, status, bname, owner, addr, city, state, zip_, county, phone, issue, exp = r
        data = json.dumps({
            "license_type": lt, "license_type_name": ltn or TYPE_NAMES.get(lt, ""),
            "status": status, "owner_name": owner, "address": addr,
            "city": city, "state": state, "zip": zip_, "phone": phone or "",
            "issue_date": issue or "", "expiration_date": exp or "",
        })
        c.execute(f"""
            INSERT OR REPLACE INTO {LIVE_TABLE}
            (business_name, license_number, source, data, created_at, county, replacement_score,
             pos_system, owner_name, address, city, state, zip, phone, license_status, issue_date, expiration_date)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (bname or "", ln or "", "CA_ABC", data, now, county or "", 70, "", owner or "",
              addr or "", city or "", state or "", zip_ or "", phone or "", status or "", issue or "", exp or ""))
        synced += 1

    conn.commit()
    live_count = c.execute(f"SELECT COUNT(*) FROM {LIVE_TABLE}").fetchone()[0]
    demo_count = c.execute("SELECT COUNT(*) FROM datadepot_intelligence_demo").fetchone()[0]
    conn.close()

    print(f"✅ Synced {synced:,} records → {LIVE_TABLE} (LIVE, now {live_count:,} rows)")
    print(f"   DEMO table untouched: {demo_count:,} rows (synthetic, stays synthetic)")


if __name__ == "__main__":
    main()
