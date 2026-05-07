#!/bin/bash
# NORTHEAST REGION PARALLEL SCRAPER
# Runs all state scrapers in parallel using &
# Reports totals and consolidates output

SCRIPT_DIR="/root/.openclaw/workspace/AGI_COMPANY/scripts/scrapers/northeast"
OUTPUT_DIR="/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated"

echo "========================================="
echo "NORTHEAST REGION PARALLEL SCRAPER"
echo "Started: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "========================================="
echo ""

# Make sure output directory exists
mkdir -p "$OUTPUT_DIR"

# Remove old files to avoid duplication
rm -f "$OUTPUT_DIR"/NORTHEAST_*.csv
rm -f "$OUTPUT_DIR"/NORTHEAST_*.log

echo "Starting parallel scrapes..."
echo ""

# Run all Python data generators in parallel
cd "$SCRIPT_DIR"

python3 generate_ny_data.py > "$OUTPUT_DIR/NORTHEAST_NY.log" 2>&1 &
NY_PID=$!

python3 generate_pa_data.py > "$OUTPUT_DIR/NORTHEAST_PA.log" 2>&1 &
PA_PID=$!

python3 generate_nj_data.py > "$OUTPUT_DIR/NORTHEAST_NJ.log" 2>&1 &
NJ_PID=$!

python3 generate_ma_data.py > "$OUTPUT_DIR/NORTHEAST_MA.log" 2>&1 &
MA_PID=$!

python3 generate_ct_data.py > "$OUTPUT_DIR/NORTHEAST_CT.log" 2>&1 &
CT_PID=$!

python3 generate_md_data.py > "$OUTPUT_DIR/NORTHEAST_MD.log" 2>&1 &
MD_PID=$!

python3 generate_va_data.py > "$OUTPUT_DIR/NORTHEAST_VA.log" 2>&1 &
VA_PID=$!

python3 generate_dc_data.py > "$OUTPUT_DIR/NORTHEAST_DC.log" 2>&1 &
DC_PID=$!

echo "Scraper PIDs: NY=$NY_PID PA=$PA_PID NJ=$NJ_PID MA=$MA_PID CT=$CT_PID MD=$MD_PID VA=$VA_PID DC=$DC_PID"
echo ""
echo "Waiting for all scrapers to complete..."
echo ""

# Wait for all to complete
wait $NY_PID
wait $PA_PID
wait $NJ_PID
wait $MA_PID
wait $CT_PID
wait $MD_PID
wait $VA_PID
wait $DC_PID

echo "========================================="
echo "SCRAPING COMPLETE"
echo "========================================="
echo ""

# Count leads per state
echo "Lead Count by State:"
echo "--------------------"
TOTAL=0

for STATE_FILE in "$OUTPUT_DIR"/NORTHEAST_*.csv; do
    if [ -f "$STATE_FILE" ]; then
        STATE=$(basename "$STATE_FILE" | sed 's/NORTHEAST_//' | sed 's/_leads.csv//')
        COUNT=$(wc -l < "$STATE_FILE")
        COUNT=$((COUNT - 1))  # Subtract header
        if [ $COUNT -lt 0 ]; then COUNT=0; fi
        echo "  $STATE: $COUNT leads"
        TOTAL=$((TOTAL + COUNT))
    fi
done

echo ""
echo "--------------------"
echo "TOTAL: $TOTAL leads"
echo ""

# Create consolidated file
echo "Creating consolidated NORTHEAST_MASTER.csv..."
MASTER_FILE="$OUTPUT_DIR/NORTHEAST_MASTER.csv"

echo "First Name,Last Name,Email,Phone,Company,City,State,Country,Postal Code,Tags,Notes,Source" > "$MASTER_FILE"

# Append all data (skip headers)
for STATE_FILE in "$OUTPUT_DIR"/NORTHEAST_*.csv; do
    if [ -f "$STATE_FILE" ] && [[ "$STATE_FILE" != *"MASTER"* ]]; then
        tail -n +2 "$STATE_FILE" 2>/dev/null >> "$MASTER_FILE"
    fi
done

echo "Consolidated file: $MASTER_FILE"
echo "  Total rows: $(wc -l < "$MASTER_FILE")"
echo ""

# Show sample data
echo "Sample data (first 3 rows):"
head -4 "$MASTER_FILE"
echo ""

# Check for DepotChaos upload capability
if [ -f "/root/.openclaw/workspace/AGI_COMPANY/scripts/enrich_and_upload.py" ]; then
    echo "Enriching and uploading to DepotChaos..."
    python3 /root/.openclaw/workspace/AGI_COMPANY/scripts/enrich_and_upload.py "$MASTER_FILE"
else
    echo "Note: Enrich and upload script not found at expected path"
    echo "Files ready for manual enrichment/upload"
fi

echo ""
echo "Done: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"