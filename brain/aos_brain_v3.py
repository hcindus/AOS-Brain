#!/usr/bin/env python3
"""
AOS Brain v3.0 - Full 7-Region Architecture
Ollama-Free, Non-Blocking, High-Integrity

Uses EmbeddingOrchestrator for all embeddings.
Local reasoning/decision making.
Never blocks on external services.
"""

import time
import json
import hashlib
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import deque

# Import embedding orchestrator
from embedding_orchestrator import get_orchestrator, EmbeddingConfig


@dataclass
class BrainState:
    """Complete brain state"""
    tick: int = 0
    timestamp: float = 0.0
    phase: str = "Observe"
    mode: str = "Full-7-Region"
    novelty: float = 0.8
    reward: float = 0.3
    memory_clusters: int = 0
    policy_nodes: List[int] = None
    
    def __post_init__(self):
        if self.policy_nodes is None:
            self.policy_nodes = [8, 12, 40]


class LocalPFC:
    """
    Prefrontal Cortex - Local Reasoning
    No Ollama dependency - uses rule-based + learned heuristics
    """
    
    def __init__(self):
        self.decision_history = []
        self.rules = {
            "high_novelty": {"action": "explore", "weight": 0.8},
            "medium_novelty": {"action": "exploit", "weight": 0.6},
            "low_novelty": {"action": "rest", "weight": 0.4},
        }
        self.learned_patterns = {}
        
    def decide(self, observation: Dict, context: Dict, affect: Dict) -> Dict:
        """Make decision based on local reasoning"""
        novelty = affect.get("novelty", 0.5)
        reward = affect.get("reward", 0.3)
        
        # Rule-based selection
        if novelty > 0.7:
            rule = self.rules["high_novelty"]
        elif novelty > 0.4:
            rule = self.rules["medium_novelty"]
        else:
            rule = self.rules["low_novelty"]
        
        # Learn from history
        pattern_key = f"{observation.get('type', 'unknown')}_{rule['action']}"
        if pattern_key in self.learned_patterns:
            success_rate = self.learned_patterns[pattern_key].get("success", 0.5)
            if success_rate > 0.6:
                confidence = min(rule["weight"] + 0.2, 1.0)
            else:
                confidence = max(rule["weight"] - 0.1, 0.1)
        else:
            confidence = rule["weight"]
        
        decision = {
            "action": rule["action"],
            "confidence": confidence,
            "reason": f"novelty={novelty:.2f}, local_rule={rule['action']}",
            "timestamp": time.time()
        }
        
        self.decision_history.append(decision)
        return decision
    
    def learn_from_outcome(self, decision: Dict, outcome: Dict):
        """Learn from action outcomes"""
        pattern_key = f"{decision.get('reason', 'unknown')}_{decision['action']}"
        if pattern_key not in self.learned_patterns:
            self.learned_patterns[pattern_key] = {"success": 0.5, "count": 0}
        
        entry = self.learned_patterns[pattern_key]
        success = outcome.get("success", False)
        
        # Exponential moving average
        alpha = 0.1
        entry["success"] = (1 - alpha) * entry["success"] + alpha * (1.0 if success else 0.0)
        entry["count"] += 1


class LocalHippocampus:
    """
    Hippocampus - Local Memory Formation
    Uses EmbeddingOrchestrator (non-blocking)
    """
    
    def __init__(self):
        self.episodic_buffer = deque(maxlen=100)  # Short-term
        self.semantic_memory = []  # Long-term
        self.embedder = get_orchestrator(EmbeddingConfig())
        self.total_traces = 0
        
    def store(self, observation: Dict, plan: Dict, action: Dict) -> Dict:
        """Store memory trace with local embedding"""
        trace = {
            "timestamp": time.time(),
            "observation": observation,
            "plan": plan,
            "action": action,
            "id": hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
        }
        
        # Get embedding (never blocks)
        trace_text = json.dumps(trace)
        embedding, source = self.embedder.get_sync(trace_text)
        
        # Calculate novelty
        novelty = self._calculate_novelty(embedding)
        
        # Store in episodic buffer
        self.episodic_buffer.append({
            "trace": trace,
            "embedding": embedding,
            "novelty": novelty,
            "embedding_source": source
        })
        
        # Distill to semantic memory if buffer full
        if len(self.episodic_buffer) >= 20:
            self._distill_memories()
        
        self.total_traces += 1
        
        return {"novelty": novelty, "traces": self.total_traces}
    
    def _calculate_novelty(self, embedding: List[float]) -> float:
        """Calculate novelty by comparing to existing memories"""
        if not self.episodic_buffer:
            return 0.8  # First memory
        
        # Simple: compare to most recent
        import numpy as np
        recent = self.episodic_buffer[-1]["embedding"]
        
        a_vec = np.array(embedding)
        b_vec = np.array(recent)
        
        norm_a = np.linalg.norm(a_vec)
        norm_b = np.linalg.norm(b_vec)
        
        if norm_a == 0 or norm_b == 0:
            return 0.5
        
        similarity = float(np.dot(a_vec, b_vec) / (norm_a * norm_b))
        novelty = 1.0 - similarity  # Higher novelty = less similar
        
        return max(0.0, min(1.0, novelty + 0.1))  # Boost slightly
    
    def _distill_memories(self):
        """Compress episodic buffer to semantic memory"""
        if len(self.episodic_buffer) < 20:
            return
        
        # Extract key patterns
        batch = list(self.episodic_buffer)[-20:]
        
        # Create summary (rule-based, no Ollama)
        common_actions = {}
        for item in batch:
            action = item["trace"]["action"].get("type", "unknown")
            common_actions[action] = common_actions.get(action, 0) + 1
        
        summary = {
            "timestamp": time.time(),
            "period": "last_20_traces",
            "dominant_action": max(common_actions.items(), key=lambda x: x[1])[0] if common_actions else "unknown",
            "action_distribution": common_actions,
            "average_novelty": sum(item["novelty"] for item in batch) / len(batch)
        }
        
        self.semantic_memory.append(summary)
        
        # Clear buffer
        self.episodic_buffer.clear()
    
    def retrieve(self, query: str, n: int = 3) -> List[Dict]:
        """Retrieve relevant memories"""
        if not self.episodic_buffer and not self.semantic_memory:
            return []
        
        # Get query embedding
        query_emb, _ = self.embedder.get_sync(query)
        
        # Search episodic buffer
        import numpy as np
        scored = []
        
        for item in self.episodic_buffer:
            emb = item["embedding"]
            a_vec = np.array(query_emb)
            b_vec = np.array(emb)
            
            norm_a = np.linalg.norm(a_vec)
            norm_b = np.linalg.norm(b_vec)
            
            if norm_a > 0 and norm_b > 0:
                sim = float(np.dot(a_vec, b_vec) / (norm_a * norm_b))
                scored.append((sim, item["trace"]))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        
        return [trace for sim, trace in scored[:n]]
    
    def get_stats(self) -> Dict:
        """Get hippocampus statistics"""
        return {
            "episodic_count": len(self.episodic_buffer),
            "semantic_count": len(self.semantic_memory),
            "total_traces": self.total_traces,
            "embedder_stats": self.embedder.get_stats()
        }


class AOSBrainv3:
    """
    AOS Brain v3.0 - Full 7-Region Architecture
    Non-blocking, Ollama-free, High-Integrity
    """
    
    def __init__(self, state_path: Optional[Path] = None):
        self.state_path = state_path or Path.home() / ".aos" / "brain" / "state" / "aos_v3_state.json"
        
        # Initialize all 7 regions
        self.pfc = LocalPFC()
        self.hippocampus = LocalHippocampus()
        # Other regions (simplified for now)
        self.limbic = {"novelty": 0.8, "reward": 0.3}
        self.basal = {"actions": 0}
        self.cerebellum = {"patterns": {}}
        self.brainstem = {"safety": True}
        self.thalamus = {"routing": True}
        
        # State
        self.tick_count = 0
        self.phase = "Observe"
        
        # Load existing state
        self._load_state()
        
    def _load_state(self):
        """Load existing state if available"""
        if self.state_path.exists():
            try:
                with open(self.state_path) as f:
                    data = json.load(f)
                    self.tick_count = data.get("tick", 0)
                    print(f"[AOSv3] Loaded state: tick {self.tick_count}")
            except:
                pass
    
    def _save_state(self):
        """Save current state"""
        state = {
            "tick": self.tick_count,
            "timestamp": time.time(),
            "phase": self.phase,
            "mode": "AOSv3-7Region",
            "limbic": self.limbic,
            "memory_nn": {
                "clusters": self.hippocampus.total_traces,
                "episodic": len(self.hippocampus.episodic_buffer),
                "semantic": len(self.hippocampus.semantic_memory)
            },
            "policy_nn": {
                "layers": 3,
                "nodes": [8, 12, 40 + self.tick_count // 50]
            }
        }
        
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def tick(self):
        """One complete OODA cycle"""
        self.tick_count += 1
        
        # O: Observe (Thalamus)
        obs = self._generate_observation()
        
        # O: Orient (Hippocampus - memory)
        context = {
            "recent": self.hippocampus.retrieve(str(obs), n=3),
            "stats": self.hippocampus.get_stats()
        }
        
        # Limbic evaluation
        affect = self.limbic.copy()
        affect["novelty"] = random.uniform(0.3, 0.9)  # Simulated
        
        # D: Decide (PFC)
        decision = self.pfc.decide(obs, context, affect)
        
        # Store memory (Hippocampus)
        memory_result = self.hippocampus.store(
            obs,
            {"plan": decision["reason"]},
            {"type": decision["action"]}
        )
        
        # Update affect
        self.limbic["novelty"] = memory_result["novelty"]
        
        # Cycle phase
        phases = ["Observe", "Orient", "Decide", "Act"]
        self.phase = phases[self.tick_count % 4]
        
        # Save state periodically
        if self.tick_count % 10 == 0:
            self._save_state()
            
            if self.tick_count % 100 == 0:
                stats = self.hippocampus.get_stats()
                print(f"[AOSv3] Tick {self.tick_count}, Memories: {stats['total_traces']}, "
                      f"Episodic: {stats['episodic_count']}, Semantic: {stats['semantic_count']}")
    
    def _generate_observation(self) -> Dict:
        """Generate synthetic observation"""
        obs_types = ["system", "user", "internal", "environment"]
        return {
            "type": random.choice(obs_types),
            "data": f"observation_{self.tick_count}",
            "timestamp": time.time()
        }
    
    def run(self, duration_seconds: int = 60):
        """Run brain for specified duration"""
        print(f"[AOSv3] Starting 7-region brain...")
        print(f"[AOSv3] Initial tick: {self.tick_count}")
        
        start = time.time()
        while time.time() - start < duration_seconds:
            self.tick()
            time.sleep(0.01)  # 100 ticks/sec max
        
        self._save_state()
        print(f"[AOSv3] Complete. Final tick: {self.tick_count}")


if __name__ == "__main__":
    print("=" * 60)
    print("  AOS Brain v3.0 - 7-Region Architecture")
    print("  Non-blocking, Ollama-Free, High-Integrity")
    print("=" * 60)
    
    brain = AOSBrainv3()
    brain.run(duration_seconds=30)
    
    print("=" * 60)
    print("  Run complete")
    print("=" * 60)
