#!/bin/bash
# Sales Team Status Check Script
# Verifies all sales employees are running on Mortimer

echo "🔍 Sales Team Status Check"
echo "=========================="
echo ""

# Check Mortimer model
echo "🧠 Model Status:"
echo "---------------"
if ollama list | grep -q "antoniohudnall/Mortimer"; then
    echo "✅ Mortimer model: AVAILABLE"
    ollama list | grep "antoniohudnall/Mortimer" | awk '{print "   Model:", $1, "| Size:", $3, "| Modified:", $4, $5}'
else
    echo "❌ Mortimer model: NOT FOUND"
    echo "   Run: ollama pull antoniohudnall/Mortimer:latest"
fi
echo ""

# Check Ollama service
echo "🔌 Ollama Service:"
echo "-----------------"
if pgrep -x "ollama" > /dev/null; then
    echo "✅ Ollama daemon: RUNNING"
else
    echo "❌ Ollama daemon: NOT RUNNING"
    echo "   Start with: ollama serve"
fi
echo ""

# Check agent configurations
echo "📋 Agent Configurations:"
echo "-----------------------"
for agent in pulp jane hume clippy42; do
    config_file="/root/.openclaw/workspace/AOS/sales/${agent}_config.yaml"
    if [ -f "$config_file" ]; then
        echo "✅ $agent: CONFIGURED"
        grep "primary:" "$config_file" | sed 's/^/   /'
    else
        echo "❌ $agent: MISSING CONFIG"
    fi
done
echo ""

# Check portal configurations
echo "🌐 Portal Configurations:"
echo "------------------------"
for agent in pulp jane hume clippy-42; do
    portal_file="/root/.openclaw/workspace/aocros/agent_sandboxes/$agent/portal/portal_config.json"
    if [ -f "$portal_file" ]; then
        hub=$(grep "portal_hub" "$portal_file" | cut -d'"' -f4)
        echo "✅ $agent: Portal hub = $hub"
    else
        echo "❌ $agent: No portal config"
    fi
done
echo ""

# Check prospect files
echo "📁 Prospect Files:"
echo "-----------------"
for tier in corporate enterprise professional starter; do
    file="/root/.openclaw/workspace/sales/prospects_${tier}.csv"
    if [ -f "$file" ]; then
        count=$(wc -l < "$file")
        echo "✅ $tier: $count prospects"
    else
        echo "❌ $tier: File missing"
    fi
done
echo ""

# Summary
echo "=========================="
echo "📊 Summary"
echo "=========================="
echo "Model Runtime: LOCAL (Ollama)"
echo "Primary Model: antoniohudnall/Mortimer:latest"
echo "Cost Model: $0/month for 4 sales agents"
echo ""
echo "To activate: ./start_sales_team.sh"
