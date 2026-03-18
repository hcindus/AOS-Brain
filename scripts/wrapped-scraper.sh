#!/bin/bash
# Wrapped CA SOS Scraper with resource guards

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JOB_QUEUE="$SCRIPT_DIR/job-queue.sh"
RESOURCE_GUARD="$SCRIPT_DIR/resource-guard.sh"

# Check resources first
if ! "$RESOURCE_GUARD" 70 4.0; then
    echo "Resources busy, queuing scraper..."
    "$JOB_QUEUE" queue "ca-sos-scraper" "node $SCRIPT_DIR/../ca_sos_scraper.js" normal
    "$JOB_QUEUE" run
    exit 0
fi

# Check if something else is running
if [[ -f /tmp/aos-job-queue/running ]]; then
    echo "Another job running, queuing scraper..."
    "$JOB_QUEUE" queue "ca-sos-scraper" "node $SCRIPT_DIR/../ca_sos_scraper.js" normal
    exit 0
fi

# Run directly if resources available
"$JOB_QUEUE" queue "ca-sos-scraper" "node $SCRIPT_DIR/../ca_sos_scraper.js" high
"$JOB_QUEUE" run
