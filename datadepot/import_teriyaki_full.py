#!/usr/bin/env python3
"""
Import Teriyaki Madness locations from CSV to unified.db
"""

import sqlite3
import csv
import json
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
CSV_PATH = "/root/.openclaw/workspace/data/teriyaki_madness_locations.csv"

def import_teriyaki_locations():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    imported = 0
    updated = 0
    coming_soon = 0
    
    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            store_name = row.get('Store_Name', '').strip()
            address = row.get('Address', '').strip()
            city = row.get('City', '').strip()
            state = row.get('State', '').strip()
            zip_code = row.get('ZIP', '').strip()
            phone = row.get('Phone', '').strip()
            status = row.get('Status', '').strip()
            lat = row.get('Latitude', '').strip()
            lng = row.get('Longitude', '').strip()
            order_url = row.get('Order_URL', '').strip()
            
            # Business name
            business_name = store_name if store_name else f"Teriyaki Madness - {city}"
            
            # Check for existing
            c.execute("SELECT id FROM leads WHERE business_name = ?", (business_name,))
            existing = c.fetchone()
            
            enrichment_data = {
                "teriyaki_store_id": row.get('Store_ID'),
                "source": "teriyaki_madness_locations.csv",
                "imported_at": datetime.now().isoformat(),
                "latitude": lat,
                "longitude": lng,
                "order_url": order_url,
                "status": status
            }
            
            if status == "COMING SOON":
                coming_soon += 1
            
            if existing:
                # Update
                c.execute("""
                    UPDATE leads SET
                        city = COALESCE(NULLIF(city, ''), ?),
                        state = COALESCE(NULLIF(state, ''), ?),
                        zip = COALESCE(NULLIF(zip, ''), ?),
                        phone = COALESCE(NULLIF(phone, ''), ?),
                        address = COALESCE(NULLIF(address, ''), ?),
                        enrichment_data = ?,
                        enrichment_status = 'enriched',
                        enriched_at = datetime('now'),
                        tier = COALESCE(NULLIF(tier, ''), 'Tier 3'),
                        source_type = 'Teriyaki Madness Official'
                    WHERE id = ?
                """, (city, state, zip_code, phone, address, json.dumps(enrichment_data), existing[0]))
                updated += 1
            else:
                # Insert new
                c.execute("""
                    INSERT INTO leads (
                        business_name, city, state, zip, phone, address,
                        enrichment_data, enrichment_status, enriched_at,
                        tier, status, source_type, created_at, deleted
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'enriched', datetime('now'),
                              'Tier 3', 'new', 'Teriyaki Madness Official', datetime('now'), 0)
                """, (business_name, city, state, zip_code, phone, address, json.dumps(enrichment_data)))
                imported += 1
    
    conn.commit()
    conn.close()
    
    print(f"Teriyaki Madness Import Complete:")
    print(f"  - New locations imported: {imported}")
    print(f"  - Existing locations updated: {updated}")
    print(f"  - Coming Soon locations: {coming_soon}")
    print(f"  - Total processed: {imported + updated}")

if __name__ == "__main__":
    import_teriyaki_locations()
