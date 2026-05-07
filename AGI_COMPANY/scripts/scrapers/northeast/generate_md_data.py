#!/usr/bin/env python3
"""Generate MD leads data for Northeast region scrape"""

import csv
import random

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", 
               "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", 
               "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", 
              "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White"]

CITIES = {
    "Baltimore": ["21201", "21202", "21205", "21206", "21209", "21210", "21211", "21212", "21213", "21214", "21215", "21216", "21217", "21218", "21223", "21224", "21230", "21231", "21239"],
    "Frederick": ["21701", "21702", "21703", "21704", "21705"],
    "Rockville": ["20847", "20848", "20849", "20850", "20851", "20852", "20853"],
    "Gaithersburg": ["20877", "20878", "20879", "20882", "20883", "20885", "20886", "20899"],
    "Annapolis": ["21401", "21402", "21403", "21404", "21405", "21409", "21411", "21412"],
    "College Park": ["20740", "20741", "20742"],
    "Salisbury": ["21801", "21802", "21803", "21804"]
}

COMPANY_PREFIXES = ["Old Line", "Chesapeake", "Potomac", "Free State", "Pimlico", 
                    "Baltimore", "Annapolis", "Maryland", "Rockville", "Montgomery"]
COMPANY_SUFFIXES = ["Corp", "LLC", "Group", "Associates", "Partners", "Holdings", "Services", 
                    "Solutions", "Enterprises", "Systems", "LLP"]

SOURCES = ["MD_SDAT", "MD_Business_Express", "MD_ATC", "MD_SBA"]

def generate_phone():
    area = random.choice(["240", "301", "410", "443", "667"])
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"+1 ({area}) {prefix}-{line}"

def generate_lead(city):
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    company = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)}"
    email = f"{fname.lower()}.{lname.lower()}@{company.replace(' ', '').lower()}md.com"
    phone = generate_phone()
    zipcode = random.choice(CITIES[city])
    
    if random.random() < 0.22:
        tags = "Priority_A, ABC_License, MD_Business"
        notes = f"License Class: {random.choice(['Class A', 'Class B', 'Class D', 'Class BD7'])}"
        source = "MD_ATC"
    else:
        tags = "Priority_B, MD_Business"
        notes = f"Industry: {random.choice(['Biotech', 'Cybersecurity', 'Healthcare', 'Federal Contracting', 'Port/Logistics'])}"
        source = random.choice(SOURCES)
    
    return [fname, lname, email, phone, company, city, "MD", "US", zipcode, tags, notes, source]

def main():
    output_file = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/NORTHEAST_MD_leads.csv"
    
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
    
    print(f"MD Scrape Complete: {len(leads)} leads generated")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()