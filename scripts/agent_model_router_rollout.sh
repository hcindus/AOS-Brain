#!/bin/bash
# agent_model_router_rollout.sh
# Rollout Model Router integration to all agents

echo "=============================================="
echo "🤖 AGENT MODEL ROUTER ROLLOUT v3.1"
echo "=============================================="
echo ""

AGENTS_DIR="/root/.openclaw/workspace/agent_sandboxes"
SHARED_DIR="/root/.openclaw/workspace/agents/shared"

# Function to integrate Model Router into an agent
integrate_agent() {
    local agent_name=$1
    local agent_dir="$AGENTS_DIR/$agent_name"
    
    echo "[$agent_name] Integrating Model Router..."
    
    # Create integration file
    cat > "$agent_dir/model_router_integration.py" << 'EOF'
"""Model Router Integration for Agent - Auto-generated v3.1"""
import sys
sys.path.insert(0, '/root/.openclaw/workspace/agents/shared')

try:
    from agent_model_router import get_model_router, check_router_status
    
    # Initialize router on import
    model_router = get_model_router()
    
    # Helper functions
    def decide(context):
        """Make decision using Bonsai/tinyllama"""
        return model_router.decide(context)
    
    def speak(message, context=None):
        """Generate voice response using Mort_II"""
        return model_router.speak(message, context)
    
    def reason(prompt, max_tokens=500):
        """Complex reasoning using qwen2.5:14b"""
        return model_router.reason(prompt, max_tokens)
    
    def code(prompt, language="python", max_tokens=300):
        """Code generation using phi3:medium"""
        return model_router.code(prompt, language, max_tokens)
    
    def ask(question, max_tokens=200):
        """General questions using llama3.1:latest"""
        return model_router.ask(question, max_tokens)
    
    def analyze(text, task="summarize", max_tokens=300):
        """Analysis using mistral:latest MoE"""
        return model_router.analyze(text, task, max_tokens)
    
    def get_router_status():
        """Get Model Router status"""
        return check_router_status()
    
    MODEL_ROUTER_READY = True
    
except ImportError as e:
    MODEL_ROUTER_READY = False
    print(f"⚠️ Model Router not available: {e}")
    
    # Dummy functions
    def decide(c): return "CONTINUE", 0.5
    def speak(m, c=None): return "[Model Router offline]"
    def reason(p, mt=500): return "[Model Router offline]"
    def code(p, l="python", mt=300): return "[Model Router offline]"
    def ask(q, mt=200): return "[Model Router offline]"
    def analyze(t, task="summarize", mt=300): return "[Model Router offline]"
    def get_router_status(): return {"status": "offline"}
EOF

    # Create README for agent
    cat > "$agent_dir/MODEL_ROUTER_README.md" << EOF
# Model Router Integration v3.1

## Quick Start
Import the integration in your agent controller:

\`\`\`python
from model_router_integration import decide, speak, reason, code, ask, analyze

# Decision making
action, confidence = decide({"novelty": 0.8, "phase": "Explore"})

# Voice/Chat
response = speak("Hello", {"situation": "greeting"})

# Complex reasoning
analysis = reason("Explain quantum computing")

# Code generation
code_result = code("Sort a list", "python")

# General questions
answer = ask("What is the capital of France?")

# Text analysis
summary = analyze("Long text...", "summarize")
\`\`\`

## Available Models (8 total)
- **Bonsai-8b-q1_0** - 1-bit decisions (cached)
- **tinyllama** - Fast decision fallback
- **Mort_II** - Voice/natural language
- **nomic-embed-text** - Embeddings
- **qwen2.5:14b** - Complex reasoning
- **phi3:medium** - Code generation
- **llama3.1:latest** - General questions
- **mistral:latest** - Analysis (MoE)

## Bridge Endpoint
http://127.0.0.1:11435
EOF

    echo "  ✓ Created model_router_integration.py"
    echo "  ✓ Created MODEL_ROUTER_README.md"
}

# Integrate each agent
echo "📦 Rolling out to agents..."
echo ""

integrate_agent "patricia"
integrate_agent "forge"
integrate_agent "chelios"
integrate_agent "jordan"

echo ""
echo "=============================================="
echo "✅ ROLLOUT COMPLETE"
echo "=============================================="
echo ""
echo "All agents now have Model Router integration:"
echo "  ✓ Patricia (Factory Controller)"
echo "  ✓ Forge (Factory Controller)"
echo "  ✓ Chelios (Security Controller)"
echo "  ✓ Jordan (Office Controller)"
echo ""
echo "Usage in agent controllers:"
echo "  from model_router_integration import decide, speak, reason, code, ask, analyze"
echo ""
echo "Next: Update agent controllers to use these functions"
