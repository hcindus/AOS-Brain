#!/usr/bin/env python3
"""
California ABC License Scraper - DataDepot Intelligence
Collects licensed alcohol establishments for POS lead generation
Public data source: CA Department of Alcoholic Beverage Control
"""

import requests
import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path
import re

class CAABCScraper:
    """Scraper for California ABC license data"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/database/datadepot.db'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.data_dir = Path('/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/data/raw')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def init_database(self):
        """Initialize SQLite database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main business table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_number TEXT UNIQUE,
                business_name TEXT,
                dba_name TEXT,
                license_type TEXT,
                status TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip TEXT,
                county TEXT,
                phone TEXT,
                license_issue_date TEXT,
                license_expiry_date TEXT,
                business_type TEXT,  -- Restaurant, Bar, Hotel, etc.
                pos_system_detected TEXT,  -- AI-enriched field
                data_source TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Contacts table (enrichment data)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id INTEGER,
                name TEXT,
                title TEXT,
                email TEXT,
                phone TEXT,
                linkedin_url TEXT,
                source TEXT,
                verified_at TIMESTAMP,
                FOREIGN KEY (business_id) REFERENCES businesses(id)
            )
        ''')
        
        # POS Intelligence table (enrichment)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pos_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id INTEGER,
                detected_pos_system TEXT,
                confidence_score REAL,
                detection_method TEXT,  -- photo_analysis, review_text, website_check
                equipment_age_estimate TEXT,
                replacement_likelihood REAL,  -- 0-1 score
                last_seen_date TEXT,
                FOREIGN KEY (business_id) REFERENCES businesses(id)
            )
        ''')
        
        # Scraping log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scrape_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                records_scraped INTEGER,
                new_records INTEGER,
                errors INTEGER,
                started_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized at {self.db_path}")
    
    def fetch_abc_data(self, county=None, city=None, limit=1000):
        """
        Fetch ABC license data from public sources
        Note: CA ABC doesn't have a public API, so we use alternative public sources
        """
        # Using OpenStreetMap + License data aggregation approach
        # For production, we'd use a combination of:
        # 1. OpenStreetMap Overpass API for amenity=bar, amenity=restaurant
        # 2. Google Places API (with appropriate key)
        # 3. Business license databases
        
        print(f"🔍 Fetching ABC license data for county={county}, city={city}")
        
        # Demo data structure - in production this would be real API calls
        sample_data = [
            {
                'license_number': 'ABC-123456',
                'business_name': 'Sample Restaurant LLC',
                'dba_name': 'The Golden Spoon',
                'license_type': '41 - On-Sale Beer & Wine',
                'status': 'Active',
                'address': '123 Main St',
                'city': 'San Francisco',
                'state': 'CA',
                'zip': '94102',
                'county': 'San Francisco',
                'phone': '415-555-0123'
            },
            {
                'license_number': 'ABC-789012',
                'business_name': 'Bay Area Bistro Inc',
                'dba_name': 'Harbor View Cafe',
                'license_type': '47 - On-Sale General',
                'status': 'Active',
                'address': '456 Waterfront Ave',
                'city': 'Oakland',
                'state': 'CA',
                'zip': '94607',
                'county': 'Alameda',
                'phone': '510-555-0456'
            }
        ]
        
        return sample_data
    
    def enrich_business_data(self, business):
        """AI enrichment for business data"""
        # This is where AI would analyze:
        # 1. Google Business Profile photos to detect POS terminals
        # 2. Reviews for equipment mentions
        # 3. Website for payment processor info
        
        enriched = business.copy()
        enriched['business_type'] = self._classify_business_type(business)
        enriched['pos_system_detected'] = None  # To be filled by AI pipeline
        enriched['data_source'] = 'CA_ABC_Public_Records'
        
        return enriched
    
    def _classify_business_type(self, business):
        """Classify business based on license type and name"""
        license_type = business.get('license_type', '').lower()
        name = business.get('dba_name', business.get('business_name', '')).lower()
        
        if 'restaurant' in name or 'cafe' in name or 'bistro' in name:
            return 'Restaurant'
        elif 'bar' in name or 'tavern' in name or 'lounge' in name:
            return 'Bar'
        elif 'hotel' in name or 'inn' in name:
            return 'Hotel'
        elif 'brewery' in name or 'distillery' in name:
            return 'Brewery/Distillery'
        elif 'wine' in name or 'winery' in name:
            return 'Winery'
        elif 'club' in name:
            return 'Private Club'
        else:
            return 'Other'
    
    def save_to_database(self, businesses):
        """Save scraped businesses to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        new_count = 0
        updated_count = 0
        
        for business in businesses:
            try:
                # Check if exists
                cursor.execute(
                    'SELECT id FROM businesses WHERE license_number = ?',
                    (business.get('license_number'),)
                )
                existing = cursor.fetchone()
                
                if existing:
                    # Update
                    cursor.execute('''
                        UPDATE businesses SET
                            business_name = ?,
                            dba_name = ?,
                            license_type = ?,
                            status = ?,
                            address = ?,
                            city = ?,
                            state = ?,
                            zip = ?,
                            county = ?,
                            phone = ?,
                            business_type = ?,
                            last_updated = CURRENT_TIMESTAMP
                        WHERE license_number = ?
                    ''', (
                        business.get('business_name'),
                        business.get('dba_name'),
                        business.get('license_type'),
                        business.get('status'),
                        business.get('address'),
                        business.get('city'),
                        business.get('state'),
                        business.get('zip'),
                        business.get('county'),
                        business.get('phone'),
                        business.get('business_type'),
                        business.get('license_number')
                    ))
                    updated_count += 1
                else:
                    # Insert
                    cursor.execute('''
                        INSERT INTO businesses (
                            license_number, business_name, dba_name, license_type,
                            status, address, city, state, zip, county, phone,
                            business_type, data_source
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        business.get('license_number'),
                        business.get('business_name'),
                        business.get('dba_name'),
                        business.get('license_type'),
                        business.get('status'),
                        business.get('address'),
                        business.get('city'),
                        business.get('state'),
                        business.get('zip'),
                        business.get('county'),
                        business.get('phone'),
                        business.get('business_type'),
                        business.get('data_source')
                    ))
                    new_count += 1
                    
            except Exception as e:
                print(f"❌ Error saving business {business.get('license_number')}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        return new_count, updated_count
    
    def log_scrape(self, source, records_scraped, new_records, errors, started_at):
        """Log scraping activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scrape_log (source, records_scraped, new_records, errors, started_at, completed_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (source, records_scraped, new_records, errors, started_at))
        
        conn.commit()
        conn.close()
    
    def run(self, county=None, city=None):
        """Main scraper run"""
        print("="*60)
        print("🚀 CA ABC License Scraper - DataDepot Intelligence")
        print("="*60)
        
        started_at = datetime.now()
        
        # Initialize database
        self.init_database()
        
        # Fetch data
        print(f"\n📥 Fetching data...")
        raw_data = self.fetch_abc_data(county=county, city=city)
        
        # Enrich with AI classification
        print(f"🧠 Enriching {len(raw_data)} records...")
        enriched_data = [self.enrich_business_data(b) for b in raw_data]
        
        # Save to database
        print(f"💾 Saving to database...")
        new_count, updated_count = self.save_to_database(enriched_data)
        
        # Log activity
        self.log_scrape(
            source='CA_ABC',
            records_scraped=len(raw_data),
            new_records=new_count,
            errors=0,
            started_at=started_at
        )
        
        # Summary
        print(f"\n✅ Scrape Complete!")
        print(f"   Records processed: {len(raw_data)}")
        print(f"   New businesses: {new_count}")
        print(f"   Updated: {updated_count}")
        print(f"   Database: {self.db_path}")
        
        return {
            'processed': len(raw_data),
            'new': new_count,
            'updated': updated_count
        }

def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CA ABC License Scraper')
    parser.add_argument('--county', help='Filter by county')
    parser.add_argument('--city', help='Filter by city')
    parser.add_argument('--db', help='Database path')
    
    args = parser.parse_args()
    
    scraper = CAABCScraper(db_path=args.db)
    result = scraper.run(county=args.county, city=args.city)
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
