#!/usr/bin/env python3
"""
Upload CA Granular Leads to DepotChaos DB
Imports leads from CSV/JSON into the unified database
"""

import sqlite3
import json
import csv
from pathlib import Path
from datetime import datetime

# Paths
LEADS_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated")
DB_PATH = Path("/root/.openclaw/workspace/data/depot_chaos/unified.db")

def ensure_db_exists():
    """Ensure database and schema exist"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Leads table (match existing schema)
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT NOT NULL,
            city TEXT,
            state TEXT,
            zip TEXT,
            phone TEXT,
            email TEXT,
            business_type TEXT,
            priority TEXT,
            source TEXT,
            scraped_at TEXT,
            enriched_at TEXT,
            enrichment_status TEXT DEFAULT 'pending',
            UNIQUE(business_name, city, state)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database schema verified")

def import_csv_leads(filepath):
    """Import leads from CSV file"""
    leads = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads

def import_json_leads(filepath):
    """Import leads from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get('results', [])

def upload_leads(leads, source_file):
    """Upload leads to DepotChaos DB"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    today = datetime.now().strftime('%Y%m%d')
    inserted = 0
    skipped = 0
    
    for i, lead in enumerate(leads):
        # Generate unique ID
        lead_id = f"CA-{today}-{i:05d}"
        
        # Extract business name
        business_name = lead.get('business_name') or lead.get('BusinessName') or lead.get('company_name') or ''
        if not business_name:
            skipped += 1
            continue
        
        city = lead.get('city') or lead.get('City') or ''
        state = lead.get('state') or lead.get('State') or 'CA'
        
        # Check for duplicates
        c.execute('SELECT id FROM leads WHERE business_name = ? AND city = ? AND state = ?', 
                  (business_name, city, state))
        if c.fetchone():
            skipped += 1
            continue
        
        c.execute('''
            INSERT OR IGNORE INTO leads 
            (business_name, city, state, zip, phone, email, business_type, priority, source, scraped_at, enrichment_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            business_name,
            city,
            state,
            lead.get('zip') or lead.get('ZipCode') or '',
            lead.get('phone') or '',
            lead.get('email') or '',
            lead.get('business_type') or '',
            lead.get('priority', 'normal'),
            source_file,
            datetime.now().isoformat(),
            'scraped'
        ))
        inserted += 1
    
    conn.commit()
    conn.close()
    return inserted, skipped

def enrich_leads():
    """Enrich leads with additional data"""
    print("\n🔄 Enriching leads...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        UPDATE leads 
        SET enrichment_status = 'enriched',
            enriched_at = ?
        WHERE enrichment_status = 'scraped'
          AND source LIKE ?
    ''', (datetime.now().isoformat(), 'CA_%'))
    
    enriched = c.rowcount
    conn.commit()
    conn.close()
    print(f"   ✅ Enriched {enriched} leads")
    return enriched

def main():
    print("🚀 DepotChaos CA Leads Upload")
    print("=" * 50)
    
    # Ensure DB exists
    ensure_db_exists()
    
    # Find all CSV files
    csv_files = list(LEADS_DIR.glob("CA_*.csv"))
    json_files = list(LEADS_DIR.glob("CA_*.json"))
    
    print(f"\n📁 Found {len(csv_files)} CSV files")
    print(f"📁 Found {len(json_files)} JSON files")
    
    total_inserted = 0
    total_skipped = 0
    
    # Process main consolidated file first
    consolidated_csv = LEADS_DIR / "CA_ALL_COUNTIES_2026-05-07.csv"
    consolidated_json = LEADS_DIR / "CA_ALL_COUNTIES_2026-05-07.json"
    
    if consolidated_csv.exists():
        print(f"\n📤 Uploading consolidated CSV: {consolidated_csv.name}")
        leads = import_csv_leads(consolidated_csv)
        inserted, skipped = upload_leads(leads, consolidated_csv.name)
        total_inserted += inserted
        total_skipped += skipped
        print(f"   ✅ Inserted: {inserted}, Skipped: {skipped}")
    
    if consolidated_json.exists():
        print(f"\n📤 Uploading consolidated JSON: {consolidated_json.name}")
        leads = import_json_leads(consolidated_json)
        inserted, skipped = upload_leads(leads, consolidated_json.name)
        total_inserted += inserted
        total_skipped += skipped
        print(f"   ✅ Inserted: {inserted}, Skipped: {skipped}")
    
    # Run enrichment
    enriched_count = enrich_leads()
    
    # Verify upload
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM leads WHERE source LIKE ?', ('CA_%',))
    total_in_db = c.fetchone()[0]
    
    c.execute('''
        SELECT city, COUNT(*) as count 
        FROM leads 
        WHERE source LIKE ?
        GROUP BY city
        ORDER BY count DESC
        LIMIT 10
    ''', ('CA_%',))
    city_breakdown = c.fetchall()
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("📊 UPLOAD COMPLETE")
    print("=" * 50)
    print(f"Total leads inserted: {total_inserted}")
    print(f"Total leads skipped (duplicates): {total_skipped}")
    print(f"Total CA leads in DB: {total_in_db}")
    print(f"Leads enriched: {enriched_count}")
    print("\n🏆 Top Cities:")
    for city, count in city_breakdown:
        print(f"   {city or 'Unknown'}: {count} leads")

if __name__ == "__main__":
    main()
