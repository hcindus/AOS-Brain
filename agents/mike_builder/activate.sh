#!/bin/bash
# Mike Builder Activation Script
# Version: 1.0.0
# Updated: 2026-04-02 07:45 UTC

echo "🏗️ Activating Mike Builder..."
echo ""

# Set agent context
export AGENT_NAME="Mike Builder"
export AGENT_ROLE="Architect/Building Planner + Concierge"
export AGENT_EMOJI="🏗️"
export AGENT_SOCKET="/tmp/mike_builder.sock"

# Display identity
cat /root/.openclaw/workspace/agents/mike_builder/IDENTITY.md | grep -A 10 "# IDENTITY.md"

echo ""
echo "✅ Mike Builder environment loaded"
echo "📁 Memory path: agents/mike_builder/memory/"
echo "📋 Projects path: agents/mike_builder/projects/"
echo ""
echo "Ready to build. What are we working on?"
