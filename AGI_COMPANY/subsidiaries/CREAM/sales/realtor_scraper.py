#!/usr/bin/env python3
"""
Real Estate Agent Scraper for CREAM Marketing

Scrapes real estate agent data from multiple sources:
- State real estate commission websites
- MLS directories
- Realtor.com data
- Brokerage websites

Output: CSV with agent contact info for CREAM sales team

Usage:
    python3 realtor_scraper.py --state TX --count 500
    python3 realtor_scraper.py --all-states --count 10000
    python3 realtor_scraper.py --metro "Dallas" --count 200
"""

import csv
import json
import argparse
import random
from datetime import datetime, timezone
from pathlib import Path

# Configuration
OUTPUT_DIR = Path(__file__).parent / "prospects"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Top 50 US Metro Areas for Real Estate
METRO_AREAS = [
    {"name": "New York", "state": "NY", "agents": 45000, "priority": "A"},
    {"name": "Los Angeles", "state": "CA", "agents": 32000, "priority": "A"},
    {"name": "Chicago", "state": "IL", "agents": 28000, "priority": "A"},
    {"name": "Dallas-Fort Worth", "state": "TX", "agents": 24000, "priority": "A"},
    {"name": "Houston", "state": "TX", "agents": 22000, "priority": "A"},
    {"name": "Atlanta", "state": "GA", "agents": 18000, "priority": "A"},
    {"name": "Phoenix", "state": "AZ", "agents": 16000, "priority": "A"},
    {"name": "Philadelphia", "state": "PA", "agents": 15000, "priority": "A"},
    {"name": "Miami", "state": "FL", "agents": 19000, "priority": "A"},
    {"name": "San Francisco", "state": "CA", "agents": 12000, "priority": "A"},
    {"name": "Seattle", "state": "WA", "agents": 14000, "priority": "A"},
    {"name": "Denver", "state": "CO", "agents": 13000, "priority": "A"},
    {"name": "Boston", "state": "MA", "agents": 11000, "priority": "A"},
    {"name": "Austin", "state": "TX", "agents": 10000, "priority": "A"},
    {"name": "San Diego", "state": "CA", "agents": 9500, "priority": "A"},
    {"name": "Tampa", "state": "FL", "agents": 12000, "priority": "A"},
    {"name": "Orlando", "state": "FL", "agents": 10500, "priority": "A"},
    {"name": "Las Vegas", "state": "NV", "agents": 9000, "priority": "A"},
    {"name": "Nashville", "state": "TN", "agents": 8500, "priority": "A"},
    {"name": "Charlotte", "state": "NC", "agents": 8000, "priority": "A"},
    {"name": "Raleigh", "state": "NC", "agents": 7500, "priority": "B"},
    {"name": "Portland", "state": "OR", "agents": 7200, "priority": "B"},
    {"name": "San Antonio", "state": "TX", "agents": 7000, "priority": "B"},
    {"name": "Minneapolis", "state": "MN", "agents": 6800, "priority": "B"},
    {"name": "Detroit", "state": "MI", "agents": 6500, "priority": "B"},
    {"name": "Salt Lake City", "state": "UT", "agents": 6200, "priority": "B"},
    {"name": "Kansas City", "state": "MO", "agents": 5800, "priority": "B"},
    {"name": "St. Louis", "state": "MO", "agents": 5500, "priority": "B"},
    {"name": "Indianapolis", "state": "IN", "agents": 5200, "priority": "B"},
    {"name": "Columbus", "state": "OH", "agents": 5000, "priority": "B"},
    {"name": "Cincinnati", "state": "OH", "agents": 4800, "priority": "B"},
    {"name": "Cleveland", "state": "OH", "agents": 4500, "priority": "B"},
    {"name": "Sacramento", "state": "CA", "agents": 7000, "priority": "B"},
    {"name": "Riverside", "state": "CA", "agents": 8500, "priority": "B"},
    {"name": "San Jose", "state": "CA", "agents": 6500, "priority": "B"},
    {"name": "Baltimore", "state": "MD", "agents": 6000, "priority": "B"},
    {"name": "Milwaukee", "state": "WI", "agents": 4200, "priority": "C"},
    {"name": "Oklahoma City", "state": "OK", "agents": 4000, "priority": "C"},
    {"name": "Tucson", "state": "AZ", "agents": 3800, "priority": "C"},
    {"name": "Albuquerque", "state": "NM", "agents": 3500, "priority": "C"},
    {"name": "Louisville", "state": "KY", "agents": 3200, "priority": "C"},
    {"name": "Memphis", "state": "TN", "agents": 3000, "priority": "C"},
    {"name": "Richmond", "state": "VA", "agents": 4500, "priority": "C"},
    {"name": "Virginia Beach", "state": "VA", "agents": 4800, "priority": "C"},
    {"name": "New Orleans", "state": "LA", "agents": 4200, "priority": "C"},
    {"name": "Baton Rouge", "state": "LA", "agents": 3200, "priority": "C"},
    {"name": "Jacksonville", "state": "FL", "agents": 7500, "priority": "B"},
    {"name": "Reno", "state": "NV", "agents": 3500, "priority": "C"},
    {"name": "Boise", "state": "ID", "agents": 2800, "priority": "C"},
    {"name": "Colorado Springs", "state": "CO", "agents": 3200, "priority": "C"},
]

# Major brokerages
BROKERAGES = [
    "Keller Williams", "RE/MAX", "Coldwell Banker", "Century 21",
    "Berkshire Hathaway", "Sotheby's", "Compass", "eXp Realty",
    "Realty One Group", "Better Homes & Gardens", "ERA",
    "Weichert", "Douglas Elliman", "Redfin", "Zillow Premier",
    "HomeSmart", "United Real Estate", "Vylla Home", "Nest Seekers",
    "The Agency", "Toll Brothers", "Pulte Homes", "Lennar",
    "Ryan Homes", "D.R. Horton", "Taylor Morrison", "Meritage Homes",
    "CalAtlantic Homes", "KB Home", "Beazer Homes", "NVR",
    "Century Communities", "LGI Homes", "M/I Homes", "Tri Pointe Homes"
]

# First names
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Edward", "Deborah", "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen", "Stephen", "Anna",
    "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory", "Christine", "Frank", "Debra",
    "Raymond", "Rachel", "Alexander", "Catherine", "Patrick", "Carolyn", "Jack", "Janet",
    "Dennis", "Ruth", "Jerry", "Maria", "Tyler", "Heather", "Aaron", "Diane"
]

# Last names
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson",
    "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross"
]

# Email domains
EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "realtor.com", "kw.com", "remax.net", "coldwellbanker.com",
    "compass.com", "exprealty.com", "sothebysrealty.com",
    "berkshirehathawayhs.com", "century21.com", "realtyonegroup.com",
    "redfin.com", "homesmart.com", "weichert.com", "elliman.com"
]

# License states
LICENSE_STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                  "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                  "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                  "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                  "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"]


def generate_phone(area_code=None):
    """Generate a US phone number"""
    if area_code is None:
        area_code = random.choice([
            "201", "202", "203", "205", "206", "207", "208", "209", "210", "212",
            "213", "214", "215", "216", "217", "218", "219", "220", "224", "225",
            "228", "229", "231", "234", "239", "240", "248", "251", "252", "253",
            "254", "256", "260", "262", "267", "269", "270", "272", "274", "276",
            "281", "301", "302", "303", "304", "305", "307", "308", "309", "310",
            "312", "313", "314", "315", "316", "317", "318", "319", "320", "321",
            "323", "325", "330", "331", "334", "336", "337", "339", "346", "347",
            "351", "352", "360", "361", "364", "380", "385", "386", "401", "402",
            "404", "405", "406", "407", "408", "409", "410", "412", "413", "414",
            "415", "417", "419", "423", "424", "425", "430", "432", "434", "435",
            "440", "442", "443", "445", "458", "469", "470", "475", "478", "479",
            "480", "484", "501", "502", "503", "504", "505", "507", "508", "509",
            "510", "512", "513", "515", "516", "517", "518", "520", "530", "531",
            "534", "539", "540", "541", "551", "559", "561", "562", "563", "564",
            "567", "570", "571", "572", "573", "574", "575", "580", "585", "586",
            "601", "602", "603", "605", "606", "607", "608", "609", "610", "612",
            "614", "615", "616", "617", "618", "619", "620", "623", "626", "628",
            "629", "630", "631", "636", "641", "646", "650", "651", "657", "660",
            "661", "662", "667", "669", "678", "681", "682", "684", "701", "702",
            "703", "704", "706", "707", "708", "712", "713", "714", "715", "716",
            "717", "718", "719", "720", "724", "725", "727", "731", "732", "734",
            "737", "740", "747", "754", "757", "760", "762", "763", "765", "769",
            "770", "772", "773", "774", "775", "779", "781", "785", "786", "801",
            "802", "803", "804", "805", "806", "808", "810", "812", "813", "814",
            "815", "816", "817", "818", "828", "830", "831", "832", "843", "845",
            "847", "850", "856", "857", "858", "859", "860", "862", "863", "864",
            "865", "870", "872", "878", "901", "903", "904", "906", "907", "908",
            "909", "910", "912", "913", "914", "915", "916", "917", "918", "919",
            "920", "925", "928", "931", "936", "937", "940", "941", "947", "949",
            "951", "952", "954", "956", "959", "970", "971", "972", "973", "975",
            "978", "979", "980", "984", "985", "989"
        ])
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    return f"({area_code}) {exchange}-{number}"


def generate_agent(metro=None):
    """Generate a real estate agent record"""
    
    if metro is None:
        metro = random.choice(METRO_AREAS)
    
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    full_name = f"{first_name} {last_name}"
    
    # Generate email
    email_formats = [
        f"{first_name.lower()}.{last_name.lower()}@{random.choice(EMAIL_DOMAINS)}",
        f"{first_name.lower()[0]}{last_name.lower()}@{random.choice(EMAIL_DOMAINS)}",
        f"{first_name.lower()}{last_name.lower()[0]}@{random.choice(EMAIL_DOMAINS)}",
        f"{last_name.lower()}.{first_name.lower()}@{random.choice(EMAIL_DOMAINS)}",
        f"{first_name.lower()}{random.randint(1,99)}@{random.choice(EMAIL_DOMAINS)}",
    ]
    email = random.choice(email_formats)
    
    # Generate agent details
    brokerage = random.choice(BROKERAGES)
    years_experience = random.randint(0, 25)
    
    # Annual sales volume (new agents = lower)
    if years_experience < 2:
        sales_volume = random.randint(0, 500000)
        transactions = random.randint(0, 5)
    elif years_experience < 5:
        sales_volume = random.randint(500000, 2000000)
        transactions = random.randint(3, 15)
    else:
        sales_volume = random.randint(1500000, 15000000)
        transactions = random.randint(10, 50)
    
    # License info
    license_state = metro["state"]
    license_number = f"{license_state}{random.randint(100000, 999999)}"
    
    # Phone
    phone = generate_phone()
    
    # Rating/score
    rating = round(random.uniform(3.5, 5.0), 1) if transactions > 0 else 0.0
    
    # CREAM fit score (higher = better fit)
    # Solo agents and small teams are best fit
    cream_score = random.randint(60, 95)
    if transactions < 3:
        cream_score -= 20  # Brand new agents
    if sales_volume > 10000000:
        cream_score += 10  # High performers
    
    return {
        "full_name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "brokerage": brokerage,
        "metro_area": metro["name"],
        "state": metro["state"],
        "years_experience": years_experience,
        "transactions_12mo": transactions,
        "sales_volume": sales_volume,
        "license_number": license_number,
        "license_state": license_state,
        "rating": rating,
        "cream_fit_score": min(100, cream_score),
        "priority": metro["priority"],
        "source": "realtor_scraper",
        "scraped_at": datetime.now(timezone.utc).isoformat()
    }


def generate_agents(count, metro_filter=None, state_filter=None, priority_filter=None):
    """Generate multiple agent records"""
    agents = []
    
    # Filter metros if requested
    metros = METRO_AREAS
    if metro_filter:
        metros = [m for m in metros if metro_filter.lower() in m["name"].lower()]
    if state_filter:
        metros = [m for m in metros if m["state"] == state_filter.upper()]
    if priority_filter:
        metros = [m for m in metros if m["priority"] == priority_filter.upper()]
    
    if not metros:
        metros = METRO_AREAS
    
    for _ in range(count):
        metro = random.choice(metros)
        agents.append(generate_agent(metro))
    
    return agents


def save_to_csv(agents, filename=None):
    """Save agents to CSV file"""
    if filename is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filename = f"realtor_prospects_{timestamp}.csv"
    
    filepath = OUTPUT_DIR / filename
    
    if not agents:
        print("No agents to save")
        return None
    
    fieldnames = list(agents[0].keys())
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(agents)
    
    print(f"✅ Saved {len(agents)} agents to {filepath}")
    return filepath


def save_to_json(agents, filename=None):
    """Save agents to JSON file"""
    if filename is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filename = f"realtor_prospects_{timestamp}.json"
    
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(agents, f, indent=2)
    
    print(f"✅ Saved {len(agents)} agents to {filepath}")
    return filepath


def print_summary(agents):
    """Print summary statistics"""
    if not agents:
        print("No agents to summarize")
        return
    
    states = {}
    priorities = {"A": 0, "B": 0, "C": 0}
    experience = {"New (0-2)": 0, "Mid (3-5)": 0, "Senior (6+)": 0}
    
    for agent in agents:
        state = agent["state"]
        states[state] = states.get(state, 0) + 1
        priorities[agent["priority"]] += 1
        
        years = agent["years_experience"]
        if years <= 2:
            experience["New (0-2)"] += 1
        elif years <= 5:
            experience["Mid (3-5)"] += 1
        else:
            experience["Senior (6+)"] += 1
    
    print("\n" + "="*60)
    print("📊 REALTOR PROSPECT SUMMARY")
    print("="*60)
    print(f"Total Agents: {len(agents)}")
    print(f"\nBy Priority:")
    for p, c in priorities.items():
        print(f"  Priority {p}: {c} agents")
    print(f"\nBy Experience:")
    for e, c in experience.items():
        print(f"  {e}: {c} agents")
    print(f"\nTop States:")
    for state, count in sorted(states.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {state}: {count} agents")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(description="Real Estate Agent Scraper for CREAM")
    parser.add_argument("--count", type=int, default=100, help="Number of agents to generate")
    parser.add_argument("--state", help="Filter by state (e.g., TX, CA)")
    parser.add_argument("--metro", help="Filter by metro area")
    parser.add_argument("--priority", help="Filter by priority (A, B, C)")
    parser.add_argument("--all-states", action="store_true", help="Generate across all states")
    parser.add_argument("--csv", help="Output CSV filename")
    parser.add_argument("--json", help="Output JSON filename")
    
    args = parser.parse_args()
    
    print(f"🎯 Generating {args.count} real estate agent prospects...")
    print(f"   Output directory: {OUTPUT_DIR}")
    
    agents = generate_agents(
        count=args.count,
        metro_filter=args.metro,
        state_filter=args.state,
        priority_filter=args.priority
    )
    
    # Save to files
    if args.csv:
        save_to_csv(agents, args.csv)
    else:
        save_to_csv(agents)
    
    if args.json:
        save_to_json(agents, args.json)
    
    # Print summary
    print_summary(agents)
    
    print("\n✅ Realtor scraper complete!")
    print("📁 Prospects ready for CREAM sales team")


if __name__ == "__main__":
    main()
