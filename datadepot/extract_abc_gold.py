#!/usr/bin/env python3
"""
Extract real gold from ABC Daily Export
Filter for PSDEPOT target businesses
"""

import csv
import sqlite3
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
CSV_PATH = "/root/.openclaw/workspace/datadepot/data/ABC-DailyDataExport.csv"

# Target counties
TARGET_COUNTIES = ['SACRAMENTO', 'PLACER', 'YOLO', 'SONOMA', 'NAPA', 'SOLANO']

# License types for PSDEPOT (receipt users)
# 41 = On-Sale Beer & Eating (restaurants)
# 42 = On-Sale Beer (bars/taverns)
# 47 = On-Sale Beer/Wine (restaurants/bars)
# 48 = On-Sale Beer/Wine (bar/tavern)
# 40 = On-Sale Beer (bar/tavern)
# 75 = Special Event Permit
GOOD_LICENSE_TYPES = ['41', '42', '47', '48', '40', '20']

def is_psdepot_target(name, dba):
    """Check if business is a PSDEPOT target (restaurant, bar, etc.)"""
    full_name = f"{name} {dba}".lower()
    
    # Receipt users
    keywords = [
        'restaurant', 'cafe', 'bar', 'tavern', 'grill', 'kitchen', 'eats',
        'dining', 'lounge', 'pub', 'sports', 'wings', 'pizza', 'burger',
        'taco', 'thai', 'indian', 'chinese', 'sushi', 'pho', 'vietnamese',
        'korean', 'japanese', 'asian', 'mexican', 'deli', 'sandwich',
        'liquor', 'market', 'mini mart', 'store', 'wine', 'winery',
        'golf', 'club', 'arcade'
    ]
    
    return any(kw in full_name for kw in keywords)

def extract_gold():
    """Extract real businesses from ABC data"""
    
    print("🪙 Panning for ABC Gold...")
    
    # Read CSV
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        next(f)  # Skip timestamp line
        reader = csv.DictReader(f)
        records = list(reader)
    
    print(f"Total ABC records: {len(records)}")
    
    # Filter for target counties and good businesses
    gold = []
    
    for r in records:
        county = r.get('Prem County', '').strip().upper()
        license_type = r.get('License Type', '').strip()
        status = r.get('Type Status', '').strip()
        
        # Skip if not target county
        if county not in TARGET_COUNTIES:
            continue
        
        # Skip if not active
        if status != 'ACTIVE':
            continue
        
        # Get business name
        dba = r.get('DBA Name', '').strip().strip('"')
        primary = r.get('Primary Name', '').strip().strip('"')
        name = dba if dba and dba not in ['', ' ', '" "'] else primary
        
        if not name or len(name) < 3:
            continue
        
        # Check if it's a PSDEPOT target
        if is_psdepot_target(name, dba):
            gold.append({
                'name': name,
                'dba': dba,
                'primary': primary,
                'city': r.get('Prem City', '').strip(),
                'county': county.title(),
                'state': r.get(' Prem State', '').strip() or 'CA',
                'zip': r.get('Prem Zip', '').strip(),
                'address': r.get('Prem Addr 1', '').strip().strip('"'),
                'license_type': license_type,
                'license_num': r.get('File Number', '').strip(),
                'expiry': r.get('Expir Date', '').strip()
            })
    
    print(f"Gold found: {len(gold)} real businesses")
    
    # Sort by county
    gold.sort(key=lambda x: (x['county'], x['city'], x['name']))
    
    return gold

def save_to_csv(gold):
    """Save gold to CSV"""
    output_path = "/root/.openclaw/workspace/datadepot/abc_real_gold.csv"
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'dba', 'primary', 'city', 'county', 'state', 'zip', 'address', 'license_type', 'license_num', 'expiry'])
        writer.writeheader()
        writer.writerows(gold)
    
    print(f"\n💾 Saved to: {output_path}")
    return output_path

def import_to_depotchaos(gold):
    """Import gold to DepotChaos"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    imported = 0
    skipped = 0
    
    for business in gold:
        # Check if exists
        c.execute("SELECT id FROM leads WHERE business_name = ? AND city = ?", 
                  (business['name'], business['city']))
        if c.fetchone():
            skipped += 1
            continue
        
        # Determine category
        name_lower = business['name'].lower()
        if 'taco' in name_lower or 'mexican' in name_lower:
            category = 'Mexican Restaurant'
        elif 'thai' in name_lower or 'asian' in name_lower:
            category = 'Asian Restaurant'
        elif 'bar' in name_lower or 'tavern' in name_lower or 'lounge' in name_lower:
            category = 'Bar'
        elif 'restaurant' in name_lower or 'cafe' in name_lower or 'eats' in name_lower:
            category = 'Restaurant'
        else:
            category = 'Food Service'
        
        enrichment = {
            'source': 'ABC_Daily_Export',
            'license_type': business['license_type'],
            'license_number': business['license_num'],
            'expiry': business['expiry'],
            'dba': business['dba'],
            'primary_name': business['primary'],
            'imported_at': datetime.now().isoformat()
        }
        
        c.execute("""
            INSERT INTO leads (
                business_name, city, state, zip, address,
                business_type, category, source_type, created_at, tags,
                enrichment_data, enrichment_status, status, deleted
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'ABC License Data', datetime('now'), 'abc_gold,prospect',
                     ?, 'enriched', 'new', 0)
        """, (
            business['name'],
            business['city'],
            business['state'],
            business['zip'],
            business['address'],
            category,
            category,
            str(enrichment)
        ))
        
        imported += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Import Complete:")
    print(f"  Imported: {imported}")
    print(f"  Skipped (duplicates): {skipped}")
    
    return imported

def show_summary(gold):
    """Show summary by county"""
    from collections import Counter
    
    counties = Counter([b['county'] for b in gold])
    
    print("\n--- Gold by County ---")
    for county, count in counties.most_common():
        print(f"  {county}: {count}")
    
    print("\n--- Sample Real Gold ---")
    for b in gold[:15]:
        print(f"  {b['name'][:40]:<40} | {b['city']:<15} | {b['county']:<12}")

if __name__ == "__main__":
    gold = extract_gold()
    
    if gold:
        show_summary(gold)
        save_to_csv(gold)
        
        print("\nImport to DepotChaos? (y/n): ", end='')
        # Auto-import for now
        import_to_depotchaos(gold)
    else:
        print("No gold found!")
