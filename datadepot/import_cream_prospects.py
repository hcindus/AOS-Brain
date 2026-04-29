#!/usr/bin/env python3
"""
QUICK IMPORT - CREAM Realtors + Tiered Prospects
"""

import sqlite3
import csv
import uuid
import glob
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def import_cream_fast():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM leads")
    start = c.fetchone()[0]
    print(f"Starting: {start:,}")
    
    cream_files = glob.glob("/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/*.csv")
    print(f"Found {len(cream_files)} CREAM files")
    
    imported = 0
    skipped = 0
    batch = []
    
    for csv_path in sorted(cream_files):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = row.get('Company', '')
                if not company:
                    continue
                
                # Simple dedupe
                c.execute("SELECT 1 FROM leads WHERE company_name = ? LIMIT 1", (company,))
                if c.fetchone():
                    skipped += 1
                    continue
                
                tags = row.get('Tags', '')
                priority = 'A' if 'Priority_A' in tags else ('B' if 'Priority_B' in tags else 'C')
                
                enrichment = {
                    'company': company,
                    'city': row.get('City', ''),
                    'state': row.get('State', ''),
                    'priority': priority,
                    'industry': 'RealEstate',
                    'source': 'CREAM'
                }
                
                score = 90 if priority == 'A' else (70 if priority == 'B' else 50)
                
                batch.append((
                    str(uuid.uuid4()), company, row.get('City', 'Unknown'), 'new', 
                    f'Tier {priority}', 'Unknown', score, 'CREAM_RealEstate',
                    'Miles', json.dumps(enrichment), datetime.now().isoformat()
                ))
                
                imported += 1
                
                if len(batch) >= 500:
                    c.executemany("""
                        INSERT INTO leads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, batch)
                    conn.commit()
                    batch = []
    
    if batch:
        c.executemany("""INSERT INTO leads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", batch)
        conn.commit()
    
    c.execute("SELECT COUNT(*) FROM leads")
    end = c.fetchone()[0]
    conn.close()
    
    print(f"CREAM: +{imported:,} new, {skipped:,} dupes")
    print(f"Total: {end:,} (+{end - start:,})")

def import_prospects_fast():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM leads")
    start = c.fetchone()[0]
    print(f"\nStarting: {start:,}")
    
    tiers = [
        ('/root/.openclaw/workspace/sales/prospects_starter.csv', 'Tier 3'),
        ('/root/.openclaw/workspace/sales/prospects_professional.csv', 'Tier 2'),
        ('/root/.openclaw/workspace/sales/prospects_corporate.csv', 'Tier 1'),
        ('/root/.openclaw/workspace/sales/prospects_enterprise.csv', 'Tier 1'),
    ]
    
    imported = 0
    skipped = 0
    
    for path, tier in tiers:
        if not Path(path).exists():
            continue
        
        batch = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = row.get('Company', '') or row.get('company', '')
                if not company:
                    continue
                
                c.execute("SELECT 1 FROM leads WHERE company_name = ? LIMIT 1", (company,))
                if c.fetchone():
                    skipped += 1
                    continue
                
                enrichment = {
                    'company': company,
                    'contact': row.get('Contact', row.get('contact', '')),
                    'email': row.get('Email', row.get('email', '')),
                    'city': row.get('City', row.get('city', '')),
                    'tier_source': tier
                }
                
                score = 70 if 'Tier 1' in tier else 50
                
                batch.append((
                    str(uuid.uuid4()), company, row.get('City', 'Unknown') or 'Unknown', 
                    'new', tier, 'Unknown', score, 'Prospects_File',
                    'Miles', json.dumps(enrichment), datetime.now().isoformat()
                ))
                
                imported += 1
                
                if len(batch) >= 500:
                    c.executemany("""INSERT INTO leads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", batch)
                    conn.commit()
                    batch = []
        
        if batch:
            c.executemany("""INSERT INTO leads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", batch)
            conn.commit()
    
    c.execute("SELECT COUNT(*) FROM leads")
    end = c.fetchone()[0]
    conn.close()
    
    print(f"Prospects: +{imported:,} new, {skipped:,} dupes")
    print(f"Total: {end:,} (+{end - start:,})")

if __name__ == "__main__":
    import json
    import_cream_fast()
    import_prospects_fast()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM leads")
    final = c.fetchone()[0]
    c.execute("SELECT source_type, COUNT(*) FROM leads GROUP BY source_type ORDER BY COUNT(*) DESC")
    sources = c.fetchall()
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"✅ FINAL COUNT: {final:,} leads")
    print(f"{'='*60}")
    print("\nTop Sources:")
    for source, count in sources[:15]:
        print(f"  {source}: {count:,}")
