#!/bin/bash
# Run All Scrapers - Performance Supply Depot
# Multi-region lead generation

set -e

echo "=========================================="
echo "🌍 MULTI-REGION SCRAPER RUNNER"
echo "Started: $(date -u)"
echo "=========================================="

# Change to workspace
cd /root/.openclaw/workspace

# Run multi-region scraper
echo ""
echo "[1/3] Running multi-region scraper..."
python3 /root/.openclaw/workspace/scripts/scrapers/multi_region_scraper.py

# Run CA ABC scraper (existing)
echo ""
echo "[2/3] Running CA ABC daily scraper..."
python3 /root/.openclaw/workspace/scripts/daily_lead_scraper.py

# Auto-trigger enrichment
echo ""
echo "[3/3] Running auto-enrichment..."
python3 /root/.openclaw/workspace/scripts/scrapers/auto_enrich_trigger.py

# Final stats
echo ""
echo "=========================================="
echo "📊 FINAL STATS"
sqlite3 /root/.openclaw/workspace/DepotChaos/depot_chaos.db "SELECT 'Total: ' || COUNT(*), 'With Phone: ' || COUNT(CASE WHEN phone IS NOT NULL AND phone != '' THEN 1 END), 'With Email: ' || COUNT(CASE WHEN email IS NOT NULL AND email != '' THEN 1 END) FROM vendors;"
echo "=========================================="
echo "Complete: $(date -u)"
echo "=========================================="
