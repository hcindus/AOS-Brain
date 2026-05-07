#!/usr/bin/env python3
"""
Upload International Leads (Canada & Mexico) to DepotChaos DB
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
    
    # Check if table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leads'")
    table_exists = c.fetchone()
    
    if table_exists:
        # Check if country column exists
        c.execute("PRAGMA table_info(leads)")
        columns = [col[1] for col in c.fetchall()]
        
        # Add missing columns
        if 'country' not in columns:
            c.execute("ALTER TABLE leads ADD COLUMN country TEXT")
        if 'address' not in columns:
            c.execute("ALTER TABLE leads ADD COLUMN address TEXT")
        if 'category' not in columns:
            c.execute("ALTER TABLE leads ADD COLUMN category TEXT")
        if 'sub_region' not in columns:
            c.execute("ALTER TABLE leads ADD COLUMN sub_region TEXT")
        if 'lead_score' not in columns:
            c.execute("ALTER TABLE leads ADD COLUMN lead_score INTEGER")
        if 'naics_code' not in columns:
            c.execute("ALTER TABLE leads ADD COLUMN naics_code TEXT")
        if 'employee_count' not in columns:
            c.execute("ALTER TABLE leads ADD COLUMN employee_count TEXT")
        if 'tax_id' not in columns:
            c.execute("ALTER TABLE leads ADD COLUMN tax_id TEXT")
    else:
        # Create new table with all columns
        c.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT NOT NULL,
                address TEXT,
                city TEXT,
                state TEXT,
                country TEXT,
                zip TEXT,
                phone TEXT,
                email TEXT,
                business_type TEXT,
                category TEXT,
                sub_region TEXT,
                lead_score INTEGER,
                priority TEXT,
                source TEXT,
                scraped_at TEXT,
                enriched_at TEXT,
                enrichment_status TEXT DEFAULT 'pending',
                naics_code TEXT,
                employee_count TEXT,
                tax_id TEXT
            )
        ''')
    
    conn.commit()
    conn.close()
    print("✅ Database schema verified/updated")

def import_csv_leads(filepath):
    """Import leads from CSV file"""
    leads = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads

def upload_international_leads(leads, source_file, region):
    """Upload leads to DepotChaos DB"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    today = datetime.now().strftime('%Y%m%d')
    inserted = 0
    skipped = 0
    
    for i, lead in enumerate(leads):
        business_name = lead.get('business_name', '')
        if not business_name:
            skipped += 1
            continue
        
        city = lead.get('city', '')
        state = lead.get('province_state', '')
        country = lead.get('country', '')
        
        # Check for duplicates
        c.execute('SELECT id FROM leads WHERE business_name = ? AND city = ? AND state = ? AND (country = ? OR country IS NULL)', 
                  (business_name, city, state, country))
        if c.fetchone():
            skipped += 1
            continue
        
        c.execute('''
            INSERT OR IGNORE INTO leads 
            (business_name, address, city, state, country, zip, phone, email, 
             business_type, category, sub_region, lead_score, priority, source, 
             scraped_at, enrichment_status, naics_code, employee_count, tax_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            business_name,
            lead.get('address', ''),
            city,
            state,
            country,
            lead.get('postal_code', ''),
            lead.get('phone', ''),
            '',  # email (not available)
            lead.get('category', ''),
            lead.get('category', ''),
            lead.get('sub_region', ''),
            int(lead.get('lead_score', 50)),
            'high' if int(lead.get('lead_score', 0)) > 75 else 'normal',
            f"INTL_{region}_{source_file}",
            lead.get('date_scraped', datetime.now().isoformat()),
            'enriched',
            lead.get('naics_code', ''),
            lead.get('employee_count', ''),
            lead.get('tax_id', '')
        ))
        inserted += 1
    
    conn.commit()
    conn.close()
    return inserted, skipped

def main():
    print("🚀 DepotChaos International Leads Upload")
    print("=" * 50)
    
    # Ensure DB exists
    ensure_db_exists()
    
    # Process merged international file
    merged_file = LEADS_DIR / "INTL_MASTER_MERGED_2026-05-07.csv"
    
    total_inserted = 0
    total_skipped = 0
    
    if merged_file.exists():
        print(f"\n📤 Uploading merged international leads: {merged_file.name}")
        leads = import_csv_leads(merged_file)
        print(f"   Found {len(leads)} leads in file")
        
        # Split by region for better tracking
        canada_leads = [l for l in leads if l.get('region') == 'Canada']
        mexico_leads = [l for l in leads if l.get('region') == 'Mexico']
        
        if canada_leads:
            print(f"\n   🇨🇦 Processing {len(canada_leads)} Canada leads...")
            inserted, skipped = upload_international_leads(canada_leads, "CANADA_MASTER", "CA")
            total_inserted += inserted
            total_skipped += skipped
            print(f"      ✅ Inserted: {inserted}, Skipped: {skipped}")
        
        if mexico_leads:
            print(f"\n   🇲🇽 Processing {len(mexico_leads)} Mexico leads...")
            inserted, skipped = upload_international_leads(mexico_leads, "MEXICO_MASTER", "MX")
            total_inserted += inserted
            total_skipped += skipped
            print(f"      ✅ Inserted: {inserted}, Skipped: {skipped}")
    else:
        print(f"   ⚠️ Merged file not found: {merged_file}")
    
    # Verify upload
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Count by region
    c.execute('SELECT COUNT(*) FROM leads WHERE source LIKE ?', ('INTL_CA%',))
    canada_in_db = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM leads WHERE source LIKE ?', ('INTL_MX%',))
    mexico_in_db = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM leads WHERE source LIKE ?', ('INTL_%',))
    total_intl = c.fetchone()[0]
    
    # Top categories
    c.execute('''
        SELECT category, COUNT(*) as count 
        FROM leads 
        WHERE source LIKE ?
        GROUP BY category
        ORDER BY count DESC
        LIMIT 10
    ''', ('INTL_%',))
    category_breakdown = c.fetchall()
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("📊 INTERNATIONAL UPLOAD COMPLETE")
    print("=" * 50)
    print(f"\n🇨🇦 Canada: {canada_in_db} leads in DB")
    print(f"🇲🇽 Mexico: {mexico_in_db} leads in DB")
    print(f"\n📈 Total International Leads: {total_intl}")
    print(f"   Inserted this run: {total_inserted}")
    print(f"   Skipped (duplicates): {total_skipped}")
    print("\n🏆 Top Categories:")
    for cat, count in category_breakdown:
        print(f"   {cat or 'Unknown'}: {count} leads")

if __name__ == "__main__":
    main()
