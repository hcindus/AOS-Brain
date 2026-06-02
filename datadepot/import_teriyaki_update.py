#!/usr/bin/env python3
"""
Update Teriyaki Madness accounts with recently pulled data
Imports from TOP_165_CALL_LIST.csv and yelp_cache.json
"""

import sqlite3
import json
import csv
from pathlib import Path

# Database path
DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
CSV_PATH = "/root/.openclaw/workspace/datadepot/leads/TOP_165_CALL_LIST.csv"
YELP_CACHE_PATH = "/root/.openclaw/workspace/DepotChaos/yelp_cache.json"

def load_yelp_cache():
    """Load Yelp enrichment data"""
    with open(YELP_CACHE_PATH) as f:
        return json.load(f)

def import_teriyaki_accounts():
    """Import Teriyaki Madness accounts from CSV and Yelp cache"""
    
    # Load Yelp cache
    yelp_cache = load_yelp_cache()
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Stats
    imported = 0
    updated = 0
    seen = set()
    
    # Read CSV
    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            business_name = row.get('business_name', '').strip()
            
            if 'teriyaki madness' not in business_name.lower():
                continue
            
            # Skip duplicates (we'll use the richer data)
            if business_name in seen:
                continue
            seen.add(business_name)
            
            # CSV columns: business_name,pos_system,status_notes,annual_projection,contact,phone,phone_2,address,city,state,email,priority
            city = row.get('city', '').strip()
            state = row.get('state', '').strip()
            phone = row.get('phone', '').strip()
            phone_2 = row.get('phone_2', '').strip()
            email = row.get('email', '').strip()
            address = row.get('address', '').strip()
            contact_name = row.get('contact', '').strip()
            notes = row.get('status_notes', '').strip()
            
            # Fix misaligned columns (email field has address in some rows)
            if '@' not in email and 'Street' in email:
                address = email
                email = ''
            if city == '' and 'O/S' in state:
                state = ''
            
            # Look for Yelp enrichment
            yelp_key = business_name.upper().replace(' ', '_').replace('-', '_') + '__'
            yelp_data = yelp_cache.get(yelp_key, {})
            
            # Merge data (Yelp takes priority for some fields if CSV is missing them)
            if yelp_data:
                yelp_phone = yelp_data.get('phone', '').replace('+1', '')
                if yelp_phone and not phone:
                    phone = yelp_phone
                if yelp_data.get('city') and not city:
                    city = yelp_data.get('city', '')
                if yelp_data.get('state') and not state:
                    state = yelp_data.get('state', '')
                if yelp_data.get('zip') and not row.get('zip'):
                    row['zip'] = yelp_data.get('zip', '')
                if yelp_data.get('address') and (not address or address == '0'):
                    address = yelp_data.get('address', '')
            
            # Check if lead exists
            c.execute("SELECT id FROM leads WHERE business_name = ?", (business_name,))
            existing = c.fetchone()
            
            enrichment_data = {
                "yelp_data": yelp_data,
                "csv_data": {
                    "phone_2": phone_2,
                    "status_notes": notes,
                    "priority": row.get('priority', '')
                },
                "source_file": "TOP_165_CALL_LIST.csv",
                "last_updated": "2026-06-02",
                "import_source": "teriyaki_update_script"
            }
            
            if existing:
                # Update existing lead
                c.execute("""
                    UPDATE leads SET
                        city = COALESCE(NULLIF(?, ''), city),
                        state = COALESCE(NULLIF(?, ''), state),
                        phone = COALESCE(NULLIF(?, ''), phone),
                        email = COALESCE(NULLIF(?, ''), email),
                        address = COALESCE(NULLIF(?, ''), address),
                        contact_name = COALESCE(NULLIF(?, ''), contact_name),
                        enrichment_data = ?,
                        enrichment_status = 'enriched',
                        enriched_at = datetime('now'),
                        tier = COALESCE(NULLIF(tier, ''), 'Tier 2'),
                        status = COALESCE(NULLIF(status, ''), 'new')
                    WHERE id = ?
                """, (city, state, phone, email, address, contact_name, 
                      json.dumps(enrichment_data), existing[0]))
                updated += 1
            else:
                # Insert new lead
                c.execute("""
                    INSERT INTO leads (
                        business_name, city, state, phone, email, address,
                        contact_name, enrichment_data, enrichment_status, 
                        enriched_at, tier, status, created_at, deleted
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'enriched', datetime('now'), 
                              'Tier 2', 'new', datetime('now'), 0)
                """, (business_name, city, state, phone, email, address,
                      contact_name, json.dumps(enrichment_data)))
                imported += 1
    
    conn.commit()
    conn.close()
    
    print(f"Teriyaki Madness Import Complete:")
    print(f"  - New leads imported: {imported}")
    print(f"  - Existing leads updated: {updated}")
    print(f"  - Total unique accounts processed: {imported + updated}")

if __name__ == "__main__":
    import_teriyaki_accounts()
