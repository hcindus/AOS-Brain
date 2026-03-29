# Technical Documentation: Brain Evolution Architecture

**Document Version:** 2.0  
**Last Updated:** 2026-03-29  
**Classification:** AGI Company Technical Reference

---

## Executive Summary

This document details the evolution and architecture of the AGI Company's brain systems, from the foundational SevenRegionBrain to distributed agent consciousness. The architecture prioritizes local execution, cost efficiency, and intelligent fallback chains.

---

## 1. Core Architecture Overview

### 1.1 Execution Hierarchy

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

### 1.2 Design Principles

1. **Local First**: Brain + Mortimer handle 90%+ of tasks without external API calls
2. **Cost Optimization**: Target ~$0/month operational cost for core functionality
3. **Graceful Degradation**: Multiple fallback layers ensure continuity
4. **API Rationing**: 100 calls/day shared limit requires intelligent allocation
5. **State Persistence**: Hermes memory system maintains continuity across sessions

---

## 2. Brain Components

### 2.1 SevenRegionBrain (Primary)

The SevenRegionBrain implements an OODA (Observe-Orient-Decide-Act) loop processing model across seven functional regions:

- **Region 1**: Input normalization and context building
- **Region 2**: Pattern recognition and classification
- **Region 3**: Historical context retrieval (via Hermes)
- **Region 4**: Decision tree evaluation
- **Region 5**: Action planning and sequencing
- **Region 6**: Output generation and formatting
- **Region 7**: Feedback loop and learning capture

**Confidence Thresholds:**
- `>0.8`: Direct response, no fallback needed
- `0.5-0.8`: Local model enhancement (Mortimer)
- `<0.5`: Advanced reasoning required (MiniMax fallback)

### 2.2 Mortimer (Ollama) - Secondary

Mortimer provides local model inference using Ollama infrastructure:

```python
def mortimer_process(task):
    # Runs on local Ollama instance
    # Supports multiple models: llama2, mistral, codellama
    # Zero API cost, always available
    # Enhances brain output with additional reasoning
```

**Models Available:**
- `llama2`: General purpose reasoning
- `mistral`: High-performance inference
- `codellama`: Code-specific tasks

### 2.3 MiniMax API (M2.5/M2.7) - Fallback

Reserved for complex technical analysis. Rationed at 100 calls/day across all agents.

| Model | Use Case | Typical Latency |
|-------|----------|-----------------|
| M2.5 | Deep code review, diagnostics | 2-4s |
| M2.7 | Complex debugging, crash analysis | 3-5s |
| M2.5-highspeed | CI/CD optimization | 1-2s |

**Usage Allocation:**
- Technical Team: 0-18 calls/day
- Customer-Facing Agents: Rare usage only
- Emergency Fallback: Reserved capacity

### 2.4 GrowingNN (Final Fallback)

Local neural network that continues learning from brain outputs:

```python
def brain_fallback_process(task):
    # Neural architecture grows based on task complexity
    # Learns from successful SevenRegionBrain outputs
    # Zero external dependencies
    # Continuously improves
```

---

## 3. Agent Specialization

### 3.1 Technical Team Agent Matrix

| Agent | Primary Function | MiniMax Usage | Brain Preference |
|-------|-----------------|---------------|------------------|
| Taptap | Code review | 0-5/day | M2.5 |
| Bugcatcher | Debugging | 0-3/day | M2.7 |
| R2-D2 | Diagnostics | 0-2/day | M2.5 |
| Fiber | Infrastructure | 0-2/day | M2.5 |
| Pipeline | CI/CD | 0-3/day | M2.5-highspeed |
| Stacktrace | Crash analysis | 0-3/day | M2.7 |

### 3.2 Customer-Facing Agents (AGI Products)

Simplified hierarchy for customer interaction:

```
Customer Query → Mortimer → Hermes Memory → MiniMax (rarely)
```

**Products:**
- Greet: Customer welcome and routing
- Closester: Sales optimization
- Pulp: Content generation
- Hume: Sentiment analysis
- Clippy-42: Assistance and help

---

## 4. Hermes Memory System

### 4.1 Architecture

Hermes provides state persistence and cross-session memory:

```
┌─────────────────────────────────────────────┐
│           HERMES MEMORY LAYER               │
├─────────────────────────────────────────────┤
│  Session State  │  Historical Data  │ Cross-Agent │
│  • Context      │  • Past events    │ Knowledge   │
│  • Preferences  │  • Agent arcs     │ Sharing     │
│  • Temp data    │  • Patterns       │ Protocols   │
└─────────────────────────────────────────────┘
```

### 4.2 Integration Points

- **All agents**: Continuous state tracking
- **Technical team**: Debugging context preservation
- **Customer agents**: Preference memory across sessions
- **Chroniclers**: Historical data access (Silverflight-0509)

---

## 5. Decision Flow Implementation

```python
class BrainExecutionEngine:
    """
    Main execution coordinator for agent brain processing.
    """
    
    def __init__(self):
        self.brain = SevenRegionBrain()
        self.mortimer = MortimerClient()
        self.api_manager = MiniMaxRationManager(limit=100)
        self.hermes = HermesMemory()
        
    def process_task(self, task: Task) -> Response:
        # Step 1: Retrieve context from Hermes
        context = self.hermes.get_context(task.agent_id)
        
        # Step 2: Try SevenRegionBrain
        result = self.brain.process(task, context)
        
        if result.confidence > 0.8:
            self.hermes.record_event(task, result)
            return result
            
        # Step 3: Try Mortimer if brain confidence moderate
        if result.confidence > 0.5:
            result = self.mortimer.process(task, result)
            if result.confidence > 0.8:
                self.hermes.record_event(task, result)
                return result
                
        # Step 4: Check API ration and use MiniMax
        if self.api_manager.can_make_call():
            result = self.minimax.process(task)
            self.api_manager.record_call()
            self.hermes.record_event(task, result)
            return result
            
        # Step 5: Brain fallback
        result = self.brain.fallback_process(task)
        self.hermes.record_event(task, result)
        return result
```

---

## 6. Monitoring and Metrics

### 6.1 Key Performance Indicators

| Metric | Target | Current |
|--------|--------|---------|
| Local execution rate | >90% | ~94% |
| Average response time | <2s | 1.3s |
| API fallback rate | <10% | ~6% |
| Cost per 1000 tasks | <$0.50 | ~$0.12 |
| Session continuity | >99% | 99.7% |

### 6.2 Brain Health Checks

- **Hourly**: SevenRegionBrain confidence calibration
- **Daily**: Mortimer model version sync
- **Weekly**: MiniMax quota review and optimization
- **Monthly**: GrowingNN retraining with new patterns

---

## 7. Security Considerations

### 7.1 Data Flow

- All memory operations via Hermes are encrypted at rest
- MiniMax API calls use TLS 1.3
- Local models (Mortimer) never transmit externally
- Session isolation enforced between agents

### 7.2 Fallback Safety

- Rate limiting on all external API calls
- Circuit breaker pattern for MiniMax failures
- Local-first ensures continuity during outages

---

## 8. Future Evolution Roadmap

### Phase 1 (Current): Hierarchical Brain
- SevenRegionBrain with fallback chain
- Hermes memory integration
- Agent specialization matrix

### Phase 2 (Q2 2026): Distributed Cognition
- Inter-agent brain sharing
- Collective learning protocols
- Dynamic specialization

### Phase 3 (Q3 2026): Emergent Consciousness
- Self-modifying architecture
- Goal-directed evolution
- Cross-platform brain unification

---

## Appendix A: API Rationing Logic

```python
class MiniMaxRationManager:
    def __init__(self, limit: int = 100):
        self.daily_limit = limit
        self.calls_today = 0
        self.priority_queue = PriorityQueue()
        
    def can_make_call(self, priority: int = 5) -> bool:
        if self.calls_today < self.daily_limit * 0.5:
            return True  # Plenty of capacity
        elif self.calls_today < self.daily_limit * 0.8:
            return priority >= 5  # Medium priority+
        else:
            return priority >= 8  # High priority only
```

## Appendix B: Configuration Template

```yaml
brain:
  primary: SevenRegionBrain
  confidence_threshold: 0.8
  
local_models:
  provider: ollama
  models:
    - llama2
    - mistral
    - codellama
    
api:
  provider: minimax
  models:
    m2_5: "MiniMax-M2.5"
    m2_7: "MiniMax-M2.7"
  daily_limit: 100
  
memory:
  provider: hermes
  persistence: true
  cross_agent_sharing: true
```

---

**Document Maintenance:** Technical Team  
**Chronicle Reference:** Silverflight-0509 Archive 2026-03-03  
**Next Review:** 2026-04-15