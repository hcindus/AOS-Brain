#!/usr/bin/env python3
"""
Import consolidated leads to DepotChaos database
Imports from COMPLETED_*.csv files (real estate, Canada, Mexico leads)
"""

import sqlite3
import csv
import uuid
import glob
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
LEADS_DIR = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_consolidated"

def import_consolidated():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Count existing
    c.execute("SELECT COUNT(*) FROM leads")
    existing = c.fetchone()[0]
    print(f"Existing leads: {existing}")
    
    # Get all completed files (exclude CA_ files - those are Canada, not California)
    completed_files = sorted(glob.glob(f"{LEADS_DIR}/COMPLETED_*.csv"))
    
    # Filter out Canada/Mexico province files if needed
    state_files = [f for f in completed_files if not any(x in f for x in ['_CA_AB_', '_CA_BC_', '_CA_MB_', '_CA_NB_', '_CA_NS_', '_CA_ON_', '_CA_QC_', '_CA_SK_', '_MX_'])]
    ca_files = [f for f in completed_files if any(x in f for x in ['_CA_AB_', '_CA_BC_', '_CA_MB_', '_CA_NB_', '_CA_NS_', '_CA_ON_', '_CA_QC_', '_CA_SK_'])]
    mx_files = [f for f in completed_files if '_MX_' in f]
    
    print(f"\nFound {len(state_files)} US state files")
    print(f"Found {len(ca_files)} Canada province files")
    print(f"Found {len(mx_files)} Mexico state files")
    
    total_imported = 0
    total_skipped = 0
    region_counts = {}
    
    # Process US state files
    for csv_path in state_files:
        region = Path(csv_path).stem.replace("COMPLETED_", "").replace("_leads", "").replace("_ALL", "")
        print(f"\n📍 Processing {region}...")
        
        imported, skipped = process_file(c, csv_path, region, is_us=True)
        region_counts[region] = imported
        total_imported += imported
        total_skipped += skipped
    
    # Process Canada files
    for csv_path in ca_files:
        region = Path(csv_path).stem.replace("COMPLETED_", "").replace("_leads", "")
        print(f"\n🇨🇦 Processing {region}...")
        
        imported, skipped = process_file(c, csv_path, region, is_us=False, is_canada=True)
        region_counts[region] = imported
        total_imported += imported
        total_skipped += skipped
    
    # Process Mexico files
    for csv_path in mx_files:
        region = Path(csv_path).stem.replace("COMPLETED_", "").replace("_leads", "")
        print(f"\n🇲🇽 Processing {region}...")
        
        imported, skipped = process_file(c, csv_path, region, is_us=False, is_mexico=True)
        region_counts[region] = imported
        total_imported += imported
        total_skipped += skipped
    
    conn.commit()
    
    # Final count
    c.execute("SELECT COUNT(*) FROM leads")
    final_count = c.fetchone()[0]
    conn.close()
    
    print(f"\n" + "="*60)
    print(f"✅ CONSOLIDATED IMPORT COMPLETE")
    print(f"="*60)
    print(f"   Total imported: {total_imported}")
    print(f"   Total skipped (duplicates): {total_skipped}")
    print(f"   Previous count: {existing}")
    print(f"   Final database count: {final_count}")
    print(f"\n   By Region:")
    for region, count in sorted(region_counts.items()):
        if count > 0:
            print(f"      {region}: {count} leads")

def process_file(c, csv_path, region, is_us=True, is_canada=False, is_mexico=False):
    imported = 0
    skipped = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    lead_id = str(uuid.uuid4())
                    
                    # Map fields
                    company = row.get('Company', '')
                    first_name = row.get('First Name', '')
                    last_name = row.get('Last Name', '')
                    email = row.get('Email', '')
                    phone = row.get('Phone', '')
                    city = row.get('City', '')
                    state = row.get('State', '')
                    
                    # For county, use city if not available
                    county = city if city else region
                    
                    # Country
                    country = row.get('Country', '')
                    if is_us:
                        country = 'US'
                    elif is_canada:
                        country = 'CA'
                    elif is_mexico:
                        country = 'MX'
                    
                    # Priority/Tier from tags
                    tags = row.get('Tags', '')
                    priority = 'C'
                    if 'Priority_A' in tags:
                        priority = 'A'
                    elif 'Priority_B' in tags:
                        priority = 'B'
                    elif 'Priority_C' in tags:
                        priority = 'C'
                    
                    tier = f"Tier {priority}" if priority in ['A', 'B', 'C'] else 'Tier 2'
                    
                    # Source
                    source = row.get('Source', f'{region}_Consolidated')
                    notes = row.get('Notes', '')
                    
                    # Check duplicate by email first, then company
                    if email:
                        c.execute("SELECT id FROM leads WHERE enrichment_data LIKE ?", (f'%"email": "{email}"%',))
                        if c.fetchone():
                            skipped += 1
                            continue
                    
                    # Check duplicate by company name
                    c.execute("SELECT id FROM leads WHERE company_name = ?", (company,))
                    if c.fetchone():
                        skipped += 1
                        continue
                    
                    # Calculate replacement score based on priority
                    replacement_score = 50
                    if priority == 'A':
                        replacement_score = 90
                    elif priority == 'B':
                        replacement_score = 70
                    elif priority == 'C':
                        replacement_score = 50
                    
                    # Build enrichment
                    enrichment = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone': phone,
                        'city': city,
                        'state': state,
                        'country': country,
                        'county': county,
                        'tags': tags,
                        'notes': notes,
                        'source_file': Path(csv_path).name,
                        'industry': 'RealEstate' if 'RealEstate' in tags else 'General'
                    }
                    
                    # Insert lead
                    c.execute("""
                        INSERT INTO leads (
                            id, company_name, county, status, tier, 
                            replacement_score, source_type, assigned_agent,
                            enrichment_data, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        lead_id, company, county, 'new', tier,
                        replacement_score, source,
                        'Miles', json.dumps(enrichment), datetime.now().isoformat()
                    ))
                    
                    imported += 1
                    
                except Exception as e:
                    continue
                    
    except Exception as e:
        print(f"   ⚠️ Error reading {region}: {e}")
    
    print(f"   ✅ Imported: {imported} | Skipped: {skipped}")
    return imported, skipped

if __name__ == "__main__":
    import json
    import_consolidated()
