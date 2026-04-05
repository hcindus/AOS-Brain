#!/bin/bash
# Dusty MVP End-to-End Test Script

set -e

echo "========================================"
echo "=== Dusty MVP End-to-End Test ==="
echo "========================================"
echo "Timestamp: $(date -Iseconds)"
TEST_ID="dusty-end-to-end-test-$(date +%s)"
echo "Test ID: $TEST_ID"
echo ""

# Timing variables
BRIDGE_MS=""
CORE_MS=""
OPENCLAW_MS=""
E2E_MS=""
QUERY_MS=""
TOTAL_START=$(date +%s%N)

# Result variables
BRIDGE_OK=false
CORE_OK=false
OPENCLAW_OK=false
E2E_OK=false
QUERY_OK=false

# Step 1: Health Checks
echo "[PHASE 1/4] Service Health Checks"
echo ""

# Check and log bridge
START=$(date +%s%N)
echo -n "  Telegram Bridge Mock (localhost:3001)... "
if HEALTH=$(curl -s --max-time 5 http://localhost:3001/health 2>/dev/null) && echo "$HEALTH" | grep -q "healthy"; then
  END=$(date +%s%N)
  BRIDGE_MS=$(((END - START) / 1000000))
  echo "OK (${BRIDGE_MS}ms)"
  BRIDGE_OK=true
else
  echo "FAILED"
fi

# Check core-agent
START=$(date +%s%N)
echo -n "  Core-Agent (localhost:3000)... "
if HEALTH=$(curl -s --max-time 5 http://localhost:3000/health 2>/dev/null) && echo "$HEALTH" | grep -q "healthy"; then
  END=$(date +%s%N)
  CORE_MS=$(((END - START) / 1000000))
  echo "OK (${CORE_MS}ms)"
  CORE_OK=true
else
  echo "FAILED"
fi

# Check openclaw
START=$(date +%s%N)
echo -n "  OpenClaw Mock (localhost:4000)... "
if HEALTH=$(curl -s --max-time 5 http://localhost:4000/status 2>/dev/null) && echo "$HEALTH" | grep -q "healthy"; then
  END=$(date +%s%N)
  OPENCLAW_MS=$(((END - START) / 1000000))
  echo "OK (${OPENCLAW_MS}ms)"
  OPENCLAW_OK=true
else
  echo "FAILED"
fi

echo ""
echo "[PHASE 2/4] End-to-End Flow Test"
echo -n "  Sending '/dust balance' via POST /webhook... "

START=$(date +%s%N)
E2E_RESULT=$(curl -s --max-time 15 -X POST http://localhost:3001/webhook \
    -H "Content-Type: application/json" \
    -d '{"update_id":1771595762,"message":{"message_id":1,"from":{"id":987654321,"is_bot":false,"first_name":"Test","username":"dusty_user"},"chat":{"id":987654321,"type":"private"},"date":1234567890,"text":"/dust balance"}}' \
    2>/dev/null || echo '{"error":"request_failed"}')
END=$(date +%s%N)
E2E_MS=$(((END - START) / 1000000))

if echo "$E2E_RESULT" | grep -q '"forwarded":true'; then
    echo "OK (${E2E_MS}ms)"
    E2E_OK=true
else
    echo "PARTIAL/FAILED (${E2E_MS}ms)"
    echo "  Response: $(echo "$E2E_RESULT" | head -c 150)"
fi

echo ""
echo "[PHASE 3/4] Dust-Specific Query Test"
echo -n "  Sending 'Get my dust balance'... "

START=$(date +%s%N)
QUERY_RESULT=$(curl -s --max-time 15 -X POST http://localhost:3001/webhook \
    -H "Content-Type: application/json" \
    -d '{"update_id":1771595763,"message":{"message_id":2,"from":{"id":987654322,"is_bot":false,"first_name":"Alice","username":"alice_test"},"chat":{"id":987654322,"type":"private"},"date":1234567891,"text":"Get my dust balance"}}' \
    2>/dev/null || echo '{"error":"request_failed"}')
END=$(date +%s%N)
QUERY_MS=$(((END - START) / 1000000))

if echo "$QUERY_RESULT" | grep -q '"forwarded":true'; then
    echo "OK (${QUERY_MS}ms)"
    QUERY_OK=true
else
    echo "PARTIAL/FAILED (${QUERY_MS}ms)"
    echo "  Response: $(echo "$QUERY_RESULT" | head -c 150)"
fi

echo ""
echo "[PHASE 4/4] Verification"
echo "  Checking Core-Agent forwarded task to OpenClaw..."
SLEEP_COUNT=0
OPENCLAW_UPDATED=false
while [ $SLEEP_COUNT -lt 3 ]; do
    sleep 1
    OPENCLAW_STATUS=$(curl -s --max-time 5 http://localhost:4000/status 2>/dev/null)
    CURRENT=$(echo "$OPENCLAW_STATUS" | grep -o '"total_interactions":[0-9]*' | cut -d: -f2 || echo "0")
    if [ -n "$CURRENT" ] && [ "$CURRENT" -gt 0 ] 2>/dev/null; then
        OPENCLAW_UPDATED=true
        break
    fi
    SLEEP_COUNT=$((SLEEP_COUNT + 1))
done

if [ "$OPENCLAW_UPDATED" = true ]; then
    echo "  OpenClaw received: $CURRENT interactions ✅"
else
    echo "  OpenClaw still at $CURRENT interactions ⚠️"
fi

echo ""
echo "========================================"
echo "=== TEST SUMMARY ==="
echo "========================================"

TOTAL_END=$(date +%s%N)
TOTAL_MS=$(((TOTAL_END - TOTAL_START) / 1000000))

PASSED=0
FAILED=0

[ "$BRIDGE_OK" = "true" ] && PASSED=$((PASSED + 1)) || FAILED=$((FAILED + 1))
[ "$CORE_OK" = "true" ] && PASSED=$((PASSED + 1)) || FAILED=$((FAILED + 1))
[ "$OPENCLAW_OK" = "true" ] && PASSED=$((PASSED + 1)) || FAILED=$((FAILED + 1))
[ "$E2E_OK" = "true" ] && PASSED=$((PASSED + 1)) || FAILED=$((FAILED + 1))
[ "$QUERY_OK" = "true" ] && PASSED=$((PASSED + 1)) || FAILED=$((FAILED + 1))

printf "\nComponent Health:\n"
printf "  Telegram Bridge Mock: %s\n" "$([ "$BRIDGE_OK" = "true" ] && echo "✅ Healthy" || echo "❌ Failed")"
printf "  Core-Agent: %s\n" "$([ "$CORE_OK" = "true" ] && echo "✅ Healthy" || echo "❌ Failed")"
printf "  OpenClaw Mock: %s\n" "$([ "$OPENCLAW_OK" = "true" ] && echo "✅ Healthy" || echo "❌ Failed")"

echo ""
printf "End-to-End Flow:\n"
printf "  POST /webhook: %s\n" "$([ "$E2E_OK" = "true" ] && echo "✅ Success" || echo "⚠️ Partial/Failed")"
printf "  Dust Query: %s\n" "$([ "$QUERY_OK" = "true" ] && echo "✅ Success" || echo "⚠️ Partial/Failed")"
printf "  Core-Agent → OpenClaw: %s\n" "$([ "$OPENCLAW_UPDATED" = "true" ] && echo "✅ Verified" || echo "⚠️ Not Confirmed")"

echo ""
printf "Timing Breakdown:\n"
[ -n "$BRIDGE_MS" ] && printf "  Bridge Health: %dms\n" "$BRIDGE_MS"
[ -n "$CORE_MS" ] && printf "  Core-Agent Health: %dms\n" "$CORE_MS"
[ -n "$OPENCLAW_MS" ] && printf "  OpenClaw Health: %dms\n" "$OPENCLAW_MS"
[ -n "$E2E_MS" ] && printf "  E2E Webhook: %dms\n" "$E2E_MS"
[ -n "$QUERY_MS" ] && printf "  Dust Query: %dms\n" "$QUERY_MS"
printf "  Total Test Time: %dms\n" "$TOTAL_MS"

echo ""
printf "Results: %d passed / %d failed\n" "$PASSED" "$FAILED"
printf "Completed: %s\n" "$(date -Iseconds)"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo "✅ ALL TESTS PASSED"
    EXIT_CODE=0
else
    echo ""
    echo "⚠️ SOME TESTS FAILED"
    EXIT_CODE=1
fi

# Generate markdown report
REPORT_FILE="/root/.openclaw/workspace/agents/dusty/test/e2e_report_${TEST_ID}.md"
cat > "$REPORT_FILE" << EOF
# Dusty MVP End-to-End Test Report

**Test ID:** \`$TEST_ID\`  
**Timestamp:** $(date -Iseconds)  
**Status:** $([ $FAILED -eq 0 ] && echo "✅ PASSED" || echo "⚠️ FAILED")

## Component Health Check

| Component | Status | Response Time |
|-----------|--------|---------------|
| Telegram Bridge Mock | $([ "$BRIDGE_OK" = "true" ] && echo "✅ Healthy" || echo "❌ Failed") | ${BRIDGE_MS}ms |
| Core-Agent | $([ "$CORE_OK" = "true" ] && echo "✅ Healthy" || echo "❌ Failed") | ${CORE_MS}ms |
| OpenClaw Mock | $([ "$OPENCLAW_OK" = "true" ] && echo "✅ Healthy" || echo "❌ Failed") | ${OPENCLAW_MS}ms |

## End-to-End Flow Tests

| Test | Status | Response Time |
|------|--------|---------------|
| POST /webhook (\`/dust balance\`) | $([ "$E2E_OK" = "true" ] && echo "✅ Success" || echo "❌ Failed") | ${E2E_MS}ms |
| Dust Query (\`Get my dust balance\`) | $([ "$QUERY_OK" = "true" ] && echo "✅ Success" || echo "❌ Failed") | ${QUERY_MS}ms |
| Core-Agent → OpenClaw Forward | $([ "$OPENCLAW_UPDATED" = "true" ] && echo "✅ Verified" || echo "⚠️ Not Confirmed") | - |

## Timing Summary

| Step | Time |
|------|------|
| Bridge Health Check | ${BRIDGE_MS}ms |
| Core-Agent Health Check | ${CORE_MS}ms |
| OpenClaw Health Check | ${OPENCLAW_MS}ms |
| E2E Webhook Test | ${E2E_MS}ms |
| Dust Query Test | ${QUERY_MS}ms |
| **Total Execution Time** | **${TOTAL_MS}ms** |

## Results

- **Passed:** $PASSED/5
- **Failed:** $FAILED/5

$([ $FAILED -eq 0 ] && echo "All tests passed successfully." || echo "Some tests failed. Check logs for details.")
EOF

echo ""
echo "Report saved to: $REPORT_FILE"

exit $EXIT_CODE
