#!/bin/bash
# Jordan Agent Heartbeat Activator
# Dedicated activation for Jordan - Sales Operations Manager
# Run every 5 minutes via cron

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/aos/jordan_activator.log"
JORDAN_SANDBOX="$WORKSPACE/agent_sandboxes/jordan"
JORDAN_AGI="$WORKSPACE/AGI_COMPANY/agents/apex/jordan"

mkdir -p /var/log/aos

echo "[$(date -Iseconds)] Jordan heartbeat check..." >> "$LOG_FILE"

# Function to activate Jordan
activate_jordan() {
    local LOCATION=$1
    local CONTEXT=$2
    
    if [ ! -d "$LOCATION" ]; then
        echo "[$(date -Iseconds)] ⚠️ Jordan $CONTEXT not found at $LOCATION" >> "$LOG_FILE"
        return
    fi
    
    # Check for tasks
    TASK_COUNT=0
    if [ -d "$LOCATION/tasks" ]; then
        TASK_COUNT=$(ls -1 "$LOCATION/tasks/"/*.md 2>/dev/null | wc -l)
    fi
    
    # Also check for CURRENT_TASKS.md
    if [ -f "$LOCATION/CURRENT_TASKS.md" ]; then
        TASK_COUNT=$((TASK_COUNT + 1))
    fi
    
    TRIGGER_FILE="$LOCATION/.heartbeat_trigger"
    
    if [ -f "$TRIGGER_FILE" ]; then
        LAST_ACTIVE=$(stat -c %Y "$TRIGGER_FILE" 2>/dev/null || echo 0)
        NOW=$(date +%s)
        AGE=$((NOW - LAST_ACTIVE))
        
        if [ "$AGE" -gt 300 ]; then
            # Reactivate if last activation was over 5 minutes ago
            echo "[$(date -Iseconds)] 🎯 Activating Jordan ($CONTEXT, tasks: $TASK_COUNT, last active ${AGE}s)" >> "$LOG_FILE"
            echo "activated:$(date -Iseconds):jordan:$CONTEXT" > "$TRIGGER_FILE"
            
            # Trigger Jordan's office controller if it exists
            if [ -f "$LOCATION/jordan_office_controller.py" ]; then
                echo "[$(date -Iseconds)] 🚀 Triggering Jordan's office controller" >> "$LOG_FILE"
            fi
        else
            echo "[$(date -Iseconds)] ⏱ Jordan recently active ($CONTEXT, ${AGE}s ago)" >> "$LOG_FILE"
        fi
    else
        echo "[$(date -Iseconds)] 🎯 Activating Jordan ($CONTEXT, tasks: $TASK_COUNT)" >> "$LOG_FILE"
        echo "activated:$(date -Iseconds):jordan:$CONTEXT" > "$TRIGGER_FILE"
    fi
}

# Activate Jordan in both locations
activate_jordan "$JORDAN_SANDBOX" "sandbox"
activate_jordan "$JORDAN_AGI" "agi_company"

# Check for any additional Jordan workspaces
for JORDAN_DIR in $(find "$WORKSPACE" -type d -name "jordan" 2>/dev/null | grep -v node_modules | head -10); do
    if [ "$JORDAN_DIR" != "$JORDAN_SANDBOX" ] && [ "$JORDAN_DIR" != "$JORDAN_AGI" ]; then
        activate_jordan "$JORDAN_DIR" "additional"
    fi
done

echo "[$(date -Iseconds)] Jordan heartbeat complete" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
