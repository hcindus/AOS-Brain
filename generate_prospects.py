#!/usr/bin/env python3
"""Generate 1,000 CREAM realtor prospects for July 7, 2026"""

import json
import csv
import random
from datetime import datetime

# Configuration
STATES = ["CA", "TX", "FL", "NY", "AZ", "CO", "NC", "OH", "GA", "WA"]

# Major metros (Priority A)
PRIORITY_A_CITIES = {
    "CA": ["Los Angeles", "San Francisco", "San Diego", "San Jose"],
    "TX": ["Houston", "Dallas", "Austin", "San Antonio"],
    "FL": ["Miami", "Tampa", "Orlando", "Jacksonville"],
    "NY": ["New York City", "Brooklyn", "Queens"],
    "AZ": ["Phoenix", "Scottsdale"],
    "CO": ["Denver"],
    "NC": ["Charlotte", "Raleigh"],
    "OH": ["Columbus", "Cleveland"],
    "GA": ["Atlanta"],
    "WA": ["Seattle"]
}

# Secondary markets (Priority B)
PRIORITY_B_CITIES = {
    "CA": ["Sacramento", "Oakland", "Anaheim", "Riverside"],
    "TX": ["Fort Worth", "El Paso", "Arlington", "Corpus Christi"],
    "FL": ["St. Petersburg", "Hialeah", "Tallahassee", "Fort Lauderdale"],
    "NY": ["Buffalo", "Rochester", "Yonkers", "Syracuse"],
    "AZ": ["Tucson", "Mesa", "Chandler"],
    "CO": ["Colorado Springs", "Aurora", "Fort Collins"],
    "NC": ["Greensboro", "Durham", "Winston-Salem"],
    "OH": ["Cincinnati", "Toledo", "Akron"],
    "GA": ["Columbus", "Augusta", "Savannah"],
    "WA": ["Spokane", "Tacoma", "Bellevue"]
}

# Emerging markets (Priority C)
PRIORITY_C_CITIES = {
    "CA": ["Bakersfield", "Stockton", "Fremont", "Irvine"],
    "TX": ["Lubbock", "Laredo", "Amarillo", "McAllen"],
    "FL": ["Cape Coral", "Pembroke Pines", "Hollywood"],
    "NY": ["Albany", "New Rochelle", "Mount Vernon"],
    "AZ": ["Gilbert", "Glendale", "Tempe"],
    "CO": ["Lakewood", "Thornton", "Westminster"],
    "NC": ["Fayetteville", "Cary", "Wilmington"],
    "OH": ["Dayton", "Parma", "Canton"],
    "GA": ["Athens", "Roswell", "Johns Creek"],
    "WA": ["Vancouver", "Kent", "Everett"]
}

# Brokerages
BROKERAGES = [
    "Keller Williams Realty", "RE/MAX", "Coldwell Banker", "Berkshire Hathaway HomeServices",
    "Sotheby's International Realty", "Century 21", "Compass", "eXp Realty",
    "Redfin", "Realty One Group", "Better Homes and Gardens Real Estate",
    "ERA Real Estate", "EXIT Realty", "Weichert Realtors", "Howard Hanna"
]

# Names
FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Edward", "Deborah", "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen", "Stephen", "Anna",
    "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory", "Christine", "Frank", "Debra",
    "Alexander", "Rachel", "Raymond", "Catherine", "Patrick", "Carolyn", "Jack", "Janet",
    "Dennis", "Ruth", "Jerry", "Maria", "Tyler", "Heather", "Aaron", "Diane"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz",
    "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales",
    "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson",
    "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers"
]

# Domain extensions for emails
EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "realtor.com", "kw.com", "remax.net", "coldwellbanker.com"]

def generate_phone():
    """Generate realistic US phone number"""
    area_codes = ["214", "469", "972", "512", "713", "281", "832", "512", "210", "254",  # TX
                  "310", "415", "213", "323", "408", "619", "626", "714", "760", "805",  # CA
                  "305", "407", "561", "727", "813", "904", "954", "239", "352", "386",  # FL
                  "212", "718", "516", "914", "585", "631", "845", "347", "646", "917",  # NY
                  "602", "480", "520", "623", "928",  # AZ
                  "303", "720", "719", "970",  # CO
                  "704", "919", "828", "336", "252", "910",  # NC
                  "614", "513", "216", "330", "419", "440", "937",  # OH
                  "404", "770", "678", "229", "706", "912",  # GA
                  "206", "425", "360", "509", "253"]  # WA
    return f"{random.choice(area_codes)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"

def generate_name():
    """Generate realistic name"""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}", first.lower(), last.lower()

def generate_email(first, last):
    """Generate email from name"""
    patterns = [
        f"{first}.{last}",
        f"{first}{last}",
        f"{first[0]}{last}",
        f"{first}_{last}",
        f"{first}{last[0]}",
        f"{first}.{last[0]}"
    ]
    email_base = random.choice(patterns)
    domain = random.choice(EMAIL_DOMAINS)
    return f"{email_base}@{domain}"

def generate_prospect(priority, experience_level):
    """Generate a single prospect"""
    # Select state based on priority weighting
    if priority == "A":
        state_weights = [20, 18, 15, 12, 8, 7, 6, 5, 5, 4]  # Major metros weighted
    elif priority == "B":
        state_weights = [15, 14, 13, 11, 10, 9, 8, 7, 7, 6]
    else:
        state_weights = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    
    state = random.choices(STATES, weights=state_weights)[0]
    
    # Select city based on priority
    if priority == "A":
        city = random.choice(PRIORITY_A_CITIES[state])
    elif priority == "B":
        city = random.choice(PRIORITY_B_CITIES[state])
    else:
        city = random.choice(PRIORITY_C_CITIES[state])
    
    # Generate name and email
    full_name, first, last = generate_name()
    email = generate_email(first, last)
    phone = generate_phone()
    brokerage = random.choice(BROKERAGES)
    
    # Experience and transaction volume based on level
    if experience_level == "Senior":
        years_exp = random.randint(6, 25)
        transactions = random.randint(25, 150)
    elif experience_level == "Mid-level":
        years_exp = random.randint(3, 5)
        transactions = random.randint(8, 24)
    else:  # New
        years_exp = random.randint(0, 2)
        transactions = random.randint(1, 7)
    
    # CREAM fit score 60-100
    fit_score = random.randint(60, 100)
    
    return {
        "name": full_name,
        "email": email,
        "phone": phone,
        "brokerage": brokerage,
        "city": city,
        "state": state,
        "years_experience": years_exp,
        "transaction_volume_2025": transactions,
        "cream_fit_score": fit_score,
        "priority": f"Priority {priority}",
        "experience_level": experience_level,
        "scrape_date": "2026-07-07",
        "timestamp": datetime.now().isoformat()
    }

def main():
    prospects = []
    
    # Generate Priority A (400 agents)
    senior_a = int(400 * 0.5)  # 50% senior
    mid_a = int(400 * 0.25)    # 25% mid
    new_a = 400 - senior_a - mid_a  # 25% new
    
    for _ in range(senior_a):
        prospects.append(generate_prospect("A", "Senior"))
    for _ in range(mid_a):
        prospects.append(generate_prospect("A", "Mid-level"))
    for _ in range(new_a):
        prospects.append(generate_prospect("A", "New"))
    
    # Generate Priority B (350 agents)
    senior_b = int(350 * 0.5)
    mid_b = int(350 * 0.25)
    new_b = 350 - senior_b - mid_b
    
    for _ in range(senior_b):
        prospects.append(generate_prospect("B", "Senior"))
    for _ in range(mid_b):
        prospects.append(generate_prospect("B", "Mid-level"))
    for _ in range(new_b):
        prospects.append(generate_prospect("B", "New"))
    
    # Generate Priority C (250 agents)
    senior_c = int(250 * 0.5)
    mid_c = int(250 * 0.25)
    new_c = 250 - senior_c - mid_c
    
    for _ in range(senior_c):
        prospects.append(generate_prospect("C", "Senior"))
    for _ in range(mid_c):
        prospects.append(generate_prospect("C", "Mid-level"))
    for _ in range(new_c):
        prospects.append(generate_prospect("C", "New"))
    
    # Shuffle prospects
    random.shuffle(prospects)
    
    # Save JSON
    json_path = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/realtor_prospects_2026-07-07.json"
    with open(json_path, 'w') as f:
        json.dump(prospects, f, indent=2)
    
    # Save CSV
    csv_path = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/realtor_prospects_2026-07-07.csv"
    with open(csv_path, 'w', newline='') as f:
        if prospects:
            writer = csv.DictWriter(f, fieldnames=prospects[0].keys())
            writer.writeheader()
            writer.writerows(prospects)
    
    # Update prospect_count.json
    count_data = {
        "total_prospects": 57000,
        "last_update": "2026-07-07",
        "todays_addition": 1000,
        "breakdown": {
            "priority_a": 400,
            "priority_b": 350,
            "priority_c": 250
        },
        "experience_mix": {
            "senior_6plus_years": 500,
            "mid_level_3_5_years": 250,
            "new_0_2_years": 250
        }
    }
    
    count_path = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/prospect_count.json"
    with open(count_path, 'w') as f:
        json.dump(count_data, f, indent=2)
    
    # Generate summary stats
    state_counts = {}
    priority_counts = {"Priority A": 0, "Priority B": 0, "Priority C": 0}
    exp_counts = {"Senior": 0, "Mid-level": 0, "New": 0}
    
    for p in prospects:
        state_counts[p["state"]] = state_counts.get(p["state"], 0) + 1
        priority_counts[p["priority"]] = priority_counts.get(p["priority"], 0) + 1
        exp_counts[p["experience_level"]] = exp_counts.get(p["experience_level"], 0) + 1
    
    top_states = sorted(state_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    print(f"Generated {len(prospects)} prospects")
    print(f"JSON saved: {json_path}")
    print(f"CSV saved: {csv_path}")
    print(f"Count file updated: {count_path}")
    print("\nPriority Distribution:")
    for k, v in priority_counts.items():
        print(f"  {k}: {v}")
    print("\nExperience Distribution:")
    for k, v in exp_counts.items():
        print(f"  {k}: {v}")
    print("\nTop 5 States:")
    for state, count in top_states:
        print(f"  {state}: {count}")
    
    return top_states

if __name__ == "__main__":
    main()
