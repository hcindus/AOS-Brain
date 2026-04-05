#!/usr/bin/env node
/**
 * YP.COM BUSINESS SCRAPER
 * Scrape Yellow Pages for business names and phone numbers
 * Build database for phone-based login system
 */

const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');

class YPBusinessScraper {
  constructor() {
    this.businesses = [];
    this.outputDir = '/root/.openclaw/workspace/data/yp_businesses';
  }

  async initBrowser() {
    console.log('[YP Scraper] Initializing browser...');
    
    this.browser = await chromium.launch({
      headless: true,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--disable-web-security'
      ]
    });

    this.context = await this.browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    });

    this.page = await this.context.newPage();
    console.log('[YP Scraper] Browser ready');
  }

  async close() {
    await this.context.close();
    await this.browser.close();
  }

  async scrapeYP(category, location, pages = 3) {
    console.log(`[YP Scraper] Searching: ${category} in ${location}`);
    
    try {
      // Navigate to Yellow Pages
      const searchUrl = `https://www.yellowpages.com/search?search_terms=${encodeURIComponent(category)}&geo_location_terms=${encodeURIComponent(location)}`;
      
      await this.page.goto(searchUrl, {
        waitUntil: 'domcontentloaded',
        timeout: 60000
      });

      // Wait for results to load
      await this.page.waitForTimeout(3000);

      for (let pageNum = 1; pageNum <= pages; pageNum++) {
        console.log(`  Processing page ${pageNum}...`);
        
        // Extract business data
        const businesses = await this.page.evaluate(() => {
          const results = [];
          const listings = document.querySelectorAll('.result, .organic, .listing');
          
          listings.forEach(listing => {
            try {
              const nameEl = listing.querySelector('.business-name, .name, h2 a, .listing-name');
              const phoneEl = listing.querySelector('.phone, .phones, [data-phone]');
              const addressEl = listing.querySelector('.street-address, .address');
              const cityEl = listing.querySelector('.locality, .city');
              const categoryEl = listing.querySelector('.categories, .category');
              
              if (nameEl && phoneEl) {
                const phone = phoneEl.textContent.replace(/\D/g, ''); // Extract digits only
                if (phone.length >= 10) { // Valid phone number
                  results.push({
                    business_name: nameEl.textContent.trim(),
                    phone: phone,
                    phone_formatted: phoneEl.textContent.trim(),
                    address: addressEl ? addressEl.textContent.trim() : '',
                    city: cityEl ? cityEl.textContent.trim() : '',
                    category: categoryEl ? categoryEl.textContent.trim() : '',
                    source: 'yellowpages.com',
                    scraped_at: new Date().toISOString()
                  });
                }
              }
            } catch (e) {}
          });
          
          return results;
        });

        businesses.forEach(b => this.businesses.push(b));
        console.log(`    Found ${businesses.length} businesses`);

        // Try to go to next page
        if (pageNum < pages) {
          try {
            const nextBtn = await this.page.$('a.next, .pagination a:last-child');
            if (nextBtn) {
              await nextBtn.click();
              await this.page.waitForTimeout(3000);
            } else {
              break;
            }
          } catch (e) {
            break;
          }
        }
      }
      
    } catch (error) {
      console.log(`  Error: ${error.message}`);
    }
  }

  async scrapeAlternative(category, location) {
    console.log(`[YP Scraper] Trying alternative source...`);
    
    // Try superpages.com as backup
    try {
      await this.page.goto(
        `https://www.superpages.com/listings/search?c=${encodeURIComponent(category)}&l=${encodeURIComponent(location)}`,
        { waitUntil: 'domcontentloaded', timeout: 30000 }
      );
      
      await this.page.waitForTimeout(3000);
      
      const businesses = await this.page.evaluate(() => {
        const results = [];
        document.querySelectorAll('.listing').forEach(listing => {
          const name = listing.querySelector('.name, h2');
          const phone = listing.querySelector('.phone');
          
          if (name && phone) {
            const phoneDigits = phone.textContent.replace(/\D/g, '');
            if (phoneDigits.length >= 10) {
              results.push({
                business_name: name.textContent.trim(),
                phone: phoneDigits,
                source: 'superpages.com',
                scraped_at: new Date().toISOString()
              });
            }
          }
        });
        return results;
      });
      
      businesses.forEach(b => this.businesses.push(b));
      console.log(`  Found ${businesses.length} from alternative source`);
      
    } catch (e) {
      console.log(`  Alternative source failed: ${e.message}`);
    }
  }

  async saveDatabase() {
    if (this.businesses.length === 0) {
      console.log('No businesses to save');
      return;
    }

    await fs.mkdir(this.outputDir, { recursive: true });

    // Save as JSON
    const timestamp = new Date().toISOString().slice(0, 10);
    const jsonFile = path.join(this.outputDir, `businesses_${timestamp}.json`);
    await fs.writeFile(jsonFile, JSON.stringify(this.businesses, null, 2));

    // Save as CSV
    const csvFile = path.join(this.outputDir, `businesses_${timestamp}.csv`);
    const csvHeader = 'business_name,phone,phone_formatted,address,city,category,source,scraped_at\n';
    const csvRows = this.businesses.map(b => 
      `"${b.business_name}","${b.phone}","${b.phone_formatted}","${b.address}","${b.city}","${b.category}","${b.source}","${b.scraped_at}"`
    ).join('\n');
    await fs.writeFile(csvFile, csvHeader + csvRows);

    // Update master database
    const masterFile = path.join(this.outputDir, 'business_database.json');
    let existing = [];
    try {
      const data = await fs.readFile(masterFile, 'utf8');
      existing = JSON.parse(data);
    } catch {}

    // Merge and deduplicate by phone
    const phoneMap = new Map();
    existing.forEach(b => phoneMap.set(b.phone, b));
    this.businesses.forEach(b => phoneMap.set(b.phone, b));
    
    const merged = Array.from(phoneMap.values());
    await fs.writeFile(masterFile, JSON.stringify(merged, null, 2));

    console.log(`\n💾 Database updated:`);
    console.log(`  - JSON: ${path.basename(jsonFile)}`);
    console.log(`  - CSV: ${path.basename(csvFile)}`);
    console.log(`  - Master DB: ${merged.length} unique businesses`);
  }

  report() {
    console.log('\n' + '='.repeat(70));
    console.log('📊 YP.COM SCRAPING REPORT');
    console.log('='.repeat(70));
    console.log(`Total businesses: ${this.businesses.length}`);
    
    // Group by source
    const bySource = {};
    this.businesses.forEach(b => {
      bySource[b.source] = (bySource[b.source] || 0) + 1;
    });

    console.log('\nBy Source:');
    Object.entries(bySource).forEach(([src, count]) => {
      console.log(`  ${src}: ${count}`);
    });

    // Sample
    console.log('\nSample:');
    this.businesses.slice(0, 5).forEach(b => {
      console.log(`  • ${b.business_name.substring(0, 40)} - ${b.phone_formatted}`);
    });

    console.log('='.repeat(70));
  }
}

async function main() {
  console.log('='.repeat(70));
  console.log('📞 YP.COM BUSINESS SCRAPER');
  console.log('Building phone-based login database');
  console.log('='.repeat(70));
  console.log();

  const scraper = new YPBusinessScraper();

  try {
    await scraper.initBrowser();

    // Scrape multiple categories
    const categories = [
      { cat: 'restaurants', loc: 'Los Angeles, CA', pages: 3 },
      { cat: 'auto repair', loc: 'Los Angeles, CA', pages: 2 },
      { cat: 'plumbers', loc: 'Los Angeles, CA', pages: 2 },
      { cat: 'electricians', loc: 'Los Angeles, CA', pages: 2 },
      { cat: 'doctors', loc: 'Los Angeles, CA', pages: 2 },
    ];

    for (const { cat, loc, pages } of categories) {
      await scraper.scrapeYP(cat, loc, pages);
    }

    // Try alternative sources
    await scraper.scrapeAlternative('retail', 'Los Angeles, CA');

    await scraper.saveDatabase();
    scraper.report();

  } finally {
    await scraper.close();
  }

  console.log('\n✅ Scraping complete!');
  console.log('Database ready for phone-based login system');
}

main().catch(console.error);
