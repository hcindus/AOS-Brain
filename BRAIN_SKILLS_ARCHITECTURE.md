# Brain-as-Skills Architecture
## A Skills-First Cognitive System for AOS

**Version:** 0.1.0  
**Date:** 2026-03-31  
**Status:** Proposal

---

## 1. Executive Summary

The AOS Brain evolves from a monolithic Python class hierarchy into a **skills-first cognitive substrate**. Each brain region becomes a skill consumer, the brain becomes a skill orchestrator, and agents gain self-diagnostic capabilities through a unified skill registry.

**Key Shift:** Brain regions don't BE agents; they CALL skills. The brain becomes a skill execution engine with OODA coordination.

---

## 2. Current State (Snapshot)

```
SevenRegionBrain (monolithic)
├── Thalamus → Python class
├── Hippocampus → Python class
├── Limbic → Python class
├── PFC → Python class + Ollama
├── Basal Ganglia → Python class
├── Cerebellum → Python class
└── Brainstem → Python class

Problems:
- Regions tightly coupled to implementation
- No self-healing capability
- Hardcoded logic, not composable
- Agent integration requires code changes
```

---

## 3. Proposed Architecture

### 3.1 Core Concept: The Skill-Executing Brain

```
┌─────────────────────────────────────────────┐
│           SKILL ORCHESTRATOR                │
│  ┌─────────────────────────────────────┐    │
│  │          OODA COORDINATOR          │    │
│  │   Observe → Orient → Decide → Act  │    │
│  └─────────────────────────────────────┘    │
│                      ↓                      │
│  ┌─────────────────────────────────────┐    │
│  │      SKILL REGISTRY & CONTRACTS     │    │
│  │  • Routes region calls to skills    │    │
│  │  • Validates input/output contracts │    │
│  │  • Manages versioning               │    │
│  └─────────────────────────────────────┘    │
│                      ↓                      │
│  ┌─────────────────────────────────────┐    │
│  │      SKILL EXECUTION LAYER          │    │
│  │  • Internal skills (fast path)      │    │
│  │  • Agent skills (async path)        │    │
│  │  • External skills (API path)       │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│         BRAIN REGION SKILLS                 │
│                                             │
│  brain.thalamus.process → SKILL:thalamus-v1│
│  brain.pfc.decide → SKILL:pfc-v2             │
│  brain.limbic.evaluate → SKILL:limbic-v1   │
│  ...                                         │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│         SELF-DIAGNOSTIC SKILLS              │
│                                             │
│  SKILL:brain-health-check                   │
│  SKILL:memory-consolidation                 │
│  SKILL:region-restart                       │
│  SKILL:tick-recovery                        │
│  SKILL:growingnn-tune                       │
└─────────────────────────────────────────────┘
```

### 3.2 Skill Tiers for Brain

| Tier | Scope | Examples | Execution |
|------|-------|----------|-----------|
| **Standard** | Safety, format, brand | `brainstem-safety-check`, `thalamus-normalize` | Internal, 5ms |
| **Methodology** | Cognitive workflows | `pfc-decision-tree`, `hippocampus-consolidate` | Internal + Ollama, 50ms |
| **Personal** | Agent-specific behaviors | `mylonen-navigation`, `mylzeron-mining` | Agent-loaded, 200ms |
| **Diagnostic** | Self-healing | `brain-health-check`, `tick-recovery` | System, 10ms |

### 3.3 Contract-Based Communication

Every skill exposes a contract:

```yaml
# SKILL:thalamus-v1
---
name: thalamus
version: "1.0.0"
tier: standard
description: "Normalize and route sensory input to appropriate regions"
contracts:
  input:
    type: object
    required: [source, data, timestamp]
    properties:
      source: {type: string, enum: [sensor, agent, system]}
      data: {type: any}
      timestamp: {type: number}
  output:
    type: object
    required: [normalized, priority, routing]
    properties:
      normalized: {type: object}
      priority: {type: number, min: 0, max: 1}
      routing: {type: array, items: {type: string}}
---

# Skill implementation (can be Python, JS, or agent)
```

---

## 4. Technical Specifications

### 4.1 Skill Registry

```python
class SkillRegistry:
    """Central registry for brain skills."""
    
    def __init__(self):
        self.skills = {}  # name -> Skill
        self.contracts = {}  # name -> Contract
        self.versions = {}  # name -> [versions]
    
    def register(self, skill: Skill):
        """Register a skill with validation."""
        # Validate contract
        validate_contract(skill.contract)
        # Store with version
        self.skills[f"{skill.name}@{skill.version}"] = skill
    
    def call(self, name: str, input: dict, timeout_ms: int = 100) -> dict:
        """Call skill with contract validation."""
        skill = self.resolve(name)
        # Validate input against contract
        validate_input(skill.contract.input, input)
        # Execute
        result = skill.execute(input)
        # Validate output
        validate_output(skill.contract.output, result)
        return result
```

### 4.2 Region-as-Skill-Consumer

```python
class ThalamusRegion:
    """Thalamus now calls skills instead of hardcoded logic."""
    
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.primary_skill = "thalamus-v1.0.0"
    
    def process(self, sensory_input: dict) -> dict:
        """Process sensory input via skill."""
        return self.registry.call(
            self.primary_skill,
            input=sensory_input,
            timeout_ms=10  # Standard tier = fast
        )
```

### 4.3 Self-Diagnostic System

```python
class BrainDiagnostics:
    """Continuous health monitoring via skills."""
    
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.health_log = []
    
    def check(self) -> HealthReport:
        """Run full diagnostic suite."""
        checks = {
            "tick_latency": self.registry.call("tick-latency-check", {}),
            "memory_health": self.registry.call("memory-health-check", {}),
            "ollama_connectivity": self.registry.call("ollama-ping", {}),
            "skill_registry": self.registry.call("registry-validate", {}),
        }
        
        if any(check.status == "fail" for check in checks.values()):
            return self.registry.call("tick-recovery", {"checks": checks})
        
        return HealthReport(status="healthy", checks=checks)
```

---

## 5. Implementation Phases

### Phase 1: Foundation (Week 1)

**Goal:** Create skill infrastructure

**Tasks:**
1. Extend SKILL.md format with contracts
2. Create `SkillRegistry` class
3. Build contract validation
4. Add skill versioning

**Deliverables:**
- `/skills/brain-registry/` - Registry implementation
- `/skills/contract-validator/` - Contract validation skill

### Phase 2: Diagnostic Skills (Week 2)

**Goal:** Brain can self-diagnose

**New Skills:**
```
skills/
├── brain-health-check/
│   └── SKILL.md
├── memory-consolidation/
│   └── SKILL.md
├── region-restart/
│   └── SKILL.md
├── tick-recovery/
│   └── SKILL.md
└── growingnn-tune/
    └── SKILL.md
```

**Integration:**
```python
# Brain now has diagnostics
brain = SevenRegionBrain()
brain.diagnostics = BrainDiagnostics(registry)

# Auto-run every 100 ticks
if brain.tick_count % 100 == 0:
    report = brain.diagnostics.check()
    if report.status != "healthy":
        brain.recover(report)
```

### Phase 3: Region Migration (Week 3-4)

**Goal:** Convert regions to skill consumers

**Migration Order:**
1. **Thalamus** (simplest, sensory routing)
2. **Brainstem** (safety checks)
3. **Limbic** (emotion/reward)
4. **PFC** (complex, requires Ollama integration)
5. **Hippocampus** (memory consolidation)
6. **Basal Ganglia** (action selection)
7. **Cerebellum** (motor coordination)

**Example Migration:**
```python
# BEFORE: Hardcoded
class ThalamusRegion:
    def process(self, data):
        if data['type'] == 'visual':
            return self.normalize_visual(data)
        elif data['type'] == 'audio':
            return self.normalize_audio(data)

# AFTER: Skill-based
class ThalamusRegion:
    def __init__(self, registry):
        self.skill = registry.get('thalamus-v1')
    
    def process(self, data):
        return self.skill.call(input=data)
```

### Phase 4: Agent Integration (Week 5-6)

**Goal:** Agents discover and use brain skills

```yaml
# Agent skill assignment
---
agent: mylonen
skills:
  - brain.sensory-input
  - brain.motor-output
  - brain.region-restart  # Can restart stuck regions!
version: "1.0.0"
---
```

---

## 6. Example: Complete System

### 6.1 Skill Definition

```markdown
<!-- skills/brain-health-check/SKILL.md -->
---
name: brain-health-check
version: "1.0.0"
tier: diagnostic
description: "Check brain health metrics and return status report"
contracts:
  input:
    type: object
    properties:
      detailed: {type: boolean, default: false}
  output:
    type: object
    required: [status, metrics, recommendations]
    properties:
      status: {type: string, enum: [healthy, warning, critical]}
      metrics: {type: object}
      recommendations: {type: array, items: {type: string}}
---

# Brain Health Check

Analyzes brain state and returns health metrics.

## Metrics Checked

1. **Tick Latency** - Time between ticks (target: <200ms)
2. **Memory Pressure** - Short/mid/long-term memory usage
3. **Ollama Connectivity** - Model availability and response time
4. **Skill Registry** - All registered skills responding
5. **GrowingNN Status** - Node growth, error rates

## Usage

```python
result = registry.call("brain-health-check", {"detailed": True})
# Returns:
# {
#   "status": "warning",
#   "metrics": {"tick_latency_ms": 150, "memory_usage": 0.7},
#   "recommendations": ["Consider memory consolidation"]
# }
```
```

### 6.2 Usage in Brain

```python
# Brain now uses skills for everything

class SevenRegionBrain:
    def __init__(self):
        self.registry = SkillRegistry()
        self._load_core_skills()
        self.diagnostics = BrainDiagnostics(self.registry)
        
        # Regions are now thin wrappers
        self.thalamus = ThalamusRegion(self.registry)
        self.pfc = PFCRegion(self.registry)
        # ... etc
    
    def tick(self, observation: Observation) -> Thought:
        """One OODA cycle using skills."""
        
        # 1. Observe - via Thalamus skill
        sensory = self.thalamus.process(observation)
        
        # 2. Orient - via Hippocampus skill
        context = self.registry.call("hippocampus-query", {
            "pattern": sensory.signature
        })
        
        # 3. Decide - via PFC skill
        decision = self.pfc.decide(sensory, context)
        
        # 4. Act - via Basal Ganglia skill
        action = self.registry.call("basal-select", {
            "candidates": decision.options,
            "context": context
        })
        
        # 5. Health check every 100 ticks
        if self.tick_count % 100 == 0:
            health = self.diagnostics.check()
            if health.status != "healthy":
                self.registry.call("tick-recovery", health)
        
        return Thought(observation, decision, action)
```

---

## 7. Benefits

| Benefit | Description |
|---------|-------------|
| **Self-Healing** | Brain diagnoses and fixes its own issues via skills |
| **Composability** | Skills compose into cognitive workflows |
| **Versioning** | Brain regions versioned like software |
| **Agent-Readable** | Agents understand brain capabilities via contracts |
| **Testability** | Skills tested independently, brain more reliable |
| **Extensibility** | Add new cognitive capabilities by adding skills |
| **Fallback Chains** | Skills can call other skills for resilience |

---

## 8. Open Questions

1. **Performance**: Contract validation adds latency. Solution: Cache compiled contracts.
2. **Debugging**: More layers = harder debugging. Solution: Full tracing in skill calls.
3. **Complexity**: Skill management overhead. Solution: Automated registry maintenance.

---

## 9. Next Steps

1. **Review** this architecture
2. **Prototype** Phase 1 (SkillRegistry + contracts)
3. **Test** with one region (Thalamus)
4. **Iterate** on contract schemas
5. **Migrate** remaining regions

---

## Appendix: File Structure

```
~/.aos/aos/
├── aos_brain_py/
│   ├── brain/
│   │   ├── skill_orchestrator.py      # NEW
│   │   ├── skill_registry.py          # NEW
│   │   ├── contract_validator.py      # NEW
│   │   ├── region_thalamus.py         # MODIFIED
│   │   ├── region_pfc.py              # MODIFIED
│   │   └── ...
│   └── skills/                        # NEW
│       ├── brain-health-check/
│       │   └── SKILL.md
│       ├── thalamus-v1/
│       │   └── SKILL.md
│       ├── pfc-v2/
│       │   └── SKILL.md
│       └── ...
└── agents/
    └── {agent_name}/
        └── skills/
            └── active_skills.json     # Points to brain skills
```

---

**Word Count:** ~1,850 words

**Ready to play?** Start with Phase 1: `SkillRegistry` implementation.
