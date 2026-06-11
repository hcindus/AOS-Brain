#!/bin/bash
# Parallel Lead Enrichment - 10 Worker Processes
# Runs enrichment across multiple counties in parallel

LEADS_DIR="/root/.openclaw/workspace/aocros/performance_supply_depot/products/leads"
ENRICHED_DIR="$LEADS_DIR/enriched"
LOG_DIR="/var/log/aos/enrichment_parallel"

mkdir -p "$ENRICHED_DIR" "$LOG_DIR"

# Define county batches for 10 workers
WORKER_1="CA_Alameda_County_Leads.xlsx CA_Amador_County_Leads.xlsx CA_Butte_County_Leads.xlsx CA_Calaveras_County_Leads.xlsx CA_Colusa_County_Leads.xlsx"
WORKER_2="CA_Contra_Costa_County_Leads.xlsx CA_Del_Norte_County_Leads.xlsx CA_El_Dorado_County_Leads.xlsx CA_Fresno_County_Leads.xlsx CA_Glenn_County_Leads.xlsx"
WORKER_3="CA_Humboldt_County_Leads.xlsx CA_Imperial_County_Leads.xlsx CA_Inyo_County_Leads.xlsx CA_Kern_County_Leads.xlsx CA_Kings_County_Leads.xlsx"
WORKER_4="CA_Lake_County_Leads.xlsx CA_Lassen_County_Leads.xlsx CA_Los_Angeles_County_Leads.xlsx CA_Madera_County_Leads.xlsx CA_Marin_County_Leads.xlsx"
WORKER_5="CA_Mariposa_County_Leads.xlsx CA_Mendocino_County_Leads.xlsx CA_Merced_County_Leads.xlsx CA_Modoc_County_Leads.xlsx CA_Mono_County_Leads.xlsx"
WORKER_6="CA_Monterey_County_Leads.xlsx CA_Napa_County_Leads.xlsx CA_Nevada_County_Leads.xlsx CA_Orange_County_Leads.xlsx CA_Placer_County_Leads.xlsx"
WORKER_7="CA_Plumas_County_Leads.xlsx CA_Riverside_County_Leads.xlsx CA_Sacramento_County_Leads.xlsx CA_San_Benito_County_Leads.xlsx CA_San_Bernardino_County_Leads.xlsx"
WORKER_8="CA_San_Diego_County_Leads.xlsx CA_San_Francisco_County_Leads.xlsx CA_San_Joaquin_County_Leads.xlsx CA_San_Luis_Obispo_County_Leads.xlsx CA_San_Mateo_County_Leads.xlsx"
WORKER_9="CA_Santa_Barbara_County_Leads.xlsx CA_Santa_Clara_County_Leads.xlsx CA_Santa_Cruz_County_Leads.xlsx CA_Shasta_County_Leads.xlsx CA_Sierra_County_Leads.xlsx"
WORKER_10="CA_Siskiyou_County_Leads.xlsx CA_Solano_County_Leads.xlsx CA_Sonoma_County_Leads.xlsx CA_Stanislaus_County_Leads.xlsx CA_Sutter_County_Leads.xlsx CA_Tehama_County_Leads.xlsx CA_Trinity_County_Leads.xlsx CA_Tulare_County_Leads.xlsx CA_Tuolumne_County_Leads.xlsx CA_Ventura_County_Leads.xlsx CA_Yolo_County_Leads.xlsx CA_Yuba_County_Leads.xlsx"

# Function to process a batch
process_batch() {
    WORKER_ID=$1
    FILE_LIST=$2
    LOG_FILE="$LOG_DIR/worker_${WORKER_ID}.log"
    
    echo "[$(date -Iseconds)] Worker $WORKER_ID starting..." > "$LOG_FILE"
    
    for file in $FILE_LIST; do
        if [ -f "$LEADS_DIR/$file" ]; then
            echo "[$(date -Iseconds)] Worker $WORKER_ID processing: $file" >> "$LOG_FILE"
            cd "$LEADS_DIR"
            python3 enrich_leads.py --input "$file" --output "$ENRICHED_DIR/enriched_$file" 2>> "$LOG_FILE"
            echo "[$(date -Iseconds)] Worker $WORKER_ID completed: $file" >> "$LOG_FILE"
        fi
    done
    
    echo "[$(date -Iseconds)] Worker $WORKER_ID finished all tasks" >> "$LOG_FILE"
}

# Export function for parallel execution
export -f process_batch
export LEADS_DIR ENRICHED_DIR LOG_DIR

echo "Starting parallel enrichment with 10 workers..."
echo "$(date -Iseconds)"

# Start all 10 workers in parallel
process_batch 1 "$WORKER_1" &
process_batch 2 "$WORKER_2" &
process_batch 3 "$WORKER_3" &
process_batch 4 "$WORKER_4" &
process_batch 5 "$WORKER_5" &
process_batch 6 "$WORKER_6" &
process_batch 7 "$WORKER_7" &
process_batch 8 "$WORKER_8" &
process_batch 9 "$WORKER_9" &
process_batch 10 "$WORKER_10" &

# Wait for all workers to complete
wait

echo ""
echo "=========================================="
echo "Parallel enrichment complete!"
echo "$(date -Iseconds)"
echo "Results in: $ENRICHED_DIR/"
echo "Logs in: $LOG_DIR/"
echo "=========================================="
