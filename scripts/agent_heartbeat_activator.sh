#!/bin/bash
# Agent Auto-Activator on Heartbeat - v2.0 (Systemd-aware)
# Place in crontab: */5 * * * * /root/.openclaw/workspace/scripts/agent_heartbeat_activator.sh

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/aos/agent_activator.log"
AGENT_SANDBOX="$WORKSPACE/agent_sandboxes"

mkdir -p /var/log/aos

echo "[$(date -Iseconds)] Heartbeat check (v2.0 systemd-aware)..." >> "$LOG_FILE"

# v2.0: Check if systemd services are managing these agents
# If systemd is active, don't spawn duplicate processes - just trigger files

# Map agents to their systemd service names
declare -A AGENT_SERVICES=(
    [aurora]="aurora-tasks"
    [chelios]="chelios-security"
    [forge]="forge-factory"
    [patricia]="patricia-factory"
)

# Function to check if systemd is managing this agent
is_systemd_managed() {
    local AGENT=$1
    local SERVICE="${AGENT_SERVICES[$AGENT]}"
    if [ -n "$SERVICE" ]; then
        systemctl is-active "$SERVICE" >/dev/null 2>&1 && return 0
    fi
    return 1
}

# Function to activate agent (file-based trigger only - NO PROCESS SPAWNING)
activate_agent() {
    local AGENT=$1
    local REASON=$2

    echo "[$(date -Iseconds)] Activating $AGENT ($REASON)" >> "$LOG_FILE"

    # Create activation trigger file (systemd service reads this)
    echo "activated:$(date -Iseconds)" > "$AGENT_SANDBOX/$AGENT/.heartbeat_trigger"

    # Log the activation
    echo "{\"agent\":\"$AGENT\",\"activated\":\"$(date -Iseconds)\",\"reason\":\"$REASON\"}" >> "$LOG_FILE"
}

# Check each agent for pending tasks
for AGENT in aurora chelios forge patricia; do
    # v2.0: Skip if systemd is managing this agent
    if is_systemd_managed "$AGENT"; then
        echo "[$(date -Iseconds)] $AGENT: Managed by systemd ✅" >> "$LOG_FILE"
        continue
    fi

    TASK_COUNT=$(ls -1 "$AGENT_SANDBOX/$AGENT/tasks/"/*.md 2>/dev/null | wc -l)

    if [ "$TASK_COUNT" -gt 0 ]; then
        # Check if agent was recently activated (within last hour)
        TRIGGER_FILE="$AGENT_SANDBOX/$AGENT/.heartbeat_trigger"
        if [ -f "$TRIGGER_FILE" ]; then
            LAST_ACTIVE=$(stat -c %Y "$TRIGGER_FILE" 2>/dev/null || echo 0)
            NOW=$(date +%s)
            AGE=$((NOW - LAST_ACTIVE))

            if [ "$AGE" -gt 3600 ]; then
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

# Special check for Patricia's production queue (file-based only)
PATRICIA_DATA="$AGENT_SANDBOX/patricia/data"
if [ -d "$PATRICIA_DATA" ]; then
    LATEST_QUEUE=$(ls -t "$PATRICIA_DATA"/patricia_queue_*.json 2>/dev/null | head -1)
    if [ -n "$LATEST_QUEUE" ]; then
        QUEUED_ITEMS=$(grep -c '"status": "queued"' "$LATEST_QUEUE" 2>/dev/null || echo 0)
        if [ "$QUEUED_ITEMS" -gt 0 ]; then
            echo "[$(date -Iseconds)] Patricia has $QUEUED_ITEMS queued production items" >> "$LOG_FILE"
            # v2.0: Only trigger file if systemd is not managing
            if ! is_systemd_managed "patricia"; then
                activate_agent "patricia" "production queue backlog ($QUEUED_ITEMS items)"
            fi
        fi
    fi
fi

echo "[$(date -Iseconds)] Heartbeat complete" >> "$LOG_FILE"
