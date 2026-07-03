#!/usr/bin/env python3
"""
Verify ABC business names against Yelp
Find real business names for generic/suspicious entries
"""

import sqlite3
import json
import time
import os
import requests
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
CACHE_FILE = "/root/.openclaw/workspace/DepotChaos/yelp_cache.json"

YELP_API_KEY = os.environ.get('YELP_API_KEY', '5DUaC-eBObfSXkjf4YfLNlViO-WqwwCk0UJYewfhav25gbTrCaPvPR_nhokKyfBNKnduMHkqd5Z_v_0RwHSj2fXs8ziaJ-O_RAkuRvc6L6Lt9dwEboKoYHBpBuL1aXYx')

# Generic words to check
GENERIC_WORDS = ['Tavern', 'Chophouse', 'Bar', 'Pub', 'Lounge', 'Cafe', 'Eatery', 
                 'Bistro', 'Restaurant', 'Kitchen', 'House', 'Diner', 'Spot', 
                 'Corner', 'Place', 'Grill']

class YelpVerifier:
    def __init__(self):
        self.verified_count = 0
        self.not_found = 0
        self.errors = 0
        self.cache = self.load_cache()
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def load_cache(self):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_cache(self):
        with open(CACHE_FILE, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def search_yelp_by_phone(self, phone):
        """Search Yelp by phone number"""
        if not phone:
            return None
        
        # Clean phone
        clean_phone = phone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        if len(clean_phone) == 10:
            clean_phone = '+1' + clean_phone
        elif len(clean_phone) == 11 and clean_phone[0] == '1':
            clean_phone = '+' + clean_phone
        
        cache_key = f"phone_{clean_phone}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
        url = 'https://api.yelp.com/v3/businesses/search/phone'
        
        try:
            response = requests.get(url, headers=headers, params={'phone': clean_phone}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                businesses = data.get('businesses', [])
                if businesses:
                    b = businesses[0]
                    result = {
                        'name': b.get('name'),
                        'phone': b.get('phone', ''),
                        'address': ' '.join(b.get('location', {}).get('display_address', [])),
                        'city': b.get('location', {}).get('city', ''),
                        'state': b.get('location', {}).get('state', ''),
                        'zip': b.get('location', {}).get('zip_code', ''),
                        'rating': b.get('rating', 0),
                        'review_count': b.get('review_count', 0),
                        'categories': [c.get('title') for c in b.get('categories', [])]
                    }
                    self.cache[cache_key] = result
                    return result
            self.cache[cache_key] = None
            return None
        except Exception as e:
            self.log(f"Error: {e}")
            return None
    
    def get_suspicious_records(self, limit=50):
        """Get ABC records with generic/suspicious names"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        placeholders = ','.join(['?' for _ in GENERIC_WORDS])
        
        c.execute(f"""
            SELECT id, business_name, city, county, state, phone, address, zip
            FROM ca_abc_licenses
            WHERE county IN ('Sacramento', 'Placer', 'Yolo', 'Sonoma', 'Napa', 'Solano')
              AND (business_name IN ({placeholders})
                   OR business_name LIKE '%0'
                   OR business_name LIKE '%1'
                   OR business_name LIKE '%2'
                   OR business_name LIKE '%3'
                   OR business_name LIKE '%4'
                   OR business_name LIKE '%5'
                   OR business_name LIKE '%6'
                   OR business_name LIKE '%7'
                   OR business_name LIKE '%8'
                   OR business_name LIKE '%9'
                   OR business_name LIKE '% Inc%'
                   OR business_name LIKE '% LLC%'
                   OR business_name LIKE '% Corp%'
                   OR business_name LIKE '%Group%'
                   OR business_name LIKE '%Co %')
              AND phone IS NOT NULL
              AND phone != ''
            LIMIT ?
        """, GENERIC_WORDS + [limit])
        
        records = c.fetchall()
        conn.close()
        return records
    
    def verify_record(self, record):
        """Verify a single record"""
        id_, name, city, county, state, phone, address, zip_code = record
        
        self.log(f"🔍 Checking: {name} | {phone} | {city}")
        
        # Try phone lookup first (most reliable)
        yelp_data = self.search_yelp_by_phone(phone)
        
        if yelp_data:
            self.log(f"   ✅ Found: {yelp_data.get('name')}")
            self.log(f"   📍 Address: {yelp_data.get('address')}")
            self.log(f"   ⭐ Rating: {yelp_data.get('rating')} ({yelp_data.get('review_count')} reviews)")
            return yelp_data
        else:
            self.log(f"   ⚠️ Not found on Yelp")
            return None
    
    def update_record(self, id_, yelp_data, original_name):
        """Update ABC record with verified data"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Build enrichment data
        enrichment = {
            'original_name': original_name,
            'yelp_verified_name': yelp_data.get('name'),
            'yelp_address': yelp_data.get('address'),
            'yelp_rating': yelp_data.get('rating'),
            'yelp_reviews': yelp_data.get('review_count'),
            'yelp_categories': yelp_data.get('categories'),
            'verified_at': datetime.now().isoformat()
        }
        
        c.execute("""
            UPDATE ca_abc_licenses
            SET business_name = ?,
                address = COALESCE(NULLIF(address, ''), ?),
                city = COALESCE(NULLIF(city, ''), ?),
                state = COALESCE(NULLIF(state, ''), ?),
                zip = COALESCE(NULLIF(zip, ''), ?),
                notes = COALESCE(notes, '') || ?
            WHERE id = ?
        """, (
            yelp_data.get('name'),
            yelp_data.get('address'),
            yelp_data.get('city'),
            yelp_data.get('state'),
            yelp_data.get('zip'),
            f"\n[YELP VERIFIED {datetime.now().strftime('%Y-%m-%d')}] Original: {original_name}",
            id_
        ))
        
        conn.commit()
        conn.close()
    
    def run(self, batch_size=25):
        """Run verification batch"""
        self.log("="*60)
        self.log("🔍 YELP VERIFICATION FOR ABC DATA")
        self.log("="*60)
        
        records = self.get_suspicious_records(limit=batch_size)
        
        if not records:
            self.log("No suspicious records found")
            return
        
        self.log(f"Found {len(records)} records to verify")
        
        for i, record in enumerate(records, 1):
            try:
                id_, name, city, county, state, phone, address, zip_code = record
                
                yelp_data = self.verify_record(record)
                
                if yelp_data:
                    self.update_record(id_, yelp_data, name)
                    self.verified_count += 1
                else:
                    self.not_found += 1
                
                # Rate limit
                time.sleep(0.5)
                
            except Exception as e:
                self.log(f"Error: {e}")
                self.errors += 1
        
        self.save_cache()
        
        self.log(f"\n📊 COMPLETE")
        self.log(f"   Verified & Updated: {self.verified_count}")
        self.log(f"   Not Found: {self.not_found}")
        self.log(f"   Errors: {self.errors}")

if __name__ == "__main__":
    verifier = YelpVerifier()
    verifier.run(batch_size=25)
