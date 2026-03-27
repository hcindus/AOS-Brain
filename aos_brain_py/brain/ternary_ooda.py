# brain/ternary_ooda.py
"""
Ternary OODA Brain - 3-tier memory architecture.

Replaces the fragile Ollama-based brain with:
- Short-term memory (working context)
- Mid-term memory (episodic/semantic)  
- Long-term memory (consolidated patterns)
- Cortical sheet for ternary wave computation
- Graph substrate for semantic growth
"""

import time
import json
import threading
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

# Lazy imports - only load when needed to avoid startup hangs
def get_numpy():
    import numpy as np
    return np

def get_cortical_sheet():
    from core.cortical_sheet import CorticalSheet
    return CorticalSheet

from substrate.graph_store import GraphStore, Node

# Import only what we need immediately
from brain.cortex import QMDAwareCortex


@dataclass
class MemoryTrace:
    """
    A trace of experience in the memory substrate.
    Lives in short-term, may consolidate to mid/long-term.
    """
    content: Any
    embedding: Optional[List[float]] = None
    ternary_signature: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    importance: float = 0.5
    timestamp: float = field(default_factory=time.time)
    access_count: int = 0
    
    def touch(self):
        """Access this memory (updates importance)."""
        self.access_count += 1
        self.importance = min(1.0, self.importance + 0.1)


@dataclass
class Observation:
    """Raw input processed by the brain."""
    source: str  # "user", "system", "sensor", "internal"
    content: Any
    timestamp: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)


@dataclass
class Decision:
    """Output of the orient/decide phase."""
    intent: str  # "respond", "act", "wait", "learn", "noop"
    action: Optional[Any] = None
    target: Optional[str] = None
    confidence: float = 0.5
    reasoning: str = ""


@dataclass
class Thought:
    """
    Complete cognitive unit.
    Contains: observation, decision, value, gates, language
    """
    observation: Observation
    decision: Decision
    value: Dict  # {importance, valence, urgency}
    gates: Dict  # {motor, emotional, language, action}
    mode: str  # QMD mode
    language: str = ""  # Natural language expression
    plan: Any = None  # Structured action plan
    
    # Ternary code: [novelty, value, action, risk, growth]
    ternary_code: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    
    # Reference to memory traces used
    memories_used: List[str] = field(default_factory=list)


class TernaryOodaBrain:
    """
    Ternary OODA Brain with 3-tier memory.
    
    Architecture:
    - Short-term: Working memory (last N inputs)
    - Mid-term: Episodic buffer (consolidated experiences)
    - Long-term: Semantic substrate (patterns in graph)
    
    Each tick:
    1. Observe: Receive input, encode to cortical sheet
    2. Orient: Query memory, compute context
    3. Decide: Apply ternary logic to select action
    4. Act: Execute decision, update memories
    5. Grow: Consolidate important traces to substrate
    """
    
    # QMD mode thresholds (from OODA-7 spec)
    QMD_THRESHOLDS = {
        "novelty": 0.6,
        "value": 0.4,
        "action": 0.5,
        "risk": 0.6,
        "growth": 0.3,
    }
    
    def __init__(self, 
                 model_path: Optional[str] = None,
                 use_qwen: bool = False,
                 short_term_limit: int = 10,
                 mid_term_limit: int = 100):
        """
        Initialize ternary brain.
        
        Args:
            model_path: Path to TinyLlama/Qwen GGUF
            use_qwen: Use Qwen instead of TinyLlama
            short_term_limit: Max working memory traces
            mid_term_limit: Max episodic buffer size
        """
        # Core components
        self.cortical = CorticalSheet()
        self.lexicon = TracrayLexicon()
        self.substrate = GraphStore()
        self.cortex = QMDAwareCortex(model_path=model_path, use_qwen=use_qwen)
        
        # 3-tier memory
        self.short_term: List[MemoryTrace] = []  # Working memory
        self.mid_term: List[MemoryTrace] = []   # Episodic buffer
        self.long_term = self.substrate          # Semantic graph
        
        # Limits
        self.short_term_limit = short_term_limit
        self.mid_term_limit = mid_term_limit
        
        # State
        self.tick_count = 0
        self.current_mode = "Analytical"
        self.last_thought: Optional[Thought] = None
        self.running = False
        
        # Thread safety
        self._lock = threading.Lock()
    
    def tick(self, observation: Observation) -> Thought:
        """
        Execute one OODA cognition cycle.
        
        Returns:
            Thought: Complete cognitive unit with decision
        """
        with self._lock:
            self.tick_count += 1
            
            # 1. OBSERVE: Encode input to cortical sheet
            sensory_pattern = self._observe(observation)
            
            # 2. ORIENT: Query memory, build context
            context = self._orient(sensory_pattern, observation)
            
            # 3. DECIDE: Apply ternary logic
            decision = self._decide(context, sensory_pattern)
            
            # 4. ACT: Generate output
            language = self._act(decision, context)
            
            # 5. GROW: Consolidate to substrate
            self._grow(observation, decision, context)
            
            # Assemble thought
            thought = Thought(
                observation=observation,
                decision=decision,
                value=context.get("value", {}),
                gates=context.get("gates", {}),
                mode=self.current_mode,
                language=language,
                plan=decision.action,
                ternary_code=context.get("ternary", [0, 0, 0, 0, 0]),
                memories_used=context.get("memories", [])
            )
            
            self.last_thought = thought
            return thought
    
    def _observe(self, observation: Observation) -> np.ndarray:
        """Encode observation to cortical pattern."""
        import numpy as np
        
        # Convert content to ternary representation
        content_str = str(observation.content)
        
        # Create initial activation pattern
        pattern = np.zeros((8, 8, 8))
        
        # Hash content to spatial coordinates
        h = hash(content_str) % (8**3)
        z, y, x = h // 64, (h // 8) % 8, h % 8
        
        # Set initial excitation
        pattern[z, y, x] = 1.0
        
        # Propagate waves through cortical sheet
        evolved = self.cortical.evolve(pattern, steps=3)
        
        return evolved
    
    def _orient(self, sensory_pattern: np.ndarray, 
                observation: Observation) -> Dict:
        """
        Orient: Query memory layers, build context.
        
        Returns context dict with:
        - relevant_memories
        - computed ternary signals
        - value assessment
        - gating decisions
        """
        context = {
            "sensory": sensory_pattern,
            "memories": [],
            "ternary": [0, 0, 0, 0, 0],
            "value": {"importance": 0.5, "valence": 0.0, "urgency": 0.5},
            "gates": {"motor": 0, "emotional": 0, "language": 1, "action": 0},
        }
        
        # Query short-term (working memory)
        recent = self.short_term[-5:] if self.short_term else []
        
        # Query mid-term (episodic)
        relevant_episodic = self._query_mid_term(observation)
        
        # Query long-term (semantic graph)
        # (simplified - would use embedding similarity)
        
        # Compute ternary signals based on query results
        # Novelty: is this new?
        is_novel = len(relevant_episodic) == 0
        context["ternary"][0] = 1 if is_novel else 0
        
        # Value: importance of content
        content_val = self._assess_value(observation)
        context["ternary"][1] = 1 if content_val > 0.5 else 0
        context["value"]["importance"] = content_val
        
        # Action: should we respond?
        needs_action = observation.source == "user" or is_novel
        context["ternary"][2] = 1 if needs_action else 0
        context["gates"]["action"] = 1 if needs_action else 0
        
        # Risk: any danger?
        risk = self._assess_risk(observation)
        context["ternary"][3] = -1 if risk > 0.7 else 0
        
        # Growth: should we learn from this?
        growth = is_novel and content_val > 0.3
        context["ternary"][4] = 1 if growth else 0
        
        # Determine QMD mode
        self.current_mode = self._determine_mode(context["ternary"])
        
        return context
    
    def _decide(self, context: Dict, sensory_pattern: np.ndarray) -> Decision:
        """
        Decide: Apply ternary logic to select action.
        """
        ternary = context["ternary"]
        
        # Decision logic based on ternary signals
        if ternary[3] == -1:  # Risk signal
            intent = "cautious"
            action = "wait"
            confidence = 0.3
        elif ternary[2] == 1:  # Action signal
            if ternary[0] == 1:  # Novelty
                intent = "explore"
                action = {"type": "query", "target": "substrate"}
            else:
                intent = "respond"
                action = {"type": "generate", "mode": self.current_mode}
            confidence = 0.7
        elif ternary[1] == 1:  # Value but no action
            intent = "learn"
            action = {"type": "consolidate"}
            confidence = 0.5
        else:
            intent = "noop"
            action = None
            confidence = 0.9
        
        # Build reasoning
        reasons = []
        if ternary[0] == 1:
            reasons.append("novel")
        if ternary[1] == 1:
            reasons.append("valuable")
        if ternary[2] == 1:
            reasons.append("actionable")
        if ternary[3] == -1:
            reasons.append("risky")
        
        return Decision(
            intent=intent,
            action=action,
            confidence=confidence,
            reasoning=", ".join(reasons) if reasons else "stable"
        )
    
    def _act(self, decision: Decision, context: Dict) -> str:
        """
        Act: Generate output based on decision.
        """
        if decision.intent == "noop":
            return "..."
        
        if decision.intent == "respond":
            # Generate language via cortex
            return self.cortex.to_language(
                decision.action, 
                mode=self.current_mode
            )
        
        if decision.intent == "explore":
            return f"[exploring in {self.current_mode} mode]"
        
        if decision.intent == "learn":
            return "[consolidating memory]"
        
        return f"[{decision.intent}]"
    
    def _grow(self, observation: Observation, 
              decision: Decision, context: Dict):
        """
        Grow: Consolidate important traces to memory layers.
        """
        # Create memory trace
        trace = MemoryTrace(
            content=observation.content,
            ternary_signature=context["ternary"],
            importance=context["value"]["importance"]
        )
        
        # Add to short-term
        self.short_term.append(trace)
        if len(self.short_term) > self.short_term_limit:
            # Move oldest to mid-term
            old = self.short_term.pop(0)
            if old.importance > 0.3:
                self.mid_term.append(old)
        
        # Consolidate mid-term to long-term if needed
        if len(self.mid_term) > self.mid_term_limit:
            self._consolidate_mid_term()
        
        # Add thought to substrate graph
        thought_dict = {
            "language": context.get("language", ""),
            "ternary_code": context["ternary"],
            "value": context["value"],
            "memories_used": context["memories"],
        }
        self.substrate.add_thought(thought_dict)
        self.substrate.grow(thought_dict)
    
    def _query_mid_term(self, observation: Observation) -> List[MemoryTrace]:
        """Query episodic memory for relevant traces."""
        # Simple string match for now
        content = str(observation.content).lower()
        relevant = []
        
        for trace in self.mid_term:
            if content in str(trace.content).lower():
                trace.touch()
                relevant.append(trace)
        
        return relevant
    
    def _assess_value(self, observation: Observation) -> float:
        """Assess value of observation (0-1)."""
        # Simple heuristics
        content = str(observation.content)
        
        value = 0.5
        
        # User input is valuable
        if observation.source == "user":
            value += 0.2
        
        # Longer content = more valuable
        if len(content) > 50:
            value += 0.1
        
        # Questions are valuable
        if "?" in content:
            value += 0.1
        
        return min(1.0, value)
    
    def _assess_risk(self, observation: Observation) -> float:
        """Assess risk of observation (0-1)."""
        # Simple keyword check
        content = str(observation.content).lower()
        
        risky = ["error", "fail", "crash", "kill", "rm -rf", "delete"]
        for r in risky:
            if r in content:
                return 0.8
        
        return 0.0
    
    def _determine_mode(self, ternary: List[int]) -> str:
        """Determine QMD mode from ternary signals."""
        # Map ternary to mode
        if ternary[3] == -1:
            return "Cautious"
        if ternary[0] == 1 and ternary[1] == 1:
            return "Exploratory"
        if ternary[0] == 1 and ternary[2] == 1:
            return "Creative"
        if ternary[1] == 1 and ternary[4] == 1:
            return "Reflective"
        if ternary[2] == 1 and ternary[0] == 0:
            return "Directive"
        if ternary[1] == 1 and ternary[2] == 0:
            return "Emotional"
        return "Analytical"
    
    def _consolidate_mid_term(self):
        """Move important traces from mid to long-term."""
        # Sort by importance
        self.mid_term.sort(key=lambda t: t.importance, reverse=True)
        
        # Keep top 80%, move rest to long-term
        keep_count = int(self.mid_term_limit * 0.8)
        to_move = self.mid_term[keep_count:]
        self.mid_term = self.mid_term[:keep_count]
        
        # Add to substrate (long-term)
        for trace in to_move:
            thought = {
                "language": str(trace.content),
                "embedding": trace.embedding or [],
                "ternary_code": trace.ternary_signature,
                "value": {"importance": trace.importance},
                "memories_used": [],
            }
            self.substrate.add_thought(thought)
    
    def get_status(self) -> Dict:
        """Get current brain status."""
        return {
            "tick_count": self.tick_count,
            "mode": self.current_mode,
            "memory": {
                "short_term": len(self.short_term),
                "mid_term": len(self.mid_term),
                "long_term": self.substrate.get_stats(),
            },
            "cortical": self.cortical.get_wave_stats(),
        }


# Stub for numpy if not available
class FakeNumpy:
    """Stub numpy for environments without it."""
    ndarray = list
    
    @staticmethod
    def zeros(shape):
        if isinstance(shape, tuple):
            return [[[0 for _ in range(shape[2])] 
                     for _ in range(shape[1])] 
                    for _ in range(shape[0])]
        return [0] * shape
    
    @staticmethod
    def array(data):
        return data

# Try to import numpy, use stub if not available
try:
    import numpy as np
except ImportError:
    np = FakeNumpy()
