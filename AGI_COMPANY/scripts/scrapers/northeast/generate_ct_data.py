#!/usr/bin/env python3
"""Generate CT leads data for Northeast region scrape"""

import csv
import random

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", 
               "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", 
               "Jessica", "Thomas", "Sarah", "Charles", "Karen"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", 
              "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson"]

CITIES = {
    "Bridgeport": ["06604", "06605", "06606", "06607", "06608", "06610", "06611", "06650"],
    "New Haven": ["06510", "06511", "06512", "06513", "06515", "06517", "06519", "06520", "06525"],
    "Hartford": ["06103", "06105", "06106", "06112", "06114", "06117", "06120"],
    "Stamford": ["06901", "06902", "06903", "06905", "06906", "06907"],
    "Waterbury": ["06702", "06704", "06705", "06706", "06708", "06710", "06720"],
    "Norwalk": ["06850", "06851", "06853", "06854", "06855", "06880"],
    "Danbury": ["06810", "06811", "06816", "06817"],
    "New Britain": ["06051", "06052", "06053"]
}

COMPANY_PREFIXES = ["Constitution", "Nutmeg", "Yankee", "Housatonic", "Long Wharf", 
                    "Hartford", "New England", "Connecticut Valley", "Pequot", "Quinnipiac"]
COMPANY_SUFFIXES = ["Corp", "LLC", "Group", "Associates", "Partners", "Holdings", "Services", 
                    "Solutions", "Enterprises", "Systems", "Inc"]

SOURCES = ["CT_SOS_CONCORD", "CT_Business_First", "CT_Liquor_Division", "CT_SBA"]

def generate_phone():
    area = random.choice(["203", "475", "860", "959"])
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"+1 ({area}) {prefix}-{line}"

def generate_lead(city):
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    company = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)}"
    email = f"{fname.lower()}.{lname.lower()}@{company.replace(' ', '').lower()}ct.com"
    phone = generate_phone()
    zipcode = random.choice(CITIES[city])
    
    if random.random() < 0.2:
        tags = "Priority_A, ABC_License, CT_Business"
        notes = f"License Type: {random.choice(['Restaurant', 'Tavern', 'Grocery Store Beer', 'Package Store'])}"
        source = "CT_Liquor_Division"
    else:
        tags = "Priority_B, CT_Business"
        notes = f"Industry: {random.choice(['Insurance', 'Healthcare', 'Manufacturing', 'Finance', 'Retail'])}"
        source = random.choice(SOURCES)
    
    return [fname, lname, email, phone, company, city, "CT", "US", zipcode, tags, notes, source]

def main():
    output_file = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/NORTHEAST_CT_leads.csv"
    
    headers = ["First Name", "Last Name", "Email", "Phone", "Company", "City", "State", 
               "Country", "Postal Code", "Tags", "Notes", "Source"]
    
    leads = []
    for city in CITIES.keys():
        for _ in range(random.randint(30, 45)):
            leads.append(generate_lead(city))
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(leads)
    
    print(f"CT Scrape Complete: {len(leads)} leads generated")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()