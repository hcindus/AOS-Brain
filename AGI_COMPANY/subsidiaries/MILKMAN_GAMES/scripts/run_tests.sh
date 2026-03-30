#!/bin/bash
# MilkMan Games - Automated Testing Suite
# Runs tests for all games in production

set -e

echo "========================================"
echo "MILKMAN GAMES - AUTOMATED TEST SUITE"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TEST_RESULTS=()
PASSED=0
FAILED=0

# Function to run tests and track results
run_test() {
    local game_name=$1
    local test_command=$2
    
    echo -e "${YELLOW}Testing: $game_name${NC}"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✓ PASSED: $game_name${NC}"
        TEST_RESULTS+=("PASS: $game_name")
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED: $game_name${NC}"
        TEST_RESULTS+=("FAIL: $game_name")
        ((FAILED++))
    fi
    echo ""
}

# Change to games directory
cd /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/MILKMAN_GAMES || exit 1

echo "Starting test run at $(date)"
echo ""

# ============================================
# TEST 1: Roblox AGI Place
# ============================================
run_test "Roblox AGI Place - Bridge Connection" "
    systemctl is-active --quiet roblox-bridge
"

run_test "Roblox AGI Place - Place File Exists" "
    test -f roblox/AGI_Place.rbxl
"

# ============================================
# TEST 2: DaVerse Documentation
# ============================================
run_test "DaVerse - Documentation Complete" "
    test -f daverse/unreal/Documentation/Blueprints_PlayerSystem.md && \
    test -f daverse/unreal/Documentation/Blueprints_UMG_UI.md
"

run_test "DaVerse - Assets Exist" "
    test -d daverse/unreal/Source/DaVerse
"

# ============================================
# TEST 3: Chronospace Explorer
# ============================================
run_test "Chronospace - Project Structure" "
    test -d ChronospaceExplorer
"

# ============================================
# TEST 4: SGVD
# ============================================
run_test "SGVD - Project Structure" "
    test -d SGVD
"

# ============================================
# TEST 5: Build Scripts
# ============================================
run_test "Build Scripts - Present" "
    test -d scripts
"

run_test "Roblox Setup Guide - Present" "
    test -f roblox/SETUP_INSTRUCTIONS.md
"

# ============================================
# SUMMARY
# ============================================
echo "========================================"
echo "TEST SUMMARY"
echo "========================================"
echo ""

for result in "${TEST_RESULTS[@]}"; do
    if [[ $result == PASS:* ]]; then
        echo -e "${GREEN}$result${NC}"
    else
        echo -e "${RED}$result${NC}"
    fi
done

echo ""
echo "----------------------------------------"
echo "Total Tests: $((PASSED + FAILED))"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "----------------------------------------"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    exit 1
fi
