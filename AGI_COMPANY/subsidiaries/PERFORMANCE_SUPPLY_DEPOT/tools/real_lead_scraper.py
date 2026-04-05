#!/usr/bin/env python3
"""
Real Lead Scraper - Actually finds missing business information
Searches web sources and extracts real addresses, phones, emails
"""

import os
import re
import time
import json
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from typing import Dict, Optional, List
import pandas as pd
from pathlib import Path

# Rate limiting
MIN_DELAY = 2
MAX_DELAY = 5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

class RealLeadScraper:
    """Actually scrapes real business information from the web"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.results_cache = {}
        
    def search_bing(self, query: str) -> Optional[str]:
        """Search Bing and return first result URL"""
        try:
            url = f"https://www.bing.com/search?q={quote_plus(query)}"
            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find first organic result
            for li in soup.find_all('li', class_='b_algo'):
                a = li.find('a', href=True)
                if a and a['href'].startswith('http'):
                    # Skip bing/google/etc
                    if not any(x in a['href'] for x in ['bing.', 'google.', 'duckduckgo.']):
                        return a['href']
            
            return None
        except Exception as e:
            print(f"    Search error: {e}")
            return None
    
    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        # US phone patterns
        patterns = [
            r'\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'([0-9]{3})[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                groups = match.groups()
                if len(groups) >= 3:
                    phone = f"({groups[0]}) {groups[1]}-{groups[2]}"
                    # Validate
                    if len(groups[0]) == 3 and len(groups[1]) == 3 and len(groups[2]) == 4:
                        return phone
        return None
    
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email from text"""
        pattern = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
        matches = re.findall(pattern, text)
        
        for email in matches:
            # Filter out common false positives
            skip = ['example', 'domain', 'email@', 'test@', 'info@example', '@gmail.com', '@yahoo.com']
            if not any(s in email.lower() for s in skip):
                return email
        return None
    
    def extract_address(self, text: str, city: str, state: str) -> Optional[str]:
        """Extract street address from text"""
        # Look for address patterns
        lines = text.replace('\n', ' ').split(' ')
        
        for i in range(len(lines)):
            segment = ' '.join(lines[i:i+10])  # Look at chunks
            
            # Pattern: number + street + city + state + zip
            addr_pattern = rf'(\d+)\s+([\w\s]+?)\s+({re.escape(city)})\s*,?\s*({re.escape(state)})\s*\d{{5}}'
            match = re.search(addr_pattern, segment, re.IGNORECASE)
            if match:
                return match.group(0).strip()
            
            # Simpler: number + street keywords
            if re.match(r'\d+\s+\w+', segment):
                street_keywords = ['st', 'street', 'ave', 'avenue', 'rd', 'road', 'dr', 'drive', 
                                  'blvd', 'boulevard', 'ln', 'lane', 'way', 'court', 'ct', 'plaza']
                if any(kw in segment.lower() for kw in street_keywords):
                    if city.lower() in segment.lower() or state.lower() in segment.lower():
                        return segment.strip()[:100]  # Limit length
        
        return None
    
    def scrape_page(self, url: str) -> Dict:
        """Scrape a webpage for business info"""
        result = {"address": None, "phone": None, "email": None}
        
        try:
            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Get all text
            text = soup.get_text(' ', strip=True)
            
            # Extract phone
            result["phone"] = self.extract_phone(text)
            
            # Extract email
            result["email"] = self.extract_email(text)
            
            return result
            
        except Exception as e:
            print(f"    Page scrape error: {e}")
            return result
    
    def enrich_business(self, business: str, city: str, state: str, 
                        zip_code: str = "") -> Dict:
        """Enrich a single business with real scraped data"""
        
        # Build search query
        query_parts = [p for p in [business, city, state] if p]
        query = " ".join(query_parts)
        
        print(f"    Searching: {query[:60]}...", end=" ")
        
        # Search for the business
        result_url = self.search_bing(query)
        
        if not result_url:
            print("✗ (no results)")
            return {"address": None, "phone": None, "email": None}
        
        print(f"→ {result_url[:40]}...", end=" ")
        
        # Scrape the result page
        data = self.scrape_page(result_url)
        
        # Try to get address
        if not data["address"]:
            data["address"] = self.extract_address(
                self.session.get(result_url, timeout=10).text if result_url else "", 
                city, state
            )
        
        found = [k for k, v in data.items() if v]
        if found:
            print(f"✓ ({', '.join(found)})")
        else:
            print("○")
        
        # Rate limit
        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
        
        return data
    
    def process_excel_file(self, input_path: str, output_dir: str) -> str:
        """Process an Excel file and generate enriched output"""
        filename = os.path.basename(input_path)
        print(f"\n{'='*70}")
        print(f"Processing: {filename}")
        print(f"{'='*70}")
        
        # Read file
        try:
            df = pd.read_excel(input_path)
        except Exception as e:
            print(f"  ✗ Error reading file: {e}")
            return ""
        
        print(f"  Rows: {len(df)}")
        
        # Detect columns
        business_col = None
        city_col = None
        state_col = None
        zip_col = None
        
        for col in df.columns:
            col_str = str(col).lower()
            if 'business' in col_str or col_str == 'name':
                business_col = col
            elif col_str == 'city':
                city_col = col
            elif col_str == 'state':
                state_col = col
            elif 'zip' in col_str:
                zip_col = col
        
        if not business_col:
            print("  ✗ No business name column found")
            return ""
        
        # Ensure output columns exist
        if 'Address' not in df.columns:
            df['Address'] = ""
        if 'Phone' not in df.columns:
            df['Phone'] = ""
        if 'Email' not in df.columns:
            df['Email'] = ""
        
        # Process each row
        enriched = {"address": 0, "phone": 0, "email": 0}
        
        for idx, row in df.iterrows():
            business = str(row.get(business_col, "")).strip()
            if not business or business.lower() in ['nan', 'none', '']:
                continue
            
            city = str(row.get(city_col, "")).strip() if city_col else ""
            state = str(row.get(state_col, "")).strip() if state_col else ""
            zip_code = str(row.get(zip_col, "")).strip() if zip_col else ""
            
            print(f"  [{idx+1}/{len(df)}] {business[:45]}...")
            
            # Check if already has data
            existing = {
                "address": str(row.get('Address', "")).strip(),
                "phone": str(row.get('Phone', "")).strip(),
                "email": str(row.get('Email', "")).strip()
            }
            
            # Skip if complete
            if all(existing.values()):
                print(f"    Already complete")
                continue
            
            # Enrich
            data = self.enrich_business(business, city, state, zip_code)
            
            # Update dataframe
            if data["address"] and not existing["address"]:
                df.at[idx, 'Address'] = data["address"]
                enriched["address"] += 1
            if data["phone"] and not existing["phone"]:
                df.at[idx, 'Phone'] = data["phone"]
                enriched["phone"] += 1
            if data["email"] and not existing["email"]:
                df.at[idx, 'Email'] = data["email"]
                enriched["email"] += 1
        
        # Save output
        base, ext = os.path.splitext(filename)
        output_name = f"{base}_COMPLETED{ext}"
        output_path = os.path.join(output_dir, output_name)
        
        os.makedirs(output_dir, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        print(f"\n  ✓ Saved: {output_name}")
        print(f"  ✓ Enriched: {enriched['address']} addresses, {enriched['phone']} phones, {enriched['email']} emails")
        
        return output_path


def main():
    """Run real lead scraper"""
    print("=" * 70)
    print("REAL LEAD SCRAPER - Live Web Search")
    print("=" * 70)
    print("\nThis scraper actually searches the web and extracts real data:")
    print("  • Addresses from business websites")
    print("  • Phone numbers from contact pages")
    print("  • Emails when publicly listed")
    print("\nRate limited to be respectful to search engines")
    
    # Find lead files
    leads_dir = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads"
    output_dir = os.path.join(leads_dir, "completed")
    
    # Find files
    files = []
    for f in os.listdir(leads_dir):
        if f.endswith('.xlsx') and '_COMPLETED' not in f and 'enriched' not in f.lower():
            files.append(os.path.join(leads_dir, f))
    
    if not files:
        print("\nNo lead files found!")
        return
    
    print(f"\nFound {len(files)} files to process")
    print(f"Output: {output_dir}")
    
    # Initialize scraper
    scraper = RealLeadScraper()
    
    # Process files
    completed = []
    for filepath in files[:3]:  # Process first 3 for demo
        output = scraper.process_excel_file(filepath, output_dir)
        if output:
            completed.append(output)
    
    # Summary
    print("\n" + "=" * 70)
    print("SCRAPING COMPLETE")
    print("=" * 70)
    print(f"Files processed: {len(completed)}")
    for f in completed:
        print(f"  • {os.path.basename(f)}")


if __name__ == "__main__":
    main()
