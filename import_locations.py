#!/usr/bin/env python3
"""
Import Mountain Mike's Pizza and Teriyaki Madness locations into DepotChaos unified.db
"""

import json
import sqlite3
from datetime import datetime
import re

DB_PATH = '/root/.openclaw/workspace/data/depot_chaos/unified.db'
TERIYAKI_JSON = '/root/.openclaw/workspace/data/teriyaki_madness_full.json'

def parse_address(address_str):
    """Parse a full address string into components"""
    if not address_str:
        return None, None, None, None
    
    # Try to extract zip code
    zip_match = re.search(r'\b(\d{5}(-\d{4})?)\b', address_str)
    zip_code = zip_match.group(1) if zip_match else None
    
    # Try to extract state (2 letter codes)
    state_match = re.search(r'\b([A-Z]{2})\b', address_str)
    state = state_match.group(1) if state_match else None
    
    # Try to extract city (usually before state and zip)
    city = None
    if state_match:
        before_state = address_str[:state_match.start()].strip()
        parts = before_state.split(',')
        if len(parts) >= 2:
            city = parts[-1].strip()
    
    return address_str, city, state, zip_code

def import_teriyaki_madness():
    """Import all Teriyaki Madness locations from JSON file"""
    
    with open(TERIYAKI_JSON, 'r') as f:
        data = json.load(f)
    
    locations = data.get('results', {}).get('locations', [])
    print(f"Found {len(locations)} Teriyaki Madness locations in JSON file")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added = 0
    updated = 0
    skipped = 0
    
    for loc in locations:
        name = loc.get('name', '')
        address_line = loc.get('address_line_1', '') or loc.get('address', '')
        city = loc.get('city', '')
        state = loc.get('state', '')
        zip_code = loc.get('postcode', '')
        phone = loc.get('phone', '')
        country = loc.get('country', 'US')
        
        # Clean up business name
        business_name = f"Teriyaki Madness - {city}" if city else f"Teriyaki Madness - {name}"
        
        # Skip if already exists
        cursor.execute("""
            SELECT id FROM leads 
            WHERE business_name = ? AND city = ? AND state = ?
        """, (business_name, city, state))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing record with any new info
            cursor.execute("""
                UPDATE leads SET 
                    phone = COALESCE(NULLIF(phone, ''), ?),
                    address = COALESCE(NULLIF(address, ''), ?),
                    zip = COALESCE(NULLIF(zip, ''), ?),
                    country = COALESCE(NULLIF(country, ''), ?),
                    business_type = COALESCE(NULLIF(business_type, ''), 'Restaurant'),
                    category = COALESCE(NULLIF(category, ''), 'Fast Food')
                WHERE id = ?
            """, (phone, address_line, zip_code, country, existing[0]))
            updated += 1
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO leads (
                    business_name, city, state, zip, phone, address, country,
                    business_type, category, source, scraped_at, status,
                    created_at, enrichment_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                business_name, city, state, zip_code, phone, address_line, country,
                'Restaurant', 'Fast Food', 'teriyaki_madness_import',
                datetime.now().isoformat(), 'new',
                datetime.now().isoformat(), 'pending'
            ))
            added += 1
    
    conn.commit()
    conn.close()
    
    print(f"Teriyaki Madness: {added} added, {updated} updated, {skipped} skipped")
    return added, updated

def import_mountain_mikes():
    """
    Mountain Mike's Pizza locations - need to fetch from web or check existing
    Based on database query, we have 7 locations already.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check existing Mountain Mike's locations
    cursor.execute("""
        SELECT business_name, city, state, phone, address 
        FROM leads 
        WHERE business_name LIKE '%Mountain Mike%'
    """)
    
    existing = cursor.fetchall()
    print(f"Found {len(existing)} Mountain Mike's Pizza locations in database:")
    for row in existing:
        print(f"  - {row[0]} ({row[1]}, {row[2]})")
    
    conn.close()
    
    # Mountain Mike's has ~200 locations across CA, OR, NV, UT
    # For now, we acknowledge we have 7 in the Sacramento area
    print(f"\nNote: Mountain Mike's Pizza has approximately 200 locations.")
    print(f"Currently have {len(existing)} locations in database (Sacramento area).")
    print(f"To add more, we would need to scrape their locations page.")
    
    return len(existing)

if __name__ == '__main__':
    print("=" * 60)
    print("Importing Restaurant Locations to DepotChaos")
    print("=" * 60)
    
    print("\n--- Teriyaki Madness ---")
    added, updated = import_teriyaki_madness()
    
    print("\n--- Mountain Mike's Pizza ---")
    existing = import_mountain_mikes()
    
    print("\n" + "=" * 60)
    print("Import Summary")
    print("=" * 60)
    print(f"Teriyaki Madness: {added} new locations added, {updated} existing updated")
    print(f"Mountain Mike's Pizza: {existing} locations currently in database")
