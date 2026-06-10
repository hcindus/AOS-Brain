#!/usr/bin/env python3
"""
McAlister's Deli Scraper - Extract from HTML directly
"""

import subprocess
import re
import sqlite3
import json
from datetime import datetime
from urllib.parse import unquote

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

def extract_cities_from_html(html, state_code, state_name):
    """Extract city links and location counts from state page"""
    locations = []
    
    # Look for JSON data in the pageProps script
    jsonld_pattern = r'<script type="application/ld\+json">\s*({"@graph".*?})\s*</script>'
    jsonld_match = re.search(jsonld_pattern, html, re.DOTALL)
    
    if jsonld_match:
        try:
            data = json.loads(jsonld_match.group(1))
            if isinstance(data, dict) and '@graph' in data:
                for item in data['@graph']:
                    if item.get('@type') == 'BreadcrumbList':
                        for elem in item.get('itemListElement', []):
                            if elem.get('position') == 2:
                                # This is the state info
                                pass
        except:
            pass
    
    # Look for pageProps data in the script
    pageprops_pattern = r'"dm_directoryChildren":(\[.*?\])'
    pageprops_match = re.search(pageprops_pattern, html)
    
    if pageprops_match:
        try:
            cities_data = json.loads(pageprops_match.group(1))
            for city in cities_data:
                city_name = city.get('name', '')
                location_count = int(city.get('dm_baseEntityCount', 1))
                slug = city.get('slug', '')
                
                # Create a lead entry for the city
                location = {
                    'business_name': f"McAlister's Deli - {city_name}",
                    'business_type': 'Restaurant - Fast Casual',
                    'city': city_name,
                    'state': state_name,
                    'source': 'McAlister\'s Deli Website',
                    'source_type': 'web_scrape',
                    'scraped_at': datetime.now().isoformat(),
                    'priority': 'medium',
                    'enrichment_status': 'pending',
                    'status': 'new',
                    'location_count': location_count,
                    'slug': slug
                }
                locations.append(location)
        except Exception as e:
            print(f"    Error parsing JSON: {e}")
    
    # Fallback: extract from city links in HTML
    if not locations:
        city_pattern = rf'href="[^"]*{state_code.lower()}/([^"/]+)[^"]*"[^>]*data-count="\((\d+)\)"'
        city_matches = re.findall(city_pattern, html)
        
        for city_slug, count in city_matches:
            city_name = city_slug.replace('-', ' ').title()
            location = {
                'business_name': f"McAlister's Deli - {city_name}",
                'business_type': 'Restaurant - Fast Casual',
                'city': city_name,
                'state': state_name,
                'source': 'McAlister\'s Deli Website',
                'source_type': 'web_scrape',
                'scraped_at': datetime.now().isoformat(),
                'priority': 'medium',
                'enrichment_status': 'pending',
                'status': 'new',
                'location_count': int(count),
                'slug': f"{state_code.lower()}/{city_slug}"
            }
            locations.append(location)
    
    return locations

def insert_location(conn, location):
    """Insert into database"""
    cursor = conn.cursor()
    
    try:
        # Check for duplicates by business_name, city, state
        cursor.execute("""
            SELECT id FROM leads 
            WHERE business_name = ? AND city = ? AND state = ?
        """, (location.get('business_name'), location.get('city'), location.get('state')))
        
        if cursor.fetchone():
            return False, "duplicate"
        
        # Remove internal fields before insert
        loc_copy = {k: v for k, v in location.items() if k not in ['location_count', 'slug']}
        
        columns = ', '.join(loc_copy.keys())
        placeholders = ', '.join(['?' for _ in loc_copy])
        
        cursor.execute(f"""
            INSERT INTO leads ({columns})
            VALUES ({placeholders})
        """, list(loc_copy.values()))
        
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
        
        locations = extract_cities_from_html(html, state_code, state_name)
        
        print(f"  Found {len(locations)} cities with {sum(l['location_count'] for l in locations)} total locations")
        
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
    print(f"Total cities found: {total_found}")
    print(f"Inserted: {total_inserted}")
    print(f"Duplicates skipped: {total_duplicates}")

if __name__ == "__main__":
    main()
