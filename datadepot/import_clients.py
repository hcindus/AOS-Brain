#!/usr/bin/env python3
"""
Import Master Client List from Clients_2025.xlsx into DepotChaos CRM
Extracts customers from the 'Master' sheet and imports via FastAPI
"""

import pandas as pd
import requests
import json
from datetime import datetime
import sys

# API Configuration
API_BASE = "http://localhost:8082"

def parse_phone(phone):
    """Normalize phone number"""
    if pd.isna(phone):
        return None
    phone = str(phone).strip()
    # Remove non-numeric except dashes and parens
    return phone if phone else None

def extract_state_from_zip(city_st_zip):
    """Extract state from city/st/zip string"""
    if pd.isna(city_st_zip):
        return None
    parts = str(city_st_zip).split(',')
    if len(parts) >= 2:
        st_zip = parts[-1].strip().split()
        if st_zip:
            return st_zip[0]
    return None

def import_clients():
    file_path = '/root/.openclaw/workspace/aocros/agents/crypto-financial/Clients_2025 (3).xlsx'
    
    print(f"📊 Loading Master sheet from {file_path}...")
    df = pd.read_excel(file_path, sheet_name='Master', header=1)
    
    # Clean records - keep rows where company name exists (column 0)
    df_clean = df[df.iloc[:, 0].notna()].copy()
    
    print(f"✅ Found {len(df_clean)} records to process")
    
    # Column mappings based on analysis
    records = []
    skipped = 0
    imported = 0
    errors = 0
    
    for idx, row in df_clean.iterrows():
        try:
            # Extract fields
            company_name = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else None
            system_type = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "Unknown"
            
            # Contact info (columns vary, use named columns if available)
            contact_name = None
            phone = None
            email = None
            
            # Try to find contact info in various columns
            for col in df.columns:
                col_str = str(col).lower()
                if 'phone' in col_str and pd.notna(row[col]):
                    phone = parse_phone(row[col])
                if 'email' in col_str and pd.notna(row[col]):
                    email = str(row[col]).strip()
                if 'contact' in col_str and 'name' in col_str and pd.notna(row[col]):
                    contact_name = str(row[col]).strip()
            
            # Address fields
            street = None
            city = None
            state = None
            zip_code = None
            
            for col in df.columns:
                col_str = str(col).upper()
                if col_str == 'STREET' and pd.notna(row[col]):
                    street = str(row[col]).strip()
                if col_str == 'CITY' and pd.notna(row[col]):
                    city = str(row[col]).strip()
                if col_str == 'ST' and pd.notna(row[col]):
                    state = str(row[col]).strip()
                if col_str == 'ZIP' and pd.notna(row[col]):
                    zip_val = row[col]
                    zip_code = str(int(zip_val)) if isinstance(zip_val, (int, float)) else str(zip_val).strip()
            
            # Skip if no company name
            if not company_name or company_name.lower() in ['nan', 'none', '']:
                skipped += 1
                continue
            
            # Build county string
            county = None
            if city and state:
                county = f"{city}, {state}"
            elif state:
                county = state
            
            # Determine tier based on system type
            tier = "Tier 2"  # Default
            if 'casio' in system_type.lower():
                tier = "Tier 1"  # POS system installed
            elif 'ecr' in system_type.lower():
                tier = "Tier 1"  # Electronic cash register
            elif 'supply only' in system_type.lower():
                tier = "Tier 2"  # Just supplies, no POS
            
            # Determine status
            status = "new"
            if system_type and system_type != 'Unknown':
                status = "contacted"  # Existing customer
            
            # Build lead record
            lead = {
                "company_name": company_name,
                "contact_name": contact_name,
                "email": email,
                "phone": phone,
                "street": street,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "county": county,
                "status": status,
                "tier": tier,
                "pos_system": system_type,
                "source": "master_client_list",
                "imported_at": datetime.utcnow().isoformat()
            }
            
            # Import via API
            try:
                resp = requests.post(
                    f"{API_BASE}/leads",
                    json=lead,
                    timeout=10
                )
                if resp.status_code in [200, 201]:
                    imported += 1
                    if imported % 50 == 0:
                        print(f"  📝 Imported {imported}...")
                else:
                    errors += 1
                    print(f"  ⚠️ Error importing {company_name}: {resp.status_code}")
            except Exception as e:
                errors += 1
                print(f"  ⚠️ API error for {company_name}: {e}")
                
        except Exception as e:
            skipped += 1
            print(f"  ⚠️ Parse error row {idx}: {e}")
            continue
    
    print(f"\n📊 IMPORT SUMMARY")
    print(f"=" * 40)
    print(f"✅ Successfully imported: {imported}")
    print(f"⚠️  Errors: {errors}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"📋 Total processed: {imported + errors + skipped}")
    
    return imported

if __name__ == "__main__":
    count = import_clients()
    sys.exit(0 if count > 0 else 1)
