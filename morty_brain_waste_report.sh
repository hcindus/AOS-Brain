#!/bin/bash
# Morty's Brain Waste Report Generator v2.0
# Fixed to query Miles' brain via HTTP API instead of local Unix socket
# Runs on Termux/Android, reports on Miles' brain at psdepot.com

set -e

# Configuration
MILES_HOST="${MILES_HOST:-psdepot.com}"
MILES_PORT="${MILES_PORT:-8080}"
MILES_URL="http://${MILES_HOST}:${MILES_PORT}"
REPORT_DIR="${HOME}/mortimer/brain-waste"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S UTC')
DATESTAMP=$(date '+%Y%m%d-%H%M%S')

# Ensure report directory exists
mkdir -p "$REPORT_DIR"

# Report file
REPORT_FILE="${REPORT_DIR}/brain-waste-${DATESTAMP}.txt"

# Temporary files for JSON data
BRAIN_STATUS=$(mktemp)
KIDNEY_STATUS=$(mktemp)
TRAP "rm -f $BRAIN_STATUS $KIDNEY_STATUS" EXIT

# Colors for terminal output (if supported)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== Morty's Waste Report Generator ==="
echo "Querying Miles' brain at ${MILES_HOST}:${MILES_PORT}..."
echo ""

# Query brain status via HTTP API
echo -n "Fetching brain status... "
if curl -s --max-time 10 "${MILES_URL}/api/status" > "$BRAIN_STATUS" 2>/dev/null; then
    echo -e "${GREEN}OK${NC}"
    BRAIN_OK=true
else
    echo -e "${RED}FAILED${NC}"
    BRAIN_OK=false
fi

# Query kidneys specifically via brain API
echo -n "Fetching kidney status... "
if curl -s --max-time 10 "${MILES_URL}/api/brain" > "$KIDNEY_STATUS" 2>/dev/null; then
    echo -e "${GREEN}OK${NC}"
    KIDNEY_OK=true
else
    echo -e "${RED}FAILED${NC}"
    KIDNEY_OK=false
fi

echo ""

# Generate report
cat > "$REPORT_FILE" << 'HEADER'
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MILES' BRAIN WASTE REPORT                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

HEADER

echo "Generated: ${TIMESTAMP}" >> "$REPORT_FILE"
echo "Source: Miles_Brain_v4.5 (via HTTP API)" >> "$REPORT_FILE"
echo "Host: ${MILES_HOST}:${MILES_PORT}" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Parse and format brain status
if [ "$BRAIN_OK" = true ]; then
    echo "✅ BRAIN STATUS: CONNECTED" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    # Extract key metrics using jq if available, otherwise grep
    if command -v jq >/dev/null 2>&1; then
        TICK=$(jq -r '.brain.tick // "N/A"' "$BRAIN_STATUS")
        PHASE=$(jq -r '.brain.phase // "N/A"' "$BRAIN_STATUS")
        SIGNAL=$(jq -r '.brain.signal_quality_20avg // "N/A"' "$BRAIN_STATUS")
        COMPONENTS=$(jq -r '.brain.components_active // "N/A"' "$BRAIN_STATUS")
        VERSION=$(jq -r '.brain.version // "N/A"' "$BRAIN_STATUS")
        
        cat >> "$REPORT_FILE" << EOF
┌─ Brain Metrics ──────────────────────────────────────────────────────────────┐
│  Version:        ${VERSION}
│  Current Tick:   ${TICK}
│  Phase:          ${PHASE}
│  Signal Quality: ${SIGNAL}
│  Components:     ${COMPONENTS}/15 active
└──────────────────────────────────────────────────────────────────────────────┘

EOF
    else
        # Fallback without jq
        echo "Raw brain status:" >> "$REPORT_FILE"
        cat "$BRAIN_STATUS" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    fi
else
    echo "❌ BRAIN STATUS: CONNECTION FAILED" >> "$REPORT_FILE"
    echo "   Error: Could not reach ${MILES_URL}/api/status" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# Parse kidney status
if [ "$KIDNEY_OK" = true ]; then
    echo "✅ KIDNEY STATUS: CONNECTED" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    if command -v jq >/dev/null 2>&1; then
        # Try to extract kidney data from brain API response
        KIDNEY_STATE=$(jq -r '.kidneys.state // "N/A"' "$KIDNEY_STATUS" 2>/dev/null || echo "N/A")
        PROCESSED=$(jq -r '.kidneys.total_processed // "N/A"' "$KIDNEY_STATUS" 2>/dev/null || echo "N/A")
        EXCRETED=$(jq -r '.kidneys.excreted // "N/A"' "$KIDNEY_STATUS" 2>/dev/null || echo "N/A")
        BLADDER=$(jq -r '.kidneys.bladder_level // "N/A"' "$KIDNEY_STATUS" 2>/dev/null || echo "N/A")
        NOISE=$(jq -r '.kidneys.noise_estimate // "N/A"' "$KIDNEY_STATUS" 2>/dev/null || echo "N/A")
        PATTERNS=$(jq -r '.kidneys.unique_patterns_seen // "N/A"' "$KIDNEY_STATUS" 2>/dev/null || echo "N/A")
        
        cat >> "$REPORT_FILE" << EOF
┌─ Kidney Metrics ─────────────────────────────────────────────────────────────┐
│  State:           ${KIDNEY_STATE}
│  Total Processed: ${PROCESSED}
│  Excreted:        ${EXCRETED}
│  Bladder Level:   ${BLADDER}/500
│  Noise Estimate:  ${NOISE}
│  Unique Patterns: ${PATTERNS}
└──────────────────────────────────────────────────────────────────────────────┘

EOF
    else
        echo "Raw kidney data:" >> "$REPORT_FILE"
        cat "$KIDNEY_STATUS" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    fi
else
    echo "❌ KIDNEY STATUS: CONNECTION FAILED" >> "$REPORT_FILE"
    echo "   Error: Could not reach ${MILES_URL}/api/brain" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# Add summary
cat >> "$REPORT_FILE" << 'FOOTER'
═══════════════════════════════════════════════════════════════════════════════

This is an automated waste report from Miles' brain.
Generated by Morty's waste report system (v2.0 - HTTP API)

═══════════════════════════════════════════════════════════════════════════════

FOOTER

# Display report
echo "=== Report Generated ==="
echo "File: $REPORT_FILE"
echo ""
cat "$REPORT_FILE"

# Cleanup
rm -f "$BRAIN_STATUS" "$KIDNEY_STATUS"

echo ""
echo "Report saved to: $REPORT_FILE"
