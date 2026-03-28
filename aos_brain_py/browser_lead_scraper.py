#!/usr/bin/env python3
"""
BROWSER LEAD SCRAPER
Use Playwright browser automation for lead generation
Helps scraping team gather leads from JavaScript-heavy sites
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime
from pathlib import Path

class BrowserLeadScraper:
    """Browser-based lead scraper using Playwright."""
    
    def __init__(self):
        self.leads = []
        self.output_dir = Path("/root/.openclaw/workspace/data/leads")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def init_browser(self):
        """Initialize browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await self.context.new_page()
    
    async def close(self):
        """Close browser."""
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
    
    async def scrape_opencorporates(self, query="technology", location="california"):
        """Scrape OpenCorporates for leads."""
        print(f"🔍 Scraping OpenCorporates: {query} in {location}")
        
        try:
            await self.page.goto(
                f"https://opencorporates.com/companies?jurisdiction_code=us_{location}&q={query}",
                wait_until='networkidle',
                timeout=60000
            )
            
            # Wait for results
            await self.page.wait_for_selector('.company-result', timeout=10000)
            
            # Extract companies
            companies = await self.page.query_selector_all('.company-result')
            
            for company in companies[:20]:  # Top 20
                try:
                    name_elem = await company.query_selector('.company-name a')
                    name = await name_elem.inner_text() if name_elem else "Unknown"
                    
                    link_elem = await company.query_selector('.company-name a')
                    link = await link_elem.get_attribute('href') if link_elem else ""
                    
                    status_elem = await company.query_selector('.company-status')
                    status = await status_elem.inner_text() if status_elem else "Unknown"
                    
                    # Check if active
                    if 'active' in status.lower():
                        self.leads.append({
                            'company_name': name.strip(),
                            'source': 'OpenCorporates',
                            'url': f"https://opencorporates.com{link}",
                            'status': status.strip(),
                            'location': location,
                            'query': query,
                            'scraped_at': datetime.now().isoformat(),
                            'priority': 'MEDIUM'
                        })
                except Exception as e:
                    print(f"  ⚠️  Error extracting company: {e}")
                    continue
            
            print(f"  ✅ Found {len(self.leads)} leads")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    async def scrape_yelp_businesses(self, category="technology", location="Los Angeles, CA"):
        """Scrape Yelp for business leads."""
        print(f"🔍 Scraping Yelp: {category} in {location}")
        
        try:
            # Note: Yelp has strong anti-bot, this is for demonstration
            await self.page.goto(
                f"https://www.yelp.com/search?find_desc={category}&find_loc={location.replace(' ', '+')}",
                wait_until='domcontentloaded',
                timeout=30000
            )
            
            # Wait for results with delay
            await asyncio.sleep(3)
            
            # Extract businesses
            businesses = await self.page.query_selector_all('[data-testid="serp-ia-card"]')
            
            for biz in businesses[:10]:
                try:
                    name_elem = await biz.query_selector('h3 a')
                    name = await name_elem.inner_text() if name_elem else "Unknown"
                    
                    self.leads.append({
                        'company_name': name.strip(),
                        'source': 'Yelp',
                        'category': category,
                        'location': location,
                        'scraped_at': datetime.now().isoformat(),
                        'priority': 'MEDIUM'
                    })
                except:
                    continue
            
            print(f"  ✅ Found {len(self.leads)} leads")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    async def scrape_linkedin_search(self, industry="technology", company_size="11-50"):
        """Scrape LinkedIn for company leads."""
        print(f"🔍 Scraping LinkedIn: {industry} companies ({company_size} employees)")
        
        try:
            # LinkedIn requires login, this is a placeholder
            print("  ℹ️  LinkedIn requires authentication - skipping")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    def save_leads(self):
        """Save leads to JSON."""
        if not self.leads:
            print("No leads to save")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.output_dir / f"browser_leads_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.leads, f, indent=2)
        
        print(f"\n💾 Saved {len(self.leads)} leads to {output_file.name}")
        
        # Also save to master leads file
        master_file = self.output_dir / "all_browser_leads.json"
        
        existing = []
        if master_file.exists():
            with open(master_file) as f:
                existing = json.load(f)
        
        existing.extend(self.leads)
        
        with open(master_file, 'w') as f:
            json.dump(existing, f, indent=2)
        
        print(f"💾 Total in master file: {len(existing)} leads")
    
    def report(self):
        """Generate report."""
        print("\n" + "=" * 70)
        print("📊 BROWSER LEAD SCRAPING REPORT")
        print("=" * 70)
        print(f"Total leads gathered: {len(self.leads)}")
        print()
        
        # Group by source
        by_source = {}
        for lead in self.leads:
            src = lead.get('source', 'Unknown')
            by_source[src] = by_source.get(src, 0) + 1
        
        print("By Source:")
        for source, count in by_source.items():
            print(f"  {source}: {count} leads")
        
        print("\nSample Leads:")
        for lead in self.leads[:5]:
            print(f"  • {lead['company_name'][:40]} ({lead['source']})")
        
        print("=" * 70)


async def main():
    """Run browser scraper."""
    print("=" * 70)
    print("🌐 BROWSER LEAD SCRAPER - DEPLOYING")
    print("Using Playwright for JavaScript-rendered sites")
    print("=" * 70)
    print()
    
    scraper = BrowserLeadScraper()
    
    try:
        await scraper.init_browser()
        
        # Scrape multiple sources
        await scraper.scrape_opencorporates("technology", "california")
        await scraper.scrape_opencorporates("software", "california")
        await scraper.scrape_opencorporates("restaurant", "california")
        
        # Save results
        scraper.save_leads()
        scraper.report()
        
    finally:
        await scraper.close()
    
    print("\n✅ Browser scraping complete!")


if __name__ == "__main__":
    asyncio.run(main())
