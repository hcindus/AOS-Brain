#!/bin/bash
# Ternary-Bonsai-8B Q2_0 Bridge for AOS Brain
# Routes decision tasks to quantized model

PRISM_LLAMA="/tmp/prism-llama.cpp/build/bin/llama-cli"
MODEL_PATH="/root/Ternary-Bonsai-8B-Q2_0.gguf"

# Function to query Ternary-Bonsai
query_ternary() {
    local prompt="$1"
    local max_tokens="${2:-50}"
    local temp="${3:-0.7}"
    
    # Run inference
    "$PRISM_LLAMA" -m "$MODEL_PATH" \
        -p "$prompt" \
        -n "$max_tokens" \
        --temp "$temp" \
        --no-display-prompt 2>/dev/null | tail -n 5
}

# Main handler
case "$1" in
    "decide")
        # Decision-making task
        context="${2:-unknown}"
        response=$(query_ternary "Decision: $context. Choose best action." 30 0.5)
        echo "{\"model\":\"ternary-bonsai-q2:8b\",\"decision\":\"$response\",\"confidence\":0.85}"
        ;;
    "analyze")
        # Analysis task
        text="${2:-}"
        response=$(query_ternary "Analyze: $text" 100 0.7)
        echo "$response"
        ;;
    "health")
        # Health check
        if [ -f "$MODEL_PATH" ] && [ -x "$PRISM_LLAMA" ]; then
            echo "{\"status\":\"healthy\",\"model_size\":\"2.7GB\",\"format\":\"Q2_0\"}"
        else
            echo "{\"status\":\"error\",\"message\":\"Model or binary not found\"}"
        fi
        ;;
    *)
        echo "Usage: $0 {decide|analyze|health} [context]"
        exit 1
        ;;
esac