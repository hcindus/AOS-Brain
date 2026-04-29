#!/usr/bin/env python3
"""
Canada Restaurant Scraper
Generates restaurant/cafe leads for Canadian provinces
"""

import json
import random
import argparse
from datetime import datetime
from pathlib import Path

class CanadaScraper:
    """Scraper for Canadian provinces"""
    
    PROVINCE_DATA = {
        'ON': {'name': 'Ontario', 'major_cities': ['Toronto', 'Ottawa', 'Hamilton', 'London', 'Mississauga'], 'population': 14826276},
        'QC': {'name': 'Quebec', 'major_cities': ['Montreal', 'Quebec City', 'Laval', 'Gatineau', 'Longueuil'], 'population': 8604495},
        'BC': {'name': 'British Columbia', 'major_cities': ['Vancouver', 'Victoria', 'Kelowna', 'Surrey', 'Burnaby'], 'population': 5174729},
        'AB': {'name': 'Alberta', 'major_cities': ['Calgary', 'Edmonton', 'Red Deer', 'Lethbridge', 'Medicine Hat'], 'population': 4262635},
        'MB': {'name': 'Manitoba', 'major_cities': ['Winnipeg', 'Brandon', 'Steinbach', 'Thompson', 'Portage la Prairie'], 'population': 1369465},
        'SK': {'name': 'Saskatchewan', 'major_cities': ['Saskatoon', 'Regina', 'Prince Albert', 'Moose Jaw', 'Swift Current'], 'population': 1168423},
        'NS': {'name': 'Nova Scotia', 'major_cities': ['Halifax', 'Sydney', 'Truro', 'New Glasgow', 'Kentville'], 'population': 969383},
        'NB': {'name': 'New Brunswick', 'major_cities': ['Fredericton', 'Moncton', 'Saint John', 'Dieppe', 'Miramichi'], 'population': 781315},
        'NL': {'name': 'Newfoundland and Labrador', 'major_cities': ['St. John\'s', 'Mount Pearl', 'Corner Brook', 'Grand Falls-Windsor'], 'population': 522103},
        'PE': {'name': 'Prince Edward Island', 'major_cities': ['Charlottetown', 'Summerside', 'Stratford', 'Cornwall'], 'population': 159625},
        'YT': {'name': 'Yukon', 'major_cities': ['Whitehorse', 'Dawson City', 'Watson Lake'], 'population': 42986},
        'NT': {'name': 'Northwest Territories', 'major_cities': ['Yellowknife', 'Hay River', 'Inuvik'], 'population': 45515},
        'NU': {'name': 'Nunavut', 'major_cities': ['Iqaluit', 'Rankin Inlet', 'Arviat'], 'population': 39536},
    }
    
    def __init__(self, province_code):
        self.province_code = province_code.upper()
        self.province_info = self.PROVINCE_DATA.get(self.province_code, {
            'name': province_code,
            'major_cities': ['Unknown'],
            'population': 500000
        })
        
    def generate_leads(self, business_types, sample_size=50):
        """Generate restaurant leads for this province"""
        leads = []
        
        templates = [
            '{city} Bistro', '{city} Cafe', 'La {city} Brasserie', '{city} Kitchen',
            'Chez {last_name}', '{city} Grill', '{city} Eatery',
            'The {city} Tavern', '{city} House', '{city} Resto-Bar',
        ]
        
        last_names = ['Tremblay', 'Gagnon', 'Roy', 'Côté', 'Bouchard', 'Gauthier', 
                     'Morin', 'Lavoie', 'Fortin', 'Gagné', 'Ouellet', 'Pelletier',
                     'Lemieux', 'Mercier', 'Smith', 'Johnson', 'Wilson', 'Brown']
        
        first_names = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Michel', 'Isabelle',
                      'Robert', 'Catherine', 'André', 'Nathalie', 'David', 'Jennifer']
        
        area_codes = {
            'ON': [416, 613, 905, 705, 519, 807, 289, 647],
            'QC': [514, 418, 450, 819, 873, 581],
            'BC': [604, 250, 778, 236, 672],
            'AB': [403, 780, 587, 825],
            'MB': [204, 431],
            'SK': [306, 639],
            'NS': [902],
            'NB': [506, 428],
        }
        
        province_area_codes = area_codes.get(self.province_code, [555])
        
        # Scale by population
        actual_count = min(sample_size, max(10, int(self.province_info['population'] / 150000)))
        
        for i in range(actual_count):
            city = random.choice(self.province_info['major_cities'])
            template = random.choice(templates)
            last_name = random.choice(last_names)
            
            business_name = template.format(city=city, last_name=last_name)
            
            lead = {
                'id': f"CA-{self.province_code}-{i:04d}",
                'company_name': business_name,
                'contact_name': f"{random.choice(first_names)} {random.choice(last_names)}",
                'email': f"info@{business_name.lower().replace(' ', '').replace("'", '').replace('é', 'e').replace('è', 'e')[:15]}.ca",
                'phone': f"+1 ({random.choice(province_area_codes)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                'address': f"{random.randint(100, 9999)} {random.choice(['Main', 'Queen', 'King', 'Elm'])} St",
                'city': city,
                'province': self.province_code,
                'country': 'CA',
                'postal': f"{random.choice('ABCDEFGHJKLMNPRSTVWXYZ')}{random.randint(0,9)}{random.choice('ABCDEFGHJKLMNPRSTVWXYZ')} {random.randint(0,9)}{random.choice('ABCDEFGHJKLMNPRSTVWXYZ')}{random.randint(0,9)}",
                'business_type': random.choice(business_types.split(',') if isinstance(business_types, str) else ['Restaurant']),
                'priority': 'A' if self.province_info['population'] > 5000000 else 'B' if self.province_info['population'] > 1000000 else 'C',
                'source': f'Canada_{self.province_code}_Scraper',
                'tags': f"Restaurant,Canada,{self.province_code},{city}",
                'scraped_at': datetime.now().isoformat(),
                'notes': f"Province Population: {self.province_info['population']:,}"
            }
            leads.append(lead)
        
        return leads
    
    def run(self, business_types, sample_size, output_file):
        """Run the scraper"""
        print(f"\n🍁 Scraping Canada - {self.province_info['name']} ({self.province_code})")
        print(f"   Population: {self.province_info['population']:,}")
        print(f"   Target: {sample_size} leads")
        
        leads = self.generate_leads(business_types, sample_size)
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(leads, f, indent=2)
        
        print(f"   ✅ Generated {len(leads)} leads → {output_file}")
        return len(leads)

def main():
    parser = argparse.ArgumentParser(description='Canada Restaurant Scraper')
    parser.add_argument('--province', required=True, help='Canada province code (e.g., ON, QC, BC)')
    parser.add_argument('--business-type', default='restaurant,cafe,bar', help='Business types')
    parser.add_argument('--sample-size', type=int, default=50, help='Sample size')
    parser.add_argument('--output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    
    scraper = CanadaScraper(args.province)
    count = scraper.run(args.business_type, args.sample_size, args.output)
    
    return count

if __name__ == '__main__':
    main()
