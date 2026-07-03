#!/usr/bin/env python3
"""
Real Business Prospecting Scraper for PSDEPOT
Uses Google Places API to find actual businesses in target areas
"""

import sqlite3
import json
import time
import os
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

# Target cities for PSDEPOT
TARGET_CITIES = [
    # Sacramento Area
    "Sacramento, CA", "Elk Grove, CA", "Folsom, CA", "Roseville, CA",
    "Citrus Heights, CA", "Rancho Cordova, CA", "Carmichael, CA",
    "West Sacramento, CA", "Davis, CA", "Woodland, CA",
    
    # North Bay / Wine Country
    "Santa Rosa, CA", "Petaluma, CA", "Napa, CA", "Vallejo, CA",
    "Sonoma, CA", "Fairfield, CA", "Vacaville, CA", "American Canyon, CA",
    "Calistoga, CA", "St Helena, CA", "Windsor, CA", "Healdsburg, CA",
    "Novato, CA", "San Rafael, CA",
    
    # Stockton Area
    "Stockton, CA", "Lodi, CA", "Manteca, CA", "Tracy, CA",
    
    # Bay Area ( selective )
    "San Jose, CA", "Oakland, CA", "Fremont, CA", "Hayward, CA",
    "Concord, CA", "Berkeley, CA", "Richmond, CA"
]

# Business categories for PSDEPOT (receipt users)
PSDEPOT_CATEGORIES = [
    # Mexican Food
    "taqueria", "carniceria", "panaderia", "tortilleria", "bodega",
    "mexican restaurant", "taco shop", "burrito place",
    
    # Asian Food
    "thai restaurant", "korean restaurant", "vietnamese restaurant",
    "pho restaurant", "chinese restaurant", "sushi restaurant",
    "japanese restaurant", "filipino restaurant", "indian restaurant",
    "bubble tea", "boba tea",
    
    # Other Food
    "restaurant", "cafe", "coffee shop", "pizza restaurant",
    "burger restaurant", "sandwich shop", "deli",
    "ice cream shop", "frozen yogurt", "bakery",
    "juice bar", "smoothie shop", "food truck",
    
    # Bars
    "bar", "pub", "sports bar", "wine bar", "cocktail bar",
    "brewery", "taproom",
    
    # Retail with receipts
    "convenience store", "liquor store", "gas station",
    "dispensary", "vape shop", "smoke shop",
    "cell phone repair", "florist", "gift shop"
]

class RealProspectingScraper:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('GOOGLE_PLACES_API_KEY')
        self.total_found = 0
        self.imported = 0
        self.skipped = 0
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def search_places(self, query, location, radius=5000):
        """Search Google Places for businesses"""
        if not self.api_key:
            self.log("❌ No Google Places API key configured")
            return []
        
        import requests
        
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': f"{query} in {location}",
            'key': self.api_key,
            'radius': radius
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if data.get('status') == 'OK':
                return data.get('results', [])
            else:
                self.log(f"API Error: {data.get('status')}")
                return []
        except Exception as e:
            self.log(f"Error: {e}")
            return []
    
    def get_place_details(self, place_id):
        """Get detailed info about a place"""
        if not self.api_key:
            return None
        
        import requests
        
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_phone_number,formatted_address,website,types,business_status',
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if data.get('status') == 'OK':
                return data.get('result', {})
            return None
        except:
            return None
    
    def check_existing(self, name, address):
        """Check if business already exists"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
            SELECT id FROM leads 
            WHERE business_name = ? OR address = ?
            LIMIT 1
        """, (name, address))
        
        existing = c.fetchone()
        conn.close()
        return existing is not None
    
    def import_business(self, place_data, category):
        """Import a business to DepotChaos"""
        name = place_data.get('name', '')
        address = place_data.get('formatted_address', '')
        phone = place_data.get('formatted_phone_number', '')
        website = place_data.get('website', '')
        place_id = place_data.get('place_id', '')
        
        # Skip if exists
        if self.check_existing(name, address):
            self.skipped += 1
            return False
        
        # Parse address
        addr_parts = address.split(',')
        city = state_zip = ""
        if len(addr_parts) >= 2:
            city = addr_parts[-2].strip() if len(addr_parts) > 2 else ""
            state_zip = addr_parts[-1].strip() if addr_parts else ""
        
        state = "CA"
        zip_code = ""
        if state_zip:
            parts = state_zip.split()
            if len(parts) >= 2:
                state = parts[0]
                zip_code = parts[1]
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        enrichment = {
            'place_id': place_id,
            'website': website,
            'category': category,
            'source': 'google_places_api',
            'scraped_at': datetime.now().isoformat()
        }
        
        c.execute("""
            INSERT INTO leads (
                business_name, city, state, zip, phone, address, website,
                business_type, category, source_type, created_at, tags,
                enrichment_data, enrichment_status, status, deleted
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Google Places API', 
                     datetime('now'), 'prospect,real_data',
                     ?, 'enriched', 'new', 0)
        """, (
            name, city, state, zip_code, phone, address, website,
            category.replace('_', ' ').title(),
            category,
            json.dumps(enrichment)
        ))
        
        conn.commit()
        conn.close()
        
        self.imported += 1
        return True
    
    def run(self, cities=None, categories=None, max_per_city=20):
        """Run prospecting for all targets"""
        cities = cities or TARGET_CITIES[:5]  # Start with first 5
        categories = categories or PSDEPOT_CATEGORIES[:10]  # Start with first 10
        
        self.log("="*60)
        self.log("🚀 REAL BUSINESS PROSPECTING SCRAPER")
        self.log("="*60)
        
        if not self.api_key:
            self.log("❌ ERROR: Google Places API key required")
            self.log("Set GOOGLE_PLACES_API_KEY environment variable")
            return
        
        self.log(f"Cities to search: {len(cities)}")
        self.log(f"Categories: {len(categories)}")
        self.log("")
        
        for city in cities:
            self.log(f"📍 Searching: {city}")
            
            for category in categories:
                try:
                    places = self.search_places(category, city)
                    
                    for place in places[:max_per_city]:
                        place_id = place.get('place_id')
                        if place_id:
                            details = self.get_place_details(place_id)
                            if details:
                                success = self.import_business(details, category)
                                if success:
                                    self.log(f"   ✅ {details.get('name')}")
                    
                    # Rate limiting
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.log(f"   Error with {category}: {e}")
            
            self.log(f"   Progress: {self.imported} imported, {self.skipped} skipped")
        
        self.log("")
        self.log("="*60)
        self.log("📊 SCRAPING COMPLETE")
        self.log("="*60)
        self.log(f"Total imported: {self.imported}")
        self.log(f"Total skipped (duplicates): {self.skipped}")
        self.log(f"Cities covered: {len(cities)}")
        self.log(f"Categories: {len(categories)}")

if __name__ == "__main__":
    scraper = RealProspectingScraper()
    # Start with small batch for testing
    scraper.run(
        cities=["Sacramento, CA", "Elk Grove, CA", "Roseville, CA"],
        categories=["taqueria", "mexican restaurant", "cafe", "restaurant", "bar"],
        max_per_city=10
    )
