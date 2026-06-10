#!/usr/bin/env python3
"""
McAlister's Deli Location Scraper
Scrapes all 30 state location pages and inserts into DepotChaos unified.db
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re
from datetime import datetime

# State URLs to scrape
STATE_URLS = [
    ("Alabama", "https://locations.mcalistersdeli.com/al"),
    ("Arizona", "https://locations.mcalistersdeli.com/az"),
    ("Arkansas", "https://locations.mcalistersdeli.com/ar"),
    ("Colorado", "https://locations.mcalistersdeli.com/co"),
    ("Florida", "https://locations.mcalistersdeli.com/fl"),
    ("Georgia", "https://locations.mcalistersdeli.com/ga"),
    ("Idaho", "https://locations.mcalistersdeli.com/id"),
    ("Illinois", "https://locations.mcalistersdeli.com/il"),
    ("Indiana", "https://locations.mcalistersdeli.com/in"),
    ("Iowa", "https://locations.mcalistersdeli.com/ia"),
    ("Kansas", "https://locations.mcalistersdeli.com/ks"),
    ("Kentucky", "https://locations.mcalistersdeli.com/ky"),
    ("Louisiana", "https://locations.mcalistersdeli.com/la"),
    ("Maryland", "https://locations.mcalistersdeli.com/md"),
    ("Michigan", "https://locations.mcalistersdeli.com/mi"),
    ("Minnesota", "https://locations.mcalistersdeli.com/mn"),
    ("Mississippi", "https://locations.mcalistersdeli.com/ms"),
    ("Missouri", "https://locations.mcalistersdeli.com/mo"),
    ("Nebraska", "https://locations.mcalistersdeli.com/ne"),
    ("New Mexico", "https://locations.mcalistersdeli.com/nm"),
    ("North Carolina", "https://locations.mcalistersdeli.com/nc"),
    ("North Dakota", "https://locations.mcalistersdeli.com/nd"),
    ("Ohio", "https://locations.mcalistersdeli.com/oh"),
    ("Oklahoma", "https://locations.mcalistersdeli.com/ok"),
    ("Pennsylvania", "https://locations.mcalistersdeli.com/pa"),
    ("South Carolina", "https://locations.mcalistersdeli.com/sc"),
    ("Tennessee", "https://locations.mcalistersdeli.com/tn"),
    ("Texas", "https://locations.mcalistersdeli.com/tx"),
    ("Utah", "https://locations.mcalistersdeli.com/ut"),
    ("Virginia", "https://locations.mcalistersdeli.com/va"),
    ("Wyoming", "https://locations.mcalistersdeli.com/wy"),
]

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def init_db():
    """Ensure database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def scrape_state_locations(state_name, url):
    """Scrape all locations from a state page"""
    locations = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        print(f"  Scraping {state_name}...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try different selectors for location cards
        selectors = [
            '.location-card',
            '.store-card',
            '.location-item',
            '[data-location]',
            '.listing-item',
            '.result-item',
            '.address-card',
        ]
        
        location_cards = []
        for selector in selectors:
            location_cards = soup.select(selector)
            if location_cards:
                break
        
        # If no cards found, look for city links and follow them
        if not location_cards:
            # Look for city links
            city_links = soup.select('a[href*="/al/"], a[href*="/az/"], a[href*="/ar/"], a[href*="/co/"], a[href*="/fl/"], a[href*="/ga/"], a[href*="/id/"], a[href*="/il/"], a[href*="/in/"], a[href*="/ia/"], a[href*="/ks/"], a[href*="/ky/"], a[href*="/la/"], a[href*="/md/"], a[href*="/mi/"], a[href*="/mn/"], a[href*="/ms/"], a[href*="/mo/"], a[href*="/ne/"], a[href*="/nm/"], a[href*="/nc/"], a[href*="/nd/"], a[href*="/oh/"], a[href*="/ok/"], a[href*="/pa/"], a[href*="/sc/"], a[href*="/tn/"], a[href*="/tx/"], a[href*="/ut/"], a[href*="/va/"], a[href*="/wy/"]')
            
            # Extract unique city URLs
            city_urls = set()
            for link in city_links:
                href = link.get('href', '')
                if href and href.count('/') >= 2:
                    full_url = urljoin(url, href)
                    city_urls.add(full_url)
            
            print(f"    Found {len(city_urls)} city pages to scrape...")
            
            for city_url in city_urls:
                try:
                    time.sleep(0.5)  # Be polite
                    city_response = requests.get(city_url, headers=headers, timeout=30)
                    city_soup = BeautifulSoup(city_response.text, 'html.parser')
                    
                    # Try to find location details on city page
                    for selector in selectors:
                        city_cards = city_soup.select(selector)
                        if city_cards:
                            for card in city_cards:
                                location = parse_location_card(card, state_name)
                                if location:
                                    locations.append(location)
                            break
                    
                    # If no cards, try parsing the whole page for single location
                    if not city_cards:
                        location = parse_page_for_location(city_soup, state_name)
                        if location:
                            locations.append(location)
                            
                except Exception as e:
                    print(f"    Error scraping {city_url}: {e}")
        else:
            # Parse found cards
            for card in location_cards:
                location = parse_location_card(card, state_name)
                if location:
                    locations.append(location)
        
        print(f"    Found {len(locations)} locations")
        return locations
        
    except Exception as e:
        print(f"  Error scraping {state_name}: {e}")
        return []

def parse_location_card(card, state_name):
    """Extract location data from a card element"""
    location = {
        'business_name': 'McAlister\'s Deli',
        'business_type': 'Restaurant - Fast Casual',
        'state': state_name,
        'source': 'McAlister\'s Deli Website',
        'source_type': 'web_scrape',
        'scraped_at': datetime.now().isoformat(),
        'priority': 'medium',
        'enrichment_status': 'pending',
        'status': 'new'
    }
    
    try:
        # Address
        address_elem = card.select_one('.address, .street-address, [itemprop="streetAddress"], .addr-line')
        if address_elem:
            location['address'] = address_elem.get_text(strip=True)
        
        # City
        city_elem = card.select_one('.city, .locality, [itemprop="addressLocality"]')
        if city_elem:
            location['city'] = city_elem.get_text(strip=True)
        
        # ZIP
        zip_elem = card.select_one('.zip, .postal-code, [itemprop="postalCode"]')
        if zip_elem:
            zip_match = re.search(r'\d{5}(-\d{4})?', zip_elem.get_text())
            if zip_match:
                location['zip'] = zip_match.group()
        
        # Phone
        phone_elem = card.select_one('.phone, .telephone, [itemprop="telephone"], [href^="tel:"]')
        if phone_elem:
            phone_text = phone_elem.get_text(strip=True) or phone_elem.get('href', '').replace('tel:', '')
            location['phone'] = clean_phone(phone_text)
        
        # Name/Location identifier
        name_elem = card.select_one('.name, .location-name, h2, h3, [itemprop="name"]')
        if name_elem:
            location_name = name_elem.get_text(strip=True)
            if location_name and location_name != "McAlister's Deli":
                location['business_name'] = f"McAlister's Deli - {location_name}"
        
        # Ensure we have minimum data
        if location.get('city') or location.get('phone'):
            return location
            
    except Exception as e:
        print(f"    Error parsing card: {e}")
    
    return None

def parse_page_for_location(soup, state_name):
    """Parse a full page for location details"""
    location = {
        'business_name': 'McAlister\'s Deli',
        'business_type': 'Restaurant - Fast Casual',
        'state': state_name,
        'source': 'McAlister\'s Deli Website',
        'source_type': 'web_scrape',
        'scraped_at': datetime.now().isoformat(),
        'priority': 'medium',
        'enrichment_status': 'pending',
        'status': 'new'
    }
    
    try:
        # Try to find address structured data
        address_elem = soup.select_one('[itemtype*="PostalAddress"], .address, address')
        if address_elem:
            # Street
            street = address_elem.select_one('[itemprop="streetAddress"], .street')
            if street:
                location['address'] = street.get_text(strip=True)
            
            # City
            city = address_elem.select_one('[itemprop="addressLocality"], .city')
            if city:
                location['city'] = city.get_text(strip=True)
            
            # ZIP
            zip_code = address_elem.select_one('[itemprop="postalCode"], .zip')
            if zip_code:
                zip_match = re.search(r'\d{5}(-\d{4})?', zip_code.get_text())
                if zip_match:
                    location['zip'] = zip_match.group()
        
        # Phone
        phone_elem = soup.select_one('[itemprop="telephone"], [href^="tel:"]')
        if phone_elem:
            phone_text = phone_elem.get_text(strip=True) or phone_elem.get('href', '').replace('tel:', '')
            location['phone'] = clean_phone(phone_text)
        
        # Location name from title or heading
        title = soup.select_one('title, h1')
        if title:
            title_text = title.get_text(strip=True)
            # Extract city name from title like "McAlister's Deli in Birmingham, AL"
            match = re.search(r'in\s+([^,]+)', title_text)
            if match:
                location['city'] = match.group(1).strip()
        
        if location.get('city') or location.get('phone'):
            return location
            
    except Exception as e:
        print(f"    Error parsing page: {e}")
    
    return None

def clean_phone(phone_text):
    """Clean phone number to standard format"""
    if not phone_text:
        return None
    # Remove non-numeric characters
    digits = re.sub(r'\D', '', phone_text)
    # Format as (XXX) XXX-XXXX if 10 digits
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    return phone_text.strip()

def insert_location(conn, location):
    """Insert a location into the leads table"""
    cursor = conn.cursor()
    
    try:
        # Check for duplicates by business_name, city, state
        cursor.execute("""
            SELECT id FROM leads 
            WHERE business_name = ? AND city = ? AND state = ?
        """, (location.get('business_name'), location.get('city'), location.get('state')))
        
        if cursor.fetchone():
            return False, "duplicate"
        
        # Insert new lead
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
    
    conn = init_db()
    
    total_locations = 0
    total_inserted = 0
    total_duplicates = 0
    total_errors = 0
    
    for state_name, url in STATE_URLS:
        print(f"\n[{state_name}]")
        
        locations = scrape_state_locations(state_name, url)
        
        for location in locations:
            success, status = insert_location(conn, location)
            if success:
                total_inserted += 1
            elif status == "duplicate":
                total_duplicates += 1
            else:
                total_errors += 1
        
        total_locations += len(locations)
        
        # Small delay between states
        time.sleep(1)
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)
    print(f"Total locations found: {total_locations}")
    print(f"Inserted: {total_inserted}")
    print(f"Duplicates skipped: {total_duplicates}")
    print(f"Errors: {total_errors}")

if __name__ == "__main__":
    main()
