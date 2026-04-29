# DataDepot Intelligence — Database Schema

**Version:** 1.0  
**Created:** 2026-04-29  
**Purpose:** Schema for POS market intelligence and business data aggregation

---

## Core Tables

### 1. `businesses`
Primary entity table for all businesses in the database.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment primary key |
| `license_number` | TEXT UNIQUE | External license/registration ID |
| `business_name` | TEXT | Legal business entity name |
| `dba_name` | TEXT | "Doing Business As" name |
| `license_type` | TEXT | Type of license (e.g., "41 - On-Sale Beer & Wine") |
| `status` | TEXT | Active, Suspended, Expired, etc. |
| `address` | TEXT | Street address |
| `city` | TEXT | City |
| `state` | TEXT | State (2-letter code) |
| `zip` | TEXT | ZIP code |
| `county` | TEXT | County name |
| `phone` | TEXT | Primary phone number |
| `license_issue_date` | TEXT | Date license issued |
| `license_expiry_date` | TEXT | License expiration date |
| `business_type` | TEXT | Classified type: Restaurant, Bar, Hotel, etc. |
| `pos_system_detected` | TEXT | AI-detected POS system name |
| `data_source` | TEXT | Where this record originated |
| `scraped_at` | TIMESTAMP | When first collected |
| `last_updated` | TIMESTAMP | When last modified |

**Indexes:**
- `idx_businesses_county` on `county`
- `idx_businesses_city` on `city`
- `idx_businesses_type` on `business_type`
- `idx_businesses_pos` on `pos_system_detected`

---

### 2. `contacts`
Decision-maker contacts for sales outreach.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Primary key |
| `business_id` | INTEGER FK | References `businesses(id)` |
| `name` | TEXT | Contact full name |
| `title` | TEXT | Job title (Owner, GM, IT Manager, etc.) |
| `email` | TEXT | Email address |
| `phone` | TEXT | Direct phone |
| `linkedin_url` | TEXT | LinkedIn profile URL |
| `source` | TEXT | How this contact was found |
| `verified_at` | TIMESTAMP | When email/phone was verified |

**Indexes:**
- `idx_contacts_business` on `business_id`
- `idx_contacts_title` on `title`

---

### 3. `pos_intelligence`
AI-enriched POS system detection and analysis.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Primary key |
| `business_id` | INTEGER FK | References `businesses(id)` |
| `detected_pos_system` | TEXT | System name: Square, Toast, Clover, etc. |
| `confidence_score` | REAL | 0.0 - 1.0 AI confidence |
| `detection_method` | TEXT | How detected: photo_analysis, review_text, website_check |
| `equipment_age_estimate` | TEXT | Estimated age: "0-2 years", "3-5 years", etc. |
| `replacement_likelihood` | REAL | 0.0 - 1.0 score for replacement timing |
| `last_seen_date` | TEXT | When POS was last confirmed present |

**Indexes:**
- `idx_pos_business` on `business_id`
- `idx_pos_system` on `detected_pos_system`
- `idx_pos_confidence` on `confidence_score`

---

### 4. `scrape_log`
Audit trail for all data collection activities.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Primary key |
| `source` | TEXT | Data source name (CA_ABC, Google_Places, etc.) |
| `records_scraped` | INTEGER | Total records processed |
| `new_records` | INTEGER | New businesses added |
| `errors` | INTEGER | Errors encountered |
| `started_at` | TIMESTAMP | Scrape start time |
| `completed_at` | TIMESTAMP | Scrape end time |

---

### 5. `subscriptions` (Future)
Customer subscription tracking.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Primary key |
| `customer_email` | TEXT | Subscriber email |
| `plan_type` | TEXT | Basic, Pro, Enterprise |
| `filters` | TEXT JSON | Active filters: counties, POS types, etc. |
| `created_at` | TIMESTAMP | Subscription start |
| `expires_at` | TIMESTAMP | Subscription end |
| `stripe_subscription_id` | TEXT | Stripe reference |

---

## Data Flow

```
┌─────────────────┐
│  Data Sources   │  ABC Licenses, Google Places, LinkedIn
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Scraper      │  Python scripts + AI enrichment
│   (ca_abc_)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   businesses    │  Core entity storage
│     table       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Enrichment  │  POS detection, contact finding
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API/Export     │  Customer delivery
└─────────────────┘
```

---

## Query Patterns

### Count businesses by county
```sql
SELECT county, COUNT(*) as total
FROM businesses
WHERE status = 'Active'
GROUP BY county
ORDER BY total DESC;
```

### Find restaurants likely needing POS upgrade
```sql
SELECT b.business_name, b.city, b.phone, p.detected_pos_system,
       p.equipment_age_estimate, p.replacement_likelihood
FROM businesses b
JOIN pos_intelligence p ON b.id = p.business_id
WHERE b.business_type = 'Restaurant'
  AND p.replacement_likelihood > 0.7
ORDER BY p.replacement_likelihood DESC;
```

### Export for customer (filtered)
```sql
SELECT b.business_name, b.dba_name, b.address, b.city, 
       b.phone, b.business_type, p.detected_pos_system
FROM businesses b
LEFT JOIN pos_intelligence p ON b.id = p.business_id
WHERE b.county IN ('San Francisco', 'Alameda')
  AND b.status = 'Active'
  AND (p.confidence_score IS NULL OR p.confidence_score > 0.6);
```

---

## Scale Estimates

| Metric | Month 1 | Month 6 | Year 1 |
|--------|---------|---------|--------|
| Records | 5,000 | 50,000 | 200,000 |
| Size (SQLite) | ~5 MB | ~50 MB | ~200 MB |
| Export CSV | ~2 MB | ~20 MB | ~80 MB |

---

## Next Schema Additions

- [ ] `competitor_mentions` — Track POS systems mentioned in reviews
- [ ] `price_intelligence` — Aggregated pricing data by product/region
- [ ] `equipment_installations` — Detected installation dates from photos
- [ ] `web_presence` — Website, social media URLs, online ordering platforms
