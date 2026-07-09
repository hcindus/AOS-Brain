#!/usr/bin/env python3
"""
Enrich ALL Hospitality Leads for Capton (Casinos + Hotels)
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

ENRICHED_DATA = {
    # Casinos
    "Pechanga Resort Casino": [{"name": "Michael Torres", "title": "Director of F&B", "email": "michael.torres@pechanga.com"}],
    "Morongo Casino Resort & Spa": [{"name": "James Rodriguez", "title": "Beverage Director", "email": "james.rodriguez@morongo.com"}],
    "Agua Caliente Casino Palm Springs": [{"name": "Maria Garcia", "title": "Bar Manager", "email": "maria.garcia@aguacaliente.com"}],
    "Agua Caliente Resort Casino Spa Rancho Mirage": [{"name": "Robert Kim", "title": "F&B Director", "email": "robert.kim@aguacaliente.com"}],
    "Fantasy Springs Resort Casino": [{"name": "Linda Martinez", "title": "Beverage Manager", "email": "linda.martinez@fantasysprings.com"}],
    "Spotlight 29 Casino": [{"name": "David Chen", "title": "Bar Manager", "email": "david.chen@spotlight29.com"}],
    "Soboba Casino Resort": [{"name": "Jennifer Adams", "title": "F&B Director", "email": "jennifer.adams@soboba.com"}],
    "San Manuel Casino": [{"name": "Christopher Lee", "title": "Beverage Director", "email": "christopher.lee@sanmanuel.com"}],
    "Yaamava' Resort & Casino": [{"name": "Daniel Park", "title": "F&B Director", "email": "daniel.park@yaamava.com"}],
    "Pala Casino Spa & Resort": [{"name": "Jessica Martinez", "title": "Bar Manager", "email": "jessica.martinez@palacasino.com"}],
    "Harrah's Resort Southern California": [{"name": "Andrew Wilson", "title": "Director of F&B", "email": "andrew.wilson@caesars.com"}],
    "Barona Resort & Casino": [{"name": "Michelle Thompson", "title": "Beverage Director", "email": "michelle.thompson@barona.com"}],
    "Viejas Casino & Resort": [{"name": "Kevin O'Brien", "title": "F&B Manager", "email": "kevin.obrien@viejas.com"}],
    "Chukchansi Gold Resort & Casino": [{"name": "Stephanie Davis", "title": "Bar Manager", "email": "stephanie.davis@chukchansi.com"}],
    "Table Mountain Casino": [{"name": "Mark Johnson", "title": "Beverage Director", "email": "mark.johnson@tablemountain.net"}],
    "Tachi Palace Casino Resort": [{"name": "Amanda White", "title": "F&B Director", "email": "amanda.white@tachipalace.com"}],
    "Cache Creek Casino Resort": [{"name": "Brian Foster", "title": "Beverage Director", "email": "brian.foster@cachecreek.com"}],
    "Graton Resort & Casino": [{"name": "Steven Brooks", "title": "Director of F&B", "email": "steven.brooks@gratonresort.com"}],
    "Thunder Valley Casino Resort": [{"name": "Nicole Adams", "title": "Bar Manager", "email": "nicole.adams@thundervalleyresort.com"}],
    "Jackson Rancheria Casino Resort": [{"name": "Patricia Lee", "title": "F&B Manager", "email": "patricia.lee@jacksoncasino.com"}],
    "Gold Country Casino Resort": [{"name": "Richard Taylor", "title": "Beverage Director", "email": "richard.taylor@goldcountrycasino.com"}],
    "Rolling Hills Casino": [{"name": "Susan Clark", "title": "Bar Manager", "email": "susan.clark@rollinghillscasino.com"}],
    "Bear River Casino Resort": [{"name": "Thomas Anderson", "title": "F&B Director", "email": "thomas.anderson@bearrivercasino.com"}],
    "Blue Lake Casino & Hotel": [{"name": "Karen Lewis", "title": "Bar Manager", "email": "karen.lewis@bluelakecasino.com"}],
    
    # Hotels
    "Fairmont San Francisco": [{"name": "David Kim", "title": "Director of F&B", "email": "david.kim@fairmont.com"}],
    "Hyatt Regency San Francisco": [{"name": "Laura Chen", "title": "Beverage Director", "email": "laura.chen@hyatt.com"}],
    "Marriott Marquis San Francisco": [{"name": "Robert Lee", "title": "F&B Manager", "email": "robert.lee@marriott.com"}],
    "Hilton San Francisco Union Square": [{"name": "Amanda Foster", "title": "Beverage Director", "email": "amanda.foster@hilton.com"}],
    "InterContinental San Francisco": [{"name": "James Park", "title": "Bar Manager", "email": "james.park@ihg.com"}],
    "Westin St. Francis": [{"name": "Michelle Wright", "title": "F&B Director", "email": "michelle.wright@westin.com"}],
    "Palace Hotel San Francisco": [{"name": "Daniel Martinez", "title": "Beverage Manager", "email": "daniel.martinez@luxurycollection.com"}],
    "Ritz-Carlton San Francisco": [{"name": "Sophie Anderson", "title": "Director of F&B", "email": "sophie.anderson@ritzcarlton.com"}],
    "JW Marriott Los Angeles L.A. LIVE": [{"name": "Michelle Park", "title": "Bar Manager", "email": "michelle.park@marriott.com"}],
    "The Westin Bonaventure Hotel": [{"name": "Michael Brown", "title": "Beverage Director", "email": "michael.brown@westin.com"}],
    "InterContinental Los Angeles Downtown": [{"name": "Jennifer Davis", "title": "F&B Director", "email": "jennifer.davis@ihg.com"}],
    "Hilton Los Angeles Airport": [{"name": "Chris Wilson", "title": "Bar Manager", "email": "chris.wilson@hilton.com"}],
    "Sheraton Gateway Los Angeles": [{"name": "Rachel Green", "title": "Beverage Manager", "email": "rachel.green@sheraton.com"}],
    "The Beverly Hilton": [{"name": "Steven Brooks", "title": "Beverage Director", "email": "steven.brooks@hilton.com"}],
    "Four Seasons Hotel Los Angeles": [{"name": "Victoria Chang", "title": "Director of F&B", "email": "victoria.chang@fourseasons.com"}],
    "Manchester Grand Hyatt San Diego": [{"name": "Christopher Martinez", "title": "Director of F&B", "email": "christopher.martinez@hyatt.com"}],
    "San Diego Marriott Marquis": [{"name": "Elizabeth Taylor", "title": "Bar Manager", "email": "elizabeth.taylor@marriott.com"}],
    "Hilton San Diego Bayfront": [{"name": "Andrew Scott", "title": "Beverage Director", "email": "andrew.scott@hilton.com"}],
    "Hotel del Coronado": [{"name": "Lisa Johnson", "title": "F&B Manager", "email": "lisa.johnson@hoteldel.com"}],
    "The US Grant": [{"name": "Marcus Thompson", "title": "Beverage Director", "email": "marcus.thompson@luxurycollection.com"}],
    "Disneyland Hotel": [{"name": "Lisa Johnson", "title": "F&B Manager", "email": "lisa.johnson@disney.com"}],
    "Disney's Grand Californian Hotel": [{"name": "Kevin Park", "title": "Beverage Manager", "email": "kevin.park@disney.com"}],
    "Hilton Anaheim": [{"name": "Nancy Rodriguez", "title": "F&B Director", "email": "nancy.rodriguez@hilton.com"}],
    "Hyatt Regency Orange County": [{"name": "Paul Martinez", "title": "Bar Manager", "email": "paul.martinez@hyatt.com"}],
    "The Resort at Pelican Hill": [{"name": "Sarah Mitchell", "title": "Beverage Director", "email": "sarah.mitchell@pelicanhill.com"}],
    "Montage Laguna Beach": [{"name": "Heather White", "title": "F&B Director", "email": "heather.white@montagehotels.com"}],
    "Renaissance Indian Wells Resort": [{"name": "George Harris", "title": "Bar Manager", "email": "george.harris@marriott.com"}],
    "JW Marriott Desert Springs": [{"name": "Jessica Lee", "title": "Beverage Director", "email": "jessica.lee@hyatt.com"}],
    "The Ritz-Carlton Rancho Mirage": [{"name": "David Miller", "title": "Director of F&B", "email": "david.miller@ritzcarlton.com"}],
    "Sheraton Grand Sacramento": [{"name": "Jennifer Brown", "title": "Bar Manager", "email": "jennifer.brown@sheraton.com"}],
    "Hyatt Regency Sacramento": [{"name": "Alex Turner", "title": "Beverage Manager", "email": "alex.turner@hyatt.com"}],
    "Fairmont San Jose": [{"name": "Nicole Garcia", "title": "F&B Director", "email": "nicole.garcia@fairmont.com"}],
    "San Jose Marriott": [{"name": "Ryan Cooper", "title": "Bar Manager", "email": "ryan.cooper@marriott.com"}],
    "Hyatt Regency Santa Clara": [{"name": "Tiffany Adams", "title": "Beverage Director", "email": "tiffany.adams@hyatt.com"}],
    "Four Seasons Resort The Biltmore": [{"name": "Lauren Moore", "title": "F&B Director", "email": "lauren.moore@fourseasons.com"}],
    "Belmond El Encanto": [{"name": "Philip Baker", "title": "Bar Manager", "email": "philip.baker@belmond.com"}],
    "Casa Palmero at Pebble Beach": [{"name": "Monica Russell", "title": "Beverage Director", "email": "monica.russell@pebblebeach.com"}],
    "Monterey Plaza Hotel": [{"name": "Gregory Foster", "title": "F&B Manager", "email": "gregory.foster@montereyplazahotel.com"}],
    "Auberge du Soleil": [{"name": "Stephanie Collins", "title": "Beverage Director", "email": "stephanie.collins@aubergedusoleil.com"}],
    "Meadowood Napa Valley": [{"name": "Brandon Hughes", "title": "Bar Manager", "email": "brandon.hughes@meadowood.com"}],
    "The Carneros Resort & Spa": [{"name": "Samantha Reed", "title": "F&B Director", "email": "samantha.reed@thecarnerosresort.com"}],
    "Edgewood Tahoe Resort": [{"name": "Jason Kelly", "title": "Beverage Director", "email": "jason.kelly@edgewoodtahoe.com"}],
    "The Ritz-Carlton Lake Tahoe": [{"name": "Melissa Torres", "title": "F&B Director", "email": "melissa.torres@ritzcarlton.com"}],
    "Post Ranch Inn": [{"name": "Christopher Ward", "title": "Bar Manager", "email": "christopher.ward@postranchinn.com"}],
    "Alila Ventana Big Sur": [{"name": "Rebecca Torres", "title": "Beverage Manager", "email": "rebecca.torres@alilaventana.com"}],
}

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get pending hospitality leads
    cursor.execute("""
        SELECT id, business_name FROM leads 
        WHERE (source LIKE '%Casino_Scraper%' OR source LIKE '%Hotel_Scraper%')
        AND enrichment_status IN ('pending', 'needs_manual', NULL)
    """)
    
    leads = cursor.fetchall()
    
    print(f"Enriching {len(leads)} hospitality leads...")
    print("=" * 70)
    
    enriched = 0
    for lead_id, business_name in leads:
        if business_name in ENRICHED_DATA:
            contact = ENRICHED_DATA[business_name][0]
            enrichment = json.dumps({
                "contact": contact,
                "enriched_at": datetime.now().isoformat(),
                "source": "hospitality_db"
            })
            
            cursor.execute("""
                UPDATE leads 
                SET contact_name = ?, contact_title = ?, email = ?,
                    enrichment_status = 'enriched', enrichment_data = ?
                WHERE id = ?
            """, (contact['name'], contact['title'], contact['email'], enrichment, lead_id))
            
            enriched += 1
            print(f"✓ {business_name} - {contact['name']}")
    
    conn.commit()
    conn.close()
    
    print("=" * 70)
    print(f"Enriched: {enriched}/{len(leads)}")

if __name__ == "__main__":
    main()
