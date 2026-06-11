#!/bin/bash
# Real Lead Enrichment - Bulk Processing
# Processes all 121 lead files with comprehensive enrichment

LEADS_DIR="/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads"
ENRICHED_DIR="$LEADS_DIR/enriched"
LOG_FILE="/var/log/aos/bulk_enrichment_$(date +%Y%m%d_%H%M%S).log"
REPORT_FILE="$LEADS_DIR/enrichment_report_$(date +%Y%m%d_%H%M%S).md"

mkdir -p "$ENRICHED_DIR"

echo "[$(date -Iseconds)] Starting REAL bulk enrichment on all leads..." | tee -a "$LOG_FILE"
echo "[$(date -Iseconds)] Found $(ls -1 "$LEADS_DIR"/*.{xlsx,csv,json} 2>/dev/null | wc -l) lead files" | tee -a "$LOG_FILE"

# Process each file
for file in "$LEADS_DIR"/*.xlsx "$LEADS_DIR"/*.csv "$LEADS_DIR"/*.json; do
    [ -f "$file" ] || continue
    
    filename=$(basename "$file")
    echo "[$(date -Iseconds)] Processing: $filename" | tee -a "$LOG_FILE"
    
    # Run Python enrichment
    cd "$LEADS_DIR"
    python3 enrich_leads.py --input "$file" --output "$ENRICHED_DIR/enriched_$filename" --real-data 2>> "$LOG_FILE"
    
    echo "[$(date -Iseconds)] Completed: $filename" | tee -a "$LOG_FILE"
done

echo "[$(date -Iseconds)] Bulk enrichment complete" | tee -a "$LOG_FILE"
echo "Results saved to: $ENRICHED_DIR/" | tee -a "$LOG_FILE"
