#!/usr/bin/env python3
"""
QUICK LEAD IMPORT - Restaurant leads only (46K records)
Fast import with batch commits
"""

import sqlite3
import csv
import uuid
import glob
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def import_restaurants_fast():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")  # Write-ahead logging for concurrency
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM leads")
    start_count = c.fetchone()[0]
    print(f"Starting lead count: {start_count:,}")
    
    restaurant_files = glob.glob("/root/.openclaw/workspace/AGI_COMPANY/data/restaurants/**/*.csv", recursive=True)
    print(f"\nFound {len(restaurant_files)} restaurant files")
    
    total_imported = 0
    total_skipped = 0
    batch = []
    batch_size = 500
    
    for csv_path in sorted(restaurant_files)[:5]:  # Process first 5 files only for testing
        region = Path(csv_path).stem.replace("_restaurants", "").replace("_20260428", "")[:30]
        print(f"\n📍 {region}...", end=" ")
        
        file_imported = 0
        file_skipped = 0
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    company = row.get('Company', '')
                    if not company:
                        continue
                    
                    city = row.get('City', '')
                    county = row.get('County', city)
                    priority = row.get('Priority', 'C')
                    
                    # Quick duplicate check
                    c.execute("SELECT 1 FROM leads WHERE company_name = ? AND enrichment_data LIKE ? LIMIT 1", 
                             (company, f'%"city": "{city}"%'))
                    if c.fetchone():
                        file_skipped += 1
                        continue
                    
                    lead_id = str(uuid.uuid4())
                    
                    enrichment = {
                        'company': company,
                        'city': city,
                        'county': county,
                        'state': row.get('State', 'CA'),
                        'priority': priority,
                        'business_type': row.get('Business Type', 'Restaurant'),
                        'industry': 'Restaurant',
                        'source_file': Path(csv_path).name
                    }
                    
                    score = 90 if priority == 'A' else (75 if priority == 'B' else 50)
                    
                    batch.append((
                        lead_id, company, county, 'new', f'Tier {priority}',
                        'Unknown', score, 'CA_Restaurant_Scraper',
                        'Miles', json.dumps(enrichment), datetime.now().isoformat()
                    ))
                    
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
        
        print(f"Imported: {file_imported} | Skipped: {file_skipped}")
        total_imported += file_imported
        total_skipped += file_skipped
    
    # Insert remaining batch
    if batch:
        c.executemany("""
            INSERT INTO leads (id, company_name, county, status, tier,
                pos_system, replacement_score, source_type,
                assigned_agent, enrichment_data, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, batch)
        conn.commit()
    
    c.execute("SELECT COUNT(*) FROM leads")
    end_count = c.fetchone()[0]
    conn.close()
    
    print(f"\n{'='*60}")
    print("RESTAURANT IMPORT COMPLETE")
    print(f"{'='*60}")
    print(f"Imported: {total_imported:,}")
    print(f"Skipped: {total_skipped:,}")
    print(f"Total leads: {end_count:,} (+{end_count - start_count:,})")

if __name__ == "__main__":
    import json
    import_restaurants_fast()
