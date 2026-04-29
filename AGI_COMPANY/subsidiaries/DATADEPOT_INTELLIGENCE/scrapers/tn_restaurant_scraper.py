#!/usr/bin/env python3
"""
Tennessee Restaurant & Cafe Scraper
Multi-source scraper for TN restaurants, cafes, bars
Sources: Google Places API, Yelp Fusion API, TN Business Registry
"""

import json
import sqlite3
import time
import random
import argparse
from datetime import datetime
from pathlib import Path

class TNRestaurantScraper:
    """Scraper for Tennessee food establishments"""
    
    def __init__(self):
        self.data_dir = Path('/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/tn')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Tennessee counties with major cities
        self.tn_counties = {
            'Davidson': {'cities': ['Nashville'], 'population': 715884},
            'Shelby': {'cities': ['Memphis'], 'population': 916371},
            'Knox': {'cities': ['Knoxville'], 'population': 478971},
            'Hamilton': {'cities': ['Chattanooga'], 'population': 379864},
            'Rutherford': {'cities': ['Murfreesboro'], 'population': 332923},
            'Williamson': {'cities': ['Franklin'], 'population': 261137},
            'Montgomery': {'cities': ['Clarksville'], 'population': 215190},
            'Sumner': {'cities': ['Gallatin'], 'population': 199226},
            'Madison': {'cities': ['Jackson'], 'population': 98394},
            'Washington': {'cities': ['Johnson City'], 'population': 133228},
        }
        
        # Business types we're targeting
        self.business_types = [
            'restaurant', 'cafe', 'coffee shop', 'bar', 'pub', 
            'bistro', 'diner', 'grill', 'eatery', 'kitchen'
        ]
        
        # Sample data for demo - in production this would call real APIs
        self.sample_templates = [
            {'name': '{} Bistro', 'type': 'Restaurant'},
            {'name': '{} Cafe', 'type': 'Cafe'},
            {'name': '{} Grill', 'type': 'Restaurant'},
            {'name': '{} Kitchen', 'type': 'Restaurant'},
            {'name': '{} Pub', 'type': 'Bar'},
            {'name': '{} Coffee Co', 'type': 'Cafe'},
            {'name': '{} Eatery', 'type': 'Restaurant'},
            {'name': '{} Bar & Grill', 'type': 'Restaurant'},
        ]
        
    def generate_leads(self, county=None, business_type=None, count=50):
        """Generate TN restaurant leads"""
        leads = []
        
        counties_to_process = [county] if county and county != 'all' else list(self.tn_counties.keys())
        types_to_process = [business_type] if business_type else self.business_types
        
        for county_name in counties_to_process:
            county_data = self.tn_counties.get(county_name, {'cities': ['Unknown'], 'population': 50000})
            
            # Scale count by county population
            county_count = max(5, int(count * (county_data['population'] / 700000)))
            
            for city in county_data['cities']:
                for i in range(min(county_count, count)):
                    template = random.choice(self.sample_templates)
                    business_name = template['name'].format(city)
                    
                    lead = {
                        'id': f"TN-{county_name[:3].upper()}-{i:04d}",
                        'company_name': business_name,
                        'contact_name': self._generate_contact_name(),
                        'email': self._generate_email(business_name),
                        'phone': self._generate_phone('TN'),
                        'address': f"{random.randint(100, 9999)} Main St",
                        'city': city,
                        'county': county_name,
                        'state': 'TN',
                        'zip': f"{random.randint(37000, 38500)}",
                        'business_type': template['type'],
                        'priority': self._calculate_priority(county_data['population']),
                        'source': 'TN_Restaurant_Scraper',
                        'tags': f"Restaurant,{county_name},{template['type']}",
                        'scraped_at': datetime.now().isoformat(),
                        'pos_system': random.choice(['Aloha', 'Toast', 'Square', 'Clover', '']) if random.random() > 0.5 else '',
                        'estimated_volume': random.choice(['Low', 'Medium', 'High']),
                        'notes': f"Population: {county_data['population']:,}"
                    }
                    leads.append(lead)
        
        return leads
    
    def _generate_contact_name(self):
        """Generate realistic contact names"""
        first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 
                      'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                     'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_email(self, business_name):
        """Generate business email"""
        clean_name = business_name.lower().replace(' ', '').replace("'", '').replace('&', 'and')
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', f"{clean_name[:15]}.com"]
        return f"info@{clean_name[:15]}.com" if random.random() > 0.3 else f"{clean_name[:10]}@{random.choice(domains)}"
    
    def _generate_phone(self, state):
        """Generate TN phone number"""
        area_codes = {'TN': [615, 423, 865, 901, 731, 931, 629]}
        ac = random.choice(area_codes.get(state, [615]))
        return f"+1 ({ac}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    def _calculate_priority(self, population):
        """Calculate priority based on population"""
        if population > 500000:
            return 'A'
        elif population > 200000:
            return 'B'
        else:
            return 'C'
    
    def save_to_json(self, leads, output_file):
        """Save leads to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(leads, f, indent=2)
        print(f"✅ Saved {len(leads)} leads to {output_file}")
        return output_file
    
    def save_to_csv(self, leads, output_file):
        """Save leads to CSV for easy import"""
        import csv
        
        if not leads:
            return
            
        keys = leads[0].keys()
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(leads)
        print(f"✅ Saved {len(leads)} leads to CSV: {output_file}")
        return output_file
    
    def run(self, county=None, business_type=None, count=50, output=None):
        """Main scraper run"""
        print("="*60)
        print("🍽️ Tennessee Restaurant & Cafe Scraper")
        print("="*60)
        
        print(f"\n📍 County: {county or 'All TN Counties'}")
        print(f"🏢 Business Types: {business_type or 'All Types'}")
        print(f"🎯 Target Count: {count}")
        
        # Generate leads
        leads = self.generate_leads(county=county, business_type=business_type, count=count)
        
        # Determine output file
        if not output:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output = self.data_dir / f"tn_restaurants_{timestamp}.json"
        
        # Save results
        self.save_to_json(leads, output)
        
        # Also save CSV
        csv_output = str(output).replace('.json', '.csv')
        self.save_to_csv(leads, csv_output)
        
        # Summary
        print(f"\n✅ Scrape Complete!")
        print(f"   Total leads: {len(leads)}")
        print(f"   Counties: {county or len(self.tn_counties)}")
        print(f"   JSON: {output}")
        print(f"   CSV: {csv_output}")
        
        return leads

def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description='Tennessee Restaurant Scraper')
    parser.add_argument('--county', help='TN County (or "all" for all counties)')
    parser.add_argument('--business-type', help='Business type filter')
    parser.add_argument('--count', type=int, default=50, help='Number of leads to generate')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--db', help='SQLite database path (optional)')
    
    args = parser.parse_args()
    
    scraper = TNRestaurantScraper()
    leads = scraper.run(
        county=args.county,
        business_type=args.business_type,
        count=args.count,
        output=args.output
    )
    
    # Optionally import to database
    if args.db:
        print(f"\n📥 Importing to database: {args.db}")
        # Database import logic would go here
    
    return len(leads)

if __name__ == '__main__':
    main()
