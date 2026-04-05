#!/bin/bash
# Simple Watchdog - No psutil dependency

WATCHDOG_LOG="/tmp/simple_watchdog.log"

echo "[$(date)] Simple Watchdog Starting..." > $WATCHDOG_LOG

while true; do
    # Check brain
    BRAIN_COUNT=$(pgrep -f "brain.py" | grep -v simple | wc -l)
    if [ "$BRAIN_COUNT" -lt 1 ]; then
        echo "[$(date)] Brain not running, restarting..." >> $WATCHDOG_LOG
        cd /root/.openclaw/workspace/AOS && nohup python3 brain.py > /tmp/brain.log 2>&1 &
        sleep 5
    fi
    
    # Check heart
    HEART_COUNT=$(pgrep -f "ternary_heart" | wc -l)
    if [ "$HEART_COUNT" -lt 1 ]; then
        echo "[$(date)] Heart not running, restarting..." >> $WATCHDOG_LOG
        cd /root/.openclaw/workspace/aos_brain_py/heart && nohup python3 -c "from ternary_heart import TernaryHeart; import time; h=TernaryHeart(); print('Heart started'); [h.beat() or time.sleep(h.rhythm.bpm/60) for _ in iter(int,1)]" > /tmp/heart.log 2>&1 &
        sleep 2
    fi
    
    # Check stomach
    STOMACH_COUNT=$(pgrep -f "run_stomach" | wc -l)
    if [ "$STOMACH_COUNT" -lt 1 ]; then
        echo "[$(date)] Stomach not running, restarting..." >> $WATCHDOG_LOG
        cd /tmp && nohup python3 /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/aos_robot_body/run_stomach.py > /tmp/stomach.log 2>&1 &
        sleep 2
    fi
    
    sleep 10
done