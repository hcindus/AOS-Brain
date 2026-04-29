#!/usr/bin/env python3
"""
Import all state lead files to DepotChaos database
Imports from FINAL_STATE_*.csv files
"""

import sqlite3
import csv
import uuid
import glob
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
LEADS_DIR = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_final"

def import_all_states():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Count existing
    c.execute("SELECT COUNT(*) FROM leads")
    existing = c.fetchone()[0]
    print(f"Existing leads: {existing}")
    
    # Get all state files
    state_files = sorted(glob.glob(f"{LEADS_DIR}/FINAL_STATE_*.csv"))
    print(f"\nFound {len(state_files)} state files")
    
    total_imported = 0
    total_skipped = 0
    state_counts = {}
    
    for csv_path in state_files:
        state_code = Path(csv_path).stem.replace("FINAL_STATE_", "")
        print(f"\n📍 Processing {state_code}...")
        
        imported = 0
        skipped = 0
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        lead_id = str(uuid.uuid4())
                        
                        # Map fields
                        company_name = row.get('Company', '') or row.get('company_name', '')
                        first_name = row.get('First Name', '')
                        last_name = row.get('Last Name', '')
                        contact = f"{first_name} {last_name}".strip()
                        email = row.get('Email', '')
                        phone = row.get('Phone', '')
                        city = row.get('City', '')
                        county = row.get('County', '') or city
                        state = row.get('State', state_code)
                        zip_code = row.get('Zip', '')
                        address = row.get('Address', '')
                        business_type = row.get('Business Type', '')
                        website = row.get('Website', '')
                        source = row.get('Source', f'{state_code}_State_Scraper')
                        priority = row.get('Priority', 'C')
                        tags = row.get('Tags', '')
                        notes = row.get('Notes', '')
                        
                        # Determine tier
                        tier = f"Tier {priority}" if priority in ['1', '2', '3'] else 'Tier 2'
                        
                        # Calculate replacement score
                        replacement_score = 50
                        if priority == 'A':
                            replacement_score = 90
                        elif priority == 'B':
                            replacement_score = 70
                        elif priority == 'C':
                            replacement_score = 50
                        
                        # Check duplicate
                        c.execute("SELECT id FROM leads WHERE company_name = ? AND county = ?", 
                                 (company_name, county))
                        if c.fetchone():
                            skipped += 1
                            continue
                        
                        # Build enrichment
                        enrichment = {
                            'first_name': first_name,
                            'last_name': last_name,
                            'contact_name': contact,
                            'email': email,
                            'phone': phone,
                            'address': address,
                            'city': city,
                            'county': county,
                            'state': state,
                            'zip': zip_code,
                            'business_type': business_type,
                            'website': website,
                            'priority': priority,
                            'tags': tags,
                            'notes': notes,
                            'source_file': f"FINAL_STATE_{state_code}.csv"
                        }
                        
                        # Insert
                        c.execute("""
                            INSERT INTO leads (
                                id, company_name, county, status, tier, 
                                pos_system, replacement_score, source_type,
                                assigned_agent, enrichment_data, created_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            lead_id, company_name, county, 'new', tier,
                            business_type, replacement_score, source,
                            'Miles', json.dumps(enrichment), datetime.now().isoformat()
                        ))
                        
                        imported += 1
                        
                    except Exception as e:
                        continue
        except Exception as e:
            print(f"   ⚠️ Error reading {state_code}: {e}")
        
        state_counts[state_code] = imported
        total_imported += imported
        total_skipped += skipped
        print(f"   ✅ Imported: {imported} | Skipped: {skipped}")
    
    conn.commit()
    
    # Final count
    c.execute("SELECT COUNT(*) FROM leads")
    final_count = c.fetchone()[0]
    conn.close()
    
    print(f"\n" + "="*60)
    print(f"✅ ALL STATES IMPORT COMPLETE")
    print(f"="*60)
    print(f"   Total imported: {total_imported}")
    print(f"   Total skipped (duplicates): {total_skipped}")
    print(f"   Previous count: {existing}")
    print(f"   Final database count: {final_count}")
    print(f"\n   By State:")
    for state, count in sorted(state_counts.items()):
        if count > 0:
            print(f"      {state}: {count} leads")

if __name__ == "__main__":
    import json
    import_all_states()
