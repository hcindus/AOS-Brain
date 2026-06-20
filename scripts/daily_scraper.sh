#!/bin/bash
#
# Daily Data Scraper & GitHub Sync
# Runs: [2026-06-20 02:00 UTC]
# Tasks: Scrape data, commit to GitHub
#

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/aos/daily_scraper.log"
DATA_DIR="$WORKSPACE/data/scraper"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
DATESTAMP=$(date -u +"%Y%m%d_%H%M")

# Logging function
log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

mkdir -p "$DATA_DIR"
mkdir -p "$(dirname $LOG_FILE)"

log "=== Daily Scraper & GitHub Sync Started ==="

# ═══════════════════════════════════════════════════════════════════
# STEP 1: Run CREAM Realtor Scraper (if exists)
# ═══════════════════════════════════════════════════════════════════
if [ -f "$WORKSPACE/cream_realtor_scraper.py" ]; then
    log "Running CREAM realtor scraper..."
    cd "$WORKSPACE"
    python3 cream_realtor_scraper.py 2>&1 | tee -a "$LOG_FILE" || log "Warning: CREAM scraper exited with error"
else
    log "CREAM scraper not found, skipping"
fi

# ═══════════════════════════════════════════════════════════════════
# STEP 2: Collect Agent Status Data
# ═══════════════════════════════════════════════════════════════════
log "Collecting agent status..."

cat > "$DATA_DIR/agent_status_$DATESTAMP.json" << EOF
{
  "timestamp": "$TIMESTAMP",
  "datestamp": "$DATESTAMP",
  "source": "daily_scraper",
  "agents": {
    "patricia_factory": $(systemctl is-active patricia-factory 2>/dev/null | grep -c "active" || echo 0),
    "forge_factory": $(systemctl is-active forge-factory 2>/dev/null | grep -c "active" || echo 0),
    "chelios_security": $(systemctl is-active chelios-security 2>/dev/null | grep -c "active" || echo 0),
    "jordan_office": $(systemctl is-active jordan-office 2>/dev/null | grep -c "active" || echo 0),
    "aurora_tasks": $(systemctl is-active aurora-tasks 2>/dev/null | grep -c "active" || echo 0)
  }
}
EOF

log "Agent status saved to agent_status_$DATESTAMP.json"

# ═══════════════════════════════════════════════════════════════════
# STEP 3: Collect Brain Metrics
# ═══════════════════════════════════════════════════════════════════
log "Collecting brain metrics..."

BRAIN_STATUS=$(echo '{"cmd":"status"}' | nc -U /tmp/aos_brain.sock 2>/dev/null || echo '{"error":"socket_unavailable"}')

cat > "$DATA_DIR/brain_metrics_$DATESTAMP.json" << EOF
{
  "timestamp": "$TIMESTAMP",
  "datestamp": "$DATESTAMP",
  "source": "daily_scraper",
  "brain_status": $BRAIN_STATUS
}
EOF

log "Brain metrics saved to brain_metrics_$DATESTAMP.json"

# ═══════════════════════════════════════════════════════════════════
# STEP 4: Sync to GitHub
# ═══════════════════════════════════════════════════════════════════
log "Syncing to GitHub..."

cd "$WORKSPACE"

# Check if git repo
if [ ! -d ".git" ]; then
    log "Error: Not a git repository"
    exit 1
fi

# Configure git if not already done
if ! git config --get user.email > /dev/null 2>&1; then
    git config user.email "miles@myl0nr0s.cloud"
    git config user.name "Miles (AOS)"
fi

# Add all scraped data
git add data/scraper/*.json 2>/dev/null || true
git add AGI_COMPANY/subsidiaries/CREAM/sales/prospects/*.json 2>/dev/null || true
git add AGI_COMPANY/subsidiaries/CREAM/sales/prospects/*.csv 2>/dev/null || true

# Check if there are changes to commit
if git diff --cached --quiet; then
    log "No changes to commit"
else
    git commit -m "Daily data scrape: $DATESTAMP [auto]" 2>&1 | tee -a "$LOG_FILE"
    git push origin main 2>&1 | tee -a "$LOG_FILE" && log "GitHub sync complete" || log "GitHub sync failed"
fi

log "=== Daily Scraper & GitHub Sync Complete ==="
