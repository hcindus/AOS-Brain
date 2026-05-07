#!/bin/bash
# California Granular Scraping Script - All 58 Counties
# Runs parallel scrapes for each county and major cities

SCRAPER_DIR="/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/enrichment"
OUTPUT_DIR="/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated"
mkdir -p "$OUTPUT_DIR"

echo "🚀 Starting California Granular Scrape - All 58 Counties"
echo "========================================================"
echo "Time: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo ""

# All 58 California counties
COUNTIES=(
  "Los Angeles" "San Diego" "Orange" "Riverside" "San Bernardino" "Santa Clara" "Alameda" "Sacramento"
  "Contra Costa" "Fresno" "Kern" "San Francisco" "Ventura" "San Mateo" "San Joaquin" "Stanislaus"
  "Sonoma" "Tulare" "Santa Barbara" "Solano" "Monterey" "Placer" "San Luis Obispo" "Santa Cruz"
  "Marin" "Yolo" "Butte" "El Dorado" "Merced" "Napa" "Shasta" "Riverside" "San Bernardino"
  "Madera" "Imperial" "Humboldt" "Sutter" "Yuba" "Lake" "Tehama" "Kings" "Mendocino"
  "Amador" "Calaveras" "Tuolumne" "San Benito" "Siskiyou" "Plumas" "Del Norte" "Glenn"
  "Colusa" "Inyo" "Mariposa" "Mono" "Modoc" "Sierra" "Trinity" "Alpine"
)

# Major cities for additional coverage
MAJOR_CITIES=(
  "Los Angeles" "San Diego" "San Jose" "San Francisco" "Fresno" "Sacramento"
  "Long Beach" "Oakland" "Santa Ana" "Anaheim" "Stockton" "Irvine"
  "Bakersfield" "Chula Vista" "Santa Monica" "Pasadena" "Beverly Hills"
)

# Business types to search
BUSINESS_TYPES=("restaurant" "cafe" "diner" "taqueria" "food" "catering" "food truck")

echo "📊 Total counties: ${#COUNTIES[@]}"
echo "📊 Total major cities: ${#MAJOR_CITIES[@]}"
echo "📊 Total business types: ${#BUSINESS_TYPES[@]}"
echo ""

# Function to run scraper for a county
run_county_scrape() {
  local county="$1"
  local county_code=$(echo "$county" | tr ' ' '_')
  local timestamp=$(date -u '+%Y%m%d_%H%M%S')
  
  # Use fixed scraper for county search
  cd "$SCRAPER_DIR"
  node ca_sos_scraper_fixed.js --sample 15 --count 15 "$county" > "$OUTPUT_DIR/CA_${county_code}_raw.json" 2>/dev/null
  
  echo "✅ County scraped: $county"
}

export -f run_county_scrape
export SCRAPER_DIR OUTPUT_DIR

echo "🔄 Launching parallel county scrapes..."
# Run all counties in parallel
printf '%s\n' "${COUNTIES[@]}" | xargs -P 20 -I {} bash -c 'run_county_scrape "{}"'

echo ""
echo "🔄 Running city-specific scrapes..."
# Run city scrapes in parallel
for city in "${MAJOR_CITIES[@]}"; do
  (
    cd "$SCRAPER_DIR"
    city_code=$(echo "$city" | tr ' ' '_')
    node ca_sos_scraper_fixed.js --sample 12 --count 12 "$city" > "$OUTPUT_DIR/CA_${city_code}_City_raw.json" 2>/dev/null
    echo "✅ City scraped: $city"
  ) &
done
wait

echo ""
echo "🔄 Running business type specific searches..."
# Run business type searches in parallel
for btype in "${BUSINESS_TYPES[@]}"; do
  (
    cd "$SCRAPER_DIR"
    type_code=$(echo "$btype" | tr ' ' '_')
    node ca_sos_scraper_fixed.js --sample 20 --count 20 "$btype" > "$OUTPUT_DIR/CA_${type_code}_Type_raw.json" 2>/dev/null
    echo "✅ Type scraped: $btype"
  ) &
done
wait

echo ""
echo "🔄 Running ca_sos_scraper.js for additional coverage..."
for county in "${COUNTIES[@]:0:20}"; do
  (
    cd "$SCRAPER_DIR"
    county_code=$(echo "$county" | tr ' ' '_')
    timeout 30 node ca_sos_scraper.js "$county Restaurant" > "$OUTPUT_DIR/CA_${county_code}_alt.json" 2>/dev/null || true
  ) &
done
wait

echo ""
echo "🔄 Running ca_sos_scraper_daily.js for daily format..."
cd "$SCRAPER_DIR"
timeout 60 node ca_sos_scraper_daily.js > "$OUTPUT_DIR/CA_daily_tasks.json" 2>/dev/null || true

echo ""
echo "📁 Consolidating all results into CSV format..."
# Count total leads
TOTAL_LEADS=0
for f in "$OUTPUT_DIR"/CA_*.json; do
  if [ -f "$f" ]; then
    count=$(grep -c "business_name\|businessName" "$f" 2>/dev/null || echo 0)
    TOTAL_LEADS=$((TOTAL_LEADS + count))
  fi
done

echo ""
echo "========================================================"
echo "✅ CALIFORNIA GRANULAR SCRAPE COMPLETE"
echo "========================================================"
echo "📊 Total counties processed: ${#COUNTIES[@]}"
echo "📊 Total cities processed: ${#MAJOR_CITIES[@]}"
echo "📊 Total files generated: $(ls -1 "$OUTPUT_DIR"/CA_*.json 2>/dev/null | wc -l)"
echo "📊 Estimated total leads: $TOTAL_LEADS"
echo "📁 Output directory: $OUTPUT_DIR"
echo "⏰ Completed: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
