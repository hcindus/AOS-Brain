#!/usr/bin/env node
/**
 * LEAD SCRAPER BROWSER
 * Browser automation for lead generation
 */

const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');

class LeadScraperBrowser {
  constructor() {
    this.leads = [];
    this.outputDir = '/root/.openclaw/workspace/data/leads';
  }

  async initBrowser() {
    console.log('[LeadScraper] Initializing browser...');
    
    this.browser = await chromium.launch({
      headless: true,
      args: ['--disable-blink-features=AutomationControlled']
    });

    this.context = await this.browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    });

    this.page = await this.context.newPage();
    console.log('[LeadScraper] Browser ready');
  }

  async close() {
    await this.context.close();
    await this.browser.close();
  }

  async scrapeOpenCorporates(query, location) {
    console.log(`[LeadScraper] Searching: ${query} in ${location}`);
    
    try {
      await this.page.goto(
        `https://opencorporates.com/companies?jurisdiction_code=us_${location}&q=${query}`,
        { waitUntil: 'networkidle', timeout: 60000 }
      );

      await this.page.waitForSelector('.company-result', { timeout: 10000 });

      const companies = await this.page.evaluate(() => {
        const results = [];
        document.querySelectorAll('.company-result').forEach(el => {
          const nameEl = el.querySelector('.company-name a');
          const statusEl = el.querySelector('.company-status');
          
          if (nameEl) {
            results.push({
              name: nameEl.textContent.trim(),
              url: nameEl.getAttribute('href'),
              status: statusEl ? statusEl.textContent.trim() : 'Unknown'
            });
          }
        });
        return results;
      });

      companies.forEach(c => {
        if (c.status.toLowerCase().includes('active')) {
          this.leads.push({
            company_name: c.name,
            source: 'OpenCorporates',
            url: `https://opencorporates.com${c.url}`,
            status: c.status,
            location: location,
            query: query,
            scraped_at: new Date().toISOString(),
            priority: 'MEDIUM'
          });
        }
      });

      console.log(`  Found ${companies.length} companies`);
      
    } catch (error) {
      console.log(`  Error: ${error.message}`);
    }
  }

  async saveLeads() {
    if (this.leads.length === 0) {
      console.log('No leads to save');
      return;
    }

    await fs.mkdir(this.outputDir, { recursive: true });

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputFile = path.join(this.outputDir, `browser_leads_${timestamp}.json`);

    await fs.writeFile(outputFile, JSON.stringify(this.leads, null, 2));
    console.log(`Saved ${this.leads.length} leads`);
  }

  report() {
    console.log('\n' + '='.repeat(70));
    console.log('LEAD SCRAPING REPORT');
    console.log(`Total leads: ${this.leads.length}`);
    
    const bySource = {};
    this.leads.forEach(l => {
      bySource[l.source] = (bySource[l.source] || 0) + 1;
    });

    console.log('\nBy Source:');
    Object.entries(bySource).forEach(([src, count]) => {
      console.log(`  ${src}: ${count}`);
    });

    console.log('='.repeat(70));
  }
}

async function main() {
  console.log('='.repeat(70));
  console.log('BROWSER LEAD SCRAPER');
  console.log('='.repeat(70));

  const scraper = new LeadScraperBrowser();

  try {
    await scraper.initBrowser();
    await scraper.scrapeOpenCorporates('technology', 'ca');
    await scraper.scrapeOpenCorporates('software', 'ca');
    await scraper.scrapeOpenCorporates('restaurant', 'ca');
    await scraper.saveLeads();
    scraper.report();
  } finally {
    await scraper.close();
  }

  console.log('\nBrowser scraping complete!');
}

main().catch(console.error);
