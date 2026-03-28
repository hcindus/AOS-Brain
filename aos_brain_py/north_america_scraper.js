#!/usr/bin/env node
/**
 * NORTH AMERICA BUSINESS SCRAPER
 * Multi-country: USA, Canada, Mexico
 * Sources: Yellow Pages (US), YellowPages.ca (Canada), Seccion Amarilla (Mexico)
 */

const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');

class NorthAmericaScraper {
  constructor() {
    this.businesses = [];
    this.outputDir = '/root/.openclaw/workspace/data/north_america_businesses';
    this.stats = {
      usa: 0,
      canada: 0,
      mexico: 0
    };
  }

  async initBrowser() {
    console.log('[NorthAmerica Scraper] Initializing browser...');
    this.browser = await chromium.launch({
      headless: true,
      args: ['--disable-blink-features=AutomationControlled']
    });
    this.context = await this.browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    });
    this.page = await this.context.newPage();
    console.log('[NorthAmerica Scraper] Browser ready');
  }

  async close() {
    await this.context.close();
    await this.browser.close();
  }

  // USA - Yellowpages.com
  async scrapeUSA(city, state, category, pages = 5) {
    console.log(`[USA] ${category} in ${city}, ${state}`);
    
    try {
      const location = `${city}, ${state}`;
      const searchUrl = `https://www.yellowpages.com/search?search_terms=${encodeURIComponent(category)}&geo_location_terms=${encodeURIComponent(location)}`;
      
      await this.page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await this.page.waitForTimeout(3000);

      for (let i = 0; i < pages; i++) {
        const businesses = await this.page.evaluate(() => {
          const results = [];
          document.querySelectorAll('.result, .organic, .listing').forEach(el => {
            const nameEl = el.querySelector('.business-name a, .name');
            const phoneEl = el.querySelector('.phone');
            const addrEl = el.querySelector('.street-address');
            const cityEl = el.querySelector('.locality');
            
            if (nameEl && phoneEl) {
              const phone = phoneEl.textContent.replace(/\D/g, '');
              if (phone.length === 10) {
                results.push({
                  name: nameEl.textContent.trim(),
                  phone: `+1${phone}`,
                  phone_formatted: phoneEl.textContent.trim(),
                  address: addrEl ? addrEl.textContent.trim() : '',
                  city: cityEl ? cityEl.textContent.trim().split(',')[0] : '',
                  country: 'USA',
                  source: 'yellowpages.com'
                });
              }
            }
          });
          return results;
        });

        businesses.forEach(b => {
          this.businesses.push({
            business_name: b.name,
            phone: b.phone,
            phone_formatted: b.phone_formatted,
            address: b.address,
            city: b.city,
            state: state,
            category: category,
            country: 'USA',
            country_code: 'US',
            source: b.source,
            scraped_at: new Date().toISOString()
          });
        });

        this.stats.usa += businesses.length;
        console.log(`  Page ${i+1}: ${businesses.length} businesses`);

        // Next page
        if (i < pages - 1) {
          try {
            const nextBtn = await this.page.$('a.next');
            if (nextBtn) {
              await nextBtn.click();
              await this.page.waitForTimeout(3000);
            }
          } catch (e) { break; }
        }
      }
    } catch (error) {
      console.log(`  Error: ${error.message}`);
    }
  }

  // Canada - YellowPages.ca
  async scrapeCanada(city, province, category, pages = 5) {
    console.log(`[Canada] ${category} in ${city}, ${province}`);
    
    try {
      const searchUrl = `https://www.yellowpages.ca/search/si/${pages}/${category}/${city}+${province}`;
      
      await this.page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await this.page.waitForTimeout(3000);

      const businesses = await this.page.evaluate(() => {
        const results = [];
        document.querySelectorAll('.listing, .result').forEach(el => {
          const nameEl = el.querySelector('.listing__name a, .name');
          const phoneEl = el.querySelector('.listing__phone, .phone');
          
          if (nameEl && phoneEl) {
            const phone = phoneEl.textContent.replace(/\D/g, '');
            if (phone.length === 10) {
              results.push({
                name: nameEl.textContent.trim(),
                phone: `+1${phone}`,
                source: 'yellowpages.ca'
              });
            }
          }
        });
        return results;
      });

      businesses.forEach(b => {
        this.businesses.push({
          business_name: b.name,
          phone: b.phone,
          country: 'Canada',
          country_code: 'CA',
          category: category,
          city: city,
          province: province,
          source: b.source,
          scraped_at: new Date().toISOString()
        });
      });

      this.stats.canada += businesses.length;
      console.log(`  Found ${businesses.length} businesses`);

    } catch (error) {
      console.log(`  Error: ${error.message}`);
    }
  }

  // Mexico - Seccion Amarilla
  async scrapeMexico(city, category, pages = 3) {
    console.log(`[Mexico] ${category} in ${city}`);
    
    try {
      // Seccion Amarilla uses different structure
      const searchUrl = `https://www.seccionamarilla.com.mx/resultados/${category}/${city}`;
      
      await this.page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await this.page.waitForTimeout(3000);

      const businesses = await this.page.evaluate(() => {
        const results = [];
        document.querySelectorAll('.listing, .resultado').forEach(el => {
          const nameEl = el.querySelector('.nombre, .title');
          const phoneEl = el.querySelector('.telefono, .phone');
          
          if (nameEl && phoneEl) {
            const phone = phoneEl.textContent.replace(/\D/g, '');
            if (phone.length >= 10) {
              results.push({
                name: nameEl.textContent.trim(),
                phone: `+52${phone}`,
                source: 'seccionamarilla.com.mx'
              });
            }
          }
        });
        return results;
      });

      businesses.forEach(b => {
        this.businesses.push({
          business_name: b.name,
          phone: b.phone,
          country: 'Mexico',
          country_code: 'MX',
          category: category,
          city: city,
          source: b.source,
          scraped_at: new Date().toISOString()
        });
      });

      this.stats.mexico += businesses.length;
      console.log(`  Found ${businesses.length} businesses`);

    } catch (error) {
      console.log(`  Error: ${error.message}`);
    }
  }

  // API Alternative: Use real-time API instead of scraping
  async fetchFromAPI(source, params) {
    console.log(`[API] Fetching from ${source}...`);
    
    // Placeholder for actual API integration
    // Examples:
    // - Data.com (formerly Jigsaw)
    // - ZoomInfo
    // - LinkedIn Sales Navigator
    // - Google Places API
    // - Yelp Fusion API
    
    console.log(`  API integration placeholder for ${source}`);
    return [];
  }

  async saveDatabase() {
    if (this.businesses.length === 0) {
      console.log('No businesses to save');
      return;
    }

    await fs.mkdir(this.outputDir, { recursive: true });

    // Save by country
    const timestamp = new Date().toISOString().slice(0, 10);
    
    for (const country of ['USA', 'Canada', 'Mexico']) {
      const countryBusinesses = this.businesses.filter(b => b.country === country);
      if (countryBusinesses.length > 0) {
        const file = path.join(this.outputDir, `${country.toLowerCase()}_businesses_${timestamp}.json`);
        await fs.writeFile(file, JSON.stringify(countryBusinesses, null, 2));
        console.log(`Saved ${country}: ${countryBusinesses.length} businesses`);
      }
    }

    // Master database
    const masterFile = path.join(this.outputDir, 'north_america_master.json');
    let existing = [];
    try {
      const data = await fs.readFile(masterFile, 'utf8');
      existing = JSON.parse(data);
    } catch {}

    // Merge and deduplicate
    const phoneMap = new Map();
    existing.forEach(b => phoneMap.set(b.phone, b));
    this.businesses.forEach(b => phoneMap.set(b.phone, b));
    
    const merged = Array.from(phoneMap.values());
    await fs.writeFile(masterFile, JSON.stringify(merged, null, 2));

    console.log(`\nMaster database: ${merged.length} unique businesses`);
  }

  report() {
    console.log('\n' + '='.repeat(70));
    console.log('📊 NORTH AMERICA SCRAPING REPORT');
    console.log('='.repeat(70));
    console.log(`Total: ${this.businesses.length} businesses`);
    console.log(`  USA: ${this.stats.usa}`);
    console.log(`  Canada: ${this.stats.canada}`);
    console.log(`  Mexico: ${this.stats.mexico}`);
    console.log('='.repeat(70));
  }
}

async function main() {
  console.log('='.repeat(70));
  console.log('🌎 NORTH AMERICA BUSINESS SCRAPER');
  console.log('USA | Canada | Mexico');
  console.log('='.repeat(70));
  console.log();

  const scraper = new NorthAmericaScraper();

  try {
    await scraper.initBrowser();

    // USA - Major cities
    console.log('\n--- UNITED STATES ---');
    const usCities = [
      { city: 'Los Angeles', state: 'CA', cats: ['restaurants', 'plumbers', 'electricians'] },
      { city: 'New York', state: 'NY', cats: ['restaurants', 'doctors', 'lawyers'] },
      { city: 'Chicago', state: 'IL', cats: ['restaurants', 'contractors', 'auto repair'] },
      { city: 'Houston', state: 'TX', cats: ['restaurants', 'oil companies', 'home services'] },
      { city: 'Phoenix', state: 'AZ', cats: ['restaurants', 'hvac', 'landscaping'] },
    ];

    for (const { city, state, cats } of usCities) {
      for (const cat of cats) {
        await scraper.scrapeUSA(city, state, cat, 2);
      }
    }

    // Canada - Major cities
    console.log('\n--- CANADA ---');
    const caCities = [
      { city: 'Toronto', province: 'ON', cats: ['restaurants', 'plumbers'] },
      { city: 'Vancouver', province: 'BC', cats: ['restaurants', 'contractors'] },
      { city: 'Montreal', province: 'QC', cats: ['restaurants', 'electricians'] },
    ];

    for (const { city, province, cats } of caCities) {
      for (const cat of cats) {
        await scraper.scrapeCanada(city, province, cat, 2);
      }
    }

    // Mexico - Major cities
    console.log('\n--- MEXICO ---');
    const mxCities = [
      { city: 'Mexico City', cats: ['restaurantes', 'plomeros'] },
      { city: 'Guadalajara', cats: ['restaurantes', 'electricistas'] },
      { city: 'Monterrey', cats: ['restaurantes', 'constructores'] },
    ];

    for (const { city, cats } of mxCities) {
      for (const cat of cats) {
        await scraper.scrapeMexico(city, cat, 2);
      }
    }

    await scraper.saveDatabase();
    scraper.report();

  } finally {
    await scraper.close();
  }

  console.log('\n✅ North America scraping complete!');
}

main().catch(console.error);
