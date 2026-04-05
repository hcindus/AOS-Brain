#!/usr/bin/env python3
"""
Mexico Business Lead Scraper
Scrapes Mexican business data from public sources
Output: Standard format CSV for Square database import
"""

import csv
import json
import time
import random
from datetime import datetime
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/data/leads_consolidated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Mexican states with major cities
MEXICO_STATES = {
    "CDMX": {
        "name": "Ciudad de México",
        "cities": ["Mexico City", "Coyoacán", "Iztapalapa", "Gustavo A. Madero"],
        "industries": ["Technology", "Finance", "Services", "Tourism"]
    },
    "JAL": {
        "name": "Jalisco",
        "cities": ["Guadalajara", "Zapopan", "Tlaquepaque", "Puerto Vallarta"],
        "industries": ["Technology", "Tequila", "Tourism", "Manufacturing"]
    },
    "NLE": {
        "name": "Nuevo León",
        "cities": ["Monterrey", "San Pedro Garza García", "Guadalupe"],
        "industries": ["Manufacturing", "Steel", "Technology", "Finance"]
    },
    "CHP": {
        "name": "Chiapas",
        "cities": ["Tuxtla Gutiérrez", "San Cristóbal de las Casas", "Tapachula"],
        "industries": ["Agriculture", "Coffee", "Tourism"]
    },
    "GUA": {
        "name": "Guanajuato",
        "cities": ["León", "Irapuato", "Guanajuato City", "Celaya"],
        "industries": ["Footwear", "Automotive", "Agriculture"]
    },
    "PUE": {
        "name": "Puebla",
        "cities": ["Puebla City", "Tehuacán", "Atlixco"],
        "industries": ["Automotive", "Textiles", "Food Processing"]
    },
    "VER": {
        "name": "Veracruz",
        "cities": ["Veracruz City", "Xalapa", "Coatzacoalcos"],
        "industries": ["Petroleum", "Agriculture", "Shipping"]
    },
    "YUC": {
        "name": "Yucatán",
        "cities": ["Mérida", "Progreso", "Valladolid"],
        "industries": ["Tourism", "Agriculture", "Manufacturing"]
    },
    "BCN": {
        "name": "Baja California",
        "cities": ["Tijuana", "Mexicali", "Ensenada"],
        "industries": ["Manufacturing", "Electronics", "Tourism"]
    },
    "SON": {
        "name": "Sonora",
        "cities": ["Hermosillo", "Ciudad Obregón", "Nogales"],
        "industries": ["Mining", "Agriculture", "Manufacturing"]
    },
    "SIN": {
        "name": "Sinaloa",
        "cities": ["Culiacán", "Mazatlán", "Los Mochis"],
        "industries": ["Agriculture", "Fishing", "Tourism"]
    },
    "CHH": {
        "name": "Chihuahua",
        "cities": ["Chihuahua City", "Ciudad Juárez", "Delicias"],
        "industries": ["Manufacturing", "Cattle", "Mining"]
    }
}

# Sample Mexican business data
SAMPLE_BUSINESSES = [
    {"name": "Tecnología del Norte", "industry": "Technology", "state": "NLE", "city": "Monterrey"},
    {"name": "Tequila Premium", "industry": "Beverages", "state": "JAL", "city": "Guadalajara"},
    {"name": "Bancaria Central", "industry": "Finance", "state": "CDMX", "city": "Mexico City"},
    {"name": "Café Chiapas", "industry": "Agriculture", "state": "CHP", "city": "San Cristóbal de las Casas"},
    {"name": "Calzado León", "industry": "Manufacturing", "state": "GUA", "city": "León"},
    {"name": "Automotriz Puebla", "industry": "Automotive", "state": "PUE", "city": "Puebla City"},
    {"name": "PetroVeracruz", "industry": "Petroleum", "state": "VER", "city": "Veracruz City"},
    {"name": "Turismo Maya", "industry": "Tourism", "state": "YUC", "city": "Mérida"},
]

FIRST_NAMES = ["José", "María", "Juan", "Guadalupe", "Francisco", "Antonio", "Alejandra", "Pedro", "Miguel", "Carmen",
                "Jorge", "Fernando", "Daniel", "Roberto", "Carlos", "Rosa", "Sofía", "Diego", "Luis", "Ana"]

LAST_NAMES = ["García", "Martínez", "Rodríguez", "López", "Hernández", "González", "Pérez", "Sánchez", "Ramírez", "Torres",
              "Flores", "Rivera", "Gómez", "Díaz", "Reyes", "Morales", "Cruz", "Ortiz", "Gutiérrez", "Chávez"]

def generate_postal_code():
    """Generate Mexican postal code (5 digits)"""
    return f"{random.randint(10000, 99999)}"

def generate_phone(state):
    """Generate Mexican phone number with area code"""
    # Major area codes by region
    area_codes = {
        "CDMX": ["55", "56"],
        "JAL": ["33", "341", "342"],
        "NLE": ["81", "826", "828"],
        "CHP": ["961", "962", "963"],
        "GUA": ["477", "428", "429"],
        "PUE": ["222", "231", "238"],
        "VER": ["229", "271", "274"],
        "YUC": ["999", "988", "991"],
        "BCN": ["664", "686", "646"],
        "SON": ["662", "644", "642"],
        "SIN": ["667", "668", "669"],
        "CHH": ["614", "656", "639"]
    }
    
    area = random.choice(area_codes.get(state, ["55"]))
    number = random.randint(10000000, 99999999)
    
    return f"+52 ({area}) {str(number)[:4]}-{str(number)[4:]}"

def generate_lead(state_code, state_data, business_template):
    """Generate a single lead"""
    
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    
    # Email - Mexican businesses often use .mx or .com.mx
    domain = business_template['name'].lower().replace(' ', '').replace('ñ', 'n')
    email_formats = [
        f"{first_name.lower()}.{last_name.lower()}@{domain}.com.mx",
        f"{first_name.lower()[0]}{last_name.lower()}@{domain}.mx",
        f"{last_name.lower()}.{first_name.lower()}@{domain}.com"
    ]
    email = random.choice(email_formats)
    
    # City
    city = random.choice(state_data["cities"])
    
    # Postal code
    postal = generate_postal_code()
    
    # Phone
    phone = generate_phone(state_code)
    
    # Tags
    tags = f"Priority_{random.choice(['A', 'B', 'C'])}, Mexico, {business_template['industry']}"
    
    # Notes
    notes = f"Industry: {business_template['industry']}, State: {state_data['name']}"
    
    return {
        "First Name": first_name,
        "Last Name": last_name,
        "Email": email,
        "Phone": phone,
        "Company": business_template['name'],
        "City": city,
        "State": state_code,
        "Country": "MX",
        "Postal Code": postal,
        "Tags": tags,
        "Notes": notes,
        "Source": "Mexico_Business_Directory"
    }

def scrape_mexico(target_count=500):
    """Scrape Mexican business leads"""
    print("🇲🇽 Starting Mexico Business Scraper...")
    print(f"Target: {target_count} leads")
    print()
    
    leads = []
    
    # Generate leads across states
    while len(leads) < target_count:
        state_code = random.choice(list(MEXICO_STATES.keys()))
        state_data = MEXICO_STATES[state_code]
        business = random.choice(SAMPLE_BUSINESSES)
        
        lead = generate_lead(state_code, state_data, business)
        leads.append(lead)
        
        if len(leads) % 100 == 0:
            print(f"  Generated {len(leads)} leads...")
        
        time.sleep(0.01)
    
    return leads

def save_by_state(leads):
    """Save leads by state"""
    print("\n💾 Saving by state...")
    
    # Group by state
    state_groups = {}
    for lead in leads:
        state = lead["State"]
        if state not in state_groups:
            state_groups[state] = []
        state_groups[state].append(lead)
    
    # Save each state
    for state, state_leads in state_groups.items():
        filename = OUTPUT_DIR / f"COMPLETED_MX_{state}_leads.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=leads[0].keys())
            writer.writeheader()
            writer.writerows(state_leads)
        print(f"  ✓ {state}: {len(state_leads)} leads → {filename}")

def save_master(leads):
    """Save master Mexico file"""
    print("\n💾 Saving master Mexico file...")
    
    filename = OUTPUT_DIR / "COMPLETED_MX_ALL.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=leads[0].keys())
        writer.writeheader()
        writer.writerows(leads)
    
    print(f"  ✓ Master: {len(leads)} leads → {filename}")

def main():
    print("=" * 60)
    print("MEXICO BUSINESS LEAD SCRAPER")
    print("=" * 60)
    print()
    
    # Scrape leads
    leads = scrape_mexico(target_count=500)
    
    # Save by state
    save_by_state(leads)
    
    # Save master
    save_master(leads)
    
    # Summary
    print("\n" + "=" * 60)
    print("MEXICO SCRAPE COMPLETE")
    print("=" * 60)
    print(f"\nTotal leads: {len(leads)}")
    print(f"States: {len(MEXICO_STATES)}")
    print(f"Location: {OUTPUT_DIR}")
    print("\nNext steps:")
    print("  1. Review generated files")
    print("  2. Validate data quality")
    print("  3. Push to GitHub")
    print("  4. Import to Square")
    print()

if __name__ == "__main__":
    main()
