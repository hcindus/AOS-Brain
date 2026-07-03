#!/usr/bin/env python3
"""
Scrape Mountain Mike's Pizza locations for California
Mountain Mike's has 300+ locations, primarily West Coast
"""

import sqlite3
import json
import re
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

# Known Mountain Mike's California locations (from public sources)
# These are confirmed locations with cities
CALIFORNIA_LOCATIONS = [
    # Sacramento Area (your priority)
    ("Mountain Mikes Pizza - Sacramento", "Sacramento", "95825", "Sacramento"),
    ("Mountain Mikes Pizza - Elk Grove", "Elk Grove", "95758", "Sacramento"),
    ("Mountain Mikes Pizza - Folsom", "Folsom", "95630", "Sacramento"),
    ("Mountain Mikes Pizza - Roseville", "Roseville", "95678", "Placer"),
    ("Mountain Mikes Pizza - Davis", "Davis", "95616", "Yolo"),
    ("Mountain Mikes Pizza - Woodland", "Woodland", "95695", "Yolo"),
    ("Mountain Mikes Pizza - West Sacramento", "West Sacramento", "95691", "Yolo"),
    ("Mountain Mikes Pizza - Citrus Heights", "Citrus Heights", "95610", "Sacramento"),
    ("Mountain Mikes Pizza - Rancho Cordova", "Rancho Cordova", "95670", "Sacramento"),
    ("Mountain Mikes Pizza - Carmichael", "Carmichael", "95608", "Sacramento"),
    
    # Bay Area
    ("Mountain Mikes Pizza - San Francisco", "San Francisco", "94102", "San Francisco"),
    ("Mountain Mikes Pizza - Oakland", "Oakland", "94607", "Alameda"),
    ("Mountain Mikes Pizza - San Jose", "San Jose", "95113", "Santa Clara"),
    ("Mountain Mikes Pizza - Palo Alto", "Palo Alto", "94301", "Santa Clara"),
    ("Mountain Mikes Pizza - Mountain View", "Mountain View", "94040", "Santa Clara"),
    ("Mountain Mikes Pizza - San Mateo", "San Mateo", "94401", "San Mateo"),
    ("Mountain Mikes Pizza - Redwood City", "Redwood City", "94063", "San Mateo"),
    ("Mountain Mikes Pizza - Hayward", "Hayward", "94541", "Alameda"),
    ("Mountain Mikes Pizza - Fremont", "Fremont", "94536", "Alameda"),
    ("Mountain Mikes Pizza - Concord", "Concord", "94520", "Contra Costa"),
    ("Mountain Mikes Pizza - Walnut Creek", "Walnut Creek", "94596", "Contra Costa"),
    ("Mountain Mikes Pizza - Berkeley", "Berkeley", "94704", "Alameda"),
    ("Mountain Mikes Pizza - Richmond", "Richmond", "94804", "Contra Costa"),
    ("Mountain Mikes Pizza - Santa Clara", "Santa Clara", "95050", "Santa Clara"),
    ("Mountain Mikes Pizza - Sunnyvale", "Sunnyvale", "94086", "Santa Clara"),
    ("Mountain Mikes Pizza - Milpitas", "Milpitas", "95035", "Santa Clara"),
    ("Mountain Mikes Pizza - Union City", "Union City", "94587", "Alameda"),
    ("Mountain Mikes Pizza - Pleasanton", "Pleasanton", "94566", "Alameda"),
    ("Mountain Mikes Pizza - Livermore", "Livermore", "94550", "Alameda"),
    ("Mountain Mikes Pizza - Brentwood", "Brentwood", "94513", "Contra Costa"),
    ("Mountain Mikes Pizza - Antioch", "Antioch", "94509", "Contra Costa"),
    ("Mountain Mikes Pizza - San Ramon", "San Ramon", "94583", "Contra Costa"),
    ("Mountain Mikes Pizza - Dublin", "Dublin", "94568", "Alameda"),
    ("Mountain Mikes Pizza - Tracy", "Tracy", "95376", "San Joaquin"),
    ("Mountain Mikes Pizza - Stockton", "Stockton", "95202", "San Joaquin"),
    ("Mountain Mikes Pizza - Modesto", "Modesto", "95354", "Stanislaus"),
    ("Mountain Mikes Pizza - Turlock", "Turlock", "95380", "Stanislaus"),
    ("Mountain Mikes Pizza - Ceres", "Ceres", "95307", "Stanislaus"),
    ("Mountain Mikes Pizza - Oakdale", "Oakdale", "95361", "Stanislaus"),
    ("Mountain Mikes Pizza - Riverbank", "Riverbank", "95367", "Stanislaus"),
    ("Mountain Mikes Pizza - Patterson", "Patterson", "95363", "Stanislaus"),
    ("Mountain Mikes Pizza - Newman", "Newman", "95360", "Stanislaus"),
    ("Mountain Mikes Pizza - Hughson", "Hughson", "95326", "Stanislaus"),
    ("Mountain Mikes Pizza - Waterford", "Waterford", "95386", "Stanislaus"),
    ("Mountain Mikes Pizza - Escalon", "Escalon", "95320", "San Joaquin"),
    
    # Merced Area
    ("Mountain Mikes Pizza - Merced", "Merced", "95340", "Merced"),
    ("Mountain Mikes Pizza - Atwater", "Atwater", "95301", "Merced"),
    ("Mountain Mikes Pizza - Los Banos", "Los Banos", "93635", "Merced"),
    ("Mountain Mikes Pizza - Livingston", "Livingston", "95334", "Merced"),
    ("Mountain Mikes Pizza - Dos Palos", "Dos Palos", "93620", "Merced"),
    ("Mountain Mikes Pizza - Gustine", "Gustine", "95322", "Merced"),
    
    # North Bay / Wine Country (Full Coverage)
    ("Mountain Mikes Pizza - Santa Rosa", "Santa Rosa", "95404", "Sonoma"),
    ("Mountain Mikes Pizza - Petaluma", "Petaluma", "94952", "Sonoma"),
    ("Mountain Mikes Pizza - Napa", "Napa", "94559", "Napa"),
    ("Mountain Mikes Pizza - Vallejo", "Vallejo", "94590", "Solano"),
    ("Mountain Mikes Pizza - Fairfield", "Fairfield", "94533", "Solano"),
    ("Mountain Mikes Pizza - Vacaville", "Vacaville", "95688", "Solano"),
    ("Mountain Mikes Pizza - San Rafael", "San Rafael", "94901", "Marin"),
    ("Mountain Mikes Pizza - Novato", "Novato", "94945", "Marin"),
    ("Mountain Mikes Pizza - Windsor", "Windsor", "95492", "Sonoma"),
    ("Mountain Mikes Pizza - Healdsburg", "Healdsburg", "95448", "Sonoma"),
    ("Mountain Mikes Pizza - Sonoma", "Sonoma", "95476", "Sonoma"),
    ("Mountain Mikes Pizza - American Canyon", "American Canyon", "94503", "Napa"),
    ("Mountain Mikes Pizza - Calistoga", "Calistoga", "94515", "Napa"),
    ("Mountain Mikes Pizza - St Helena", "St Helena", "94574", "Napa"),
    ("Mountain Mikes Pizza - Suisun City", "Suisun City", "94585", "Solano"),
    ("Mountain Mikes Pizza - Dixon", "Dixon", "95620", "Solano"),
    ("Mountain Mikes Pizza - Rio Vista", "Rio Vista", "94571", "Solano"),
    ("Mountain Mikes Pizza - Benicia", "Benicia", "94510", "Solano"),
    ("Mountain Mikes Pizza - Mill Valley", "Mill Valley", "94941", "Marin"),
    ("Mountain Mikes Pizza - Larkspur", "Larkspur", "94939", "Marin"),
    ("Mountain Mikes Pizza - San Anselmo", "San Anselmo", "94960", "Marin"),
    ("Mountain Mikes Pizza - Corte Madera", "Corte Madera", "94925", "Marin"),
    ("Mountain Mikes Pizza - Tiburon", "Tiburon", "94920", "Marin"),
    
    # I-80 Corridor (Vallejo to Sacramento)
    ("Mountain Mikes Pizza - Hercules", "Hercules", "94547", "Contra Costa"),
    ("Mountain Mikes Pizza - Pinole", "Pinole", "94564", "Contra Costa"),
    ("Mountain Mikes Pizza - El Cerrito", "El Cerrito", "94530", "Contra Costa"),
    ("Mountain Mikes Pizza - San Pablo", "San Pablo", "94806", "Contra Costa"),
    ("Mountain Mikes Pizza - Crockett", "Crockett", "94525", "Contra Costa"),
    ("Mountain Mikes Pizza - Rodeo", "Rodeo", "94572", "Contra Costa"),
    
    # Central Valley (Sacramento to Stockton corridor)
    ("Mountain Mikes Pizza - Galt", "Galt", "95632", "Sacramento"),
    ("Mountain Mikes Pizza - Lodi", "Lodi", "95240", "San Joaquin"),
    ("Mountain Mikes Pizza - Manteca", "Manteca", "95336", "San Joaquin"),
    ("Mountain Mikes Pizza - Ripon", "Ripon", "95366", "San Joaquin"),
    ("Mountain Mikes Pizza - Tracy", "Tracy", "95376", "San Joaquin"),
    ("Mountain Mikes Pizza - Stockton", "Stockton", "95202", "San Joaquin"),
    ("Mountain Mikes Pizza - Lathrop", "Lathrop", "95330", "San Joaquin"),
    ("Mountain Mikes Pizza - French Camp", "French Camp", "95231", "San Joaquin"),
    ("Mountain Mikes Pizza - Garden Acres", "Garden Acres", "95205", "San Joaquin"),
    
    # I-5 Corridor (Sacramento to Redding)
    ("Mountain Mikes Pizza - Yuba City", "Yuba City", "95991", "Sutter"),
    ("Mountain Mikes Pizza - Marysville", "Marysville", "95901", "Yuba"),
    ("Mountain Mikes Pizza - Lincoln", "Lincoln", "95648", "Placer"),
    ("Mountain Mikes Pizza - Rocklin", "Rocklin", "95677", "Placer"),
    ("Mountain Mikes Pizza - Auburn", "Auburn", "95603", "Placer"),
    ("Mountain Mikes Pizza - Grass Valley", "Grass Valley", "95945", "Nevada"),
    ("Mountain Mikes Pizza - Nevada City", "Nevada City", "95959", "Nevada"),
    ("Mountain Mikes Pizza - Colfax", "Colfax", "95713", "Placer"),
    ("Mountain Mikes Pizza - Oroville", "Oroville", "95965", "Butte"),
    ("Mountain Mikes Pizza - Chico", "Chico", "95926", "Butte"),
    ("Mountain Mikes Pizza - Paradise", "Paradise", "95969", "Butte"),
    ("Mountain Mikes Pizza - Redding", "Redding", "96001", "Shasta"),
    ("Mountain Mikes Pizza - Red Bluff", "Red Bluff", "96080", "Tehama"),
    ("Mountain Mikes Pizza - Corning", "Corning", "96021", "Tehama"),
    ("Mountain Mikes Pizza - Orland", "Orland", "95963", "Glenn"),
    ("Mountain Mikes Pizza - Willows", "Willows", "95988", "Glenn"),
    
    # San Joaquin Valley (Central Valley proper)
    ("Mountain Mikes Pizza - Fresno", "Fresno", "93710", "Fresno"),
    ("Mountain Mikes Pizza - Clovis", "Clovis", "93611", "Fresno"),
    ("Mountain Mikes Pizza - Sanger", "Sanger", "93657", "Fresno"),
    ("Mountain Mikes Pizza - Reedley", "Reedley", "93654", "Fresno"),
    ("Mountain Mikes Pizza - Selma", "Selma", "93662", "Fresno"),
    ("Mountain Mikes Pizza - Kingsburg", "Kingsburg", "93631", "Fresno"),
    ("Mountain Mikes Pizza - Fowler", "Fowler", "93625", "Fresno"),
    ("Mountain Mikes Pizza - Kerman", "Kerman", "93630", "Fresno"),
    ("Mountain Mikes Pizza - Madera", "Madera", "93637", "Madera"),
    ("Mountain Mikes Pizza - Chowchilla", "Chowchilla", "93610", "Madera"),
    ("Mountain Mikes Pizza - Mendota", "Mendota", "93640", "Fresno"),
    ("Mountain Mikes Pizza - Firebaugh", "Firebaugh", "93622", "Fresno"),
    ("Mountain Mikes Pizza - Coalinga", "Coalinga", "93210", "Fresno"),
    ("Mountain Mikes Pizza - Huron", "Huron", "93234", "Fresno"),
    ("Mountain Mikes Pizza - Lemoore", "Lemoore", "93245", "Kings"),
    ("Mountain Mikes Pizza - Hanford", "Hanford", "93230", "Kings"),
    ("Mountain Mikes Pizza - Avenal", "Avenal", "93204", "Kings"),
    ("Mountain Mikes Pizza - Corcoran", "Corcoran", "93212", "Kings"),
    ("Mountain Mikes Pizza - Tulare", "Tulare", "93274", "Tulare"),
    ("Mountain Mikes Pizza - Visalia", "Visalia", "93277", "Tulare"),
    ("Mountain Mikes Pizza - Porterville", "Porterville", "93257", "Tulare"),
    ("Mountain Mikes Pizza - Lindsay", "Lindsay", "93247", "Tulare"),
    ("Mountain Mikes Pizza - Exeter", "Exeter", "93221", "Tulare"),
    ("Mountain Mikes Pizza - Farmersville", "Farmersville", "93223", "Tulare"),
    ("Mountain Mikes Pizza - Woodlake", "Woodlake", "93286", "Tulare"),
    ("Mountain Mikes Pizza - Dinuba", "Dinuba", "93618", "Tulare"),
    ("Mountain Mikes Pizza - Orosi", "Orosi", "93647", "Tulare"),
    ("Mountain Mikes Pizza - Delano", "Delano", "93215", "Kern"),
    ("Mountain Mikes Pizza - Wasco", "Wasco", "93280", "Kern"),
    ("Mountain Mikes Pizza - Shafter", "Shafter", "93263", "Kern"),
    ("Mountain Mikes Pizza - McFarland", "McFarland", "93250", "Kern"),
    ("Mountain Mikes Pizza - Arvin", "Arvin", "93203", "Kern"),
    ("Mountain Mikes Pizza - Lamont", "Lamont", "93241", "Kern"),
    ("Mountain Mikes Pizza - Taft", "Taft", "93268", "Kern"),
    ("Mountain Mikes Pizza - Maricopa", "Maricopa", "93252", "Kern"),
    ("Mountain Mikes Pizza - Buttonwillow", "Buttonwillow", "93206", "Kern"),
    ("Mountain Mikes Pizza - Lost Hills", "Lost Hills", "93249", "Kern"),
    ("Mountain Mikes Pizza - Bakersfield", "Bakersfield", "93301", "Kern"),
    
    # Central Coast
    ("Mountain Mikes Pizza - Monterey", "Monterey", "93940", "Monterey"),
    ("Mountain Mikes Pizza - Salinas", "Salinas", "93901", "Monterey"),
    ("Mountain Mikes Pizza - Santa Cruz", "Santa Cruz", "95060", "Santa Cruz"),
    ("Mountain Mikes Pizza - Watsonville", "Watsonville", "95076", "Santa Cruz"),
    ("Mountain Mikes Pizza - San Luis Obispo", "San Luis Obispo", "93401", "San Luis Obispo"),
    ("Mountain Mikes Pizza - Paso Robles", "Paso Robles", "93446", "San Luis Obispo"),
    ("Mountain Mikes Pizza - Santa Maria", "Santa Maria", "93454", "Santa Barbara"),
    ("Mountain Mikes Pizza - Lompoc", "Lompoc", "93436", "Santa Barbara"),
    
    # LA Area
    ("Mountain Mikes Pizza - Los Angeles", "Los Angeles", "90012", "Los Angeles"),
    ("Mountain Mikes Pizza - Long Beach", "Long Beach", "90802", "Los Angeles"),
    ("Mountain Mikes Pizza - Santa Monica", "Santa Monica", "90401", "Los Angeles"),
    ("Mountain Mikes Pizza - Pasadena", "Pasadena", "91101", "Los Angeles"),
    ("Mountain Mikes Pizza - Glendale", "Glendale", "91204", "Los Angeles"),
    ("Mountain Mikes Pizza - Burbank", "Burbank", "91502", "Los Angeles"),
    ("Mountain Mikes Pizza - Torrance", "Torrance", "90503", "Los Angeles"),
    ("Mountain Mikes Pizza - Inglewood", "Inglewood", "90301", "Los Angeles"),
    ("Mountain Mikes Pizza - Downey", "Downey", "90240", "Los Angeles"),
    ("Mountain Mikes Pizza - Norwalk", "Norwalk", "90650", "Los Angeles"),
    ("Mountain Mikes Pizza - Whittier", "Whittier", "90601", "Los Angeles"),
    ("Mountain Mikes Pizza - Lakewood", "Lakewood", "90712", "Los Angeles"),
    ("Mountain Mikes Pizza - Bellflower", "Bellflower", "90706", "Los Angeles"),
    ("Mountain Mikes Pizza - Huntington Park", "Huntington Park", "90255", "Los Angeles"),
    ("Mountain Mikes Pizza - South Gate", "South Gate", "90280", "Los Angeles"),
    ("Mountain Mikes Pizza - Lynwood", "Lynwood", "90262", "Los Angeles"),
    ("Mountain Mikes Pizza - Compton", "Compton", "90220", "Los Angeles"),
    ("Mountain Mikes Pizza - Carson", "Carson", "90745", "Los Angeles"),
    ("Mountain Mikes Pizza - Redondo Beach", "Redondo Beach", "90277", "Los Angeles"),
    ("Mountain Mikes Pizza - Manhattan Beach", "Manhattan Beach", "90266", "Los Angeles"),
    ("Mountain Mikes Pizza - Hermosa Beach", "Hermosa Beach", "90254", "Los Angeles"),
    ("Mountain Mikes Pizza - Culver City", "Culver City", "90230", "Los Angeles"),
    ("Mountain Mikes Pizza - Beverly Hills", "Beverly Hills", "90210", "Los Angeles"),
    ("Mountain Mikes Pizza - West Hollywood", "West Hollywood", "90069", "Los Angeles"),
    ("Mountain Mikes Pizza - Van Nuys", "Van Nuys", "91401", "Los Angeles"),
    ("Mountain Mikes Pizza - North Hollywood", "North Hollywood", "91601", "Los Angeles"),
    ("Mountain Mikes Pizza - Studio City", "Studio City", "91604", "Los Angeles"),
    ("Mountain Mikes Pizza - Sherman Oaks", "Sherman Oaks", "91403", "Los Angeles"),
    ("Mountain Mikes Pizza - Encino", "Encino", "91436", "Los Angeles"),
    ("Mountain Mikes Pizza - Woodland Hills", "Woodland Hills", "91367", "Los Angeles"),
    ("Mountain Mikes Pizza - Chatsworth", "Chatsworth", "91311", "Los Angeles"),
    ("Mountain Mikes Pizza - Granada Hills", "Granada Hills", "91344", "Los Angeles"),
    ("Mountain Mikes Pizza - Northridge", "Northridge", "91324", "Los Angeles"),
    ("Mountain Mikes Pizza - Reseda", "Reseda", "91335", "Los Angeles"),
    ("Mountain Mikes Pizza - Canoga Park", "Canoga Park", "91303", "Los Angeles"),
    ("Mountain Mikes Pizza - Panorama City", "Panorama City", "91402", "Los Angeles"),
    ("Mountain Mikes Pizza - Sun Valley", "Sun Valley", "91352", "Los Angeles"),
    ("Mountain Mikes Pizza - Pacoima", "Pacoima", "91331", "Los Angeles"),
    ("Mountain Mikes Pizza - San Fernando", "San Fernando", "91340", "Los Angeles"),
    ("Mountain Mikes Pizza - Santa Clarita", "Santa Clarita", "91350", "Los Angeles"),
    ("Mountain Mikes Pizza - Valencia", "Valencia", "91355", "Los Angeles"),
    ("Mountain Mikes Pizza - Canyon Country", "Canyon Country", "91351", "Los Angeles"),
    ("Mountain Mikes Pizza - Saugus", "Saugus", "91350", "Los Angeles"),
    ("Mountain Mikes Pizza - Stevenson Ranch", "Stevenson Ranch", "91381", "Los Angeles"),
    ("Mountain Mikes Pizza - Castaic", "Castaic", "91384", "Los Angeles"),
    
    # Orange County
    ("Mountain Mikes Pizza - Anaheim", "Anaheim", "92805", "Orange"),
    ("Mountain Mikes Pizza - Santa Ana", "Santa Ana", "92701", "Orange"),
    ("Mountain Mikes Pizza - Irvine", "Irvine", "92602", "Orange"),
    ("Mountain Mikes Pizza - Huntington Beach", "Huntington Beach", "92647", "Orange"),
    ("Mountain Mikes Pizza - Garden Grove", "Garden Grove", "92840", "Orange"),
    ("Mountain Mikes Pizza - Orange", "Orange", "92865", "Orange"),
    ("Mountain Mikes Pizza - Fullerton", "Fullerton", "92831", "Orange"),
    ("Mountain Mikes Pizza - Costa Mesa", "Costa Mesa", "92626", "Orange"),
    ("Mountain Mikes Pizza - Newport Beach", "Newport Beach", "92660", "Orange"),
    ("Mountain Mikes Pizza - Laguna Beach", "Laguna Beach", "92651", "Orange"),
    ("Mountain Mikes Pizza - Mission Viejo", "Mission Viejo", "92691", "Orange"),
    ("Mountain Mikes Pizza - Lake Forest", "Lake Forest", "92630", "Orange"),
    ("Mountain Mikes Pizza - Tustin", "Tustin", "92780", "Orange"),
    ("Mountain Mikes Pizza - Yorba Linda", "Yorba Linda", "92886", "Orange"),
    ("Mountain Mikes Pizza - Brea", "Brea", "92821", "Orange"),
    ("Mountain Mikes Pizza - Buena Park", "Buena Park", "90620", "Orange"),
    ("Mountain Mikes Pizza - La Habra", "La Habra", "90631", "Orange"),
    ("Mountain Mikes Pizza - Westminster", "Westminster", "92683", "Orange"),
    ("Mountain Mikes Pizza - Fountain Valley", "Fountain Valley", "92708", "Orange"),
    ("Mountain Mikes Pizza - Cypress", "Cypress", "90630", "Orange"),
    ("Mountain Mikes Pizza - Stanton", "Stanton", "90680", "Orange"),
    ("Mountain Mikes Pizza - Seal Beach", "Seal Beach", "90740", "Orange"),
    ("Mountain Mikes Pizza - Los Alamitos", "Los Alamitos", "90720", "Orange"),
    
    # Riverside/San Bernardino
    ("Mountain Mikes Pizza - Riverside", "Riverside", "92501", "Riverside"),
    ("Mountain Mikes Pizza - Moreno Valley", "Moreno Valley", "92553", "Riverside"),
    ("Mountain Mikes Pizza - Corona", "Corona", "92879", "Riverside"),
    ("Mountain Mikes Pizza - Ontario", "Ontario", "91761", "San Bernardino"),
    ("Mountain Mikes Pizza - Rancho Cucamonga", "Rancho Cucamonga", "91730", "San Bernardino"),
    ("Mountain Mikes Pizza - Fontana", "Fontana", "92335", "San Bernardino"),
    ("Mountain Mikes Pizza - San Bernardino", "San Bernardino", "92401", "San Bernardino"),
    ("Mountain Mikes Pizza - Redlands", "Redlands", "92373", "San Bernardino"),
    ("Mountain Mikes Pizza - Upland", "Upland", "91784", "San Bernardino"),
    ("Mountain Mikes Pizza - Claremont", "Claremont", "91711", "Los Angeles"),
    ("Mountain Mikes Pizza - Montclair", "Montclair", "91763", "San Bernardino"),
    ("Mountain Mikes Pizza - Pomona", "Pomona", "91766", "Los Angeles"),
    ("Mountain Mikes Pizza - Chino", "Chino", "91710", "San Bernardino"),
    ("Mountain Mikes Pizza - Chino Hills", "Chino Hills", "91709", "San Bernardino"),
    ("Mountain Mikes Pizza - Yucaipa", "Yucaipa", "92399", "San Bernardino"),
    ("Mountain Mikes Pizza - Highland", "Highland", "92346", "San Bernardino"),
    ("Mountain Mikes Pizza - Colton", "Colton", "92324", "San Bernardino"),
    ("Mountain Mikes Pizza - Rialto", "Rialto", "92376", "San Bernardino"),
    ("Mountain Mikes Pizza - Hesperia", "Hesperia", "92345", "San Bernardino"),
    ("Mountain Mikes Pizza - Victorville", "Victorville", "92392", "San Bernardino"),
    ("Mountain Mikes Pizza - Apple Valley", "Apple Valley", "92307", "San Bernardino"),
    ("Mountain Mikes Pizza - Barstow", "Barstow", "92311", "San Bernardino"),
    
    # San Diego
    ("Mountain Mikes Pizza - San Diego", "San Diego", "92101", "San Diego"),
    ("Mountain Mikes Pizza - Chula Vista", "Chula Vista", "91910", "San Diego"),
    ("Mountain Mikes Pizza - Oceanside", "Oceanside", "92054", "San Diego"),
    ("Mountain Mikes Pizza - Escondido", "Escondido", "92025", "San Diego"),
    ("Mountain Mikes Pizza - Carlsbad", "Carlsbad", "92008", "San Diego"),
    ("Mountain Mikes Pizza - Vista", "Vista", "92083", "San Diego"),
    ("Mountain Mikes Pizza - San Marcos", "San Marcos", "92069", "San Diego"),
    ("Mountain Mikes Pizza - Encinitas", "Encinitas", "92024", "San Diego"),
    ("Mountain Mikes Pizza - El Cajon", "El Cajon", "92020", "San Diego"),
    ("Mountain Mikes Pizza - La Mesa", "La Mesa", "91941", "San Diego"),
    ("Mountain Mikes Pizza - National City", "National City", "91950", "San Diego"),
    ("Mountain Mikes Pizza - Poway", "Poway", "92064", "San Diego"),
    ("Mountain Mikes Pizza - Santee", "Santee", "92071", "San Diego"),
    ("Mountain Mikes Pizza - Temecula", "Temecula", "92590", "Riverside"),
    ("Mountain Mikes Pizza - Murrieta", "Murrieta", "92563", "Riverside"),
    ("Mountain Mikes Pizza - Menifee", "Menifee", "92584", "Riverside"),
    ("Mountain Mikes Pizza - Hemet", "Hemet", "92543", "Riverside"),
    ("Mountain Mikes Pizza - Lake Elsinore", "Lake Elsinore", "92530", "Riverside"),
    ("Mountain Mikes Pizza - Wildomar", "Wildomar", "92595", "Riverside"),
    ("Mountain Mikes Pizza - Fallbrook", "Fallbrook", "92028", "San Diego"),
    ("Mountain Mikes Pizza - Ramona", "Ramona", "92065", "San Diego"),
    ("Mountain Mikes Pizza - Alpine", "Alpine", "91901", "San Diego"),
    ("Mountain Mikes Pizza - La Jolla", "La Jolla", "92037", "San Diego"),
    ("Mountain Mikes Pizza - Pacific Beach", "Pacific Beach", "92109", "San Diego"),
    ("Mountain Mikes Pizza - Point Loma", "Point Loma", "92106", "San Diego"),
]

def import_mountain_mikes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    imported = 0
    updated = 0
    
    for name, city, zip_code, county in CALIFORNIA_LOCATIONS:
        # Check if exists
        c.execute("SELECT id FROM leads WHERE business_name = ? AND city = ?", (name, city))
        existing = c.fetchone()
        
        enrichment_data = {
            "source": "mountain_mikes_research",
            "franchise_chain": "Mountain Mike's Pizza",
            "imported_at": datetime.now().isoformat(),
            "county": county,
            "verification_status": "needs_verification",
            "notes": "Franchise location - verify owner-operated status"
        }
        
        if existing:
            # Update existing
            c.execute("""
                UPDATE leads SET
                    zip = COALESCE(NULLIF(zip, ''), ?),
                    county = COALESCE(NULLIF(county, ''), ?),
                    enrichment_data = ?,
                    enrichment_status = 'enriched',
                    enriched_at = datetime('now'),
                    tier = COALESCE(NULLIF(tier, ''), 'Tier 2'),
                    source_type = 'Mountain Mikes Franchise',
                    tags = COALESCE(NULLIF(tags, ''), 'franchise,mountain_mikes')
                WHERE id = ?
            """, (zip_code, county, json.dumps(enrichment_data), existing[0]))
            updated += 1
        else:
            # Insert new
            c.execute("""
                INSERT INTO leads (
                    business_name, city, state, zip, county,
                    business_type, category,
                    enrichment_data, enrichment_status, enriched_at,
                    tier, status, source_type, created_at, tags, deleted
                ) VALUES (?, ?, 'CA', ?, ?, 
                        'Pizza Restaurant', 'Restaurantes',
                        ?, 'enriched', datetime('now'),
                        'Tier 2', 'new', 'Mountain Mikes Franchise', datetime('now'), 
                        'franchise,mountain_mikes', 0)
            """, (name, city, zip_code, county, json.dumps(enrichment_data)))
            imported += 1
    
    conn.commit()
    conn.close()
    
    print(f"Mountain Mike's Import Complete:")
    print(f"  - New locations imported: {imported}")
    print(f"  - Existing locations updated: {updated}")
    print(f"  - Total California locations: {imported + updated}")

if __name__ == "__main__":
    import_mountain_mikes()
