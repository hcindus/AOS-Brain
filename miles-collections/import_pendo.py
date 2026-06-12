#!/usr/bin/env python3
"""
Excel Importer for Miles Collections Module
Reads pendo.xls/unpaids.xlsx and imports to collections system
"""

import json
import sys
from pathlib import Path

# Try to use openpyxl or xlsxreader
try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

DATA_DIR = Path("/root/.openclaw/workspace/miles-collections/data")
VENDOR_DIR = Path("/root/.openclaw/workspace/data/vendor_attachments")

def find_excel_files():
    """Find all Excel files with 'pendo' or 'unpaid' in name"""
    files = []
    if VENDOR_DIR.exists():
        for f in VENDOR_DIR.iterdir():
            if f.suffix in ['.xlsx', '.xls'] and ('pendo' in f.name.lower() or 'unpaid' in f.name.lower()):
                files.append(f)
    return sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)

def read_excel_pandas(filepath):
    """Read Excel using pandas"""
    try:
        df = pd.read_excel(filepath)
        return df.to_dict('records')
    except Exception as e:
        print(f"Pandas read error: {e}")
        return None

def read_excel_openpyxl(filepath):
    """Read Excel using openpyxl"""
    try:
        wb = openpyxl.load_workbook(filepath)
        sheet = wb.active
        
        # Get headers
        headers = []
        for cell in sheet[1]:
            headers.append(cell.value)
        
        # Get data
        records = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            record = {}
            for i, value in enumerate(row):
                if i < len(headers):
                    record[headers[i]] = value
            records.append(record)
        
        return records
    except Exception as e:
        print(f"Openpyxl read error: {e}")
        return None

def parse_records(records):
    """Parse records into collection account format"""
    accounts = []
    
    for record in records:
        if not record:
            continue
        
        # Debug: print record keys
        # print(f"Record keys: {list(record.keys())[:10]}")
            
        # Try to identify fields - handle various column naming
        name = None
        balance = 0
        days = 0
        
        for key, value in record.items():
            if not key:
                continue
            key_str = str(key).lower()
            
            # Pendo format: ACCOUNT, LOCATION, etc.
            if key_str in ['account', 'unnamed: 1'] or 'account' in key_str:
                if value and not pd.isna(value):
                    name = str(value)
            elif key_str in ['equip sale', 'unnamed: 8'] or 'sale' in key_str or 'balance' in key_str or 'amount' in key_str:
                try:
                    if value and not pd.isna(value):
                        val = float(str(value).replace('$', '').replace(',', ''))
                        if val > 0:
                            balance = val
                except:
                    pass
            elif 'days' in key_str or 'overdue' in key_str or 'age' in key_str:
                try:
                    if value and not pd.isna(value):
                        days = int(float(str(value).replace('days', '').strip()))
                except:
                    pass
        
        if name and balance > 0:
            accounts.append({
                'debtorName': str(name),
                'debtorEmail': 'pending@example.com',
                'debtorPhone': '000-000-0000',
                'balance': balance,
                'daysDelinquent': days,
                'invoiceRefs': [],
                'notes': 'Imported from Pendo'
            })
    
    return accounts

def save_to_collections(accounts):
    """Save accounts to Miles Collections JSON format"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    imported = 0
    for account in accounts:
        account_id = f"pendo_{imported:04d}_{hash(account['debtorName']) % 10000}"
        filepath = DATA_DIR / f"{account_id}.json"
        
        data = {
            'id': account_id,
            'debtor': {
                'name': account['debtorName'],
                'email': account['debtorEmail'],
                'phone': account['debtorPhone'],
                'address': ''
            },
            'originalBalance': account['balance'],
            'currentBalance': account['balance'],
            'daysDelinquent': account['daysDelinquent'],
            'invoiceRefs': account['invoiceRefs'],
            'status': 'active',
            'workflow': 'early_stage' if account['daysDelinquent'] < 30 else 'mid_stage',
            'priority': 'medium',
            'createdAt': pd.Timestamp.now().isoformat() if HAS_PANDAS else str(pd.Timestamp.now()),
            'lastActivity': pd.Timestamp.now().isoformat() if HAS_PANDAS else str(pd.Timestamp.now()),
            'communications': [],
            'payments': [],
            'notes': account.get('notes', '')
        }
        
        # Calculate priority
        score = (data['currentBalance'] * 0.6) + (data['daysDelinquent'] * 10)
        if score >= 5000:
            data['priority'] = 'critical'
        elif score >= 2000:
            data['priority'] = 'high'
        elif score >= 500:
            data['priority'] = 'medium'
        else:
            data['priority'] = 'low'
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        imported += 1
    
    return imported

def main():
    print("="*60)
    print("PENDO EXCEL IMPORTER")
    print("="*60)
    
    # Find files
    files = find_excel_files()
    if not files:
        print("No Excel files found matching 'pendo' or 'unpaid'")
        return
    
    print(f"\nFound {len(files)} Excel files:")
    for i, f in enumerate(files[:5], 1):
        size = f.stat().st_size / 1024
        print(f"  {i}. {f.name} ({size:.1f} KB)")
    
    # Read the most recent file
    target_file = files[0]
    print(f"\nReading: {target_file.name}")
    
    # Try to read
    records = None
    if HAS_PANDAS:
        print("Using pandas...")
        records = read_excel_pandas(target_file)
    
    if not records and HAS_OPENPYXL:
        print("Using openpyxl...")
        records = read_excel_openpyxl(target_file)
    
    if not records:
        print("ERROR: Cannot read Excel file. Install pandas or openpyxl:")
        print("  pip3 install pandas openpyxl")
        return
    
    print(f"\nRead {len(records)} rows")
    
    # Show sample
    if records:
        print("\nSample record:")
        print(str(records[0])[:500])
    
    # Parse and import
    accounts = parse_records(records)
    print(f"\nParsed {len(accounts)} valid collection accounts")
    
    if accounts:
        imported = save_to_collections(accounts)
        print(f"\n✅ Imported {imported} accounts to Miles Collections")
        print(f"   Location: {DATA_DIR}")
        
        # Show summary
        total_balance = sum(a['balance'] for a in accounts)
        print(f"\n   Total Balance: ${total_balance:,.2f}")
        print(f"   Avg Days Delinquent: {sum(a['daysDelinquent'] for a in accounts) / len(accounts):.0f}")
    else:
        print("\n⚠️ No valid accounts found to import")

if __name__ == '__main__':
    main()
