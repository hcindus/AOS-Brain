# AOS Brain: Technical Specification
## Skills-First Cognitive Architecture v1.0

---

## 1. System Overview

### 1.1 Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                      SKILL ORCHESTRATOR                     │
├─────────────────────────────────────────────────────────────┤
│  OODA Loop (Observe → Orient → Decide → Act)              │
│  └─ Coordinates via SkillRegistry                         │
├─────────────────────────────────────────────────────────────┤
│  Skill Registry                                             │
│  ├─ Contract validation                                   │
│  ├─ Version management                                      │
│  ├─ Routing to handlers                                   │
│  └─ Performance tracking                                  │
├─────────────────────────────────────────────────────────────┤
│  Region Consumers (thin wrappers)                         │
│  ├─ ThalamusRegion → SKILL:thalamus-v1                  │
│  ├─ PFCRegion → SKILL:pfc-v2                            │
│  └─ ...                                                   │
├─────────────────────────────────────────────────────────────┤
│  Self-Diagnostics                                           │
│  ├─ Health check (every 100 ticks)                        │
│  ├─ Auto-recovery (tick-recovery skill)                   │
│  └─ GrowingNN tuning                                      │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow

```
Input (Observation)
    ↓
[SKILL:thalamus-v1] → Normalization + Routing
    ↓
[SKILL:pfc-v2] → Decision-making
    ↓
Output (Action)
    ↓
Health Check (every 100 ticks)
```

---

## 2. Skill Specification

### 2.1 Skill File Structure

```
skills/
└── {skill-name}-v{version}/
    ├── SKILL.md          # Contract + documentation
    ├── handler.py        # Implementation
    └── schema.json       # JSON Schema (optional)
```

### 2.2 SKILL.md Format

```yaml
---
name: {skill-name}
version: "{semver}"
tier: {standard|methodology|personal|diagnostic}
description: "{clear, specific description}"
contracts:
  input:
    type: object
    required: [field1, field2]
    properties:
      field1: {type: string}
      field2: {type: number}
  output:
    type: object
    required: [result]
    properties:
      result: {type: any}
---

# {Skill Title}

Detailed documentation...

## Example

```python
result = registry.call("{skill-name}", {
    "field1": "value",
    "field2": 42
})
```
```

### 2.3 Handler Interface

```python
# handler.py
def {skill_name}_handler(input_data: dict) -> dict:
    """
    Implement skill logic.
    
    Args:
        input_data: Validated per contract.input
        
    Returns:
        dict matching contract.output
    """
    # Implementation
    return {"result": ...}
```

---

## 3. API Reference

### 3.1 SkillRegistry

```python
class SkillRegistry:
    def register(self, skill: Skill) -> bool
    def get(self, name: str, version: Optional[str] = None) -> Optional[Skill]
    def call(self, name: str, input_data: Dict, version: Optional[str] = None, timeout_ms: int = 100) -> Dict
    def list_skills(self, tier: Optional[SkillTier] = None) -> List[Skill]
    def health_check(self) -> Dict
```

### 3.2 SevenRegionBrainV2

```python
class SevenRegionBrainV2:
    def __init__(self, config_path: Optional[str] = None)
    def tick(self, observation: Dict) -> Dict
    def run_forever(self)
    def get_health(self) -> Dict
```

### 3.3 BrainClient (for Agents)

```python
class BrainClient:
    def __init__(self, brain_url: str = "http://localhost:5000")
    def discover_skills(self) -> List[Dict]
    def call_skill(self, skill_name: str, input_data: Dict) -> Dict
    def get_brain_health(self) -> Dict
    def process_sensory(self, source: str, data: any, priority: float = 0.5) -> Dict
    def request_decision(self, context: Dict, options: List[Dict]) -> Dict
```

---

## 4. Performance Specifications

### 4.1 Latency Targets

| Tier | Target Latency | Max Latency | Use Case |
|------|------------------|-------------|----------|
| Standard | 5ms | 20ms | Routing, safety checks |
| Methodology | 50ms | 200ms | Decision-making, memory query |
| Personal | 200ms | 500ms | Agent-specific behaviors |
| Diagnostic | 10ms | 50ms | Health checks, recovery |

### 4.2 Throughput

- **Ticks/second:** 5+ (sustained)
- **Skill calls/second:** 100+ (burstable)
- **Registry queries/second:** 1000+

### 4.3 Reliability

- **Uptime SLA:** 99.9%
- **Auto-recovery:** <100ms detection, <500ms recovery
- **Skill success rate:** 99.5% (with contract validation)

---

## 5. Contract Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "version", "tier", "contracts"],
  "properties": {
    "name": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
    "tier": {"enum": ["standard", "methodology", "personal", "diagnostic"]},
    "description": {"type": "string", "maxLength": 500},
    "contracts": {
      "type": "object",
      "required": ["input", "output"],
      "properties": {
        "input": {"type": "object"},
        "output": {"type": "object"}
      }
    }
  }
}
```

---

## 6. Configuration

### 6.1 Brain Configuration (config.yaml)

```yaml
brain:
  tick_interval: 0.2  # 200ms between ticks
  health_check_interval: 100  # ticks between checks
  
  skills:
    directory: "~/.aos/aos/aos_brain_py/skills"
    auto_load: true
    
  ollama:
    enabled: true
    url: "http://localhost:11434"
    timeout: 60
    fallback_enabled: true
    
  growingnn:
    add_node_threshold:
      novelty: 0.8
      error: 0.6
    add_layer_threshold:
      complexity: 0.9
      
  diagnostic:
    enabled: true
    auto_recover: true
    log_level: "info"
```

### 6.2 Agent Configuration (active_skills.json)

```json
{
  "brain-sensory": {
    "active": true,
    "skill": "thalamus-v1",
    "priority": 0.5
  },
  "brain-decision": {
    "active": true,
    "skill": "pfc-v2",
    "ollama_available": true
  },
  "brain-health": {
    "active": true,
    "skill": "brain-health-check-v1"
  }
}
```

---

## 7. Monitoring & Observability

### 7.1 Metrics Exposed

```python
# Available via brain.get_health()
{
  "tick_count": int,
  "avg_latency_ms": float,
  "skills_registered": int,
  "registry_health": {
    "status": "healthy|warning|critical",
    "by_tier": {...}
  },
  "diagnostics": {
    "status": "healthy|warning|critical",
    "metrics": {...}
  }
}
```

### 7.2 Logging

- **Skill calls:** JSON structured logs
- **Contract violations:** ERROR level
- **Recovery events:** WARN level
- **Tick execution:** DEBUG level

---

## 8. Security Considerations

### 8.1 Contract Validation

- Input validation prevents injection attacks
- Output validation prevents data leakage
- Schema enforcement at runtime

### 8.2 Skill Isolation

- Skills run in isolated namespaces
- No direct access to brain state
- All communication via registry

### 8.3 Agent Privileges

- **Standard agents:** sensory, decision, health
- **Privileged agents:** + recovery, config
- **Admin agents:** full registry access

---

## 9. Migration Guide

### 9.1 From Monolithic Brain

```python
# OLD
from seven_region import SevenRegionBrain
brain = SevenRegionBrain()

# NEW
from seven_region_v2 import SevenRegionBrainV2
brain = SevenRegionBrainV2()  # Skills-first, backward compatible
```

### 9.2 Adding New Skills

1. Create skill directory: `skills/{name}-v{version}/`
2. Write SKILL.md with contract
3. Implement handler.py
4. Register in brain startup

### 9.3 Versioning

- Follow SemVer (MAJOR.MINOR.PATCH)
- Major: Breaking contract changes
- Minor: New features, backward compatible
- Patch: Bug fixes

---

## 10. Troubleshooting

### 10.1 Common Issues

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| High latency | Ollama timeout | Check Ollama status, enable fallback |
| Skill not found | Not registered | Verify skill registration in startup |
| Contract violation | Schema mismatch | Check SKILL.md vs handler output |
| Tick stall | Region blocking | Enable auto-recovery |

### 10.2 Debug Mode

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug
brain = SevenRegionBrainV2()
brain.tick({...}, debug=True)
```

---

## 11. References

- Whitepaper: `/docs/AOS_BRAIN_SKILLS_WHITEPAPER.md`
- Architecture: `/docs/BRAIN_SKILLS_ARCHITECTURE.md`
- Examples: `/examples/`
- Tests: `/tests/`

---

**Document Version:** 1.0.0  
**Last Updated:** 2026-03-31  
**Maintainer:** AGI Company Engineering
