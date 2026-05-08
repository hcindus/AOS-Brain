<!--
VERSION: 1.0.0
UPDATED: 2026-05-08
STATUS: Active
-->

# 📊 DATABASE OPERATIONS SOP
## Standard Operating Procedure for Complete Beginners

**Prepared for:** Captain (root)  
**Email:** Antonio.Hudnall@gmail.com  
**Date:** 2026-05-08  
**Classification:** Beginner-Friendly Documentation

---

## 🎯 WHAT THIS DOCUMENT IS

This is your step-by-step guide to working with databases. **No prior knowledge assumed.** If you've never touched a database in your life, this will get you from zero to confidently adding and updating records.

Think of a database like a really smart Excel spreadsheet that:
- Never gets corrupted
- Can handle millions of rows
- Lets multiple people use it at once
- Remembers every change

---

## 📁 WHAT DATABASES YOU HAVE

### 1. **DepotChaos Database** (Primary Sales/Leads)
- **Location:** `/root/.openclaw/workspace/data/depot_chaos/unified.db`
- **Type:** SQLite
- **Purpose:** Sales leads, customer data, California ABC license tracking
- **Tables:** `leads`, `scrape_runs`, `enriched_leads`, `unified_leads`, `ca_abc_licenses`, `psd_customers`, `datadepot_intelligence`

### 2. **DataDepot Intelligence Database**
- **Location:** `/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/database/datadepot.db`
- **Type:** SQLite
- **Purpose:** Business intelligence, POS data
- **Tables:** `businesses`, `leads`, `contacts`, `scrape_log`, `pos_intelligence`

### 3. **DepotChaos Vendors Database**
- **Location:** `/root/.openclaw/workspace/DepotChaos/depot_chaos.db`
- **Type:** SQLite
- **Purpose:** Vendor management, supplier tracking
- **Tables:** `vendors`, `vendor_interactions`

### 4. **Dark Factory Database**
- **Location:** `/root/.openclaw/workspace/data/factory/dark_factory.db`
- **Type:** SQLite
- **Purpose:** Factory operations data

---

## 🧰 TOOLS YOU'LL USE

### Option 1: Command Line (SQLite)
**Best for:** Quick commands, scripts, automation

### Option 2: Python (Recommended for Applications)
**Best for:** Building apps, complex logic, integrations

### Option 3: Database Browser GUI
**Best for:** Visual editing, exploring data

---

## 📖 PART 1: THE BASICS (Read This First)

### What is a Database Table?
Think of a table like a spreadsheet with **rows** and **columns**:

| id | business_name | city     | phone      |
|----|---------------|----------|------------|
| 1  | Joe's Pizza   | Fresno   | 559-1234   |
| 2  | Sally's Spa   | Bakersfield| 661-5678 |

- **Row** = One record (like Joe's Pizza)
- **Column** = One field (like phone number)
- **id** = Unique identifier (auto-generated)

### Key Terms
| Term | Meaning | Example |
|------|---------|---------|
| **INSERT** | Add a new record | "Add a new lead" |
| **UPDATE** | Change existing record | "Update the phone number" |
| **SELECT** | Read/view records | "Show me all leads in Fresno" |
| **DELETE** | Remove a record | "Delete duplicate entry" |
| **WHERE** | Filter which records | "WHERE city = 'Fresno'" |

---

## 📖 PART 2: COMMAND LINE OPERATIONS

### 2.1 CONNECTING TO A DATABASE

```bash
# Connect to DepotChaos database
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db

# You'll see a prompt: sqlite>
# Type .quit to exit
```

**Useful commands once inside:**
```sql
.tables                    -- List all tables
.schema leads              -- Show table structure
.headers on                -- Show column names
.mode column               -- Format output in columns
.mode csv                 -- Format output as CSV
.quit                     -- Exit
```

### 2.2 ADDING RECORDS (INSERT)

#### DepotChaos: Add a New Lead

```sql
-- The basic pattern:
-- INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...);

-- Add a new lead
INSERT INTO leads (
    business_name, 
    city, 
    state, 
    phone, 
    email, 
    business_type,
    priority,
    source,
    status
) VALUES (
    'Tony\'s Tacos',           -- Text needs quotes
    'Fresno',                   -- City
    'CA',                       -- State
    '559-555-1234',            -- Phone
    'tony@tonystacos.com',     -- Email
    'Restaurant',              -- Business type
    'high',                    -- Priority: high/medium/low
    'manual_entry',            -- Where it came from
    'new'                      -- Status: new/contacted/qualified/closed
);
```

**Important Notes:**
- Text values need **single quotes** 'like this'
- If text has quotes inside, double them: 'Tony\'s Tacos'
- Numbers don't need quotes: 123
- `id` is auto-generated (don't include it)
- `scraped_at` will be set automatically

#### Add Multiple Records at Once

```sql
INSERT INTO leads (business_name, city, state, phone, priority, status) VALUES 
('Burger Barn', 'Bakersfield', 'CA', '661-555-0001', 'medium', 'new'),
('Coffee Corner', 'Visalia', 'CA', '559-555-0002', 'high', 'new'),
('Tech Shop', 'Fresno', 'CA', '559-555-0003', 'low', 'new');
```

### 2.3 UPDATING RECORDS (UPDATE)

#### Update a Single Field

```sql
-- Pattern: UPDATE table SET column = value WHERE condition;

-- Update phone number for specific business
UPDATE leads 
SET phone = '559-555-9999' 
WHERE business_name = 'Tony\'s Tacos';
```

#### Update Multiple Fields

```sql
-- Update several things at once
UPDATE leads 
SET 
    phone = '559-555-8888',
    email = 'newemail@tonystacos.com',
    priority = 'urgent'
WHERE business_name = 'Tony\'s Tacos';
```

#### Update Based on Conditions

```sql
-- Mark all Fresno leads as high priority
UPDATE leads 
SET priority = 'high' 
WHERE city = 'Fresno';

-- Change status for contacted leads
UPDATE leads 
SET status = 'qualified' 
WHERE status = 'contacted' 
  AND last_contact IS NOT NULL;
```

### 2.4 QUERYING RECORDS (SELECT)

#### View All Records

```sql
-- See everything (limit to 10 for sanity)
SELECT * FROM leads LIMIT 10;

-- See specific columns
SELECT business_name, city, phone, status FROM leads LIMIT 10;
```

#### Filter Records

```sql
-- Find leads in specific city
SELECT business_name, phone, email 
FROM leads 
WHERE city = 'Fresno';

-- Find high priority leads
SELECT * FROM leads WHERE priority = 'high';

-- Find leads with phone numbers (not null)
SELECT business_name, phone 
FROM leads 
WHERE phone IS NOT NULL;

-- Find leads containing "Pizza" (case insensitive)
SELECT * FROM leads 
WHERE business_name LIKE '%Pizza%';

-- Find leads with multiple conditions
SELECT * FROM leads 
WHERE city = 'Fresno' 
  AND priority = 'high'
  AND status = 'new';
```

#### Count and Statistics

```sql
-- Count total leads
SELECT COUNT(*) FROM leads;

-- Count by city
SELECT city, COUNT(*) as lead_count 
FROM leads 
GROUP BY city 
ORDER BY lead_count DESC;

-- Count by status
SELECT status, COUNT(*) 
FROM leads 
GROUP BY status;
```

### 2.5 VIEWING TABLE STRUCTURE

```sql
-- See what columns exist
.schema leads

-- Get detailed info
PRAGMA table_info(leads);

-- See indexes (speed optimizations)
PRAGMA index_list(leads);
```

---

## 📖 PART 3: PYTHON OPERATIONS (Recommended)

### 3.1 SETUP

Create a Python script (e.g., `database_operations.py`):

```python
import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('/root/.openclaw/workspace/data/depot_chaos/unified.db')
cursor = conn.cursor()

# Don't forget to close when done!
# conn.close()
```

### 3.2 ADDING RECORDS WITH PYTHON

```python
import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('/root/.openclaw/workspace/data/depot_chaos/unified.db')
cursor = conn.cursor()

# Add a single lead
lead_data = {
    'business_name': 'Python Pizza Palace',
    'city': 'Fresno',
    'state': 'CA',
    'phone': '559-555-PYTHON',
    'email': 'python@example.com',
    'business_type': 'Restaurant',
    'priority': 'high',
    'source': 'manual_entry',
    'status': 'new',
    'scraped_at': datetime.now().isoformat()
}

cursor.execute("""
    INSERT INTO leads 
    (business_name, city, state, phone, email, business_type, priority, source, status, scraped_at)
    VALUES 
    (:business_name, :city, :state, :phone, :email, :business_type, :priority, :source, :status, :scraped_at)
""", lead_data)

# Commit the transaction
conn.commit()

# Get the ID of the inserted record
new_id = cursor.lastrowid
print(f"Added lead with ID: {new_id}")

conn.close()
```

### 3.3 ADDING MULTIPLE RECORDS (BULK INSERT)

```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect('/root/.openclaw/workspace/data/depot_chaos/unified.db')
cursor = conn.cursor()

# Prepare multiple records
leads = [
    ('Bulk Business 1', 'Fresno', 'CA', '559-0001', 'Retail', 'medium', 'import'),
    ('Bulk Business 2', 'Bakersfield', 'CA', '661-0002', 'Restaurant', 'high', 'import'),
    ('Bulk Business 3', 'Visalia', 'CA', '559-0003', 'Service', 'low', 'import'),
]

now = datetime.now().isoformat()

# Insert all at once
# Note: Using ? placeholders for SQLite
cursor.executemany("""
    INSERT INTO leads 
    (business_name, city, state, phone, business_type, priority, source, scraped_at, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'new')
""", [(l[0], l[1], l[2], l[3], l[4], l[5], l[6], now) for l in leads])

conn.commit()
print(f"Added {cursor.rowcount} leads")
conn.close()
```

### 3.4 UPDATING RECORDS WITH PYTHON

```python
import sqlite3

conn = sqlite3.connect('/root/.openclaw/workspace/data/depot_chaos/unified.db')
cursor = conn.cursor()

# Update by ID
lead_id = 42
cursor.execute("""
    UPDATE leads 
    SET phone = ?, email = ?, priority = ?
    WHERE id = ?
""", ('559-NEW-PHONE', 'new@email.com', 'urgent', lead_id))

# Update by business name
cursor.execute("""
    UPDATE leads 
    SET status = 'contacted', last_contact = ?
    WHERE business_name = ?
""", (datetime.now().isoformat(), 'Python Pizza Palace'))

conn.commit()
print(f"Updated {cursor.rowcount} records")
conn.close()
```

### 3.5 QUERYING WITH PYTHON

```python
import sqlite3

conn = sqlite3.connect('/root/.openclaw/workspace/data/depot_chaos/unified.db')
cursor = conn.cursor()

# Get all high priority Fresno leads
cursor.execute("""
    SELECT id, business_name, phone, email, status
    FROM leads
    WHERE city = 'Fresno' AND priority = 'high'
    ORDER BY scraped_at DESC
""")

leads = cursor.fetchall()

for lead in leads:
    print(f"ID: {lead[0]}")
    print(f"Business: {lead[1]}")
    print(f"Phone: {lead[2]}")
    print(f"Email: {lead[3]}")
    print(f"Status: {lead[4]}")
    print("-" * 40)

conn.close()
```

### 3.6 USING CONTEXT MANAGERS (Safer)

```python
import sqlite3

# Context manager automatically closes connection
with sqlite3.connect('/root/.openclaw/workspace/data/depot_chaos/unified.db') as conn:
    cursor = conn.cursor()
    
    # Your operations here
    cursor.execute("SELECT COUNT(*) FROM leads")
    count = cursor.fetchone()[0]
    print(f"Total leads: {count}")
    
    # Auto-commits on successful exit
# Connection automatically closed
```

---

## 📖 PART 4: COMMON OPERATIONS BY USE CASE

### 4.1 SALES WORKFLOW

#### Mark Lead as Contacted
```sql
-- SQL
UPDATE leads 
SET 
    status = 'contacted',
    last_contact = datetime('now'),
    assigned_agent = 'Miles'
WHERE id = 123;
```

```python
# Python
with sqlite3.connect('/root/.openclaw/workspace/data/depot_chaos/unified.db') as conn:
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leads 
        SET status = 'contacted', last_contact = ?, assigned_agent = ?
        WHERE id = ?
    """, (datetime.now().isoformat(), 'Miles', lead_id))
```

#### Schedule Callback
```sql
UPDATE leads 
SET 
    callback_date = '2026-05-15',
    callback_notes = 'Call back to discuss POS system quote'
WHERE id = 123;
```

#### Mark as Converted (Sale Made!)
```sql
UPDATE leads 
SET 
    converted = 1,
    converted_at = datetime('now'),
    status = 'closed'
WHERE id = 123;
```

### 4.2 DATA IMPORT OPERATIONS

#### Import from CSV

```python
import csv
import sqlite3

conn = sqlite3.connect('/root/.openclaw/workspace/data/depot_chaos/unified.db')
cursor = conn.cursor()

with open('new_leads.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute("""
            INSERT INTO leads (business_name, city, state, phone, source)
            VALUES (?, ?, ?, ?, 'csv_import')
        """, (row['Business Name'], row['City'], row['State'], row['Phone']))

conn.commit()
conn.close()
```

### 4.3 REPORTING QUERIES

#### Daily Activity Report
```sql
-- Leads added today
SELECT COUNT(*) 
FROM leads 
WHERE date(scraped_at) = date('now');

-- Leads contacted today
SELECT COUNT(*) 
FROM leads 
WHERE date(last_contact) = date('now');

-- Conversion rate
SELECT 
    COUNT(CASE WHEN converted = 1 THEN 1 END) * 100.0 / COUNT(*) as conversion_rate
FROM leads 
WHERE scraped_at >= date('now', '-30 days');
```

#### Agent Performance
```sql
SELECT 
    assigned_agent,
    COUNT(*) as total_leads,
    COUNT(CASE WHEN status = 'closed' THEN 1 END) as closed,
    COUNT(CASE WHEN converted = 1 THEN 1 END) as converted
FROM leads
WHERE assigned_agent IS NOT NULL
GROUP BY assigned_agent;
```

---

## 📖 PART 5: BEST PRACTICES

### 5.1 ALWAYS USE WHERE WITH UPDATE/DELETE

**❌ WRONG - Updates EVERYTHING:**
```sql
UPDATE leads SET status = 'contacted';  -- DON'T DO THIS!
```

**✅ RIGHT - Updates specific record:**
```sql
UPDATE leads SET status = 'contacted' WHERE id = 123;
```

### 5.2 BACKUP BEFORE MASS OPERATIONS

```bash
# Copy the database file before big changes
cp /root/.openclaw/workspace/data/depot_chaos/unified.db \
   /root/.openclaw/workspace/data/depot_chaos/unified_backup_$(date +%Y%m%d).db
```

### 5.3 VALIDATE BEFORE INSERTING

```python
# Check if business already exists before adding
cursor.execute("SELECT id FROM leads WHERE business_name = ? AND city = ?", 
               (business_name, city))
if cursor.fetchone():
    print("Lead already exists!")
else:
    # Insert new lead
    pass
```

### 5.4 USE TRANSACTIONS FOR MULTIPLE OPERATIONS

```python
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    # Multiple operations
    cursor.execute("INSERT INTO leads ...", data1)
    cursor.execute("UPDATE something ...", data2)
    cursor.execute("INSERT INTO notes ...", data3)
    
    # All or nothing - commit together
    conn.commit()
    print("All operations successful")
    
except Exception as e:
    # Something failed - rollback everything
    conn.rollback()
    print(f"Error: {e}")
finally:
    conn.close()
```

### 5.5 SANITIZE INPUT (Security)

**❌ NEVER DO THIS:**
```python
query = f"SELECT * FROM leads WHERE city = '{user_input}'"
# Vulnerable to SQL injection!
```

**✅ ALWAYS USE PARAMETERIZED QUERIES:**
```python
cursor.execute("SELECT * FROM leads WHERE city = ?", (user_input,))
```

---

## 📖 PART 6: QUICK REFERENCE

### DepotChaos Schema Summary

#### `leads` Table - Main Sales Table
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Auto-generated primary key |
| business_name | TEXT | Company name |
| city | TEXT | City |
| state | TEXT | State (usually 'CA') |
| zip | TEXT | ZIP code |
| phone | TEXT | Phone number |
| email | TEXT | Email address |
| business_type | TEXT | Category |
| priority | TEXT | high/medium/low |
| source | TEXT | Where lead came from |
| status | TEXT | new/contacted/qualified/closed |
| scraped_at | TEXT | When added |
| assigned_agent | TEXT | Who's working it |
| converted | BOOLEAN | 0 or 1 |
| notes | TEXT | Free text notes |

### Common Status Values
- `new` - Just added
- `contacted` - Called/emailed
- `qualified` - Interested/potential sale
- `closed` - Deal done or lost

### Common Priority Values
- `urgent` - Hot lead
- `high` - Good potential
- `medium` - Standard
- `low` - Cold lead

---

## 📖 PART 7: TROUBLESHOOTING

### "database is locked" Error
```bash
# Another process has the database open
# Wait a moment and retry, or:

# Find and kill blocking process
lsof /root/.openclaw/workspace/data/depot_chaos/unified.db
```

### "no such column" Error
Check the actual column names:
```sql
PRAGMA table_info(leads);
```

### "UNIQUE constraint failed"
You're trying to add a duplicate. Check unique fields:
```sql
-- In leads table: business_name + city + state must be unique
SELECT * FROM leads WHERE business_name = 'Your Business' AND city = 'Your City';
```

### "datatype mismatch"
You're putting text where a number should be (or vice versa). Check the schema.

---

## 📞 NEED HELP?

1. **Check the schema:** `.schema table_name`
2. **Check existing data:** `SELECT * FROM table_name LIMIT 5`
3. **Make a backup** before big changes
4. **Test your query** with SELECT before UPDATE/DELETE

---

**Document Version:** 1.0.0  
**Last Updated:** 2026-05-08  
**Next Review:** As needed

---

## ✅ APPENDIX: ONE-PAGE CHEAT SHEET

### Connect
```bash
sqlite3 /path/to/database.db
```

### Add Record
```sql
INSERT INTO table (col1, col2) VALUES ('val1', 'val2');
```

### Update Record
```sql
UPDATE table SET col1 = 'newval' WHERE id = 123;
```

### View Records
```sql
SELECT * FROM table WHERE condition LIMIT 10;
```

### Count Records
```sql
SELECT COUNT(*) FROM table WHERE condition;
```

### Exit
```sql
.quit
```

---

**End of SOP**
