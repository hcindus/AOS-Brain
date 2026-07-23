#!/bin/bash
# Refresh leads older than 30 days
# Re-enrich with latest data

DB_PATH="/root/.openclaw/workspace/data/depot_chaos/unified.db"
LOG_FILE="/var/log/aos/lead_refresh.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== LEAD REFRESH (30+ days old) ==="

# Find stale leads
STALE_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM leads WHERE DATE(created_at) < DATE('now', '-30 days') AND (phone IS NULL OR phone = '');" 2>/dev/null)
log "Stale leads needing refresh: $STALE_COUNT"

# Re-enrich first 100 stale leads
log "Re-enriching stale leads via Yelp..."
cd /root/.openclaw/workspace/DepotChaos
python3 yelp_enrichment.py --batch-size 100 2>&1 | tail -5

log "Lead refresh complete"
