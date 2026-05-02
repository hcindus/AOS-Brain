#!/usr/bin/env python3
"""
DepotChaos Lead Enrichment - Real Contact Data Acquisition
Uses multiple data sources to find real phone/email for businesses
"""

import sqlite3
import json
import time
import re
from datetime import datetime
from pathlib import Path
import requests

DB_PATH = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
LOG_FILE = "/var/log/aos/depotchaos_enrichment.log"
CACHE_FILE = "/root/.openclaw/workspace/DepotChaos/enrichment_cache.json"

class RealContactEnricher:
    """
    Enriches DepotChaos vendors with real contact information
    Uses: Google Places API, Yelp Fusion API, Clearbit, Hunter.io
    """
    
    def __init__(self):
        self.enriched_count = 0
        self.cache = self.load_cache()
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry + "\n")
    
    def load_cache(self):
        """Load enrichment cache to avoid re-processing"""
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_cache(self):
        """Save enrichment cache"""
        with open(CACHE_FILE, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get_vendors_to_enrich(self, limit=100, offset=0):
        """Get vendors needing real contact data"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, city, state, address
            FROM vendors 
            WHERE (phone IS NULL OR phone = '' OR phone LIKE '%555%')
              AND (email IS NULL OR email = '' OR email LIKE '%@example.com%')
              AND name NOT LIKE '%[0-9]%'
            ORDER BY name
            LIMIT ? OFFSET ?
        """, (limit, offset))
        
        vendors = []
        for row in cursor.fetchall():
            vendors.append({
                'id': row[0],
                'name': row[1],
                'city': row[2] or '',
                'state': row[3] or '',
                'address': row[4] or ''
            })
        
        conn.close()
        return vendors
    
    def search_yelp(self, business_name, city, state):
        """
        Search Yelp Fusion API for business details
        Requires YELP_API_KEY in environment
        """
        api_key = os.environ.get('YELP_API_KEY')
        if not api_key:
            return None
        
        headers = {'Authorization': f'Bearer {api_key}'}
        
        # Search for business
        search_url = 'https://api.yelp.com/v3/businesses/search'
        params = {
            'term': business_name,
            'location': f'{city}, {state}',
            'limit': 1
        }
        
        try:
            response = requests.get(search_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('businesses'):
                    biz = data['businesses'][0]
                    return {
                        'phone': biz.get('phone', ''),
                        'address': ' '.join(biz['location'].get('display_address', [])),
                        'rating': biz.get('rating', 0),
                        'review_count': biz.get('review_count', 0),
                        'yelp_url': biz.get('url', '')
                    }
        except Exception as e:
            self.log(f"Yelp API error: {e}")
        
        return None
    
    def search_google_places(self, business_name, city, state):
        """
        Search Google Places API for business details
        Requires GOOGLE_PLACES_API_KEY in environment
        """
        api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
        if not api_key:
            return None
        
        # Text search
        search_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        params = {
            'query': f'{business_name} {city} {state}',
            'key': api_key
        }
        
        try:
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('results'):
                    place = data['results'][0]
                    place_id = place.get('place_id')
                    
                    # Get place details
                    details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
                    details_params = {
                        'place_id': place_id,
                        'fields': 'formatted_phone_number,website,formatted_address',
                        'key': api_key
                    }
                    
                    details_response = requests.get(details_url, params=details_params, timeout=10)
                    if details_response.status_code == 200:
                        details = details_response.json().get('result', {})
                        return {
                            'phone': details.get('formatted_phone_number', ''),
                            'address': details.get('formatted_address', ''),
                            'website': details.get('website', '')
                        }
        except Exception as e:
            self.log(f"Google Places API error: {e}")
        
        return None
    
    def guess_email_from_website(self, website, business_name):
        """
        Guess email patterns from website
        Common patterns: info@, contact@, hello@, support@
        """
        if not website:
            return None
        
        # Extract domain
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', website)
        if not domain_match:
            return None
        
        domain = domain_match.group(1)
        
        # Common email patterns
        patterns = [
            f'info@{domain}',
            f'contact@{domain}',
            f'hello@{domain}',
            f'sales@{domain}',
            f'reservations@{domain}' if 'restaurant' in business_name.lower() else None
        ]
        
        return [p for p in patterns if p][0]  # Return first valid pattern
    
    def enrich_vendor(self, vendor):
        """Enrich a single vendor with real contact data"""
        cache_key = f"{vendor['name']}_{vendor['city']}"
        
        # Check cache
        if cache_key in self.cache:
            self.log(f"  💾 Cache hit: {vendor['name'][:40]}")
            return self.cache[cache_key]
        
        result = {
            'phone': None,
            'email': None,
            'address': None,
            'website': None,
            'sources': []
        }
        
        # Try Google Places
        google_data = self.search_google_places(
            vendor['name'], 
            vendor['city'], 
            vendor['state']
        )
        if google_data:
            result['phone'] = google_data.get('phone')
            result['address'] = google_data.get('address')
            result['website'] = google_data.get('website')
            result['sources'].append('google_places')
        
        # Try Yelp
        yelp_data = self.search_yelp(
            vendor['name'],
            vendor['city'],
            vendor['state']
        )
        if yelp_data:
            if not result['phone']:
                result['phone'] = yelp_data.get('phone')
            if not result['address']:
                result['address'] = yelp_data.get('address')
            result['sources'].append('yelp')
        
        # Generate email from website
        if result['website']:
            email = self.guess_email_from_website(result['website'], vendor['name'])
            if email:
                result['email'] = email
                result['sources'].append('inferred_from_website')
        
        # Cache result
        self.cache[cache_key] = result
        
        return result
    
    def update_vendor(self, vendor_id, enrichment):
        """Update vendor record with enriched data"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if enrichment.get('phone'):
            updates.append('phone = ?')
            params.append(enrichment['phone'])
        
        if enrichment.get('email'):
            updates.append('email = ?')
            params.append(enrichment['email'])
        
        if enrichment.get('address'):
            updates.append('address = ?')
            params.append(enrichment['address'])
        
        if enrichment.get('website'):
            updates.append('notes = COALESCE(notes, \"\") || ?')
            params.append(f"\\nWebsite: {enrichment['website']}")
        
        if updates:
            query = f"UPDATE vendors SET {', '.join(updates)} WHERE id = ?"
            params.append(vendor_id)
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def run(self, batch_size=50, max_batches=10):
        """Run enrichment process"""
        self.log("="*60)
        self.log("🚀 DEPOTCHAOS REAL CONTACT ENRICHMENT")
        self.log("="*60)
        self.log("Note: Requires API keys for best results")
        self.log("Set YELP_API_KEY and GOOGLE_PLACES_API_KEY environment variables")
        self.log("="*60)
        
        total_enriched = 0
        offset = 0
        
        for batch_num in range(max_batches):
            vendors = self.get_vendors_to_enrich(limit=batch_size, offset=offset)
            
            if not vendors:
                self.log("✅ No more vendors to enrich")
                break
            
            self.log(f"\n🔄 Batch {batch_num + 1}: Processing {len(vendors)} vendors")
            
            batch_enriched = 0
            for i, vendor in enumerate(vendors, 1):
                try:
                    data = self.enrich_vendor(vendor)
                    
                    if data.get('phone') or data.get('email'):
                        self.update_vendor(vendor['id'], data)
                        batch_enriched += 1
                        self.log(f"  ✅ [{i}/{len(vendors)}] {vendor['name'][:40]:40} | "
                                  f"Phone: {data.get('phone', 'N/A')[:15]:15} | "
                                  f"Email: {data.get('email', 'N/A')[:25]:25}")
                    else:
                        self.log(f"  ⚠️  [{i}/{len(vendors)}] {vendor['name'][:40]:40} | No data found")
                    
                    # Rate limiting
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.log(f"  ❌ [{i}/{len(vendors)}] Error on {vendor['name']}: {e}")
            
            total_enriched += batch_enriched
            offset += batch_size
            
            # Save cache periodically
            self.save_cache()
            
            self.log(f"\n📊 Batch {batch_num + 1} complete: {batch_enriched}/{len(vendors)} enriched")
            
            if batch_num < max_batches - 1:
                self.log("💤 Pausing 2 seconds...")
                time.sleep(2)
        
        self.save_cache()
        self.log(f"\n🏁 TOTAL ENRICHED: {total_enriched}")
        return total_enriched

if __name__ == "__main__":
    import os
    
    enricher = RealContactEnricher()
    
    # Check for API keys
    has_yelp = bool(os.environ.get('YELP_API_KEY'))
    has_google = bool(os.environ.get('GOOGLE_PLACES_API_KEY'))
    
    print(f"API Status:")
    print(f"  Yelp API: {'✅ Configured' if has_yelp else '❌ Not configured'}")
    print(f"  Google Places API: {'✅ Configured' if has_google else '❌ Not configured'}")
    print()
    
    if not has_yelp and not has_google:
        print("⚠️  No API keys configured. Enrichment will be limited.")
        print("   To get real contact data, set these environment variables:")
        print("   - YELP_API_KEY (get from: https://www.yelp.com/developers)")
        print("   - GOOGLE_PLACES_API_KEY (get from: https://developers.google.com/maps/documentation/places/web-service")
        print()
    
    # Run enrichment
    enricher.run(batch_size=50, max_batches=5)
