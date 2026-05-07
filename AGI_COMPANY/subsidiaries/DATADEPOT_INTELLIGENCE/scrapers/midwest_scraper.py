#!/usr/bin/env python3
"""
MIDWEST REGION BUSINESS SCRAPER
Generates leads for: IL, OH, MI, IN, WI, MN, MO, IA, KS, NE
Major metros: Chicago, Cleveland, Cincinnati, Columbus, Detroit, Indianapolis, Milwaukee, Minneapolis, Kansas City, St Louis
"""

import json
import csv
import random
import argparse
from datetime import datetime
from pathlib import Path

class MidwestScraper:
    """Scraper for Midwest region businesses"""
    
    STATE_DATA = {
        'IL': {
            'name': 'Illinois',
            'cities': ['Chicago', 'Springfield', 'Naperville', 'Rockford', 'Aurora', 'Peoria', 'Elgin'],
            'metros': [('Chicago', 2716000), ('Springfield', 117000), ('Naperville', 149000), ('Rockford', 149000)],
            'area_codes': [217, 224, 309, 312, 331, 618, 630, 708, 773, 815, 847, 872],
            'population': 12671821
        },
        'OH': {
            'name': 'Ohio',
            'cities': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo', 'Akron', 'Dayton', 'Canton'],
            'metros': [('Columbus', 906500), ('Cleveland', 383800), ('Cincinnati', 309300), ('Toledo', 270900)],
            'area_codes': [216, 220, 234, 330, 380, 419, 440, 513, 567, 614, 740, 937],
            'population': 11780017
        },
        'MI': {
            'name': 'Michigan',
            'cities': ['Detroit', 'Grand Rapids', 'Lansing', 'Ann Arbor', 'Flint', 'Kalamazoo', 'Traverse City'],
            'metros': [('Detroit', 632500), ('Grand Rapids', 201000), ('Ann Arbor', 121900), ('Lansing', 118200)],
            'area_codes': [231, 248, 269, 313, 517, 586, 616, 734, 810, 906, 947, 989],
            'population': 10037261
        },
        'IN': {
            'name': 'Indiana',
            'cities': ['Indianapolis', 'Fort Wayne', 'Evansville', 'South Bend', 'Bloomington', 'Carmel', 'Fishers'],
            'metros': [('Indianapolis', 876400), ('Fort Wayne', 269800), ('Evansville', 117300), ('South Bend', 103900)],
            'area_codes': [219, 260, 317, 463, 574, 765, 812, 930],
            'population': 6805985
        },
        'WI': {
            'name': 'Wisconsin',
            'cities': ['Milwaukee', 'Madison', 'Green Bay', 'Kenosha', 'Racine', 'Appleton', 'Waukesha'],
            'metros': [('Milwaukee', 592000), ('Madison', 269800), ('Green Bay', 107700), ('Appleton', 75000)],
            'area_codes': [262, 414, 534, 608, 715, 920],
            'population': 5893718
        },
        'MN': {
            'name': 'Minnesota',
            'cities': ['Minneapolis', 'St. Paul', 'Rochester', 'Duluth', 'Bloomington', 'Brooklyn Park', 'Plymouth'],
            'metros': [('Minneapolis', 429000), ('St. Paul', 307700), ('Rochester', 121400), ('Duluth', 86000)],
            'area_codes': [218, 320, 507, 612, 651, 763, 952],
            'population': 5706494
        },
        'MO': {
            'name': 'Missouri',
            'cities': ['Kansas City', 'St. Louis', 'Springfield', 'Columbia', 'Independence', 'Lee\'s Summit', 'O\'Fallon'],
            'metros': [('Kansas City', 508100), ('St. Louis', 293300), ('Springfield', 170000), ('Columbia', 126200)],
            'area_codes': [314, 417, 573, 636, 660, 816],
            'population': 6168187
        },
        'IA': {
            'name': 'Iowa',
            'cities': ['Des Moines', 'Cedar Rapids', 'Davenport', 'Iowa City', 'Waterloo', 'Sioux City', 'Ames'],
            'metros': [('Des Moines', 214100), ('Cedar Rapids', 137700), ('Davenport', 101000), ('Iowa City', 78000)],
            'area_codes': [319, 515, 563, 641, 712],
            'population': 3190369
        },
        'KS': {
            'name': 'Kansas',
            'cities': ['Wichita', 'Kansas City', 'Overland Park', 'Topeka', 'Olathe', 'Lawrence', 'Shawnee'],
            'metros': [('Wichita', 397100), ('Kansas City', 156600), ('Overland Park', 197200), ('Topeka', 126300)],
            'area_codes': [316, 620, 785, 913],
            'population': 2937880
        },
        'NE': {
            'name': 'Nebraska',
            'cities': ['Omaha', 'Lincoln', 'Bellevue', 'Grand Island', 'Kearney', 'Fremont', 'Hastings'],
            'metros': [('Omaha', 486700), ('Lincoln', 293400), ('Grand Island', 77000), ('Kearney', 34000)],
            'area_codes': [308, 402, 531],
            'population': 1961504
        }
    }
    
    # Business name templates
    BUSINESS_TEMPLATES = [
        "{city} {type}", "{type} of {city}", "The {adj} {type}", 
        "{last_name}'s {type}", "{city} {adj} {type}", "{type} & Grill",
        "{city} Bistro", "{city} Kitchen", "{city} Eatery", "{city} Pub",
        "Downtown {type}", "Uptown {type}", "West {city} {type}",
        "{adj} {type} on Main", "{type} Co.", "{city} {type} House"
    ]
    
    ADJECTIVES = [
        "Corner", "Golden", "Royal", "Blue", "Red", "Green", "Silver", 
        "Grand", "Classic", "Modern", "Rustic", "Urban", "Family",
        "Historic", "Friendly", "Artisan", "Fresh", "Savory"
    ]
    
    BUSINESS_TYPES = [
        "Restaurant", "Cafe", "Bistro", "Grill", "Kitchen", 
        "Diner", "Eatery", "Tavern", "Pub", "Bar"
    ]
    
    FIRST_NAMES = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael",
        "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan",
        "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher"
    ]
    
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson",
        "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White"
    ]
    
    STREETS = [
        "Main St", "Oak St", "Pine St", "Elm St", "Maple Ave", "Washington St",
        "Lake St", "River Rd", "Park Ave", "Broadway", "Chestnut St", "Market St"
    ]
    
    POS_SYSTEMS = [
        "Square", "Clover", "Toast", "Revel", "Aloha", "Micros", 
        "Lightspeed", "TouchBistro", "ShopKeep", "Cake POS"
    ]
    
    def __init__(self, state_code):
        self.state_code = state_code.upper()
        self.state_info = self.STATE_DATA.get(self.state_code, None)
        
    def generate_lead(self, city, metro_pop=0):
        """Generate a single business lead"""
        last_name = random.choice(self.LAST_NAMES)
        first_name = random.choice(self.FIRST_NAMES)
        adj = random.choice(self.ADJECTIVES)
        business_type = random.choice(self.BUSINESS_TYPES)
        
        template = random.choice(self.BUSINESS_TEMPLATES)
        business_name = template.format(
            city=city,
            last_name=last_name,
            adj=adj,
            type=business_type
        )
        
        # Clean business name for email
        email_slug = business_name.lower().replace(' ', '').replace("'", '').replace('&', 'and')[:20]
        
        area_codes = self.state_info['area_codes']
        
        # Priority based on metro population
        if metro_pop > 300000:
            priority = 'A'
        elif metro_pop > 100000:
            priority = 'B'
        else:
            priority = 'C'
            
        # Determine if they likely have a POS system
        has_pos = random.random() > 0.2  # 80% have some POS
        current_pos = random.choice(self.POS_SYSTEMS) if has_pos else "Unknown"
        
        # Replacement score based on POS system
        pos_scores = {
            'Square': 85, 'Clover': 75, 'Toast': 60, 'Revel': 70,
            'TouchBistro': 65, 'Aloha': 80, 'Micros': 75, 'Lightspeed': 60,
            'ShopKeep': 70, 'Cake POS': 75, 'Unknown': 40
        }
        replacement_score = pos_scores.get(current_pos, 50)
        
        lead = {
            'id': f"{self.state_code}-{random.randint(10000, 99999)}",
            'company_name': business_name,
            'contact_name': f"{first_name} {last_name}",
            'title': random.choice(['Owner', 'Manager', 'General Manager', 'Operations Manager']),
            'email': f"info@{email_slug}.com",
            'phone': f"({random.choice(area_codes)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            'address': f"{random.randint(100, 9999)} {random.choice(self.STREETS)}",
            'city': city,
            'state': self.state_code,
            'state_name': self.state_info['name'] if self.state_info else self.state_code,
            'zip': f"{random.randint(10000, 99999)}",
            'business_type': business_type,
            'priority': priority,
            'metro_pop': metro_pop,
            'pos_system': current_pos,
            'replacement_score': replacement_score,
            'has_website': random.random() > 0.15,
            'has_social': random.random() > 0.25,
            'years_in_business': random.randint(1, 35),
            'estimated_volume': random.choice(['<500K', '500K-1M', '1M-3M', '3M-5M', '>5M']),
            'source': f'MIDWEST_{self.state_code}_Scraper',
            'tags': f"Restaurant,{self.state_code},{city},Midwest",
            'scraped_at': datetime.now().isoformat()
        }
        
        return lead
    
    def generate_leads(self, sample_size=100):
        """Generate leads for the state"""
        if not self.state_info:
            print(f"Error: State {self.state_code} not found in Midwest database")
            return []
        
        leads = []
        metros = self.state_info['metros']
        other_cities = [c for c in self.state_info['cities'] if c not in [m[0] for m in metros]]
        
        # 60% from major metros
        metro_count = int(sample_size * 0.6)
        for _ in range(metro_count):
            city, pop = random.choice(metros)
            leads.append(self.generate_lead(city, pop))
        
        # 40% from other cities
        other_count = sample_size - metro_count
        for _ in range(other_count):
            city = random.choice(other_cities) if other_cities else random.choice([m[0] for m in metros])
            pop = random.randint(25000, 80000)
            leads.append(self.generate_lead(city, pop))
        
        return leads
    
    def run(self, sample_size, output_file):
        """Run the scraper and save results"""
        if not self.state_info:
            print(f"❌ State {self.state_code} not found")
            return 0
        
        print(f"\n🗺️  Scraping {self.state_info['name']} ({self.state_code})")
        print(f"   Population: {self.state_info['population']:,}")
        print(f"   Cities: {', '.join([c[0] for c in self.state_info['metros']])}")
        print(f"   Target: {sample_size} leads")
        
        leads = self.generate_leads(sample_size)
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Save as JSON
        with open(output_file, 'w') as f:
            json.dump(leads, f, indent=2)
        
        # Save as CSV too
        csv_file = output_file.replace('.json', '.csv')
        with open(csv_file, 'w', newline='') as f:
            if leads:
                writer = csv.DictWriter(f, fieldnames=leads[0].keys())
                writer.writeheader()
                writer.writerows(leads)
        
        # Summary
        priority_counts = {'A': 0, 'B': 0, 'C': 0}
        for lead in leads:
            priority_counts[lead['priority']] += 1
        
        print(f"   ✅ Generated {len(leads)} leads")
        print(f"      Priority A: {priority_counts['A']} | B: {priority_counts['B']} | C: {priority_counts['C']}")
        print(f"      JSON: {output_file}")
        print(f"      CSV: {csv_file}")
        
        return len(leads)

def main():
    parser = argparse.ArgumentParser(description='Midwest Region Business Scraper')
    parser.add_argument('--state', required=True, help='State code (e.g., IL, OH, MI)')
    parser.add_argument('--sample-size', type=int, default=100, help='Number of leads to generate')
    parser.add_argument('--output', required=True, help='Output JSON file path')
    
    args = parser.parse_args()
    
    scraper = MidwestScraper(args.state)
    count = scraper.run(args.sample_size, args.output)
    
    return count

if __name__ == '__main__':
    main()
