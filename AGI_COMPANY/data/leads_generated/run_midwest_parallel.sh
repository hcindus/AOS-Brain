#!/bin/bash
# MIDWEST REGION SCRAPER - Parallel Execution
# Runs scrapers for: IL, OH, MI, IN, WI, MN, MO, IA, KS, NE

OUTPUT_DIR="/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated"
SCRAPER_SCRIPT="/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/scrapers/midwest_scraper.py"
DB_PATH="/root/.openclaw/workspace/data/depot_chaos/unified.db"
LOG_FILE="/var/log/aos/midwest_scrape_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$OUTPUT_DIR"
mkdir -p "/var/log/aos"

echo "==========================================" | tee -a "$LOG_FILE"
echo "MIDWEST REGION SCRAPER - $(date)" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

# ============================================================
# MIDWEST STATES CONFIGURATION
# ============================================================
# Format: STATE_CODE:SAMPLE_SIZE:CITY_FOCUS
# Higher sample sizes for major markets

declare -A STATES
STATES=(
    ["IL"]="150:Chicago"        # Illinois - Chicago focus
    ["OH"]="150:Columbus"       # Ohio - Cleveland, Cincinnati, Columbus
    ["MI"]="120:Detroit"        # Michigan - Detroit focus
    ["IN"]="100:Indianapolis"   # Indiana - Indianapolis focus
    ["WI"]="100:Milwaukee"      # Wisconsin - Milwaukee, Madison
    ["MN"]="100:Minneapolis"    # Minnesota - Minneapolis, St Paul
    ["MO"]="120:Kansas City"    # Missouri - Kansas City, St Louis
    ["IA"]="80:Des Moines"      # Iowa - Des Moines focus
    ["KS"]="80:Wichita"         # Kansas - Wichita, Kansas City
    ["NE"]="60:Omaha"           # Nebraska - Omaha, Lincoln
)

TOTAL_LEADS=0

# ============================================================
# RUN SCRAPERS IN PARALLEL BACKGROUND PROCESSES
# ============================================================

echo "" | tee -a "$LOG_FILE"
echo "--- LAUNCHING PARALLEL SCRAPERS ---" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

PIDS=()

for STATE_CODE in "${!STATES[@]}"; do
    CONFIG="${STATES[$STATE_CODE]}"
    SAMPLE_SIZE=$(echo "$CONFIG" | cut -d: -f1)
    FOCUS=$(echo "$CONFIG" | cut -d: -f2)
    
    OUTPUT_JSON="$OUTPUT_DIR/MIDWEST_${STATE_CODE}_$(date +%Y%m%d_%H%M%S).json"
    OUTPUT_CSV="$OUTPUT_DIR/MIDWEST_${STATE_CODE}_$(date +%Y%m%d_%H%M%S).csv"
    
    echo "[$STATE_CODE] Launching scraper for $SAMPLE_SIZE leads..." | tee -a "$LOG_FILE"
    
    # Run scraper in background
    python3 "$SCRAPER_SCRIPT" \
        --state "$STATE_CODE" \
        --sample-size "$SAMPLE_SIZE" \
        --output "$OUTPUT_JSON" \
        >> "$LOG_FILE" 2>&1 &
    
    PIDS+=($!)
    
    # Small stagger to avoid resource contention
    sleep 0.5
done

echo "" | tee -a "$LOG_FILE"
echo "--- WAITING FOR ALL SCRAPERS TO COMPLETE ---" | tee -a "$LOG_FILE"
echo "Started ${#PIDS[@]} parallel processes: ${PIDS[*]}" | tee -a "$LOG_FILE"

# Wait for all background processes
WAITED=0
for PID in "${PIDS[@]}"; do
    wait $PID
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✓ Process $PID completed successfully" | tee -a "$LOG_FILE"
    else
        echo "✗ Process $PID failed with exit code $EXIT_CODE" | tee -a "$LOG_FILE"
    fi
    ((WAITED++))
    echo "Progress: $WAITED/${#PIDS[@]} completed" | tee -a "$LOG_FILE"
done

echo "" | tee -a "$LOG_FILE"
echo "--- SCRAPING COMPLETE ---" | tee -a "$LOG_FILE"

# ============================================================
# COUNT GENERATED LEADS
# ============================================================

echo "" | tee -a "$LOG_FILE"
echo "--- PER-STATE RESULTS ---" | tee -a "$LOG_FILE"

for STATE_CODE in "${!STATES[@]}"; do
    CONFIG="${STATES[$STATE_CODE]}"
    SAMPLE_SIZE=$(echo "$CONFIG" | cut -d: -f1)
    
    JSON_FILE=$(ls -t "$OUTPUT_DIR"/MIDWEST_${STATE_CODE}_*.json 2>/dev/null | head -1)
    if [ -f "$JSON_FILE" ]; then
        COUNT=$(python3 -c "import json; d=json.load(open('$JSON_FILE')); print(len(d))" 2>/dev/null || echo "0")
        echo "$STATE_CODE: $COUNT leads" | tee -a "$LOG_FILE"
        TOTAL_LEADS=$((TOTAL_LEADS + COUNT))
    else
        echo "$STATE_CODE: NO FILE FOUND" | tee -a "$LOG_FILE"
    fi
done

echo "" | tee -a "$LOG_FILE"
echo "--- TOTAL ---" | tee -a "$LOG_FILE"
echo "TOTAL LEADS GENERATED: $TOTAL_LEADS" | tee -a "$LOG_FILE"

# ============================================================
# IMPORT TO DEPOT CHAOS DATABASE
# ============================================================

echo "" | tee -a "$LOG_FILE"
echo "--- IMPORTING TO DEPOT CHAOS DB ---" | tee -a "$LOG_FILE"

IMPORT_SCRIPT="/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/import_midwest_to_db.py"
if [ -f "$IMPORT_SCRIPT" ]; then
    python3 "$IMPORT_SCRIPT" --input-dir "$OUTPUT_DIR" >> "$LOG_FILE" 2>&1
    echo "Import complete. Check log for details." | tee -a "$LOG_FILE"
else
    echo "Import script not found: $IMPORT_SCRIPT" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"
echo "MIDWEST SCRAPE COMPLETE: $(date)" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

# Summary output
echo ""
echo "📊 FINAL SUMMARY:"
echo "   Total Leads: $TOTAL_LEADS"
echo "   Files: $OUTPUT_DIR/MIDWEST_*.csv"
echo "   Log: $LOG_FILE"
