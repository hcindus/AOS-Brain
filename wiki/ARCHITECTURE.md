# AGENT ARCHITECTURE HIERARCHY
## Clear Model Fallback Chain

---

## EXECUTION ORDER

```
USER REQUEST
      ↓
[1] LOCAL BRAIN (SevenRegionBrain) ← PRIMARY
      ↓ (if insufficient/confident)
[2] LOCAL MODELS (Mortimer/Ollama) ← SECONDARY
      ↓ (if needs advanced reasoning)
[3] MINIMAX API (M2.5/M2.7) ← FALLBACK ONLY
      ↓ (if API limit reached)
[4] BRAIN FALLBACK (GrowingNN local) ← FINAL
```

---

## TECHNICAL TEAM FALLBACK CHAIN

| Priority | Model | When Used | Cost |
|----------|-------|-----------|------|
| **1** | **SevenRegionBrain** | Always first - OODA loop processing | $0 |
| **2** | **Mortimer (Ollama)** | Brain needs reasoning boost | $0 |
| **3** | **MiniMax-M2.5/M2.7** | Complex analysis, debugging, planning | API rationed |
| **4** | **GrowingNN (local)** | Everything else failed | $0 |

---

## SKILL ACQUISITION (NOT EXECUTION)

Skills are being added FROM these sources TO the team:

### From Mini-Agent → Technical Team
- Deep code analysis techniques
- Debugging pattern recognition  
- Error diagnosis frameworks
- Reasoning methodologies

### From Hermes → All Agents
- State persistence patterns
- Cross-session memory
- Historical tracking methods
- Shared knowledge protocols

**NOTE:** These are SKILLS/TECHNIQUES being integrated, not runtime dependencies.

---

## API RATIONING (MiniMax)

**100 calls/day shared across all agents**

### Technical Team MiniMax Usage:
| Agent | Use Case | Model | Typical Calls/Day |
|-------|----------|-------|-------------------|
| Taptap | Deep code review | M2.5 | 0-5 |
| Bugcatcher | Complex debugging | M2.7 | 0-3 |
| R2-D2 | Technical diagnostics | M2.5 | 0-2 |
| Fiber | Infrastructure analysis | M2.5 | 0-2 |
| Pipeline | CI/CD optimization | M2.5-highspeed | 0-3 |
| Stacktrace | Crash analysis | M2.7 | 0-3 |

**TOTAL ESTIMATED:** 0-18 calls/day (well under 100 limit)

---

## DECISION FLOW FOR TECHNICAL AGENTS

```python
def process_task(task):
    # Step 1: Try local brain
    result = brain.process(task)
    if result.confidence > 0.8:
        return result
    
    # Step 2: Try Mortimer
    if result.confidence > 0.5:
        result = mortimer.process(task)
        if result.confidence > 0.8:
            return result
    
    # Step 3: Check API ration
    if api_manager.can_make_call():
        # Step 3a: Route to MiniMax (fallback)
        result = minimax.process(task)
        api_manager.record_call()
        return result
    
    # Step 4: Brain fallback
    return brain.fallback_process(task)
```

---

## HERMES vs MINIMAX

| Aspect | Hermes | MiniMax |
|--------|--------|---------|
| **Type** | State tracking | API model |
| **Cost** | $0 | Rationed (100/day) |
| **Use** | Always active | Fallback only |
| **Purpose** | Memory/persistence | Reasoning/analysis |
| **Integration** | All agents | Technical team |

---

## CLARIFICATION: AGI PRODUCTS

The **AGI Products** (Greet, Closester, Pulp, Hume, Clippy-42) are CUSTOMER-FACING and run on **Mortimer primarily**:

- **Primary:** Mortimer (Ollama) - $0, always available
- **Enhancement:** Hermes persistence - memory across sessions
- **Fallback:** MiniMax for complex queries (if customer needs deep analysis)

These are NOT technical agents - they use simplified hierarchy:
```
Customer Query → Mortimer → Hermes Memory → MiniMax (rarely)
```

---

## SUMMARY

✅ **Local First** - Brain + Mortimer handle 90%+ of tasks
✅ **MiniMax Fallback** - Only for complex technical needs
✅ **Hermes Always** - State tracking active for all agents
✅ **Rationed API** - 100 calls/day, use sparingly
✅ **Cost Optimized** - ~$0/month with smart fallback chain

**The Technical Team is self-sufficient with local resources. MiniMax is the safety net, not the foundation.**
