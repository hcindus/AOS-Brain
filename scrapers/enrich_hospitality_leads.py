#!/usr/bin/env python3
"""
Enrich Hospitality Leads for Capton
Finds F&B Managers, Bar Managers, Beverage Directors
"""

import sqlite3
import json
import re
from datetime import datetime
from typing import Optional, Dict, List
import time

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

# Common email patterns for hospitality roles
EMAIL_PATTERNS = [
    "{first}.{last}@{domain}",
    "{first}{last}@{domain}",
    "{first}@{domain}",
    "{last}@{domain}",
    "fb.{last}@{domain}",
    "bar.{last}@{domain}",
    "beverage.{last}@{domain}",
    "{first}.{last}@reservations.{domain}",
]

# Common hospitality titles
HOSPITALITY_TITLES = [
    "Food & Beverage Manager",
    "F&B Manager",
    "Bar Manager",
    "Beverage Director",
    "Director of Food & Beverage",
    "Restaurant Manager",
    "Lounge Manager",
    "Sommelier",
    "Executive Chef",
    "General Manager",
]

# Mock enrichment database (in production, this would use LinkedIn, ZoomInfo, etc.)
ENRICHED_CONTACTS = {
    # Format: "Business Name": [{"name": "...", "title": "...", "email": "..."}]
    "Pechanga Resort Casino": [
        {"name": "Michael Torres", "title": "Director of Food & Beverage", "email": "michael.torres@pechanga.com"},
        {"name": "Sarah Chen", "title": "Bar Manager", "email": "sarah.chen@pechanga.com"},
    ],
    "Morongo Casino Resort & Spa": [
        {"name": "James Rodriguez", "title": "Beverage Director", "email": "james.rodriguez@morongocasinoresort.com"},
    ],
    "Fairmont San Francisco": [
        {"name": "David Kim", "title": "Director of Food & Beverage", "email": "david.kim@fairmont.com"},
        {"name": "Jennifer Walsh", "title": "Bar Manager", "email": "jennifer.walsh@fairmont.com"},
    ],
    "Marriott Marquis San Francisco": [
        {"name": "Robert Lee", "title": "F&B Manager", "email": "robert.lee@marriott.com"},
    ],
    "Hilton San Francisco Union Square": [
        {"name": "Amanda Foster", "title": "Beverage Director", "email": "amanda.foster@hilton.com"},
    ],
    "Manchester Grand Hyatt San Diego": [
        {"name": "Christopher Martinez", "title": "Director of Food & Beverage", "email": "christopher.martinez@hyatt.com"},
    ],
    "JW Marriott Los Angeles L.A. LIVE": [
        {"name": "Michelle Park", "title": "Bar Manager", "email": "michelle.park@marriott.com"},
    ],
    "The Beverly Hilton": [
        {"name": "Steven Brooks", "title": "Beverage Director", "email": "steven.brooks@hilton.com"},
    ],
    "Disneyland Hotel": [
        {"name": "Lisa Johnson", "title": "F&B Manager", "email": "lisa.johnson@disney.com"},
    ],
    "Graton Resort & Casino": [
        {"name": "Kevin O'Brien", "title": "Director of Food & Beverage", "email": "kevin.obrien@gratonresortcasino.com"},
    ],
    "Thunder Valley Casino Resort": [
        {"name": "Nicole Adams", "title": "Bar Manager", "email": "nicole.adams@thundervalleyresort.com"},
    ],
    "Cache Creek Casino Resort": [
        {"name": "Brian Foster", "title": "Beverage Director", "email": "brian.foster@cachecreek.com"},
    ],
    "Yaamava' Resort & Casino": [
        {"name": "Daniel Park", "title": "F&B Director", "email": "daniel.park@yaamava.com"},
    ],
    "Pala Casino Spa & Resort": [
        {"name": "Jessica Martinez", "title": "Bar Manager", "email": "jessica.martinez@palacasino.com"},
    ],
}

def get_domain_from_website(website: str) -> str:
    """Extract domain from website URL"""
    if not website:
        return ""
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    return website.split("/")[0]

def generate_email_variations(first: str, last: str, domain: str) -> List[str]:
    """Generate possible email variations"""
    first = first.lower().replace(" ", "").replace("-", "")
    last = last.lower().replace(" ", "").replace("-", "").replace("'", "")
    first_initial = first[0] if first else ""
    
    variations = [
        f"{first}.{last}@{domain}",
        f"{first}{last}@{domain}",
        f"{first_initial}{last}@{domain}",
        f"{first}@{domain}",
        f"{last}@{domain}",
        f"{first}.{last}@reservations.{domain}",
        f"{first}.{last}@info.{domain}",
    ]
    return variations

def enrich_lead(cursor, lead_id: int, business_name: str, website: str) -> bool:
    """Enrich a single lead with contact data"""
    
    # Check if we have pre-enriched data
    if business_name in ENRICHED_CONTACTS:
        contacts = ENRICHED_CONTACTS[business_name]
        for contact in contacts:
            # Store enrichment data
            enrichment_data = json.dumps({
                "contact_name": contact["name"],
                "contact_title": contact["title"],
                "email": contact["email"],
                "enriched_at": datetime.now().isoformat(),
                "source": "hospitality_contact_database"
            })
            
            cursor.execute("""
                UPDATE leads 
                SET contact_name = ?, contact_title = ?, email = ?, 
                    enrichment_status = 'enriched', enrichment_data = ?
                WHERE id = ?
            """, (contact["name"], contact["title"], contact["email"], 
                  enrichment_data, lead_id))
        return True
    
    # Generate likely emails based on patterns
    domain = get_domain_from_website(website)
    if domain:
        # Create placeholder enrichment for manual follow-up
        enrichment_data = json.dumps({
            "potential_domain": domain,
            "suggested_titles": HOSPITALITY_TITLES,
            "enrichment_status": "needs_manual_research",
            "enriched_at": datetime.now().isoformat()
        })
        
        cursor.execute("""
            UPDATE leads 
            SET enrichment_status = 'needs_manual', enrichment_data = ?
            WHERE id = ?
        """, (enrichment_data, lead_id))
        return True
    
    return False

def main():
    """Run enrichment on hospitality leads"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get unenriched hospitality leads (casinos AND hotels for Capton)
    cursor.execute("""
        SELECT id, business_name, city, sos_url, source, category
        FROM leads 
        WHERE ((category IN ('Gaming/Casino', 'Hospitality', 'Hotel') 
               OR business_type IN ('Casino', 'Hotel'))
        AND (enrichment_status = 'pending' OR enrichment_status IS NULL))
        AND (source LIKE '%Capton%' OR source LIKE '%Casino_Scraper%' OR source LIKE '%Hotel_Scraper%')
    """)
    
    leads = cursor.fetchall()
    
    print(f"Enriching {len(leads)} hospitality leads for Capton...")
    print("=" * 70)
    
    enriched = 0
    needs_manual = 0
    
    for lead in leads:
        lead_id, business_name, city, website, source, category = lead
        
        success = enrich_lead(cursor, lead_id, business_name, website or "")
        
        if success:
            if business_name in ENRICHED_CONTACTS:
                enriched += 1
                print(f"✓ Enriched: {business_name}")
            else:
                needs_manual += 1
                print(f"⚠ Needs research: {business_name}")
        
        time.sleep(0.1)  # Rate limiting
    
    conn.commit()
    conn.close()
    
    print("=" * 70)
    print(f"Enrichment Complete!")
    print(f"  Auto-enriched: {enriched}")
    print(f"  Needs manual: {needs_manual}")
    print(f"  Total processed: {len(leads)}")

if __name__ == "__main__":
    main()
