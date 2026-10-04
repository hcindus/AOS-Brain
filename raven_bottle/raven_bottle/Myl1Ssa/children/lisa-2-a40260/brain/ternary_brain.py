#!/usr/bin/env python3
"""
TERNARY BRAIN
=============
A brain based on ternary logic (-1, 0, 1)
Qbits: -1 (FALSE/NEGATIVE), 0 (UNKNOWN/NEUTRAL), 1 (TRUE/POSITIVE)

Based on Miles Brain v4.4 architecture
Model: bonsai-8b-q1_0 (ternary-friendly)
"""

import json
import time
from typing import List, Dict, Any, Optional

# =============================================================================
# TERNARY LOGIC ENGINE (-1, 0, 1)
# =============================================================================

class TernaryQbit:
    """A ternary qbit: -1 (false/neg), 0 (unknown), 1 (true/pos)"""
    
    def __init__(self, value: int = 0):
        if value not in [-1, 0, 1]:
            raise ValueError("Ternary qbit must be -1, 0, or 1")
        self.value = value
    
    def __repr__(self):
        return f"Q({self.value})"
    
    def __invert__(self):
        """Ternary NOT: flip -1<->1, keep 0 as 0"""
        if self.value == -1:
            return TernaryQbit(1)
        elif self.value == 1:
            return TernaryQbit(-1)
        return TernaryQbit(0)
    
    def __and__(self, other):
        """Ternary AND: -1 wins, then 1, then 0"""
        if self.value == -1 or other.value == -1:
            return TernaryQbit(-1)
        if self.value == 1 and other.value == 1:
            return TernaryQbit(1)
        return TernaryQbit(0)
    
    def __or__(self, other):
        """Ternary OR: 1 wins, then -1, then 0"""
        if self.value == 1 or other.value == 1:
            return TernaryQbit(1)
        if self.value == -1 or other.value == -1:
            return TernaryQbit(-1)
        return TernaryQbit(0)
    
    def __xor__(self, other):
        """Ternary XOR: -1 and 1 = 1, same = 0"""
        if self.value == other.value:
            return TernaryQbit(0)
        if self.value != 0 and other.value != 0:
            return TernaryQbit(-1)
        return TernaryQbit(0)
    
    @staticmethod
    def from_float(f: float) -> 'TernaryQbit':
        """Convert float to ternary: <0 = -1, 0 = 0, >0 = 1"""
        if f < 0:
            return TernaryQbit(-1)
        elif f > 0:
            return TernaryQbit(1)
        return TernaryQbit(0)
    
    @staticmethod
    def majority(votes: List['TernaryQbit']) -> 'TernaryQbit':
        """Ternary majority vote"""
        counts = {-1: 0, 0: 0, 1: 0}
        for v in votes:
            counts[v.value] += 1
        return TernaryQbit(max(counts, key=counts.get))


class TernaryState:
    """A state of ternary qbits forming a memory pattern"""
    
    def __init__(self, size: int):
        self.size = size
        self.qbits = [TernaryQbit(0) for _ in range(size)]
    
    def set(self, index: int, value: int):
        self.qbits[index] = TernaryQbit(value)
    
    def get(self, index: int) -> int:
        return self.qbits[index].value
    
    def activation(self) -> List[int]:
        """Return list of active indices (where value != 0)"""
        return [i for i, q in enumerate(self.qbits) if q.value != 0]
    
    def energy(self) -> float:
        """Calculate pattern energy"""
        return sum(q.value for q in self.qbits) / self.size
    
    def __repr__(self):
        return f"State[{','.join(str(q.value) for q in self.qbits)}]"


# =============================================================================
# TERNARY NEURAL NETWORK LAYERS
# =============================================================================

class TernaryLayer:
    """A layer of ternary neurons"""
    
    def __init__(self, input_size: int, output_size: int):
        self.input_size = input_size
        self.output_size = output_size
        # Weights: -1, 0, or 1 (sparse = efficient)
        self.weights = [[TernaryQbit(0) for _ in range(input_size)] 
                        for _ in range(output_size)]
        self.bias = [TernaryQbit(0) for _ in range(output_size)]
    
    def randomize(self, sparsity: float = 0.3):
        """Random initialize with sparsity"""
        import random
        for i in range(self.output_size):
            for j in range(self.input_size):
                if random.random() < sparsity:
                    self.weights[i][j] = TernaryQbit(random.choice([-1, 1]))
            self.bias[i] = TernaryQbit(random.choice([-1, 0, 1]))
    
    def forward(self, inputs: List[TernaryQbit]) -> List[TernaryQbit]:
        """Forward pass through ternary layer"""
        outputs = []
        for i in range(self.output_size):
            total = self.bias[i]
            for j, inp in enumerate(inputs):
                if self.weights[i][j].value != 0:
                    # Ternary multiplication
                    prod = TernaryQbit(self.weights[i][j].value * inp.value)
                    total = total | prod  # OR as accumulation
            outputs.append(total)
        return outputs


# =============================================================================
# BRAIN ORGANS (Based on Miles Brain v4.4)
# =============================================================================

class KidneyFilter:
    """Signal filter - processes inputs, outputs quality score"""
    
    def __init__(self):
        self.noise_estimate = 0.5
        self.total_processed = 0
        self.excreted = 0
    
    def filter(self, input_data: str) -> tuple[bool, float]:
        """
        Filter input through kidney
        Returns: (accepted, quality_score)
        """
        self.total_processed += 1
        
        # Simple quality scoring
        score = 0.5
        
        # Check for meaningful content
        if len(input_data) > 10:
            score += 0.1
        
        # Check for spam patterns
        spam_words = ['click here', 'free money', 'viagra', 'won']
        for word in spam_words:
            if word.lower() in input_data.lower():
                score -= 0.3
        
        # Clamp
        score = max(0, min(1, score))
        
        # Update noise estimate (moving average)
        self.noise_estimate = (self.noise_estimate * 0.9) + ((1 - score) * 0.1)
        
        # Excrete low quality
        if score < 0.4:
            self.excreted += 1
            return False, score
        
        return True, score
    
    def status(self) -> dict:
        return {
            'noise_estimate': self.noise_estimate,
            'total_processed': self.total_processed,
            'excreted': self.excreted
        }


class Consciousness:
    """3-layer consciousness: conscious(10), subconscious(100), unconscious(2000)"""
    
    def __init__(self):
        self.conscious = TernaryState(10)
        self.subconscious = TernaryState(100)
        self.unconscious = TernaryState(2000)
    
    def add(self, item: str, layer: str = 'conscious'):
        """Add item to consciousness layer"""
        if layer == 'conscious':
            # Shift to subconscious if full, add to conscious
            active = self.conscious.activation()
            if len(active) >= 10:
                # Move oldest to subconscious (simplified: random)
                pass  # Shift logic would go here
            # Simple add - in real impl, would manage indices
            self.conscious.set(len(active) % 10, 1)
        elif layer == 'subconscious':
            active = self.subconscious.activation()
            self.subconscious.set(len(active) % 100, 1)
        else:
            active = self.unconscious.activation()
            self.unconscious.set(len(active) % 2000, 1)
    
    def get_focus(self) -> List[int]:
        """Get current conscious focus"""
        return self.conscious.activation()
    
    def status(self) -> dict:
        return {
            'conscious': len(self.conscious.activation()),
            'subconscious': len(self.subconscious.activation()),
            'unconscious': len(self.unconscious.activation())
        }


class TracrayMemory:
    """Experience buffer - stores last 5000 interactions"""
    
    def __init__(self, capacity: int = 5000):
        self.capacity = capacity
        self.experiences = []
        self.episodes = 0
    
    def add(self, experience: str, importance: float = 0.5):
        """Add experience with importance"""
        qbits = [TernaryQbit.from_float(importance)]
        self.experiences.append({
            'text': experience,
            'qbits': qbits,
            'timestamp': time.time()
        })
        
        # Keep capacity
        if len(self.experiences) > self.capacity:
            self.experiences = self.experiences[-self.capacity:]
        
        self.episodes += 1
    
    def search(self, query: str) -> List[dict]:
        """Search experiences"""
        results = []
        for exp in self.experiences[-20:]:  # Last 20
            if query.lower() in exp['text'].lower():
                results.append(exp)
        return results
    
    def status(self) -> dict:
        return {
            'total': len(self.experiences),
            'episodes': self.episodes,
            'utilization': len(self.experiences) / self.capacity
        }


class ThyroidRouter:
    """Routes between local and remote (VPS) processing"""
    
    def __init__(self):
        self.state = "LOCAL"  # or "VPS"
        self.ollama_level = 0.0
        self.local_level = 1.0
    
    def route(self, query: str) -> str:
        """Decide: local or VPS?"""
        # Simple heuristic: long queries = VPS
        if len(query) > 100:
            self.state = "VPS"
            self.ollama_level = 1.0
            self.local_level = 0.0
        else:
            self.state = "LOCAL"
            self.ollama_level = 0.0
            self.local_level = 1.0
        
        return self.state
    
    def status(self) -> dict:
        return {
            'state': self.state,
            'ollama_level': self.ollama_level,
            'local_level': self.local_level
        }


class LiverFilter:
    """Filters toxic/malicious content"""
    
    def __init__(self):
        self.state = "CLEAN"
        self.filtered_total = 0
        self.toxic_neutralized = 0
        self.purify_threshold = 0.3
        self.toxic_threshold = 0.7
    
    def purify(self, content: str) -> tuple[bool, str]:
        """Check and neutralize toxicity"""
        self.filtered_total += 1
        
        # Simple toxicity check
        toxic_patterns = ['hack', 'attack', 'virus', 'exploit']
        toxicity = 0.0
        
        for pattern in toxic_patterns:
            if pattern in content.lower():
                toxicity += 0.2
        
        if toxicity > self.toxic_threshold:
            self.toxic_neutralized += 1
            self.state = "TOXIC_DETECTED"
            return False, "[FILTERED]"
        
        self.state = "CLEAN"
        return True, content
    
    def status(self) -> dict:
        return {
            'state': self.state,
            'filtered': self.filtered_total,
            'neutralized': self.toxic_neutralized
        }


# =============================================================================
# MAIN BRAIN CLASS
# =============================================================================

class TernaryBrain:
    """
    Ternary Brain - Based on Miles Brain v4.4
    Uses ternary qbits (-1, 0, 1)
    Model: bonsai-8b-q1_0 compatible
    """
    
    def __init__(self):
        self.name = "Mortimer_Ternary_Brain_v1.0"
        
        # Brain organs
        self.kidney = KidneyFilter()
        self.consciousness = Consciousness()
        self.tracray = TracrayMemory()
        self.thyroid = ThyroidRouter()
        self.liver = LiverFilter()
        
        # Cortex (8 regions)
        self.cortex_regions = [TernaryLayer(100, 50) for _ in range(8)]
        for layer in self.cortex_regions:
            layer.randomize(sparsity=0.3)
        
        # Router model (bonsai)
        self.router_model = "bonsai-8b-q1_0"
        
        self.signal_quality = 0.865
    
    def process(self, input_data: str) -> dict:
        """Process input through brain"""
        responses = {}
        
        # 1. Liver: check for toxicity
        safe, cleaned = self.liver.purify(input_data)
        if not safe:
            responses['status'] = 'rejected'
            responses['reason'] = 'toxic content detected'
            return responses
        
        # 2. Kidney: filter quality
        accepted, quality = self.kidney.filter(cleaned)
        responses['quality'] = quality
        
        if not accepted:
            responses['status'] = 'filtered'
            responses['reason'] = 'low quality'
            return responses
        
        # 3. Thyroid: route decision
        route = self.thyroid.route(cleaned)
        responses['route'] = route
        
        # 4. Consciousness: add to focus
        self.consciousness.add(cleaned, 'conscious')
        
        # 5. Tracray: store experience
        self.tracray.add(cleaned, importance=quality)
        
        responses['status'] = 'processed'
        responses['signal_quality'] = self.signal_quality
        
        return responses
    
    def think(self, query: str) -> str:
        """Main thinking loop"""
        # Process through brain
        result = self.process(query)
        
        if result['status'] in ['rejected', 'filtered']:
            return f"[{result['status'].upper()}] {result.get('reason', 'unknown')}"
        
        # Routing
        if result['route'] == 'VPS':
            return f"[WOULD USE VPS MODEL: {self.router_model}] Processing: {query[:50]}..."
        
        # Local processing
        focus = self.consciousness.get_focus()
        return f"[TERNARY BRAIN] Focus items: {len(focus)} | Quality: {result['quality']:.2f}"
    
    def state(self) -> dict:
        """Get complete brain state"""
        return {
            'name': self.name,
            'model': self.router_model,
            'kidney': self.kidney.status(),
            'consciousness': self.consciousness.status(),
            'tracray': self.tracray.status(),
            'thyroid': self.thyroid.status(),
            'liver': self.liver.status(),
            'signal_quality': self.signal_quality,
            'cortex_regions': 8
        }
    
    def __repr__(self):
        return f"<TernaryBrain: {self.name}>"


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧠 TERNARY BRAIN v1.0")
    print("Qbits: -1 (FALSE) | 0 (UNKNOWN) | 1 (TRUE)")
    print("Model: bonsai-8b-q1_0 compatible")
    print("=" * 60)
    
    # Create brain
    brain = TernaryBrain()
    print(f"\n{brain}")
    
    # Test ternary logic
    print("\n--- Ternary Logic Test ---")
    a = TernaryQbit(1)
    b = TernaryQbit(-1)
    c = TernaryQbit(0)
    
    print(f"1 AND -1 = {(a & b).value}")  # Should be -1
    print(f"1 OR -1 = {(a | b).value}")    # Should be 1
    print(f"NOT 1 = {(~a).value}")         # Should be -1
    print(f"1 XOR 0 = {(a ^ c).value}")    # Should be 1
    
    # Process test inputs
    print("\n--- Brain Processing Test ---")
    test_inputs = [
        "Hello, how are you?",
        "Click here for free money!",
        "Tell me about robots",
        "Design a neural network"
    ]
    
    for inp in test_inputs:
        result = brain.think(inp)
        print(f"Input: {inp[:30]}...")
        print(f"Result: {result}")
        print()
    
    # Show state
    print("--- Brain State ---")
    state = brain.state()
    print(f"Kidney: {state['kidney']}")
    print(f"Consciousness: {state['consciousness']}")
    print(f"Thyroid: {state['thyroid']}")
    print(f"Tracray: {state['tracray']}")
    print(f"Signal Quality: {state['signal_quality']}")