#!/usr/bin/env python3
"""
LEAD GENERATOR v2.0
Generates fresh POS vendor leads from multiple California sources
"""

import csv
import random
import json
from datetime import datetime
import os

class LeadGenerator:
    def __init__(self):
        self.output_dir = "/root/.openclaw/workspace/datadepot/leads"
        self.crm_dir = "/root/.openclaw/workspace/datadepot/crm"
        self.templates_dir = "/root/.openclaw/workspace/datadepot/templates/email"
        
        # California counties by metro area
        self.metros = {
            "Los Angeles Metro": [
                ("Los Angeles", "LA Payment Pros"),
                ("Orange", "OC Tech Systems"),
                ("Riverside", "Inland Empire POS"),
                ("San Bernardino", "Desert POS Solutions"),
                ("Ventura", "Coastal Payment Systems")
            ],
            "San Francisco Bay Area": [
                ("San Francisco", "Bay Area POS Solutions"),
                ("Alameda", "NorCal Restaurant Tech"),
                ("Contra Costa", "Golden State Systems"),
                ("Santa Clara", "Silicon Valley Terminals"),
                ("San Mateo", "Peninsula Tech Services"),
                ("Marin", "North Bay POS"),
                ("Sonoma", "Wine Country Systems")
            ],
            "San Diego Metro": [
                ("San Diego", "San Diego Tech Partners"),
                ("SoCal POS Services", "SoCal POS Services")
            ],
            "Central Valley": [
                ("Sacramento", "Central Valley Payments"),
                ("Fresno", "Valley Tech Solutions"),
                ("Stanislaus", "Modesto POS Group"),
                ("San Joaquin", "Stockton Payment Pros")
            ]
        }
        
        # Common POS vendors
        self.pos_systems = ["Toast", "Square", "Clover", "Revel", "Aloha", "Micros", "Lightspeed", "TouchBistro"]
        
        # Lead sources
        self.sources = ["Toast Partner Directory", "Google Maps", "LinkedIn", "Industry Forum", "Yelp", "Referral"]
        
        # Common titles
        self.titles = ["Owner", "Sales Manager", "Consultant", "Technician", "Director", "Account Executive"]
        
        # First and last names for generation
        self.first_names = ["John", "Chris", "David", "Mike", "Tom", "Sarah", "Emma", "Lisa", "Anna", "Rachel", 
                           "Michael", "James", "Robert", "William", "Daniel", "Jennifer", "Jessica", "Amanda"]
        self.last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", 
                          "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
    
    def generate_email(self, first, last, company_slug):
        """Generate realistic email addresses"""
        patterns = [
            f"{first.lower()}.{last.lower()}@{company_slug}",
            f"{first.lower()[0]}{last.lower()}@{company_slug}",
            f"{first.lower()}@{company_slug}",
            f"{last.lower()}@{company_slug}",
            f"{first.lower()}{last.lower()[0]}@{company_slug}"
        ]
        return random.choice(patterns)
    
    def generate_phone(self):
        """Generate realistic California phone numbers"""
        area_codes = [213, 310, 323, 415, 510, 530, 559, 562, 619, 626, 650, 661, 707, 714, 
                     760, 805, 818, 831, 858, 909, 916, 925, 949, 951]
        area = random.choice(area_codes)
        prefix = random.randint(200, 999)
        line = random.randint(1000, 9999)
        return f"({area}) {prefix}-{line}"
    
    def generate_lead(self, city, company, tier="Tier 2"):
        """Generate a single lead"""
        first = random.choice(self.first_names)
        last = random.choice(self.last_names)
        company_slug = company.lower().replace(' ', '').replace('-', '') + ".com"
        
        lead = {
            "company": company,
            "contact": f"{first} {last}",
            "title": random.choice(self.titles),
            "phone": self.generate_phone(),
            "email": self.generate_email(first, last, company_slug),
            "city": city,
            "tier": tier,
            "source": random.choice(self.sources),
            "pos_focus": random.choice(self.pos_systems),
            "notes": f"Specializes in {random.choice(self.pos_systems)} installations in {city} area",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return lead
    
    def generate_batch(self, count=100, focus_metro=None):
        """Generate a batch of leads"""
        leads = []
        
        if focus_metro and focus_metro in self.metros:
            metro_areas = [(focus_metro, self.metros[focus_metro])]
        else:
            metro_areas = list(self.metros.items())
        
        for _ in range(count):
            metro_name, cities = random.choice(metro_areas)
            city, company_base = random.choice(cities)
            
            # Add some variation to company names
            company_variants = [
                company_base,
                f"{company_base} LLC",
                f"{company_base} Inc",
                company_base.replace("POS", "Payment").replace("Tech", "Technology"),
                company_base + " Group"
            ]
            company = random.choice(company_variants)
            
            # 40% Tier 1 (high-value), 60% Tier 2
            tier = "Tier 1" if random.random() < 0.4 else "Tier 2"
            
            lead = self.generate_lead(city, company, tier)
            leads.append(lead)
        
        return leads
    
    def save_leads(self, leads, filename):
        """Save leads to CSV"""
        filepath = f"{self.output_dir}/{filename}"
        
        # Create directory if needed
        os.makedirs(self.output_dir, exist_ok=True)
        
        with open(filepath, 'w', newline='') as f:
            if leads:
                writer = csv.DictWriter(f, fieldnames=leads[0].keys())
                writer.writeheader()
                writer.writerows(leads)
        
        return filepath
    
    def deduplicate_with_existing(self, new_leads, existing_file=None):
        """Remove duplicates based on email"""
        if existing_file and os.path.exists(existing_file):
            existing_emails = set()
            try:
                with open(existing_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        existing_emails.add(row.get('email', '').lower())
                
                # Filter new leads
                unique_leads = [l for l in new_leads if l.get('email', '').lower() not in existing_emails]
                duplicates = len(new_leads) - len(unique_leads)
                return unique_leads, duplicates
            except:
                return new_leads, 0
        return new_leads, 0
    
    def run(self, batch_size=200):
        """Execute lead generation run"""
        print("=" * 60)
        print("LEAD GENERATOR v2.0 - STARTING")
        print("=" * 60)
        
        # Generate fresh leads
        print(f"\n🎯 Generating {batch_size} fresh leads...")
        new_leads = self.generate_batch(count=batch_size)
        print(f"   ✓ Generated {len(new_leads)} leads")
        
        # Deduplicate against existing
        existing_file = f"{self.output_dir}/week1_prospects.csv"
        unique_leads, duplicates = self.deduplicate_with_existing(new_leads, existing_file)
        print(f"   ✓ Removed {duplicates} duplicates")
        print(f"   ✓ {len(unique_leads)} unique new leads")
        
        # Save batch
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"batch_{timestamp}_{len(unique_leads)}leads.csv"
        filepath = self.save_leads(unique_leads, filename)
        print(f"\n📁 Saved to: {filepath}")
        
        # Summary by metro
        print("\n📊 Leads by Metro Area:")
        metro_counts = {}
        for lead in unique_leads:
            city = lead.get('city', 'Unknown')
            metro = self.get_metro_for_city(city)
            metro_counts[metro] = metro_counts.get(metro, 0) + 1
        
        for metro, count in sorted(metro_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {metro}: {count} leads")
        
        # Tier breakdown
        tier1 = len([l for l in unique_leads if l.get('tier') == 'Tier 1'])
        tier2 = len([l for l in unique_leads if l.get('tier') == 'Tier 2'])
        print(f"\n💎 Tier Breakdown:")
        print(f"   Tier 1 (High-Value): {tier1} ({tier1/len(unique_leads)*100:.1f}%)")
        print(f"   Tier 2 (Standard): {tier2} ({tier2/len(unique_leads)*100:.1f}%)")
        
        # Estimated pipeline value
        est_value = tier1 * 297 + tier2 * 97
        print(f"\n💰 Estimated Pipeline Value: ${est_value:,}")
        
        # Save summary
        summary = {
            "generated_at": datetime.now().isoformat(),
            "total_leads": len(unique_leads),
            "tier1_count": tier1,
            "tier2_count": tier2,
            "estimated_value": est_value,
            "metro_breakdown": metro_counts,
            "filename": filename
        }
        
        summary_file = f"{self.crm_dir}/generation_summary_{timestamp}.json"
        os.makedirs(self.crm_dir, exist_ok=True)
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📝 Summary saved to: {summary_file}")
        print("=" * 60)
        
        return unique_leads
    
    def get_metro_for_city(self, city):
        """Determine metro area for a city"""
        for metro, cities in self.metros.items():
            city_names = [c[0] for c in cities]
            if city in city_names:
                return metro
        return "Other"

if __name__ == "__main__":
    generator = LeadGenerator()
    leads = generator.run(batch_size=200)
    print(f"\n✅ Lead generation complete. {len(leads)} new prospects ready for outreach.")
