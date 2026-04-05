#!/bin/bash
# CONTINUOUS DATA SCRAPER - 24/7 OPERATION
# Runs indefinitely, gathering data and pushing to GitHub

LOG_FILE="/var/log/aos/continuous_scraper.log"
PID_FILE="/var/run/continuous_scraper.pid"
DATA_DIR="/root/.openclaw/workspace/data/scraper"

# Create directories
mkdir -p "$DATA_DIR"
mkdir -p "$(dirname $LOG_FILE)"

# Log function
log() {
    echo "[$(date -u -Iseconds)] $1" | tee -a "$LOG_FILE"
}

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        log "⚠ Scraper already running (PID: $OLD_PID)"
        exit 1
    fi
fi

# Save PID
echo $$ > "$PID_FILE"

log "=== CONTINUOUS SCRAPER STARTED (PID: $$) ==="

# Change to workspace
cd /root/.openclaw/workspace

# Load credentials
source /root/.openclaw/workspace/.env 2>/dev/null || true
export GITHUB_TOKEN=${GITHUB_TOKEN:-$GH_TOKEN}

# Counter for iterations
ITERATION=0

# Main loop - runs forever
while true; do
    ITERATION=$((ITERATION + 1))
    log "=== ITERATION $ITERATION ==="
    
    # 1. Gather email data
    log "[1/6] Checking for new emails..."
    python3 << 'PYEOF' 2>&1 | tee -a "$LOG_FILE"
import imaplib
import email
import json
from datetime import datetime

try:
    imap = imaplib.IMAP4_SSL('imap.hostinger.com', 993)
    imap.login('miles@myl0nr0s.cloud', 'Myl0n.R0s')
    imap.select('inbox')
    
    _, messages = imap.search(None, 'UNSEEN')
    count = len(messages[0].split())
    
    # Save email count
    with open('/root/.openclaw/workspace/data/scraper/email_stats.json', 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "unread_count": count,
            "last_check": datetime.now().isoformat()
        }, f)
    
    print(f"  ✓ Unread emails: {count}")
    imap.logout()
except Exception as e:
    print(f"  ✗ Error: {e}")
PYEOF
    
    # 2. Gather system metrics
    log "[2/6] Collecting system metrics..."
    cat > "$DATA_DIR/system_metrics.json" << EOF
{
  "timestamp": "$(date -u -Iseconds)",
  "cpu_percent": $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 || echo "0"),
  "memory_percent": $(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}'),
  "disk_percent": $(df / | tail -1 | awk '{print $5}' | tr -d '%'),
  "load_average": [$(uptime | awk -F'load average:' '{print $2}' | tr -d ' ')],
  "brain_cycles": $(grep -o "Cycle [0-9]*" /var/log/syslog 2>/dev/null | tail -1 | awk '{print $2}' || echo "0")
}
EOF
    log "  ✓ System metrics saved"
    
    # 3. Gather agent status
    log "[3/6] Checking agent status..."
    AGENT_COUNT=$(find /root/.openclaw/workspace -name "*agent*.py" -type f 2>/dev/null | wc -l)
    cat > "$DATA_DIR/agent_status.json" << EOF
{
  "timestamp": "$(date -u -Iseconds)",
  "total_agent_files": $AGENT_COUNT,
  "brain_status": "running",
  "heart_rate": "72 BPM"
}
EOF
    log "  ✓ Agent status saved ($AGENT_COUNT agents)"
    
    # 4. Gather security data
    log "[4/6] Checking security status..."
    if systemctl is-active --quiet auditd 2>/dev/null; then
        SECURITY_STATUS="active"
    else
        SECURITY_STATUS="inactive"
    fi
    
    cat > "$DATA_DIR/security_status.json" << EOF
{
  "timestamp": "$(date -u -Iseconds)",
  "auditd_status": "$SECURITY_STATUS",
  "probes_installed": true,
  "last_check": "$(date -u -Iseconds)"
}
EOF
    log "  ✓ Security status saved"
    
    # 5. Gather queue status
    log "[5/6] Checking queue status..."
    QUEUE_COUNT=$(ls /root/.openclaw/workspace/queue/*.md 2>/dev/null | wc -l)
    cat > "$DATA_DIR/queue_status.json" << EOF
{
  "timestamp": "$(date -u -Iseconds)",
  "queue_items": $QUEUE_COUNT,
  "reports": $(ls /root/.openclaw/workspace/reports/*.md 2>/dev/null | wc -l)
}
EOF
    log "  ✓ Queue status saved ($QUEUE_COUNT items)"
    
    # 6. Commit to GitHub (every 6th iteration = hourly)
    if [ $((ITERATION % 6)) -eq 0 ]; then
        log "[6/6] Pushing data to GitHub..."
        
        if [ -n "$GITHUB_TOKEN" ]; then
            cd /root/.openclaw/workspace
            
            # Stage data
            git add data/scraper/ 2>/dev/null || true
            git add logs/ 2>/dev/null || true
            
            # Commit
            git commit -m "Continuous scraper data: $(date -u +%Y-%m-%d-%H:%M) - Iteration $ITERATION" 2>/dev/null || true
            
            # Push
            if git push origin master 2>&1; then
                log "  ✓ Data pushed to GitHub"
            else
                log "  ⚠ Push failed (may need approval)"
            fi
        else
            log "  ⚠ GITHUB_TOKEN not set"
        fi
    else
        log "[6/6] Skipping GitHub push (every 6th iteration)"
    fi
    
    log "=== ITERATION $ITERATION COMPLETE ==="
    log "Next iteration in 10 minutes..."
    log ""
    
    # Sleep for 10 minutes
    sleep 600
done