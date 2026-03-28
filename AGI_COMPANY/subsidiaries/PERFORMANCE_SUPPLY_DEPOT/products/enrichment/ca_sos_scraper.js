#!/usr/bin/env node3
/**
 * CA Secretary of State Business Search Scraper
 * 
 * Searches CA business filings to get officer/owner information
 * for lead enrichment.
 * 
 * Usage: node ca_sos_scraper.js "Business Name"
 */

const https = require('https');
const http = require('http');

// CA SOS Business Search API endpoint
const BASE_URL = 'businesssearch.sos.ca.gov';

class CASOSScraper {
  constructor() {
    this.results = [];
  }

  /**
   * Make HTTPS request
   */
  request(options, data = null) {
    return new Promise((resolve, reject) => {
      const req = https.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
            resolve(JSON.parse(body));
          } catch (e) {
            resolve(body);
          }
        });
      });
      req.on('error', reject);
      if (data) req.write(data);
      req.end();
    });
  }

  /**
   * Search for a business
   */
  async search(businessName) {
    console.log(`🔍 Searching for: "${businessName}"`);
    
    const postData = JSON.stringify({
      "SearchType": "Business",
      "SearchValue": businessName,
      "StartRow": 1,
      "PageSize": 10
    });

    const options = {
      hostname: BASE_URL,
      path: '/api/v1/business/search',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'User-Agent': 'Mozilla/5.0 (compatible; LeadEnrichment/1.0)',
        'Accept': 'application/json'
      }
    };

    try {
      const result = await this.request(options, postData);
      return this.parseResults(result);
    } catch (e) {
      console.error('❌ Search error:', e.message);
      return [];
    }
  }

  /**
   * Parse search results
   */
  parseResults(data) {
    if (!data || !data.results) return [];
    
    return data.results.map(b => ({
      name: b.BusinessName || b.Name,
      status: b.Status,
      jurisdiction: b.Jurisdiction,
      incorporationDate: b.IncorporationDate || b.DateOfRegistration,
      agent: b.AgentName || b.RegisteredAgent,
      address: b.Address || b.BusinessAddress,
      city: b.City,
      state: b.State,
      zip: b.ZipCode,
      sosId: b.SOSID || b.FileNumber
    }));
  }

  /**
   * Get detailed business info
   */
  async getDetails(sosId) {
    console.log(`📋 Getting details for SOS ID: ${sosId}`);
    
    const options = {
      hostname: BASE_URL,
      path: `/api/v1/business/${sosId}`,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; LeadEnrichment/1.0)',
        'Accept': 'application/json'
      }
    };

    try {
      const result = await this.request(options);
      return {
        officers: result.Officers || [],
        principals: result.Principals || [],
        filings: result.Filings || []
      };
    } catch (e) {
      console.error('❌ Details error:', e.message);
      return null;
    }
  }
}

// Simple search (can be expanded)
async function main() {
  const query = process.argv[2] || 'Starbucks';
  const scraper = new CASOSScraper();
  const results = await scraper.search(query);
  
  console.log('\n📊 Results:');
  console.log(JSON.stringify(results, null, 2));
}

// Export for use in other scripts
module.exports = CASOSScraper;

// Run if called directly
if (require.main === module) {
  main();
}
