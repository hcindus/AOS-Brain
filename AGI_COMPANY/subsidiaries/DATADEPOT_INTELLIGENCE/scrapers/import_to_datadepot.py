#!/usr/bin/env python3
"""
Import scraper output to DataDepot database
"""

import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime

def import_leads_to_db(leads_data, db_path):
    """Import leads to unified database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create leads table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY,
            company_name TEXT,
            contact_name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            county TEXT,
            state TEXT,
            zip TEXT,
            country TEXT DEFAULT 'US',
            business_type TEXT,
            priority TEXT,
            source TEXT,
            tags TEXT,
            scraped_at TIMESTAMP,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    new_count = 0
    updated_count = 0
    
    for lead in leads_data:
        try:
            lead_id = lead.get('id', f"{lead.get('source', 'UNKNOWN')}-{datetime.now().timestamp()}")
            
            # Check if exists
            cursor.execute('SELECT id FROM leads WHERE id = ?', (lead_id,))
            existing = cursor.fetchone()
            
            if existing:
                # Update
                cursor.execute('''
                    UPDATE leads SET
                        company_name = ?,
                        contact_name = ?,
                        email = ?,
                        phone = ?,
                        city = ?,
                        county = ?,
                        state = ?,
                        country = ?,
                        priority = ?,
                        notes = ?
                    WHERE id = ?
                ''', (
                    lead.get('company_name'),
                    lead.get('contact_name'),
                    lead.get('email'),
                    lead.get('phone'),
                    lead.get('city'),
                    lead.get('county'),
                    lead.get('state', lead.get('province', lead.get('state_code', ''))),
                    lead.get('country', 'US'),
                    lead.get('priority', 'C'),
                    lead.get('notes', ''),
                    lead_id
                ))
                updated_count += 1
            else:
                # Insert
                cursor.execute('''
                    INSERT INTO leads (
                        id, company_name, contact_name, email, phone, address,
                        city, county, state, zip, country, business_type, priority,
                        source, tags, scraped_at, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    lead_id,
                    lead.get('company_name'),
                    lead.get('contact_name'),
                    lead.get('email'),
                    lead.get('phone'),
                    lead.get('address'),
                    lead.get('city'),
                    lead.get('county'),
                    lead.get('state', lead.get('province', lead.get('state_code', ''))),
                    lead.get('zip', lead.get('postal', '')),
                    lead.get('country', 'US'),
                    lead.get('business_type'),
                    lead.get('priority', 'C'),
                    lead.get('source'),
                    lead.get('tags'),
                    lead.get('scraped_at'),
                    lead.get('notes')
                ))
                new_count += 1
                
        except Exception as e:
            print(f"  ⚠️  Error importing lead: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    return new_count, updated_count

def main():
    parser = argparse.ArgumentParser(description='Import scraper data to database')
    parser.add_argument('--input-dir', required=True, help='Directory with JSON files')
    parser.add_argument('--db', required=True, help='SQLite database path')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_dir)
    total_new = 0
    total_updated = 0
    files_processed = 0
    
    print("📥 Importing scraper data to database...")
    print(f"   Database: {args.db}")
    print(f"   Input dir: {input_path}")
    
    # Find all JSON files
    json_files = list(input_path.rglob('*.json'))
    print(f"   Found {len(json_files)} JSON files")
    
    for json_file in json_files:
        try:
            with open(json_file) as f:
                leads = json.load(f)
            
            if isinstance(leads, list) and len(leads) > 0:
                new, updated = import_leads_to_db(leads, args.db)
                total_new += new
                total_updated += updated
                files_processed += 1
                print(f"   ✅ {json_file.name}: +{new} new, ~{updated} updated")
        except Exception as e:
            print(f"   ⚠️  {json_file.name}: {e}")
    
    print(f"\n📊 Import Complete!")
    print(f"   Files processed: {files_processed}")
    print(f"   New leads: {total_new}")
    print(f"   Updated: {total_updated}")

if __name__ == '__main__':
    main()
