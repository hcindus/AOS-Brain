# Memory Bridge Documentation

## Purpose
Connects the AOS Brain's limbic system to workspace memory files (MEMORY.md, memory/*.md) for automatic semantic retrieval when novelty is high.

## Architecture

### Components
1. **MemoryBridge Class** (`memory_bridge.py`)
   - Indexes workspace memory files using Ollama embeddings (nomic-embed-text)
   - Stores embeddings in-memory (no external DB required)
   - Provides semantic similarity search

2. **OODA Integration** (`ooda.py`)
   - Initializes MemoryBridge on startup
   - Queries memory when `novelty > 0.75` or `novelty > avg + 0.15`
   - Injects results into context for conscious layer
   - Writes workspace_memory to brain_state.json

### Data Flow
```
Tick → Limbic evaluates novelty → If high → Query MemoryBridge → 
Embed query → Cosine similarity search → Return top-2 results → 
Inject into ctx["workspace_memory"] → Conscious layer can access
```

## Configuration
- **Similarity threshold:** 0.5 (cosine similarity)
- **Novelty trigger:** 0.75
- **Max results:** 2 chunks
- **Embedding model:** nomic-embed-text:latest (768-dim)

## Files Indexed
- `/root/.openclaw/workspace/MEMORY.md`
- `/root/.openclaw/workspace/memory/*.md`

## Testing
```bash
cd /root/.openclaw/workspace/AOS/brain
python3 memory_bridge.py  # Standalone test
python3 -c "from ooda import OODA; ooda.tick()"  # Integration test
```

## Status Output
When memory is retrieved, brain_state.json includes:
```json
{
  "workspace_memory": {
    "queried": true,
    "source_count": 2,
    "results": [
      {"source": "memory/2026-03-16.md", "relevance": 0.587, "text": "..."}
    ]
  }
}
```

## Deployment Notes
- No restart required for new memory files (auto-indexed on query)
- Errors are caught and logged, don't crash brain
- Embeddings cached in MemoryBridge instance
