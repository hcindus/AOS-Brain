#!/usr/bin/env python3
"""
QMD - Query-Memory-Decision Loop
Ported from legacy brain with Ollama integration
"""

import time
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import deque
import requests


@dataclass
class QMDState:
    """QMD cycle state"""
    query: str
    memories: List[Dict]
    decision: str
    confidence: float
    timestamp: float


class QMDLoop:
    """
    Query-Memory-Decision Loop
    
    The core cognitive loop:
    1. Query: Formulate question based on current context
    2. Memory: Retrieve relevant memories
    3. Decision: Use Ollama to make informed decision
    
    Ported from legacy SimpleTernaryBrain
    """
    
    def __init__(self, model: str = "antoniohudnall/Mortimer:latest", use_ollama: bool = False):
        self.model = model
        self.use_ollama = use_ollama
        self.history: deque = deque(maxlen=100)
        self.stats = {
            "total_cycles": 0,
            "avg_latency": 0.0,
            "cache_hits": 0,
            "local_decisions": 0
        }
        
        # Decision cache
        self.decision_cache: Dict[str, QMDState] = {}
        
        # Local decision rules (when Ollama disabled)
        self.decision_rules = {
            "high_novelty": {"action": "explore", "confidence": 0.8, "reason": "high novelty detected"},
            "low_novelty_high_reward": {"action": "exploit", "confidence": 0.9, "reason": "stable system, maximize reward"},
            "low_reward": {"action": "explore", "confidence": 0.7, "reason": "seeking better outcomes"},
            "rest_phase": {"action": "rest", "confidence": 0.6, "reason": "consolidation needed"},
            "default": {"action": "continue", "confidence": 0.5, "reason": "maintain current trajectory"}
        }
        
        mode = "Ollama" if use_ollama else "LOCAL"
        print(f"[QMD] Initialized in {mode} mode")
    
    def cycle(self, context: Dict, memory_bridge=None) -> Dict:
        """Execute one QMD cycle (Ollama or local)"""
        start_time = time.time()
        
        # 1. QUERY: Formulate question
        query = self._formulate_query(context)
        
        # Check cache
        cache_key = hash(f"{context.get('phase', '')}:{context.get('observation', '')}")
        if cache_key in self.decision_cache:
            cached = self.decision_cache[cache_key]
            if time.time() - cached.timestamp < 60:  # 60 second cache
                self.stats["cache_hits"] += 1
                return {
                    "action": cached.decision,
                    "confidence": cached.confidence,
                    "reasoning": "cached",
                    "latency": 0.0
                }
        
        # 2. MEMORY: Retrieve relevant memories
        memories = []
        if memory_bridge:
            try:
                memories = memory_bridge.query(query, n=3)
            except Exception as e:
                pass  # Silent fail
        
        # 3. DECISION: Ollama or local rules
        if self.use_ollama:
            decision, confidence = self._query_ollama(query, context, memories)
            reasoning = "ollama"
        else:
            decision, confidence = self._local_decision(context)
            reasoning = "local_rules"
            self.stats["local_decisions"] += 1
        
        # Record cycle
        cycle = QMDState(
            query=query,
            memories=memories,
            decision=decision,
            confidence=confidence,
            timestamp=time.time()
        )
        self.history.append(cycle)
        
        # Update stats
        latency = time.time() - start_time
        self.stats["total_cycles"] += 1
        self.stats["avg_latency"] = (self.stats["avg_latency"] * 0.9 + latency * 0.1)
        
        # Cache decision
        self.decision_cache[cache_key] = cycle
        
        return {
            "action": decision,
            "confidence": confidence,
            "query": query,
            "memories_used": len(memories),
            "latency": latency,
            "reasoning": reasoning
        }
    
    def _formulate_query(self, context: Dict) -> str:
        """Formulate query from context"""
        phase = context.get("phase", "unknown")
        observation = context.get("observation", "")
        limbic = context.get("limbic", {})
        
        # Context-aware query
        if limbic.get("novelty", 0.5) > 0.7:
            query = f"High novelty detected in {phase}. Best action for {observation[:50]}?"
        elif limbic.get("reward", 0.3) < 0.3:
            query = f"Low reward in {phase}. Recovery strategy for {observation[:50]}?"
        else:
            query = f"Current phase {phase}: optimal action for {observation[:50]}?"
        
        return query
    
    def _local_decision(self, context: Dict) -> tuple:
        """Make decision using local rules (no Ollama)"""
        limbic = context.get("limbic", {})
        novelty = limbic.get("novelty", 0.5)
        reward = limbic.get("reward", 0.3)
        phase = context.get("phase", "unknown")
        
        # Apply decision rules
        if novelty > 0.7:
            rule = self.decision_rules["high_novelty"]
        elif reward < 0.3:
            rule = self.decision_rules["low_reward"]
        elif reward > 0.7 and novelty < 0.3:
            rule = self.decision_rules["low_novelty_high_reward"]
        elif phase == "Act" and reward > 0.6:
            rule = self.decision_rules["rest_phase"]
        else:
            rule = self.decision_rules["default"]
        
        return rule["action"], rule["confidence"]
    
    def _query_ollama(self, query: str, context: Dict, memories: List[Dict]) -> tuple:
        """Query Ollama for decision"""
        try:
            # Build prompt
            prompt = self._build_prompt(query, context, memories)
            
            # Call Ollama
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 50
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json().get("response", "").strip().lower()
                
                # Parse action from response
                if "explore" in result:
                    return "explore", 0.8
                elif "exploit" in result:
                    return "exploit", 0.7
                elif "rest" in result:
                    return "rest", 0.6
                else:
                    return "continue", 0.5
            else:
                return "continue", 0.3
                
        except requests.exceptions.Timeout:
            print("[QMD] Ollama timeout, using fallback")
            return "continue", 0.5
        except Exception as e:
            print(f"[QMD] Error: {e}")
            return "continue", 0.5
    
    def _build_prompt(self, query: str, context: Dict, memories: List[Dict]) -> str:
        """Build prompt for Ollama"""
        prompt = f"""You are an autonomous AI brain. Given the current state, what action should you take?

Current Context:
- Phase: {context.get('phase', 'unknown')}
- Novelty: {context.get('limbic', {}).get('novelty', 0.5):.2f}
- Reward: {context.get('limbic', {}).get('reward', 0.3):.2f}
- Observation: {context.get('observation', 'none')[:100]}

Query: {query}
"""
        
        if memories:
            prompt += "\nRelevant Memories:\n"
            for i, mem in enumerate(memories[:3]):
                prompt += f"- {mem.get('content', 'memory')[:80]}...\n"
        
        prompt += "\nDecide: explore, exploit, rest, or continue. Brief reason:"
        
        return prompt
    
    def get_stats(self) -> Dict:
        """Get QMD statistics"""
        return {
            "total_cycles": self.stats["total_cycles"],
            "avg_latency_ms": self.stats["avg_latency"] * 1000,
            "cache_hits": self.stats["cache_hits"],
            "cache_size": len(self.decision_cache)
        }
    
    def get_recent_decisions(self, n: int = 5) -> List[Dict]:
        """Get recent decisions"""
        recent = list(self.history)[-n:]
        return [{
            "decision": d.decision,
            "confidence": d.confidence,
            "query": d.query[:50]
        } for d in recent]


if __name__ == "__main__":
    print("=" * 70)
    print("  QMD LOOP TEST")
    print("=" * 70)
    
    qmd = QMDLoop()
    
    # Simulate cycles
    print("\nSimulating QMD cycles...")
    test_contexts = [
        {"phase": "Observe", "observation": "High novelty detected", "limbic": {"novelty": 0.9, "reward": 0.5}},
        {"phase": "Decide", "observation": "Multiple options available", "limbic": {"novelty": 0.5, "reward": 0.3}},
        {"phase": "Act", "observation": "Action completed successfully", "limbic": {"novelty": 0.2, "reward": 0.8}},
    ]
    
    for ctx in test_contexts:
        print(f"\nContext: {ctx['phase']}")
        result = qmd.cycle(ctx)
        print(f"  Query: {result.get('query', 'N/A')[:50]}...")
        print(f"  Decision: {result['action']} (confidence: {result['confidence']:.2f})")
        print(f"  Latency: {result['latency']*1000:.1f}ms")
        time.sleep(0.5)  # Rate limit
    
    # Stats
    print("\nQMD Statistics:")
    stats = qmd.get_stats()
    print(f"  Total cycles: {stats['total_cycles']}")
    print(f"  Avg latency: {stats['avg_latency_ms']:.1f}ms")
    print(f"  Cache hits: {stats['cache_hits']}")
    
    print("\n" + "=" * 70)
