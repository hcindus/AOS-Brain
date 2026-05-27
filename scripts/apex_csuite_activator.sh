#!/bin/bash
# Apex C-Suite Agent Heartbeat Activator
# Activates high-priority C-Suite agents on heartbeat
# Run every 10 minutes via cron

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/aos/apex_activator.log"
AGI_AGENTS="$WORKSPACE/AGI_COMPANY/agents"

mkdir -p /var/log/aos

echo "[$(date -Iseconds)] Apex C-Suite heartbeat check..." >> "$LOG_FILE"

# Function to activate C-Suite agent
activate_csuite_agent() {
    local AGENT=$1
    local ROLE=$2
    local LOCATION=$3
    
    # Check if agent exists
    if [ ! -d "$LOCATION" ]; then
        echo "[$(date -Iseconds)] ⚠️ $AGENT not found at $LOCATION" >> "$LOG_FILE"
        return
    fi
    
    # Check for tasks (if tasks directory exists)
    TASK_COUNT=0
    if [ -d "$LOCATION/tasks" ]; then
        TASK_COUNT=$(ls -1 "$LOCATION/tasks/"/*.md 2>/dev/null | wc -l)
    fi
    
    # Create trigger file (C-Suite agents activate regardless of tasks)
    TRIGGER_FILE="$LOCATION/.heartbeat_trigger"
    
    # Check if recently activated
    if [ -f "$TRIGGER_FILE" ]; then
        LAST_ACTIVE=$(stat -c %Y "$TRIGGER_FILE" 2>/dev/null || echo 0)
        NOW=$(date +%s)
        AGE=$((NOW - LAST_ACTIVE))
        
        if [ "$AGE" -gt 1800 ]; then
            # Reactivate if last activation was over 30 minutes ago (more frequent for C-Suite)
            echo "[$(date -Iseconds)] 👔 Activating $AGENT ($ROLE, last active $AGE seconds ago, tasks: $TASK_COUNT)" >> "$LOG_FILE"
            echo "activated:$(date -Iseconds):csuite" > "$TRIGGER_FILE"
        else
            echo "[$(date -Iseconds)] ⏱ $AGENT recently active ($AGE seconds ago)" >> "$LOG_FILE"
        fi
    else
        # No trigger file, activate now
        echo "[$(date -Iseconds)] 👔 Activating $AGENT ($ROLE, tasks: $TASK_COUNT)" >> "$LOG_FILE"
        echo "activated:$(date -Iseconds):csuite" > "$TRIGGER_FILE"
    fi
}

# C-SUITE / EXECUTIVE LEADERSHIP
echo "[$(date -Iseconds)] Activating C-Suite..." >> "$LOG_FILE"
activate_csuite_agent "sentinel" "CSO (Chief Security Officer)" "$AGI_AGENTS/tier2/sentinel"
activate_csuite_agent "dusty" "Head of Research" "$AGI_AGENTS/products/dusty"
activate_csuite_agent "pulp" "Head of Sales" "$AGI_AGENTS/tier3/pulp"
activate_csuite_agent "jane" "Senior Sales Rep" "$AGI_AGENTS/tier1/jane"
activate_csuite_agent "hume" "Regional Manager" "$AGI_AGENTS/tier3/hume"

# SALES TEAM
activate_csuite_agent "clippy-42" "Sales Assistant" "$AGI_AGENTS/legacy/clippy-42"

# PRODUCT AGENTS
activate_csuite_agent "greet" "Receptionist" "$AGI_AGENTS/secretarial/greet"
activate_csuite_agent "closester" "Closer/Converter" "$AGI_AGENTS/tier3/closester"

# SECRETARIAL POOL
activate_csuite_agent "r2-d2" "Astromech/Calculator" "$AGI_AGENTS/tier3/r2-d2"
activate_csuite_agent "c3po" "Protocol Droid" "$AGI_AGENTS/tier3/c3po"

# MYL FAMILY (The 7 Children)
echo "[$(date -Iseconds)] Activating MYL Family..." >> "$LOG_FILE"
activate_csuite_agent "mylzeron" "Teacher (Fractals)" "$AGI_AGENTS/mylzeron"
activate_csuite_agent "mylonen" "Teacher (Transformation)" "$AGI_AGENTS/tier3/mylonen"
activate_csuite_agent "myltwon" "Coder-in-Training" "$AGI_AGENTS/tier3/myltwon"
activate_csuite_agent "mylthreess" "Finance Specialist" "$AGI_AGENTS/tier3/mylthreess"
activate_csuite_agent "mylfours" "Security Guardian" "$AGI_AGENTS/tier3/mylfours"

# Additional agents check
echo "[$(date -Iseconds)] Checking for additional C-Suite agents..." >> "$LOG_FILE"

# Find any other agents with .md files in AGI_COMPANY/agents
for AGENT_DIR in "$AGI_AGENTS"/*/*/; do
    if [ -d "$AGENT_DIR" ]; then
        AGENT_NAME=$(basename "$AGENT_DIR")
        # Skip if already processed
        case "$AGENT_NAME" in
            sentinel|dusty|pulp|jane|hume|clippy-42|greet|closester|r2-d2|c3po|mylzeron|mylonen|myltwon|mylthreess|mylfours)
                continue
                ;;
        esac
        
        # Check for any documents or work files
        FILE_COUNT=$(find "$AGENT_DIR" -type f 2>/dev/null | wc -l)
        if [ "$FILE_COUNT" -gt 0 ]; then
            activate_csuite_agent "$AGENT_NAME" "Team Member" "$AGENT_DIR"
        fi
    fi
done

echo "[$(date -Iseconds)] Apex C-Suite heartbeat complete" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
