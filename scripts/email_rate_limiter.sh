#!/bin/bash
# Email Rate Limiter - Prevents Hostinger rate limit issues
# Processes email queue in batches with delays

BATCH_SIZE=10
DELAY_BETWEEN_BATCHES=300  # 5 minutes
MAX_RETRIES=3

LOG_FILE="/var/log/aos/email_rate_limiter.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Count emails in queue
QUEUE_COUNT=$(mailq | grep -c "^[A-F0-9]" || echo "0")

if [ "$QUEUE_COUNT" -eq 0 ]; then
    log "No emails in queue"
    exit 0
fi

log "Processing $QUEUE_COUNT emails in batches of $BATCH_SIZE"

# Process in batches
PROCESSED=0
while [ "$PROCESSED" -lt "$QUEUE_COUNT" ]; do
    # Try to flush a batch
    for i in $(seq 1 $BATCH_SIZE); do
        # Get next email ID
        MSG_ID=$(mailq | grep "^[A-F0-9]" | head -1 | awk '{print $1}' | tr -d '*!')
        
        if [ -n "$MSG_ID" ]; then
            # Try to send
            if postsuper -r "$MSG_ID" 2>/dev/null; then
                log "Processed: $MSG_ID"
                ((PROCESSED++))
            else
                log "Failed to process: $MSG_ID"
            fi
        fi
        
        # Small delay between individual emails
        sleep 2
    done
    
    log "Batch complete. Processed: $PROCESSED/$QUEUE_COUNT"
    
    # Wait before next batch
    if [ "$PROCESSED" -lt "$QUEUE_COUNT" ]; then
        log "Waiting ${DELAY_BETWEEN_BATCHES}s before next batch..."
        sleep $DELAY_BETWEEN_BATCHES
    fi
done

log "Email queue processing complete. Total processed: $PROCESSED"
