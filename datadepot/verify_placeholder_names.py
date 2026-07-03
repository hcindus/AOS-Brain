#!/usr/bin/env python3
"""
Verify placeholder business names in DepotChaos
Check against Whitepages/Yellow Pages
"""

import sqlite3
import re
import csv
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
REPORT_PATH = "/root/.openclaw/workspace/datadepot/data_verification_report.csv"

def find_suspicious_records():
    """Find records with placeholder names"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Pattern: names ending in numbers or starting with "20 "
    patterns = [
        "business_name LIKE '20 %'",
        "business_name LIKE 'Bar %'",
        "business_name LIKE 'Bistro %'", 
        "business_name LIKE 'Cafe %'",
        "business_name LIKE 'Coffee Shop%'",
        "business_name LIKE 'Diner %'",
        "business_name LIKE 'Restaurant %'",
        "business_name LIKE 'Taqueria %'",
        "business_name LIKE '% 1'",
        "business_name LIKE '% 2'",
        "business_name LIKE '% 3'",
        "business_name LIKE '% 4'",
        "business_name LIKE '% 5'",
        "business_name LIKE '% 6'",
        "business_name LIKE '% 7'",
        "business_name LIKE '% 8'",
        "business_name LIKE '% 9'",
        "business_name LIKE '% 10'",
    ]
    
    where_clause = " OR ".join(patterns)
    
    c.execute(f"""
        SELECT id, business_name, city, state, phone, address
        FROM leads 
        WHERE ({where_clause}) 
          AND (source_type IS NULL OR source_type = '')
        LIMIT 50
    """)
    
    records = c.fetchall()
    conn.close()
    
    return records

def analyze_records(records):
    """Analyze records and categorize them"""
    report = {
        'suspicious': [],
        'has_phone': [],
        'needs_verification': []
    }
    
    for rec in records:
        id_, name, city, state, phone, address = rec
        
        # Check if name looks like a placeholder
        is_placeholder = (
            re.match(r'^20\s+', name) or  # Starts with "20 "
            re.search(r'\s+\d+$', name) or  # Ends with number
            re.match(r'^(Bar|Bistro|Cafe|Coffee|Diner|Restaurant|Taqueria)\s+\d', name)
        )
        
        if is_placeholder:
            report['suspicious'].append({
                'id': id_,
                'name': name,
                'city': city,
                'state': state,
                'phone': phone,
                'address': address,
                'issue': 'placeholder_name'
            })
            
            if phone and len(phone) > 6:
                report['has_phone'].append({
                    'id': id_,
                    'name': name,
                    'city': city,
                    'state': state,
                    'phone': phone,
                    'address': address
                })
    
    return report

def generate_report(report):
    """Generate CSV report"""
    with open(REPORT_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'city', 'state', 'phone', 'address', 'issue', 'suggested_action'])
        writer.writeheader()
        
        for rec in report['suspicious']:
            action = 'VERIFY_PHONE' if rec['phone'] else 'DELETE'
            writer.writerow({
                'id': rec['id'],
                'name': rec['name'],
                'city': rec['city'],
                'state': rec['state'],
                'phone': rec['phone'],
                'address': rec['address'],
                'issue': rec['issue'],
                'suggested_action': action
            })
    
    return len(report['suspicious']), len(report['has_phone'])

def main():
    print("Finding suspicious records...")
    records = find_suspicious_records()
    
    print(f"Found {len(records)} potential placeholder records")
    
    if records:
        print("\nAnalyzing records...")
        report = analyze_records(records)
        
        total, with_phone = generate_report(report)
        
        print(f"\n=== VERIFICATION REPORT ===")
        print(f"Total suspicious records: {total}")
        print(f"Records with phone numbers: {with_phone}")
        print(f"Records without phone: {total - with_phone}")
        print(f"\nReport saved to: {REPORT_PATH}")
        
        print("\n--- Sample Records ---")
        for rec in report['suspicious'][:10]:
            phone_status = "HAS PHONE" if rec['phone'] else "NO PHONE"
            print(f"  [{rec['id']}] {rec['name']} ({rec['city']}, {rec['state']}) - {phone_status}")
        
        print("\n--- Recommendations ---")
        print(f"1. {with_phone} records need Whitepages/Yellow Pages verification")
        print(f"2. {total - with_phone} records can be safely deleted (no phone)")
        print("\nNext step: Manual verification or automated phone lookup")
    else:
        print("No suspicious records found")

if __name__ == "__main__":
    main()
