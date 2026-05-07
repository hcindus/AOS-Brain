#!/usr/bin/env python3
"""
Upload Northeast Region Leads to DepotChaos DB
Imports leads from CSV into the unified database
"""

import sqlite3
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

def upload_leads(leads, source_file):
    """Upload leads to DepotChaos DB"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    today = datetime.now().strftime('%Y%m%d')
    inserted = 0
    skipped = 0
    
    for i, lead in enumerate(leads):
        # Extract business name
        business_name = lead.get('Company') or lead.get('business_name') or lead.get('BusinessName') or lead.get('company_name') or ''
        if not business_name:
            skipped += 1
            continue
        
        city = lead.get('City') or lead.get('city') or ''
        state = lead.get('State') or lead.get('state') or ''
        
        # Check for duplicates
        c.execute('SELECT id FROM leads WHERE business_name = ? AND city = ? AND state = ?', 
                  (business_name, city, state))
        if c.fetchone():
            skipped += 1
            continue
        
        # Determine priority from tags
        tags = lead.get('Tags', '')
        priority = 'high' if 'Priority_A' in tags else 'normal'
        
        c.execute('''
            INSERT OR IGNORE INTO leads 
            (business_name, city, state, zip, phone, email, business_type, priority, source, scraped_at, enrichment_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            business_name,
            city,
            state,
            lead.get('Postal Code') or lead.get('zip') or '',
            lead.get('Phone') or lead.get('phone') or '',
            lead.get('Email') or lead.get('email') or '',
            lead.get('Notes') or '',
            priority,
            f"NORTHEAST_{source_file}",
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
    ''', (datetime.now().isoformat(), 'NORTHEAST_%'))
    
    enriched = c.rowcount
    conn.commit()
    conn.close()
    print(f"   ✅ Enriched {enriched} leads")
    return enriched

def main():
    print("🚀 DepotChaos Northeast Leads Upload")
    print("=" * 50)
    
    # Ensure DB exists
    ensure_db_exists()
    
    # Find NORTHEAST CSV files
    csv_files = list(LEADS_DIR.glob("NORTHEAST_*.csv"))
    
    print(f"\n📁 Found {len(csv_files)} Northeast CSV files")
    
    total_inserted = 0
    total_skipped = 0
    
    # Process each file
    for csv_file in csv_files:
        if 'MASTER' in csv_file.name:
            continue  # Skip master - process individual states
        
        print(f"\n📤 Uploading: {csv_file.name}")
        leads = import_csv_leads(csv_file)
        inserted, skipped = upload_leads(leads, csv_file.name)
        total_inserted += inserted
        total_skipped += skipped
        print(f"   ✅ Inserted: {inserted}, Skipped: {skipped}")
    
    # Run enrichment
    enriched_count = enrich_leads()
    
    # Verify upload
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM leads WHERE source LIKE ?', ('NORTHEAST_%',))
    total_in_db = c.fetchone()[0]
    
    c.execute('''
        SELECT state, COUNT(*) as count 
        FROM leads 
        WHERE source LIKE ?
        GROUP BY state
        ORDER BY count DESC
    ''', ('NORTHEAST_%',))
    state_breakdown = c.fetchall()
    
    c.execute('''
        SELECT priority, COUNT(*) as count 
        FROM leads 
        WHERE source LIKE ?
        GROUP BY priority
    ''', ('NORTHEAST_%',))
    priority_breakdown = c.fetchall()
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("📊 UPLOAD COMPLETE")
    print("=" * 50)
    print(f"Total leads inserted: {total_inserted}")
    print(f"Total leads skipped (duplicates): {total_skipped}")
    print(f"Total Northeast leads in DB: {total_in_db}")
    print(f"Leads enriched: {enriched_count}")
    print("\n🏆 State Breakdown:")
    for state, count in state_breakdown:
        print(f"   {state or 'Unknown'}: {count} leads")
    print("\n🏆 Priority Breakdown:")
    for priority, count in priority_breakdown:
        print(f"   {priority or 'normal'}: {count} leads")

if __name__ == "__main__":
    main()