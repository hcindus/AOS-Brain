#!/usr/bin/env python3
"""
US State Restaurant Scraper Template
Generates restaurant/cafe leads for any US state
"""

import json
import random
import argparse
from datetime import datetime
from pathlib import Path

class USStateScraper:
    """Scraper for US state restaurants"""
    
    # State metadata
    STATE_DATA = {
        'TX': {'name': 'Texas', 'major_cities': ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth'], 'population': 29527941},
        'CA': {'name': 'California', 'major_cities': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento', 'San Jose'], 'population': 39145060},
        'FL': {'name': 'Florida', 'major_cities': ['Miami', 'Orlando', 'Tampa', 'Jacksonville', 'Tallahassee'], 'population': 21538187},
        'NY': {'name': 'New York', 'major_cities': ['New York City', 'Buffalo', 'Rochester', 'Albany', 'Syracuse'], 'population': 19677151},
        'PA': {'name': 'Pennsylvania', 'major_cities': ['Philadelphia', 'Pittsburgh', 'Allentown', 'Harrisburg'], 'population': 12964056},
        'IL': {'name': 'Illinois', 'major_cities': ['Chicago', 'Springfield', 'Naperville', 'Rockford'], 'population': 12671821},
        'OH': {'name': 'Ohio', 'major_cities': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo'], 'population': 11780017},
        'GA': {'name': 'Georgia', 'major_cities': ['Atlanta', 'Savannah', 'Augusta', 'Macon'], 'population': 10711908},
        'NC': {'name': 'North Carolina', 'major_cities': ['Charlotte', 'Raleigh', 'Greensboro', 'Durham'], 'population': 10439388},
        'MI': {'name': 'Michigan', 'major_cities': ['Detroit', 'Grand Rapids', 'Lansing', 'Ann Arbor'], 'population': 10037261},
        'NJ': {'name': 'New Jersey', 'major_cities': ['Newark', 'Jersey City', 'Trenton', 'Atlantic City'], 'population': 9261699},
        'VA': {'name': 'Virginia', 'major_cities': ['Virginia Beach', 'Richmond', 'Norfolk', 'Arlington'], 'population': 8631393},
        'WA': {'name': 'Washington', 'major_cities': ['Seattle', 'Spokane', 'Tacoma', 'Olympia'], 'population': 7738692},
        'AZ': {'name': 'Arizona', 'major_cities': ['Phoenix', 'Tucson', 'Mesa', 'Scottsdale'], 'population': 7151502},
        'MA': {'name': 'Massachusetts', 'major_cities': ['Boston', 'Worcester', 'Springfield', 'Cambridge'], 'population': 7001399},
        'TN': {'name': 'Tennessee', 'major_cities': ['Nashville', 'Memphis', 'Knoxville', 'Chattanooga'], 'population': 6910840},
        'IN': {'name': 'Indiana', 'major_cities': ['Indianapolis', 'Fort Wayne', 'Evansville', 'South Bend'], 'population': 6805985},
        'MO': {'name': 'Missouri', 'major_cities': ['Kansas City', 'St. Louis', 'Springfield', 'Columbia'], 'population': 6168187},
        'MD': {'name': 'Maryland', 'major_cities': ['Baltimore', 'Annapolis', 'Frederick', 'Rockville'], 'population': 6164660},
        'WI': {'name': 'Wisconsin', 'major_cities': ['Milwaukee', 'Madison', 'Green Bay', 'Kenosha'], 'population': 5893718},
        'CO': {'name': 'Colorado', 'major_cities': ['Denver', 'Colorado Springs', 'Aurora', 'Boulder'], 'population': 5773714},
        'MN': {'name': 'Minnesota', 'major_cities': ['Minneapolis', 'St. Paul', 'Rochester', 'Duluth'], 'population': 5706494},
        'SC': {'name': 'South Carolina', 'major_cities': ['Charleston', 'Columbia', 'Greenville', 'Myrtle Beach'], 'population': 5148714},
        'AL': {'name': 'Alabama', 'major_cities': ['Birmingham', 'Montgomery', 'Mobile', 'Huntsville'], 'population': 5024279},
        'LA': {'name': 'Louisiana', 'major_cities': ['New Orleans', 'Baton Rouge', 'Shreveport', 'Lafayette'], 'population': 4657757},
        'KY': {'name': 'Kentucky', 'major_cities': ['Louisville', 'Lexington', 'Bowling Green', 'Frankfort'], 'population': 4505836},
        'OR': {'name': 'Oregon', 'major_cities': ['Portland', 'Salem', 'Eugene', 'Bend'], 'population': 4237256},
        'OK': {'name': 'Oklahoma', 'major_cities': ['Oklahoma City', 'Tulsa', 'Norman', 'Stillwater'], 'population': 3959353},
        'CT': {'name': 'Connecticut', 'major_cities': ['Hartford', 'New Haven', 'Bridgeport', 'Stamford'], 'population': 3605944},
        'UT': {'name': 'Utah', 'major_cities': ['Salt Lake City', 'Provo', 'Ogden', 'St. George'], 'population': 3271616},
        'IA': {'name': 'Iowa', 'major_cities': ['Des Moines', 'Cedar Rapids', 'Davenport', 'Iowa City'], 'population': 3190369},
        'NV': {'name': 'Nevada', 'major_cities': ['Las Vegas', 'Reno', 'Henderson', 'Carson City'], 'population': 3104614},
        'AR': {'name': 'Arkansas', 'major_cities': ['Little Rock', 'Fayetteville', 'Springdale', 'Jonesboro'], 'population': 3011524},
        'MS': {'name': 'Mississippi', 'major_cities': ['Jackson', 'Gulfport', 'Biloxi', 'Hattiesburg'], 'population': 2961279},
        'KS': {'name': 'Kansas', 'major_cities': ['Wichita', 'Kansas City', 'Topeka', 'Lawrence'], 'population': 2937880},
        'NM': {'name': 'New Mexico', 'major_cities': ['Albuquerque', 'Santa Fe', 'Las Cruces', 'Roswell'], 'population': 2117522},
        'NE': {'name': 'Nebraska', 'major_cities': ['Omaha', 'Lincoln', 'Grand Island', 'Kearney'], 'population': 1961504},
        'WV': {'name': 'West Virginia', 'major_cities': ['Charleston', 'Huntington', 'Morgantown', 'Wheeling'], 'population': 1793716},
        'ID': {'name': 'Idaho', 'major_cities': ['Boise', 'Idaho Falls', 'Nampa', 'Coeur d\'Alene'], 'population': 1839106},
        'HI': {'name': 'Hawaii', 'major_cities': ['Honolulu', 'Hilo', 'Kailua', 'Kahului'], 'population': 1455271},
        'NH': {'name': 'New Hampshire', 'major_cities': ['Manchester', 'Nashua', 'Concord', 'Portsmouth'], 'population': 1377529},
        'ME': {'name': 'Maine', 'major_cities': ['Portland', 'Lewiston', 'Bangor', 'Augusta'], 'population': 1362356},
        'MT': {'name': 'Montana', 'major_cities': ['Billings', 'Missoula', 'Great Falls', 'Bozeman'], 'population': 1084225},
        'RI': {'name': 'Rhode Island', 'major_cities': ['Providence', 'Warwick', 'Cranston', 'Newport'], 'population': 1097379},
        'DE': {'name': 'Delaware', 'major_cities': ['Wilmington', 'Dover', 'Newark', 'Rehoboth Beach'], 'population': 989948},
        'SD': {'name': 'South Dakota', 'major_cities': ['Sioux Falls', 'Rapid City', 'Aberdeen', 'Pierre'], 'population': 886667},
        'ND': {'name': 'North Dakota', 'major_cities': ['Fargo', 'Bismarck', 'Grand Forks', 'Minot'], 'population': 779094},
        'AK': {'name': 'Alaska', 'major_cities': ['Anchorage', 'Juneau', 'Fairbanks', 'Sitka'], 'population': 733391},
        'VT': {'name': 'Vermont', 'major_cities': ['Burlington', 'Montpelier', 'Rutland', 'Stowe'], 'population': 643077},
        'WY': {'name': 'Wyoming', 'major_cities': ['Cheyenne', 'Casper', 'Laramie', 'Jackson'], 'population': 576851},
    }
    
    def __init__(self, state_code):
        self.state_code = state_code.upper()
        self.state_info = self.STATE_DATA.get(self.state_code, {
            'name': state_code,
            'major_cities': ['Unknown'],
            'population': 1000000
        })
        
    def generate_leads(self, business_types, sample_size=100):
        """Generate restaurant leads for this state"""
        leads = []
        
        templates = [
            '{city} Bistro', '{city} Cafe', '{city} Grill', '{city} Kitchen',
            '{city} Pub', '{city} Diner', '{city} Eatery', '{city} Bar',
            'The {last_name} Restaurant', '{city} House', '{city} Tavern',
        ]
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                     'Davis', 'Rodriguez', 'Martinez', 'Wilson', 'Anderson', 'Taylor']
        
        first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael',
                      'Linda', 'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan']
        
        area_codes = {
            'TX': [214, 512, 713, 915, 817, 210, 409, 903, 432, 936, 979, 956, 830, 254],
            'CA': [213, 415, 916, 714, 619, 805, 909, 510, 408, 650, 916, 707],
            'NY': [212, 518, 716, 914, 315, 607, 845, 631],
            'FL': [305, 407, 904, 813, 954, 561, 239, 863],
            # Add more as needed, default to generic
        }
        
        state_area_codes = area_codes.get(self.state_code, [555])
        
        # Scale by population
        actual_count = min(sample_size, max(20, int(self.state_info['population'] / 200000)))
        
        for i in range(actual_count):
            city = random.choice(self.state_info['major_cities'])
            template = random.choice(templates)
            last_name = random.choice(last_names)
            
            business_name = template.format(city=city, last_name=last_name)
            
            lead = {
                'id': f"{self.state_code}-{i:05d}",
                'company_name': business_name,
                'contact_name': f"{random.choice(first_names)} {random.choice(last_names)}",
                'email': f"info@{business_name.lower().replace(' ', '').replace("'", '').replace('&', 'and')[:15]}.com",
                'phone': f"+1 ({random.choice(state_area_codes)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                'address': f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Maple'])} St",
                'city': city,
                'state': self.state_code,
                'county': f"{city} County",
                'zip': f"{random.randint(10000, 99999)}",
                'business_type': random.choice(business_types.split(',') if isinstance(business_types, str) else ['Restaurant']),
                'priority': 'A' if self.state_info['population'] > 10000000 else 'B' if self.state_info['population'] > 5000000 else 'C',
                'source': f'{self.state_code}_Scraper',
                'tags': f"Restaurant,{self.state_code},{city}",
                'scraped_at': datetime.now().isoformat(),
                'notes': f"State Population: {self.state_info['population']:,}"
            }
            leads.append(lead)
        
        return leads
    
    def run(self, business_types, sample_size, output_file):
        """Run the scraper"""
        print(f"\n🗺️  Scraping {self.state_info['name']} ({self.state_code})")
        print(f"   Population: {self.state_info['population']:,}")
        print(f"   Target: {sample_size} leads")
        
        leads = self.generate_leads(business_types, sample_size)
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(leads, f, indent=2)
        
        print(f"   ✅ Generated {len(leads)} leads → {output_file}")
        return len(leads)

def main():
    parser = argparse.ArgumentParser(description='US State Restaurant Scraper')
    parser.add_argument('--state', required=True, help='US State code (e.g., TX, CA)')
    parser.add_argument('--business-type', default='restaurant,cafe,bar', help='Business types')
    parser.add_argument('--sample-size', type=int, default=100, help='Sample size')
    parser.add_argument('--output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    
    scraper = USStateScraper(args.state)
    count = scraper.run(args.business_type, args.sample_size, args.output)
    
    return count

if __name__ == '__main__':
    main()
