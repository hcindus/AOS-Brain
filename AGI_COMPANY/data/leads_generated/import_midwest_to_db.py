#!/usr/bin/env python3
"""
Import Midwest leads to DepotChaos database
Processes MIDWEST_*.json files and imports to SQLite
"""

import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def create_tables(conn):
    """Ensure tables exist"""
    c = conn.cursor()
    
    # Leads table
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
    
    # Enriched leads table
    c.execute('''
        CREATE TABLE IF NOT EXISTS enriched_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            company_name TEXT,
            phone TEXT,
            email TEXT,
            website TEXT,
            pos_system TEXT,
            replacement_score INTEGER,
            estimated_volume TEXT,
            status TEXT,
            enriched_at TEXT,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
        )
    ''')
    
    conn.commit()

def import_file(conn, filepath):
    """Import a single JSON file"""
    c = conn.cursor()
    
    try:
        with open(filepath, 'r') as f:
            leads = json.load(f)
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return 0, 0
    
    imported = 0
    skipped = 0
    
    for lead in leads:
        try:
            # Check if exists
            c.execute('''
                SELECT id FROM leads 
                WHERE business_name = ? AND city = ? AND state = ?
            ''', (lead.get('company_name'), lead.get('city'), lead.get('state')))
            
            if c.fetchone():
                skipped += 1
                continue
            
            # Insert lead
            c.execute('''
                INSERT INTO leads (
                    business_name, city, state, zip, phone, email,
                    business_type, priority, source, scraped_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead.get('company_name'),
                lead.get('city'),
                lead.get('state'),
                lead.get('zip'),
                lead.get('phone'),
                lead.get('email'),
                lead.get('business_type'),
                lead.get('priority'),
                lead.get('source'),
                lead.get('scraped_at', datetime.now().isoformat())
            ))
            
            lead_id = c.lastrowid
            
            # Insert enriched data if available
            if lead.get('pos_system') or lead.get('replacement_score'):
                c.execute('''
                    INSERT INTO enriched_leads (
                        lead_id, company_name, phone, email, pos_system,
                        replacement_score, estimated_volume, status, enriched_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    lead_id,
                    lead.get('company_name'),
                    lead.get('phone'),
                    lead.get('email'),
                    lead.get('pos_system'),
                    lead.get('replacement_score'),
                    lead.get('estimated_volume'),
                    'enriched',
                    datetime.now().isoformat()
                ))
            
            imported += 1
            
        except Exception as e:
            print(f"  Error importing lead {lead.get('id')}: {e}")
            skipped += 1
    
    conn.commit()
    return imported, skipped

def main():
    parser = argparse.ArgumentParser(description='Import Midwest leads to DB')
    parser.add_argument('--input-dir', required=True, help='Directory with MIDWEST_*.json files')
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    
    if not input_dir.exists():
        print(f"Error: Directory not found: {input_dir}")
        return 1
    
    # Find all MIDWEST_*.json files
    files = sorted(input_dir.glob("MIDWEST_*.json"))
    
    if not files:
        print(f"No MIDWEST_*.json files found in {input_dir}")
        return 1
    
    print(f"Found {len(files)} Midwest files to import")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    
    # Get existing count
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM leads")
    existing = c.fetchone()[0]
    print(f"Existing leads in DB: {existing}")
    
    # Process each file
    total_imported = 0
    total_skipped = 0
    
    for filepath in files:
        print(f"\nProcessing: {filepath.name}")
        imported, skipped = import_file(conn, filepath)
        total_imported += imported
        total_skipped += skipped
        print(f"  Imported: {imported} | Skipped: {skipped}")
    
    conn.close()
    
    print("\n" + "="*50)
    print("IMPORT SUMMARY")
    print("="*50)
    print(f"Files processed: {len(files)}")
    print(f"Total imported: {total_imported}")
    print(f"Total skipped (duplicates): {total_skipped}")
    print(f"New total in DB: {existing + total_imported}")
    
    return 0

if __name__ == '__main__':
    exit(main())
