#!/bin/bash
# Continuous Rotation Office Protocol
# Processes employee compliance records in batches

COMPLIANCE_DIR="/root/.openclaw/workspace/AGI_COMPANY/compliance"
LOG_FILE="/var/log/aos/rotation_office.log"
BATCH_SIZE=5

mkdir -p "$COMPLIANCE_DIR/processed"
mkdir -p "$COMPLIANCE_DIR/pending"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Rotation Office Protocol Started ==="

# Count pending records
PENDING_COUNT=$(ls "$COMPLIANCE_DIR/pending/"*.md 2>/dev/null | wc -l)
log "Pending compliance records: $PENDING_COUNT"

if [ "$PENDING_COUNT" -eq 0 ]; then
    log "No pending records. Protocol complete."
    exit 0
fi

# Process batch
PROCESSED=0
for record in "$COMPLIANCE_DIR/pending/"*.md; do
    if [ -f "$record" ]; then
        filename=$(basename "$record")
        log "Processing: $filename"
        
        # Move to processed
        mv "$record" "$COMPLIANCE_DIR/processed/"
        
        # Update tracking
        PROCESSED=$((PROCESSED + 1))
        
        if [ "$PROCESSED" -ge "$BATCH_SIZE" ]; then
            log "Batch complete. Processed: $PROCESSED"
            break
        fi
    fi
done

# Calculate new compliance rate
TOTAL_EMPLOYEES=43
PROCESSED_TOTAL=$(ls "$COMPLIANCE_DIR/processed/"*.md 2>/dev/null | wc -l)
COMPLIANCE_RATE=$((PROCESSED_TOTAL * 100 / TOTAL_EMPLOYEES))

log "Compliance rate: $COMPLIANCE_RATE% ($PROCESSED_TOTAL/$TOTAL_EMPLOYEES)"
log "Rotation office protocol batch complete."

# Alert if compliance still low
if [ "$COMPLIANCE_RATE" -lt 50 ]; then
    log "ALERT: Compliance below 50%. Immediate attention required."
fi
