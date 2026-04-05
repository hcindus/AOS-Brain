#!/usr/bin/env python3
"""
REAL Lead Scraper - Actually extracts business data
Uses BeautifulSoup + requests to scrape real websites
"""

import os
import re
import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

class RealScraper:
    """Actually scrapes business contact info"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def search_bing(self, query):
        """Search Bing and return results HTML"""
        url = f"https://www.bing.com/search?q={quote_plus(query)}"
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.text
        except Exception as e:
            print(f"Search error: {e}")
        return ""
    
    def get_business_url(self, search_html):
        """Extract business website URL from Bing results"""
        soup = BeautifulSoup(search_html, 'html.parser')
        
        # Find organic results
        for li in soup.find_all('li', class_='b_algo'):
            a = li.find('a', href=True)
            if not a:
                continue
                
            # Get the href - could be direct URL or Bing redirect
            href = a['href']
            
            # Check the link text/title for business indicators
            link_text = a.get_text().lower()
            title = a.get('title', '').lower()
            
            # Skip if it looks like Shakespeare, news, etc
            skip_keywords = ['sparknotes', 'shakespeare', 'wikipedia', 'facebook', 'yelp', 
                           'bbb.org', 'yellowpages', 'news', 'article', 'wikipedia']
            if any(k in link_text or k in title or k in href.lower() for k in skip_keywords):
                continue
            
            # Check if it's a restaurant/cafe site
            if href.startswith('http') and not href.startswith('https://www.bing.com'):
                # Direct URL
                skip = ['bing.com', 'google.', 'yelp.com', 'bbb.org', 'facebook.com', 'yellowpages.com']
                if not any(s in href.lower() for s in skip):
                    return href
            elif 'bing.com/ck/a' in href:
                # Bing redirect - extract real URL from data attributes or onclick
                # Look for cite tag which shows actual URL
                cite = li.find('cite')
                if cite:
                    actual_url = cite.get_text().strip()
                    if actual_url.startswith('http'):
                        return actual_url
        
        return ""
    
    def scrape_page(self, url):
        """Scrape a webpage and return BeautifulSoup object"""
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, 'html.parser')
        except Exception as e:
            print(f"Scrape error: {e}")
        return None
    
    def extract_phone(self, soup):
        """Extract phone number from page"""
        if not soup:
            return ""
        
        text = soup.get_text()
        
        # Phone patterns
        patterns = [
            r'\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                groups = match.groups()
                if len(groups) >= 3:
                    phone = f"({groups[0]}) {groups[1]}-{groups[2]}"
                    # Filter out fake numbers
                    if groups[0] not in ['555', '000', '123'] and len(groups[0]) == 3:
                        return phone
        return ""
    
    def extract_email(self, soup):
        """Extract email from page"""
        if not soup:
            return ""
        
        text = soup.get_text()
        
        # Email pattern
        pattern = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
        matches = re.findall(pattern, text)
        
        for email in matches:
            # Clean email - remove trailing non-alphanumeric chars
            email = re.sub(r'[^a-zA-Z0-9._%+-@]$', '', email)
            
            # Filter out templates and common fakes
            skip = ['example.com', 'domain.com', 'email.com', 'test.com', 'yourdomain',
                   'info@example', 'contact@example', 'admin@example', 'email@email']
            if not any(s in email.lower() for s in skip):
                if len(email) < 50 and '.' in email.split('@')[1]:
                    return email
        return ""
    
    def extract_address(self, soup, city, state):
        """Extract address from page"""
        if not soup or not city or not state:
            return ""
        
        text = soup.get_text()
        
        # Address pattern: number + street + city + state
        city_pattern = re.escape(city)
        state_pattern = re.escape(state)
        
        patterns = [
            rf'(\d+)\s+([\w\s]+?)\s+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln)\.?,?\s*{city_pattern}[^\w]*{state_pattern}',
            rf'(\d+)\s+([\w\s]+?),?\s*{city_pattern}',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                addr = match.group(0).strip()
                addr = re.sub(r'\s+', ' ', addr)  # Clean whitespace
                if 10 < len(addr) < 150:
                    return addr
        return ""
    
    def find_contact_page(self, soup, base_url):
        """Find contact/about page URL"""
        if not soup:
            return ""
        
        for a in soup.find_all('a', href=True):
            text = a.get_text().lower()
            href = a['href'].lower()
            
            if any(x in text for x in ['contact', 'about', 'reach us', 'get in touch']):
                return urljoin(base_url, a['href'])
            if any(x in href for x in ['/contact', '/about', 'contact.', 'about.']):
                return urljoin(base_url, a['href'])
        return ""
    
    def enrich_business(self, business, city, state):
        """Enrich a single business with real scraped data"""
        result = {"address": "", "phone": "", "email": ""}
        
        # Search
        query = f"{business} {city} {state}"
        print(f"      Searching: {query[:50]}...")
        
        search_html = self.search_bing(query)
        if not search_html:
            print(f"      ✗ No search results")
            return result
        
        # Get business URL
        business_url = self.get_business_url(search_html)
        if not business_url:
            print(f"      ✗ No business website found")
            return result
        
        print(f"      → {business_url[:50]}...")
        
        # Scrape main page
        soup = self.scrape_page(business_url)
        if soup:
            result["phone"] = self.extract_phone(soup)
            result["email"] = self.extract_email(soup)
            result["address"] = self.extract_address(soup, city, state)
        
        # Try contact page if missing data
        if not result["phone"] or not result["email"]:
            contact_url = self.find_contact_page(soup, business_url)
            if contact_url and contact_url != business_url:
                print(f"      → Contact page...")
                contact_soup = self.scrape_page(contact_url)
                if contact_soup:
                    if not result["phone"]:
                        result["phone"] = self.extract_phone(contact_soup)
                    if not result["email"]:
                        result["email"] = self.extract_email(contact_soup)
        
        # Show results
        found = [k for k, v in result.items() if v]
        if found:
            print(f"      ✓ Found: {', '.join(found)}")
        else:
            print(f"      ○ No data found")
        
        time.sleep(random.uniform(2, 4))
        return result
    
    def process_file(self, input_path, output_dir):
        """Process an Excel file"""
        filename = os.path.basename(input_path)
        print(f"\n{'='*70}")
        print(f"Processing: {filename}")
        print(f"{'='*70}")
        
        try:
            df = pd.read_excel(input_path)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return ""
        
        print(f"  Rows: {len(df)}")
        
        if len(df) == 0:
            print(f"  ✗ Empty file")
            return ""
        
        # Find columns
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
            print(f"  ✗ No business column found")
            return ""
        
        # Ensure output columns exist (as string type)
        if 'Address' not in df.columns:
            df['Address'] = ""
        else:
            df['Address'] = df['Address'].astype(str)
        if 'Phone' not in df.columns:
            df['Phone'] = ""
        else:
            df['Phone'] = df['Phone'].astype(str)
        if 'Email' not in df.columns:
            df['Email'] = ""
        else:
            df['Email'] = df['Email'].astype(str)
        
        # Process rows
        found = {"address": 0, "phone": 0, "email": 0}
        
        for idx, row in df.iterrows():
            business = str(row.get(business_col, "")).strip()
            if not business or business.lower() in ['nan', 'none', '']:
                continue
            
            city = str(row.get(city_col, "")).strip() if city_col else ""
            state = str(row.get(state_col, "")).strip() if state_col else ""
            
            print(f"  [{idx+1}/{len(df)}] {business[:40]}...")
            
            # Check existing - handle NaN properly
            existing = {
                "address": str(row.get('Address', "")).strip() if pd.notna(row.get('Address')) else "",
                "phone": str(row.get('Phone', "")).strip() if pd.notna(row.get('Phone')) else "",
                "email": str(row.get('Email', "")).strip() if pd.notna(row.get('Email')) else ""
            }
            
            # Filter out 'nan' strings
            existing = {k: "" if v.lower() == 'nan' else v for k, v in existing.items()}
            
            if all([existing["address"], existing["phone"], existing["email"]]):
                print(f"      Already complete")
                continue
            
            # Scrape
            data = self.enrich_business(business, city, state)
            
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
    """Run real scraper"""
    print("=" * 70)
    print("REAL LEAD SCRAPER - Actually Scrapes Websites")
    print("=" * 70)
    print("\nThis scraper:")
    print("  • Searches Bing")
    print("  • Finds business website")
    print("  • Visits website")
    print("  • Checks contact page")
    print("  • Extracts real phone/email/address")
    
    leads_dir = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads"
    output_dir = os.path.join(leads_dir, "completed")
    
    # Find files with actual data to enrich
    files = []
    for f in sorted(os.listdir(leads_dir)):
        if f.endswith('.xlsx') and '_COMPLETED' not in f and 'enriched' not in f.lower():
            filepath = os.path.join(leads_dir, f)
            try:
                df = pd.read_excel(filepath)
                if len(df) > 0:
                    files.append(filepath)
            except:
                pass
    
    if not files:
        print("\nNo files found!")
        return
    
    print(f"\nFound {len(files)} files")
    
    scraper = RealScraper()
    
    # Process first 3 small files
    files.sort(key=lambda x: os.path.getsize(x))
    
    completed = []
    for filepath in files[:3]:
        output = scraper.process_file(filepath, output_dir)
        if output:
            completed.append(output)
    
    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"Files processed: {len(completed)}")
    
    # Verification
    print("\nVerification:")
    for f in completed:
        df = pd.read_excel(f)
        has_phone = df['Phone'].notna().sum() if 'Phone' in df.columns else 0
        has_email = df['Email'].notna().sum() if 'Email' in df.columns else 0
        has_address = df['Address'].notna().sum() if 'Address' in df.columns else 0
        
        # Count non-empty strings too
        phone_non_empty = (df['Phone'] != '').sum() if 'Phone' in df.columns else 0
        email_non_empty = (df['Email'] != '').sum() if 'Email' in df.columns else 0
        addr_non_empty = (df['Address'] != '').sum() if 'Address' in df.columns else 0
        
        print(f"\n{os.path.basename(f)}:")
        print(f"  Phones: {phone_non_empty}")
        print(f"  Emails: {email_non_empty}")
        print(f"  Addresses: {addr_non_empty}")


if __name__ == "__main__":
    main()
