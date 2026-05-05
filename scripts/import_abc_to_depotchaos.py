#!/usr/bin/env python3
"""
Import CA ABC licenses from daily collection to DepotChaos unified database
"""

import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
ENRICHMENT_FILE = "/root/.openclaw/workspace/datadepot/data/enriched_2026-05-05.json"

def import_abc_licenses():
    # Load enrichment data
    if not Path(ENRICHMENT_FILE).exists():
        print(f"❌ Enrichment file not found: {ENRICHMENT_FILE}")
        return
    
    with open(ENRICHMENT_FILE, 'r') as f:
        licenses = json.load(f)
    
    print(f"📊 Found {len(licenses)} ABC licenses to import")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get current count
    c.execute("SELECT COUNT(*) FROM leads WHERE source_type = 'CA_ABC_Intelligence'")
    existing = c.fetchone()[0]
    print(f"   Existing ABC leads: {existing}")
    
    imported = 0
    skipped = 0
    
    for lic in licenses:
        company = lic.get('business_name', '')
        if not company:
            continue
        
        # Check for duplicate by company name
        c.execute("SELECT id FROM leads WHERE company_name = ? LIMIT 1", (company,))
        if c.fetchone():
            skipped += 1
            continue
        
        # Build enrichment data
        enrichment = {
            'license_number': lic.get('license_number', ''),
            'dba_name': lic.get('dba_name', ''),
            'address': lic.get('address', ''),
            'city': lic.get('city', ''),
            'zip': lic.get('zip', ''),
            'state': lic.get('state', 'CA'),
            'county': lic.get('county', ''),
            'license_type': lic.get('license_type', ''),
            'issue_date': lic.get('issue_date', ''),
            'expiration': lic.get('expiration', ''),
            'capacity': lic.get('capacity', ''),
            'status': lic.get('status', ''),
            'pos_system': lic.get('pos_system', 'Unknown'),
            'replacement_score': lic.get('replacement_score', 50),
            'lead_priority': lic.get('lead_priority', 'C')
        }
        
        # Determine tier from priority
        priority = lic.get('lead_priority', 'C')
        tier = f"Tier {priority}"
        
        # Insert into database - match actual schema
        lead_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        c.execute("""
            INSERT INTO leads (
                id, company_name, county, status, tier,
                pos_system, replacement_score, source_type,
                assigned_agent, enrichment_data, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead_id,
            company,
            lic.get('county', lic.get('city', '')),
            'new',
            tier,
            lic.get('pos_system', 'Unknown'),
            lic.get('replacement_score', 50),
            'CA_ABC_Intelligence',
            'Miles',
            json.dumps(enrichment),
            created_at
        ))
        
        imported += 1
    
    conn.commit()
    
    # Get new count
    c.execute("SELECT COUNT(*) FROM leads WHERE source_type = 'CA_ABC_Intelligence'")
    new_count = c.fetchone()[0]
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"✅ CA ABC IMPORT COMPLETE")
    print(f"{'='*60}")
    print(f"   New licenses imported: {imported}")
    print(f"   Duplicates skipped: {skipped}")
    print(f"   Previous ABC count: {existing}")
    print(f"   New ABC count: {new_count}")

if __name__ == "__main__":
    import_abc_licenses()
