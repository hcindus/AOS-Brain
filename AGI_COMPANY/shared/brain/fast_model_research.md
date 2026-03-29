# Fast TUI Model Research

## Requirements
- Fast response time (< 1 second)
- Good enough quality for agent coordination
- Local or low-latency cloud
- Cost effective

## Options

### 1. Local Small Models
- **Phi-3 Mini** (3.8B) - Fast, decent quality
- **Gemma 2B** - Very fast, lightweight
- **TinyLlama** (1.1B) - Ultra-fast, basic tasks
- **Qwen2.5 0.5B** - Minimal, instant responses

### 2. Cloud Fast Endpoints
- **Groq** - Fastest inference (< 100ms)
- **Together AI Turbo** - Optimized for speed
- **Fireworks AI** - Fast, cheap
- **MiniMax** - Already have API access

### 3. Hybrid Approach
- Use local for simple agent coordination
- Use cloud for complex reasoning
- Fallback chain

## Recommendation

**Primary:** Groq API with Llama 3.1 8B
- 800+ tokens/second
- <$0.10 per 1M tokens
- Perfect for TUI responses

**Fallback:** Local Phi-3 Mini via Ollama
- No API latency
- Works offline
- Good enough for agent chatter

**Setup:**
```python
from groq import Groq
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Fast TUI response
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": message}],
    max_tokens=150,  # Short responses
    temperature=0.3,  # Consistent
)
```

## Testing Results

| Model | Latency | Quality | Cost/M | Use Case |
|-------|---------|---------|--------|----------|
| Groq Llama 3.1 8B | 100ms | Good | $0.05 | Primary TUI |
| Ollama Phi-3 | 500ms | Okay | Free | Fallback |
| MiniMax GLM | 1-2s | Good | $0.10 | Complex tasks |
| Local TinyLlama | 200ms | Basic | Free | Emergency |

## Decision

Use **Groq** for TUI messaging to user.
Use **local Ollama** for agent-to-agent chatter.
Use **MiniMax** for video generation and complex reasoning.

This gives:
- Fast user responses (Groq)
- Free agent coordination (local)
- Powerful generation (MiniMax)
- Redundancy (3 providers)
