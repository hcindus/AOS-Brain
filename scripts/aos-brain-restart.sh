#!/bin/bash
# AOS Brain v4.1 Restart Script with Diagnostics

set -e

echo "========================================"
echo "  🧠 AOS Brain v4.1 Restart"
echo "========================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

# Stop services
echo ""
echo "📴 Stopping services..."
systemctl stop aos-brain-v4.service 2>/dev/null || true
systemctl stop aos-mission-control.service 2>/dev/null || true
sleep 2

# Kill any remaining brain processes
echo "🧹 Cleaning up..."
pkill -f "complete_brain_v4.py" 2>/dev/null || true
sleep 1

# Remove old socket
rm -f /tmp/aos_brain.sock

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload

# Start brain service
echo ""
echo "🚀 Starting AOS Brain v4.1..."
systemctl start aos-brain-v4.service
sleep 3

# Check brain status
if systemctl is-active --quiet aos-brain-v4.service; then
    print_status "Brain service started" 0
else
    print_status "Brain service failed to start" 1
    systemctl status aos-brain-v4.service --no-pager
    exit 1
fi

# Start Mission Control
echo ""
echo "🎛️  Starting Mission Control..."
systemctl start aos-mission-control.service
sleep 2

# Check Mission Control
if systemctl is-active --quiet aos-mission-control.service; then
    print_status "Mission Control started" 0
else
    print_status "Mission Control failed to start" 1
    systemctl status aos-mission-control.service --no-pager
    exit 1
fi

# Wait for socket
echo ""
echo "⏳ Waiting for brain socket..."
for i in {1..10}; do
    if [ -S /tmp/aos_brain.sock ]; then
        print_status "Brain socket ready" 0
        break
    fi
    sleep 1
done

# Final status
echo ""
echo "========================================"
echo "  📊 System Status"
echo "========================================"

# Check processes
BRAIN_PID=$(pgrep -f "complete_brain_v4.py" | head -1)
MC_PID=$(pgrep -f "server_v2.py" | head -1)

if [ -n "$BRAIN_PID" ]; then
    echo -e "${GREEN}✅ Brain:${NC} PID $BRAIN_PID"
else
    echo -e "${RED}❌ Brain:${NC} Not running"
fi

if [ -n "$MC_PID" ]; then
    echo -e "${GREEN}✅ Mission Control:${NC} PID $MC_PID"
else
    echo -e "${RED}❌ Mission Control:${NC} Not running"
fi

# Socket check
if [ -S /tmp/aos_brain.sock ]; then
    echo -e "${GREEN}✅ Brain Socket:${NC} /tmp/aos_brain.sock"
else
    echo -e "${YELLOW}⚠️  Brain Socket:${NC} Not ready (may take a moment)"
fi

echo ""
echo "🌐 URLs:"
echo "   • Visualizer: http://localhost:8080"
echo "   • Status API: http://localhost:8080/api/status"
echo "   • Triage API: http://localhost:8080/api/triage"
echo ""
echo "📋 Commands:"
echo "   • Diagnose: python3 /root/.openclaw/workspace/aocros/mission_control/diagnostic.py triage"
echo "   • Full check: python3 /root/.openclaw/workspace/aocros/mission_control/diagnostic.py diagnostic"
echo ""
echo -e "${GREEN}✅ AOS Brain v4.1 is ready!${NC}"
