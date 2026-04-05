#!/bin/bash
# Sales Team Startup Script
# Activates all sales employees on local Mortimer model

echo "🚀 Starting Sales Team on Mortimer..."
echo "======================================"

# Verify Mortimer is available
if ! ollama list | grep -q "antoniohudnall/Mortimer"; then
    echo "❌ Error: Mortimer model not found. Please install first:"
    echo "   ollama pull antoniohudnall/Mortimer:latest"
    exit 1
fi

echo "✅ Mortimer model verified"

# Set environment for local runtime
export AOS_MODEL=ollama/antoniohudnall/Mortimer:latest
export AOS_RUNTIME=local
export OLLAMA_HOST=http://localhost:11434

echo ""
echo "📋 Sales Team Configuration:"
echo "----------------------------"

# Pulp - Head of Sales
echo "📞💼 Activating Pulp (Head of Sales - Corporate Tier)..."
export AOS_CONFIG=/root/.openclaw/workspace/AOS/sales/pulp_config.yaml
export AGENT_NAME=pulp
export AGENT_ROLE="Head of Sales"
export PROSPECT_FILE=/root/.openclaw/workspace/sales/prospects_corporate.csv
export MONTHLY_TARGET=50
export PRICE_TIER="$3,999/mo"
echo "   Config: $AOS_CONFIG"
echo "   Prospects: $PROSPECT_FILE"
echo "   Target: $MONTHLY_TARGET clients @ $PRICE_TIER"
echo "   ✅ Pulp ready"
echo ""

# Jane - Senior Sales Rep
echo "🤝📈 Activating Jane (Senior Sales Rep - Enterprise Tier)..."
export AOS_CONFIG=/root/.openclaw/workspace/AOS/sales/jane_config.yaml
export AGENT_NAME=jane
export AGENT_ROLE="Senior Sales Rep"
export PROSPECT_FILE=/root/.openclaw/workspace/sales/prospects_enterprise.csv
export MONTHLY_TARGET=100
export PRICE_TIER="$1,999/mo"
echo "   Config: $AOS_CONFIG"
echo "   Prospects: $PROSPECT_FILE"
echo "   Target: $MONTHLY_TARGET clients @ $PRICE_TIER"
echo "   ✅ Jane ready"
echo ""

# Hume - Regional Manager
echo "🗺️📍 Activating Hume (Regional Manager - Professional Tier)..."
export AOS_CONFIG=/root/.openclaw/workspace/AOS/sales/hume_config.yaml
export AGENT_NAME=hume
export AGENT_ROLE="Regional Manager"
export PROSPECT_FILE=/root/.openclaw/workspace/sales/prospects_professional.csv
export MONTHLY_TARGET=200
export PRICE_TIER="$999/mo"
echo "   Config: $AOS_CONFIG"
echo "   Prospects: $PROSPECT_FILE"
echo "   Target: $MONTHLY_TARGET clients @ $PRICE_TIER"
echo "   ✅ Hume ready"
echo ""

# Clippy-42 - Assistant
echo "📝📎 Activating Clippy-42 (Assistant - Starter Tier)..."
export AOS_CONFIG=/root/.openclaw/workspace/AOS/sales/clippy42_config.yaml
export AGENT_NAME=clippy-42
export AGENT_ROLE="Assistant to Regional Manager"
export PROSPECT_FILE=/root/.openclaw/workspace/sales/prospects_starter.csv
export MONTHLY_TARGET=401
export PRICE_TIER="$499/mo"
echo "   Config: $AOS_CONFIG"
echo "   Prospects: $PROSPECT_FILE"
echo "   Target: $MONTHLY_TARGET clients @ $PRICE_TIER"
echo "   ✅ Clippy-42 ready"
echo ""

echo "======================================"
echo "✅ Sales Team Activated on Mortimer!"
echo ""
echo "💰 Cost Savings Summary:"
echo "   Before: ~$2,000-2,500/month (5 agents cloud)"
echo "   After:  ~$400-500/month (1 cloud + 4 local)"
echo "   Monthly Savings: ~$1,500-2,000"
echo ""
echo "📊 Team Targets:"
echo "   Pulp:      50 clients  @ $3,999/mo = $199,950/mo"
echo "   Jane:     100 clients  @ $1,999/mo = $199,900/mo"
echo "   Hume:     200 clients  @ $999/mo  = $199,800/mo"
echo "   Clippy:   401 clients  @ $499/mo  = $200,099/mo"
echo "   -------------------------------------------"
echo "   TOTAL:    751 clients             = $799,749/mo"
echo ""
echo "🎯 Ready to crush those sales targets!"
echo ""
echo "To start individual agents:"
echo "   aos agent start pulp"
echo "   aos agent start jane"
echo "   aos agent start hume"
echo "   aos agent start clippy-42"
