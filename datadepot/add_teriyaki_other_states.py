#!/usr/bin/env python3
"""
Add Teriyaki Madness locations from other states (not CA)
"""

import sqlite3
import csv
import json
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
CSV_PATH = "/root/.openclaw/workspace/data/teriyaki_madness_locations.csv"

def import_teriyaki_nationwide():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    imported = 0
    skipped = 0
    
    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            store_name = row.get('Store_Name', '').strip()
            address = row.get('Address', '').strip()
            city = row.get('City', '').strip()
            state_col = row.get('State', '').strip()
            zip_code = row.get('ZIP', '').strip()
            phone = row.get('Phone', '').strip()
            status = row.get('Status', '').strip()
            lat = row.get('Latitude', '').strip()
            lng = row.get('Longitude', '').strip()
            order_url = row.get('Order_URL', '').strip()
            
            # Skip California (already imported)
            if state_col == 'CA' or state_col == 'California':
                continue
            
            # Parse state
            state = state_col if state_col else ''
            if not state and store_name:
                parts = store_name.split(' - ')
                if len(parts) > 0 and len(parts[0]) == 2:
                    state = parts[0]
            
            # Clean business name
            business_name = store_name
            for prefix in ['AL', 'AZ', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 
                          'KS', 'KY', 'LA', 'MA', 'MD', 'MI', 'MN', 'MO', 'MT', 'NC', 'ND', 'NE',
                          'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'SC', 'SD', 'TN',
                          'TX', 'UT', 'VA', 'WA', 'WI', 'WV']:
                if store_name.startswith(f'{prefix} - '):
                    business_name = store_name.replace(f'{prefix} - ', 'Teriyaki Madness - ')
                    if not state:
                        state = prefix
                    break
            
            if not state:
                skipped += 1
                continue
            
            # Check existing
            c.execute("SELECT id FROM leads WHERE business_name = ? AND state = ? AND city = ?", 
                     (business_name, state, city))
            existing = c.fetchone()
            
            enrichment_data = {
                "teriyaki_store": True,
                "source": "teriyaki_nationwide",
                "imported_at": datetime.now().isoformat(),
                "latitude": lat,
                "longitude": lng,
                "order_url": order_url,
                "status": status,
                "address": address
            }
            
            if not existing:
                c.execute("""
                    INSERT INTO leads (
                        business_name, city, state, zip, phone, address,
                        business_type, category,
                        enrichment_data, enrichment_status, enriched_at,
                        tier, status, source_type, created_at, tags, deleted
                    ) VALUES (?, ?, ?, ?, ?, ?, 
                            'Fast Casual Restaurant', 'Restaurantes',
                            ?, 'enriched', datetime('now'),
                            'Tier 3', 'new', 'Teriyaki Madness Franchise', datetime('now'), 
                            'franchise,teriyaki_madness', 0)
                """, (business_name, city, state, zip_code, phone, address, json.dumps(enrichment_data)))
                imported += 1
    
    conn.commit()
    conn.close()
    
    print(f"Teriyaki Madness Nationwide Import:")
    print(f"  - New imported: {imported}")
    print(f"  - Skipped: {skipped}")

if __name__ == "__main__":
    import_teriyaki_nationwide()
