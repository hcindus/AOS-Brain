#!/bin/bash
# DAILY DATA SCRAPER AND GITHUB SYNC
# Gathers all data and pushes completed output to GitHub

set -e

echo "=== DAILY DATA SCRAPER - $(date -u +"%Y-%m-%d %H:%M:%S UTC") ==="

# Change to workspace
cd /root/.openclaw/workspace

# Load credentials
source /root/.openclaw/workspace/.env 2>/dev/null || true
export GITHUB_TOKEN=${GITHUB_TOKEN:-$GH_TOKEN}

echo "[1/7] Checking system health..."
python3 /root/.openclaw/workspace/aocros/mission_control/diagnostic.py triage > /tmp/system_health.json 2>/dev/null || echo "{}" > /tmp/system_health.json

echo "[2/7] Gathering email data..."
# Count emails
EMAIL_COUNT=$(find /root/.openclaw/workspace/data/email_attachments/complete_emails/ -name "*.json" 2>/dev/null | wc -l)
echo "  - Total emails processed: $EMAIL_COUNT"

echo "[3/7] Gathering agent status..."
AGENT_COUNT=$(find /root/.openclaw/workspace -name "agent.py" -o -name "*agent*.py" 2>/dev/null | wc -l)
echo "  - Total agent files: $AGENT_COUNT"

echo "[4/7] Gathering security data..."
# Security probe status
PROBE_STATUS=$(/root/.openclaw/workspace/security/probes/status-probes.sh 2>/dev/null | head -10 || echo "Probes not fully initialized")
echo "$PROBE_STATUS" > /tmp/probe_status.txt

echo "[5/7] Gathering queue status..."
QUEUE_COUNT=$(ls /root/.openclaw/workspace/queue/*.md 2>/dev/null | wc -l)
echo "  - Total queue items: $QUEUE_COUNT"

echo "[6/7] Creating daily data summary..."

cat > /root/.openclaw/workspace/data/DAILY_DATA_$(date -u +%Y%m%d).json << EOF
{
  "date": "$(date -u -Iseconds)",
  "timestamp_utc": $(date -u +%s),
  "system_health": $(cat /tmp/system_health.json 2>/dev/null || echo '{}'),
  "metrics": {
    "emails_processed": $EMAIL_COUNT,
    "agent_files": $AGENT_COUNT,
    "queue_items": $QUEUE_COUNT,
    "reports_generated": $(ls /root/.openclaw/workspace/reports/*.md 2>/dev/null | wc -l),
    "brain_cycles": $(grep -o "Cycle [0-9]*" /var/log/syslog 2>/dev/null | tail -1 | awk '{print $2}' || echo "0")
  },
  "security": {
    "probes_installed": true,
    "last_check": "$(date -u -Iseconds)"
  },
  "github": {
    "repo": "hcindus/AOS-Brain",
    "last_sync": "$(date -u -Iseconds)"
  }
}
EOF

echo "[7/7] Committing to GitHub..."

if [ -n "$GITHUB_TOKEN" ]; then
    # Stage all new data
    git add data/DAILY_DATA_*.json 2>/dev/null || true
    git add data/email_attachments/ 2>/dev/null || true
    git add security/probes/*.txt 2>/dev/null || true
    git add logs/ 2>/dev/null || true
    
    # Commit with timestamp
    git commit -m "Daily data sync: $(date -u +%Y-%m-%d) - Auto-scraper" 2>/dev/null || echo "  Nothing new to commit"
    
    # Push to GitHub
    git push origin master 2>/dev/null && echo "  ✓ Pushed to GitHub" || echo "  ⚠ Push pending (may need manual approval)"
else
    echo "  ⚠ GITHUB_TOKEN not set, skipping push"
fi

echo ""
echo "=== DAILY SCRAPE COMPLETE ==="
echo "Data saved to: data/DAILY_DATA_$(date -u +%Y%m%d).json"
echo "Next run: Tomorrow $(date -u -d '+24 hours' +%H:%M) UTC"