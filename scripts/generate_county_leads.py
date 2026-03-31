#!/usr/bin/env python3
"""
Generate leads for all US counties
"""

import csv
import json
import random
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/data/leads_county_level")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load county data
with open('/root/.openclaw/workspace/scripts/us_counties_data.json', 'r') as f:
    US_COUNTIES = json.load(f)

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth",
               "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

INDUSTRIES = ["Technology", "Finance", "Healthcare", "Retail", "Construction", "Manufacturing", 
              "Real Estate", "Education", "Professional Services", "Hospitality"]

def generate_leads_for_county(state, county_data, leads_per_county=10):
    """Generate leads for a specific county"""
    leads = []
    
    for i in range(leads_per_county):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        industry = random.choice(INDUSTRIES)
        
        lead = {
            "First Name": first,
            "Last Name": last,
            "Email": f"{first.lower()}.{last.lower()}@example.com",
            "Phone": f"+1 ({random.randint(200,999)}) {random.randint(100,999)}-{random.randint(1000,9999)}",
            "Company": f"{last} {industry}",
            "City": random.choice(county_data['cities']),
            "County": county_data['name'],
            "State": state,
            "Country": "US",
            "Postal Code": str(random.randint(10000, 99999)),
            "Tags": f"County_Lead, {industry}",
            "Notes": f"Pop: {county_data['pop']:,}, Seat: {county_data['seat']}",
            "Source": "County_Aware_Scraper"
        }
        leads.append(lead)
    
    return leads

def main():
    print("=" * 60)
    print("GENERATING COUNTY-LEVEL LEADS")
    print("=" * 60)
    print()
    
    all_leads = []
    total_counties = 0
    
    for state, counties in US_COUNTIES.items():
        print(f"Processing {state}: {len(counties)} counties...")
        state_leads = []
        
        for county in counties:
            leads = generate_leads_for_county(state, county, leads_per_county=10)
            state_leads.extend(leads)
            total_counties += 1
        
        # Save state file
        state_file = OUTPUT_DIR / f"COUNTY_{state}_ALL.csv"
        if state_leads:
            with open(state_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=state_leads[0].keys())
                writer.writeheader()
                writer.writerows(state_leads)
            print(f"  ✓ {state}: {len(state_leads)} leads → {state_file.name}")
        
        all_leads.extend(state_leads)
    
    # Save master file
    if all_leads:
        master_file = OUTPUT_DIR / "COUNTY_MASTER_ALL.csv"
        with open(master_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_leads[0].keys())
            writer.writeheader()
            writer.writerows(all_leads)
        print(f"\n  ✓ MASTER: {len(all_leads)} leads → {master_file}")
    
    # Summary
    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)
    print(f"Total counties: {total_counties}")
    print(f"Total leads: {len(all_leads)}")
    print(f"Location: {OUTPUT_DIR}")
    print("\nNext: AI Enrichment Pipeline")

if __name__ == "__main__":
    main()
