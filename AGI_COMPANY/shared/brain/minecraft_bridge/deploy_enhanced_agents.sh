#!/bin/bash
#
# Deploy 14 Enhanced Ternary OODA Agents v2.0
#

cd /root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge

echo "=========================================="
echo "  DEPLOYING ENHANCED AGENTS v2.0"
echo "=========================================="
echo ""
echo "Features:"
echo "  - Ternary Heart Sync (REST/BALANCE/ACTIVE)"
echo "  - Memory System (locations, resources, dangers)"
echo "  - Emotional State (confidence, fear, curiosity)"
echo "  - Combat Skills (martial arts integration)"
echo "  - Multi-Agent Coordination"
echo ""

# MYL Series (7 agents)
MYL_AGENTS=(
    "mylzeron:male:MYL-0"
    "mylonen:male:MYL-1"
    "myltwon:male:MYL-2"
    "mylthreen:female:MYL-3"
    "mylforon:male:MYL-4"
    "mylfivon:female:MYL-5"
    "mylsixon:female:MYL-6"
)

# Robot Lineages (7 agents)
ROBOT_AGENTS=(
    "cobra_001:snake:COBRA-v1"
    "cobra_002:snake:COBRA-v1"
    "prometheus_001:humanoid:PROMETHEUS-v1"
    "prometheus_002:humanoid:PROMETHEUS-v1"
    "myl_dual_001:hybrid:MYL+COBRA"
    "myl_dual_002:hybrid:MYL+PROMETHEUS"
    "technical_001:specialist:Technical"
)

echo "Deploying MYL Series..."
for agent_info in "${MYL_AGENTS[@]}"; do
    IFS=':' read -r name gender series <<< "$agent_info"
    node enhanced_agent.js $name localhost 25566 ws://localhost:8767 > /tmp/${name}.log 2>&1 &
    echo "  $name ($gender, $series) - PID $!"
    sleep 4
done

echo ""
echo "Deploying Robot Lineages..."
for agent_info in "${ROBOT_AGENTS[@]}"; do
    IFS=':' read -r name type lineage <<< "$agent_info"
    node enhanced_agent.js $name localhost 25566 ws://localhost:8767 > /tmp/${name}.log 2>&1 &
    echo "  $name ($type, $lineage) - PID $!"
    sleep 4
done

echo ""
echo "=========================================="
echo "  DEPLOYMENT COMPLETE"
echo "=========================================="
sleep 10

echo ""
echo "Active enhanced agents:"
ps aux | grep "enhanced_agent" | grep -v grep | wc -l

echo ""
echo "System status:"
echo "  CPU: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1)%"
echo "  Load: $(cat /proc/loadavg | awk '{print $1}')"

echo ""
echo "Mission: SURVIVE, BUILD, GATHER, MULTIPLY, REACH FOR THE STARS"
echo ""
echo "Agents now have:"
echo "  - Emotional awareness (fear, confidence, curiosity)"
echo "  - Memory of camps, resources, dangers"
echo "  - Combat skills from martial arts training"
echo "  - Coordination via Brain WebSocket"
echo "  - Ternary state synchronization with Heart"
