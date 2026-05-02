#!/bin/bash
# Daily Lead Scraper - Performance Supply Depot
# Runs daily at 6 AM UTC to scrape new leads

set -e

echo "=== DAILY LEAD SCRAPER - $(date -u +"%Y-%m-%d %H:%M:%S UTC") ==="

# Change to workspace
cd /root/.openclaw/workspace

# Run the scraper
echo "[1/3] Running daily lead scraper..."
python3 /root/.openclaw/workspace/scripts/daily_lead_scraper.py

echo "[2/3] Running enrichment on new leads..."
# Run yelp enrichment on new leads
cd /root/.openclaw/workspace/DepotChaos
python3 /root/.openclaw/workspace/DepotChaos/yelp_enrichment.py 2>&1 | tail -20

echo "[3/3] Generating report..."
# Count stats
TOTAL=$(sqlite3 /root/.openclaw/workspace/DepotChaos/depot_chaos.db "SELECT COUNT(*) FROM vendors;")
WITH_PHONE=$(sqlite3 /root/.openclaw/workspace/DepotChaos/depot_chaos.db "SELECT COUNT(*) FROM vendors WHERE phone IS NOT NULL AND phone != '';")

echo ""
echo "=== DAILY SCRAPE COMPLETE ==="
echo "Total vendors: $TOTAL"
echo "With phone: $WITH_PHONE"
echo "Enrichment rate: $(echo "scale=1; $WITH_PHONE * 100 / $TOTAL" | bc)%"
echo "Next run: Tomorrow $(date -u -d '+24 hours' +%H:%M) UTC"
echo ""
