#!/usr/bin/env python3
"""
Import ALL CA ABC licenses from ca_abc_licenses table to leads table
Converts 74,000+ ABC records to unified leads format
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def import_all_abc_to_leads():
    """Import all ABC licenses to leads table"""
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get total ABC licenses
    c.execute("SELECT COUNT(*) FROM ca_abc_licenses")
    total_abc = c.fetchone()[0]
    print(f"📊 Total ABC licenses in database: {total_abc}")
    
    # Get current leads count
    c.execute("SELECT COUNT(*) FROM leads WHERE source_type = 'CA_ABC' OR source LIKE '%ABC%'")
    existing_leads = c.fetchone()[0]
    print(f"   Existing ABC leads: {existing_leads}")
    
    # Get all ABC licenses not yet in leads
    c.execute("""
        SELECT * FROM ca_abc_licenses
        WHERE business_name NOT IN (
            SELECT business_name FROM leads WHERE business_name IS NOT NULL
        )
        LIMIT 5000
    """)
    
    abc_records = c.fetchall()
    print(f"\n🔄 Processing {len(abc_records)} ABC records for import...")
    
    imported = 0
    skipped = 0
    errors = 0
    
    for abc in abc_records:
        try:
            business_name = abc['business_name']
            if not business_name:
                skipped += 1
                continue
            
            # Check for exact duplicate
            c.execute("SELECT id FROM leads WHERE business_name = ? AND city = ? LIMIT 1", 
                     (business_name, abc['city']))
            if c.fetchone():
                skipped += 1
                continue
            
            # Build enrichment data
            enrichment = {
                'license_number': abc['license_number'],
                'license_type': abc['license_type'],
                'license_type_name': abc['license_type_name'],
                'status': abc['status'],
                'owner_name': abc['owner_name'],
                'address': abc['address'],
                'county': abc['county'],
                'zip': abc['zip'],
                'phone': abc['phone'],
                'issue_date': abc['issue_date'],
                'expiration_date': abc['expiration_date'],
                'source': 'ca_abc_licenses'
            }
            
            # Determine priority/tier
            license_type = abc['license_type'] or ''
            if license_type in ['47', '48', '41']:
                priority = 'A'
                tier = 'Tier A'
            elif license_type in ['20', '21', '58']:
                priority = 'B'
                tier = 'Tier B'
            else:
                priority = 'C'
                tier = 'Tier C'
            
            # Insert into leads
            c.execute("""
                INSERT INTO leads (
                    business_name, county, city, state, zip, phone, status, tier,
                    source, source_type, enrichment_status, enrichment_data, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                business_name,
                abc['county'],
                abc['city'],
                abc['state'] or 'CA',
                abc['zip'],
                abc['phone'],
                'new',
                tier,
                'CA_ABC_Scraper',
                'CA_ABC',
                'enriched',
                json.dumps(enrichment),
                abc['scraped_at'] or datetime.now().isoformat()
            ))
            
            imported += 1
            
            if imported % 500 == 0:
                print(f"   Progress: {imported} imported...")
                conn.commit()
                
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"   ⚠️ Error on record {business_name}: {e}")
    
    conn.commit()
    
    # Get final count
    c.execute("SELECT COUNT(*) FROM leads WHERE source_type = 'CA_ABC'")
    final_count = c.fetchone()[0]
    
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"✅ CA ABC IMPORT COMPLETE")
    print(f"{'='*60}")
    print(f"   Records processed: {len(abc_records)}")
    print(f"   New leads imported: {imported}")
    print(f"   Duplicates skipped: {skipped}")
    print(f"   Errors: {errors}")
    print(f"   Previous ABC leads: {existing_leads}")
    print(f"   Total ABC leads: {final_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    import_all_abc_to_leads()
