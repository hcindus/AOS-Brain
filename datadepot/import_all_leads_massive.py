#!/usr/bin/env python3
"""
MASSIVE LEAD IMPORT - All sources to DepotChaos
Imports restaurants, realtors, prospects, and county leads
"""

import sqlite3
import csv
import uuid
import glob
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def get_db_counts(c):
    """Get current database stats"""
    c.execute("SELECT COUNT(*) FROM leads")
    leads = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM datadepot_intelligence")
    intel = c.fetchone()[0]
    return leads, intel

def import_restaurants(conn, c):
    """Import all restaurant leads"""
    print("\n" + "="*60)
    print(" RESTAURANT LEADS IMPORT")
    print("="*60)
    
    restaurant_files = glob.glob("/root/.openclaw/workspace/AGI_COMPANY/data/restaurants/**/*.csv", recursive=True)
    
    total_imported = 0
    total_skipped = 0
    
    for csv_path in sorted(restaurant_files):
        region = Path(csv_path).stem.replace("_restaurants", "").replace("_20260428", "")
        print(f"\n📍 {region}...")
        
        imported = 0
        skipped = 0
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        lead_id = str(uuid.uuid4())
                        
                        company = row.get('Company', '')
                        if not company:
                            continue
                        
                        first_name = row.get('First Name', '')
                        last_name = row.get('Last Name', '')
                        email = row.get('Email', '')
                        phone = row.get('Phone', '')
                        city = row.get('City', '')
                        county = row.get('County', city)
                        state = row.get('State', 'CA')
                        zip_code = row.get('Zip', '')
                        address = row.get('Address', '')
                        business_type = row.get('Business Type', 'Restaurant')
                        website = row.get('Website', '')
                        priority = row.get('Priority', 'C')
                        tags = row.get('Tags', '')
                        notes = row.get('Notes', '')
                        yelp_url = row.get('Yelp URL', '')
                        gmaps = row.get('Google Maps', '')
                        rating = row.get('Yelp Rating', '')
                        reviews = row.get('Yelp Reviews', '')
                        revenue = row.get('Est. Revenue', '')
                        employees = row.get('Employees', '')
                        pos_urgency = row.get('POS Urgency', '')
                        region_tag = row.get('Region', '')
                        
                        # Check duplicate by company + city
                        c.execute("SELECT id FROM leads WHERE company_name = ? AND enrichment_data LIKE ?", 
                                 (company, f'%"city": "{city}"%'))
                        if c.fetchone():
                            skipped += 1
                            continue
                        
                        # Calculate replacement score
                        replacement_score = 50
                        if priority == 'A':
                            replacement_score = 90
                        elif priority == 'B':
                            replacement_score = 75
                        elif priority == 'C':
                            replacement_score = 50
                        
                        # POS system detection from notes/tags
                        pos_system = 'Unknown'
                        if 'Toast' in notes or 'Toast' in tags:
                            pos_system = 'Toast'
                        elif 'Square' in notes or 'Square' in tags:
                            pos_system = 'Square'
                        elif 'Clover' in notes or 'Clover' in tags:
                            pos_system = 'Clover'
                        elif 'Revel' in notes or 'Revel' in tags:
                            pos_system = 'Revel'
                        
                        enrichment = {
                            'first_name': first_name,
                            'last_name': last_name,
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
                            'yelp_url': yelp_url,
                            'google_maps': gmaps,
                            'yelp_rating': rating,
                            'yelp_reviews': reviews,
                            'est_revenue': revenue,
                            'employees': employees,
                            'pos_urgency': pos_urgency,
                            'region': region_tag,
                            'source_file': Path(csv_path).name,
                            'industry': 'Restaurant'
                        }
                        
                        c.execute("""
                            INSERT INTO leads (
                                id, company_name, county, status, tier,
                                pos_system, replacement_score, source_type,
                                assigned_agent, enrichment_data, created_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            lead_id, company, county, 'new', f'Tier {priority}' if priority in ['A','B','C'] else 'Tier 2',
                            pos_system, replacement_score, 'CA_Restaurant_Scraper',
                            'Miles', json.dumps(enrichment), datetime.now().isoformat()
                        ))
                        
                        imported += 1
                        
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"   ⚠️ Error: {e}")
        
        print(f"   ✅ Imported: {imported} | Skipped: {skipped}")
        total_imported += imported
        total_skipped += skipped
        
        # Commit every 1000 leads
        if imported > 0 and imported % 1000 == 0:
            conn.commit()
    
    conn.commit()
    return total_imported, total_skipped

def import_cream_prospects(conn, c):
    """Import CREAM realtor prospects"""
    print("\n" + "="*60)
    print("🏠 CREAM REALTOR PROSPECTS IMPORT")
    print("="*60)
    
    cream_files = glob.glob("/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/*.csv")
    
    total_imported = 0
    total_skipped = 0
    
    for csv_path in sorted(cream_files):
        date_tag = Path(csv_path).stem.replace("realtor_prospects_", "")
        print(f"\n📅 {date_tag}...")
        
        imported = 0
        skipped = 0
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        lead_id = str(uuid.uuid4())
                        
                        company = row.get('Company', '')
                        first_name = row.get('First Name', '')
                        last_name = row.get('Last Name', '')
                        email = row.get('Email', '')
                        phone = row.get('Phone', '')
                        city = row.get('City', '')
                        state = row.get('State', '')
                        
                        if not company:
                            continue
                        
                        # Check duplicate
                        if email:
                            c.execute("SELECT id FROM leads WHERE enrichment_data LIKE ?", 
                                     (f'%"email": "{email}"%',))
                            if c.fetchone():
                                skipped += 1
                                continue
                        
                        tags = row.get('Tags', '')
                        priority = 'C'
                        if 'Priority_A' in tags:
                            priority = 'A'
                        elif 'Priority_B' in tags:
                            priority = 'B'
                        
                        notes = row.get('Notes', '')
                        
                        # Calculate score
                        replacement_score = 50
                        if priority == 'A':
                            replacement_score = 90
                        elif priority == 'B':
                            replacement_score = 70
                        
                        enrichment = {
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'phone': phone,
                            'city': city,
                            'state': state,
                            'county': city,
                            'tags': tags,
                            'notes': notes,
                            'priority': priority,
                            'source_file': Path(csv_path).name,
                            'industry': 'RealEstate',
                            'date_batch': date_tag
                        }
                        
                        c.execute("""
                            INSERT INTO leads (
                                id, company_name, county, status, tier,
                                replacement_score, source_type,
                                assigned_agent, enrichment_data, created_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            lead_id, company, city, 'new', f'Tier {priority}',
                            replacement_score, 'CREAM_RealEstate',
                            'Miles', json.dumps(enrichment), datetime.now().isoformat()
                        ))
                        
                        imported += 1
                        
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"   ⚠️ Error: {e}")
        
        print(f"   ✅ Imported: {imported} | Skipped: {skipped}")
        total_imported += imported
        total_skipped += skipped
        
        if imported > 0 and imported % 1000 == 0:
            conn.commit()
    
    conn.commit()
    return total_imported, total_skipped

def import_prospects_tiered(conn, c):
    """Import tiered prospects (starter, professional, corporate, enterprise)"""
    print("\n" + "="*60)
    print("💼 TIERED PROSPECTS IMPORT")
    print("="*60)
    
    tiers = {
        'prospects_starter': 'Tier 3',
        'prospects_professional': 'Tier 2',
        'prospects_corporate': 'Tier 1',
        'prospects_enterprise': 'Tier 1'
    }
    
    total_imported = 0
    total_skipped = 0
    
    for filename, tier in tiers.items():
        for base_path in [
            f"/root/.openclaw/workspace/sales/{filename}.csv",
            f"/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/sales/{filename}.csv"
        ]:
            if not Path(base_path).exists():
                continue
                
            print(f"\n📁 {filename} ({tier})...")
            
            imported = 0
            skipped = 0
            
            try:
                with open(base_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            lead_id = str(uuid.uuid4())
                            
                            # Parse the prospects CSV format
                            company = row.get('Company', '') or row.get('company', '')
                            contact = row.get('Contact', '') or row.get('contact', '')
                            title = row.get('Title', '') or row.get('title', '')
                            phone = row.get('Phone', '') or row.get('phone', '')
                            email = row.get('Email', '') or row.get('email', '')
                            city = row.get('City', '') or row.get('city', '')
                            state = row.get('State', '') or row.get('state', '')
                            
                            if not company:
                                continue
                            
                            # Check duplicate
                            c.execute("SELECT id FROM leads WHERE company_name = ?", (company,))
                            if c.fetchone():
                                skipped += 1
                                continue
                            
                            replacement_score = 70 if 'Tier 1' in tier else 50
                            
                            enrichment = {
                                'contact_name': contact,
                                'contact_title': title,
                                'email': email,
                                'phone': phone,
                                'city': city,
                                'state': state,
                                'county': city,
                                'tier_source': filename,
                                'source_file': Path(base_path).name
                            }
                            
                            c.execute("""
                                INSERT INTO leads (
                                    id, company_name, county, status, tier,
                                    replacement_score, source_type,
                                    assigned_agent, enrichment_data, created_at
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                lead_id, company, city or 'Unknown', 'new', tier,
                                replacement_score, f'Prospects_{filename}',
                                'Miles', json.dumps(enrichment), datetime.now().isoformat()
                            ))
                            
                            imported += 1
                            
                        except Exception as e:
                            continue
                            
            except Exception as e:
                print(f"   ⚠️ Error: {e}")
            
            print(f"   ✅ Imported: {imported} | Skipped: {skipped}")
            total_imported += imported
            total_skipped += skipped
    
    conn.commit()
    return total_imported, total_skipped

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get starting counts
    start_leads, start_intel = get_db_counts(c)
    print(f"\n📊 STARTING STATE:")
    print(f"   Leads: {start_leads:,}")
    print(f"   Intelligence: {start_intel:,}")
    
    # Import all sources
    restaurant_imported, restaurant_skipped = import_restaurants(conn, c)
    cream_imported, cream_skipped = import_cream_prospects(conn, c)
    prospects_imported, prospects_skipped = import_prospects_tiered(conn, c)
    
    # Get final counts
    end_leads, end_intel = get_db_counts(c)
    
    # Summary
    print("\n" + "="*60)
    print("✅ MASSIVE IMPORT COMPLETE")
    print("="*60)
    print(f"\n📈 RESULTS:")
    print(f"   Restaurants:  {restaurant_imported:,} new ({restaurant_skipped:,} dupes)")
    print(f"   CREAM Realtors: {cream_imported:,} new ({cream_skipped:,} dupes)")
    print(f"   Tiered Prospects: {prospects_imported:,} new ({prospects_skipped:,} dupes)")
    print(f"\n📊 DATABASE STATE:")
    print(f"   Starting leads: {start_leads:,}")
    print(f"   New leads added: {restaurant_imported + cream_imported + prospects_imported:,}")
    print(f"   Final lead count: {end_leads:,}")
    print(f"   Intelligence records: {end_intel:,}")
    
    conn.close()

if __name__ == "__main__":
    import json
    main()
