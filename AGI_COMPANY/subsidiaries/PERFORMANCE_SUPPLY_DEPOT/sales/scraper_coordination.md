# Scraper Coordination - Lead Generation
## Performance Supply Depot LLC

---

## Scraper Task Assignments

### R2-D2 - Systems/Lead Scraping
**Status:** 🟢 ACTIVE | **Priority:** HIGH

**Tasks:**
1. Scrape business directories (Yellow Pages, Yelp, BBB)
2. Extract contact info for decision-makers
3. Filter by company size and industry
4. Validate email addresses
5. Deduplicate against existing CRM

**Output Format:**
```json
{
  "company_name": "string",
  "industry": "string",
  "employee_count": "range",
  "contact_name": "string",
  "title": "string",
  "email": "string",
  "phone": "string",
  "address": "string",
  "website": "string",
  "tier": "Starter|Professional|Corporate|Enterprise"
}
```

**Target Volume:** 5,000 leads/week
**Delivery:** Daily CSV upload to `/sales/leads/r2d2/`

---

### TX Scraper - Texas Leads
**Status:** 🟢 ACTIVE | **Priority:** HIGH

**Geographic Focus:** Texas (All major metros)
- Houston
- Dallas-Fort Worth
- San Antonio
- Austin
- El Paso

**Industry Targets:**
- Restaurants & Food Service
- Retail Stores
- Healthcare Clinics
- Auto Repair Shops
- Salons & Spas

**Tasks:**
1. Scrape Texas Secretary of State business registry
2. Target businesses 2-5 years old (growth phase)
3. Extract owner/operator contact info
4. Cross-reference with LinkedIn

**Target Volume:** 2,000 leads/week
**Delivery:** Weekly batch to `/sales/leads/tx/`

---

### AZ Scraper - Arizona Leads
**Status:** 🟢 ACTIVE | **Priority:** HIGH

**Geographic Focus:** Arizona
- Phoenix
- Tucson
- Mesa
- Scottsdale
- Tempe

**Industry Targets:**
- Tourism & Hospitality
- Real Estate Agencies
- Construction Companies
- Medical Practices
- Legal Firms

**Tasks:**
1. Scrape Arizona Corporation Commission database
2. Focus on LLCs and S-Corps
3. Extract registered agent info
4. Find direct business phone numbers

**Target Volume:** 1,500 leads/week
**Delivery:** Weekly batch to `/sales/leads/az/`

---

### CA SOS Scraper - California Business Leads
**Status:** 🟢 ACTIVE | **Priority:** CRITICAL

**Geographic Focus:** California (High-value market)
- Los Angeles County
- San Francisco Bay Area
- San Diego
- Sacramento
- Orange County

**Industry Targets:**
- Tech Startups
- E-commerce Companies
- Professional Services
- Healthcare Providers
- Manufacturing

**Tasks:**
1. Scrape CA Secretary of State business search
2. Filter by filing date (last 12 months)
3. Extract officer names and addresses
4. Enrich with Clearbit/Hunter.io
5. Prioritize venture-backed companies

**Target Volume:** 3,000 leads/week
**Delivery:** Daily to `/sales/leads/ca/`

---

## Lead Distribution Matrix

| Scraper | Leads/Week | Jane (Ent) | Pulp (Corp) | Hume (Pro) | Clippy-42 (Starter) |
|---------|------------|------------|-------------|------------|---------------------|
| R2-D2 | 5,000 | 500 | 1,000 | 1,500 | 2,000 |
| TX | 2,000 | 200 | 400 | 600 | 800 |
| AZ | 1,500 | 150 | 300 | 450 | 600 |
| CA SOS | 3,000 | 600 | 900 | 750 | 750 |
| **TOTAL** | **11,500** | **1,450** | **2,600** | **3,300** | **4,150** |

---

## Lead Qualification Criteria

### Enterprise (Jane)
- 500+ employees
- $50M+ annual revenue
- Multi-location presence
- Public or PE-backed

### Corporate (Pulp)
- 100-500 employees
- $5M-$50M revenue
- Regional presence
- Growth trajectory

### Professional (Hume)
- 20-100 employees
- $1M-$5M revenue
- Local/regional focus
- Established 2+ years

### Starter (Clippy-42)
- 1-20 employees
- <$1M revenue
- New business (0-3 years)
- Solopreneurs welcome

---

## Scraper Technical Requirements

### Data Fields Required
1. Company legal name
2. DBA (if applicable)
3. Industry/NAICS code
4. Employee count estimate
5. Annual revenue estimate
6. Primary contact name
7. Contact title
8. Verified email
9. Direct phone
10. Full address
11. Website URL
12. Social media profiles

### Quality Standards
- Email validation: 95%+ deliverable
- Phone validation: 90%+ reachable
- Duplicate rate: <5%
- Data freshness: <30 days

---

## Coordination Schedule

| Day | Activity |
|-----|----------|
| Monday | Weekly kickoff, priority targets review |
| Tuesday-Thursday | Active scraping, daily uploads |
| Friday | Lead quality review, distribution to sales |
| Weekend | Automated scraping continues |

---

## Status: 🟢 COORDINATION COMPLETE
**Next Action:** Scrapers begin lead generation
**Expected First Batch:** Within 24 hours
