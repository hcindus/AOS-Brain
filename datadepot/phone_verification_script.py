#!/usr/bin/env python3
"""
Verify phone numbers and enrich with emails
Uses Google Places API or alternative sources
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def get_records_needing_verification():
    """Get records with placeholder names that have phones"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, business_name, city, state, phone, address
        FROM leads 
        WHERE (business_name LIKE '20 %' OR business_name LIKE 'Bar %' OR business_name LIKE 'Bistro %' 
               OR business_name LIKE 'Cafe %' OR business_name LIKE 'Coffee Shop%' OR business_name LIKE 'Diner %' 
               OR business_name LIKE 'Restaurant %' OR business_name LIKE 'Taqueria %')
          AND phone IS NOT NULL 
          AND phone != ''
          AND (deleted = 0 OR deleted IS NULL)
        LIMIT 100
    """)
    
    records = c.fetchall()
    conn.close()
    return records

def find_duplicates():
    """Find potential duplicate records"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT business_name, city, state, COUNT(*) as count,
               GROUP_CONCAT(id) as ids,
               GROUP_CONCAT(phone) as phones
        FROM leads 
        WHERE (deleted = 0 OR deleted IS NULL)
        GROUP BY business_name, city, state 
        HAVING count > 1
        ORDER BY count DESC
        LIMIT 50
    """)
    
    duplicates = c.fetchall()
    conn.close()
    return duplicates

def generate_verification_report(records, duplicates):
    """Generate report for Patricia"""
    report_path = "/root/.openclaw/workspace/datadepot/phone_verification_queue.csv"
    
    with open(report_path, 'w') as f:
        f.write("id,business_name,city,state,phone,address,verification_status,real_name,email\n")
        for rec in records:
            id_, name, city, state, phone, address = rec
            f.write(f'{id_},"{name}",{city},{state},{phone},"{address}",PENDING,,\n')
    
    dup_report_path = "/root/.openclaw/workspace/datadepot/duplicate_report.csv"
    with open(dup_report_path, 'w') as f:
        f.write("business_name,city,state,count,ids,phones,recommended_action\n")
        for dup in duplicates:
            name, city, state, count, ids, phones = dup
            action = "MERGE" if count == 2 else "REVIEW"
            f.write(f'"{name}",{city},{state},{count},"{ids}","{phones}",{action}\n')
    
    return len(records), len(duplicates)

def main():
    print("Finding records needing phone verification...")
    records = get_records_needing_verification()
    
    print("Finding duplicates...")
    duplicates = find_duplicates()
    
    phone_count, dup_count = generate_verification_report(records, duplicates)
    
    print(f"\n=== PHONE VERIFICATION QUEUE ===")
    print(f"Records with phones needing verification: {phone_count}")
    print(f"Duplicate groups found: {dup_count}")
    
    print(f"\nReports generated:")
    print(f"  - Phone verification: /root/.openclaw/workspace/datadepot/phone_verification_queue.csv")
    print(f"  - Duplicates: /root/.openclaw/workspace/datadepot/duplicate_report.csv")
    
    if records:
        print("\n--- Sample Records to Verify ---")
        for rec in records[:5]:
            id_, name, city, state, phone, address = rec
            print(f"  [{id_}] {name} | {phone} | {city}, {state}")
    
    if duplicates:
        print("\n--- Duplicate Groups ---")
        for dup in duplicates[:5]:
            name, city, state, count, ids, phones = dup
            print(f"  {name} ({city}, {state}): {count} records")

if __name__ == "__main__":
    main()
