#!/usr/bin/env python3
"""
Lead Enrichment Pipeline for California Leads
Performance Supply Depot LLC

This pipeline enriches lead data by querying multiple APIs to fill missing:
- Email addresses
- Phone numbers  
- Contact/Owner names

Supports resume capability and rate limiting to avoid API blocks.
"""

import os
import sys
import json
import time
import logging
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enrichment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
LEADS_DIR = Path('/root/.openclaw/workspace/aocros/performance_supply_depot/leads/')
OUTPUT_DIR = Path('/root/.openclaw/workspace/aocros/performance_supply_depot/leads/enriched/')
PROGRESS_FILE = Path('enrichment_progress.json')
RATE_LIMIT_DELAY = 1.0  # Seconds between API calls
MAX_RETRIES = 3

# API Keys from environment
HUNTER_API_KEY = os.getenv('HUNTER_API_KEY', '')
CLEARBIT_API_KEY = os.getenv('CLEARBIT_API_KEY', '')
BRAVE_API_KEY = os.getenv('BRAVE_API_KEY', '')
SERPER_API_KEY = os.getenv('SERPER_API_KEY', '')


@dataclass
class EnrichmentResult:
    """Result of enriching a single lead"""
    business_name: str
    email_found: Optional[str] = None
    phone_found: Optional[str] = None
    contact_name_found: Optional[str] = None
    source: str = ""
    confidence: str = "low"
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class LeadEnricher:
    """Main enrichment engine with multiple API sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PerformanceSupplyDepot-LeadEnricher/1.0'
        })
        self.stats = {
            'total_processed': 0,
            'emails_found': 0,
            'phones_found': 0,
            'contacts_found': 0,
            'api_calls': 0,
            'errors': 0
        }
        
    def _rate_limit(self):
        """Apply rate limiting between API calls"""
        time.sleep(RATE_LIMIT_DELAY)
        
    def _make_request(self, url: str, headers: Dict = None, params: Dict = None, 
                      method: str = 'GET', json_data: Dict = None) -> Optional[Dict]:
        """Make HTTP request with retries"""
        for attempt in range(MAX_RETRIES):
            try:
                self._rate_limit()
                self.stats['api_calls'] += 1
                
                if method == 'GET':
                    response = self.session.get(url, headers=headers, params=params, timeout=30)
                else:
                    response = self.session.post(url, headers=headers, json=json_data, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    logger.warning(f"Rate limited on {url}, backing off...")
                    time.sleep(5 * (attempt + 1))
                else:
                    logger.warning(f"API error {response.status_code} for {url}")
                    
            except Exception as e:
                logger.error(f"Request error (attempt {attempt + 1}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    
        self.stats['errors'] += 1
        return None
    
    # ==================== HUNTER.IO ====================
    def enrich_with_hunter(self, business_name: str, domain: str = None) -> EnrichmentResult:
        """Use Hunter.io to find email addresses"""
        result = EnrichmentResult(business_name=business_name, source="hunter.io")
        
        if not HUNTER_API_KEY:
            logger.debug("Hunter API key not configured")
            return result
            
        # Try domain search if we have a domain
        if domain:
            url = "https://api.hunter.io/v2/domain-search"
            params = {
                'domain': domain,
                'api_key': HUNTER_API_KEY,
                'limit': 5
            }
            
            data = self._make_request(url, params=params)
            if data and 'data' in data:
                emails = data['data'].get('emails', [])
                if emails:
                    # Get the most confident email
                    best_email = max(emails, key=lambda x: x.get('confidence', 0))
                    result.email_found = best_email.get('value')
                    result.confidence = f"{best_email.get('confidence', 0)}%"
                    if best_email.get('first_name') and best_email.get('last_name'):
                        result.contact_name_found = f"{best_email['first_name']} {best_email['last_name']}"
                        
        # Try email finder with business name
        if not result.email_found:
            # Try to guess common patterns
            guessed_domains = self._guess_domains(business_name)
            for guessed_domain in guessed_domains[:2]:
                url = "https://api.hunter.io/v2/domain-search"
                params = {
                    'domain': guessed_domain,
                    'api_key': HUNTER_API_KEY,
                    'limit': 3
                }
                data = self._make_request(url, params=params)
                if data and 'data' in data and data['data'].get('emails'):
                    emails = data['data']['emails']
                    best_email = max(emails, key=lambda x: x.get('confidence', 0))
                    result.email_found = best_email.get('value')
                    result.confidence = f"{best_email.get('confidence', 0)}%"
                    break
                    
        return result
    
    # ==================== CLEARBIT ====================
    def enrich_with_clearbit(self, business_name: str, domain: str = None) -> EnrichmentResult:
        """Use Clearbit to enrich company data"""
        result = EnrichmentResult(business_name=business_name, source="clearbit")
        
        if not CLEARBIT_API_KEY:
            logger.debug("Clearbit API key not configured")
            return result
            
        headers = {'Authorization': f'Bearer {CLEARBIT_API_KEY}'}
        
        # Try domain lookup
        if domain:
            url = f"https://company.clearbit.com/v2/companies/find"
            params = {'domain': domain}
            data = self._make_request(url, headers=headers, params=params)
            
            if data:
                result.contact_name_found = data.get('name')
                if data.get('site', {}).get('phoneNumbers'):
                    result.phone_found = data['site']['phoneNumbers'][0]
                result.confidence = "medium"
                
        # Try name search
        if not result.contact_name_found:
            url = "https://company.clearbit.com/v1/companies/suggest"
            params = {'query': business_name, 'limit': 5}
            data = self._make_request(url, headers=headers, params=params)
            
            if data and len(data) > 0:
                company = data[0]
                result.contact_name_found = company.get('name')
                if company.get('domain'):
                    # Now get full details
                    detail_url = f"https://company.clearbit.com/v2/companies/find"
                    detail_data = self._make_request(
                        detail_url, 
                        headers=headers, 
                        params={'domain': company['domain']}
                    )
                    if detail_data and detail_data.get('site', {}).get('phoneNumbers'):
                        result.phone_found = detail_data['site']['phoneNumbers'][0]
                result.confidence = "medium"
                
        return result
    
    # ==================== BRAVE SEARCH ====================
    def enrich_with_brave(self, business_name: str, city: str = None, state: str = None) -> EnrichmentResult:
        """Use Brave Search API to find contact info"""
        result = EnrichmentResult(business_name=business_name, source="brave")
        
        if not BRAVE_API_KEY:
            logger.debug("Brave API key not configured")
            return result
            
        headers = {'X-Subscription-Token': BRAVE_API_KEY}
        
        # Search for business contact info
        location = f"{city}, {state}" if city and state else "California"
        query = f'"{business_name}" {location} contact email phone'
        
        url = "https://api.search.brave.com/res/v1/web/search"
        params = {
            'q': query,
            'count': 10,
            'offset': 0
        }
        
        data = self._make_request(url, headers=headers, params=params)
        
        if data and 'web' in data and 'results' in data['web']:
            for web_result in data['web']['results']:
                description = web_result.get('description', '')
                
                # Extract email from description
                if not result.email_found:
                    result.email_found = self._extract_email(description)
                    
                # Extract phone from description
                if not result.phone_found:
                    result.phone_found = self._extract_phone(description)
                    
                if result.email_found or result.phone_found:
                    result.confidence = "low"
                    break
                    
        return result
    
    # ==================== SERPER (Google Search) ====================
    def enrich_with_serper(self, business_name: str, city: str = None, state: str = None) -> EnrichmentResult:
        """Use Serper.dev (Google Search API) to find contact info"""
        result = EnrichmentResult(business_name=business_name, source="serper")
        
        if not SERPER_API_KEY:
            logger.debug("Serper API key not configured")
            return result
            
        location = f"{city}, {state}" if city and state else "California"
        query = f'"{business_name}" {location} contact information'
        
        url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        payload = {
            'q': query,
            'num': 10
        }
        
        data = self._make_request(url, headers=headers, json_data=payload, method='POST')
        
        if data:
            # Check organic results
            for organic in data.get('organic', []):
                snippet = organic.get('snippet', '')
                
                if not result.email_found:
                    result.email_found = self._extract_email(snippet)
                if not result.phone_found:
                    result.phone_found = self._extract_phone(snippet)
                    
            # Check knowledge graph if available
            kg = data.get('knowledgeGraph', {})
            if kg:
                if not result.contact_name_found:
                    result.contact_name_found = kg.get('title')
                if not result.phone_found:
                    result.phone_found = kg.get('phone')
                    
        return result
    
    # ==================== FREE/LOCAL SOURCES ====================
    def enrich_with_patterns(self, business_name: str, city: str = None) -> EnrichmentResult:
        """Use pattern matching and local heuristics"""
        result = EnrichmentResult(business_name=business_name, source="pattern_match")
        
        # Clean business name
        clean_name = business_name.lower().replace("'", "").replace("&", "and")
        words = clean_name.split()
        
        # Generate potential domains
        domains = self._guess_domains(business_name)
        
        # Generate potential emails based on common patterns
        if len(words) >= 2:
            first_word = words[0]
            last_word = words[-1]
            
            # Common email patterns
            for domain in domains[:2]:
                patterns = [
                    f"info@{domain}",
                    f"contact@{domain}",
                    f"hello@{domain}",
                    f"support@{domain}",
                    f"sales@{domain}",
                ]
                # We can't verify without API, but we can suggest
                if not result.email_found:
                    result.email_found = f"info@{domain}"
                    result.confidence = "very_low"
                    
        return result
    
    # ==================== HELPER METHODS ====================
    def _guess_domains(self, business_name: str) -> List[str]:
        """Generate likely domain names from business name"""
        domains = []
        clean = business_name.lower().replace("'", "").replace("&", "and")
        words = clean.split()
        
        # Common patterns
        if len(words) >= 1:
            # First word + .com
            domains.append(f"{words[0]}.com")
            
        if len(words) >= 2:
            # First + last word
            domains.append(f"{words[0]}{words[-1]}.com")
            domains.append(f"{words[0]}-{words[-1]}.com")
            
        # Full name variations
        no_spaces = clean.replace(" ", "").replace(".", "").replace(",", "")
        domains.append(f"{no_spaces}.com")
        domains.append(f"{no_spaces.replace(' ', '-')}.com")
        
        return list(set(domains))
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email from text using regex"""
        import re
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract US phone number from text"""
        import re
        # Various phone patterns
        patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (555) 123-4567 or 555-123-4567
            r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1 (555) 123-4567
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                phone = match.group(0)
                # Normalize to (XXX) XXX-XXXX
                digits = re.sub(r'\D', '', phone)
                if len(digits) == 10:
                    return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
                elif len(digits) == 11 and digits[0] == '1':
                    return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        return None
    
    def enrich_lead(self, row: pd.Series) -> EnrichmentResult:
        """Enrich a single lead using all available sources"""
        business_name = row.get('Business Name', '')
        city = row.get('City', '')
        state = row.get('State', '')
        
        if not business_name:
            return EnrichmentResult(business_name="", source="none")
            
        logger.info(f"Enriching: {business_name}")
        
        # Try sources in order of preference
        result = None
        
        # 1. Try Hunter.io for emails
        if not result or (not result.email_found and not result.contact_name_found):
            try:
                hunter_result = self.enrich_with_hunter(business_name)
                if hunter_result.email_found or hunter_result.contact_name_found:
                    result = hunter_result
            except Exception as e:
                logger.error(f"Hunter error: {e}")
                
        # 2. Try Clearbit for company data
        if not result or (not result.contact_name_found and not result.phone_found):
            try:
                clearbit_result = self.enrich_with_clearbit(business_name)
                if clearbit_result.contact_name_found or clearbit_result.phone_found:
                    if result:
                        # Merge results
                        if not result.contact_name_found:
                            result.contact_name_found = clearbit_result.contact_name_found
                        if not result.phone_found:
                            result.phone_found = clearbit_result.phone_found
                        result.source += ",clearbit"
                    else:
                        result = clearbit_result
            except Exception as e:
                logger.error(f"Clearbit error: {e}")
                
        # 3. Try Brave Search
        if not result or (not result.email_found and not result.phone_found):
            try:
                brave_result = self.enrich_with_brave(business_name, city, state)
                if brave_result.email_found or brave_result.phone_found:
                    if result:
                        if not result.email_found:
                            result.email_found = brave_result.email_found
                        if not result.phone_found:
                            result.phone_found = brave_result.phone_found
                        result.source += ",brave"
                    else:
                        result = brave_result
            except Exception as e:
                logger.error(f"Brave error: {e}")
                
        # 4. Try Serper
        if not result or (not result.email_found and not result.phone_found):
            try:
                serper_result = self.enrich_with_serper(business_name, city, state)
                if serper_result.email_found or serper_result.phone_found:
                    if result:
                        if not result.email_found:
                            result.email_found = serper_result.email_found
                        if not result.phone_found:
                            result.phone_found = serper_result.phone_found
                        result.source += ",serper"
                    else:
                        result = serper_result
            except Exception as e:
                logger.error(f"Serper error: {e}")
                
        # 5. Fallback to pattern matching
        if not result:
            result = self.enrich_with_patterns(business_name, city)
            
        # Update stats
        self.stats['total_processed'] += 1
        if result.email_found:
            self.stats['emails_found'] += 1
        if result.phone_found:
            self.stats['phones_found'] += 1
        if result.contact_name_found:
            self.stats['contacts_found'] += 1
            
        return result


def load_progress() -> Dict:
    """Load progress from file to enable resume"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'completed_files': [], 'completed_leads': []}


def save_progress(progress: Dict):
    """Save progress to file"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def process_county_file(filepath: Path, enricher: LeadEnricher, progress: Dict) -> pd.DataFrame:
    """Process a single county file"""
    filename = filepath.name
    logger.info(f"Processing {filename}...")
    
    # Read file
    df = pd.read_excel(filepath)
    
    # Add enrichment columns if they don't exist
    for col in ['Enriched_Email', 'Enriched_Phone', 'Enriched_Contact', 'Enrichment_Source', 'Enrichment_Date']:
        if col not in df.columns:
            df[col] = None
            
    # Process each row
    for idx, row in df.iterrows():
        business_name = row.get('Business Name', '')
        
        # Skip if already enriched
        lead_id = f"{filename}:{business_name}"
        if lead_id in progress['completed_leads']:
            logger.debug(f"Skipping already enriched: {business_name}")
            continue
            
        # Skip if already has all data
        if (pd.notna(row.get('Email')) and pd.notna(row.get('Phone')) and 
            pd.notna(row.get('Owner Name'))):
            progress['completed_leads'].append(lead_id)
            continue
            
        # Enrich the lead
        result = enricher.enrich_lead(row)
        
        # Update dataframe
        if result.email_found and pd.isna(row.get('Email')):
            df.at[idx, 'Enriched_Email'] = result.email_found
        if result.phone_found and pd.isna(row.get('Phone')):
            df.at[idx, 'Enriched_Phone'] = result.phone_found
        if result.contact_name_found and pd.isna(row.get('Owner Name')):
            df.at[idx, 'Enriched_Contact'] = result.contact_name_found
            
        df.at[idx, 'Enrichment_Source'] = result.source
        df.at[idx, 'Enrichment_Date'] = result.timestamp
        
        # Mark as completed
        progress['completed_leads'].append(lead_id)
        
        # Save progress every 10 leads
        if len(progress['completed_leads']) % 10 == 0:
            save_progress(progress)
            
    return df


def generate_report(all_data: List[pd.DataFrame], enricher: LeadEnricher, output_path: Path):
    """Generate enrichment report"""
    
    # Combine all data
    combined = pd.concat(all_data, ignore_index=True)
    
    # Calculate statistics
    total_leads = len(combined)
    original_emails = combined['Email'].notna().sum()
    original_phones = combined['Phone'].notna().sum()
    original_contacts = combined['Owner Name'].notna().sum()
    
    enriched_emails = combined['Enriched_Email'].notna().sum()
    enriched_phones = combined['Enriched_Phone'].notna().sum()
    enriched_contacts = combined['Enriched_Contact'].notna().sum()
    
    final_emails = original_emails + enriched_emails
    final_phones = original_phones + enriched_phones
    final_contacts = original_contacts + enriched_contacts
    
    email_rate_before = (original_emails / total_leads) * 100 if total_leads > 0 else 0
    email_rate_after = (final_emails / total_leads) * 100 if total_leads > 0 else 0
    phone_rate_before = (original_phones / total_leads) * 100 if total_leads > 0 else 0
    phone_rate_after = (final_phones / total_leads) * 100 if total_leads > 0 else 0
    contact_rate_before = (original_contacts / total_leads) * 100 if total_leads > 0 else 0
    contact_rate_after = (final_contacts / total_leads) * 100 if total_leads > 0 else 0
    
    report = f"""# Lead Enrichment Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total Leads | {total_leads} | {total_leads} | - |
| Emails | {original_emails} ({email_rate_before:.1f}%) | {final_emails} ({email_rate_after:.1f}%) | +{enriched_emails} |
| Phones | {original_phones} ({phone_rate_before:.1f}%) | {final_phones} ({phone_rate_after:.1f}%) | +{enriched_phones} |
| Contacts | {original_contacts} ({contact_rate_before:.1f}%) | {final_contacts} ({contact_rate_after:.1f}%) | +{enriched_contacts} |

## API Usage

- Total API Calls: {enricher.stats['api_calls']}
- Errors Encountered: {enricher.stats['errors']}

## Data Sources Used

- Hunter.io: Email discovery
- Clearbit: Company data enrichment
- Brave Search: Web search for contact info
- Serper.dev: Google search results
- Pattern Matching: Domain guessing and pattern-based inference

## Completion Rates by County

"""
    
    # Add per-county stats
    for df in all_data:
        if len(df) > 0:
            county = df['County'].iloc[0] if 'County' in df.columns else 'Unknown'
            total = len(df)
            emails = (df['Email'].notna().sum() + df['Enriched_Email'].notna().sum())
            phones = (df['Phone'].notna().sum() + df['Enriched_Phone'].notna().sum())
            contacts = (df['Owner Name'].notna().sum() + df['Enriched_Contact'].notna().sum())
            report += f"- **{county}**: {total} leads | Email: {emails}/{total} | Phone: {phones}/{total} | Contact: {contacts}/{total}\n"
    
    report += f"""
## Notes

- Enrichment confidence levels vary by source
- Pattern-matched emails should be verified before use
- API rate limits may have affected enrichment coverage
- Resume capability allows re-running without duplicating work

## Output Files

Enriched files saved to: `{OUTPUT_DIR}`
"""
    
    with open(output_path, 'w') as f:
        f.write(report)
        
    logger.info(f"Report saved to {output_path}")


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("Lead Enrichment Pipeline Starting")
    logger.info("=" * 60)
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Load progress
    progress = load_progress()
    logger.info(f"Loaded progress: {len(progress['completed_files'])} files, {len(progress['completed_leads'])} leads already processed")
    
    # Initialize enricher
    enricher = LeadEnricher()
    
    # Find all CA county files
    ca_files = sorted([f for f in LEADS_DIR.glob('CA_*_County_Leads.xlsx') 
                      if 'All' not in f.name and 'Priority' not in f.name])
    
    logger.info(f"Found {len(ca_files)} CA county files to process")
    
    all_enriched_data = []
    
    # Process each file
    for filepath in ca_files:
        if filepath.name in progress['completed_files']:
            logger.info(f"Skipping already completed file: {filepath.name}")
            # Still load for report
            df = pd.read_excel(filepath)
            all_enriched_data.append(df)
            continue
            
        try:
            enriched_df = process_county_file(filepath, enricher, progress)
            
            # Save enriched file
            output_path = OUTPUT_DIR / f"enriched_{filepath.name}"
            enriched_df.to_excel(output_path, index=False)
            logger.info(f"Saved enriched file: {output_path}")
            
            all_enriched_data.append(enriched_df)
            progress['completed_files'].append(filepath.name)
            save_progress(progress)
            
        except Exception as e:
            logger.error(f"Error processing {filepath.name}: {e}")
            continue
    
    # Generate report
    report_path = OUTPUT_DIR / 'enrichment_report.md'
    generate_report(all_enriched_data, enricher, report_path)
    
    # Also save a copy in the main directory
    generate_report(all_enriched_data, enricher, Path('enrichment_report.md'))
    
    logger.info("=" * 60)
    logger.info("Enrichment Complete!")
    logger.info(f"Total processed: {enricher.stats['total_processed']}")
    logger.info(f"Emails found: {enricher.stats['emails_found']}")
    logger.info(f"Phones found: {enricher.stats['phones_found']}")
    logger.info(f"Contacts found: {enricher.stats['contacts_found']}")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
