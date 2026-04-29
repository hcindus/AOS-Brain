#!/usr/bin/env python3
"""
Import adapted master clients to DepotChaos database
Imports from ADAPTED_MASTER_CLIENTS.csv and ADAPTED_CLIENTS_US.csv
These are the primary client database for POS sales
"""

import sqlite3
import csv
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
MASTER_CLIENTS_PATH = "/root/.openclaw/workspace/AGI_COMPANY/data/clients_adapted/ADAPTED_MASTER_CLIENTS.csv"

def import_master_clients():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Count existing
    c.execute("SELECT COUNT(*) FROM leads")
    existing = c.fetchone()[0]
    print(f"Existing leads: {existing}")
    
    imported = 0
    skipped = 0
    
    print(f"\n📍 Processing Master Clients...")
    
    try:
        with open(MASTER_CLIENTS_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    lead_id = str(uuid.uuid4())
                    
                    # Map fields from ADAPTED_MASTER_CLIENTS.csv
                    company_name = row.get('Client', '')
                    client_type = row.get('Type', '')  # REAL ESTATE, etc
                    rep = row.get('Rep', '')  # LG, AH, RA, DK
                    system = row.get('System', '')
                    hw_maint = row.get('HW_Maint', '')
                    revenue_tracking = row.get('Revenue_Tracking', '')
                    primary_contact = row.get('Primary_Contact', '')
                    phone = row.get('Phone', '')
                    cell = row.get('Cell', '')
                    tax_pct = row.get('Tax_Pct', '')
                    tax_district = row.get('Tax_District', '')
                    store_address = row.get('Store_Address', '')
                    city = row.get('City', '')
                    state = row.get('State', '')
                    zip_code = row.get('Zip', '')
                    email = row.get('Email', '')
                    ops_email = row.get('Ops_Email', '')
                    billing_email = row.get('Billing_Email', '')
                    notes = row.get('Notes', '')
                    country = row.get('Country', 'US')
                    source = row.get('Source', 'Master_Client_Database')
                    import_date = row.get('Import_Date', '')
                    
                    # Skip empty rows
                    if not company_name:
                        continue
                    
                    # Determine tier based on rep and type
                    tier = 'Tier 2'
                    if rep == 'LG':  # Likely Large accounts
                        tier = 'Tier 1'
                    elif rep == 'AH':
                        tier = 'Tier 1'
                    
                    # Calculate replacement score
                    replacement_score = 60
                    if hw_maint == 'NO':
                        replacement_score += 15  # Need hardware maintenance = better lead
                    if client_type == 'REAL ESTATE':
                        replacement_score += 10  # Real estate = high transaction volume
                    
                    # Check duplicate by email
                    if email:
                        c.execute("SELECT id FROM leads WHERE enrichment_data LIKE ?", (f'%"email": "{email}"%',))
                        if c.fetchone():
                            skipped += 1
                            continue
                    
                    # Check duplicate by company name
                    c.execute("SELECT id FROM leads WHERE company_name = ?", (company_name,))
                    if c.fetchone():
                        skipped += 1
                        continue
                    
                    # Build enrichment data
                    enrichment = {
                        'client_type': client_type,
                        'rep': rep,
                        'system': system,
                        'hw_maintenance': hw_maint,
                        'revenue_tracking': revenue_tracking,
                        'primary_contact': primary_contact,
                        'phone': phone,
                        'cell': cell,
                        'tax_pct': tax_pct,
                        'tax_district': tax_district,
                        'store_address': store_address,
                        'city': city,
                        'state': state,
                        'zip': zip_code,
                        'email': email,
                        'ops_email': ops_email,
                        'billing_email': billing_email,
                        'notes': notes,
                        'country': country,
                        'source_file': 'ADAPTED_MASTER_CLIENTS.csv',
                        'import_date': import_date,
                        'is_master_client': True
                    }
                    
                    # Determine source type
                    source_type = f"Master_{client_type.replace(' ', '_')}" if client_type else 'Master_Client'
                    
                    # County is city for now
                    county = city if city else f"{state}_County"
                    
                    # Insert lead
                    c.execute("""
                        INSERT INTO leads (
                            id, company_name, county, status, tier, 
                            replacement_score, source_type, assigned_agent,
                            enrichment_data, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        lead_id, company_name, county, 'new', tier,
                        replacement_score, source_type,
                        'Miles', json.dumps(enrichment), datetime.now().isoformat()
                    ))
                    
                    imported += 1
                    
                    if imported % 100 == 0:
                        print(f"   Imported {imported}...")
                        
                except Exception as e:
                    continue
                    
    except Exception as e:
        print(f"   ⚠️ Error reading master clients: {e}")
    
    conn.commit()
    
    # Final count
    c.execute("SELECT COUNT(*) FROM leads")
    final_count = c.fetchone()[0]
    conn.close()
    
    print(f"\n" + "="*60)
    print(f"✅ MASTER CLIENTS IMPORT COMPLETE")
    print(f"="*60)
    print(f"   Total imported: {imported}")
    print(f"   Total skipped (duplicates): {skipped}")
    print(f"   Previous count: {existing}")
    print(f"   Final database count: {final_count}")

if __name__ == "__main__":
    import json
    import_master_clients()
