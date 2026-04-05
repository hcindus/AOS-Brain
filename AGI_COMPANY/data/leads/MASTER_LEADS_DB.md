# Master Leads Database
## Centralized Lead Management System

**Created:** March 30, 2026
**Status:** Proposed - Awaiting approval

---

## CURRENT STATE (Fragmented)

### Lead Files Spread Across:

| Location | File Type | Count | Last Updated |
|----------|-----------|-------|--------------|
| `/sales/` | prospects_*.csv | ~800 | Mar 28 |
| `/products/leads/` | CA, TX, OR, WA | ~2,500+ | Mar 30 |
| `/CREAM/sales/` | realtor_prospects.csv | 1,000 | Mar 30 |
| `workspace/sales/` | prospects_*.csv | ~800 | Mar 28 |

**Total:** ~5,100+ leads scattered across 20+ files

---

## PROPOSED: UNIFIED DATABASE

### SQLite Schema

```sql
-- Master leads table
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    first_name TEXT,
    last_name TEXT,
    company TEXT,
    title TEXT,
    phone TEXT,
    state TEXT,
    city TEXT,
    zip TEXT,
    source TEXT, -- 'CREAM', 'PSDEPOT', 'TX_scraper', etc.
    source_file TEXT,
    priority TEXT, -- 'A', 'B', 'C'
    status TEXT DEFAULT 'new', -- 'new', 'contacted', 'qualified', 'converted', 'dead'
    assigned_to TEXT, -- Agent name
    industry TEXT, -- 'real_estate', 'tech', 'retail', etc.
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_contact_date TIMESTAMP,
    contact_count INTEGER DEFAULT 0
);

-- Contact history
CREATE TABLE contact_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER,
    agent TEXT,
    method TEXT, -- 'email', 'phone', 'meeting'
    outcome TEXT, -- 'no_answer', 'interested', 'not_interested', 'scheduled_demo'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);

-- Campaign tracking
CREATE TABLE campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    type TEXT, -- 'email', 'phone', 'mail'
    target_audience TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    status TEXT
);

-- Campaign results
CREATE TABLE campaign_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER,
    lead_id INTEGER,
    opened BOOLEAN,
    clicked BOOLEAN,
    responded BOOLEAN,
    converted BOOLEAN,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);
```

---

## BENEFITS

### Before (Fragmented)
- ❌ 20+ separate files
- ❌ No deduplication
- ❌ Can't track status across sources
- ❌ No assignment visibility
- ❌ Duplicate outreach risk

### After (Unified)
- ✅ Single source of truth
- ✅ Automatic deduplication
- ✅ Status tracking across all touches
- ✅ Clear assignment ownership
- ✅ Campaign performance metrics
- ✅ Searchable by any field

---

## MIGRATION PLAN

### Step 1: Extract (1 hour)
- Parse all CSV/JSON/XLSX files
- Standardize field names
- Handle missing data

### Step 2: Transform (1 hour)
- Normalize email addresses (lowercase, trim)
- Standardize phone numbers
- Clean up state abbreviations
- Score priorities consistently

### Step 3: Load (30 min)
- Insert into SQLite
- Detect duplicates by email
- Merge duplicate records
- Flag conflicts

### Step 4: Validate (30 min)
- Spot-check random records
- Verify counts match
- Test queries

---

## IMMEDIATE ACTIONS POSSIBLE

Once database exists:

1. **Deduplicate** - Find same person across files
2. **Assign** - Distribute to sales team (Pulp, Jane, Hume, Clippy-42)
3. **Prioritize** - Sort by potential value
4. **Enrich** - Add missing contact info
5. **Campaign** - Launch targeted outreach

---

## SAMPLE QUERIES

### High-Priority Uncontacted Leads
```sql
SELECT * FROM leads 
WHERE priority = 'A' 
  AND status = 'new'
ORDER BY created_at DESC
LIMIT 100;
```

### Sales Team Workload
```sql
SELECT assigned_to, COUNT(*) as lead_count
FROM leads
WHERE status != 'dead'
GROUP BY assigned_to;
```

### Conversion Funnel
```sql
SELECT status, COUNT(*) 
FROM leads 
GROUP BY status;
```

### Campaign Performance
```sql
SELECT 
    c.name,
    COUNT(cr.id) as total_sent,
    SUM(cr.opened) as opened,
    SUM(cr.responded) as responded,
    SUM(cr.converted) as converted
FROM campaigns c
LEFT JOIN campaign_results cr ON c.id = cr.campaign_id
GROUP BY c.id;
```

---

## NEXT STEPS

**Option A: Build Now** (3 hours)
- I create the database
- Migrate all existing leads
- Set up daily sync cron job
- Hand off to Sales team

**Option B: Build Later** (when you say)
- Keep current fragmented system
- I can query individual files as needed
- Migrate when ready

**Option C: Quick Consolidation** (30 min)
- Create simple master CSV
- Basic deduplication only
- No database complexity

---

**Recommendation:** Option A

A unified database will save hours of manual work and prevent duplicate outreach.

**Ready when you are!** 🎯
