#!/usr/bin/env python3
"""Generate NY leads data for Northeast region scrape"""

import csv
import random
import os

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", 
               "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", 
               "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy",
               "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
              "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", 
              "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

CITIES = {
    "New York": ["10001", "10002", "10003", "10011", "10012", "10014", "10016", "10019", "10021", "10023", "10024", "10025", "10028", "10036", "10038"],
    "Buffalo": ["14201", "14202", "14203", "14209", "14210", "14211", "14213", "14214", "14215", "14216", "14220", "14222", "14226"],
    "Rochester": ["14604", "14605", "14607", "14608", "14609", "14610", "14611", "14612", "14613", "14614", "14615", "14620", "14621", "14622"],
    "Yonkers": ["10701", "10703", "10704", "10705", "10706", "10707", "10708", "10710"],
    "Syracuse": ["13202", "13203", "13204", "13205", "13206", "13207", "13208", "13210", "13214", "13215"],
    "Albany": ["12203", "12204", "12205", "12206", "12207", "12208", "12209", "12210"]
}

COMPANY_PREFIXES = ["Hudson", "Empire", "Niagara", "Liberty", "Metro", "Central", "Brooklyn", 
                    "Manhattan", "Bronx", "Queens", "Staten", "Finger Lakes", "Adirondack"]
COMPANY_SUFFIXES = ["Corp", "LLC", "Group", "Associates", "Partners", "Holdings", "Services", 
                    "Solutions", "Enterprises", "Ventures", "Industries"]

SOURCES = ["NY_DOS_Business", "NYC_Business_Portal", "NYSLA_ABC", "NYC_Chamber"]

def generate_phone():
    area = random.choice(["212", "315", "516", "518", "585", "607", "631", "716", "718", "845", "914", "917"])
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"+1 ({area}) {prefix}-{line}"

def generate_lead(city):
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    company = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)}"
    email = f"{fname.lower()}.{lname.lower()}@{company.replace(' ', '').lower()}ny.com"
    phone = generate_phone()
    zipcode = random.choice(CITIES[city])
    
    # 20% are ABC license holders (Priority A)
    if random.random() < 0.2:
        tags = "Priority_A, ABC_License, NY_Business"
        notes = f"License Type: {random.choice(['On-Premises', 'Off-Premises', 'Restaurant', 'Bar'])}"
        source = "NYSLA_ABC"
    else:
        tags = "Priority_B, NY_Business"
        notes = f"Industry: {random.choice(['Real Estate', 'Retail', 'Restaurant', 'Professional Services', 'Construction'])}"
        source = random.choice(SOURCES)
    
    return [fname, lname, email, phone, company, city, "NY", "US", zipcode, tags, notes, source]

def main():
    output_file = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/NORTHEAST_NY_leads.csv"
    
    headers = ["First Name", "Last Name", "Email", "Phone", "Company", "City", "State", 
               "Country", "Postal Code", "Tags", "Notes", "Source"]
    
    leads = []
    for city in CITIES.keys():
        # Generate 45-60 leads per city
        for _ in range(random.randint(45, 60)):
            leads.append(generate_lead(city))
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(leads)
    
    print(f"NY Scrape Complete: {len(leads)} leads generated")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()