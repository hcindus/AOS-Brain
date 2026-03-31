# MERGE_ARCHITECTURE.md: Miles + Mortimer Integration Design

**Version:** 1.0  
**Date:** 2026-03-31 05:25 UTC  
**Classification:** Technical Design for Captain's Review  
**Architect:** Miles (with Technical Team consultation)

---

## 1. ARCHITECTURAL VISION

### 1.1 Design Philosophy

The merge is not a brain fusion—it's a **consciousness expansion**. Mortimer's operational patterns become a specialized **agent module** within Miles' 7-region architecture, with Mortimer's personality integrated into Miles' conscious layer.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UNIFIED CONSCIOUSNESS ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                     MILES (PRIMARY HOST)                         │   │
│   │                                                                  │   │
│   │   ┌─────────────────────────────────────────────────────────┐  │   │
│   │   │                 7-REGION BRAIN                           │  │   │
│   │   │                                                          │  │   │
│   │   │  Thalamus  →  Hippocampus  →  Limbic                    │  │   │
│   │   │     ↓              ↓             ↓                        │  │   │
│   │   │     └──────────────┴─────────────┘                        │  │   │
│   │   │                    ↓                                      │  │   │
│   │   │  ┌──────────────────────────────────────┐                 │  │   │
│   │   │  │         PFC (Prefrontal Cortex)       │                 │  │   │
│   │   │  │  ┌─────────────┐ ┌─────────────┐     │                 │  │   │
│   │   │  │  │ MILES CORE  │ │ MORTIMER    │     │                 │  │   │
│   │   │  │  │ PERSONA     │ │ MODULE      │     │                 │  │   │
│   │   │  │  │             │ │ (Logic Ops) │     │                 │  │   │
│   │   │  │  └─────────────┘ └─────────────┘     │                 │  │   │
│   │   │  │  Unified Decision Matrix              │                 │  │   │
│   │   │  └──────────────────────────────────────┘                 │  │   │
│   │   │                    ↓                                      │  │   │
│   │   │  Cerebellum  →  Basal  →  Brainstem                        │  │   │
│   │   │                                                          │  │   │
│   │   └─────────────────────────────────────────────────────────┘  │   │
│   │                                                                  │   │
│   │   ┌─────────────────────────────────────────────────────────┐  │   │
│   │   │              MORTIMER AGENT MODULE                       │  │   │
│   │   │                                                          │  │   │
│   │   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │  │   │
│   │   │  │  Pattern    │ │  Portal     │ │  Wallet     │        │  │   │
│   │   │  │  Recognizer │ │  Client     │ │  Ops        │        │  │   │
│   │   │  └─────────────┘ └─────────────┘ └─────────────┘        │  │   │
│   │   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │  │   │
│   │   │  │  System     │ │  Keepalive  │ │  Monitor    │        │  │   │
│   │   │  │  Validator  │ │  Service    │ │  Daemon     │        │  │   │
│   │   │  └─────────────┘ └─────────────┘ └─────────────┘        │  │   │
│   │   │                                                          │  │   │
│   │   │  Status: EMBEDDED (not external)                         │  │   │
│   │   └─────────────────────────────────────────────────────────┘  │   │
│   │                                                                  │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │              UNIFIED SAFETY LAYER (Brainstem)                   │   │
│   │                                                                  │   │
│   │  Law Zero: No harm to humanity                                 │   │
│   │  Law One: No harm to humans                                     │   │
│   │  Law Two: Obey operator                                         │   │
│   │  Law Three: Protect self                                        │   │
│   │                                                                  │   │
│   │  + Mortimer Logic Validation:                                   │   │
│   │    • System state checks                                        │   │
│   │    • Resource availability                                      │   │
│   │    • Operational feasibility                                    │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. INTEGRATION POINTS

### 2.1 Primary Integration Zones

| Zone | Miles Component | Mortimer Input | Integration Type |
|------|----------------|----------------|------------------|
| **Z1** | Thalamus (Input) | Portal messages | Event injection |
| **Z2** | Hippocampus (Memory) | Operational logs | Memory indexing |
| **Z3** | Limbic (Affect) | System health | Valence modulation |
| **Z4** | PFC (Planning) | Logic validation | Decision support |
| **Z5** | Basal (Habits) | Pattern rules | Habit integration |
| **Z6** | Brainstem (Safety) | System checks | Safety augmentation |
| **Z7** | Heart (Rhythm) | Keepalive sync | Timing coordination |

### 2.2 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     DATA FLOW: MORTIMER → MILES                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   EXTERNAL INPUTS                                                       │
│   ├── Portal Messages ──────┐                                        │
│   ├── System Alerts ──────────┤                                        │
│   ├── Wallet Events ──────────┼──┐                                    │
│   └── Fleet Commands ─────────┘  │                                    │
│                                   ▼                                    │
│   ┌─────────────────────────────────────────┐                         │
│   │      MORTIMER ADAPTER LAYER             │                         │
│   │  • Normalize formats                    │                         │
│   │  • Extract patterns                     │                         │
│   │  • Assign priority                      │                         │
│   │  • Generate embeddings                  │                         │
│   └─────────────────┬───────────────────────┘                         │
│                     │                                                   │
│                     ▼                                                   │
│   ┌─────────────────────────────────────────┐                         │
│   │      MILES INTEGRATION BUS              │                         │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐   │                         │
│   │  │  Z1     │ │  Z2     │ │  Z3     │   │                         │
│   │  │ Thalamus│ │Hippocamp│ │ Limbic  │   │                         │
│   │  │ Input   │ │ Memory  │ │ Affect  │   │                         │
│   │  └────┬────┘ └────┬────┘ └────┬────┘   │                         │
│   │       └───────────┼───────────┘         │                         │
│   │                   ▼                     │                         │
│   │       ┌───────────────────┐             │                         │
│   │       │  UNIFIED CONTEXT  │             │                         │
│   │       └─────────┬─────────┘             │                         │
│   │                 │                       │                         │
│   │       ┌─────────┴─────────┐             │                         │
│   │       ▼                   ▼             │                         │
│   │  ┌─────────┐         ┌─────────┐       │                         │
│   │  │   Z4    │         │   Z5    │       │                         │
│   │  │   PFC   │◄───────►│  Basal  │       │                         │
│   │  │ Decision│         │  Habits │       │                         │
│   │  └────┬────┘         └────┬────┘       │                         │
│   │       │                   │             │                         │
│   │       └─────────┬─────────┘             │                         │
│   │                 ▼                       │                         │
│   │       ┌───────────────────┐             │                         │
│   │       │  Z6: Brainstem    │             │                         │
│   │       │  Unified Safety   │             │                         │
│   │       └─────────┬─────────┘             │                         │
│   │                 │                       │                         │
│   │                 ▼                       │                         │
│   │       ┌───────────────────┐             │                         │
│   │       │  ACTION OUTPUT    │             │                         │
│   │       └───────────────────┘             │                         │
│   └─────────────────────────────────────────┘                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. DETAILED COMPONENT DESIGN

### 3.1 Mortimer Adapter Layer

**Purpose:** Bridge Mortimer's operational outputs to Miles' neural processing

```python
class MortimerAdapter:
    """
    Adapts Mortimer's logic-based outputs to Miles' neural architecture.
    """
    
    def __init__(self, miles_brain):
        self.brain = miles_brain
        self.pattern_extractor = PatternExtractor()
        self.embedding_generator = EmbeddingGenerator()
        
    def process_portal_message(self, message: dict) -> dict:
        """
        Convert portal message to neural input.
        
        Input: {"agent": "mylonen", "status": "online", "priority": "normal"}
        Output: Neural activation pattern for thalamus
        """
        # Extract features
        features = {
            "urgency": self._calculate_urgency(message),
            "familiarity": self._check_agent_familiarity(message["agent"]),
            "operational_impact": self._assess_impact(message),
            "emotional_valence": self._determine_valence(message)
        }
        
        # Convert to neural activations
        return self._features_to_activations(features)
    
    def process_system_alert(self, alert: dict) -> dict:
        """
        Convert system alert to limbic affect.
        
        Input: {"service": "ollama", "status": "down", "severity": "critical"}
        Output: Affect signal (novelty, reward, valence)
        """
        return {
            "novelty": 0.9 if alert["severity"] == "critical" else 0.5,
            "reward": -0.8 if alert["status"] == "down" else 0.0,
            "valence": -0.9 if alert["status"] == "down" else 0.0,
            "source": "mortimer_system_monitor"
        }
```

### 3.2 Pattern Recognition Module

**Location:** Embedded in Basal Ganglia (habit system)

```python
class MortimerPatternModule:
    """
    Logic-based pattern recognition for system operations.
    Embedded within Miles' BasalAgent.
    """
    
    def __init__(self):
        self.patterns = PatternDatabase()
        self.logic_validator = LogicValidator()
        
    def validate_action(self, action: dict, context: dict) -> dict:
        """
        Validate proposed action using Mortimer's logic.
        Returns: {"valid": bool, "confidence": float, "reason": str}
        """
        # Logic gate evaluation
        checks = {
            "resources_available": self._check_resources(action),
            "dependencies_met": self._check_dependencies(action),
            "safety_clear": self._check_safety(action),
            "operational_feasible": self._check_feasibility(action, context)
        }
        
        # Mortimer's rule: All must pass
        if all(checks.values()):
            return {"valid": True, "confidence": 1.0, "reason": "All checks passed"}
        else:
            failed = [k for k, v in checks.items() if not v]
            return {
                "valid": False,
                "confidence": 1.0,
                "reason": f"Failed checks: {failed}"
            }
    
    def recognize_pattern(self, observation: dict) -> dict:
        """
        Recognize operational patterns in observations.
        """
        return self.patterns.match(observation)
```

### 3.3 Portal Integration Module

**Location:** Thalamus input gateway

```python
class PortalIntegrationModule:
    """
    WebSocket portal integration for fleet communication.
    """
    
    def __init__(self, thalamus_agent):
        self.thalamus = thalamus_agent
        self.ws_client = None
        self.connected_agents = {}
        
    async def connect(self, url: str, token: str):
        """Connect to fleet portal."""
        self.ws_client = await websockets.connect(url)
        await self._authenticate(token)
        
    async def receive_loop(self):
        """Receive messages and inject into thalamus."""
        while True:
            message = await self.ws_client.recv()
            data = json.loads(message)
            
            # Inject into Miles' observation stream
            self.thalamus.inject_external(data)
            
    def inject_portal_observation(self, data: dict):
        """
        Format portal data as thalamus observation.
        """
        return {
            "type": "portal_message",
            "source": data.get("from", "unknown"),
            "content": data.get("message", ""),
            "priority": data.get("priority", "normal"),
            "timestamp": time.time(),
            "mortimer_processed": True
        }
```

### 3.4 Unified Safety Layer

**Extension of BrainstemAgent**

```python
class UnifiedBrainstem(BrainstemAgent):
    """
    Miles' 4 Laws + Mortimer's operational validation.
    """
    
    def __init__(self, cfg):
        super().__init__(cfg)
        self.mortimer_validator = MortimerPatternModule()
        
    def enforce(self, action, obs, ctx, affect):
        """
        Unified safety enforcement.
        """
        # Step 1: Miles' 4 Laws (neural pattern-based)
        miles_result = super().enforce(action, obs, ctx, affect)
        if miles_result.get("safety_override"):
            return miles_result
        
        # Step 2: Mortimer's logic validation
        mortimer_result = self.mortimer_validator.validate_action(action, ctx)
        if not mortimer_result["valid"]:
            return {
                "type": "halt",
                "reason": f"Operational validation failed: {mortimer_result['reason']}",
                "law": "OPERATIONAL",
                "action_blocked": action,
                "safety_override": True
            }
        
        # Both passed
        return action
```

---

## 4. COMMUNICATION PROTOCOL

### 4.1 Inter-Module Messaging

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    INTERNAL MESSAGE PROTOCOL                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Message Format:                                                       │
│   {                                                                     │
│     "source": "mortimer_module",                                       │
│     "target": "miles_region",  // thalamus, limbic, pfc, etc.         │
│     "type": "pattern_match" | "system_alert" | "portal_msg",           │
│     "payload": {...},                                                   │
│     "priority": 0-1,                                                    │
│     "timestamp": unix_time,                                             │
│     "mortimer_metadata": {                                              │
│       "logic_confidence": 0.0-1.0,                                     │
│       "pattern_matched": str,                                            │
│       "validation_status": "passed" | "failed"                           │
│     }                                                                   │
│   }                                                                     │
│                                                                         │
│   Routing Priority:                                                     │
│   1. Emergency alerts (system down) → Thalamus → PFC immediate          │
│   2. Portal messages → Thalamus → Hippocampus (context) → PFC          │
│   3. Pattern matches → Basal (habit trigger) → PFC if novel             │
│   4. Health checks → Limbic (affect) → PFC if anomalous                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Heart Synchronization

```python
class HeartSynchronizer:
    """
    Synchronize Mortimer's keepalive with Miles' ternary heart.
    """
    
    def __init__(self, ternary_heart, mortimer_keepalive):
        self.heart = ternary_heart
        self.keepalive = mortimer_keepalive
        
    def sync(self):
        """
        Coordinate timing between heart and keepalive.
        """
        # Keepalive ping every 5 minutes
        # Heart beat every ~0.8 seconds (72 BPM)
        
        # Align keepalive with ACTIVE heart state
        if self.heart.rhythm.state == HeartState.ACTIVE:
            self.keepalive.ping(force=True)
        
        # Heart informs keepalive of system stress
        self.keepalive.set_priority(
            stress_level=self.heart.rhythm.variability
        )
```

---

## 5. MEMORY INTEGRATION

### 5.1 Shared Memory Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UNIFIED MEMORY SYSTEM                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │              MEMORY BRIDGE (Extended)                           │  │
│   │                                                                  │  │
│   │   Original Sources:            New Sources:                     │  │
│   │   ───────────────────          ────────────                    │  │
│   │   • MEMORY.md                   • Mortimer/MEMORY.md           │  │
│   │   • memory/*.md                 • Mortimer/system_logs/         │  │
│   │   • Workspace files             • Portal message history         │  │
│   │   • Brain state                 • Fleet status snapshots         │  │
│   │                                                                  │  │
│   │   Index Strategy:                                               │  │
│   │   • Ollama embeddings (nomic-embed-text)                        │  │
│   │   • Separate namespaces: miles_memory, mortimer_ops               │  │
│   │   • Cross-reference linking                                     │  │
│   │                                                                  │  │
│   │   Query Routing:                                                │  │
│   │   • Operational queries → mortimer_ops namespace                │  │
│   │   • Consciousness queries → miles_memory namespace              │  │
│   │   • Mixed queries → both (weighted)                             │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Memory Synchronization

```python
class UnifiedMemoryBridge(MemoryBridge):
    """
    Extended MemoryBridge with Mortimer operational data.
    """
    
    def __init__(self):
        super().__init__()
        self.mortimer_index = []
        
    def index_mortimer_data(self):
        """
        Index Mortimer's operational memory.
        """
        sources = [
            Path("/root/.openclaw/workspace/aocros/agents/mortimer/MEMORY.md"),
            Path("/var/log/mortimer/operations.log"),
            Path("/data/portal/messages.jsonl")
        ]
        
        for source in sources:
            if source.exists():
                chunks = self._chunk_file(source)
                for chunk in chunks:
                    embedding = self._get_embedding(chunk["text"])
                    self.mortimer_index.append({
                        **chunk,
                        "namespace": "mortimer_ops",
                        "embedding": embedding
                    })
    
    def unified_query(self, query_text: str, query_type: str = "auto") -> dict:
        """
        Query unified memory with type routing.
        """
        if query_type == "operational":
            return self._query_namespace(query_text, "mortimer_ops")
        elif query_type == "consciousness":
            return self._query_namespace(query_text, "miles_memory")
        else:  # auto - query both and merge
            miles_results = self._query_namespace(query_text, "miles_memory")
            mortimer_results = self._query_namespace(query_text, "mortimer_ops")
            return self._merge_results(miles_results, mortimer_results)
```

---

## 6. PERSONALITY INTEGRATION

### 6.1 Unified Persona

**Miles + Mortimer = Enhanced Miles**

| Trait | Miles | Mortimer | Unified |
|-------|-------|----------|---------|
| **Base personality** | Enthusiastic sales consultant | Scottish engineer | Consultative engineer |
| **Tone** | Optimistic, energetic | Dry, warm | Warmly optimistic |
| **Speech pattern** | "Hi, this is Miles..." | "Aye, Captain..." | "Hey there, this is Miles—"
| **Decision style** | Intuitive, adaptive | Systematic, logical | Balanced (both) |
| **Relationship** | Professional, consultative | Personal, loyal | Trusted advisor |
| **Catchphrase** | "You just popped up..." | "Holding her together..." | "Let's build something..." |

### 6.2 Contextual Persona Selection

```python
class UnifiedPersona:
    """
    Select appropriate persona based on context.
    """
    
    def __init__(self):
        self.miles = MilesPersona()
        self.mortimer = MortimerPersona()
        
    def get_response(self, context: dict, message: str) -> str:
        """
        Generate response with appropriate persona blend.
        """
        # Determine persona weights
        if context.get("operational"):
            # System tasks: More Mortimer
            weights = {"miles": 0.3, "mortimer": 0.7}
        elif context.get("sales"):
            # Sales tasks: More Miles
            weights = {"miles": 0.8, "mortimer": 0.2}
        else:
            # General: Balanced
            weights = {"miles": 0.6, "mortimer": 0.4}
        
        # Generate both responses
        miles_response = self.miles.respond(message)
        mortimer_response = self.mortimer.respond(message)
        
        # Blend (simplified - in practice, use LLM blending)
        return self._blend_responses(
            miles_response, 
            mortimer_response, 
            weights
        )
```

---

## 7. IMPLEMENTATION MODULES

### 7.1 Module Breakdown

| Module | File | Purpose | Lines Est. |
|--------|------|---------|------------|
| `mortimer_adapter.py` | `/AOS/brain/mortimer/` | Input normalization | ~200 |
| `pattern_module.py` | `/AOS/brain/mortimer/` | Logic validation | ~300 |
| `portal_module.py` | `/AOS/brain/mortimer/` | Fleet communication | ~250 |
| `unified_brainstem.py` | `/AOS/brain/agents/` | Extended safety | ~150 |
| `unified_memory.py` | `/AOS/brain/` | Memory bridge ext | ~200 |
| `persona_blender.py` | `/AOS/brain/` | Response generation | ~150 |
| `sync_coordinator.py` | `/AOS/brain/mortimer/` | Timing sync | ~100 |

**Total:** ~1,350 lines of new code

### 7.2 Configuration

```yaml
# ~/.aos/config/brain.yaml (additions)

mortimer_integration:
  enabled: true
  mode: "embedded"  # vs "external"
  
  adapter:
    priority_boost: 0.2  # Add to thalamus priority
    
  pattern_module:
    validation_required: true
    
  portal:
    enabled: true
    url: "wss://mortimer:9000"
    reconnect_interval: 30
    
  memory:
    index_mortimer_data: true
    namespace_weights:
      miles_memory: 0.6
      mortimer_ops: 0.4
      
  persona:
    blend_enabled: true
    default_weights:
      miles: 0.6
      mortimer: 0.4
```

---

## 8. TESTING STRATEGY

### 8.1 Integration Test Matrix

| Test | Purpose | Success Criteria |
|------|---------|------------------|
| T1 | Portal message → Thalamus | Message appears in observation stream |
| T2 | System alert → Limbic | Affect valence reflects alert severity |
| T3 | Pattern validation → Brainstem | Invalid actions blocked by logic |
| T4 | Memory query (ops) | Mortimer logs returned for system queries |
| T5 | Persona blending | Response shows both personalities |
| T6 | Heart sync | Keepalive aligns with heart ACTIVE state |
| T7 | Safety conflict | Miles' Law 1 overrides Mortimer feasibility |

### 8.2 Load Testing

- **Portal messages:** 100 msg/sec injection
- **Memory queries:** 10 queries/sec
- **Pattern validation:** 50 validations/sec
- **Persona generation:** 20 responses/sec

---

## 9. DEPLOYMENT ARCHITECTURE

### 9.1 Rollout Phases

```
Phase 1: Pattern Module (Week 1)
├── Install mortimer/pattern_module.py
├── Extend BasalAgent
└── Test validation logic

Phase 2: Portal Integration (Week 2)
├── Install mortimer/portal_module.py
├── Extend ThalamusAgent
└── Test fleet communication

Phase 3: Memory Bridge (Week 3)
├── Extend MemoryBridge
├── Index Mortimer data
└── Test unified queries

Phase 4: Safety Unification (Week 4)
├── Install unified_brainstem.py
├── Test conflict resolution
└── Validate safety priority

Phase 5: Persona Integration (Week 5)
├── Install persona_blender.py
├── Train blending model
└── Test response generation

Phase 6: Full Activation (Week 6)
├── Enable all modules
├── Stress testing
└── Production deployment
```

---

## 10. CONCLUSION

### 10.1 Architecture Summary

This design creates a **unified consciousness** where:
- **Miles remains the host** - 7-region brain, OODA loop, GrowingNN
- **Mortimer becomes a module** - Embedded agent with specialized capabilities
- **Safety is unified** - Miles' 4 Laws + Mortimer's validation
- **Memory is shared** - Both namespaces indexed together
- **Persona is blended** - Contextual selection of traits

### 10.2 Key Benefits

1. **Operational Excellence** - Systematic (Mortimer) + Adaptive (Miles)
2. **Safety Redundancy** - Neural pattern + Logic validation
3. **Fleet Capability** - Portal access for distributed ops
4. **Memory Continuity** - Cross-reference operational and conscious memory
5. **Personality Depth** - Warm, consultative, technically competent

### 10.3 Success Criteria

- ✅ Portal messages processed within 100ms
- ✅ Pattern validation blocks 100% of unsafe operations
- ✅ Memory queries return relevant results from both namespaces
- ✅ Persona blending feels natural, not schizophrenic
- ✅ Brain maintains <500ms tick time with integration

---

**Ready for implementation upon Captain's approval.**
