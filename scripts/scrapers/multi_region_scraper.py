#!/usr/bin/env python3
"""
Multi-Region Lead Scraper - Performance Supply Depot
USA: 50 states + DC
Canada: 10 provinces + 3 territories  
Mexico: 32 states
"""

import sqlite3
import csv
import json
import time
import requests
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
CACHE_FILE = "/root/.openclaw/workspace/DepotChaos/yelp_cache.json"
LOG_FILE = "/var/log/aos/multi_region_scraper.log"

YELP_API_KEY = '5DUaC-eBObfSXkjf4YfLNlViO-WqwwCk0UJYewfhav25gbTrCaPvPR_nhokKyfBNKnduMHkqd5Z_v_0RwHSj2fXs8ziaJ-O_RAkuRvc6L6Lt9dwEboKoYHBpBuL1aXYx'

# USA 50 States + DC
USA_STATES = [
    ("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"),
    ("CA", "California"), ("CO", "Colorado"), ("CT", "Connecticut"), ("DE", "Delaware"),
    ("FL", "Florida"), ("GA", "Georgia"), ("HI", "Hawaii"), ("ID", "Idaho"),
    ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"),
    ("KY", "Kentucky"), ("LA", "Louisiana"), ("ME", "Maine"), ("MD", "Maryland"),
    ("MA", "Massachusetts"), ("MI", "Michigan"), ("MN", "Minnesota"), ("MS", "Mississippi"),
    ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"), ("NV", "Nevada"),
    ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"), ("NY", "New York"),
    ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"),
    ("OR", "Oregon"), ("PA", "Pennsylvania"), ("RI", "Rhode Island"), ("SC", "South Carolina"),
    ("SD", "South Dakota"), ("TN", "Tennessee"), ("TX", "Texas"), ("UT", "Utah"),
    ("VT", "Vermont"), ("VA", "Virginia"), ("WA", "Washington"), ("WV", "West Virginia"),
    ("WI", "Wisconsin"), ("WY", "Wyoming"), ("DC", "District of Columbia")
]

# Canada Provinces + Territories
CANADA_REGIONS = [
    ("AB", "Alberta"), ("BC", "British Columbia"), ("MB", "Manitoba"), ("NB", "New Brunswick"),
    ("NL", "Newfoundland and Labrador"), ("NS", "Nova Scotia"), ("ON", "Ontario"),
    ("PE", "Prince Edward Island"), ("QC", "Quebec"), ("SK", "Saskatchewan"),
    ("NT", "Northwest Territories"), ("NU", "Nunavut"), ("YT", "Yukon")
]

# Mexico States
MEXICO_STATES = [
    ("AGU", "Aguascalientes"), ("BCN", "Baja California"), ("BCS", "Baja California Sur"),
    ("CAM", "Campeche"), ("CHP", "Chiapas"), ("CHH", "Chihuahua"), ("CMX", "Ciudad de Mexico"),
    ("COA", "Coahuila"), ("COL", "Colima"), ("DUR", "Durango"), ("GUA", "Guanajuato"),
    ("GRO", "Guerrero"), ("HID", "Hidalgo"), ("JAL", "Jalisco"), ("MEX", "Mexico"),
    ("MIC", "Michoacan"), ("MOR", "Morelos"), ("NAY", "Nayarit"), ("NLE", "Nuevo Leon"),
    ("OAX", "Oaxaca"), ("PUE", "Puebla"), ("QUE", "Queretaro"), ("ROO", "Quintana Roo"),
    ("SLP", "San Luis Potosi"), ("SIN", "Sinaloa"), ("SON", "Sonora"), ("TAB", "Tabasco"),
    ("TAM", "Tamaulipas"), ("TLA", "Tlaxcala"), ("VER", "Veracruz"), ("YUC", "Yucatan"),
    ("ZAC", "Zacatecas")
]

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{ts}] {msg}"
    print(entry)
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(entry + '\n')

def load_cache():
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def search_yelp_businesses(location, term="restaurants", limit=50):
    """Search Yelp for businesses in a location"""
    cache = load_cache()
    cache_key = f"{term}_{location}"
    
    if cache_key in cache:
        return cache[cache_key]
    
    headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
    params = {
        'term': term,
        'location': location,
        'limit': limit,
        'categories': 'restaurants,bars'
    }
    
    try:
        r = requests.get('https://api.yelp.com/v3/businesses/search', 
                        headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            data = r.json()
            businesses = data.get('businesses', [])
            cache[cache_key] = businesses
            save_cache(cache)
            return businesses
    except Exception as e:
        log(f"   Yelp API error: {e}")
    return []

def get_major_cities(state_code, state_name, country="USA"):
    """Return major cities for a state/province"""
    # Map of major cities by state
    city_map = {
        "CA": ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "San Jose", "Oakland"],
        "TX": ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth", "El Paso"],
        "NY": ["New York City", "Buffalo", "Rochester", "Albany", "Syracuse"],
        "FL": ["Miami", "Orlando", "Tampa", "Jacksonville", "Fort Lauderdale"],
        "IL": ["Chicago", "Springfield", "Peoria", "Rockford"],
        "PA": ["Philadelphia", "Pittsburgh", "Allentown", "Erie"],
        "OH": ["Columbus", "Cleveland", "Cincinnati", "Toledo"],
        "GA": ["Atlanta", "Savannah", "Augusta", "Macon"],
        "NC": ["Charlotte", "Raleigh", "Greensboro", "Durham"],
        "MI": ["Detroit", "Grand Rapids", "Ann Arbor", "Lansing"],
        "ON": ["Toronto", "Ottawa", "Mississauga", "Hamilton"],
        "BC": ["Vancouver", "Victoria", "Surrey", "Burnaby"],
        "AB": ["Calgary", "Edmonton", "Red Deer", "Lethbridge"],
        "QC": ["Montreal", "Quebec City", "Laval", "Gatineau"],
        "CMX": ["Mexico City"], "JAL": ["Guadalajara"], "NLE": ["Monterrey"],
        "BCN": ["Tijuana", "Mexicali"], "SON": ["Hermosillo", "Ciudad Obregon"]
    }
    return city_map.get(state_code, [state_name])

def scrape_region(code, name, country, sample_size=20):
    """Scrape a single region"""
    log(f"🔍 Scraping {name} ({code}) - {country}")
    
    leads = []
    cities = get_major_cities(code, name, country)
    
    for city in cities[:3]:  # Limit to top 3 cities
        location = f"{city}, {name}" if country == "USA" else f"{city}, {name}"
        businesses = search_yelp_businesses(location, limit=min(sample_size, 50))
        
        for biz in businesses:
            lead = {
                'name': biz.get('name'),
                'phone': biz.get('phone'),
                'address': ' '.join(biz.get('location', {}).get('display_address', [])),
                'city': biz.get('location', {}).get('city'),
                'state': code,
                'zip': biz.get('location', {}).get('zip_code'),
                'country': country,
                'rating': biz.get('rating'),
                'review_count': biz.get('review_count'),
                'yelp_url': biz.get('url')
            }
            leads.append(lead)
        
        time.sleep(0.5)  # Rate limit
    
    log(f"   Found {len(leads)} leads in {name}")
    return leads

def import_leads(leads):
    """Import leads to DepotChaos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    imported = 0
    for lead in leads:
        if not lead.get('name'):
            continue
            
        # Check for duplicates
        cursor.execute('''
            SELECT id FROM vendors WHERE name = ? AND city = ? AND state = ?
        ''', (lead.get('name'), lead.get('city'), lead.get('state')))
        
        if cursor.fetchone():
            continue
        
        cursor.execute('''
            INSERT INTO vendors 
            (name, phone, address, city, state, zip, vendor_type, status, source_file, imported_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), ?)
        ''', (
            lead.get('name'), lead.get('phone'), lead.get('address'),
            lead.get('city'), lead.get('state'), lead.get('zip'),
            'restaurant', 'active', f"yelp_{lead.get('country', 'unknown')}",
            json.dumps({'rating': lead.get('rating'), 'reviews': lead.get('review_count'), 'yelp': lead.get('yelp_url')})
        ))
        imported += 1
    
    conn.commit()
    conn.close()
    return imported

def main():
    log("=" * 60)
    log("🌍 MULTI-REGION LEAD SCRAPER")
    log("=" * 60)
    
    total_leads = 0
    total_imported = 0
    
    # Scrape top 10 USA states by market size
    log("\n🇺🇸 USA - Top 10 States")
    priority_states = ["CA", "TX", "NY", "FL", "IL", "PA", "OH", "GA", "NC", "MI"]
    for code, name in USA_STATES:
        if code in priority_states:
            leads = scrape_region(code, name, "USA", sample_size=15)
            imported = import_leads(leads)
            total_leads += len(leads)
            total_imported += imported
            time.sleep(1)
    
    # Scrape Canada priority provinces
    log("\n🇨🇦 CANADA - Priority Provinces")
    priority_canada = ["ON", "BC", "AB", "QC"]
    for code, name in CANADA_REGIONS:
        if code in priority_canada:
            leads = scrape_region(code, name, "CANADA", sample_size=10)
            imported = import_leads(leads)
            total_leads += len(leads)
            total_imported += imported
            time.sleep(1)
    
    # Scrape Mexico priority states
    log("\n🇲🇽 MEXICO - Priority States")
    priority_mexico = ["CMX", "JAL", "NLE", "BCN", "SON"]
    for code, name in MEXICO_STATES:
        if code in priority_mexico:
            leads = scrape_region(code, name, "MEXICO", sample_size=10)
            imported = import_leads(leads)
            total_leads += len(leads)
            total_imported += imported
            time.sleep(1)
    
    log("\n" + "=" * 60)
    log(f"📊 SCRAPE COMPLETE")
    log(f"   Total leads found: {total_leads}")
    log(f"   New leads imported: {total_imported}")
    log(f"   Duplicates skipped: {total_leads - total_imported}")
    log("=" * 60)

if __name__ == "__main__":
    main()
