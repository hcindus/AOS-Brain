#!/bin/bash
# Parallel Texas Scraper - Run all metros simultaneously

SCRAPER_DIR="/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/enrichment"
OUTPUT_DIR="/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated"

# Metro areas with target counts
# Format: CITY_NAME|TARGET_COUNT|OUTPUT_FILENAME
declare -a METROS=(
    "Houston|300|TX_Houston.csv"
    "Dallas|250|TX_Dallas.csv"
    "Fort Worth|150|TX_FortWorth.csv"
    "San Antonio|200|TX_SanAntonio.csv"
    "Austin|150|TX_Austin.csv"
    "El Paso|100|TX_ElPaso.csv"
    "Corpus Christi|75|TX_CorpusChristi.csv"
    "Amarillo|50|TX_Amarillo.csv"
    "Lubbock|50|TX_Lubbock.csv"
    "Waco|50|TX_Waco.csv"
    "Beaumont|50|TX_Beaumont.csv"
    "Midland|50|TX_Midland.csv"
    "Odessa|50|TX_Odessa.csv"
)

# Function to scrape a single metro
scrape_metro() {
    local city=$1
    local count=$2
    local output=$3
    
    echo "[START] Scraping $city (target: $count)"
    
    # Run scraper with city-specific output
    cd "$SCRAPER_DIR" && python3 tx_scraper_fixed.py --city "$city" --sample $count --format csv 2>&1 | tee "/tmp/tx_${city}.log"
    
    # Move output to correct location with correct name
    if [ -f "$SCRAPER_DIR/../leads/TX_"*.csv ]; then
        mv "$SCRAPER_DIR/../leads/TX_"*.csv "$OUTPUT_DIR/$output" 2>/dev/null || cp "$SCRAPER_DIR/../leads/TX_"*.csv "$OUTPUT_DIR/$output"
        echo "[DONE] $city -> $output ($(wc -l < "$OUTPUT_DIR/$output" 2>/dev/null || echo 0) lines)"
    else
        echo "[WARN] No output file for $city"
    fi
}

export -f scrape_metro
export SCRAPER_DIR OUTPUT_DIR

# Run all metros in parallel
echo "Starting parallel Texas scrape for ${#METROS[@]} metros..."
for metro in "${METROS[@]}"; do
    IFS='|' read -r city count output <<< "$metro"
    scrape_metro "$city" "$count" "$output" &
done

# Wait for all background jobs
wait
echo "All parallel scrapes completed!"
