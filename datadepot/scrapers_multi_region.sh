#!/bin/bash
# Multi-State/Country Restaurant & Cafe Scraper Daily Runner
# Generates leads for TN, all states, Canada, and Mexico

LOG_FILE="/var/log/aos/scrapers_multi_region.log"
OUTPUT_DIR="/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated"
DB_PATH="/root/.openclaw/workspace/data/depot_chaos/unified.db"

mkdir -p "$OUTPUT_DIR/tn"
mkdir -p "$OUTPUT_DIR/us_states"
mkdir -p "$OUTPUT_DIR/canada"
mkdir -p "$OUTPUT_DIR/mexico"

echo "[$(date)] ==========================================" >> "$LOG_FILE"
echo "[$(date)] Starting Multi-Region Restaurant Scraper" >> "$LOG_FILE"
echo "[$(date)] ==========================================" >> "$LOG_FILE"

# Source the Python environment
export PYTHONPATH="/root/.openclaw/workspace:$PYTHONPATH"

# ============================================================
# TENNESSEE - Priority Region
# ============================================================
echo "[$(date)] --- TENNESSEE Priority Run ---" >> "$LOG_FILE"

# Run Tennessee scraper for restaurants
python3 /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/scrapers/tn_restaurant_scraper.py \
    --county all \
    --business-type restaurant,cafe,bar \
    --output "$OUTPUT_DIR/tn/tn_restaurants_$(date +%Y%m%d).json" \
    >> "$LOG_FILE" 2>&1 || echo "[$(date)] TN scraper had errors" >> "$LOG_FILE"

# ============================================================
# US STATES - All Remaining States
# ============================================================
echo "[$(date)] --- US STATES Run ---" >> "$LOG_FILE"

PRIORITY_STATES="TX CA FL NY IL PA OH GA NC MI NJ VA WA AZ MA IN MO MD CO MN WI SC AL LA KY OR OK CT UT NV IA MS AR KS NM NE WV NH ID ME MT RI SD ND DE VT WY AK HI DC"

for STATE in $PRIORITY_STATES; do
    echo "[$(date)] Processing $STATE..." >> "$LOG_FILE"
    
    python3 /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/scrapers/us_state_scraper.py \
        --state $STATE \
        --business-type restaurant,cafe,bar,food_service \
        --sample-size 100 \
        --output "$OUTPUT_DIR/us_states/${STATE}_$(date +%Y%m%d).json" \
        >> "$LOG_FILE" 2>&1 || echo "[$(date)] $STATE scraper had errors" >> "$LOG_FILE"
    
    # Small delay between states
    sleep 2
done

# ============================================================
# CANADA - Provinces
# ============================================================
echo "[$(date)] --- CANADA Run ---" >> "$LOG_FILE"

CANADA_PROVINCES="ON QC BC AB MB SK NS NB NL PE YT NT NU"

for PROV in $CANADA_PROVINCES; do
    echo "[$(date)] Processing Canada province $PROV..." >> "$LOG_FILE"
    
    python3 /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/scrapers/canada_scraper.py \
        --province $PROV \
        --business-type restaurant,cafe,bar \
        --sample-size 50 \
        --output "$OUTPUT_DIR/canada/${PROV}_$(date +%Y%m%d).json" \
        >> "$LOG_FILE" 2>&1 || echo "[$(date)] Canada $PROV scraper had errors" >> "$LOG_FILE"
    
    sleep 2
done

# ============================================================
# MEXICO - States
# ============================================================
echo "[$(date)] --- MEXICO Run ---" >> "$LOG_FILE"

MEXICO_STATES="MX-AG MX-BC MX-BS MX-CM MX-CH MX-CA MX-CL MX-CP MX-DF MX-DG MX-GT MX-GR MX-HG MX-JA MX-EM MX-MI MX-MO MX-NA MX-NL MX-OA MX-PU MX-QE MX-QR MX-SL MX-SI MX-SO MX-TB MX-TM MX-TL MX-VE MX-YU MX-ZA"

for STATE in $MEXICO_STATES; do
    echo "[$(date)] Processing Mexico state $STATE..." >> "$LOG_FILE"
    
    python3 /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/scrapers/mexico_scraper.py \
        --state $STATE \
        --business-type restaurant,cafe,bar,comedor \
        --sample-size 30 \
        --output "$OUTPUT_DIR/mexico/${STATE}_$(date +%Y%m%d).json" \
        >> "$LOG_FILE" 2>&1 || echo "[$(date)] Mexico $STATE scraper had errors" >> "$LOG_FILE"
    
    sleep 2
done

# ============================================================
# Import all to database
# ============================================================
echo "[$(date)] --- Importing to Database ---" >> "$LOG_FILE"

python3 /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/scrapers/import_to_datadepot.py \
    --input-dir "$OUTPUT_DIR" \
    --db "$DB_PATH" \
    >> "$LOG_FILE" 2>&1

echo "[$(date)] ==========================================" >> "$LOG_FILE"
echo "[$(date)] Multi-Region Scraper Complete" >> "$LOG_FILE"
echo "[$(date)] ==========================================" >> "$LOG_FILE"

# Summary
find "$OUTPUT_DIR" -name "*.json" -mtime -1 -exec wc -l {} + | tail -1 >> "$LOG_FILE"
