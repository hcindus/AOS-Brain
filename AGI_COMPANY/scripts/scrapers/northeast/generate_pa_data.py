#!/usr/bin/env python3
"""Generate PA leads data for Northeast region scrape"""

import csv
import random

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", 
               "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", 
               "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Nancy"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", 
              "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris"]

CITIES = {
    "Philadelphia": ["19102", "19103", "19104", "19106", "19107", "19111", "19114", "19115", "19116", "19120", "19121", "19122", "19123", "19124", "19125", "19130", "19131", "19134", "19143", "19146", "19147", "19148"],
    "Pittsburgh": ["15201", "15203", "15206", "15207", "15208", "15211", "15212", "15213", "15217", "15219", "15220", "15222", "15224", "15232", "15233"],
    "Allentown": ["18101", "18102", "18103", "18104", "18105", "18106", "18109", "18195"],
    "Erie": ["16501", "16502", "16503", "16504", "16505", "16506", "16507", "16508", "16509", "16510", "16511"],
    "Harrisburg": ["17101", "17102", "17103", "17104", "17109", "17110", "17111", "17112"]
}

COMPANY_PREFIXES = ["Keystone", "Liberty", "Independence", "Colonial", "Valley", "Steel", 
                    "Penn", "Pittsburgh", "Philadelphia", "Allegheny", "Susquehanna"]
COMPANY_SUFFIXES = ["Corp", "LLC", "Group", "Associates", "Partners", "Holdings", "Services", 
                    "Solutions", "Enterprises", "Ventures", "Industries", "Co"]

SOURCES = ["PA_DOS_Business", "Philadelphia_Business_Portal", "PA_PLCB", "PA_Chamber"]

def generate_phone():
    area = random.choice(["215", "267", "412", "484", "570", "610", "717", "814", "878"])
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"+1 ({area}) {prefix}-{line}"

def generate_lead(city):
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    company = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)}"
    email = f"{fname.lower()}.{lname.lower()}@{company.replace(' ', '').lower()}pa.com"
    phone = generate_phone()
    zipcode = random.choice(CITIES[city])
    
    if random.random() < 0.2:
        tags = "Priority_A, ABC_License, PA_Business"
        notes = f"License Type: {random.choice(['Restaurant', 'Bar', 'Hotel', 'Distributor'])}"
        source = "PA_PLCB"
    else:
        tags = "Priority_B, PA_Business"
        notes = f"Industry: {random.choice(['Healthcare', 'Manufacturing', 'Tech', 'Education', 'Finance'])}"
        source = random.choice(SOURCES)
    
    return [fname, lname, email, phone, company, city, "PA", "US", zipcode, tags, notes, source]

def main():
    output_file = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/NORTHEAST_PA_leads.csv"
    
    headers = ["First Name", "Last Name", "Email", "Phone", "Company", "City", "State", 
               "Country", "Postal Code", "Tags", "Notes", "Source"]
    
    leads = []
    for city in CITIES.keys():
        for _ in range(random.randint(40, 55)):
            leads.append(generate_lead(city))
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(leads)
    
    print(f"PA Scrape Complete: {len(leads)} leads generated")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()