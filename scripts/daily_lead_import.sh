#!/bin/bash
#
# Daily Lead Import to DepotChaos
# Imports CREAM realtor prospects and enriches leads
# Runs daily at 03:00 UTC
#

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/aos/daily_lead_import.log"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
DATESTAMP=$(date -u +"%Y%m%d")

# Logging function
log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

mkdir -p "$(dirname $LOG_FILE)"

log "=== Daily Lead Import Started ==="

# ═══════════════════════════════════════════════════════════════════
# STEP 1: Find today's CREAM prospects
# ═══════════════════════════════════════════════════════════════════
TODAY=$(date -u +"%Y-%m-%d")
PROSPECTS_DIR="$WORKSPACE/AGI_COMPANY/subsidiaries/CREAM/sales/prospects"
TODAY_CSV="$PROSPECTS_DIR/realtor_prospects_$TODAY.csv"
TODAY_JSON="$PROSPECTS_DIR/realtor_prospects_$TODAY.json"

if [ ! -f "$TODAY_CSV" ]; then
    log "⚠️ Today's prospects not found: $TODAY_CSV"
    log "Checking for any available prospects..."
    TODAY_CSV=$(ls -t $PROSPECTS_DIR/realtor_prospects_*.csv 2>/dev/null | head -1)
    if [ -z "$TODAY_CSV" ]; then
        log "❌ No prospect files found. Exiting."
        exit 1
    fi
    log "Using most recent: $TODAY_CSV"
fi

log "Found prospects file: $TODAY_CSV"

# ═══════════════════════════════════════════════════════════════════
# STEP 2: Run Python import script
# ═══════════════════════════════════════════════════════════════════
cd "$WORKSPACE"

python3 << PYTHON_EOF
import sqlite3
import csv
import uuid
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "$WORKSPACE/data/depot_chaos/unified.db"
CSV_PATH = "$TODAY_CSV"

def import_daily_prospects():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Ensure leads table exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY,
            company_name TEXT,
            county TEXT,
            status TEXT DEFAULT 'new',
            tier TEXT,
            pos_system TEXT,
            replacement_score INTEGER DEFAULT 50,
            source_type TEXT,
            assigned_agent TEXT DEFAULT 'Miles',
            enrichment_data TEXT,
            created_at TEXT,
            last_contact TEXT,
            email_count INTEGER DEFAULT 0,
            response_count INTEGER DEFAULT 0
        )
    ''')
    
    # Get existing count
    c.execute("SELECT COUNT(*) FROM leads")
    existing = c.fetchone()[0]
    print(f"Existing leads: {existing}")
    
    # Get existing companies for duplicate check (business_name + city + state)
    c.execute("SELECT business_name, city, state FROM leads")
    existing_companies = set((row[0], row[1], row[2]) for row in c.fetchall())
    
    imported = 0
    skipped = 0
    
    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Let SQLite auto-generate the ID
            
            # Map CREAM fields to DepotChaos schema
            company = row.get('company_name', '')
            contact = row.get('contact_name', '')
            email = row.get('email', '')
            phone = row.get('phone', '')
            city = row.get('city', '')
            state = row.get('state', '')
            priority = row.get('priority', 'C')
            experience = row.get('experience_years', '0')
            brokerage = row.get('brokerage', '')
            
            # Skip duplicates (check business_name + city + state)
            company_key = (company, city, state)
            if company_key in existing_companies:
                skipped += 1
                continue
            
            # Calculate tier and score
            tier = f"Tier {priority}" if priority in ['A', 'B', 'C'] else 'Tier C'
            score = 50
            if priority == 'A':
                score = 90
            elif priority == 'B':
                score = 70
            
            # Build enrichment data
            enrichment = {
                'contact_name': contact,
                'email': email,
                'phone': phone,
                'city': city,
                'state': state,
                'experience_years': experience,
                'brokerage': brokerage,
                'industry': 'RealEstate',
                'priority': priority,
                'import_date': datetime.now().isoformat(),
                'source_file': Path(CSV_PATH).name
            }
            
            # Insert lead - match schema with business_name as primary key
            c.execute("""
                INSERT INTO leads (
                    business_name, company_name, city, state, status, tier,
                    replacement_score, source_type, assigned_agent, email, phone,
                    enrichment_data, created_at, contact_name, enrichment_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
            """, (
                company, company, city, state, 'new', tier,
                score, 'CREAM_RealEstate_Daily', 'Miles', email, phone,
                json.dumps(enrichment), datetime.now().isoformat(), contact
            ))
            
            imported += 1
            existing_companies.add(company_key)
    
    conn.commit()
    
    # Final count
    c.execute("SELECT COUNT(*) FROM leads")
    final_count = c.fetchone()[0]
    
    # Get breakdown by tier for today's imports
    c.execute("SELECT tier, COUNT(*) FROM leads WHERE source_type = 'CREAM_RealEstate_Daily' AND created_at LIKE ? GROUP BY tier", (f'{datetime.now().strftime("%Y-%m-%d")}%',))
    tier_breakdown = c.fetchall()
    
    conn.close()
    
    print(f"\n✅ Import complete:")
    print(f"   Imported: {imported}")
    print(f"   Skipped (duplicates): {skipped}")
    print(f"   Previous count: {existing}")
    print(f"   Final count: {final_count}")
    print(f"\n   By Tier:")
    for tier, count in tier_breakdown:
        print(f"      {tier}: {count}")
    
    return imported, skipped, final_count

if __name__ == "__main__":
    import_daily_prospects()
PYTHON_EOF

IMPORT_STATUS=$?
if [ $IMPORT_STATUS -eq 0 ]; then
    log "✅ Lead import completed successfully"
else
    log "❌ Lead import failed with exit code $IMPORT_STATUS"
fi

# ═══════════════════════════════════════════════════════════════════
# STEP 3: Update daily stats
# ═══════════════════════════════════════════════════════════════════
python3 << PYTHON_EOF
import sqlite3
import json
from datetime import datetime

DB_PATH = "$WORKSPACE/data/depot_chaos/unified.db"
STATS_FILE = "$WORKSPACE/data/depot_chaos/daily_stats.json"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Get current stats
c.execute("SELECT COUNT(*) FROM leads")
total_leads = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM leads WHERE status = 'new'")
new_leads = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM leads WHERE status = 'contacted'")
contacted = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM leads WHERE source_type LIKE '%CREAM%'")
cream_leads = c.fetchone()[0]

conn.close()

stats = {
    "last_import": "$TIMESTAMP",
    "total_leads": total_leads,
    "new_leads": new_leads,
    "contacted": contacted,
    "cream_leads": cream_leads,
    "date": "$TODAY"
}

with open(STATS_FILE, 'w') as f:
    json.dump(stats, f, indent=2)

print(f"Stats updated: {stats}")
PYTHON_EOF

log "=== Daily Lead Import Complete ==="
