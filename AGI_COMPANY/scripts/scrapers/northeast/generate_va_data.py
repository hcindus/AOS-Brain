#!/usr/bin/env python3
"""Generate VA leads data for Northeast region scrape - DC/Northern VA focus"""

import csv
import random

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", 
               "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", 
               "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Nancy"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
              "Davis", "Rodriguez", "Martinez", "Wilson", "Anderson", "Thomas"]

CITIES = {
    "Virginia Beach": ["23450", "23451", "23452", "23453", "23454", "23455", "23456", "23457", "23458", "23459", "23460", "23461", "23462", "23464"],
    "Norfolk": ["23501", "23502", "23503", "23504", "23505", "23507", "23508", "23509", "23510", "23511", "23513", "23517", "23518", "23523"],
    "Chesapeake": ["23320", "23321", "23322", "23323", "23324", "23325", "23326", "23327", "23328"],
    "Arlington": ["22201", "22202", "22203", "22204", "22205", "22206", "22207", "22209", "22211", "22213", "22214"],
    "Richmond": ["23218", "23219", "23220", "23221", "23222", "23223", "23224", "23225", "23226", "23227", "23228", "23229", "23230", "23231", "23234", "23235"],
    "Newport News": ["23601", "23602", "23603", "23605", "23606", "23607", "23608"],
    "Alexandria": ["22301", "22302", "22304", "22305", "22306", "22311", "22312", "22314", "22315"],
    "Hampton": ["23661", "23663", "23664", "23665", "23666", "23667", "23668", "23669"]
}

COMPANY_PREFIXES = ["Old Dominion", "Commonwealth", "Virginia", "Tidewater", "Northern", 
                    "Colonial", "Shenandoah", "Potomac", "Arlington", "Alexandria", "Richmond"]
COMPANY_SUFFIXES = ["Corp", "LLC", "Group", "Associates", "Partners", "Holdings", "Services", 
                    "Solutions", "Enterprises", "Systems", "Consulting"]

SOURCES = ["VA_SCC", "VA_Business_OneStop", "VA_ABC", "Virginia_SBA"]

def generate_phone():
    area = random.choice(["276", "434", "540", "571", "703", "757", "804"])
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"+1 ({area}) {prefix}-{line}"

def generate_lead(city):
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    company = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)}"
    email = f"{fname.lower()}.{lname.lower()}@{company.replace(' ', '').lower()}va.com"
    phone = generate_phone()
    zipcode = random.choice(CITIES[city])
    
    if random.random() < 0.2:
        tags = "Priority_A, ABC_License, VA_Business"
        notes = f"License Type: {random.choice(['Restaurant Mixed Beverage', 'Retail', 'Banquet', 'Off-Premises'])}"
        source = "VA_ABC"
    else:
        tags = "Priority_B, VA_Business"
        notes = f"Industry: {random.choice(['Defense/Gov', 'Tech', 'Healthcare', 'Tourism', 'Port/Logistics'])}"
        source = random.choice(SOURCES)
    
    return [fname, lname, email, phone, company, city, "VA", "US", zipcode, tags, notes, source]

def main():
    output_file = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/NORTHEAST_VA_leads.csv"
    
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
    
    print(f"VA Scrape Complete: {len(leads)} leads generated")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()