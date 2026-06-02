#!/usr/bin/env python3
"""
Fix Teriyaki Madness field alignment issues and merge Yelp cache data
"""

import sqlite3
import json
import re

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
YELP_CACHE_PATH = "/root/.openclaw/workspace/DepotChaos/yelp_cache.json"

def load_yelp_cache():
    """Load Yelp enrichment data"""
    with open(YELP_CACHE_PATH) as f:
        return json.load(f)

def is_valid_email(text):
    """Check if text looks like an email"""
    if not text:
        return False
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', text))

def is_valid_address(text):
    """Check if text looks like an address"""
    if not text:
        return False
    # Address typically contains numbers, street keywords, or is long
    address_keywords = ['street', 'st', 'road', 'rd', 'avenue', 'ave', 'boulevard', 'blvd', 
                        'drive', 'dr', 'lane', 'ln', 'way', 'circle', 'ct', 'suite', 'unit',
                        'building', 'floor', 'apt', '#']
    text_lower = text.lower()
    has_number = bool(re.search(r'\d', text))
    has_keyword = any(kw in text_lower for kw in address_keywords)
    return has_number or has_keyword or len(text) > 20

def fix_teriyaki_records():
    """Fix field alignment and merge Yelp data"""
    
    yelp_cache = load_yelp_cache()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get all Teriyaki Madness records
    c.execute("""
        SELECT id, business_name, city, state, phone, email, address, 
               enrichment_data, contact_name
        FROM leads 
        WHERE business_name LIKE '%Teriyaki%Madness%'
    """)
    
    records = c.fetchall()
    fixed = 0
    merged_yelp = 0
    
    for record in records:
        (lead_id, business_name, city, state, phone, email, address, 
         enrichment_data, contact_name) = record
        
        changes = {}
        
        # Parse enrichment data
        try:
            enrich = json.loads(enrichment_data) if enrichment_data else {}
        except:
            enrich = {}
        
        # Fix field alignment issues
        # Check if email contains address data
        if email and is_valid_address(email) and not is_valid_email(email):
            # Email field has address data, swap it
            if not address or address == '0' or address == 'N/A':
                changes['address'] = email
                changes['email'] = ''  # Clear the email since it's not valid
            else:
                changes['address'] = email
                changes['email'] = ''
        
        # Check if address contains email
        if address and is_valid_email(address):
            changes['email'] = address
            changes['address'] = ''
        
        # Look up in Yelp cache
        # Try different key formats
        yelp_keys = [
            business_name.upper().replace(' ', '_').replace('-', '_') + '__',
            business_name.upper().replace(' - ', '_').replace(' ', '_').replace('-', '_') + '__',
            re.sub(r'[^A-Z0-9]', '_', business_name.upper()) + '__'
        ]
        
        yelp_data = None
        for key in yelp_keys:
            if key in yelp_cache:
                yelp_data = yelp_cache[key]
                break
        
        # Also try searching by business name in cache
        if not yelp_data:
            for cache_key, cache_data in yelp_cache.items():
                if cache_data and 'name' in cache_data:
                    if 'teriyaki madness' in cache_data['name'].lower():
                        # Check if city matches
                        if cache_data.get('city', '').lower() == city.lower():
                            yelp_data = cache_data
                            break
        
        if yelp_data:
            merged_yelp += 1
            
            # Extract Yelp data
            yelp_phone = yelp_data.get('phone', '').replace('+1', '')
            yelp_address = yelp_data.get('address', '')
            yelp_city = yelp_data.get('city', '')
            yelp_state = yelp_data.get('state', '')
            yelp_zip = yelp_data.get('zip', '')
            yelp_rating = yelp_data.get('rating', '')
            yelp_review_count = yelp_data.get('review_count', '')
            
            # Merge data (Yelp takes priority if current field is empty or looks wrong)
            if yelp_phone and (not phone or phone == 'N/A'):
                changes['phone'] = yelp_phone
            
            if yelp_address and (not address or address == '0' or address == 'N/A'):
                changes['address'] = yelp_address
            
            if yelp_city and (not city or city == 'N/A'):
                changes['city'] = yelp_city
            
            if yelp_state and (not state or state == 'O/S' or state == 'N/A'):
                changes['state'] = yelp_state
            
            # Update enrichment data with Yelp info
            enrich['yelp'] = {
                'phone': yelp_phone,
                'address': yelp_address,
                'city': yelp_city,
                'state': yelp_state,
                'zip': yelp_zip,
                'rating': yelp_rating,
                'review_count': yelp_review_count,
                'categories': yelp_data.get('categories', [])
            }
        
        # Apply changes
        if changes:
            fixed += 1
            
            # Build update query
            update_fields = []
            params = []
            
            for field, value in changes.items():
                update_fields.append(f"{field} = ?")
                params.append(value)
            
            # Update enrichment data
            update_fields.append("enrichment_data = ?")
            params.append(json.dumps(enrich))
            
            # Add lead_id to params
            params.append(lead_id)
            
            query = f"UPDATE leads SET {', '.join(update_fields)} WHERE id = ?"
            c.execute(query, params)
            
            print(f"Fixed {business_name}:")
            for field, value in changes.items():
                print(f"  - {field}: {value}")
    
    conn.commit()
    conn.close()
    
    print(f"\n=== Summary ===")
    print(f"Total Teriyaki Madness records processed: {len(records)}")
    print(f"Records fixed/updated: {fixed}")
    print(f"Records with Yelp data merged: {merged_yelp}")

if __name__ == "__main__":
    fix_teriyaki_records()
