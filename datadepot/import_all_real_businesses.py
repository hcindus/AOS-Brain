#!/usr/bin/env python3
"""
Import all real businesses from various tables
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def import_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("=" * 70)
    print("🚀 IMPORTING ALL REAL BUSINESSES")
    print("=" * 70)
    
    total_imported = 0
    
    # 1. From ca_abc_licenses (raw table)
    print("\n1️⃣ From ca_abc_licenses table...")
    c.execute("""
        SELECT business_name, owner_name, address, city, state, zip, county, phone
        FROM ca_abc_licenses
        WHERE business_name IS NOT NULL 
          AND business_name != ''
          AND county IN ('Sacramento', 'Placer', 'Yolo', 'Sonoma', 'Napa', 'Solano')
        LIMIT 10000
    """)
    
    abc_records = c.fetchall()
    imported = 0
    for name, owner, addr, city, state, zip_, county, phone in abc_records:
        enrichment = json.dumps({
            'source': 'ca_abc_licenses_raw',
            'owner_name': owner,
            'imported_at': datetime.now().isoformat()
        })
        
        try:
            c.execute("""
                INSERT OR IGNORE INTO leads
                (business_name, city, state, zip, county, phone, address,
                 source_type, created_at, tags, enrichment_data, status, deleted)
                VALUES (?, ?, COALESCE(?, 'CA'), ?, ?, ?, ?, 'CA_ABC_Raw',
                       datetime('now'), 'abc_raw,prospect', ?, 'new', 0)
            """, (name, city, state, zip_, county, phone, addr, enrichment))
            if c.rowcount > 0:
                imported += 1
        except:
            pass
    
    print(f"   Imported: {imported}")
    total_imported += imported
    
    # 2. From datadepot_intelligence
    print("\n2️⃣ From datadepot_intelligence...")
    c.execute("""
        SELECT business_name, city, state, zip, county, phone, 
               license_number, pos_system, replacement_score
        FROM datadepot_intelligence
        WHERE business_name IS NOT NULL
          AND business_name != ''
          AND county IN ('Sacramento', 'Placer', 'Yolo', 'Sonoma', 'Napa', 'Solano')
        LIMIT 10000
    """)
    
    dd_records = c.fetchall()
    imported = 0
    for name, city, state, zip_, county, phone, lic, pos, score in dd_records:
        enrichment = json.dumps({
            'source': 'datadepot_intelligence',
            'license_number': lic,
            'pos_system': pos,
            'replacement_score': score,
            'imported_at': datetime.now().isoformat()
        })
        
        try:
            c.execute("""
                INSERT OR IGNORE INTO leads
                (business_name, city, state, zip, county, phone,
                 pos_system, replacement_score, source_type, created_at, 
                 tags, enrichment_data, status, deleted)
                VALUES (?, ?, COALESCE(?, 'CA'), ?, ?, ?, ?, ?,
                       'DataDepot_Intel', datetime('now'), 'datadepot,prospect',
                       ?, 'new', 0)
            """, (name, city, state, zip_, county, phone, pos, score, enrichment))
            if c.rowcount > 0:
                imported += 1
        except:
            pass
    
    print(f"   Imported: {imported}")
    total_imported += imported
    
    # 3. From unified_leads
    print("\n3️⃣ From unified_leads...")
    c.execute("""
        SELECT business_name, business_type, owner_name, address, city, state, zip, county,
               phone, email, website
        FROM unified_leads
        WHERE business_name IS NOT NULL
          AND business_name != ''
        LIMIT 5000
    """)
    
    unified_records = c.fetchall()
    imported = 0
    for row in unified_records:
        name, biz_type, owner, addr, city, state, zip_, county, phone, email, website = row
        
        enrichment = json.dumps({
            'source': 'unified_leads',
            'owner_name': owner,
            'website': website,
            'imported_at': datetime.now().isoformat()
        })
        
        try:
            c.execute("""
                INSERT OR IGNORE INTO leads
                (business_name, business_type, city, state, zip, county, 
                 phone, email, address, source_type, created_at, 
                 tags, enrichment_data, status, deleted)
                VALUES (?, ?, ?, COALESCE(?, 'CA'), ?, ?, ?, ?, ?,
                       'Unified_Leads', datetime('now'), 'unified,prospect',
                       ?, 'new', 0)
            """, (name, biz_type, city, state, zip_, county, phone, email, addr, enrichment))
            if c.rowcount > 0:
                imported += 1
        except Exception as e:
            pass
    
    print(f"   Imported: {imported}")
    total_imported += imported
    
    # Get new totals
    conn.commit()
    
    print("\n--- Verification ---")
    c.execute("""
        SELECT COUNT(*) FROM leads 
        WHERE (deleted = 0 OR deleted IS NULL)
        AND county IN ('Sacramento', 'Placer', 'Yolo', 'Sonoma', 'Napa', 'Solano')
    """)
    target_total = c.fetchone()[0]
    
    c.execute("""
        SELECT source_type, COUNT(*) 
        FROM leads 
        WHERE (deleted = 0 OR deleted IS NULL)
        AND county IN ('Sacramento', 'Placer', 'Yolo', 'Sonoma', 'Napa', 'Solano')
        GROUP BY source_type
        ORDER BY COUNT(*) DESC
    """)
    
    print(f"\nTarget counties total: {target_total}")
    print("\nBy source:")
    for source, count in c.fetchall():
        print(f"  {source or 'N/A':<35} | {count}")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print(f"✅ IMPORT COMPLETE: {total_imported} new records")
    print("=" * 70)

if __name__ == "__main__":
    import_all()
