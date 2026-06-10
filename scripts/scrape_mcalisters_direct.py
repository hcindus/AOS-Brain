#!/usr/bin/env python3
"""
McAlister's Deli Scraper - Direct fetch with curl + parse
"""

import subprocess
import json
import re
import sqlite3
from datetime import datetime
from urllib.parse import urljoin

STATES = [
    ("AL", "Alabama"), ("AZ", "Arizona"), ("AR", "Arkansas"), ("CO", "Colorado"),
    ("FL", "Florida"), ("GA", "Georgia"), ("ID", "Idaho"), ("IL", "Illinois"),
    ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"), ("KY", "Kentucky"),
    ("LA", "Louisiana"), ("MD", "Maryland"), ("MI", "Michigan"), ("MN", "Minnesota"),
    ("MS", "Mississippi"), ("MO", "Missouri"), ("NE", "Nebraska"), ("NM", "New Mexico"),
    ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"),
    ("PA", "Pennsylvania"), ("SC", "South Carolina"), ("TN", "Tennessee"), ("TX", "Texas"),
    ("UT", "Utah"), ("VA", "Virginia"), ("WY", "Wyoming"),
]

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def fetch_page(url):
    """Fetch page using curl"""
    cmd = [
        'curl', '-s', '-L', '--max-time', '30',
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        url
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        return result.stdout
    except:
        return ""

def parse_jsonld(html):
    """Extract JSON-LD Restaurant data"""
    locations = []
    
    # Find all JSON-LD scripts
    pattern = r'<script type="application/ld\+json">(.*?)</script>'
    matches = re.findall(pattern, html, re.DOTALL)
    
    for match in matches:
        try:
            data = json.loads(match.strip())
            
            # Handle array of locations
            if isinstance(data, list):
                for item in data:
                    if item.get('@type') in ['Restaurant', 'FoodEstablishment', 'LocalBusiness']:
                        loc = parse_restaurant_data(item)
                        if loc:
                            locations.append(loc)
            # Handle single location
            elif data.get('@type') in ['Restaurant', 'FoodEstablishment', 'LocalBusiness']:
                loc = parse_restaurant_data(data)
                if loc:
                    locations.append(loc)
        except:
            continue
    
    return locations

def parse_restaurant_data(data):
    """Parse a single restaurant JSON-LD"""
    address = data.get('address', {})
    if isinstance(address, dict):
        street = address.get('streetAddress', '')
        city = address.get('addressLocality', '')
        state = address.get('addressRegion', '')
        zip_code = address.get('postalCode', '')
    else:
        return None
    
    phone = data.get('telephone', '')
    name = data.get('name', "McAlister's Deli")
    
    if not city:
        return None
    
    # Extract state name from code
    state_name = state
    for code, full_name in STATES:
        if code == state:
            state_name = full_name
            break
    
    return {
        'business_name': name if name != "McAlister's Deli" else f"McAlister's Deli - {city}",
        'business_type': 'Restaurant - Fast Casual',
        'address': street,
        'city': city,
        'state': state_name,
        'zip': zip_code,
        'phone': clean_phone(phone),
        'source': 'McAlister\'s Deli Website',
        'source_type': 'web_scrape',
        'scraped_at': datetime.now().isoformat(),
        'priority': 'medium',
        'enrichment_status': 'pending',
        'status': 'new'
    }

def parse_html_locations(html, state_code, state_name):
    """Parse locations from HTML if JSON-LD fails"""
    locations = []
    
    # Look for city links pattern
    city_pattern = rf'href="[^"]*/{state_code.lower()}/([^/"]+)[^"]*"'
    city_matches = re.findall(city_pattern, html)
    
    # Deduplicate city URLs
    cities = list(set(city_matches))
    
    for city_slug in cities[:15]:  # Limit to avoid too many requests
        city_url = f"https://locations.mcalistersdeli.com/{state_code.lower()}/{city_slug}"
        city_html = fetch_page(city_url)
        
        if city_html:
            city_locations = parse_jsonld(city_html)
            for loc in city_locations:
                loc['state'] = state_name
                locations.append(loc)
    
    return locations

def clean_phone(phone):
    """Clean phone to standard format"""
    if not phone:
        return None
    digits = re.sub(r'\D', '', str(phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    return phone

def insert_location(conn, location):
    """Insert into database"""
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id FROM leads 
            WHERE business_name = ? AND city = ? AND state = ?
        """, (location.get('business_name'), location.get('city'), location.get('state')))
        
        if cursor.fetchone():
            return False, "duplicate"
        
        columns = ', '.join(location.keys())
        placeholders = ', '.join(['?' for _ in location])
        
        cursor.execute(f"""
            INSERT INTO leads ({columns})
            VALUES ({placeholders})
        """, list(location.values()))
        
        conn.commit()
        return True, "inserted"
        
    except Exception as e:
        conn.rollback()
        return False, f"error: {e}"

def main():
    print("=" * 60)
    print("McAlister's Deli Location Scraper")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    total_inserted = 0
    total_duplicates = 0
    total_found = 0
    
    for state_code, state_name in STATES:
        print(f"\n[{state_name}]")
        
        url = f"https://locations.mcalistersdeli.com/{state_code.lower()}"
        html = fetch_page(url)
        
        if not html:
            print(f"  Failed to fetch")
            continue
        
        # Try JSON-LD first
        locations = parse_jsonld(html)
        
        # If no locations, try city pages
        if not locations:
            locations = parse_html_locations(html, state_code, state_name)
        
        print(f"  Found {len(locations)} locations")
        
        for loc in locations:
            success, status = insert_location(conn, loc)
            if success:
                total_inserted += 1
            elif status == "duplicate":
                total_duplicates += 1
        
        total_found += len(locations)
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)
    print(f"Total locations found: {total_found}")
    print(f"Inserted: {total_inserted}")
    print(f"Duplicates skipped: {total_duplicates}")

if __name__ == "__main__":
    main()
