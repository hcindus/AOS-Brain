#!/usr/bin/env python3
"""
Real Hospitality Lead Enrichment
Uses multiple data sources to find actual F&B and bar manager contacts
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import time
import json
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

class RealHospitalityEnricher:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_pending_leads(self):
        """Get leads needing real enrichment"""
        self.cursor.execute("""
            SELECT id, business_name, city, sos_url 
            FROM leads
            WHERE (source LIKE '%Casino_Scraper%' OR source LIKE '%Hotel_Scraper%')
            AND (enrichment_status IN ('pending', 'needs_manual') OR enrichment_status IS NULL)
            ORDER BY business_name
        """)
        return self.cursor.fetchall()
    
    def scrape_casino_website(self, url, business_name):
        """Scrape casino website for staff/contact info"""
        contacts = []
        
        if not url:
            return contacts
        
        # Ensure URL has protocol
        if not url.startswith('http'):
            url = f"https://{url}"
        
        try:
            # Try common pages where staff info might be
            pages = ['/about', '/about-us', '/team', '/management', 
                    '/contact', '/careers', '/our-team', '/leadership']
            
            for page in pages[:3]:  # Limit to avoid rate limits
                try:
                    full_url = f"{url}{page}"
                    response = self.session.get(full_url, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for common patterns in staff listings
                        text = soup.get_text()
                        
                        # Search for beverage/bar related titles
                        patterns = [
                            r'([A-Z][a-z]+\s+[A-Z][a-z]+),?\s*(?:Director|Manager|VP)\s+of\s+(?:Food\s+&?\s*Beverage|Beverage|Bar|Operations)',
                            r'([A-Z][a-z]+\s+[A-Z][a-z]+),?\s*(?:Food\s+and\s+Beverage|F\s*\&\s*B|Beverage)\s+(?:Director|Manager)',
                            r'([A-Z][a-z]+\s+[A-Z][a-z]+),?\s*(?:Bar|Lounge|Restaurant)\s+Manager',
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, text, re.IGNORECASE)
                            for match in matches:
                                contacts.append({
                                    'name': match.strip(),
                                    'source': f"website:{page}"
                                })
                        
                        time.sleep(2)  # Rate limiting
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        return contacts
    
    def find_linkedin_contacts(self, business_name, city):
        """Search for LinkedIn profiles (mock - would need LinkedIn API)"""
        # This would require LinkedIn Sales Navigator API or similar
        # For now, return empty - implement with proper API access
        return []
    
    def verify_email_format(self, name, domain):
        """Generate likely email formats"""
        if not name or not domain:
            return []
        
        parts = name.split()
        if len(parts) < 2:
            return []
        
        first = parts[0].lower()
        last = parts[-1].lower().replace("'", "")
        first_initial = first[0]
        
        formats = [
            f"{first}.{last}@{domain}",
            f"{first}{last}@{domain}",
            f"{first_initial}{last}@{domain}",
            f"{first}@{domain}",
            f"{last}@{domain}",
        ]
        
        return formats
    
    def enrich_lead(self, lead_id, business_name, city, website):
        """Attempt real enrichment for one lead"""
        print(f"\nEnriching: {business_name} ({city})")
        
        # Try website scraping
        website_contacts = self.scrape_casino_website(website, business_name)
        
        # Try LinkedIn (mock for now)
        linkedin_contacts = self.find_linkedin_contacts(business_name, city)
        
        all_contacts = website_contacts + linkedin_contacts
        
        if all_contacts:
            # Store the first found contact
            contact = all_contacts[0]
            
            # Try to find/verify email
            domain = website.replace('https://', '').replace('http://', '').split('/')[0] if website else ''
            emails = self.verify_email_format(contact['name'], domain)
            
            enrichment_data = {
                'contact_name': contact['name'],
                'title': contact.get('title', 'Unknown'),
                'email': emails[0] if emails else None,
                'email_variations': emails,
                'source': contact['source'],
                'enriched_at': datetime.now().isoformat(),
                'method': 'real_scrape'
            }
            
            self.cursor.execute("""
                UPDATE leads 
                SET contact_name = ?, 
                    contact_title = ?,
                    email = ?,
                    enrichment_status = 'enriched',
                    enrichment_data = ?
                WHERE id = ?
            """, (
                contact['name'],
                contact.get('title', 'Unknown'),
                emails[0] if emails else None,
                json.dumps(enrichment_data),
                lead_id
            ))
            
            self.conn.commit()
            print(f"  ✓ Found: {contact['name']} from {contact['source']}")
            return True
        else:
            # Mark as needs_manual if no data found
            self.cursor.execute("""
                UPDATE leads 
                SET enrichment_status = 'needs_manual',
                    enrichment_data = ?
                WHERE id = ?
            """, (json.dumps({
                'attempted_at': datetime.now().isoformat(),
                'website_searched': website,
                'notes': 'No contacts found via automated scraping'
            }), lead_id))
            
            self.conn.commit()
            print(f"  ⚠ No contacts found - marked for manual research")
            return False
    
    def run_enrichment(self, limit=20):
        """Run enrichment on pending leads"""
        leads = self.get_pending_leads()
        
        print(f"Found {len(leads)} leads needing enrichment")
        print(f"Processing up to {limit}...")
        print("=" * 70)
        
        enriched = 0
        for i, (lead_id, business_name, city, website) in enumerate(leads[:limit]):
            success = self.enrich_lead(lead_id, business_name, city, website)
            if success:
                enriched += 1
            time.sleep(3)  # Rate limiting
        
        print("\n" + "=" * 70)
        print(f"Enriched: {enriched}/{min(limit, len(leads))}")
        
    def close(self):
        self.conn.close()

def main():
    enricher = RealHospitalityEnricher()
    enricher.run_enrichment(limit=10)  # Process 10 at a time
    enricher.close()

if __name__ == "__main__":
    main()
