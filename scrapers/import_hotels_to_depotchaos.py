#!/usr/bin/env python3
"""
Import California Hotels into DepotChaos CRM (for Capton)
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
HOTEL_JSON = "/root/.openclaw/workspace/scrapers/ca_hotels_20260708_223517.json"

def import_hotels():
    """Import hotel data into DepotChaos leads table"""
    
    with open(HOTEL_JSON, 'r') as f:
        data = json.load(f)
    
    hotels = data['hotels']
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    imported = 0
    skipped = 0
    
    print(f"Importing {len(hotels)} California hotels into DepotChaos...")
    print("=" * 60)
    
    for hotel in hotels:
        # Check if already exists
        cursor.execute(
            "SELECT id FROM leads WHERE business_name = ? AND city = ? AND state = ?",
            (hotel['name'], hotel['city'], 'CA')
        )
        
        if cursor.fetchone():
            print(f"  Skipping (exists): {hotel['name']}")
            skipped += 1
            continue
        
        # Insert new lead
        cursor.execute("""
            INSERT INTO leads (
                business_name, city, state, zip, phone, address, 
                sos_url, business_type, category, source, 
                scraped_at, priority, status, enrichment_status,
                created_at, tags, employee_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            hotel['name'],
            hotel['city'],
            'CA',
            hotel.get('zip_code', ''),
            hotel.get('phone', ''),
            hotel.get('address', ''),
            '',  # sos_url
            'Hotel',
            'Hospitality',
            'CA_Hotel_Scraper_Capton',
            hotel.get('scraped_at', datetime.now().isoformat()),
            'high',
            'new',
            'pending',
            datetime.now().isoformat(),
            f"Rooms: {hotel.get('rooms', 'N/A')}, Has Bar: {hotel.get('has_bar', True)}",
            str(hotel.get('rooms', ''))  # employee_count used for room count
        ))
        
        imported += 1
        print(f"  ✓ Imported: {hotel['name']}")
    
    conn.commit()
    conn.close()
    
    print("=" * 60)
    print(f"Import complete!")
    print(f"  Imported: {imported}")
    print(f"  Skipped: {skipped}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM leads")
    total = cursor.fetchone()[0]
    print(f"\nTotal leads in DepotChaos: {total:,}")
    conn.close()

if __name__ == "__main__":
    import_hotels()
