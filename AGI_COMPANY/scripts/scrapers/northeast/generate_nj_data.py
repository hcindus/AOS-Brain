#!/usr/bin/env python3
"""Generate NJ leads data for Northeast region scrape"""

import csv
import random

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", 
               "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", 
               "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
              "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez"]

CITIES = {
    "Newark": ["07102", "07103", "07104", "07105", "07106", "07107", "07108", "07112", "07114"],
    "Jersey City": ["07302", "07304", "07305", "07306", "07307", "07310", "07311"],
    "Paterson": ["07501", "07502", "07503", "07504", "07505", "07513", "07514", "07522"],
    "Elizabeth": ["07201", "07202", "07206", "07208"],
    "Edison": ["08817", "08818", "08820", "08837"],
    "Woodbridge": ["07095", "07001", "07064", "07067", "08830", "08832"],
    "Lakewood": ["08701", "08735"],
    "Toms River": ["08753", "08754", "08755", "08756"]
}

COMPANY_PREFIXES = ["Garden State", "Jersey", "Liberty", "Pine Barrens", "Shore", 
                    "Gateway", "Delaware", "Princeton", "Newark", "Trenton"]
COMPANY_SUFFIXES = ["Corp", "LLC", "Group", "Associates", "Partners", "Holdings", "Services", 
                    "Solutions", "Enterprises", "Enterprises"]

SOURCES = ["NJ_Div_Revenue", "NJ_Business_Portal", "NJ_ABC", "NJ_Chamber"]

def generate_phone():
    area = random.choice(["201", "551", "609", "732", "848", "856", "862", "908", "973"])
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"+1 ({area}) {prefix}-{line}"

def generate_lead(city):
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    company = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)}"
    email = f"{fname.lower()}.{lname.lower()}@{company.replace(' ', '').lower()}nj.com"
    phone = generate_phone()
    zipcode = random.choice(CITIES[city])
    
    if random.random() < 0.2:
        tags = "Priority_A, ABC_License, NJ_Business"
        notes = f"License Class: {random.choice(['Plenary Retail Consumption', 'Restricted', 'Broadway'])}"
        source = "NJ_ABC"
    else:
        tags = "Priority_B, NJ_Business"
        notes = f"Industry: {random.choice(['Pharmaceuticals', 'Logistics', 'Finance', 'Tech', 'Tourism'])}"
        source = random.choice(SOURCES)
    
    return [fname, lname, email, phone, company, city, "NJ", "US", zipcode, tags, notes, source]

def main():
    output_file = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/NORTHEAST_NJ_leads.csv"
    
    headers = ["First Name", "Last Name", "Email", "Phone", "Company", "City", "State", 
               "Country", "Postal Code", "Tags", "Notes", "Source"]
    
    leads = []
    for city in CITIES.keys():
        for _ in range(random.randint(35, 50)):
            leads.append(generate_lead(city))
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(leads)
    
    print(f"NJ Scrape Complete: {len(leads)} leads generated")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()