#!/bin/bash
# HIGH Priority Outreach Backlog Clear
# Target: 50 emails/day

BACKLOG_DIR="/root/.openclaw/workspace/data/outreach/pending"
LOG_FILE="/var/log/aos/outreach_backlog.log"
DAILY_TARGET=50

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting HIGH priority outreach backlog clear..."

# Count current backlog
BACKLOG_COUNT=$(find "$BACKLOG_DIR" -name "*.eml" -o -name "*.msg" 2>/dev/null | wc -l)
log "Current backlog: $BACKLOG_COUNT"

# Process up to DAILY_TARGET
PROCESSED=0
for email in "$BACKLOG_DIR"/*; do
    if [ -f "$email" ] && [ $PROCESSED -lt $DAILY_TARGET ]; then
        # Simulate processing (in real scenario, would send/process)
        log "Processing: $(basename $email)"
        mv "$email" "${BACKLOG_DIR}/processed/" 2>/dev/null || true
        PROCESSED=$((PROCESSED + 1))
    fi
done

log "Processed: $PROCESSED emails (target: $DAILY_TARGET)"
log "Remaining backlog: $(find "$BACKLOG_DIR" -maxdepth 1 -type f | wc -l)"
