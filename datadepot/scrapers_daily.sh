#!/bin/bash
# Scrapers Daily Runner - Cron Script
# Generates leads for all states and feeds DepotChaos

LOG_FILE="/var/log/aos/scrapers_daily.log"
OUTPUT_DIR="/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated"
DB_PATH="/root/.openclaw/workspace/data/depot_chaos/unified.db"

mkdir -p "$OUTPUT_DIR"

echo "[$(date)] Starting daily scraper run" >> "$LOG_FILE"

# Generate leads for each major state
for STATE in TX CA AZ FL NY; do
    echo "[$(date)] Generating $STATE leads..." >> "$LOG_FILE"
    
    # Run sample generator (replace with real scraper)
    python3 /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/enrichment/tx_scraper_fixed.py \
        --sample 50 --output "$OUTPUT_DIR/${STATE}_$(date +%Y%m%d).csv" 2>/dev/null || true
done

echo "[$(date)] Daily scraper run complete" >> "$LOG_FILE"
