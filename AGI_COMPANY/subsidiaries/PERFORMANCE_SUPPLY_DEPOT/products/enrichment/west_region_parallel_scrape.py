#!/usr/bin/env python3
"""
WEST & MOUNTAIN REGION PARALLEL SCRAPER
Runs scrapers for: WA, OR, AZ, NV, CO, UT, NM, ID, MT, WY, AK, HI
"""

import subprocess
import json
import csv
import os
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3

# Configuration
OUTPUT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# State configurations
WEST_REGION_STATES = {
    'WA': {
        'name': 'Washington',
        'major_cities': ['Seattle', 'Spokane', 'Tacoma', 'Vancouver', 'Bellevue'],
        'population': 7738692,
        'scraper_type': 'dedicated',  # has wa_scraper.py
        'scraper_file': '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/enrichment/wa_scraper.py'
    },
    'OR': {
        'name': 'Oregon',
        'major_cities': ['Portland', 'Salem', 'Eugene', 'Gresham', 'Bend'],
        'population': 4237256,
        'scraper_type': 'dedicated',  # has or_scraper.py
        'scraper_file': '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/enrichment/or_scraper.py'
    },
    'AZ': {
        'name': 'Arizona',
        'major_cities': ['Phoenix', 'Tucson', 'Mesa', 'Scottsdale', 'Glendale'],
        'population': 7151502,
        'scraper_type': 'template',
        'target_leads': 300
    },
    'NV': {
        'name': 'Nevada',
        'major_cities': ['Las Vegas', 'Reno', 'Henderson', 'Carson City', 'North Las Vegas'],
        'population': 3104614,
        'scraper_type': 'template',
        'target_leads': 200
    },
    'CO': {
        'name': 'Colorado',
        'major_cities': ['Denver', 'Colorado Springs', 'Aurora', 'Boulder', 'Fort Collins'],
        'population': 5773714,
        'scraper_type': 'template',
        'target_leads': 250
    },
    'UT': {
        'name': 'Utah',
        'major_cities': ['Salt Lake City', 'Provo', 'Ogden', 'St. George', 'West Valley City'],
        'population': 3271616,
        'scraper_type': 'template',
        'target_leads': 200
    },
    'NM': {
        'name': 'New Mexico',
        'major_cities': ['Albuquerque', 'Santa Fe', 'Las Cruces', 'Roswell', 'Farmington'],
        'population': 2117522,
        'scraper_type': 'template',
        'target_leads': 150
    },
    'ID': {
        'name': 'Idaho',
        'major_cities': ['Boise', 'Idaho Falls', 'Nampa', 'Coeur d\'Alene', 'Twin Falls'],
        'population': 1839106,
        'scraper_type': 'template',
        'target_leads': 150
    },
    'MT': {
        'name': 'Montana',
        'major_cities': ['Billings', 'Missoula', 'Great Falls', 'Bozeman', 'Helena'],
        'population': 1084225,
        'scraper_type': 'template',
        'target_leads': 125
    },
    'WY': {
        'name': 'Wyoming',
        'major_cities': ['Cheyenne', 'Casper', 'Laramie', 'Jackson', 'Gillette'],
        'population': 576851,
        'scraper_type': 'template',
        'target_leads': 100
    },
    'AK': {
        'name': 'Alaska',
        'major_cities': ['Anchorage', 'Juneau', 'Fairbanks', 'Sitka', 'Ketchikan'],
        'population': 733391,
        'scraper_type': 'template',
        'target_leads': 100
    },
    'HI': {
        'name': 'Hawaii',
        'major_cities': ['Honolulu', 'Hilo', 'Kailua', 'Kahului', 'Kapa\'a'],
        'population': 1455271,
        'scraper_type': 'template',
        'target_leads': 125
    }
}

TEMPLATE_SCRAPER = '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/scrapers/us_state_scraper.py'
DB_PATH = '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/database/datadepot.db'


def run_dedicated_scraper(state_code, config):
    """Run dedicated scraper (WA or OR)"""
    print(f"🚀 [{state_code}] Starting dedicated scraper...")
    
    try:
        result = subprocess.run(
            ['python3', config['scraper_file']],
            capture_output=True,
            text=True,
            cwd=str(Path(config['scraper_file']).parent)
        )
        
        # Parse output to get lead count
        output = result.stdout + result.stderr
        
        # Find the leads directory
        leads_dir = Path('/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/enrichment/leads') / state_code.lower()
        csv_file = leads_dir / f"{state_code.lower()}_leads.csv"
        
        leads = []
        if csv_file.exists():
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                leads = list(reader)
        
        # Save to standardized location
        output_json = OUTPUT_DIR / f"WEST_{state_code}_leads.json"
        with open(output_json, 'w') as f:
            json.dump(leads, f, indent=2)
        
        print(f"✅ [{state_code}] Complete: {len(leads)} leads")
        return {'state': state_code, 'count': len(leads), 'file': str(output_json)}
        
    except Exception as e:
        print(f"❌ [{state_code}] Error: {e}")
        return {'state': state_code, 'count': 0, 'error': str(e)}


def run_template_scraper(state_code, config):
    """Run template scraper for other states"""
    print(f"🚀 [{state_code}] Starting template scraper...")
    
    output_file = OUTPUT_DIR / f"WEST_{state_code}_leads.json"
    
    try:
        result = subprocess.run(
            [
                'python3', TEMPLATE_SCRAPER,
                '--state', state_code,
                '--business-type', 'restaurant,cafe,bar,food service,catering,bakery,brewery',
                '--sample-size', str(config.get('target_leads', 100)),
                '--output', str(output_file)
            ],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Parse the generated file
        if output_file.exists():
            with open(output_file, 'r') as f:
                leads = json.load(f)
            
            # Also save as CSV
            csv_file = OUTPUT_DIR / f"WEST_{state_code}_leads.csv"
            if leads:
                with open(csv_file, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=leads[0].keys())
                    writer.writeheader()
                    writer.writerows(leads)
            
            print(f"✅ [{state_code}] Complete: {len(leads)} leads")
            return {'state': state_code, 'count': len(leads), 'file': str(output_file)}
        else:
            raise Exception("Output file not created")
            
    except Exception as e:
        print(f"❌ [{state_code}] Error: {e}")
        return {'state': state_code, 'count': 0, 'error': str(e)}


def scrape_state(state_code, config):
    """Route to appropriate scraper"""
    if config['scraper_type'] == 'dedicated':
        return run_dedicated_scraper(state_code, config)
    else:
        return run_template_scraper(state_code, config)


def enrich_and_upload(results):
    """Enrich leads and upload to database"""
    print("\n" + "="*70)
    print("ENRICHMENT & DATABASE UPLOAD")
    print("="*70)
    
    all_leads = []
    total_leads = 0
    
    # Collect all leads
    for result in results:
        if 'file' in result and Path(result['file']).exists():
            try:
                with open(result['file'], 'r') as f:
                    leads = json.load(f)
                    # Add state metadata
                    for lead in leads:
                        lead['region'] = 'WEST'
                        lead['upload_batch'] = datetime.now().isoformat()
                    all_leads.extend(leads)
                    total_leads += len(leads)
                    print(f"📊 {result['state']}: {len(leads)} leads loaded")
            except Exception as e:
                print(f"⚠️  Error loading {result['state']}: {e}")
    
    print(f"\n📦 Total leads to upload: {total_leads}")
    
    # Upload to database
    try:
        new_count, updated_count = upload_to_database(all_leads)
        print(f"✅ Database upload complete: {new_count} new, {updated_count} updated")
    except Exception as e:
        print(f"❌ Database upload failed: {e}")
        new_count, updated_count = 0, 0
    
    # Save consolidated file
    consolidated_file = OUTPUT_DIR / f"WEST_ALL_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(consolidated_file, 'w') as f:
        json.dump(all_leads, f, indent=2)
    
    print(f"💾 Consolidated file saved: {consolidated_file}")
    
    return total_leads, new_count, updated_count


def upload_to_database(leads):
    """Upload leads to DepotChaos database"""
    # Ensure DB directory exists
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
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
            region TEXT,
            upload_batch TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    new_count = 0
    updated_count = 0
    
    for lead in leads:
        try:
            lead_id = lead.get('id') or f"{lead.get('source', 'WEST')}-{lead.get('state', 'XX')}-{datetime.now().timestamp()}"
            
            # Check if exists
            cursor.execute('SELECT id FROM leads WHERE id = ?', (lead_id,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute('''
                    UPDATE leads SET
                        company_name = ?,
                        contact_name = ?,
                        email = ?,
                        phone = ?,
                        city = ?,
                        county = ?,
                        state = ?,
                        zip = ?,
                        business_type = ?,
                        priority = ?,
                        notes = ?,
                        upload_batch = ?
                    WHERE id = ?
                ''', (
                    lead.get('company_name') or lead.get('business_name'),
                    lead.get('contact_name'),
                    lead.get('email'),
                    lead.get('phone'),
                    lead.get('city'),
                    lead.get('county'),
                    lead.get('state'),
                    lead.get('zip', lead.get('postal')),
                    lead.get('business_type'),
                    lead.get('priority', 'C'),
                    lead.get('notes', ''),
                    lead.get('upload_batch'),
                    lead_id
                ))
                updated_count += 1
            else:
                cursor.execute('''
                    INSERT INTO leads (
                        id, company_name, contact_name, email, phone, address,
                        city, county, state, zip, country, business_type, priority,
                        source, tags, scraped_at, notes, region, upload_batch
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    lead_id,
                    lead.get('company_name') or lead.get('business_name'),
                    lead.get('contact_name'),
                    lead.get('email'),
                    lead.get('phone'),
                    lead.get('address'),
                    lead.get('city'),
                    lead.get('county'),
                    lead.get('state'),
                    lead.get('zip', lead.get('postal')),
                    lead.get('country', 'US'),
                    lead.get('business_type'),
                    lead.get('priority', 'C'),
                    lead.get('source'),
                    lead.get('tags'),
                    lead.get('scraped_at'),
                    lead.get('notes', ''),
                    lead.get('region', 'WEST'),
                    lead.get('upload_batch')
                ))
                new_count += 1
                
        except Exception as e:
            print(f"  ⚠️ Error importing lead {lead_id}: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    return new_count, updated_count


def main():
    print("="*70)
    print("WEST & MOUNTAIN REGION PARALLEL SCRAPER")
    print("="*70)
    print(f"Started: {datetime.now().isoformat()}")
    print(f"States: {', '.join(WEST_REGION_STATES.keys())}")
    print(f"Output: {OUTPUT_DIR}")
    print("="*70)
    
    results = []
    
    # Run all scrapers in parallel
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_state = {
            executor.submit(scrape_state, state_code, config): state_code 
            for state_code, config in WEST_REGION_STATES.items()
        }
        
        for future in as_completed(future_to_state):
            state_code = future_to_state[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"❌ [{state_code}] Thread error: {e}")
                results.append({'state': state_code, 'count': 0, 'error': str(e)})
    
    # Report results
    print("\n" + "="*70)
    print("SCRAPING RESULTS")
    print("="*70)
    
    total_scraped = 0
    for result in sorted(results, key=lambda x: x['state']):
        status = "✅" if 'error' not in result else "❌"
        count = result.get('count', 0)
        total_scraped += count
        error_msg = f" ({result.get('error', '')})" if 'error' in result else ""
        print(f"{status} {result['state']}: {count} leads{error_msg}")
    
    print(f"\n📊 Total Scraped: {total_scraped} leads")
    
    # Enrich and upload
    total_leads, new_db, updated_db = enrich_and_upload(results)
    
    # Final report
    print("\n" + "="*70)
    print("WEST & MOUNTAIN REGION SCRAPE COMPLETE")
    print("="*70)
    print(f"Total leads scraped: {total_scraped}")
    print(f"Database - New: {new_db}, Updated: {updated_db}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Completed: {datetime.now().isoformat()}")
    print("="*70)
    
    return total_scraped, new_db, updated_db


if __name__ == "__main__":
    main()
