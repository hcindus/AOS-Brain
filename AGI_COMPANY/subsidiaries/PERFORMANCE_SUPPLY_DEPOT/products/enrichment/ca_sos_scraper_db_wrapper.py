#!/usr/bin/env python3
"""
CA SOS Scraper Database Upload Wrapper
Calls the Node.js scraper and uploads results to unified.db
"""

import subprocess
import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def run_scraper(sample_count=50):
    """Run the Node.js CA SOS scraper"""
    scraper_path = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/enrichment/ca_sos_scraper_fixed.js"
    
    try:
        result = subprocess.run(
            ['node', scraper_path, '--sample', str(sample_count)],
            capture_output=True,
            text=True,
            cwd=Path(scraper_path).parent
        )
        
        # Parse output for lead file path
        output = result.stdout
        print(output)
        
        # Look for saved file
        leads_dir = Path(scraper_path).parent / "../leads"
        json_files = sorted(leads_dir.glob("CA_leads_*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        if json_files:
            latest_file = json_files[0]
            print(f"Found leads file: {latest_file}")
            with open(latest_file, 'r') as f:
                return json.load(f)
        
        return []
    except Exception as e:
        print(f"Error running scraper: {e}")
        return []

def upload_to_database(leads):
    """Upload leads to unified.db"""
    if not leads:
        print("No leads to upload")
        return 0
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
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
            region TEXT,
            upload_batch TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    uploaded = 0
    batch_id = datetime.now().isoformat()
    
    for i, lead in enumerate(leads):
        try:
            lead_id = lead.get('sos_id') or f"CA-SOS-{i}-{datetime.now().timestamp()}"
            cursor.execute('''
                INSERT OR REPLACE INTO leads 
                (id, company_name, contact_name, email, phone, address, city, county, state, 
                 zip, country, business_type, priority, source, tags, scraped_at, notes, region, upload_batch)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead_id,
                lead.get('business_name'),
                lead.get('agent'),
                lead.get('email'),
                lead.get('phone'),
                lead.get('address'),
                lead.get('city'),
                lead.get('county'),
                lead.get('state', 'CA'),
                lead.get('zip'),
                'US',
                lead.get('business_type'),
                lead.get('priority', 'normal'),
                'CA_SOS_Scraper',
                f"restaurant,california,{lead.get('city', '')}",
                lead.get('discovered_at') or datetime.now().isoformat(),
                f"Status: {lead.get('status', 'Unknown')}",
                'WEST',
                batch_id
            ))
            uploaded += 1
        except Exception as e:
            print(f"   ⚠️ Error uploading lead: {e}")
    
    conn.commit()
    conn.close()
    print(f"📤 Uploaded {uploaded} CA leads to unified.db")
    return uploaded

def main():
    print("=" * 60)
    print("CA SOS SCRAPER + DATABASE UPLOAD")
    print("=" * 60)
    
    leads = run_scraper(sample_count=50)
    if leads:
        upload_to_database(leads)
    
    print("\n✅ CA SOS scraper complete!")

if __name__ == "__main__":
    main()
