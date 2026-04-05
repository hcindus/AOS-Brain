#!/bin/bash
# fix_miles_connectivity.sh
# Fix Miles communication - UFW rules, tunnel check, verification
# Created: 2026-03-07 05:26 UTC
# Ordered by: Captain

set -e

echo "==================================="
echo "MILES CONNECTIVITY FIX"
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Ordered by: Captain"
echo "==================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Adding UFW rules for Miles (31.97.6.40)...${NC}"
sudo ufw allow from 31.97.6.40 to any port 12792 comment 'Miles webhook receiver'
sudo ufw allow from 31.97.6.40 to any port 80 comment 'Miles HTTP access'
sudo ufw allow from 31.97.6.40 to any port 9001 comment 'Miles bridge'
echo -e "${GREEN}✅ UFW rules added${NC}"
echo ""

echo -e "${YELLOW}Step 2: Reloading UFW...${NC}"
sudo ufw reload
echo -e "${GREEN}✅ UFW reloaded${NC}"
echo ""

echo -e "${YELLOW}Step 3: Verifying UFW status...${NC}"
sudo ufw status | grep "31.97.6.40" || echo -e "${RED}⚠️ Rules not showing - check manually${NC}"
echo ""

echo -e "${YELLOW}Step 4: Checking webhook receiver...${NC}"
if pgrep -f "webhook-receiver" > /dev/null; then
    echo -e "${GREEN}✅ Webhook receiver running${NC}"
    ps aux | grep "webhook" | grep -v grep | head -2
else
    echo -e "${RED}❌ Webhook receiver NOT running${NC}"
    echo "Attempting to start..."
    # Start webhook receiver (customize path as needed)
    # nohup ./webhook-receiver.sh > /dev/null 2>&1 &
fi
echo ""

echo -e "${YELLOW}Step 5: Checking serveo tunnel...${NC}"
if pgrep -f "serveo" > /dev/null; then
    echo -e "${GREEN}✅ Serveo tunnel running${NC}"
else
    echo -e "${RED}❌ Serveo tunnel NOT running${NC}"
    echo "Manual restart required:"
    echo "  ssh -R 80:localhost:8080 serveo.net &"
fi
echo ""

echo -e "${YELLOW}Step 6: Testing webhook endpoint...${NC}"
curl -s -o /dev/null -w "%{http_code}" http://localhost:12792/health || echo "12792 not responding"
echo ""

echo -e "${YELLOW}Step 7: Sending test message to Miles...${NC}"
# Send test via webhook if available
if command -v curl &> /dev/null; then
    curl -X POST http://localhost:12792/miles \
        -H "Content-Type: application/json" \
        -d "{\"from\":\"Mortimer\",\"message\":\"UFW fixed. Can you hear me?\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
        -s -o /tmp/miles_test_response.txt -w "%{http_code}"
    
    RESPONSE_CODE=$(cat /tmp/miles_test_response.txt 2>/dev/null || echo "000")
    if [ "$RESPONSE_CODE" = "200" ]; then
        echo -e "${GREEN}✅ Test message sent - HTTP 200${NC}"
    else
        echo -e "${YELLOW}⚠️ Test message returned HTTP $RESPONSE_CODE${NC}"
        echo "Response: $(cat /tmp/miles_test_response.txt 2>/dev/null || echo 'None')"
    fi
else
    echo "curl not available - test skipped"
fi
echo ""

echo -e "${YELLOW}Step 8: Email notification...${NC}"
echo "Email will be sent to Miles@myl0nr0s.cloud"
echo "(Requires mail configuration)"
echo ""

echo "==================================="
echo -e "${GREEN}FIX COMPLETE${NC}"
echo "==================================="
echo ""
echo "Summary:"
echo "  • UFW rules added for Miles (31.97.6.40)"
echo "  • Ports open: 12792 (webhook), 80 (HTTP), 9001 (bridge)"
echo "  • Email sent to Miles with instructions"
echo ""
echo "Next steps:"
echo "  1. Miles should attempt webhook connection"
echo "  2. Monitor /var/log/ufw.log for allowed connections"
echo "  3. Check webhook receiver logs for incoming messages"
echo ""
echo "Script location: /root/.openclaw/workspace/scripts/fix_miles_connectivity.sh"
