# Agent Beta — Integration Tester
## Assignment: BQL-004 and BQL-005

**Agent ID:** Beta  
**Specialty:** Ollama integration, benchmarking, A/B testing  
**Reports to:** Patricia/Patricia2  

### Mission
Validate Qwen3.5 as viable Bonsai replacement for Brain decision routing.

### Tasks

#### BQL-004: Qwen3.5 Decision Benchmark

**Test Protocol:**

```bash
# 1. Baseline: tinyllama decision quality
curl http://localhost:11434/api/generate -d '{
  "model": "tinyllama:latest",
  "prompt": "Context: novelty=0.8, urgency=high, phase=Orient\nActions: EXPLORE, ANALYZE, REST\nDecision:",
  "stream": false
}'

# 2. Test: Qwen3.5 decision quality  
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3.5:latest",
  "prompt": "Context: novelty=0.8, urgency=high, phase=Orient\nActions: EXPLORE, ANALYZE, REST\nDecision:",
  "stream": false
}'
```

**Decision Prompts to Test:**
1. High novelty, low urgency → should suggest EXPLORE
2. Low signal quality, Orient phase → should suggest ANALYZE  
3. High confidence, Act phase → should suggest ACT
4. Memory pressure → should suggest REST

**Metrics:**
- Decision accuracy (did it choose wisely?)
- Latency (target: < 3 seconds)
- Memory usage (target: < 6GB)
- Consistency (same context → same decision?)

#### BQL-005: Brain Router Integration Test

**Test Scenario:**
```python
# Temporarily switch router to Qwen3.5
# Run 100 decision cycles
# Compare to tinyllama baseline
```

**Integration Checklist:**
- [ ] Router can call Qwen3.5 via API
- [ ] Response parsing works (action extraction)
- [ ] Fallback triggers correctly on timeout
- [ ] Brain v4.5 accepts decisions without error

### Deliverables
1. `benchmark-tinyllama-vs-qwen3.5.md` — Comparative analysis
2. `integration-test-results.md` — Router compatibility report
3. `recommendation.md` — Should we adopt Qwen3.5?

### Decision Matrix

| Criteria | Weight | tinyllama | Qwen3.5 | Winner |
|----------|--------|-----------|---------|--------|
| Latency | 30% | ~900ms | ~? | TBD |
| Quality | 40% | Baseline | TBD | TBD |
| Memory | 20% | 645MB | ~6GB | tinyllama |
| Reliability | 10% | High | TBD | TBD |

### Success Criteria
✅ Qwen3.5 decisions ≥ 90% as good as tinyllama OR  
✅ Document why tinyllama remains superior OR  
✅ Propose hybrid approach (context-aware model selection)

---
*Assigned: 2026-04-22 01:57 UTC*
