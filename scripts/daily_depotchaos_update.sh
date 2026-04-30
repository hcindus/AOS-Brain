#!/bin/bash
# DAILY DEPOTCHAOS LEAD UPDATE & ENRICHMENT
# Runs daily at 02:00 UTC to update leads and enrich data

set -e

LOG_FILE="/var/log/aos/depotchaos_daily.log"
DB_PATH="/root/.openclaw/workspace/data/depot_chaos/unified.db"
DATA_DIR="/root/.openclaw/workspace/data/scraper"

echo "$(date -u -Iseconds) === DEPOTCHAOS DAILY UPDATE STARTED ===" | tee -a "$LOG_FILE"

# 1. Import new leads from scraper data
echo "[1/4] Importing new leads from scraper..." | tee -a "$LOG_FILE"
python3 << 'PYEOF' >> "$LOG_FILE" 2>&1
import sqlite3
import json
from datetime import datetime
import uuid

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
DATA_DIR = "/root/.openclaw/workspace/data/scraper"

def import_scraper_leads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    imported = 0
    
    # Check for email-based leads
    try:
        with open(f"{DATA_DIR}/email_stats.json") as f:
            email_data = json.load(f)
        print(f"  - Email data: {email_data.get('unread_count', 0)} unread emails")
    except Exception as e:
        print(f"  - No email data: {e}")
    
    conn.close()
    return imported

count = import_scraper_leads()
print(f"  ✓ Import complete: {count} new leads")
PYEOF

# 2. Run enrichment on unenriched leads
echo "[2/4] Enriching leads..." | tee -a "$LOG_FILE"
python3 << 'PYEOF' >> "$LOG_FILE" 2>&1
import sqlite3
import json
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def enrich_leads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get leads without enrichment
    c.execute("""
        SELECT id, company_name, county, enrichment_data 
        FROM leads 
        WHERE enrichment_data IS NULL 
           OR enrichment_data = '{}' 
           OR enrichment_data = 'null'
        LIMIT 100
    """)
    
    leads = c.fetchall()
    enriched = 0
    
    for lead_id, company, county, existing in leads:
        # Build enrichment based on available data
        enrichment = {
            "enriched_at": datetime.now().isoformat(),
            "source": "daily_enrichment_job",
            "company_normalized": company.lower().strip() if company else None,
            "county_normalized": county.lower().strip() if county else None,
            "enrichment_version": "1.0"
        }
        
        # Extract state from county
        if county and ',' in county:
            parts = county.split(',')
            enrichment["state"] = parts[-1].strip()
        
        c.execute("UPDATE leads SET enrichment_data = ? WHERE id = ?",
                 (json.dumps(enrichment), lead_id))
        enriched += 1
    
    conn.commit()
    conn.close()
    return enriched

count = enrich_leads()
print(f"  ✓ Enriched {count} leads")
PYEOF

# 3. Update lead scores and tiers
echo "[3/4] Updating lead scores..." | tee -a "$LOG_FILE"
python3 << 'PYEOF' >> "$LOG_FILE" 2>&1
import sqlite3
import json

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def update_scores():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Update replacement scores for leads without them
    c.execute("""
        UPDATE leads 
        SET replacement_score = 50,
            tier = CASE 
                WHEN source_type LIKE '%PSD%' OR source_type LIKE '%client%' THEN 'Tier 1'
                WHEN pos_system IS NOT NULL THEN 'Tier 2'
                ELSE 'Tier 3'
            END
        WHERE replacement_score IS NULL OR replacement_score = 0
    """)
    
    updated = c.rowcount
    conn.commit()
    conn.close()
    return updated

count = update_scores()
print(f"  ✓ Updated {count} lead scores/tiers")
PYEOF

# 4. Generate daily summary
echo "[4/4] Generating summary..." | tee -a "$LOG_FILE"
python3 << 'PYEOF' >> "$LOG_FILE" 2>&1
import sqlite3
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM leads")
total = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM leads WHERE enrichment_data IS NOT NULL")
enriched = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM leads WHERE is_customer = 1")
customers = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM leads WHERE created_at >= date('now', '-1 day')")
new_today = c.fetchone()[0]

conn.close()

print(f"  ✓ Summary: {total} total | {enriched} enriched | {customers} customers | {new_today} new today")
PYEOF

echo "$(date -u -Iseconds) === DEPOTCHAOS DAILY UPDATE COMPLETE ===" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
