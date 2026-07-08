#!/usr/bin/env python3
"""
Import California Casinos into DepotChaos CRM
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
CASINO_JSON = "/root/.openclaw/workspace/scrapers/ca_casinos_20260708_222948.json"

def import_casinos():
    """Import casino data into DepotChaos leads table"""
    
    # Load casino data
    with open(CASINO_JSON, 'r') as f:
        data = json.load(f)
    
    casinos = data['casinos']
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    imported = 0
    skipped = 0
    
    print(f"Importing {len(casinos)} California casinos into DepotChaos...")
    print("=" * 60)
    
    for casino in casinos:
        # Check if already exists
        cursor.execute(
            "SELECT id FROM leads WHERE business_name = ? AND city = ? AND state = ?",
            (casino['name'], casino['city'], 'CA')
        )
        
        if cursor.fetchone():
            print(f"  Skipping (exists): {casino['name']}")
            skipped += 1
            continue
        
        # Insert new lead - use sos_url for website since that's available
        cursor.execute("""
            INSERT INTO leads (
                business_name, city, state, zip, phone, address, 
                sos_url, business_type, category, source, 
                scraped_at, priority, status, enrichment_status,
                created_at, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            casino['name'],
            casino['city'],
            'CA',
            casino.get('zip_code', ''),
            casino.get('phone', ''),
            casino.get('address', ''),
            casino.get('website', ''),
            'Casino',
            'Gaming/Casino',
            'CA_Casino_Scraper',
            casino.get('scraped_at', datetime.now().isoformat()),
            'high',  # High priority
            'new',
            'pending',
            datetime.now().isoformat(),
            f"Tribe: {casino.get('tribe', 'Unknown')}, Gaming: {', '.join(casino.get('gaming_types', []))}"
        ))
        
        imported += 1
        print(f"  ✓ Imported: {casino['name']}")
    
    conn.commit()
    conn.close()
    
    print("=" * 60)
    print(f"Import complete!")
    print(f"  Imported: {imported}")
    print(f"  Skipped (duplicates): {skipped}")
    print(f"  Total: {imported + skipped}")
    
    # Get total count
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM leads")
    total_leads = cursor.fetchone()[0]
    print(f"\nTotal leads in DepotChaos: {total_leads:,}")
    conn.close()

if __name__ == "__main__":
    import_casinos()
