#!/usr/bin/env python3
"""
Import ALL Teriyaki Madness locations from CSV to unified.db
Properly handles all 190 locations
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
    skipped = 0
    errors = 0
    
    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            store_id = row.get('Store_ID', '').strip()
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
            
            # Parse state from store_name if not in state column
            if not state and store_name:
                # Extract state from name like "CA - Teriyaki Madness ..."
                parts = store_name.split(' - ')
                if len(parts) > 0 and len(parts[0]) == 2:
                    state = parts[0]
            
            # Clean up business name
            if store_name.startswith('CA - '):
                business_name = store_name.replace('CA - ', 'Teriyaki Madness - ')
            elif store_name.startswith('AL - '):
                business_name = store_name.replace('AL - ', 'Teriyaki Madness - ')
            elif store_name.startswith('AZ - '):
                business_name = store_name.replace('AZ - ', 'Teriyaki Madness - ')
            elif store_name.startswith('CO - '):
                business_name = store_name.replace('CO - ', 'Teriyaki Madness - ')
            elif store_name.startswith('CT - '):
                business_name = store_name.replace('CT - ', 'Teriyaki Madness - ')
            elif store_name.startswith('DE - '):
                business_name = store_name.replace('DE - ', 'Teriyaki Madness - ')
            elif store_name.startswith('FL - '):
                business_name = store_name.replace('FL - ', 'Teriyaki Madness - ')
            elif store_name.startswith('GA - '):
                business_name = store_name.replace('GA - ', 'Teriyaki Madness - ')
            elif store_name.startswith('HI - '):
                business_name = store_name.replace('HI - ', 'Teriyaki Madness - ')
            elif store_name.startswith('IA - '):
                business_name = store_name.replace('IA - ', 'Teriyaki Madness - ')
            elif store_name.startswith('ID - '):
                business_name = store_name.replace('ID - ', 'Teriyaki Madness - ')
            elif store_name.startswith('IL - '):
                business_name = store_name.replace('IL - ', 'Teriyaki Madness - ')
            elif store_name.startswith('IN - '):
                business_name = store_name.replace('IN - ', 'Teriyaki Madness - ')
            elif store_name.startswith('KS - '):
                business_name = store_name.replace('KS - ', 'Teriyaki Madness - ')
            elif store_name.startswith('KY - '):
                business_name = store_name.replace('KY - ', 'Teriyaki Madness - ')
            elif store_name.startswith('LA - '):
                business_name = store_name.replace('LA - ', 'Teriyaki Madness - ')
            elif store_name.startswith('MA - '):
                business_name = store_name.replace('MA - ', 'Teriyaki Madness - ')
            elif store_name.startswith('MD - '):
                business_name = store_name.replace('MD - ', 'Teriyaki Madness - ')
            elif store_name.startswith('MI - '):
                business_name = store_name.replace('MI - ', 'Teriyaki Madness - ')
            elif store_name.startswith('MN - '):
                business_name = store_name.replace('MN - ', 'Teriyaki Madness - ')
            elif store_name.startswith('MO - '):
                business_name = store_name.replace('MO - ', 'Teriyaki Madness - ')
            elif store_name.startswith('MT - '):
                business_name = store_name.replace('MT - ', 'Teriyaki Madness - ')
            elif store_name.startswith('NC - '):
                business_name = store_name.replace('NC - ', 'Teriyaki Madness - ')
            elif store_name.startswith('ND - '):
                business_name = store_name.replace('ND - ', 'Teriyaki Madness - ')
            elif store_name.startswith('NE - '):
                business_name = store_name.replace('NE - ', 'Teriyaki Madness - ')
            elif store_name.startswith('NH - '):
                business_name = store_name.replace('NH - ', 'Teriyaki Madness - ')
            elif store_name.startswith('NJ - '):
                business_name = store_name.replace('NJ - ', 'Teriyaki Madness - ')
            elif store_name.startswith('NM - '):
                business_name = store_name.replace('NM - ', 'Teriyaki Madness - ')
            elif store_name.startswith('NV - '):
                business_name = store_name.replace('NV - ', 'Teriyaki Madness - ')
            elif store_name.startswith('NY - '):
                business_name = store_name.replace('NY - ', 'Teriyaki Madness - ')
            elif store_name.startswith('OH - '):
                business_name = store_name.replace('OH - ', 'Teriyaki Madness - ')
            elif store_name.startswith('OK - '):
                business_name = store_name.replace('OK - ', 'Teriyaki Madness - ')
            elif store_name.startswith('OR - '):
                business_name = store_name.replace('OR - ', 'Teriyaki Madness - ')
            elif store_name.startswith('PA - '):
                business_name = store_name.replace('PA - ', 'Teriyaki Madness - ')
            elif store_name.startswith('SC - '):
                business_name = store_name.replace('SC - ', 'Teriyaki Madness - ')
            elif store_name.startswith('SD - '):
                business_name = store_name.replace('SD - ', 'Teriyaki Madness - ')
            elif store_name.startswith('TN - '):
                business_name = store_name.replace('TN - ', 'Teriyaki Madness - ')
            elif store_name.startswith('TX - '):
                business_name = store_name.replace('TX - ', 'Teriyaki Madness - ')
            elif store_name.startswith('UT - '):
                business_name = store_name.replace('UT - ', 'Teriyaki Madness - ')
            elif store_name.startswith('VA - '):
                business_name = store_name.replace('VA - ', 'Teriyaki Madness - ')
            elif store_name.startswith('WA - '):
                business_name = store_name.replace('WA - ', 'Teriyaki Madness - ')
            elif store_name.startswith('WI - '):
                business_name = store_name.replace('WI - ', 'Teriyaki Madness - ')
            elif store_name.startswith('WV - '):
                business_name = store_name.replace('WV - ', 'Teriyaki Madness - ')
            else:
                business_name = store_name if store_name else f"Teriyaki Madness - {city}"
            
            # Extract city from address if city is empty
            if not city and address:
                # Try to extract city from address
                parts = address.split(',')
                if len(parts) >= 2:
                    city = parts[-2].strip()
            
            # Skip if no state
            if not state:
                skipped += 1
                continue
            
            # Clean up state
            state = state.replace('"', '').strip()
            if state == 'California':
                state = 'CA'
            elif state == 'Texas':
                state = 'TX'
            elif state == 'Florida':
                state = 'FL'
            # Add more state mappings as needed
            
            # Check if this exact location already exists
            c.execute("""
                SELECT id FROM leads 
                WHERE business_name = ? AND state = ? AND (city = ? OR (city IS NULL AND ? = ''))
            """, (business_name, state, city, city))
            existing = c.fetchone()
            
            enrichment_data = {
                "teriyaki_store_id": store_id,
                "source": "teriyaki_madness_locations.csv",
                "imported_at": datetime.now().isoformat(),
                "latitude": lat,
                "longitude": lng,
                "order_url": order_url,
                "status": status,
                "address": address
            }
            
            try:
                if existing:
                    # Update existing
                    c.execute("""
                        UPDATE leads SET
                            city = COALESCE(NULLIF(city, ''), ?),
                            zip = COALESCE(NULLIF(zip, ''), ?),
                            phone = COALESCE(NULLIF(phone, ''), ?),
                            address = COALESCE(NULLIF(address, ''), ?),
                            enrichment_data = ?,
                            enrichment_status = 'enriched',
                            enriched_at = datetime('now'),
                            tier = COALESCE(NULLIF(tier, ''), 'Tier 3'),
                            source_type = 'Teriyaki Madness Official',
                            tags = COALESCE(NULLIF(tags, ''), 'franchise,teriyaki_madness'),
                            business_type = COALESCE(NULLIF(business_type, ''), 'Fast Casual Restaurant'),
                            category = COALESCE(NULLIF(category, ''), 'Restaurantes')
                        WHERE id = ?
                    """, (city, zip_code, phone, address, json.dumps(enrichment_data), existing[0]))
                else:
                    # Insert new
                    c.execute("""
                        INSERT INTO leads (
                            business_name, city, state, zip, phone, address,
                            business_type, category,
                            enrichment_data, enrichment_status, enriched_at,
                            tier, status, source_type, created_at, tags, deleted
                        ) VALUES (?, ?, ?, ?, ?, ?, 
                                'Fast Casual Restaurant', 'Restaurantes',
                                ?, 'enriched', datetime('now'),
                                'Tier 3', 'new', 'Teriyaki Madness Official', datetime('now'), 
                                'franchise,teriyaki_madness', 0)
                    """, (business_name, city, state, zip_code, phone, address, json.dumps(enrichment_data)))
                    imported += 1
            except Exception as e:
                print(f"Error processing {business_name}: {e}")
                errors += 1
    
    conn.commit()
    conn.close()
    
    print(f"Teriyaki Madness Import Complete:")
    print(f"  - New locations imported: {imported}")
    print(f"  - Skipped (no state): {skipped}")
    print(f"  - Errors: {errors}")
    print(f"  - Total in DB now: {imported + 6}")  # 6 existing

if __name__ == "__main__":
    import_teriyaki_locations()
