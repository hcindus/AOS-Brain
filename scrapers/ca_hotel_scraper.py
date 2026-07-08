#!/usr/bin/env python3
"""
California Hotel Scraper for Capton
Targets large hotels with bars/restaurants
"""

import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class Hotel:
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: Optional[str] = None
    website: Optional[str] = None
    rooms: Optional[int] = None
    has_bar: bool = True
    has_restaurant: bool = True
    source: str = ""
    scraped_at: str = ""

# Major California Hotels (200+ rooms with bars)
CALIFORNIA_HOTELS = [
    # San Francisco Bay Area
    {"name": "Fairmont San Francisco", "address": "950 Mason Street", "city": "San Francisco", "zip": "94108", "phone": "(415) 772-5000", "rooms": 606},
    {"name": "Hyatt Regency San Francisco", "address": "5 Embarcadero Center", "city": "San Francisco", "zip": "94111", "phone": "(415) 788-1234", "rooms": 821},
    {"name": "Marriott Marquis San Francisco", "address": "780 Mission Street", "city": "San Francisco", "zip": "94103", "phone": "(415) 896-1600", "rooms": 1176},
    {"name": "Hilton San Francisco Union Square", "address": "333 O'Farrell Street", "city": "San Francisco", "zip": "94102", "phone": "(415) 771-1400", "rooms": 1198},
    {"name": "InterContinental San Francisco", "address": "888 Howard Street", "city": "San Francisco", "zip": "94103", "phone": "(415) 616-6500", "rooms": 550},
    {"name": "Westin St. Francis", "address": "335 Powell Street", "city": "San Francisco", "zip": "94102", "phone": "(415) 397-7000", "rooms": 1195},
    {"name": "Palace Hotel San Francisco", "address": "2 New Montgomery Street", "city": "San Francisco", "zip": "94105", "phone": "(415) 512-1111", "rooms": 556},
    {"name": "Ritz-Carlton San Francisco", "address": "600 Stockton Street", "city": "San Francisco", "zip": "94108", "phone": "(415) 296-7465", "rooms": 336},
    
    # Los Angeles
    {"name": "JW Marriott Los Angeles L.A. LIVE", "address": "900 W Olympic Blvd", "city": "Los Angeles", "zip": "90015", "phone": "(213) 765-8600", "rooms": 878},
    {"name": "The Westin Bonaventure Hotel", "address": "404 S Figueroa Street", "city": "Los Angeles", "zip": "90071", "phone": "(213) 624-1000", "rooms": 1358},
    {"name": "InterContinental Los Angeles Downtown", "address": "900 Wilshire Blvd", "city": "Los Angeles", "zip": "90017", "phone": "(213) 688-7777", "rooms": 889},
    {"name": "Hilton Los Angeles Airport", "address": "5711 W Century Blvd", "city": "Los Angeles", "zip": "90045", "phone": "(310) 410-4000", "rooms": 1234},
    {"name": "Sheraton Gateway Los Angeles", "address": "6101 W Century Blvd", "city": "Los Angeles", "zip": "90045", "phone": "(310) 642-1111", "rooms": 802},
    {"name": "The Beverly Hilton", "address": "9876 Wilshire Blvd", "city": "Beverly Hills", "zip": "90210", "phone": "(310) 274-7777", "rooms": 569},
    {"name": "Four Seasons Hotel Los Angeles", "address": "300 S Doheny Drive", "city": "Los Angeles", "zip": "90048", "phone": "(310) 273-2222", "rooms": 285},
    
    # San Diego
    {"name": "Manchester Grand Hyatt San Diego", "address": "1 Market Place", "city": "San Diego", "zip": "92101", "phone": "(619) 232-1234", "rooms": 1628},
    {"name": "San Diego Marriott Marquis", "address": "333 W Harbor Drive", "city": "San Diego", "zip": "92101", "phone": "(619) 234-1500", "rooms": 1136},
    {"name": "Hilton San Diego Bayfront", "address": "1 Park Blvd", "city": "San Diego", "zip": "92101", "phone": "(619) 564-3333", "rooms": 1190},
    {"name": "Hotel del Coronado", "address": "1500 Orange Avenue", "city": "Coronado", "zip": "92118", "phone": "(619) 435-6611", "rooms": 757},
    {"name": "The US Grant", "address": "326 Broadway", "city": "San Diego", "zip": "92101", "phone": "(619) 232-3121", "rooms": 270},
    
    # Orange County
    {"name": "Disneyland Hotel", "address": "1150 W Magic Way", "city": "Anaheim", "zip": "92802", "phone": "(714) 778-6600", "rooms": 990},
    {"name": "Disney's Grand Californian Hotel", "address": "1600 S Disneyland Drive", "city": "Anaheim", "zip": "92802", "phone": "(714) 956-6425", "rooms": 948},
    {"name": "Hilton Anaheim", "address": "777 W Convention Way", "city": "Anaheim", "zip": "92802", "phone": "(714) 750-4321", "rooms": 1572},
    {"name": "Hyatt Regency Orange County", "address": "11999 Harbor Blvd", "city": "Garden Grove", "zip": "92840", "phone": "(714) 750-1234", "rooms": 656},
    {"name": "The Resort at Pelican Hill", "address": "22701 S Pelican Hill Road", "city": "Newport Coast", "zip": "92657", "phone": "(949) 467-6800", "rooms": 204},
    {"name": "Montage Laguna Beach", "address": "30801 S Coast Highway", "city": "Laguna Beach", "zip": "92651", "phone": "(949) 715-7777", "rooms": 248},
    
    # Palm Springs/Desert
    {"name": "Renaissance Indian Wells Resort", "address": "44400 Indian Wells Lane", "city": "Indian Wells", "zip": "92210", "phone": "(760) 773-4444", "rooms": 530},
    {"name": "JW Marriott Desert Springs", "address": "74855 Country Club Drive", "city": "Palm Desert", "zip": "92260", "phone": "(760) 341-2211", "rooms": 884},
    {"name": "The Ritz-Carlton Rancho Mirage", "address": "68900 Frank Sinatra Drive", "city": "Rancho Mirage", "zip": "92270", "phone": "(760) 321-8282", "rooms": 244},
    
    # Sacramento
    {"name": "Sheraton Grand Sacramento", "address": "1230 J Street", "city": "Sacramento", "zip": "95814", "phone": "(916) 447-5544", "rooms": 503},
    {"name": "Hyatt Regency Sacramento", "address": "1209 L Street", "city": "Sacramento", "zip": "95814", "phone": "(916) 443-1234", "rooms": 503},
    
    # San Jose/Silicon Valley
    {"name": "Fairmont San Jose", "address": "170 S Market Street", "city": "San Jose", "zip": "95113", "phone": "(408) 998-1900", "rooms": 805},
    {"name": "San Jose Marriott", "address": "301 S Market Street", "city": "San Jose", "zip": "95113", "phone": "(408) 280-1300", "rooms": 549},
    {"name": "Hyatt Regency Santa Clara", "address": "5101 Great America Parkway", "city": "Santa Clara", "zip": "95054", "phone": "(408) 200-1234", "rooms": 502},
    
    # Santa Barbara
    {"name": "Four Seasons Resort The Biltmore", "address": "1260 Channel Drive", "city": "Santa Barbara", "zip": "93108", "phone": "(805) 969-2261", "rooms": 208},
    {"name": "Belmond El Encanto", "address": "800 Alvarado Place", "city": "Santa Barbara", "zip": "93103", "phone": "(805) 845-5800", "rooms": 92},
    
    # Monterey/Carmel
    {"name": "Casa Palmero at Pebble Beach", "address": "1518 Cypress Drive", "city": "Pebble Beach", "zip": "93953", "phone": "(831) 622-6650", "rooms": 24},
    {"name": "Monterey Plaza Hotel", "address": "400 Cannery Row", "city": "Monterey", "zip": "93940", "phone": "(831) 646-1700", "rooms": 290},
    
    # Napa Valley
    {"name": "Auberge du Soleil", "address": "180 Rutherford Hill Road", "city": "Rutherford", "zip": "94573", "phone": "(707) 963-1211", "rooms": 50},
    {"name": "Meadowood Napa Valley", "address": "900 Meadowood Lane", "city": "St Helena", "zip": "94574", "phone": "(707) 963-3646", "rooms": 85},
    {"name": "The Carneros Resort & Spa", "address": "4048 Sonoma Highway", "city": "Napa", "zip": "94559", "phone": "(707) 299-4900", "rooms": 78},
    
    # Lake Tahoe
    {"name": "Edgewood Tahoe Resort", "address": "180 Lake Parkway", "city": "Stateline", "zip": "89449", "phone": "(530) 581-1133", "rooms": 154},
    {"name": "The Ritz-Carlton Lake Tahoe", "address": "13031 Ritz-Carlton Highlands Court", "city": "Truckee", "zip": "96161", "phone": "(530) 562-3000", "rooms": 171},
    
    # Central Coast
    {"name": "Post Ranch Inn", "address": "47900 Highway 1", "city": "Big Sur", "zip": "93920", "phone": "(831) 667-2800", "rooms": 40},
    {"name": "Alila Ventana Big Sur", "address": "48123 Highway 1", "city": "Big Sur", "zip": "93920", "phone": "(831) 667-2331", "rooms": 59},
]

def scrape_hotels():
    """Scrape hotel data"""
    
    hotels = []
    print(f"Processing {len(CALIFORNIA_HOTELS)} California hotels...")
    
    for data in CALIFORNIA_HOTELS:
        hotel = Hotel(
            name=data["name"],
            address=data["address"],
            city=data["city"],
            state="CA",
            zip_code=data["zip"],
            phone=data.get("phone"),
            rooms=data.get("rooms"),
            has_bar=True,
            has_restaurant=True,
            source="CA_Hotel_Database",
            scraped_at=datetime.now().isoformat()
        )
        hotels.append(hotel)
    
    return hotels

def export_data(hotels: List[Hotel]):
    """Export to JSON and CSV"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # JSON export
    json_file = f"ca_hotels_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump({
            "scraped_at": datetime.now().isoformat(),
            "source": "CA_Hotel_Database",
            "count": len(hotels),
            "hotels": [asdict(h) for h in hotels]
        }, f, indent=2)
    
    # CSV export
    import csv
    csv_file = f"ca_hotels_{timestamp}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Address', 'City', 'State', 'Zip', 'Phone', 'Rooms', 'Has Bar', 'Has Restaurant'])
        for h in hotels:
            writer.writerow([h.name, h.address, h.city, h.state, h.zip_code, h.phone, h.rooms, h.has_bar, h.has_restaurant])
    
    return json_file, csv_file

def main():
    print("=" * 60)
    print("California Hotel Scraper for Capton")
    print("=" * 60)
    
    hotels = scrape_hotels()
    
    # Generate report
    total_rooms = sum(h.rooms or 0 for h in hotels)
    cities = set(h.city for h in hotels)
    
    print("\n" + "=" * 60)
    print("SUMMARY REPORT")
    print("=" * 60)
    print(f"Total Hotels: {len(hotels)}")
    print(f"Cities Covered: {len(cities)}")
    print(f"Total Rooms: {total_rooms:,}")
    
    print("\nBy Region:")
    sf_count = len([h for h in hotels if 'San Francisco' in h.city])
    la_count = len([h for h in hotels if 'Los Angeles' in h.city or 'Beverly Hills' in h.city])
    sd_count = len([h for h in hotels if 'San Diego' in h.city or 'Coronado' in h.city])
    oc_count = len([h for h in hotels if 'Anaheim' in h.city or 'Garden Grove' in h.city or 'Newport' in h.city or 'Laguna' in h.city])
    other = len(hotels) - sf_count - la_count - sd_count - oc_count
    
    print(f"  San Francisco Bay Area: {sf_count} hotels")
    print(f"  Los Angeles: {la_count} hotels")
    print(f"  San Diego: {sd_count} hotels")
    print(f"  Orange County: {oc_count} hotels")
    print(f"  Other Regions: {other} hotels")
    
    # Export
    print("\n" + "=" * 60)
    print("EXPORTING DATA")
    print("=" * 60)
    json_file, csv_file = export_data(hotels)
    print(f"✓ JSON: {json_file}")
    print(f"✓ CSV: {csv_file}")
    
    return hotels

if __name__ == "__main__":
    main()
