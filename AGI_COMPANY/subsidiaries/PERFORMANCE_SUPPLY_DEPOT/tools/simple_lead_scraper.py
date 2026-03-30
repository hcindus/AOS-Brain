#!/usr/bin/env python3
"""
Simple Lead Scraper - Uses regex instead of BeautifulSoup
Actually searches web and extracts real business info
"""

import os
import re
import time
import random
import requests
import pandas as pd
from urllib.parse import quote_plus
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

class SimpleLeadScraper:
    """Scrapes real business data using regex (no external deps)"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def search_bing(self, query: str) -> str:
        """Search Bing, return HTML"""
        try:
            url = f"https://www.bing.com/search?q={quote_plus(query)}"
            resp = self.session.get(url, timeout=15)
            return resp.text if resp.status_code == 200 else ""
        except Exception as e:
            return ""
    
    def extract_from_html(self, html: str, city: str, state: str) -> dict:
        """Extract data from HTML using regex"""
        result = {"address": "", "phone": "", "email": ""}
        
        if not html:
            return result
        
        # Clean HTML for text extraction
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        
        # Extract phone
        phone_pattern = r'\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        if phones:
            result["phone"] = f"({phones[0][0]}) {phones[0][1]}-{phones[0][2]}"
        
        # Extract email
        email_pattern = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        if emails:
            # Filter out common false positives
            skip = ['example', 'domain', 'email@', 'test@', '@google', '@bing']
            for email in emails:
                if not any(s in email.lower() for s in skip) and len(email) < 50:
                    result["email"] = email
                    break
        
        # Extract address (number + street + city + state + zip)
        if city and state:
            addr_pattern = rf'(\d+)\s+([\w\s]+?)(?:\s+(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Blvd|Boulevard|Ln|Lane))[^\w]*{re.escape(city)}[^\w]*{re.escape(state)}[^\w]*(?:\d{{5}})?'
            addr_match = re.search(addr_pattern, text, re.IGNORECASE)
            if addr_match:
                result["address"] = addr_match.group(0).strip()[:100]
        
        return result
    
    def find_result_url(self, html: str) -> str:
        """Find first organic result URL in Bing HTML"""
        if not html:
            return ""
        
        # Look for result URLs
        # Pattern: <a href="http..." ...>
        url_pattern = r'<a[^>]+href="(https?://[^"]+)"'
        urls = re.findall(url_pattern, html)
        
        for url in urls:
            # Skip search engines and common non-business domains
            skip = ['bing.com', 'microsoft.com', 'facebook.com', 'youtube.com', 
                   'wikipedia.org', 'yelp.com/biz', 'maps.google']
            if not any(s in url.lower() for s in skip):
                return url
        
        return ""
    
    def scrape_url(self, url: str) -> str:
        """Scrape a URL, return HTML"""
        try:
            resp = self.session.get(url, timeout=15)
            return resp.text if resp.status_code == 200 else ""
        except Exception as e:
            return ""
    
    def enrich_business(self, business: str, city: str, state: str) -> dict:
        """Enrich a single business"""
        query = f"{business} {city} {state}"
        
        print(f"    Searching: {query[:50]}...", end=" ")
        
        # Search
        search_html = self.search_bing(query)
        if not search_html:
            print("✗ (no search)")
            return {"address": "", "phone": "", "email": ""}
        
        # Try to extract from search results first
        data = self.extract_from_html(search_html, city, state)
        
        # If we need more, visit first result
        if not data["address"] or not data["phone"]:
            result_url = self.find_result_url(search_html)
            if result_url:
                print(f"→ {result_url[:30]}...", end=" ")
                page_html = self.scrape_url(result_url)
                if page_html:
                    page_data = self.extract_from_html(page_html, city, state)
                    # Merge results
                    if not data["address"] and page_data["address"]:
                        data["address"] = page_data["address"]
                    if not data["phone"] and page_data["phone"]:
                        data["phone"] = page_data["phone"]
                    if not data["email"] and page_data["email"]:
                        data["email"] = page_data["email"]
        
        found = [k for k, v in data.items() if v]
        if found:
            print(f"✓ ({', '.join(found)})")
        else:
            print("○")
        
        time.sleep(random.uniform(2, 4))
        return data
    
    def process_file(self, input_path: str, output_dir: str) -> str:
        """Process an Excel file"""
        filename = os.path.basename(input_path)
        print(f"\n{'='*70}")
        print(f"Processing: {filename}")
        print(f"{'='*70}")
        
        try:
            df = pd.read_excel(input_path)
        except Exception as e:
            print(f"  ✗ Error reading: {e}")
            return ""
        
        print(f"  Rows: {len(df)}")
        
        # Detect columns
        business_col = None
        city_col = None
        state_col = None
        
        for col in df.columns:
            col_str = str(col).lower()
            if 'business' in col_str or col_str == 'name':
                business_col = col
            elif col_str == 'city':
                city_col = col
            elif col_str == 'state':
                state_col = col
        
        if not business_col:
            print("  ✗ No business column found")
            return ""
        
        # Ensure output columns
        if 'Address' not in df.columns:
            df['Address'] = ""
        if 'Phone' not in df.columns:
            df['Phone'] = ""
        if 'Email' not in df.columns:
            df['Email'] = ""
        
        # Process rows
        enriched = {"address": 0, "phone": 0, "email": 0}
        
        for idx, row in df.iterrows():
            business = str(row.get(business_col, "")).strip()
            if not business or business.lower() in ['nan', 'none', '']:
                continue
            
            city = str(row.get(city_col, "")).strip() if city_col else ""
            state = str(row.get(state_col, "")).strip() if state_col else ""
            
            print(f"  [{idx+1}/{len(df)}] {business[:40]}...")
            
            # Check existing
            existing = {
                "address": str(row.get('Address', "")).strip(),
                "phone": str(row.get('Phone', "")).strip(),
                "email": str(row.get('Email', "")).strip()
            }
            
            if all(existing.values()):
                print(f"    Already complete")
                continue
            
            # Enrich
            data = self.enrich_business(business, city, state)
            
            # Update
            if data["address"] and not existing["address"]:
                df.at[idx, 'Address'] = data["address"]
                enriched["address"] += 1
            if data["phone"] and not existing["phone"]:
                df.at[idx, 'Phone'] = data["phone"]
                enriched["phone"] += 1
            if data["email"] and not existing["email"]:
                df.at[idx, 'Email'] = data["email"]
                enriched["email"] += 1
        
        # Save
        base, ext = os.path.splitext(filename)
        output_name = f"{base}_COMPLETED{ext}"
        output_path = os.path.join(output_dir, output_name)
        
        os.makedirs(output_dir, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        print(f"\n  ✓ Saved: {output_name}")
        print(f"  ✓ Found: {enriched['address']} addresses, {enriched['phone']} phones, {enriched['email']} emails")
        
        return output_path


def main():
    """Run scraper"""
    print("=" * 70)
    print("SIMPLE LEAD SCRAPER - Live Web Search")
    print("=" * 70)
    print("Uses regex - no external dependencies required")
    
    leads_dir = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads"
    output_dir = os.path.join(leads_dir, "completed")
    
    # Find files
    files = []
    for f in os.listdir(leads_dir):
        if f.endswith('.xlsx') and '_COMPLETED' not in f and 'enriched' not in f.lower():
            files.append(os.path.join(leads_dir, f))
    
    if not files:
        print("\nNo files found!")
        return
    
    print(f"\nFound {len(files)} files")
    
    scraper = SimpleLeadScraper()
    
    # Process small files first
    files.sort(key=lambda x: os.path.getsize(x))
    
    completed = []
    for filepath in files[:3]:  # First 3
        output = scraper.process_file(filepath, output_dir)
        if output:
            completed.append(output)
    
    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"Processed: {len(completed)} files")
    for f in completed:
        print(f"  • {os.path.basename(f)}")


if __name__ == "__main__":
    main()
