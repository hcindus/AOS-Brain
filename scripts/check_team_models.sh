#!/bin/bash
# ============================================================================
# TEAM MODEL STATUS CHECKER
# Quick check of which models are loaded and available
# ============================================================================

echo "======================================================================"
echo "  🧠 TEAM MODEL STATUS"
echo "======================================================================"
echo ""

# Check Ollama
echo "📡 Ollama Service Status:"
if pgrep -x "ollama" > /dev/null; then
    echo "   ✅ Ollama daemon running"
else
    echo "   ⚠️  Ollama daemon not detected"
fi
echo ""

# List loaded models
echo "📦 Currently Loaded Models:"
echo "----------------------------------------------------------------------"
if command -v ollama > /dev/null 2>&1; then
    ollama list 2>/dev/null | while read line; do
        if [[ $line == NAME* ]]; then
            continue
        fi
        if [[ -n $line ]]; then
            echo "   • $line"
        fi
    done
else
    echo "   ❌ Ollama CLI not available"
fi
echo ""

# Team model requirements
echo "🎯 Team Model Requirements:"
echo "----------------------------------------------------------------------"
declare -A TEAM_MODELS=(
    ["antoniohudnall/Mortimer:latest"]="PRIMARY - All agents"
    ["nomic-embed-text:latest"]="EMBEDDINGS - MemoryBridge"
    ["phi3:latest"]="FALLBACK - Lightweight"
    ["qwen2.5:3b"]="FALLBACK - Multilingual"
    ["tinyllama:latest"]="TESTING - Ultra-light"
)

for model in "${!TEAM_MODELS[@]}"; do
    purpose="${TEAM_MODELS[$model]}"
    if ollama list 2>/dev/null | grep -q "^${model}"; then
        size=$(ollama list 2>/dev/null | grep "^${model}" | awk '{print $3}')
        echo "   ✅ $model | $purpose ($size)"
    else
        echo "   ⬜ $model | $purpose [NOT LOADED]"
    fi
done
echo ""

echo "💡 To load missing models: bash /root/.openclaw/workspace/scripts/load_team_models.sh"
echo ""
echo "======================================================================"
