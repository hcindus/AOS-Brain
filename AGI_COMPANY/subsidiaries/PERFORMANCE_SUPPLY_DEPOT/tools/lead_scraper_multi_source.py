#!/usr/bin/env python3
"""
Multi-Source Lead Enrichment System

Distributes load across multiple data sources to avoid overloading any single site.
Rotates between: search engines, state registries, directories, company websites

Input: Excel files with Business Name, City, State, Zip
Output: *_COMPLETED.xlsx with Address, Phone, Email populated
"""

import os
import time
import re
import random
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Configuration
INPUT_FOLDER = "./LeadFiles"
OUTPUT_SUFFIX = "_COMPLETED"
SLEEP_MIN = 1.0
SLEEP_MAX = 3.0
MAX_RETRIES = 3

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


@dataclass
class Source:
    """A data source for enrichment"""
    name: str
    weight: float  # Usage weight (0-1)
    rate_limit: float  # Seconds between requests
    url_template: str
    enabled: bool = True


class SourceRotator:
    """
    Rotates between multiple data sources to distribute load.
    Not evasion - just smart load balancing.
    """
    
    def __init__(self):
        self.sources: List[Source] = [
            Source("bing_search", 0.30, 1.5, 
                   "https://www.bing.com/search?q={query}"),
            Source("google_search", 0.25, 2.0,
                   "https://www.google.com/search?q={query}"),
            Source("duckduckgo", 0.20, 1.5,
                   "https://html.duckduckgo.com/html/?q={query}"),
            Source("yelp_search", 0.15, 2.5,
                   "https://www.yelp.com/search?find_desc={business}&find_loc={city}%2C+{state}"),
            Source("bbb_search", 0.10, 3.0,
                   "https://www.bbb.org/search?find_text={business}&find_loc={city}%2C+{state}"),
        ]
        self.last_used: Dict[str, float] = {}
        self.stats: Dict[str, int] = {s.name: 0 for s in self.sources}
        
    def get_next_source(self) -> Optional[Source]:
        """Get next available source using weighted rotation"""
        enabled = [s for s in self.sources if s.enabled]
        if not enabled:
            return None
        
        # Filter by rate limit
        now = time.time()
        available = []
        for s in enabled:
            last = self.last_used.get(s.name, 0)
            if now - last >= s.rate_limit:
                available.append(s)
        
        if not available:
            # Wait for first available
            soonest = min(enabled, key=lambda s: self.last_used.get(s.name, 0) + s.rate_limit)
            wait = (self.last_used.get(soonest.name, 0) + soonest.rate_limit) - now
            if wait > 0:
                time.sleep(wait)
            available = [soonest]
        
        # Weighted selection
        total_weight = sum(s.weight for s in available)
        r = random.uniform(0, total_weight)
        cumsum = 0
        for s in available:
            cumsum += s.weight
            if r <= cumsum:
                self.last_used[s.name] = time.time()
                self.stats[s.name] += 1
                return s
        
        return available[0] if available else None
    
    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return self.stats.copy()


class DataExtractor:
    """Extract business data from various sources"""
    
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract phone number from text"""
        # US/Canada/Mexico formats
        patterns = [
            r'(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'([0-9]{3})[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) >= 3:
                    return f"({groups[0]}) {groups[1]}-{groups[2]}"
        return None
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email from text"""
        pattern = r'[\w\.-]+@[\w\.-]+\.\w{2,}'
        match = re.search(pattern, text)
        if match:
            email = match.group(0)
            # Filter out common false positives
            if not any(x in email.lower() for x in ['example', 'domain', 'email', 'test']):
                return email
        return None
    
    @staticmethod
    def extract_address(text: str, city: str, state: str) -> Optional[str]:
        """Extract address from text"""
        # Look for street address patterns
        lines = text.replace('\n', ' ').split(' ')
        
        for i, segment in enumerate(lines):
            segment = segment.strip()
            if len(segment) < 10:
                continue
            
            # Check for address indicators
            has_number = any(c.isdigit() for c in segment)
            has_street = any(x in segment.lower() for x in [
                'st', 'street', 'ave', 'avenue', 'blvd', 'boulevard',
                'rd', 'road', 'dr', 'drive', 'ln', 'lane', 'way',
                'calle', 'camino', 'plaza', 'suite', 'unit'
            ])
            has_zip = re.search(r'\d{5}(-\d{4})?', segment)
            
            if has_number and (has_street or has_zip):
                # Verify contains city or state
                if city.lower() in segment.lower() or state.lower() in segment.lower():
                    return segment
        
        return None


class LeadEnricher:
    """Main enrichment engine"""
    
    def __init__(self):
        self.rotator = SourceRotator()
        self.extractor = DataExtractor()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def enrich_business(self, business: str, city: str, state: str, 
                       zip_code: str, existing_data: Dict) -> Dict:
        """Enrich a single business record"""
        result = {
            "address": existing_data.get("Address", ""),
            "phone": existing_data.get("Phone", ""),
            "email": existing_data.get("Email", ""),
            "sources_used": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Skip if already complete
        if all([result["address"], result["phone"], result["email"]]):
            return result
        
        # Try multiple sources
        for attempt in range(MAX_RETRIES):
            source = self.rotator.get_next_source()
            if not source:
                time.sleep(SLEEP_MIN)
                continue
            
            try:
                # Build query
                query_parts = [p for p in [business, city, state, zip_code] if p]
                query = " ".join(query_parts)
                
                # Search
                search_url = source.url_template.format(
                    query=query.replace(' ', '+'),
                    business=business.replace(' ', '+'),
                    city=city.replace(' ', '+'),
                    state=state.replace(' ', '+')
                )
                
                resp = self.session.get(search_url, timeout=20)
                resp.raise_for_status()
                
                # Parse results
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                # Find first result link
                result_link = None
                if source.name in ['bing_search', 'google_search']:
                    for a in soup.find_all('a', href=True):
                        href = a['href']
                        if href.startswith('http') and not any(x in href for x in ['bing', 'google', 'duckduckgo']):
                            result_link = href
                            break
                
                if result_link:
                    # Visit result page
                    page_resp = self.session.get(result_link, timeout=15)
                    page_text = BeautifulSoup(page_resp.text, 'html.parser').get_text(' ', strip=True)
                    
                    # Extract data
                    if not result["address"]:
                        addr = self.extractor.extract_address(page_text, city, state)
                        if addr:
                            result["address"] = addr
                    
                    if not result["phone"]:
                        phone = self.extractor.extract_phone(page_text)
                        if phone:
                            result["phone"] = phone
                    
                    if not result["email"]:
                        email = self.extractor.extract_email(page_text)
                        if email:
                            result["email"] = email
                    
                    result["sources_used"].append(source.name)
                
                # Check if complete
                if all([result["address"], result["phone"], result["email"]]):
                    break
                
                # Random sleep
                time.sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))
                
            except Exception as e:
                print(f"    [!] {source.name} failed: {str(e)[:50]}")
                continue
        
        return result
    
    def process_file(self, filepath: str) -> str:
        """Process a single Excel file"""
        filename = os.path.basename(filepath)
        print(f"\n{'='*70}")
        print(f"Processing: {filename}")
        print(f"{'='*70}")
        
        try:
            df = pd.read_excel(filepath)
        except Exception as e:
            print(f"  [!] Could not read file: {e}")
            return ""
        
        # Validate columns
        required = ["Business Name", "City", "State", "Zip"]
        optional = ["Address", "Phone", "Email"]
        
        for col in required:
            if col not in df.columns:
                print(f"  [!] Missing required column: {col}")
                return ""
        
        # Add optional columns if missing
        for col in optional:
            if col not in df.columns:
                df[col] = ""
        
        total = len(df)
        enriched = 0
        
        for idx, row in df.iterrows():
            business = str(row.get("Business Name", "")).strip()
            city = str(row.get("City", "")).strip()
            state = str(row.get("State", "")).strip()
            zip_code = str(row.get("Zip", "")).strip()
            
            if not business or not city or not state:
                print(f"  [row {idx+1}/{total}] Skipping (missing data)")
                continue
            
            print(f"  [row {idx+1}/{total}] {business[:40]}... ", end="", flush=True)
            
            existing = {
                "Address": row.get("Address", ""),
                "Phone": row.get("Phone", ""),
                "Email": row.get("Email", "")
            }
            
            result = self.enrich_business(business, city, state, zip_code, existing)
            
            # Update dataframe
            if result["address"]:
                df.at[idx, "Address"] = result["address"]
            if result["phone"]:
                df.at[idx, "Phone"] = result["phone"]
            if result["email"]:
                df.at[idx, "Email"] = result["email"]
            
            if result["address"] or result["phone"] or result["email"]:
                enriched += 1
                print(f"✓ ({len(result['sources_used'])} sources)")
            else:
                print("✗")
        
        # Save output
        base, ext = os.path.splitext(filename)
        output_name = f"{base}{OUTPUT_SUFFIX}{ext}"
        output_path = os.path.join(os.path.dirname(filepath), output_name)
        
        try:
            df.to_excel(output_path, index=False)
            print(f"\n  [+] Saved: {output_name}")
            print(f"  [+] Enriched: {enriched}/{total} ({enriched/total*100:.1f}%)")
        except Exception as e:
            print(f"  [!] Could not save: {e}")
            return ""
        
        return output_path
    
    def process_folder(self, folder_path: str) -> List[str]:
        """Process all Excel files in folder"""
        if not os.path.isdir(folder_path):
            print(f"[!] Folder not found: {folder_path}")
            return []
        
        files = [f for f in os.listdir(folder_path) 
                if f.lower().endswith('.xlsx') and not f.endswith(f'{OUTPUT_SUFFIX}.xlsx')]
        
        if not files:
            print(f"[!] No Excel files found in {folder_path}")
            return []
        
        print(f"\nFound {len(files)} files to process")
        print(f"Sources available: {len([s for s in self.rotator.sources if s.enabled])}")
        
        results = []
        for f in files:
            full_path = os.path.join(folder_path, f)
            output = self.process_file(full_path)
            if output:
                results.append(output)
        
        return results


def main():
    """Run lead enrichment"""
    print("=" * 70)
    print("MULTI-SOURCE LEAD ENRICHMENT SYSTEM")
    print("=" * 70)
    print("\nFeatures:")
    print("  • Source rotation (search engines, directories, registries)")
    print("  • Rate limiting and respectful scraping")
    print("  • Extracts: Address, Phone, Email")
    print("  • Output: *_COMPLETED.xlsx files")
    print("\nConfiguration:")
    print(f"  • Input folder: {INPUT_FOLDER}")
    print(f"  • Sleep range: {SLEEP_MIN}-{SLEEP_MAX}s")
    print(f"  • Max retries: {MAX_RETRIES}")
    
    enricher = LeadEnricher()
    results = enricher.process_folder(INPUT_FOLDER)
    
    print("\n" + "=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)
    print(f"Files processed: {len(results)}")
    
    if results:
        print("\nSource usage stats:")
        for source, count in enricher.rotator.get_stats().items():
            print(f"  {source}: {count} requests")
    
    print("\nOutput files:")
    for r in results:
        print(f"  • {os.path.basename(r)}")


if __name__ == "__main__":
    main()
