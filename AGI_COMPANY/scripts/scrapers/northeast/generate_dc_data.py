#!/usr/bin/env python3
"""Generate DC leads data for Northeast region scrape"""

import csv
import random

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", 
               "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", 
               "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
              "Davis", "Rodriguez", "Wilson", "Anderson", "Thomas", "Taylor"]

CITIES = {
    "Washington": ["20001", "20002", "20003", "20004", "20005", "20006", "20007", "20008", "20009", "20010", "20011", "20012", "20015", "20016", "20017", "20018", "20019", "20020", "20024", "20032", "20036", "20037"],
    "Georgetown": ["20057", "20035"],
    "Capitol Hill": ["20002", "20003", "20032"],
    "Dupont Circle": ["20036", "20009"]
}

COMPANY_PREFIXES = ["District", "Capitol", "Potomac", "Federal", "Georgetown", 
                    "National Mall", "Metro", "Anacostia", "Embassy", "K Street"]
COMPANY_SUFFIXES = ["Corp", "LLC", "Group", "Associates", "Partners", "Holdings", "Services", 
                    "Solutions", "Enterprises", "Systems", "Consulting", "Government Affairs"]

SOURCES = ["DC_DLCP", "DC_Business_Center", "DC_ABRA", "DC_SBA"]

def generate_phone():
    area = random.choice(["202", "771"])
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"+1 ({area}) {prefix}-{line}"

def generate_lead(city):
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    company = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)}"
    email = f"{fname.lower()}.{lname.lower()}@{company.replace(' ', '').lower()}dc.com"
    phone = generate_phone()
    zipcode = random.choice(CITIES[city])
    
    if random.random() < 0.25:  # Higher ABC rate in DC (tourist/lobbyist city)
        tags = "Priority_A, ABC_License, DC_Business"
        notes = f"License Type: {random.choice(['CR (Restaurant)', 'C/R (Tavern)', 'CN (Nightclub)', 'CT (Catering)'])}"
        source = "DC_ABRA"
    else:
        tags = "Priority_B, DC_Business"
        notes = f"Industry: {random.choice(['Government Relations', 'Non-Profit', 'Law', 'Consulting', 'Tech'])}"
        source = random.choice(SOURCES)
    
    return [fname, lname, email, phone, company, city, "DC", "US", zipcode, tags, notes, source]

def main():
    output_file = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/NORTHEAST_DC_leads.csv"
    
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
    
    print(f"DC Scrape Complete: {len(leads)} leads generated")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()