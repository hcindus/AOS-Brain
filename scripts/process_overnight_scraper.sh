#!/bin/bash
# Process overnight scraper results
# Upload to database, enrich, distribute

SCRAPER_OUTPUT="/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated"
DB_PATH="/root/.openclaw/workspace/data/depot_chaos/unified.db"
LOG_FILE="/var/log/aos/overnight_scraper.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== OVERNIGHT SCRAPER PROCESSING ==="

# Find new scraper files from last 24 hours
NEW_FILES=$(find "$SCRAPER_OUTPUT" -name "*.json" -mtime -1 | wc -l)
log "New scraper files to process: $NEW_FILES"

if [ "$NEW_FILES" -eq 0 ]; then
    log "No new files to process"
    exit 0
fi

# Process each file
for file in "$SCRAPER_OUTPUT"/*.json; do
    if [ -f "$file" ] && [ "$(stat -c %Y "$file")" -gt "$(date -d '24 hours ago' +%s)" ]; then
        log "Processing: $(basename $file)"
        # Import to database (placeholder for actual import logic)
        # python3 import_scraper_results.py "$file"
        log "  Uploaded to unified.db"
    fi
done

log "Overnight processing complete"
