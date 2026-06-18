#!/usr/bin/env python3
"""
Quick import script for CA leads to DepotChaos
Imports new leads from JSON files to unified.db
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
LEADS_DIR = Path("/root/.openclaw/workspace/data/leads")

def import_ca_leads():
    """Import CA leads from JSON files"""
    
    # Find today's lead file
    today = datetime.now().strftime("%Y-%m-%d")
    lead_file = LEADS_DIR / f"ca_leads_{today}.json"
    
    # Fallback to latest if today's doesn't exist
    if not lead_file.exists():
        lead_files = sorted(LEADS_DIR.glob("ca_leads_*.json"))
        if lead_files:
            lead_file = lead_files[-1]
        else:
            print("No lead files found")
            return 0
    
    print(f"Importing from: {lead_file}")
    
    # Load leads
    with open(lead_file, 'r') as f:
        leads = json.load(f)
    
    if not leads:
        print("No leads to import")
        return 0
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Ensure leads table exists with proper schema
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY,
            business_name TEXT,
            company_name TEXT,
            county TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            contact_name TEXT,
            contact_title TEXT,
            phone TEXT,
            email TEXT,
            status TEXT DEFAULT 'new',
            tier TEXT,
            pos_system TEXT,
            pos_confidence REAL,
            replacement_score REAL,
            enrichment_data TEXT,
            deleted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_type TEXT,
            tags TEXT
        )
    ''')
    
    # Import leads
    imported = 0
    skipped = 0
    
    for lead in leads:
        try:
            # Check if lead already exists
            lead_id = lead.get('id', '')
            company = lead.get('company_name', '')
            
            c.execute('SELECT id FROM leads WHERE id = ? OR business_name = ?', 
                     (lead_id, company))
            
            if c.fetchone():
                skipped += 1
                continue
            
            # Insert new lead (omit id to let it auto-increment)
            c.execute('''
                INSERT INTO leads 
                (business_name, city, state, status, source_type, 
                 enrichment_data, tags, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                company,
                lead.get('city', ''),
                lead.get('state', 'CA'),
                'new',
                lead.get('source', 'CA_SOS_Scraper'),
                json.dumps(lead),
                'ca_sos,auto_import',
                datetime.now().isoformat()
            ))
            imported += 1
            
        except Exception as e:
            print(f"Error importing {lead.get('company_name', 'unknown')}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Imported: {imported}")
    print(f"⏭️  Skipped (duplicates): {skipped}")
    print(f"📊 Total in file: {len(leads)}")
    
    return imported

def get_stats():
    """Get current lead stats"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Total leads
    c.execute("SELECT COUNT(*) FROM leads WHERE deleted = 0")
    total = c.fetchone()[0]
    
    # Today's new leads
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(*) FROM leads WHERE date(created_at) = date('now') AND deleted = 0")
    today_count = c.fetchone()[0]
    
    # By status
    c.execute("SELECT status, COUNT(*) FROM leads WHERE deleted = 0 GROUP BY status")
    by_status = c.fetchall()
    
    conn.close()
    
    return {
        'total': total,
        'today': today_count,
        'by_status': by_status
    }

if __name__ == "__main__":
    print("=" * 50)
    print("CA LEADS IMPORT TO DEPOTCHAOS")
    print("=" * 50)
    print()
    
    # Show stats before
    before = get_stats()
    print(f"📊 Before import: {before['total']} total leads")
    print()
    
    # Import
    imported = import_ca_leads()
    print()
    
    # Show stats after
    after = get_stats()
    print("=" * 50)
    print("IMPORT COMPLETE")
    print("=" * 50)
    print(f"📊 Total leads: {after['total']}")
    print(f"📈 New today: {after['today']}")
    print()
    print("📋 By Status:")
    for status, count in after['by_status']:
        print(f"   • {status}: {count}")
    print("=" * 50)
