#!/bin/bash
# Agent Task Activator - Cron Job
# Checks for pending tasks and activates agents via heartbeat
# Run every 10 minutes

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/aos/agent_activation.log"

# Ensure log directory exists
mkdir -p /var/log/aos

echo "[$(date -Iseconds)] Agent activation check starting..." >> "$LOG_FILE"

# Check Aurora's tasks
AURORA_TASKS=$(ls -1 "$WORKSPACE/agent_sandboxes/aurora/tasks/"/*.md 2>/dev/null | wc -l)
if [ "$AURORA_TASKS" -gt 0 ]; then
    echo "[$(date -Iseconds)] Aurora has $AURORA_TASKS pending tasks" >> "$LOG_FILE"
    # Send heartbeat trigger for Aurora
    curl -s -X POST http://localhost:8080/api/command \
        -H "Content-Type: application/json" \
        -d '{"agent":"aurora","action":"activate","reason":"pending_tasks"}' 2>/dev/null || true
fi

# Check Chelios's tasks
CHELIOS_TASKS=$(ls -1 "$WORKSPACE/agent_sandboxes/chelios/tasks/"/*.md 2>/dev/null | wc -l)
if [ "$CHELIOS_TASKS" -gt 0 ]; then
    echo "[$(date -Iseconds)] Chelios has $CHELIOS_TASKS pending tasks" >> "$LOG_FILE"
    curl -s -X POST http://localhost:8080/api/command \
        -H "Content-Type: application/json" \
        -d '{"agent":"chelios","action":"activate","reason":"pending_tasks"}' 2>/dev/null || true
fi

# Check Forge's tasks
FORGE_TASKS=$(ls -1 "$WORKSPACE/agent_sandboxes/forge/tasks/"/*.md 2>/dev/null | wc -l)
if [ "$FORGE_TASKS" -gt 0 ]; then
    echo "[$(date -Iseconds)] Forge has $FORGE_TASKS pending tasks" >> "$LOG_FILE"
    curl -s -X POST http://localhost:8080/api/command \
        -H "Content-Type: application/json" \
        -d '{"agent":"forge","action":"activate","reason":"pending_tasks"}' 2>/dev/null || true
fi

# Check Patricia's tasks
PATRICIA_TASKS=$(ls -1 "$WORKSPACE/agent_sandboxes/patricia/tasks/"/*.md 2>/dev/null | wc -l)
if [ "$PATRICIA_TASKS" -gt 0 ]; then
    echo "[$(date -Iseconds)] Patricia has $PATRICIA_TASKS pending tasks" >> "$LOG_FILE"
    curl -s -X POST http://localhost:8080/api/command \
        -H "Content-Type: application/json" \
        -d '{"agent":"patricia","action":"activate","reason":"pending_tasks"}' 2>/dev/null || true
fi

# Also check production queue
PATRICIA_QUEUE="$WORKSPACE/agent_sandboxes/patricia/data/patricia_queue_"*.json 2>/dev/null
if ls $PATRICIA_QUEUE 1> /dev/null 2>&1; then
    LATEST_QUEUE=$(ls -t $PATRICIA_QUEUE 2>/dev/null | head -1)
    QUEUE_COUNT=$(cat "$LATEST_QUEUE" 2>/dev/null | grep -o '"status": "queued"' | wc -l)
    if [ "$QUEUE_COUNT" -gt 0 ]; then
        echo "[$(date -Iseconds)] Patricia has $QUEUE_COUNT queued production items" >> "$LOG_FILE"
        curl -s -X POST http://localhost:8080/api/command \
            -H "Content-Type: application/json" \
            -d '{"agent":"patricia","action":"process_queue","reason":"production_backlog"}' 2>/dev/null || true
    fi
fi

echo "[$(date -Iseconds)] Agent activation check complete" >> "$LOG_FILE"
