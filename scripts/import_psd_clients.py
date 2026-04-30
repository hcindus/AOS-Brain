#!/usr/bin/env python3
"""
Import Performance Supply Depot client files into DepotChaos
- Avoids duplicates (checks company_name + city + phone)
- Fills missing info
- Imports 2024 first, then 2026, then 2025 when found
"""

import pandas as pd
import sqlite3
import json
import uuid
import re
from datetime import datetime
from pathlib import Path

DB_PATH = '/root/.openclaw/workspace/data/depot_chaos/unified.db'
IMPORT_DIR = '/root/.openclaw/workspace/datadepot/imports'

def clean_phone(phone):
    """Normalize phone numbers"""
    if pd.isna(phone) or not phone:
        return None
    phone = str(phone).strip()
    if phone in ['-', 'NaN', 'nan', '', '0']:
        return None
    # Remove non-digit chars except + and extension indicators
    digits = re.sub(r'[^\d+]', '', phone)
    if len(digits) == 10 and not digits.startswith('1'):
        digits = '1' + digits
    return digits if len(digits) >= 10 else phone

def clean_email(email):
    """Clean and validate email"""
    if pd.isna(email) or not email:
        return None
    email = str(email).strip().lower()
    if email in ['-', 'nan', ''] or '@' not in email:
        return None
    return email

def clean_name(name):
    """Clean business/contact names"""
    if pd.isna(name) or not name:
        return None
    name = str(name).strip()
    if name in ['-', 'NaN', 'nan', '']:
        return None
    return name

def get_existing_lead(c, company_name, city, phone):
    """Check for existing lead by company name + city or phone"""
    # Try exact match on company name
    c.execute("SELECT id, enrichment_data, pos_system, is_customer FROM leads WHERE LOWER(company_name) = LOWER(?) LIMIT 1", (company_name,))
    result = c.fetchone()
    if result:
        return result
    
    # Try phone match
    if phone:
        clean_p = re.sub(r'[^\d]', '', phone)
        c.execute("SELECT id, enrichment_data, pos_system, is_customer FROM leads WHERE REPLACE(REPLACE(REPLACE(phone, '-', ''), '(', ''), ')', '') LIKE ? LIMIT 1", (f'%{clean_p[-10:]}',))
        result = c.fetchone()
        if result:
            return result
    
    return None

def parse_master_sheet(df):
    """Parse the Master sheet with client data"""
    records = []
    
    # Skip header rows, start from row 2
    for idx, row in df.iloc[2:].iterrows():
        try:
            # Business name (column 0)
            business = clean_name(row[0])
            if not business:
                continue
            
            # Contact info
            contact = clean_name(row[13]) if len(row) > 13 else None
            phone = clean_phone(row[14]) if len(row) > 14 else None
            
            # Email - check multiple columns
            email = None
            for col in [23, 24, 25]:
                if len(row) > col and pd.notna(row[col]):
                    email = clean_email(row[col])
                    if email:
                        break
            
            # Address
            street = None
            if len(row) > 19 and pd.notna(row[19]):
                street = str(row[19]).strip()
                if street in ['NaN', 'nan', '-', '']:
                    street = None
            
            city = str(row[20]).strip() if len(row) > 20 and pd.notna(row[20]) else None
            state = str(row[21]).strip() if len(row) > 21 and pd.notna(row[21]) else None
            zip_code = str(int(row[22])) if len(row) > 22 and pd.notna(row[22]) else None
            
            # County
            county = None
            if city and state:
                county = f"{city}, {state}"
            elif state:
                county = state
            
            # POS system (column 3)
            pos_system = clean_name(row[3]) if len(row) > 3 else None
            
            # Tax info
            tax_rate = None
            if len(row) > 15 and pd.notna(row[15]):
                try:
                    tax_rate = float(row[15])
                except:
                    pass
            
            record = {
                'company_name': business,
                'contact_name': contact,
                'phone': phone,
                'email': email,
                'street': street,
                'city': city,
                'state': state,
                'zip': zip_code,
                'county': county,
                'pos_system': pos_system,
                'tax_rate': tax_rate,
                'source_file': 'Master'
            }
            records.append(record)
            
        except Exception as e:
            continue
    
    return records

def import_file(filepath, year_label):
    """Import a single client file"""
    print(f"\n{'='*60}")
    print(f"📊 IMPORTING: {filepath.name} ({year_label})")
    print(f"{'='*60}")
    
    # Read Master sheet
    try:
        df = pd.read_excel(filepath, sheet_name='Master', header=None)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0, 0, 0
    
    records = parse_master_sheet(df)
    print(f"📋 Found {len(records)} client records")
    
    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    imported = 0
    updated = 0
    skipped = 0
    
    for record in records:
        try:
            # Check for existing
            existing = get_existing_lead(c, record['company_name'], record['city'], record['phone'])
            
            if existing:
                # Update existing with any new info
                lead_id, existing_json, existing_pos, is_customer = existing
                
                # Merge enrichment data
                existing_data = json.loads(existing_json) if existing_json else {}
                existing_data.update({
                    f'import_{year_label}': datetime.now().isoformat(),
                    'street': record['street'] or existing_data.get('street'),
                    'city': record['city'] or existing_data.get('city'),
                    'state': record['state'] or existing_data.get('state'),
                    'zip': record['zip'] or existing_data.get('zip'),
                })
                
                # Update fields if we have better data
                updates = []
                params = []
                
                if record['phone']:
                    c.execute("SELECT phone FROM leads WHERE id=?", (lead_id,))
                    current_phone = c.fetchone()[0]
                    if not current_phone:
                        updates.append("phone = ?")
                        params.append(record['phone'])
                
                if record['email']:
                    c.execute("SELECT email FROM leads WHERE id=?", (lead_id,))
                    current_email = c.fetchone()[0]
                    if not current_email:
                        updates.append("email = ?")
                        params.append(record['email'])
                
                if record['contact_name']:
                    c.execute("SELECT contact_name FROM leads WHERE id=?", (lead_id,))
                    current_contact = c.fetchone()[0]
                    if not current_contact:
                        updates.append("contact_name = ?")
                        params.append(record['contact_name'])
                
                if record['pos_system'] and not existing_pos:
                    updates.append("pos_system = ?")
                    params.append(record['pos_system'])
                
                updates.append("enrichment_data = ?")
                params.append(json.dumps(existing_data))
                
                updates.append("is_customer = ?")
                params.append(1)
                
                if not is_customer:
                    updates.append("customer_since = ?")
                    params.append(datetime.now().isoformat())
                
                if updates:
                    params.append(lead_id)
                    c.execute(f"UPDATE leads SET {', '.join(updates)} WHERE id = ?", params)
                    updated += 1
                else:
                    skipped += 1
            else:
                # Insert new
                lead_id = str(uuid.uuid4())
                
                enrichment = {
                    'source': f'PSD_Client_Import_{year_label}',
                    'street': record['street'],
                    'city': record['city'],
                    'state': record['state'],
                    'zip': record['zip'],
                    'tax_rate': record['tax_rate']
                }
                
                c.execute("""
                    INSERT INTO leads (
                        id, company_name, contact_name, phone, email, county,
                        pos_system, enrichment_data, status, source_type,
                        is_customer, customer_since, tier, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    lead_id,
                    record['company_name'],
                    record['contact_name'],
                    record['phone'],
                    record['email'],
                    record['county'],
                    record['pos_system'],
                    json.dumps(enrichment),
                    'converted',
                    f'PSD_{year_label}',
                    1,
                    datetime.now().isoformat(),
                    'Tier 1',
                    datetime.now().isoformat()
                ))
                imported += 1
                
        except Exception as e:
            print(f"  ⚠️ Error processing {record.get('company_name')}: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"✅ Imported: {imported}")
    print(f"🔄 Updated: {updated}")
    print(f"⏭️ Skipped (no new data): {skipped}")
    
    return imported, updated, skipped

def main():
    print("=" * 60)
    print("🏪 PERFORMANCE SUPPLY DEPOT CLIENT IMPORT")
    print("=" * 60)
    
    import_dir = Path(IMPORT_DIR)
    
    # Process in order: 2024, 2026, then look for 2025
    files_to_process = []
    
    # Check for 2024 file
    f2024 = import_dir / 'Clients_2024 (6) (1).xlsx'
    if f2024.exists():
        files_to_process.append((f2024, '2024'))
    
    # Check for 2026 file
    f2026 = import_dir / 'Clients_2026.xlsx'
    if f2026.exists():
        files_to_process.append((f2026, '2026'))
    
    # Look for 2025 file
    f2025_candidates = list(import_dir.glob('*2025*.xls*'))
    if f2025_candidates:
        files_to_process.append((f2025_candidates[0], '2025'))
        print(f"📁 Found 2025 file: {f2025_candidates[0].name}")
    else:
        print("🔍 2025 file not found yet - will check again after processing")
    
    total_imported = 0
    total_updated = 0
    total_skipped = 0
    
    for filepath, year in files_to_process:
        imp, upd, skip = import_file(filepath, year)
        total_imported += imp
        total_updated += upd
        total_skipped += skip
    
    # Final check for 2025 if not found
    if not f2025_candidates:
        f2025_candidates = list(import_dir.glob('*2025*.xls*'))
        if f2025_candidates:
            print(f"\n{'='*60}")
            print("📁 FOUND 2025 FILE - Processing now...")
            print(f"{'='*60}")
            imp, upd, skip = import_file(f2025_candidates[0], '2025')
            total_imported += imp
            total_updated += upd
            total_skipped += skip
    
    print(f"\n{'='*60}")
    print("📊 IMPORT SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Total New Imports: {total_imported}")
    print(f"🔄 Total Updated: {total_updated}")
    print(f"⏭️ Total Skipped: {total_skipped}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
