# Lead Enrichment Pipeline

Tools for enriching CA business leads with contact information.

## Status

⚠️ **Network blocked** - Cannot access external business APIs directly from this environment.

## Available Tools

### 1. CA SOS Scraper (`ca_sos_scraper.js`)
Attempts to query CA Secretary of State business registry.

**Usage:**
```bash
node ca_sos_scraper.js "Business Name"
```

### 2. Enrichment Pipeline (`enrich_leads.js`)
Processes county lead files and creates enrichment queues.

**Usage:**
```bash
# Process single county
node enrich_leads.js Alameda

# Process all counties
node enrich_leads.js
```

## Recommended Approach

Since direct API access is blocked, recommend:

1. **Manual research queue** - Export leads to CSV, use virtual assistant
2. **Third-party service** - Use Apollo.io, Clearbit, ZoomInfo (paid)
3. **Local scraping** - Run scraper from different network
4. **Cold calling** - Call businesses directly

## Output

Enriched leads saved to `leads_enriched/` directory.

## Files

- `ca_sos_scraper.js` - CA SOS API client
- `enrich_leads.js` - Main enrichment pipeline
- `README.md` - This file
