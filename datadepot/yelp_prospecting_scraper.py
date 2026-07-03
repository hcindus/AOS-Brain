#!/usr/bin/env python3
"""
Yelp Prospecting Scraper for PSDEPOT
Uses existing Yelp Fusion API key
"""

import sqlite3
import json
import time
import os
import requests
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
YELP_API_KEY = os.environ.get('YELP_API_KEY', '5DUaC-eBObfSXkjf4YfLNlViO-WqwwCk0UJYewfhav25gbTrCaPvPR_nhokKyfBNKnduMHkqd5Z_v_0RwHSj2fXs8ziaJ-O_RAkuRvc6L6Lt9dwEboKoYHBpBuL1aXYx')

# Target cities for PSDEPOT - California Focus
TARGET_CITIES = [
    # Sacramento Area
    ("Sacramento", "CA"), ("Elk Grove", "CA"), ("Folsom", "CA"), 
    ("Roseville", "CA"), ("Citrus Heights", "CA"), ("Rancho Cordova", "CA"),
    ("Carmichael", "CA"), ("West Sacramento", "CA"), ("Davis", "CA"), 
    ("Woodland", "CA"), ("Galt", "CA"),
    
    # North Bay / Wine Country
    ("Santa Rosa", "CA"), ("Petaluma", "CA"), ("Napa", "CA"), 
    ("Vallejo", "CA"), ("Sonoma", "CA"), ("Fairfield", "CA"), 
    ("Vacaville", "CA"), ("American Canyon", "CA"), ("Calistoga", "CA"), 
    ("St Helena", "CA"), ("Windsor", "CA"), ("Healdsburg", "CA"),
    ("Novato", "CA"), ("San Rafael", "CA"),
    
    # Stockton Area
    ("Stockton", "CA"), ("Lodi", "CA"), ("Manteca", "CA"), 
    ("Tracy", "CA"), ("Ripon", "CA"),
    
    # Bay Area (selective)
    ("San Jose", "CA"), ("Oakland", "CA"), ("Fremont", "CA"), 
    ("Hayward", "CA"), ("Concord", "CA"), ("Berkeley", "CA"), 
    ("Richmond", "CA"), ("San Francisco", "CA"),
    
    # Central Valley
    ("Modesto", "CA"), ("Turlock", "CA"), ("Merced", "CA"), 
    ("Fresno", "CA"), ("Clovis", "CA"), ("Bakersfield", "CA")
]

# PSDEPOT Categories - receipt users
PSDEPOT_TERMS = [
    # Mexican
    "taqueria", "taco", "burrito", "mexican restaurant",
    
    # Asian
    "thai restaurant", "korean restaurant", "vietnamese restaurant", 
    "pho", "chinese restaurant", "sushi", "japanese restaurant",
    "filipino restaurant", "indian restaurant", "bubble tea", "boba",
    
    # Food service
    "restaurant", "cafe", "coffee shop", "pizza", "burger", 
    "sandwich", "bakery", "food truck", "catering",
    
    # Bars
    "bar", "pub", "sports bar", "wine bar", "cocktail bar",
    "brewery", "taproom",
    
    # Retail with receipts
    "convenience store", "liquor store", "smoke shop", "vape shop"
]

class YelpProspectingScraper:
    def __init__(self):
        self.total_found = 0
        self.imported = 0
        self.skipped = 0
        self.errors = 0
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def search_yelp(self, term, location, limit=50):
        """Search Yelp for businesses"""
        headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
        url = 'https://api.yelp.com/v3/businesses/search'
        
        params = {
            'term': term,
            'location': location,
            'limit': limit,
            'sort_by': 'best_match'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('businesses', [])
            elif response.status_code == 429:
                self.log("⚠️ Rate limit hit - waiting 60s")
                time.sleep(60)
                return self.search_yelp(term, location, limit)
            else:
                self.log(f"Yelp API error: {response.status_code}")
                return []
        except Exception as e:
            self.log(f"Error: {e}")
            self.errors += 1
            return []
    
    def check_existing(self, yelp_id):
        """Check if business already exists"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT id FROM leads WHERE enrichment_data LIKE ?", (f'%"yelp_id": "{yelp_id}"%',))
        existing = c.fetchone()
        
        # Also check by name
        c.execute("SELECT id FROM leads WHERE tags LIKE '%yelp%' LIMIT 1")
        has_yelp = c.fetchone()
        
        conn.close()
        return existing is not None
    
    def import_business(self, business, term):
        """Import a business to DepotChaos"""
        yelp_id = business.get('id')
        name = business.get('name', '')
        phone = business.get('phone', '')
        rating = business.get('rating', 0)
        review_count = business.get('review_count', 0)
        
        # Location data
        location = business.get('location', {})
        address = ', '.join(location.get('display_address', []))
        city = location.get('city', '')
        state = location.get('state', '')
        zip_code = location.get('zip_code', '')
        
        # Categories
        categories = [c.get('title') for c in business.get('categories', [])]
        
        # Skip if exists
        if self.check_existing(yelp_id):
            self.skipped += 1
            return False
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        enrichment = {
            'yelp_id': yelp_id,
            'yelp_rating': rating,
            'yelp_reviews': review_count,
            'yelp_categories': categories,
            'search_term': term,
            'source': 'yelp_api',
            'scraped_at': datetime.now().isoformat()
        }
        
        # Determine business type
        business_type = 'Restaurant'
        if any('cafe' in c.lower() or 'coffee' in c.lower() for c in categories):
            business_type = 'Cafe'
        elif any('bar' in c.lower() or 'pub' in c.lower() for c in categories):
            business_type = 'Bar'
        elif any('mexican' in c.lower() or 'taco' in c.lower() for c in categories):
            business_type = 'Mexican Restaurant'
        elif any('asian' in c.lower() or 'thai' in c.lower() or 'korean' in c.lower() for c in categories):
            business_type = 'Asian Restaurant'
        
        c.execute("""
            INSERT INTO leads (
                business_name, city, state, zip, phone, address,
                business_type, category,
                source_type, created_at, tags,
                enrichment_data, enrichment_status, status, deleted
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Yelp API', 
                     datetime('now'), 'prospect,yelp',
                     ?, 'enriched', 'new', 0)
        """, (
            name, city, state, zip_code, phone, address,
            business_type, ', '.join(categories[:3]),
            json.dumps(enrichment)
        ))
        
        conn.commit()
        conn.close()
        
        self.imported += 1
        return True
    
    def run(self, cities=None, terms=None, max_per_city=50):
        """Run prospecting for all targets"""
        cities = cities or TARGET_CITIES[:10]  # Start with 10 cities
        terms = terms or PSDEPOT_TERMS[:8]  # Start with top categories
        
        self.log("="*60)
        self.log("🍜 YELP PROSPECTING SCRAPER - CALIFORNIA")
        self.log("="*60)
        self.log(f"Cities: {len(cities)}")
        self.log(f"Categories: {len(terms)}")
        self.log("")
        
        for city, state in cities:
            location = f"{city}, {state}"
            self.log(f"📍 {location}")
            
            city_count = 0
            for term in terms:
                try:
                    businesses = self.search_yelp(term, location, limit=max_per_city)
                    
                    for business in businesses:
                        if business.get('is_closed'):
                            continue
                        success = self.import_business(business, term)
                        if success:
                            city_count += 1
                            self.log(f"   ✅ {business.get('name')}")
                    
                    # Rate limiting - Yelp allows 5000/day
                    time.sleep(0.2)
                    
                except Exception as e:
                    self.log(f"   Error: {e}")
            
            self.log(f"   Imported: {city_count} | Total: {self.imported}")
            self.log("")
        
        self.log("="*60)
        self.log("📊 COMPLETE")
        self.log("="*60)
        self.log(f"Total imported: {self.imported}")
        self.log(f"Total skipped (duplicates): {self.skipped}")
        self.log(f"Errors: {self.errors}")
        self.log(f"Cities covered: {len(cities)}")

if __name__ == "__main__":
    scraper = YelpProspectingScraper()
    # Start with Sacramento area + Mexican/Asian food
    scraper.run(
        cities=[
            ("Sacramento", "CA"), ("Elk Grove", "CA"), ("Folsom", "CA"),
            ("Roseville", "CA"), ("Citrus Heights", "CA"), ("Davis", "CA"),
            ("Santa Rosa", "CA"), ("Napa", "CA"), ("Vallejo", "CA"),
            ("Stockton", "CA")
        ],
        terms=[
            "taqueria", "mexican restaurant", "taco",
            "thai restaurant", "vietnamese restaurant", "pho",
            "korean restaurant", "chinese restaurant", "sushi"
        ],
        max_per_city=30
    )
