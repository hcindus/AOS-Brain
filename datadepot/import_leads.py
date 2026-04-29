#!/usr/bin/env python3
"""
Import lead CSV to DepotChaos database
Maps CSV columns to database schema
"""

import sqlite3
import csv
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
CSV_PATH = "/root/.openclaw/workspace/datadepot/leads/batch_20260429_194121_200leads.csv"

def import_leads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Count existing
    c.execute("SELECT COUNT(*) FROM leads")
    existing = c.fetchone()[0]
    print(f"Existing leads: {existing}")
    
    imported = 0
    skipped = 0
    
    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Generate UUID
            lead_id = str(uuid.uuid4())
            
            # Map CSV to database columns
            company_name = row.get('company', '')
            contact = row.get('contact', '')
            title = row.get('title', '')
            phone = row.get('phone', '')
            email = row.get('email', '')
            city = row.get('city', '')
            county = city  # Use city as county for now
            tier = row.get('tier', 'Tier 2')
            source = row.get('source', '')
            pos_system = row.get('pos_focus', '')
            notes = row.get('notes', '')
            
            # Calculate replacement score based on POS system
            replacement_score = 50  # default
            if pos_system:
                scores = {
                    'Square': 85,
                    'Clover': 75,
                    'Toast': 60,
                    'Revel': 70,
                    'TouchBistro': 65,
                    'Aloha': 80,
                    'Micros': 75,
                    'Lightspeed': 60
                }
                replacement_score = scores.get(pos_system, 50)
            
            # Check if company already exists
            c.execute("SELECT id FROM leads WHERE company_name = ?", (company_name,))
            if c.fetchone():
                skipped += 1
                continue
            
            # Build enrichment data with contact info
            enrichment = {
                'contact_name': contact,
                'contact_title': title,
                'phone': phone,
                'email': email,
                'city': city,
                'notes': notes
            }
            
            # Insert lead - only use columns that exist in schema
            c.execute("""
                INSERT INTO leads (
                    id, company_name, county, status, tier, 
                    pos_system, replacement_score, source_type,
                    assigned_agent, enrichment_data, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lead_id, company_name, county, 'new', tier,
                pos_system, replacement_score, source,
                'Miles', json.dumps(enrichment), datetime.now().isoformat()
            ))
            
            imported += 1
            if imported % 50 == 0:
                print(f"Imported {imported}...")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Import complete:")
    print(f"   Imported: {imported}")
    print(f"   Skipped (duplicates): {skipped}")
    print(f"   Total in database: {existing + imported}")

if __name__ == "__main__":
    import json
    import_leads()
