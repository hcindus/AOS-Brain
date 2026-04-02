#!/bin/bash
# ============================================================================
# TEAM MODEL LOADER
# Ensures all required Ollama models are available for the AGI team
# ============================================================================

echo "======================================================================"
echo "  🧠 TEAM MODEL LOADER - Ollama Model Management"
echo "======================================================================"
echo ""

# Check if Ollama is running
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install Ollama first."
    exit 1
fi

# Check Ollama status
echo "📊 Current Ollama Status:"
echo "----------------------------------------------------------------------"
ollama list 2>/dev/null || echo "   Ollama service not responding"
echo ""

# Define required models for the team
# Format: "model_name:description"
declare -a REQUIRED_MODELS=(
    "antoniohudnall/Mortimer:latest:Primary team model (Sales, Agents, General)"
    "nomic-embed-text:latest:Embeddings for MemoryBridge"
    "phi3:latest:Lightweight fallback (3.8B)"
    "qwen2.5:3b:Multilingual capable fallback"
    "tinyllama:latest:Ultra-lightweight for testing"
    "llama3.2:latest:General purpose (3.2B)"
)

echo "🎯 Required Models for AGI Team:"
echo "----------------------------------------------------------------------"
for model_info in "${REQUIRED_MODELS[@]}"; do
    IFS=':' read -r model desc <<< "$model_info"
    if ollama list 2>/dev/null | grep -q "^${model}"; then
        size=$(ollama list 2>/dev/null | grep "^${model}" | awk '{print $3}')
        echo "   ✅ $model (${size}) - $desc"
    else
        echo "   ⬜ $model - $desc [NEEDS DOWNLOAD]"
    fi
done
echo ""

# Ask to load missing models
read -p "📥 Download missing models? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔄 Downloading missing models..."
    echo "----------------------------------------------------------------------"
    
    for model_info in "${REQUIRED_MODELS[@]}"; do
        IFS=':' read -r model desc <<< "$model_info"
        if ! ollama list 2>/dev/null | grep -q "^${model}"; then
            echo "   📥 Pulling $model..."
            ollama pull "$model" 2>&1 | while read line; do
                echo "      $line"
            done
            echo "   ✅ $model downloaded"
        fi
    done
    
    echo ""
    echo "======================================================================"
    echo "  ✅ ALL MODELS LOADED"
    echo "======================================================================"
else
    echo "⏭️  Skipping downloads. Run this script again to download."
fi

echo ""
echo "📊 Updated Model List:"
echo "----------------------------------------------------------------------"
ollama list 2>/dev/null || echo "   Ollama service not responding"
echo ""
echo "💡 Models are now available for the team."
echo "   Primary: antoniohudnall/Mortimer:latest"
echo "   Fallback: phi3:latest, qwen2.5:3b"
echo "   Embeddings: nomic-embed-text:latest"
