#!/bin/bash
# ACTIVATE TECHNICAL TEAM - Stacktrace, Taptap, and Technical_001

echo "========================================"
echo "  ACTIVATING TECHNICAL TEAM"
echo "========================================"
echo ""

cd /root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge

# Technical_001 is already running - verify
TECH_PID=$(ps aux | grep "technical_001" | grep -v grep | grep node | awk '{print $2}')
if [ -n "$TECH_PID" ]; then
    echo "✅ technical_001: RUNNING (PID $TECH_PID)"
else
    echo "🔄 technical_001: STARTING..."
    nohup node lightweight_agent.js technical_001 localhost 25566 > /tmp/technical_001.log 2>&1 &
    sleep 2
    NEW_PID=$(ps aux | grep "technical_001" | grep -v grep | grep node | awk '{print $2}')
    if [ -n "$NEW_PID" ]; then
        echo "   ✅ Started (PID $NEW_PID)"
    else
        echo "   ❌ Failed to start"
    fi
fi

# Taptap - Lead Mobile Developer
echo ""
echo "🔄 taptap (Lead Mobile Developer): STARTING..."
nohup node lightweight_agent.js taptap localhost 25566 > /tmp/taptap.log 2>&1 &
sleep 2
TAP_PID=$(ps aux | grep "taptap" | grep -v grep | grep node | awk '{print $2}')
if [ -n "$TAP_PID" ]; then
    echo "   ✅ Started (PID $TAP_PID)"
else
    echo "   ❌ Failed to start"
fi

# Stacktrace - Chief Software Architect
echo ""
echo "🔄 stacktrace (Chief Software Architect): STARTING..."
nohup node lightweight_agent.js stacktrace localhost 25566 > /tmp/stacktrace.log 2>&1 &
sleep 2
STACK_PID=$(ps aux | grep "stacktrace" | grep -v grep | grep node | awk '{print $2}')
if [ -n "$STACK_PID" ]; then
    echo "   ✅ Started (PID $STACK_PID)"
else
    echo "   ❌ Failed to start"
fi

echo ""
echo "========================================"
echo "  TECHNICAL TEAM STATUS"
echo "========================================"
echo ""

# Verify all technical agents
ps aux | grep -E "(technical_001|taptap|stacktrace)" | grep -v grep | grep node | while read line; do
    PID=$(echo "$line" | awk '{print $2}')
    NAME=$(echo "$line" | awk '{print $11 $12}')
    CPU=$(echo "$line" | awk '{print $3}')
    echo "  ✅ $NAME | PID $PID | CPU $CPU%"
done

echo ""
echo "Technical Team: ACTIVATED"
echo "========================================"