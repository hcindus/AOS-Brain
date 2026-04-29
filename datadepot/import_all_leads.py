#!/usr/bin/env python3
"""
Import all 7K leads to DepotChaos database
Maps the FINAL_INTEGRATED_LEADS.csv columns
"""

import sqlite3
import csv
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
CSV_PATH = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_final/FINAL_INTEGRATED_LEADS.csv"

def import_all_leads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Count existing
    c.execute("SELECT COUNT(*) FROM leads")
    existing = c.fetchone()[0]
    print(f"Existing leads: {existing}")
    
    imported = 0
    skipped = 0
    failed = 0
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Generate UUID
                lead_id = str(uuid.uuid4())
                
                # Map CSV columns to database
                company_name = row.get('Company', '')
                first_name = row.get('First Name', '')
                last_name = row.get('Last Name', '')
                contact = f"{first_name} {last_name}".strip()
                email = row.get('Email', '')
                phone = row.get('Phone', '')
                city = row.get('City', '')
                county = row.get('County', '')
                state = row.get('State', '')
                zip_code = row.get('Zip', '')
                address = row.get('Address', '')
                business_type = row.get('Business Type', '')
                website = row.get('Website', '')
                source = row.get('Source', 'Final Integrated')
                priority = row.get('Priority', 'C')
                tags = row.get('Tags', '')
                notes = row.get('Notes', '')
                scrape_date = row.get('Scrape Date', datetime.now().strftime('%Y-%m-%d'))
                
                # Determine tier from Priority
                tier = f"Tier {priority}" if priority in ['1', '2', '3'] else 'Tier 2'
                
                # Calculate replacement score based on priority
                replacement_score = 50
                if priority == 'A':
                    replacement_score = 90
                elif priority == 'B':
                    replacement_score = 70
                elif priority == 'C':
                    replacement_score = 50
                
                # Check if company already exists
                c.execute("SELECT id FROM leads WHERE company_name = ?", (company_name,))
                if c.fetchone():
                    skipped += 1
                    continue
                
                # Build enrichment data
                enrichment = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'contact_name': contact,
                    'email': email,
                    'phone': phone,
                    'address': address,
                    'city': city,
                    'county': county,
                    'state': state,
                    'zip': zip_code,
                    'business_type': business_type,
                    'website': website,
                    'priority': priority,
                    'tags': tags,
                    'notes': notes,
                    'scrape_date': scrape_date
                }
                
                # Insert lead
                c.execute("""
                    INSERT INTO leads (
                        id, company_name, county, status, tier, 
                        pos_system, replacement_score, source_type,
                        assigned_agent, enrichment_data, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    lead_id, company_name, county, 'new', tier,
                    business_type, replacement_score, source,
                    'Miles', json.dumps(enrichment), datetime.now().isoformat()
                ))
                
                imported += 1
                if imported % 500 == 0:
                    conn.commit()
                    print(f"Imported {imported}...")
                    
            except Exception as e:
                failed += 1
                if failed % 100 == 0:
                    print(f"  {failed} failed...")
    
    conn.commit()
    
    # Get final count
    c.execute("SELECT COUNT(*) FROM leads")
    final_count = c.fetchone()[0]
    conn.close()
    
    print(f"\n✅ Import complete:")
    print(f"   Imported: {imported}")
    print(f"   Skipped (duplicates): {skipped}")
    print(f"   Failed: {failed}")
    print(f"   Total in database: {final_count}")

if __name__ == "__main__":
    import json
    import_all_leads()
