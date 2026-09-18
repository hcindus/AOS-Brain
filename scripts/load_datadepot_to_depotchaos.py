#!/usr/bin/env python3
"""
ETL Bridge — load DataDepot ABC export (30-col CSV) into DepotChaos unified.db.

Maps the CA ABC DailyExport format → ca_abc_licenses table, replacing the stale
synthetic data with the real live ABC export.

Non-destructive: backs up the existing table first (to ca_abc_licenses_backup).
"""
import sqlite3, csv, sys
from datetime import datetime, timezone

CSV_PATH = "/root/.openclaw/workspace/datadepot/data/ca_abc_licenses_raw.csv"
DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

# License type code → name (CA ABC standard)
TYPE_NAMES = {
    "20": "Off-Sale Beer & Wine",
    "21": "Off-Sale General",
    "40": "On-Sale Beer (Restaurant)",
    "41": "On-Sale Beer & Wine - Eating Place",
    "42": "On-Sale Beer & Wine - Public Premises",
    "47": "On-Sale General - Restaurant",
    "48": "On-Sale General - Bar/Tavern",
    "58": "Caterer's Permit",
    "75": "Event Permit",
}

# 30-col ABC DailyExport → (column index, field)
# 0-based indices from the CSV
COLMAP = {
    "license_type": 0,       # "20"
    "license_number": 1,     # "00232733"
    "status": 3,             # "ACTIVE"
    "business_name": 12,     # "TRI COUNTY PRODUCE CO LTD"
    "address": 13,           # "335 S MILPAS ST"
    "city": 15,              # "SANTA BARBARA"
    "state": 16,             # "CA"
    "zip": 17,               # "93103-3657"
    "dba": 18,               # "TRI COUNTY PRODUCE" (stored as owner_name fallback)
    "county": 24,            # "SANTA BARBARA"
}

def get(row, field):
    idx = COLMAP[field]
    return (row[idx] if idx < len(row) else "").strip()

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Back up existing table
    c.execute("DROP TABLE IF EXISTS ca_abc_licenses_backup")
    c.execute("CREATE TABLE ca_abc_licenses_backup AS SELECT * FROM ca_abc_licenses")
    backup_count = c.execute("SELECT COUNT(*) FROM ca_abc_licenses_backup").fetchone()[0]
    print(f"✅ Backed up existing table ({backup_count:,} rows → ca_abc_licenses_backup)")

    # 2. Clear the stale (synthetic) data
    c.execute("DELETE FROM ca_abc_licenses")
    print(f"✅ Cleared stale data")

    # 3. Load the real ABC export
    now = datetime.now(timezone.utc).isoformat()
    loaded = 0
    skipped = 0

    with open(CSV_PATH, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if len(row) < 30:
                skipped += 1
                continue
            license_type = get(row, "license_type")
            license_number = get(row, "license_number")
            if not license_number:
                skipped += 1
                continue

            c.execute("""
                INSERT OR REPLACE INTO ca_abc_licenses
                (license_number, license_type, license_type_name, status,
                 business_name, owner_name, address, city, state, zip, county,
                 phone, issue_date, expiration_date, scraped_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                license_number,
                license_type,
                TYPE_NAMES.get(license_type, ""),
                get(row, "status"),
                get(row, "business_name"),
                get(row, "dba"),  # DBA as owner_name (closest available field)
                get(row, "address"),
                get(row, "city"),
                get(row, "state"),
                get(row, "zip"),
                get(row, "county"),
                "",   # phone — not in ABC export (needs Google Places enrichment)
                "",   # issue_date — not cleanly in export
                "",   # expiration_date — not cleanly in export
                now,
            ))
            loaded += 1

    conn.commit()

    final = c.execute("SELECT COUNT(*) FROM ca_abc_licenses").fetchone()[0]
    conn.close()

    print(f"✅ Loaded {loaded:,} real ABC records (skipped {skipped:,} malformed)")
    print(f"\n{'='*50}")
    print(f"  ca_abc_licenses: {final:,} records (was {backup_count:,} synthetic)")
    print(f"  → now LIVE with the real CA ABC export")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
