#!/bin/bash
# Agent Auto-Activator on Heartbeat
# Place in crontab: */5 * * * * /root/.openclaw/workspace/scripts/agent_heartbeat_activator.sh

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/aos/agent_activator.log"
AGENT_SANDBOX="$WORKSPACE/agent_sandboxes"

mkdir -p /var/log/aos

echo "[$(date -Iseconds)] Heartbeat check..." >> "$LOG_FILE"

# Function to activate agent
activate_agent() {
    local AGENT=$1
    local REASON=$2
    
    echo "[$(date -Iseconds)] Activating $AGENT ($REASON)" >> "$LOG_FILE"
    
    # Create activation trigger file
    echo "activated:$(date -Iseconds)" > "$AGENT_SANDBOX/$AGENT/.heartbeat_trigger"
    
    # Log the activation
    echo "{\"agent\":\"$AGENT\",\"activated\":\"$(date -Iseconds)\",\"reason\":\"$REASON\"}" >> "$LOG_FILE"
}

# Check each agent for pending tasks
for AGENT in aurora chelios forge patricia; do
    TASK_COUNT=$(ls -1 "$AGENT_SANDBOX/$AGENT/tasks/"/*.md 2>/dev/null | wc -l)
    
    if [ "$TASK_COUNT" -gt 0 ]; then
        # Check if agent was recently activated (within last hour)
        TRIGGER_FILE="$AGENT_SANDBOX/$AGENT/.heartbeat_trigger"
        if [ -f "$TRIGGER_FILE" ]; then
            LAST_ACTIVE=$(stat -c %Y "$TRIGGER_FILE" 2>/dev/null || echo 0)
            NOW=$(date +%s)
            AGE=$((NOW - LAST_ACTIVE))
            
            if [ "$AGE" -gt 3600 ]; then
                # Reactivate if last activation was over an hour ago
                activate_agent "$AGENT" "$TASK_COUNT pending tasks (last activation $AGE seconds ago)"
            else
                echo "[$(date -Iseconds)] $AGENT already active ($AGE seconds since last trigger)" >> "$LOG_FILE"
            fi
        else
            # No trigger file, activate now
            activate_agent "$AGENT" "$TASK_COUNT pending tasks"
        fi
    fi
done

# Special check for Patricia's production queue
PATRICIA_DATA="$AGENT_SANDBOX/patricia/data"
if [ -d "$PATRICIA_DATA" ]; then
    LATEST_QUEUE=$(ls -t "$PATRICIA_DATA"/patricia_queue_*.json 2>/dev/null | head -1)
    if [ -n "$LATEST_QUEUE" ]; then
        QUEUED_ITEMS=$(grep -c '"status": "queued"' "$LATEST_QUEUE" 2>/dev/null || echo 0)
        if [ "$QUEUED_ITEMS" -gt 0 ]; then
            echo "[$(date -Iseconds)] Patricia has $QUEUED_ITEMS queued production items" >> "$LOG_FILE"
            activate_agent "patricia" "production queue backlog ($QUEUED_ITEMS items)"
        fi
    fi
fi

echo "[$(date -Iseconds)] Heartbeat complete" >> "$LOG_FILE"
