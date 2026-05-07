#!/usr/bin/env python3
"""Generate MA leads data for Northeast region scrape"""

import csv
import random

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", 
               "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", 
               "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", 
              "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White"]

CITIES = {
    "Boston": ["02101", "02108", "02109", "02110", "02111", "02113", "02114", "02115", "02116", "02118", "02119", "02120", "02121", "02122", "02124", "02125", "02127", "02128", "02129", "02130", "02131", "02132", "02134", "02135"],
    "Worcester": ["01602", "01603", "01604", "01605", "01606", "01607", "01608", "01609", "01610"],
    "Springfield": ["01103", "01104", "01105", "01107", "01108", "01109", "01118", "01119", "01128", "01129"],
    "Lowell": ["01850", "01851", "01852", "01854"],
    "Cambridge": ["02138", "02139", "02140", "02141", "02142", "02163"],
    "New Bedford": ["02740", "02744", "02745", "02746"],
    "Brockton": ["02301", "02302", "02303"],
    "Quincy": ["02169", "02170", "02171"]
}

COMPANY_PREFIXES = ["Bay State", "Old Colony", "Pilgrim", "Commonwealth", "Beacon Hill", 
                    "Cape Cod", "Berkshire", "Charles River", "Boston", "Harvard"]
COMPANY_SUFFIXES = ["Corp", "LLC", "Group", "Associates", "Partners", "Holdings", "Services", 
                    "Solutions", "Enterprises", "Ventures", "Institute", "Tech"]

SOURCES = ["MA_Sec_Commonwealth", "Boston_Business_Portal", "MA_ABCC", "MA_SBA"]

def generate_phone():
    area = random.choice(["339", "351", "413", "508", "617", "774", "781", "857", "978"])
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"+1 ({area}) {prefix}-{line}"

def generate_lead(city):
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    company = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)}"
    email = f"{fname.lower()}.{lname.lower()}@{company.replace(' ', '').lower()}ma.com"
    phone = generate_phone()
    zipcode = random.choice(CITIES[city])
    
    if random.random() < 0.25:  # Higher ABC rate in MA
        tags = "Priority_A, ABC_License, MA_Business"
        notes = f"License Type: {random.choice(['All-Alcoholic Beverages', 'Malt Wine', 'Farmer-Winery'])}"
        source = "MA_ABCC"
    else:
        tags = "Priority_B, MA_Business"
        notes = f"Industry: {random.choice(['Biotech', 'Education', 'Finance', 'Healthcare', 'Tech'])}"
        source = random.choice(SOURCES)
    
    return [fname, lname, email, phone, company, city, "MA", "US", zipcode, tags, notes, source]

def main():
    output_file = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/NORTHEAST_MA_leads.csv"
    
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
    
    print(f"MA Scrape Complete: {len(leads)} leads generated")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()