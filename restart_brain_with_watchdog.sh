#!/bin/bash
# RESTART BRAIN WITH WATCHDOG

echo "========================================"
echo "  RESTARTING BRAIN WITH WATCHDOG"
echo "========================================"
echo ""

# Step 1: Stop old brain
echo "[1/4] Stopping old brain..."
OLD_BRAIN=$(ps aux | grep "brain.py" | grep -v grep | grep -v simple | awk '{print $2}')
if [ -n "$OLD_BRAIN" ]; then
    kill -TERM $OLD_BRAIN 2>/dev/null
    sleep 2
    kill -KILL $OLD_BRAIN 2>/dev/null
    echo "      Old brain stopped (PID $OLD_BRAIN)"
else
    echo "      No old brain found"
fi

# Step 2: Start watchdog
echo ""
echo "[2/4] Starting watchdog..."
nohup python3 /root/.openclaw/workspace/watchdog.py > /tmp/watchdog.log 2>&1 &
WATCHDOG_PID=$!
echo "      Watchdog started (PID $WATCHDOG_PID)"

# Step 3: Wait for brain to start
echo ""
echo "[3/4] Waiting for brain to start (watchdog will spawn)..."
sleep 5

# Step 4: Verify
echo ""
echo "[4/4] Verifying systems..."
echo ""
echo "Active Processes:"
echo "-----------------"

# Check watchdog
WATCHDOG_CHECK=$(ps aux | grep "watchdog.py" | grep -v grep | awk '{print $2}')
if [ -n "$WATCHDOG_CHECK" ]; then
    echo "  ✅ Watchdog: PID $WATCHDOG_CHECK"
else
    echo "  ❌ Watchdog: NOT RUNNING"
fi

# Check brain
BRAIN_CHECK=$(ps aux | grep "brain.py" | grep -v grep | grep -v simple | awk '{print $2}')
if [ -n "$BRAIN_CHECK" ]; then
    echo "  ✅ Brain: PID $BRAIN_CHECK"
else
    echo "  ❌ Brain: NOT RUNNING"
fi

# Check heart
HEART_CHECK=$(ps aux | grep "ternary_heart" | grep -v grep | awk '{print $2}')
if [ -n "$HEART_CHECK" ]; then
    echo "  ✅ Heart: PID $HEART_CHECK"
else
    echo "  ❌ Heart: NOT RUNNING"
fi

# Check stomach
STOMACH_CHECK=$(ps aux | grep "run_stomach\|ternary_stomach" | grep -v grep | awk '{print $2}')
if [ -n "$STOMACH_CHECK" ]; then
    echo "  ✅ Stomach: PID $STOMACH_CHECK"
else
    echo "  ❌ Stomach: NOT RUNNING"
fi

echo ""
echo "========================================"
echo "  BRAIN RESTART COMPLETE"
echo "========================================"
echo ""
echo "Watchdog will auto-restart any crashed components."
echo "Log: tail -f /tmp/watchdog.log"
