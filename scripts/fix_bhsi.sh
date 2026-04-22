#!/bin/bash
# Fix BHSI v4 - clear cache, kill stuck processes, restart

echo "=== BHSI v4 Fix Script ==="

# Kill stuck systemctl processes
echo "Killing stuck systemctl processes..."
pkill -9 -f "systemctl.*bhsi" 2>/dev/null
pkill -9 -f "bhsi_v4" 2>/dev/null
sleep 2

# Clear Python bytecode cache
echo "Clearing Python cache..."
rm -rf /root/.openclaw/workspace/aocros/BHSI/__pycache__
rm -rf /root/.aos/aos/__pycache__
find /root -name "*.pyc" -path "*BHSI*" -delete 2>/dev/null
find /root -name "*.pyc" -path "*aos*" -delete 2>/dev/null

# Reset systemd state
echo "Resetting systemd..."
systemctl reset-failed aos-bhsi-v4 2>/dev/null
systemctl daemon-reload 2>/dev/null

# Check if we can start
echo "Testing BHSI v4 startup..."
cd /root/.openclaw/workspace/aocros/BHSI
timeout 5 python3 -c "from bhsi_v4_complete import BHSI_V4; b=BHSI_V4(); print('get_stats exists:', hasattr(b, 'get_stats'))" 2>&1

echo "=== Fix complete ==="
