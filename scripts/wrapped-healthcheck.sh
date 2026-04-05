#!/bin/bash
# Wrapped Health Check with resource guards

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JOB_QUEUE="$SCRIPT_DIR/job-queue.sh"
RESOURCE_GUARD="$SCRIPT_DIR/resource-guard.sh"

# Health checks are light - run if load < 8
if ! "$RESOURCE_GUARD" 85 8.0; then
    echo "System overloaded, skipping non-critical health check"
    exit 0
fi

# Check if heavy job is running
if [[ -f /tmp/aos-job-queue/running ]]; then
    running_job=$(tail -1 /tmp/aos-job-queue/running 2>/dev/null)
    if [[ "$running_job" == *"scraper"* ]] || [[ "$running_job" == *"build"* ]]; then
        echo "Heavy job running, deferring health check"
        exit 0
    fi
fi

# Run health check
"$SCRIPT_DIR/../healthcheck.sh"
