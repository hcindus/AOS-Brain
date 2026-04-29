#!/usr/bin/env python3
"""
Import Master Client List from Clients_2025.xlsx into DepotChaos CRM
Extracts customers from the 'Master' sheet and writes directly to database
"""

import pandas as pd
import sqlite3
import uuid
from datetime import datetime
import sys

# Database path
DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

# Column indices from the Master sheet
COL_COMPANY = 0
COL_SYSTEM = 1
COL_CONTACT = 13
COL_PHONE = 14
COL_STREET = 19
COL_CITY = 20
COL_STATE = 21
COL_ZIP = 22

def parse_phone(phone):
    """Normalize phone number"""
    if pd.isna(phone):
        return None
    phone = str(phone).strip()
    return phone if phone and phone.lower() != 'nan' else None

def import_clients():
    file_path = '/root/.openclaw/workspace/aocros/agents/crypto-financial/Clients_2025 (3).xlsx'
    
    print(f"📊 Loading Master sheet from {file_path}...")
    df = pd.read_excel(file_path, sheet_name='Master', header=1)
    
    # Clean records - keep rows where company name exists
    df_clean = df[df.iloc[:, COL_COMPANY].notna()].copy()
    
    print(f"✅ Found {len(df_clean)} records to process\n")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Count existing
    c.execute("SELECT COUNT(*) FROM leads WHERE source_type = 'master_client_list_2025'")
    existing_clients = c.fetchone()[0]
    print(f"ℹ️  Existing clients from this source: {existing_clients}")
    
    imported = 0
    skipped = 0
    errors = 0
    
    for idx, row in df_clean.iterrows():
        try:
            # Extract fields
            company_name = str(row.iloc[COL_COMPANY]).strip()
            system_type = str(row.iloc[COL_SYSTEM]).strip() if pd.notna(row.iloc[COL_SYSTEM]) else "Unknown"
            
            # Skip header-like rows or invalid entries
            if not company_name or company_name.lower() in ['nan', 'none', '', 'store', 'company', 'name']:
                skipped += 1
                continue
            
            contact_name = str(row.iloc[COL_CONTACT]).strip() if pd.notna(row.iloc[COL_CONTACT]) else None
            phone = parse_phone(row.iloc[COL_PHONE])
            
            street = str(row.iloc[COL_STREET]).strip() if pd.notna(row.iloc[COL_STREET]) else None
            city = str(row.iloc[COL_CITY]).strip() if pd.notna(row.iloc[COL_CITY]) else None
            state = str(row.iloc[COL_STATE]).strip() if pd.notna(row.iloc[COL_STATE]) else None
            
            # Handle ZIP (may be float)
            zip_val = row.iloc[COL_ZIP]
            zip_code = None
            if pd.notna(zip_val):
                if isinstance(zip_val, (int, float)):
                    zip_code = str(int(zip_val))
                else:
                    zip_code = str(zip_val).strip().replace('.0', '')
            
            # Build county/location string
            county = None
            if city and state:
                county = f"{city}, {state}"
            elif state:
                county = state
            
            # Check if company already exists (by name)
            c.execute("SELECT id FROM leads WHERE company_name = ? AND source_type = 'master_client_list_2025'", 
                     (company_name,))
            if c.fetchone():
                skipped += 1
                continue
            
            # Determine tier based on system type
            system_upper = system_type.upper()
            if any(x in system_upper for x in ['CASIO', 'ECR', 'SAM4S', 'LP-1000', 'QT-6600', 'TE7000', 'SAP-630', 'ER260', 'ER945']):
                tier = "Tier 1"  # Has POS system
            elif 'SUPPLY ONLY' in system_upper:
                tier = "Tier 2"  # Just supplies
            elif 'SCALE' in system_upper:
                tier = "Tier 2"
            else:
                tier = "Tier 2"
            
            # Build enrichment data
            enrichment = {
                'contact_name': contact_name,
                'phone': phone,
                'street': street,
                'city': city,
                'state': state,
                'zip': zip_code,
                'system_type': system_type,
                'imported_from': 'Clients_2025.xlsx Master sheet'
            }
            
            # Generate UUID
            lead_id = str(uuid.uuid4())
            
            # Insert lead
            c.execute("""
                INSERT INTO leads (
                    id, company_name, county, status, tier, 
                    pos_system, replacement_score, source_type,
                    assigned_agent, enrichment_data, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lead_id,
                company_name,
                county,
                'new',
                tier,
                system_type,
                75 if tier == "Tier 1" else 50,  # Replacement score
                'master_client_list_2025',
                None,  # assigned_agent
                json.dumps(enrichment),
                datetime.now().isoformat()
            ))
            
            imported += 1
            if imported % 100 == 0:
                print(f"  ✅ Imported {imported}/{len(df_clean)}...")
                conn.commit()  # Periodic commit
                
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"  ⚠️  Error on row {idx}: {e}")
            continue
    
    # Final commit
    conn.commit()
    
    # Get final count
    c.execute("SELECT COUNT(*) FROM leads")
    total_leads = c.fetchone()[0]
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"📊 IMPORT SUMMARY")
    print(f"{'='*50}")
    print(f"✅ Successfully imported: {imported}")
    print(f"⚠️  Errors:              {errors}")
    print(f"⏭️  Skipped/duplicates:  {skipped}")
    print(f"📋 Total in database:    {total_leads:,}")
    
    return imported

if __name__ == "__main__":
    import json
    count = import_clients()
    sys.exit(0 if count > 0 else 1)
