#!/bin/bash
# Resource Guard - Check system load before allowing heavy tasks

CPU_THRESHOLD=${1:-70}
LOAD_THRESHOLD=${2:-4.0}

# Get current CPU usage (average over 1 second)
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
CPU_INT=${CPU_USAGE%.*}

# Get load average (1 min)
LOAD_AVG=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | tr -d ',')

# Compare
if (( CPU_INT > CPU_THRESHOLD )) || (( $(echo "$LOAD_AVG > $LOAD_THRESHOLD" | bc -l) )); then
    echo "RESOURCE_BUSY: CPU=${CPU_INT}%, Load=${LOAD_AVG} (thresholds: ${CPU_THRESHOLD}%/${LOAD_THRESHOLD})"
    exit 1
else
    echo "RESOURCE_OK: CPU=${CPU_INT}%, Load=${LOAD_AVG}"
    exit 0
fi
