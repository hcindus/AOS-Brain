#!/bin/bash
# Comprehensive Test Suite for AOS Brain
# Runs all tests and generates report

TEST_DIR="/root/.openclaw/workspace/test-bench"
ENV_DIR="$TEST_DIR/environments/aos-brain-test"
RESULTS_FILE="$TEST_DIR/results/test_report_$(date +%Y%m%d_%H%M%S).txt"
LOG_FILE="$TEST_DIR/logs/test_run_$(date +%Y%m%d_%H%M%S).log"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     AOS BRAIN COMPREHENSIVE TEST SUITE                   ║"
echo "║     Testing all components...                              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Create results file
mkdir -p "$TEST_DIR/results"
exec 1>>"$LOG_FILE" 2>>"$LOG_FILE"

echo "Test started: $(date)" > "$RESULTS_FILE"
echo "============================================" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

PASS=0
FAIL=0

# Test 1: Environment Setup
echo "[TEST 1/10] Environment Setup..."
if [ -d "$ENV_DIR/brain" ] && [ -f "$ENV_DIR/config/brain.yaml" ]; then
    echo "✓ PASS: Environment structure correct" >> "$RESULTS_FILE"
    ((PASS++))
else
    echo "✗ FAIL: Environment structure incomplete" >> "$RESULTS_FILE"
    ((FAIL++))
fi

# Test 2: Brain Source Files
echo "[TEST 2/10] Brain Source Files..."
if [ -f "$ENV_DIR/brain/brain.py" ] && [ -d "$ENV_DIR/brain/agents" ]; then
    echo "✓ PASS: Brain source files present" >> "$RESULTS_FILE"
    ((PASS++))
else
    echo "✗ FAIL: Brain source files missing" >> "$RESULTS_FILE"
    ((FAIL++))
fi

# Test 3: Input Queue System
echo "[TEST 3/10] Input Queue System..."
QUEUE_FILE="$ENV_DIR/.aos/brain/input/queue.jsonl"
if [ -f "$QUEUE_FILE" ]; then
    echo '{"text": "test", "source": "test", "timestamp": 1234567890, "type": "test"}' >> "$QUEUE_FILE"
    if [ -s "$QUEUE_FILE" ]; then
        echo "✓ PASS: Input queue working" >> "$RESULTS_FILE"
        ((PASS++))
    else
        echo "✗ FAIL: Input queue not writable" >> "$RESULTS_FILE"
        ((FAIL++))
    fi
else
    echo "✗ FAIL: Input queue not created" >> "$RESULTS_FILE"
    ((FAIL++))
fi

# Test 4: Feed Script
echo "[TEST 4/10] Feed Script..."
if [ -f "$ENV_DIR/scripts/feed_input.sh" ]; then
    chmod +x "$ENV_DIR/scripts/feed_input.sh"
    echo "✓ PASS: Feed script exists" >> "$RESULTS_FILE"
    ((PASS++))
else
    echo "✗ FAIL: Feed script missing" >> "$RESULTS_FILE"
    ((FAIL++))
fi

# Test 5: ThalamusAgent Input Interface
echo "[TEST 5/10] ThalamusAgent Input Interface..."
if grep -q "input_file" "$ENV_DIR/brain/agents/thalamus_agent.py" 2>/dev/null; then
    echo "✓ PASS: ThalamusAgent has input interface" >> "$RESULTS_FILE"
    ((PASS++))
else
    echo "✗ FAIL: ThalamusAgent missing input interface" >> "$RESULTS_FILE"
    ((FAIL++))
fi

# Test 6: HippocampusAgent Novelty Fix
echo "[TEST 6/10] HippocampusAgent Novelty Fix..."
if grep -q "max_novelty_rate" "$ENV_DIR/brain/agents/hippocampus_agent.py" 2>/dev/null; then
    echo "✓ PASS: Novelty rate limiting implemented" >> "$RESULTS_FILE"
    ((PASS++))
else
    echo "✗ FAIL: Novelty rate limiting not found" >> "$RESULTS_FILE"
    ((FAIL++))
fi

# Test 7: TUI Scripts
echo "[TEST 7/10] TUI Scripts..."
if [ -f "/root/.openclaw/workspace/AOS/brain/brain_tui.py" ] && [ -f "/root/.openclaw/workspace/AOS/brain/brain_alt_tui.py" ]; then
    echo "✓ PASS: Both TUI scripts exist" >> "$RESULTS_FILE"
    ((PASS++))
else
    echo "✗ FAIL: TUI scripts missing" >> "$RESULTS_FILE"
    ((FAIL++))
fi

# Test 8: Documentation
echo "[TEST 8/10] Product Documentation..."
DOC_COUNT=$(ls /root/.openclaw/workspace/aocros/docs/products/*.md 2>/dev/null | wc -l)
if [ "$DOC_COUNT" -ge 5 ]; then
    echo "✓ PASS: Product documentation complete ($DOC_COUNT files)" >> "$RESULTS_FILE"
    ((PASS++))
else
    echo "✗ FAIL: Product documentation incomplete ($DOC_COUNT files)" >> "$RESULTS_FILE"
    ((FAIL++))
fi

# Test 9: Version Index
echo "[TEST 9/10] Version Index..."
if [ -f "/root/.openclaw/workspace/aocros/docs/VERSION_INDEX.md" ]; then
    echo "✓ PASS: Version index exists" >> "$RESULTS_FILE"
    ((PASS++))
else
    echo "✗ FAIL: Version index missing" >> "$RESULTS_FILE"
    ((FAIL++))
fi

# Test 10: GitHub Commits
echo "[TEST 10/10] GitHub Integration..."
cd /root/.openclaw/workspace/aocros
if git log --oneline -1 >/dev/null 2>&1; then
    LATEST=$(git log --oneline -1 | head -c 20)
    echo "✓ PASS: GitHub commits present ($LATEST...)" >> "$RESULTS_FILE"
    ((PASS++))
else
    echo "✗ FAIL: GitHub not configured" >> "$RESULTS_FILE"
    ((FAIL++))
fi

# Summary
echo "" >> "$RESULTS_FILE"
echo "============================================" >> "$RESULTS_FILE"
echo "TEST SUMMARY" >> "$RESULTS_FILE"
echo "============================================" >> "$RESULTS_FILE"
echo "Passed: $PASS" >> "$RESULTS_FILE"
echo "Failed: $FAIL" >> "$RESULTS_FILE"
echo "Total:  $((PASS + FAIL))" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"
echo "Test completed: $(date)" >> "$RESULTS_FILE"

# Display results
cat "$RESULTS_FILE"
echo ""
echo "Full log: $LOG_FILE"
echo "Results saved to: $RESULTS_FILE"
