#!/usr/bin/env python3
"""
COMPLETE RESTAURANT IMPORT - All 46K+ restaurant leads
"""

import sqlite3
import csv
import uuid
import glob
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def import_all_restaurants():
    conn = sqlite3.connect(DB_PATH, timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")  # Faster commits
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM leads")
    start = c.fetchone()[0]
    print(f"Starting: {start:,} leads")
    
    # Get all restaurant files
    restaurant_files = glob.glob("/root/.openclaw/workspace/AGI_COMPANY/data/restaurants/**/*.csv", recursive=True)
    print(f"Found {len(restaurant_files)} restaurant files")
    
    imported = 0
    skipped = 0
    batch = []
    batch_size = 1000
    
    for i, csv_path in enumerate(sorted(restaurant_files), 1):
        region = Path(csv_path).stem.replace("_restaurants", "").replace("_20260428", "").replace("_0340", "").replace("_0344", "")[:40]
        print(f"[{i}/{len(restaurant_files)}] {region}...", end=" ", flush=True)
        
        file_imported = 0
        file_skipped = 0
        
        try:
            with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    company = row.get('Company', '')
                    if not company:
                        continue
                    
                    city = row.get('City', '')
                    
                    # Quick duplicate check using company name only
                    c.execute("SELECT 1 FROM leads WHERE company_name = ? LIMIT 1", (company,))
                    if c.fetchone():
                        skipped += 1
                        file_skipped += 1
                        continue
                    
                    county = row.get('County', city) or city
                    priority = row.get('Priority', 'C')
                    state = row.get('State', 'CA')
                    
                    # Build minimal enrichment
                    enrichment = {
                        'company': company,
                        'city': city,
                        'county': county,
                        'state': state,
                        'priority': priority,
                        'business_type': row.get('Business Type', 'Restaurant'),
                        'industry': 'Restaurant'
                    }
                    
                    score = 90 if priority == 'A' else (75 if priority == 'B' else 50)
                    
                    batch.append((
                        str(uuid.uuid4()), company, county, 'new', f'Tier {priority}',
                        'Unknown', score, 'CA_Restaurant_Scraper',
                        'Miles', json.dumps(enrichment), datetime.now().isoformat()
                    ))
                    
                    imported += 1
                    file_imported += 1
                    
                    if len(batch) >= batch_size:
                        c.executemany("""
                            INSERT INTO leads (id, company_name, county, status, tier,
                                pos_system, replacement_score, source_type,
                                assigned_agent, enrichment_data, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, batch)
                        conn.commit()
                        batch = []
                        
        except Exception as e:
            print(f"Error: {e}")
        
        print(f"+{file_imported} (skipped {file_skipped})")
        
        # Progress update every 10 files
        if i % 10 == 0:
            print(f"  → Progress: {imported:,} imported, {skipped:,} skipped")
    
    # Insert remaining
    if batch:
        c.executemany("""
            INSERT INTO leads (id, company_name, county, status, tier,
                pos_system, replacement_score, source_type,
                assigned_agent, enrichment_data, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, batch)
        conn.commit()
    
    c.execute("SELECT COUNT(*) FROM leads")
    end = c.fetchone()[0]
    conn.close()
    
    print(f"\n{'='*60}")
    print("RESTAURANT IMPORT COMPLETE")
    print(f"{'='*60}")
    print(f"New restaurants: {imported:,}")
    print(f"Duplicates skipped: {skipped:,}")
    print(f"Total leads now: {end:,} (+{end - start:,})")

if __name__ == "__main__":
    import json
    import_all_restaurants()
