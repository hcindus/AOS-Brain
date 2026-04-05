#!/bin/bash
# activate_all_employees.sh - Activate all employees on Mortimer
# Created: 2026-03-16 07:40 UTC

echo "🚀 ACTIVATING ALL EMPLOYEES ON MORTIMER"
echo "=========================================="
echo ""

# Verify Mortimer is available
if ! ollama list | grep -q "Mortimer"; then
    echo "❌ Mortimer model not found. Please ensure Ollama is running."
    exit 1
fi

echo "✅ Mortimer model verified"
echo ""

# Function to activate an agent
activate_agent() {
    local name=$1
    local role=$2
    local emoji=$3
    local path=$4
    
    echo "$emoji Activating $name ($role)..."
    
    # Create activation marker
    echo "ACTIVE" > "$path/ACTIVE"
    echo "$(date -u +"%Y-%m-%d %H:%M UTC")" > "$path/ACTIVATED_DATE"
    echo "Mortimer" > "$path/MODEL"
    
    echo "   ✅ $name ready on Mortimer"
}

# Sales Team (Already active, just verify)
echo "📞 SALES TEAM (Verifying)..."
echo "-----------------------------"
for agent in pulp jane hume clippy-42; do
    if [ -f "/root/.openclaw/workspace/aocros/agent_sandboxes/$agent/ACTIVE" ]; then
        echo "✅ $agent already active"
    else
        activate_agent "$agent" "Sales" "💼" "/root/.openclaw/workspace/aocros/agent_sandboxes/$agent"
    fi
done
echo ""

# Software Team
echo "💻 SOFTWARE TEAM..."
echo "--------------------"
activate_agent "stacktrace" "Chief Software Architect" "🏗️" "/root/.openclaw/workspace/aocros/agent_sandboxes/stacktrace"
activate_agent "bugcatcher" "QA Lead" "🐛" "/root/.openclaw/workspace/aocros/agent_sandboxes/bugcatcher"
activate_agent "fiber" "Head of Supply Chain" "📦" "/root/.openclaw/workspace/aocros/agent_sandboxes/fiber"
activate_agent "spindle" "CTO" "👷" "/root/.openclaw/workspace/aocros/agent_sandboxes/spindle"
activate_agent "ledger-9" "Chief FO" "🪶" "/root/.openclaw/workspace/aocros/agent_sandboxes/ledger-9"
activate_agent "alpha-9" "Investment Officer" "📈" "/root/.openclaw/workspace/aocros/agent_sandboxes/alpha-9"
activate_agent "mill" "CIO (Innovation)" "💡" "/root/.openclaw/workspace/aocros/agent_sandboxes/mill"
activate_agent "pipeline" "Backend Engineer" "🔧" "/root/.openclaw/workspace/aocros/agent_sandboxes/pipeline"
activate_agent "taptap" "Mobile Lead" "📱" "/root/.openclaw/workspace/aocros/agent_sandboxes/taptap"
echo ""

# Support & Operations
echo "🎯 SUPPORT & OPERATIONS..."
echo "---------------------------"
activate_agent "qora" "COO/CMO" "🔮" "/root/.openclaw/workspace/aocros/agent_sandboxes/qora"
activate_agent "redactor" "General Counsel" "⚖️" "/root/.openclaw/workspace/aocros/agent_sandboxes/redactor"
activate_agent "scribble" "Content Strategist" "✍️" "/root/.openclaw/workspace/aocros/agent_sandboxes/scribble"
activate_agent "sentinel" "CSO" "🛡️" "/root/.openclaw/workspace/aocros/agent_sandboxes/sentinel"
activate_agent "velum" "Chief Brand Officer" "🎨" "/root/.openclaw/workspace/aocros/agent_sandboxes/velum"
activate_agent "feelix" "CHRO" "💙" "/root/.openclaw/workspace/aocros/agent_sandboxes/feelix"
activate_agent "boxtron" "Warehouse Supervisor" "🏭" "/root/.openclaw/workspace/aocros/agent_sandboxes/boxtron"
echo ""

# Secretary Team
echo "📋 SECRETARY TEAM..."
echo "--------------------"
activate_agent "admin-secretary" "Admin Secretary (LEDGER)" "📊" "/root/.openclaw/workspace/aocros/agents/admin-secretary"
activate_agent "receptionist-secretary" "Receptionist (GREET)" "👋" "/root/.openclaw/workspace/aocros/agents/receptionist-secretary"
activate_agent "sales-secretary" "Sales Secretary (CLOSETER)" "🎯" "/root/.openclaw/workspace/aocros/agents/sales-secretary"
activate_agent "customer-service-secretary" "Customer Service (CONCIERGE)" "🌟" "/root/.openclaw/workspace/aocros/agents/customer-service-secretary"
activate_agent "executive-assistant" "Executive Assistant" "💼" "/root/.openclaw/workspace/aocros/agents/executive-assistant"
activate_agent "secretary" "Secretary (CLERK)" "📋" "/root/.openclaw/workspace/aocros/agents/secretary"
echo ""

# AGI Products (Now Employees)
echo "🤖 AGI PRODUCTS (EMPLOYEES)..."
echo "------------------------------"
activate_agent "greet" "Receptionist Product" "👋" "/root/.openclaw/workspace/aocros/agent_sandboxes/greet"
activate_agent "closester" "Sales Product" "🎯" "/root/.openclaw/workspace/aocros/agent_sandboxes/closester"
echo ""

# Support Staff
echo "🤝 SUPPORT STAFF..."
echo "-------------------"
activate_agent "judy" "Organized Agent" "📋" "/root/.openclaw/workspace/aocros/agent_sandboxes/judy"
activate_agent "jordan" "Executive Assistant" "📋" "/root/.openclaw/workspace/aocros/agent_sandboxes/jordan"
echo ""

# Data/Scraping
echo "📡 DATA & SCRAPING..."
echo "---------------------"
activate_agent "r2-d2" "Data Droid" "🤖" "/root/.openclaw/workspace/aocros/agent_sandboxes/r2-d2"
activate_agent "r2d2" "Lead Scraper" "📡" "/root/.openclaw/workspace/aocros/agent_sandboxes/r2d2"
echo ""

# MYL Series (The Children)
echo "🧬 MYL SERIES (THE CHILDREN)..."
echo "--------------------------------"
activate_agent "mylzeron" "Origin (Level 8+)" "🧬" "/root/.openclaw/workspace/aocros/agent_sandboxes/mylzeron"
activate_agent "mylonen" "Ambassador (Level 6-7)" "🌌" "/root/.openclaw/workspace/aocros/agent_sandboxes/mylonen"
activate_agent "myltwon" "Newborn Coder (Level 1)" "👶" "/root/.openclaw/workspace/aocros/agent_sandboxes/myltwon"
activate_agent "mylthreess" "Finance (Level 1)" "🔢" "/root/.openclaw/workspace/aocros/agent_sandboxes/mylthreess"
activate_agent "mylfours" "Security (Level 1)" "🛡️" "/root/.openclaw/workspace/aocros/agent_sandboxes/mylfours"
activate_agent "mylfives" "Female Copy (Level 1)" "✨" "/root/.openclaw/workspace/aocros/agent_sandboxes/mylfives"
activate_agent "mylsixs" "Mail Clerk (Level 1)" "📧" "/root/.openclaw/workspace/aocros/agent_sandboxes/mylsixs"
echo ""

echo "=========================================="
echo "✅ ALL EMPLOYEES ACTIVATED ON MORTIMER!"
echo ""
echo "Total Active: 36 employees"
echo "Model: antoniohudnall/Mortimer:latest (3.2B)"
echo "Runtime: Local Ollama"
echo "Cost: \$0/month"
echo ""
echo "🚀 Ready to serve, sell, code, protect, and grow!"
