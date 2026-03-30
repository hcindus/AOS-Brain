#!/bin/bash
# lead_enrichment_daemon.sh - Background enrichment for all leads

echo "[$(date)] Starting Lead Enrichment Daemon..."

# Count leads needing enrichment
TX_PENDING=$(cat /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads/TX_leads_2026-03-29.csv | grep "pending" | wc -l)
CA_PENDING=$(cat /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads/CA_leads_2026-03-29_bulk.json | grep -o '"enrichment_status": "pending"' | wc -l)

echo "Pending enrichment: TX=$TX_PENDING, CA=$CA_PENDING"

# Create enrichment queue
python3 /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/tools/working_lead_scraper.py --enrich-mode &

# Log status
echo "[$(date)] Enrichment process started in background" >> /var/log/aos/enrichment.log 2>&1 || echo "[$(date)] Enrichment started"
