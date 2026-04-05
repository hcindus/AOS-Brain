#!/usr/bin/env python3
"""
WORKING Lead Scraper - Actually makes HTTP requests
Uses only requests + regex (no BeautifulSoup needed)
"""

import os
import re
import time
import json
import requests
import pandas as pd
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

class WorkingLeadScraper:
    """Actually scrapes real business data"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def search_and_extract(self, business: str, city: str, state: str) -> dict:
        """Search Bing and extract real data"""
        result = {"address": "", "phone": "", "email": ""}
        
        # Build search query
        query = f"{business} {city} {state}"
        
        try:
            # Search Bing
            search_url = f"https://www.bing.com/search?q={quote_plus(query)}"
            print(f"      Searching...", end=" ")
            
            resp = self.session.get(search_url, timeout=15)
            
            if resp.status_code != 200:
                print(f"✗ (status {resp.status_code})")
                return result
            
            html = resp.text
            
            # Extract from search results page
            result["phone"] = self._extract_phone(html)
            result["email"] = self._extract_email(html)
            result["address"] = self._extract_address(html, city, state)
            
            # If we found phone or email, great
            if result["phone"] or result["email"]:
                found = []
                if result["phone"]: found.append("phone")
                if result["email"]: found.append("email")
                if result["address"]: found.append("address")
                print(f"✓ found {', '.join(found)}")
            else:
                print("○ (no data in search results)")
            
            time.sleep(2)  # Rate limit
            
        except Exception as e:
            print(f"✗ error: {e}")
        
        return result
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone from HTML/text"""
        # Pattern: (xxx) xxx-xxxx or xxx-xxx-xxxx
        pattern = r'\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        matches = re.findall(pattern, text)
        
        for m in matches:
            # Filter out common false positives
            phone = f"({m[0]}) {m[1]}-{m[2]}"
            # Skip if starts with 555 (fake) or is too common
            if m[0] not in ['555', '000', '123']:
                return phone
        return ""
    
    def _extract_email(self, text: str) -> str:
        """Extract email from HTML/text"""
        pattern = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
        matches = re.findall(pattern, text)
        
        for email in matches:
            # Filter common false positives
            skip = ['example.com', 'domain.com', 'email.com', 'test.com', 
                   'yourdomain.com', 'company.com', 'business.com', 'site.com']
            if not any(s in email.lower() for s in skip):
                # Skip if looks like a template
                if len(email) < 50 and '.' in email.split('@')[1]:
                    return email
        return ""
    
    def _extract_address(self, text: str, city: str, state: str) -> str:
        """Extract address from HTML/text"""
        if not city or not state:
            return ""
        
        # Pattern: number + street + city + state + zip
        # Look for: 123 Main St, City, State 12345
        city_escaped = re.escape(city)
        state_escaped = re.escape(state)
        
        # Try multiple patterns
        patterns = [
            rf'(\d+)\s+([\w\s]+?)(?:\s+(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Blvd|Boulevard|Ln|Lane))[^\w]*{city_escaped}[^\w]*{state_escaped}[^\w]*(?:\d{{5}})?',
            rf'(\d+)\s+([\w\s]+?),?\s*{city_escaped}[^\w]*{state_escaped}',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                addr = match.group(0).strip()
                # Clean up
                addr = re.sub(r'\s+', ' ', addr)
                if len(addr) > 10 and len(addr) < 150:
                    return addr
        
        return ""
    
    def process_excel(self, input_path: str, output_dir: str) -> str:
        """Process an Excel file"""
        filename = os.path.basename(input_path)
        print(f"\n{'='*70}")
        print(f"Processing: {filename}")
        print(f"{'='*70}")
        
        # Read file
        try:
            df = pd.read_excel(input_path)
            print(f"  Rows: {len(df)}")
        except Exception as e:
            print(f"  ✗ Error reading: {e}")
            return ""
        
        # Find columns
        business_col = None
        city_col = None
        state_col = None
        
        for col in df.columns:
            col_str = str(col).lower()
            if 'business' in col_str:
                business_col = col
            elif col_str == 'city':
                city_col = col
            elif col_str == 'state':
                state_col = col
        
        if not business_col:
            print("  ✗ No business column")
            return ""
        
        print(f"  Columns: Business={business_col}, City={city_col}, State={state_col}")
        
        # Ensure output columns
        if 'Address' not in df.columns:
            df['Address'] = ""
        if 'Phone' not in df.columns:
            df['Phone'] = ""
        if 'Email' not in df.columns:
            df['Email'] = ""
        
        # Process rows
        found = {"address": 0, "phone": 0, "email": 0}
        
        for idx, row in df.iterrows():
            business = str(row.get(business_col, "")).strip()
            if not business or business.lower() in ['nan', 'none', '']:
                continue
            
            city = str(row.get(city_col, "")).strip() if city_col else ""
            state = str(row.get(state_col, "")).strip() if state_col else ""
            
            print(f"  [{idx+1}/{len(df)}] {business[:40]}...")
            
            # Check if already has data
            existing = {
                "address": str(row.get('Address', "")).strip(),
                "phone": str(row.get('Phone', "")).strip(),
                "email": str(row.get('Email', "")).strip()
            }
            
            if all(existing.values()):
                print(f"      Already complete")
                continue
            
            # Scrape
            data = self.search_and_extract(business, city, state)
            
            # Update
            if data["address"] and not existing["address"]:
                df.at[idx, 'Address'] = data["address"]
                found["address"] += 1
            if data["phone"] and not existing["phone"]:
                df.at[idx, 'Phone'] = data["phone"]
                found["phone"] += 1
            if data["email"] and not existing["email"]:
                df.at[idx, 'Email'] = data["email"]
                found["email"] += 1
        
        # Save
        base, ext = os.path.splitext(filename)
        output_name = f"{base}_COMPLETED{ext}"
        output_path = os.path.join(output_dir, output_name)
        
        os.makedirs(output_dir, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        print(f"\n  ✓ Saved: {output_name}")
        print(f"  ✓ Found: {found['address']} addresses, {found['phone']} phones, {found['email']} emails")
        
        return output_path


def main():
    """Run working scraper"""
    print("=" * 70)
    print("WORKING LEAD SCRAPER - Makes Real HTTP Requests")
    print("=" * 70)
    print("\nThis scraper actually:")
    print("  • Searches Bing for each business")
    print("  • Extracts phone numbers from results")
    print("  • Extracts email addresses")
    print("  • Extracts addresses")
    print("\nRate limited: 2 seconds between requests")
    
    leads_dir = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads"
    output_dir = os.path.join(leads_dir, "completed")
    
    # Find files
    files = []
    for f in sorted(os.listdir(leads_dir)):
        if f.endswith('.xlsx') and '_COMPLETED' not in f and 'enriched' not in f.lower():
            files.append(os.path.join(leads_dir, f))
    
    if not files:
        print("\nNo files found!")
        return
    
    print(f"\nFound {len(files)} files")
    
    # Test with a small file first
    small_files = sorted(files, key=lambda x: os.path.getsize(x))[:3]
    
    scraper = WorkingLeadScraper()
    completed = []
    
    for filepath in small_files:
        output = scraper.process_excel(filepath, output_dir)
        if output:
            completed.append(output)
    
    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"Files processed: {len(completed)}")
    for f in completed:
        print(f"  • {os.path.basename(f)}")
    
    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    for f in completed:
        df = pd.read_excel(f)
        has_phone = df['Phone'].notna().sum() if 'Phone' in df.columns else 0
        has_email = df['Email'].notna().sum() if 'Email' in df.columns else 0
        has_address = df['Address'].notna().sum() if 'Address' in df.columns else 0
        print(f"{os.path.basename(f)}:")
        print(f"  Addresses: {has_address}, Phones: {has_phone}, Emails: {has_email}")


if __name__ == "__main__":
    main()
