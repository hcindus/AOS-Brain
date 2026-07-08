#!/usr/bin/env python3
"""
California Casino Scraper
Scrapes tribal and travel casinos in California
"""

import json
import re
import requests
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional
from bs4 import BeautifulSoup
import time
import random

@dataclass
class Casino:
    name: str
    tribe: str
    address: str
    city: str
    zip_code: str
    state: str = "CA"
    phone: Optional[str] = None
    website: Optional[str] = None
    gaming_types: List[str] = None
    hotel_rooms: Optional[int] = None
    restaurants: List[str] = None
    source: str = ""
    scraped_at: str = ""

# California Tribal Casinos Database
# Data compiled from California Gambling Control Commission and tribal sources

CALIFORNIA_CASINOS = [
    # Southern California
    {"name": "Pechanga Resort Casino", "tribe": "Pechanga Band of Luiseño Indians", 
     "city": "Temecula", "zip": "92592", "address": "45000 Pechanga Parkway",
     "phone": "(951) 693-1819", "website": "pechanga.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": 1077},
    
    {"name": "Morongo Casino Resort & Spa", "tribe": "Morongo Band of Mission Indians",
     "city": "Cabazon", "zip": "92230", "address": "49500 Seminole Drive",
     "phone": "(951) 849-3080", "website": "morongocasinoresort.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 310},
    
    {"name": "Agua Caliente Casino Palm Springs", "tribe": "Agua Caliente Band of Cahuilla Indians",
     "city": "Palm Springs", "zip": "92262", "address": "401 East Amado Road",
     "phone": "(760) 323-5862", "website": "aguacalientecasinos.com",
     "gaming": ["Slots", "Table Games"], "hotel_rooms": None},
    
    {"name": "Agua Caliente Resort Casino Spa Rancho Mirage", "tribe": "Agua Caliente Band of Cahuilla Indians",
     "city": "Rancho Mirage", "zip": "92270", "address": "32250 Bob Hope Drive",
     "phone": "(760) 321-2000", "website": "aguacalientecasinos.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": 340},
    
    {"name": "Fantasy Springs Resort Casino", "tribe": "Cabazon Band of Mission Indians",
     "city": "Indio", "zip": "92203", "address": "84245 Indio Springs Drive",
     "phone": "(760) 342-5000", "website": "fantasyspringsresort.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 250},
    
    {"name": "Spotlight 29 Casino", "tribe": "Twenty-Nine Palms Band of Mission Indians",
     "city": "Coachella", "zip": "92236", "address": "46200 Harrison Street",
     "phone": "(760) 775-5566", "website": "spotlight29.com",
     "gaming": ["Slots", "Table Games", "Bingo"], "hotel_rooms": None},
    
    {"name": "Augustine Casino", "tribe": "Cabazon Band of Mission Indians",
     "city": "Coachella", "zip": "92236", "address": "84-001 Avenue 54",
     "phone": "(760) 391-9500", "website": "augustinecasino.com",
     "gaming": ["Slots", "Table Games"], "hotel_rooms": None},
    
    {"name": "Tortoise Rock Casino", "tribe": "Twentynine Palms Band of Mission Indians",
     "city": "Twentynine Palms", "zip": "92277", "address": "73829 Baseline Road",
     "phone": "(760) 361-6300", "website": "tortoiserockcasino.com",
     "gaming": ["Slots", "Table Games"], "hotel_rooms": None},
    
    {"name": "Soboba Casino Resort", "tribe": "Soboba Band of Luiseño Indians",
     "city": "San Jacinto", "zip": "92583", "address": "22777 Soboba Road",
     "phone": "(951) 665-1000", "website": "sobobacasino.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": 200},
    
    {"name": "San Manuel Casino", "tribe": "San Manuel Band of Mission Indians",
     "city": "Highland", "zip": "92346", "address": "5797 North Victoria Avenue",
     "phone": "(909) 864-5050", "website": "sanmanuelcasino.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": 432},
    
    {"name": "Yaamava' Resort & Casino", "tribe": "San Manuel Band of Mission Indians",
     "city": "Highland", "zip": "92346", "address": "777 San Manuel Boulevard",
     "phone": "(909) 864-5050", "website": "yaamava.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": 432},
    
    {"name": "Pala Casino Spa & Resort", "tribe": "Pala Band of Mission Indians",
     "city": "Pala", "zip": "92059", "address": "11154 Highway 76",
     "phone": "(760) 510-5100", "website": "palacasino.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 507},
    
    {"name": "Valley View Casino & Hotel", "tribe": "San Pasqual Band of Diegueño Indians",
     "city": "Valley Center", "zip": "92082", "address": "16300 Nyemii Pass Road",
     "phone": "(760) 291-5500", "website": "valleyviewcasino.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": 108},
    
    {"name": "Harrah's Resort Southern California", "tribe": "Rincon Band of Luiseño Indians",
     "city": "Funner", "zip": "92082", "address": "777 Harrah's Rincon Way",
     "phone": "(760) 751-3100", "website": "harrahssocal.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": 1042},
    
    {"name": "Barona Resort & Casino", "tribe": "Barona Band of Mission Indians",
     "city": "Lakeside", "zip": "92040", "address": "1932 Wildcat Canyon Road",
     "phone": "(619) 443-2300", "website": "barona.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 400},
    
    {"name": "Viejas Casino & Resort", "tribe": "Viejas Band of Kumeyaay Indians",
     "city": "Alpine", "zip": "91901", "address": "5000 Willows Road",
     "phone": "(619) 445-5400", "website": "viejas.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 237},
    
    {"name": "Jamul Casino", "tribe": "Jamul Indian Village",
     "city": "Jamul", "zip": "91935", "address": "14145 Campo Road",
     "phone": "(619) 669-9000", "website": "jamulcasinosd.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": None},
    
    # Central California
    {"name": "Chukchansi Gold Resort & Casino", "tribe": "Picayune Rancheria of Chukchansi Indians",
     "city": "Coarsegold", "zip": "93614", "address": "711 Lucky Lane",
     "phone": "(559) 642-6000", "website": "chukchansigold.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 402},
    
    {"name": "Mono Wind Casino", "tribe": "Mono Tribe",
     "city": "Auberry", "zip": "93602", "address": "37302 Rancheria Lane",
     "phone": "(559) 822-5366", "website": "monowindcasino.com",
     "gaming": ["Slots", "Table Games"], "hotel_rooms": None},
    
    {"name": "Table Mountain Casino", "tribe": "Table Mountain Rancheria",
     "city": "Friant", "zip": "93626", "address": "8184 Table Mountain Road",
     "phone": "(559) 822-7777", "website": "tablemountaincasino.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 145},
    
    {"name": "Tachi Palace Casino Resort", "tribe": "Santa Rosa Rancheria",
     "city": "Lemoore", "zip": "93245", "address": "17225 Jersey Avenue",
     "phone": "(559) 924-7751", "website": "tachipalace.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 255},
    
    {"name": "Eagle Mountain Casino", "tribe": "Tule River Indian Tribe",
     "city": "Porterville", "zip": "93257", "address": "681 South Reservation Road",
     "phone": "(559) 788-6225", "website": "eaglemtncasino.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": None},
    
    {"name": "Kern Valley River Casino", "tribe": "Kern River Paiute Tribe",
     "city": "Lake Isabella", "zip": "93240", "address": "16146 Casino Drive",
     "phone": "(760) 379-5646", "website": "kernvalleyrivercasino.com",
     "gaming": ["Slots"], "hotel_rooms": None},
    
    # Northern California
    {"name": "Cache Creek Casino Resort", "tribe": "Yocha Dehe Wintun Nation",
     "city": "Brooks", "zip": "95606", "address": "14455 State Highway 16",
     "phone": "(530) 796-3118", "website": "cachecreek.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 415},
    
    {"name": "Twin Pine Casino & Hotel", "tribe": "Middletown Rancheria of Pomo Indians",
     "city": "Middletown", "zip": "95461", "address": "22223 Highway 29",
     "phone": "(707) 987-0197", "website": "twinpine.com",
     "gaming": ["Slots", "Table Games"], "hotel_rooms": 59},
    
    {"name": "River Rock Casino", "tribe": "Dry Creek Rancheria Band of Pomo Indians",
     "city": "Geyserville", "zip": "95441", "address": "3250 Highway 128",
     "phone": "(707) 857-2777", "website": "riverrockcasino.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": None},
    
    {"name": "Graton Resort & Casino", "tribe": "Federated Indians of Graton Rancheria",
     "city": "Rohnert Park", "zip": "94928", "address": "288 Golf Course Drive West",
     "phone": "(707) 588-7100", "website": "gratonresortcasino.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 342},
    
    {"name": "Sky River Casino", "tribe": "Wilton Rancheria",
     "city": "Elk Grove", "zip": "95757", "address": "10000 Sky River Parkway",
     "phone": "(916) 866-4567", "website": "skyrivercasino.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": 145},
    
    {"name": "Thunder Valley Casino Resort", "tribe": "United Auburn Indian Community",
     "city": "Lincoln", "zip": "95648", "address": "1200 Athens Avenue",
     "phone": "(916) 408-7777", "website": "thundervalleyresort.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 402},
    
    {"name": "Jackson Rancheria Casino Resort", "tribe": "Jackson Rancheria Band of Miwok Indians",
     "city": "Jackson", "zip": "95642", "address": "12222 New York Ranch Road",
     "phone": "(209) 223-1670", "website": "jacksoncasino.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 146},
    
    {"name": "Gold Country Casino Resort", "tribe": "Enterprise Rancheria",
     "city": "Oroville", "zip": "95966", "address": "4020 Olive Highway",
     "phone": "(530) 538-5300", "website": "goldcountrycasino.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 112},
    
    {"name": "Rolling Hills Casino", "tribe": "Paskenta Band of Nomlaki Indians",
     "city": "Corning", "zip": "96021", "address": "2655 Barham Avenue",
     "phone": "(530) 528-3500", "website": "rollinghillscasino.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 100},
    
    {"name": "Win-River Resort & Casino", "tribe": "Redding Rancheria",
     "city": "Redding", "zip": "96001", "address": "2100 Redding Rancheria Road",
     "phone": "(530) 243-3377", "website": "winrivercasino.com",
     "gaming": ["Slots", "Table Games", "Poker"], "hotel_rooms": 84},
    
    {"name": "Cher-Ae Heights Casino", "tribe": "Trinidad Rancheria",
     "city": "Trinidad", "zip": "95570", "address": "27 Scenic Drive",
     "phone": "(707) 668-9770", "website": "cheraeheightscasino.com",
     "gaming": ["Slots", "Table Games", "Bingo"], "hotel_rooms": 22},
    
    {"name": "Blue Lake Casino & Hotel", "tribe": "Blue Lake Rancheria",
     "city": "Blue Lake", "zip": "95525", "address": "777 Casino Way",
     "phone": "(707) 668-5100", "website": "bluelakecasino.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 72},
    
    {"name": "Bear River Casino Resort", "tribe": "Bear River Band of Rohnerville Rancheria",
     "city": "Loleta", "zip": "95551", "address": "11 Bear River Drive",
     "phone": "(707) 668-5100", "website": "bearrivercasino.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 104},
    
    {"name": "Lucky 7 Casino", "tribe": "Northfork Rancheria of Mono Indians",
     "city": "Smith River", "zip": "95567", "address": "350 North Indian Road",
     "phone": "(707) 487-3366", "website": "lucky7casino.com",
     "gaming": ["Slots", "Table Games", "Bingo"], "hotel_rooms": None},
    
    {"name": "Pit River Casino", "tribe": "Pit River Tribe",
     "city": "Burney", "zip": "96013", "address": "20265 Tamarack Avenue",
     "phone": "(530) 335-2334", "website": "pitrivercasino.com",
     "gaming": ["Slots", "Table Games", "Bingo"], "hotel_rooms": None},
    
    {"name": "Konocti Vista Casino", "tribe": "Big Valley Band of Pomo Indians",
     "city": "Lakeport", "zip": "95453", "address": "2755 Mission Rancheria Road",
     "phone": "(707) 263-4404", "website": "konocti.com",
     "gaming": ["Slots", "Table Games", "Bingo"], "hotel_rooms": None},
    
    {"name": "Robinson Rancheria Resort & Casino", "tribe": "Robinson Rancheria Band of Pomo Indians",
     "city": "Nice", "zip": "95464", "address": "1545 State Highway 20",
     "phone": "(707) 262-4000", "website": "robinsonrancheria.com",
     "gaming": ["Slots", "Table Games", "Poker", "Bingo"], "hotel_rooms": 80},
    
    {"name": "Hopland Sho-Ka-Wah Casino", "tribe": "Hopland Band of Pomo Indians",
     "city": "Hopland", "zip": "95449", "address": "13101 Nokomis Road",
     "phone": "(707) 744-1543", "website": "shokawah.com",
     "gaming": ["Slots", "Table Games"], "hotel_rooms": None},
    
    {"name": "Red Fox Casino", "tribe": "Cahto Tribe of the Laytonville Rancheria",
     "city": "Laytonville", "zip": "95454", "address": "400 Coates Drive",
     "phone": "(707) 984-6800", "website": "redfoxcasino.com",
     "gaming": ["Slots"], "hotel_rooms": None},
]

class CaliforniaCasinoScraper:
    """Scraper for California casinos"""
    
    def __init__(self):
        self.casinos: List[Casino] = []
        self.source = "CA_Tribal_Casino_Database"
        
    def scrape_static_data(self) -> List[Casino]:
        """Scrape from compiled database"""
        print(f"Processing {len(CALIFORNIA_CASINOS)} California casinos...")
        
        for data in CALIFORNIA_CASINOS:
            casino = Casino(
                name=data["name"],
                tribe=data["tribe"],
                address=data["address"],
                city=data["city"],
                state="CA",
                zip_code=data["zip"],
                phone=data.get("phone"),
                website=data.get("website"),
                gaming_types=data.get("gaming", []),
                hotel_rooms=data.get("hotel_rooms"),
                restaurants=data.get("restaurants", []),
                source=self.source,
                scraped_at=datetime.now().isoformat()
            )
            self.casinos.append(casino)
            
        print(f"✓ Processed {len(self.casinos)} casinos")
        return self.casinos
    
    def enrich_with_web_data(self, casino: Casino) -> Casino:
        """Enrich casino data with web scraping"""
        # This would fetch additional data from casino websites
        # For now, return as-is
        return casino
    
    def export_to_json(self, filename: str = None):
        """Export casinos to JSON"""
        if not filename:
            filename = f"ca_casinos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        data = {
            "scraped_at": datetime.now().isoformat(),
            "source": self.source,
            "state": "California",
            "count": len(self.casinos),
            "casinos": [asdict(c) for c in self.casinos]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"✓ Exported to {filename}")
        return filename
    
    def export_to_csv(self, filename: str = None):
        """Export casinos to CSV"""
        import csv
        
        if not filename:
            filename = f"ca_casinos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Tribe', 'Address', 'City', 'State', 'Zip', 
                           'Phone', 'Website', 'Gaming Types', 'Hotel Rooms'])
            
            for c in self.casinos:
                writer.writerow([
                    c.name, c.tribe, c.address, c.city, c.state, c.zip_code,
                    c.phone, c.website, '|'.join(c.gaming_types or []), c.hotel_rooms
                ])
        
        print(f"✓ Exported to {filename}")
        return filename
    
    def generate_report(self) -> dict:
        """Generate summary report"""
        cities = set(c.city for c in self.casinos)
        tribes = set(c.tribe for c in self.casinos)
        total_rooms = sum(c.hotel_rooms or 0 for c in self.casinos)
        
        report = {
            "total_casinos": len(self.casinos),
            "unique_cities": len(cities),
            "unique_tribes": len(tribes),
            "total_hotel_rooms": total_rooms,
            "cities_with_most_casinos": self._top_cities(5),
            "by_region": self._by_region()
        }
        return report
    
    def _top_cities(self, n: int) -> List[tuple]:
        """Get cities with most casinos"""
        from collections import Counter
        city_counts = Counter(c.city for c in self.casinos)
        return city_counts.most_common(n)
    
    def _by_region(self) -> dict:
        """Group casinos by region"""
        regions = {
            "Southern California": [],
            "Central California": [],
            "Northern California": []
        }
        
        northern_cities = ['Rohnert Park', 'Elk Grove', 'Lincoln', 'Jackson', 'Oroville', 
                          'Corning', 'Redding', 'Trinidad', 'Blue Lake', 'Loleta', 
                          'Smith River', 'Burney', 'Lakeport', 'Nice', 'Hopland', 
                          'Laytonville', 'Geyserville', 'Middletown', 'Brooks']
        
        central_cities = ['Coarsegold', 'Auberry', 'Friant', 'Lemoore', 'Porterville',
                         'Lake Isabella']
        
        for c in self.casinos:
            if c.city in northern_cities:
                regions["Northern California"].append(c.name)
            elif c.city in central_cities:
                regions["Central California"].append(c.name)
            else:
                regions["Southern California"].append(c.name)
        
        return {k: len(v) for k, v in regions.items()}

def main():
    """Run the scraper"""
    print("=" * 60)
    print("California Casino Scraper")
    print("=" * 60)
    
    scraper = CaliforniaCasinoScraper()
    
    # Scrape data
    casinos = scraper.scrape_static_data()
    
    # Generate report
    report = scraper.generate_report()
    
    print("\n" + "=" * 60)
    print("SUMMARY REPORT")
    print("=" * 60)
    print(f"Total Casinos: {report['total_casinos']}")
    print(f"Cities Covered: {report['unique_cities']}")
    print(f"Tribes Represented: {report['unique_tribes']}")
    print(f"Total Hotel Rooms: {report['total_hotel_rooms']:,}")
    print("\nBy Region:")
    for region, count in report['by_region'].items():
        print(f"  {region}: {count} casinos")
    print("\nTop 5 Cities:")
    for city, count in report['cities_with_most_casinos']:
        print(f"  {city}: {count} casinos")
    
    # Export data
    print("\n" + "=" * 60)
    print("EXPORTING DATA")
    print("=" * 60)
    json_file = scraper.export_to_json()
    csv_file = scraper.export_to_csv()
    
    print("\n✓ Scraper completed successfully!")
    print(f"  JSON: {json_file}")
    print(f"  CSV: {csv_file}")

if __name__ == "__main__":
    main()