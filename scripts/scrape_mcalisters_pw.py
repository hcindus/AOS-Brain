#!/usr/bin/env python3
"""
McAlister's Deli Location Scraper - Playwright Version
Uses headless browser to handle JavaScript-rendered content
"""

import asyncio
import sqlite3
import re
from datetime import datetime
from playwright.async_api import async_playwright

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

async def scrape_mcalisters():
    """Main scraping function"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        total_inserted = 0
        total_duplicates = 0
        total_locations = 0
        
        for state_name, url in STATE_URLS:
            print(f"\n[{state_name}]")
            
            try:
                page = await context.new_page()
                await page.goto(url, wait_until='networkidle', timeout=60000)
                
                # Wait for page to load
                await asyncio.sleep(3)
                
                # Try multiple selectors for location data
                locations = await extract_locations_from_page(page, state_name)
                
                await page.close()
                
                print(f"  Found {len(locations)} locations")
                
                for location in locations:
                    success, status = insert_location(conn, location)
                    if success:
                        total_inserted += 1
                    elif status == "duplicate":
                        total_duplicates += 1
                    
                total_locations += len(locations)
                
            except Exception as e:
                print(f"  Error: {e}")
                continue
        
        await browser.close()
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)
    print(f"Total locations found: {total_locations}")
    print(f"Inserted: {total_inserted}")
    print(f"Duplicates skipped: {total_duplicates}")

async def extract_locations_from_page(page, state_name):
    """Extract location data from a page"""
    locations = []
    
    # Try to find location cards/links
    selectors_to_try = [
        '.location-card',
        '.store-card', 
        '.location-item',
        '[data-location]',
        '.listing-item',
        '.result-item',
        '.address-card',
        '.card',
        'article',
        '.location',
        '.store',
    ]
    
    for selector in selectors_to_try:
        try:
            cards = await page.query_selector_all(selector)
            if cards:
                print(f"    Using selector: {selector}")
                for card in cards:
                    location = await parse_card(card, state_name)
                    if location:
                        locations.append(location)
                break
        except:
            continue
    
    # If no cards found, look for JSON-LD or structured data
    if not locations:
        try:
            # Try to extract from JSON-LD
            jsonld_scripts = await page.query_selector_all('script[type="application/ld+json"]')
            for script in jsonld_scripts:
                content = await script.text_content()
                if 'Restaurant' in content or 'LocalBusiness' in content:
                    import json
                    try:
                        data = json.loads(content)
                        if isinstance(data, list):
                            for item in data:
                                location = parse_jsonld_location(item, state_name)
                                if location:
                                    locations.append(location)
                        else:
                            location = parse_jsonld_location(data, state_name)
                            if location:
                                locations.append(location)
                    except:
                        pass
        except Exception as e:
            print(f"    JSON-LD extraction error: {e}")
    
    # If still no locations, try to extract city links and visit them
    if not locations:
        try:
            # Look for links to city pages
            city_links = await page.query_selector_all(f'a[href*="/{url.split("/")[-1]}/"]')
            print(f"    Found {len(city_links)} potential city links")
            
            for link in city_links[:20]:  # Limit to avoid too many requests
                href = await link.get_attribute('href')
                if href and href.count('/') >= 4:
                    try:
                        city_page = await page.context.new_page()
                        await city_page.goto(href, wait_until='networkidle', timeout=30000)
                        await asyncio.sleep(2)
                        
                        # Try to get location from city page
                        location = await extract_single_location(city_page, state_name)
                        if location:
                            locations.append(location)
                        
                        await city_page.close()
                    except:
                        pass
        except Exception as e:
            print(f"    City link extraction error: {e}")
    
    return locations

async def parse_card(card, state_name):
    """Parse a location card element"""
    location = {
        'business_name': "McAlister's Deli",
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
        # Try to get text content and parse
        text = await card.text_content()
        
        # Look for address patterns
        address_match = re.search(r'(\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way))', text, re.I)
        if address_match:
            location['address'] = address_match.group(1).strip()
        
        # Look for phone number
        phone_match = re.search(r'(\(\d{3}\)\s*\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\d{10})', text)
        if phone_match:
            location['phone'] = clean_phone(phone_match.group(1))
        
        # Look for city, state, zip
        csz_match = re.search(r'([\w\s]+),?\s*[A-Za-z]{2}\s*(\d{5}(-\d{4})?)', text)
        if csz_match:
            location['city'] = csz_match.group(1).strip()
            location['zip'] = csz_match.group(2)
        
        if location.get('city') or location.get('phone'):
            return location
            
    except Exception as e:
        pass
    
    return None

async def extract_single_location(page, state_name):
    """Extract a single location from a detail page"""
    location = {
        'business_name': "McAlister's Deli",
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
        # Try structured data
        jsonld_scripts = await page.query_selector_all('script[type="application/ld+json"]')
        for script in jsonld_scripts:
            content = await script.text_content()
            try:
                import json
                data = json.loads(content)
                if data.get('@type') in ['Restaurant', 'FoodEstablishment', 'LocalBusiness']:
                    address = data.get('address', {})
                    if isinstance(address, dict):
                        location['address'] = address.get('streetAddress', '')
                        location['city'] = address.get('addressLocality', '')
                        location['zip'] = address.get('postalCode', '')
                    location['phone'] = data.get('telephone', '')
                    
                    if data.get('name') and data['name'] != "McAlister's Deli":
                        location['business_name'] = f"McAlister's Deli - {data['name']}"
                    break
            except:
                pass
        
        # Try to get from address element
        if not location.get('city'):
            address_elem = await page.query_selector('address, [itemprop="address"], .address')
            if address_elem:
                text = await address_elem.text_content()
                # Parse address text
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                if lines:
                    location['address'] = lines[0]
                    if len(lines) > 1:
                        csz_match = re.search(r'([\w\s]+),?\s*[A-Za-z]{2}\s*(\d{5})', lines[-1])
                        if csz_match:
                            location['city'] = csz_match.group(1).strip()
                            location['zip'] = csz_match.group(2)
        
        # Get phone
        phone_elem = await page.query_selector('[itemprop="telephone"], [href^="tel:"], .phone')
        if phone_elem:
            phone = await phone_elem.text_content()
            if phone:
                location['phone'] = clean_phone(phone)
        
        if location.get('city') or location.get('phone'):
            return location
            
    except Exception as e:
        print(f"    Error extracting single location: {e}")
    
    return None

def parse_jsonld_location(data, state_name):
    """Parse JSON-LD structured data"""
    location = {
        'business_name': "McAlister's Deli",
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
        address = data.get('address', {})
        if isinstance(address, dict):
            location['address'] = address.get('streetAddress', '')
            location['city'] = address.get('addressLocality', '')
            location['zip'] = address.get('postalCode', '')
        
        location['phone'] = data.get('telephone', '')
        
        if data.get('name') and data['name'] != "McAlister's Deli":
            location['business_name'] = f"McAlister's Deli - {data['name']}"
        
        if location.get('city'):
            return location
    except:
        pass
    
    return None

def clean_phone(phone_text):
    """Clean phone number to standard format"""
    if not phone_text:
        return None
    digits = re.sub(r'\D', '', str(phone_text))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    return phone_text.strip()

def insert_location(conn, location):
    """Insert a location into the leads table"""
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

if __name__ == "__main__":
    asyncio.run(scrape_mcalisters())
