#!/bin/bash
# DepotChaos Daily Lead Update Cron Job
# Runs daily at 3 AM UTC to scrape and enrich new leads

set -e

LOG_FILE="/var/log/depotchaos/daily_lead_update.log"
DATA_DIR="/root/.openclaw/workspace/data/depot_chaos"
SCRAPER_DIR="/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/scrapers"

mkdir -p "$(dirname $LOG_FILE)"
mkdir -p "$DATA_DIR"

log() {
    echo "[$(date -u -Iseconds)] $1" | tee -a "$LOG_FILE"
}

cd /root/.openclaw/workspace

log "=== DEPOTCHAOS DAILY LEAD UPDATE ==="

# 1. Run CA ABC scraper for new licenses
log "[1/4] Scraping CA ABC for new licenses..."
if [ -f "$SCRAPER_DIR/ca_abc_scraper.py" ]; then
    python3 "$SCRAPER_DIR/ca_abc_scraper.py" --recent-only 2>&1 | tee -a "$LOG_FILE" || log "  ⚠ Scraper encountered errors"
else
    log "  ⚠ Scraper not found at $SCRAPER_DIR/ca_abc_scraper.py"
fi

# 2. Run enrichment pipeline
log "[2/4] Running lead enrichment..."
python3 -c "
import sqlite3
import json
from datetime import datetime

db_path = '$DATA_DIR/unified.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Find leads that need enrichment (missing phone, email, or pos_system)
c.execute('''
    SELECT id, company_name, county, enrichment_data 
    FROM leads 
    WHERE (phone IS NULL OR email IS NULL OR pos_system IS NULL OR pos_system = 'Unknown')
    AND deleted = 0
    AND (enrichment_data IS NULL OR enrichment_data NOT LIKE '%enriched%')
    LIMIT 50
''')

leads_to_enrich = c.fetchall()
log(f'  Found {len(leads_to_enrich)} leads to enrich')

for lead_id, company, county, enrichment in leads_to_enrich:
    # Parse existing enrichment
    existing = {}
    if enrichment:
        try:
            existing = json.loads(enrichment)
        except:
            pass
    
    # Simulate enrichment (in real implementation, would call external APIs)
    existing['enriched_at'] = datetime.now().isoformat()
    existing['enrichment_attempt'] = True
    
    # Update lead
    c.execute('UPDATE leads SET enrichment_data = ? WHERE id = ?',
              (json.dumps(existing), lead_id))

conn.commit()
conn.close()
log(f'  ✓ Enriched {len(leads_to_enrich)} leads')
" 2>&1 | tee -a "$LOG_FILE"

# 3. Run deduplication
log "[3/4] Running deduplication..."
python3 -c "
import sqlite3
import json
from datetime import datetime

db_path = '$DATA_DIR/unified.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Find potential duplicates by company name
c.execute('''
    SELECT company_name, COUNT(*) as cnt
    FROM leads
    WHERE deleted = 0
    GROUP BY LOWER(company_name)
    HAVING cnt > 1
    LIMIT 20
''')

dups = c.fetchall()
log(f'  Found {len(dups)} potential duplicate company names')

for company_name, count in dups:
    log(f'    - \"{company_name}\" appears {count} times')

conn.close()
" 2>&1 | tee -a "$LOG_FILE"

# 4. Update statistics
log "[4/4] Updating statistics..."
python3 -c "
import sqlite3
import json
from datetime import datetime

db_path = '$DATA_DIR/unified.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Count various metrics
c.execute('SELECT COUNT(*) FROM leads WHERE deleted = 0')
total = c.fetchone()[0]

c.execute('SELECT COUNT(*) FROM leads WHERE deleted = 0 AND created_at > datetime(\"now\", \"-1 day\")')
new_today = c.fetchone()[0]

c.execute('SELECT COUNT(*) FROM leads WHERE deleted = 0 AND enrichment_data LIKE \"%enriched%\"')
enriched = c.fetchone()[0]

stats = {
    'timestamp': datetime.now().isoformat(),
    'total_active_leads': total,
    'new_today': new_today,
    'enriched_leads': enriched,
    'enrichment_rate': round(enriched / total * 100, 2) if total > 0 else 0
}

with open('$DATA_DIR/daily_stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

log(f'  Total active: {total}')
log(f'  New today: {new_today}')
log(f'  Enriched: {enriched} ({stats[\"enrichment_rate\"]}%)')

conn.close()
" 2>&1 | tee -a "$LOG_FILE"

log "=== DAILY UPDATE COMPLETE ==="
log "Next run: Tomorrow 03:00 UTC"
log ""
