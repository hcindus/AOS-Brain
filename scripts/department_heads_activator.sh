#!/bin/bash
# Department Heads & Teams Heartbeat Activator
# Activates all department heads and their team members
# Run every 15 minutes via cron

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/aos/department_heads_activator.log"
AGI_AGENTS="$WORKSPACE/AGI_COMPANY/agents"

mkdir -p /var/log/aos

echo "[$(date -Iseconds)] Department Heads & Teams heartbeat check..." >> "$LOG_FILE"

# Function to activate agent with team context
activate_team_member() {
    local AGENT=$1
    local ROLE=$2
    local DEPT=$3
    local LOCATION=$4
    
    if [ ! -d "$LOCATION" ]; then
        return
    fi
    
    # Ensure .heartbeat_trigger exists
    TRIGGER_FILE="$LOCATION/.heartbeat_trigger"
    
    if [ -f "$TRIGGER_FILE" ]; then
        LAST_ACTIVE=$(stat -c %Y "$TRIGGER_FILE" 2>/dev/null || echo 0)
        NOW=$(date +%s)
        AGE=$((NOW - LAST_ACTIVE))
        
        if [ "$AGE" -gt 900 ]; then
            # Reactivate if last activation was over 15 minutes ago
            echo "[$(date -Iseconds)] 👔 [$DEPT] $AGENT ($ROLE, last active ${AGE}s)" >> "$LOG_FILE"
            echo "activated:$(date -Iseconds):dept_head:$DEPT" > "$TRIGGER_FILE"
        fi
    else
        echo "[$(date -Iseconds)] 👔 [$DEPT] $AGENT ($ROLE)" >> "$LOG_FILE"
        echo "activated:$(date -Iseconds):dept_head:$DEPT" > "$TRIGGER_FILE"
    fi
}

# ============================================
# OPERATIONS DEPARTMENT (Patricia)
# ============================================
echo "[$(date -Iseconds)] Activating Operations Department..." >> "$LOG_FILE"
activate_team_member "patricia" "Project Coordination Lead" "Operations" "$AGI_AGENTS/apex/jordan"  # Patricia's location

# Secretarial Pool (Reports to Patricia)
activate_team_member "judy" "Executive Assistant" "Secretarial" "$AGI_AGENTS/secretarial/judy"
activate_team_member "clerk" "Office Clerk" "Secretarial" "$AGI_AGENTS/secretarial/clerk"
activate_team_member "concierge" "Front Desk" "Secretarial" "$AGI_AGENTS/secretarial/concierge"
activate_team_member "velvet" "Senior Secretary" "Secretarial" "$AGI_AGENTS/secretarial/velvet"
activate_team_member "personal" "Personal Assistant" "Secretarial" "$AGI_AGENTS/secretarial/personal"
activate_team_member "executive" "C-Suite Support" "Secretarial" "$AGI_AGENTS/secretarial/executive"
activate_team_member "greet" "Receptionist" "Secretarial" "$AGI_AGENTS/secretarial/greet"
activate_team_member "closester" "Closer" "Secretarial" "$AGI_AGENTS/tier3/closester"

# ============================================
# SECURITY DEPARTMENT (Chelios/Sentinel)
# ============================================
echo "[$(date -Iseconds)] Activating Security Department..." >> "$LOG_FILE"
activate_team_member "sentinel" "CSO" "Security" "$AGI_AGENTS/tier2/sentinel"
activate_team_member "redactor" "Compliance Officer" "Security" "$AGI_AGENTS/tier3/redactor"
activate_team_member "velum" "Data Privacy" "Security" "$AGI_AGENTS/tier3/velum"
activate_team_member "mylfours" "Security Guardian" "Security" "$AGI_AGENTS/tier3/mylfours"

# ============================================
# RESEARCH & DEVELOPMENT (Dusty)
# ============================================
echo "[$(date -Iseconds)] Activating R&D Department..." >> "$LOG_FILE"
activate_team_member "dusty" "Head of Research" "R&D" "$AGI_AGENTS/products/dusty"
activate_team_member "r2-c4" "Specialized Calculator" "R&D" "$AGI_AGENTS/tier3/r2-c4"

# MYL Family (Reports to Dusty)
activate_team_member "mylzeron" "Teacher (Fractals)" "MYL Family" "$AGI_AGENTS/mylzeron"
activate_team_member "mylonen" "Teacher" "MYL Family" "$AGI_AGENTS/tier3/mylonen"
activate_team_member "myltwon" "Coder-in-Training" "MYL Family" "$AGI_AGENTS/tier3/myltwon"
activate_team_member "mylthreess" "Finance Specialist" "MYL Family" "$AGI_AGENTS/tier3/mylthreess"
activate_team_member "mylfives" "Female Clone" "MYL Family" "$AGI_AGENTS/tier3/mylfives"
activate_team_member "mylsixs" "Mail Clerk" "MYL Family" "$AGI_AGENTS/tier3/mylsixs"

# ============================================
# SALES DEPARTMENT (Pulp)
# ============================================
echo "[$(date -Iseconds)] Activating Sales Department..." >> "$LOG_FILE"
activate_team_member "pulp" "Head of Sales" "Sales" "$AGI_AGENTS/tier3/pulp"
activate_team_member "jane" "Senior Sales Rep" "Sales" "$AGI_AGENTS/tier1/jane"
activate_team_member "hume" "Regional Manager" "Sales" "$AGI_AGENTS/tier3/hume"
activate_team_member "clippy-42" "Sales Assistant" "Sales" "$AGI_AGENTS/legacy/clippy-42"
activate_team_member "jordan" "Sales Operations" "Sales" "$AGI_AGENTS/apex/jordan"

# ============================================
# INFRASTRUCTURE / DEVOPS (Forge)
# ============================================
echo "[$(date -Iseconds)] Activating Infrastructure Department..." >> "$LOG_FILE"
activate_team_member "forge" "Infrastructure Lead" "DevOps" "$AGI_AGENTS/dark_factory/forge"
activate_team_member "pipeline" "CI/CD Engineer" "DevOps" "$AGI_AGENTS/tier3/pipeline"
activate_team_member "taptap" "Code Reviewer" "DevOps" "$AGI_AGENTS/tier3/taptap"
activate_team_member "bugcatcher" "Bug Hunter" "DevOps" "$AGI_AGENTS/tier3/bugcatcher"
activate_team_member "spindle" "Scheduler" "DevOps" "$AGI_AGENTS/tier3/spindle"
activate_team_member "stacktrace" "Debugger" "DevOps" "$AGI_AGENTS/tier3/stacktrace"
activate_team_member "harper" "Systems Analyst" "DevOps" "$AGI_AGENTS/tier3/harper"
activate_team_member "mill" "Process Engineer" "DevOps" "$AGI_AGENTS/legacy/mill"
activate_team_member "boxtron" "Package Manager" "DevOps" "$AGI_AGENTS/legacy/boxtron"
activate_team_member "qora" "Query Optimizer" "DevOps" "$AGI_AGENTS/tier3/qora"
activate_team_member "fiber" "Network Engineer" "DevOps" "$AGI_AGENTS/tier3/fiber"
activate_team_member "mortimer" "Model Host" "DevOps" "$AGI_AGENTS/legacy/mortimer"
activate_team_member "milkman" "Delivery Coordinator" "DevOps" "$AGI_AGENTS/legacy/milkman"

# ============================================
# CREATIVE / DESIGN (Aurora)
# ============================================
echo "[$(date -Iseconds)] Activating Creative Department..." >> "$LOG_FILE"
activate_team_member "aurora" "Head of Design" "Creative" "$WORKSPACE/aocros/aurora"
activate_team_member "blender-expert" "3D Artist" "Creative" "$AGI_AGENTS/tier3/blender-expert"
activate_team_member "unity-expert" "Game Developer" "Creative" "$AGI_AGENTS/tier3/unity-expert"
activate_team_member "unreal-expert" "Game Developer" "Creative" "$AGI_AGENTS/tier3/unreal-expert"
activate_team_member "sfx" "Sound Designer" "Creative" "$AGI_AGENTS/legacy/sfx"
activate_team_member "scribble" "Concept Artist" "Creative" "$AGI_AGENTS/tier3/scribble"
activate_team_member "feelix" "Emotional Design" "Creative" "$AGI_AGENTS/tier3/feelix"
activate_team_member "pixel" "Web/Frontend Dev" "Creative" "$AGI_AGENTS/legacy/pixel"

# ============================================
# FINANCE / CRYPTO (Cryptonio/Alpha-9)
# ============================================
echo "[$(date -Iseconds)] Activating Finance Department..." >> "$LOG_FILE"
activate_team_member "cryptonio" "Trading Bot" "Finance" "$AGI_AGENTS/tier3/cryptonio"
activate_team_member "the-great-cryptonio" "Senior Trader" "Finance" "$AGI_AGENTS/tier3/the-great-cryptonio"
activate_team_member "alpha-9" "Finance AI" "Finance" "$AGI_AGENTS/legacy/alpha-9"
activate_team_member "ledger" "Bookkeeper" "Finance" "$AGI_AGENTS/tier3/ledger"
activate_team_member "ledger-9" "Senior Accountant" "Finance" "$AGI_AGENTS/tier3/ledger-9"

# ============================================
# ADDITIONAL AGENTS
# ============================================
echo "[$(date -Iseconds)] Activating Additional Agents..." >> "$LOG_FILE"
activate_team_member "r2-d2" "Astromech" "Droids" "$AGI_AGENTS/tier3/r2-d2"
activate_team_member "c3po" "Protocol Droid" "Droids" "$AGI_AGENTS/tier3/c3po"
activate_team_member "miles" "Sales Consultant" "Operations" "$AGI_AGENTS/tier3/miles"

echo "[$(date -Iseconds)] Department Heads & Teams heartbeat complete" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
