#!/usr/bin/env python3
"""
AOS KIDNEYS v1.0 - Ternary Waste Management & Pattern Recycling
Biological analogy: Filter blood, reabsorb nutrients, excrete waste as urine

Ternary States:
- FILTER: Pass useful patterns to memory/storage
- REABSORB: Extract and recycle valuable signal from waste streams
- EXCRETE: Discard pure noise/waste permanently

Key Concept: Signal vs Noise
- SIGNAL: Information that advances goals, reveals patterns, enables predictions
- NOISE: Random variation that obscures patterns, redundant data, corruption
"""

import time
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum, auto
from collections import defaultdict


class KidneyState(Enum):
    FILTER = auto()     # Standard filtering - keep useful, discard waste
    REABSORB = auto()   # Aggressive recycling - extract signal from garbage
    EXCRETE = auto()    # Emergency purge - discard everything


@dataclass
class Filtrate:
    """A filtered unit ready for processing"""
    content: str
    source: str
    timestamp: float
    signal_score: float = 0.0      # 0.0-1.0, higher = more signal
    pattern_hash: str = ""         # Fingerprint for deduplication
    recycle_count: int = 0         # How many times reabsorbed
    
    def __post_init__(self):
        if not self.pattern_hash:
            self.pattern_hash = hashlib.md5(self.content.encode()).hexdigest()[:8]


class AOSKidneysV1:
    """
    Ternary Kidneys - Pattern recycling and waste management
    
    Like biological kidneys:
    - FILTER: Keep the good stuff, send waste to bladder
    - REABSORB: When dehydrated (low signal), squeeze waste for every drop of value
    - EXCRETE: When flooded (too much noise), purge to prevent system damage
    
    Signal vs Noise Detection:
    - Signal: Novel, structured, goal-relevant, low entropy
    - Noise: Repetitive, random, irrelevant, high entropy
    """
    
    def __init__(self,
                 signal_threshold: float = 0.5,
                 reabsorb_threshold: float = 0.2,
                 bladder_capacity: int = 500,
                 pattern_memory: int = 1000):
        
        self.signal_threshold = signal_threshold    # Above this = keep
        self.reabsorb_threshold = reabsorb_threshold # Below this = potential waste
        self.bladder_capacity = bladder_capacity
        self.pattern_limit = pattern_memory
        
        self.state = KidneyState.FILTER
        
        # Storage systems
        self.bladder = []           # Waste waiting for potential reabsorption
        self.nutrients = []         # Valuable patterns going to memory
        self.pattern_history = defaultdict(int)  # Seen patterns (for dedup)
        
        # Statistics
        self.total_processed = 0
        self.reabsorbed_count = 0
        self.excreted_count = 0
        
        # Signal/Noise tracking
        self.signal_history = []
        self.noise_estimate = 0.5
        
        print(f"[Kidneys v1.0] Initialized - ternary waste management")
        print(f"  FILTER:   Keep signal >{signal_threshold}, queue rest")
        print(f"  REABSORB: Extract value from waste when signal low")
        print(f"  EXCRETE:  Emergency purge when overwhelmed")
    
    def calculate_signal_score(self, content: str, context: dict = None) -> float:
        """
        Calculate signal-to-noise ratio for content
        
        SIGNAL indicators:
        - Novel (hasn't been seen before)
        - Structured (has patterns, not random)
        - Goal-relevant (contains actionable info)
        - Low entropy (predictable, not chaotic)
        
        NOISE indicators:
        - Repetitive (already seen)
        - Random/gibberish
        - Irrelevant (no action possible)
        - High entropy (chaotic)
        """
        score = 0.5  # Baseline
        
        # Novelty check (signal is novel)
        pattern_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        if pattern_hash not in self.pattern_history:
            score += 0.2  # Novel = signal
            self.pattern_history[pattern_hash] = 1
        else:
            score -= 0.3  # Repetitive = noise
            self.pattern_history[pattern_hash] += 1
        
        # Structure check (signal has structure)
        words = content.split()
        if len(words) > 3:
            avg_len = sum(len(w) for w in words) / len(words)
            if 3 < avg_len < 12:  # Normal word lengths = structured
                score += 0.15
            else:
                score -= 0.1
        
        # Actionability check (signal enables action)
        action_keywords = ['error', 'warning', 'complete', 'failed', 'success', 
                          'created', 'deleted', 'updated', 'running', 'stopped',
                          'temperature', 'pressure', 'status', 'alert']
        if any(kw in content.lower() for kw in action_keywords):
            score += 0.15  # Actionable = signal
        
        # Context boost (if provided)
        if context:
            if context.get('is_alert', False):
                score += 0.2
            if context.get('is_user_input', False):
                score += 0.1
        
        # Entropy estimate (low entropy = signal)
        if len(content) > 10:
            unique_ratio = len(set(content.lower())) / len(content)
            if unique_ratio < 0.7:  # Low character diversity = structure
                score += 0.1
            else:
                score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def process(self, content: str, source: str = "unknown", 
                context: dict = None, force_state: KidneyState = None) -> Tuple[KidneyState, Optional[str], dict]:
        """
        Process content through kidney filtration
        
        Returns: (state, result_content, metadata)
        """
        signal_score = self.calculate_signal_score(content, context)
        self.total_processed += 1
        
        # Determine state
        if force_state:
            self.state = force_state
        else:
            self.state = self._determine_state(signal_score, content)
        
        # Process based on state
        if self.state == KidneyState.FILTER:
            result = self._filter(content, signal_score, source)
            
        elif self.state == KidneyState.REABSORB:
            result = self._reabsorb()
            
        else:  # EXCRETE
            result = self._excrete()
        
        # Update noise estimate (exponential moving average)
        self.noise_estimate = 0.9 * self.noise_estimate + 0.1 * (1 - signal_score)
        self.signal_history.append(signal_score)
        if len(self.signal_history) > 100:
            self.signal_history.pop(0)
        
        metadata = {
            "signal_score": signal_score,
            "noise_estimate": self.noise_estimate,
            "bladder_level": len(self.bladder),
            "nutrients_stored": len(self.nutrients),
            "unique_patterns": len(self.pattern_history)
        }
        
        return self.state, result, metadata
    
    def _determine_state(self, signal_score: float, content: str) -> KidneyState:
        """Determine which filtration mode to use"""
        
        # Check for emergency (bladder full)
        if len(self.bladder) > self.bladder_capacity * 0.9:
            return KidneyState.EXCRETE
        
        # Check for dehydration (low recent signal)
        recent_signal = sum(self.signal_history[-10:]) / max(len(self.signal_history[-10:]), 1)
        if recent_signal < 0.3 and len(self.bladder) > 10:
            return KidneyState.REABSORB
        
        # Normal filtering
        return KidneyState.FILTER
    
    def _filter(self, content: str, signal_score: float, source: str) -> Optional[str]:
        """FILTER: Keep signal, queue potential noise"""
        if signal_score >= self.signal_threshold:
            # Good signal - store as nutrient
            filtrate = Filtrate(
                content=content,
                source=source,
                timestamp=time.time(),
                signal_score=signal_score
            )
            self.nutrients.append(filtrate)
            
            # Keep nutrients bounded
            if len(self.nutrients) > self.pattern_limit:
                self.nutrients.pop(0)
            
            return content
        else:
            # Low signal - store in bladder for possible reabsorption
            filtrate = Filtrate(
                content=content,
                source=source,
                timestamp=time.time(),
                signal_score=signal_score
            )
            self.bladder.append(filtrate)
            
            # Keep bladder bounded
            if len(self.bladder) > self.bladder_capacity:
                old = self.bladder.pop(0)
                self.excreted_count += 1
            
            return None  # Not immediately passed through
    
    def _reabsorb(self) -> Optional[str]:
        """REABSORB: Squeeze waste for valuable patterns"""
        if not self.bladder:
            return None
        
        # Sort bladder by signal score (highest first)
        self.bladder.sort(key=lambda x: x.signal_score, reverse=True)
        
        # Take best from waste
        best_waste = self.bladder.pop(0)
        best_waste.recycle_count += 1
        self.reabsorbed_count += 1
        
        # Re-add to nutrients
        self.nutrients.append(best_waste)
        
        print(f"[Kidneys] REABSORBED pattern from waste (score: {best_waste.signal_score:.2f})")
        
        return best_waste.content
    
    def _excrete(self) -> None:
        """EXCRETE: Emergency purge of all waste"""
        purged = len(self.bladder)
        self.bladder = []
        self.excreted_count += purged
        
        print(f"[Kidneys] EXCRETED {purged} waste items (emergency purge)")
        
        return None
    
    def get_nutrients(self, n: int = 10) -> List[Filtrate]:
        """Get top nutrients for memory storage"""
        self.nutrients.sort(key=lambda x: x.signal_score, reverse=True)
        return self.nutrients[:n]
    
    def get_status(self) -> dict:
        """Current kidney status"""
        recent_signal = sum(self.signal_history[-20:]) / max(len(self.signal_history[-20:]), 1) if self.signal_history else 0
        
        return {
            "state": self.state.name,
            "total_processed": self.total_processed,
            "reabsorbed": self.reabsorbed_count,
            "excreted": self.excreted_count,
            "bladder_level": len(self.bladder),
            "bladder_capacity": self.bladder_capacity,
            "nutrients_stored": len(self.nutrients),
            "recent_signal_avg": recent_signal,
            "noise_estimate": self.noise_estimate,
            "unique_patterns_seen": len(self.pattern_history)
        }


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("  🫘 KIDNEYS v1.0 - Ternary Waste Management Test")
    print("=" * 70)
    
    kidneys = AOSKidneysV1()
    
    print("\nSIGNAL vs NOISE Examples:")
    print("-" * 70)
    
    test_inputs = [
        ("ERROR: Database connection failed at 07:42:15", "log", {"is_alert": True}),
        ("asdfasdf jkl;jkl; random gibberish content here", "garbage", {}),
        ("System temperature: 45°C, CPU: 12%", "sensor", {}),
        ("The quick brown fox jumps over the lazy dog", "text", {}),
        ("!!!!!!!!! ALERT !!!!!!!!!!", "alert", {"is_alert": True}),
        ("User input: Start the backup process", "user", {"is_user_input": True}),
        ("lorem ipsum dolor sit amet consectetur", "filler", {}),
        ("Backup completed successfully at 2026-04-05 07:42:30", "log", {}),
    ]
    
    print("\nProcessing stream...\n")
    for content, source, context in test_inputs:
        state, result, meta = kidneys.process(content, source, context)
        
        signal_type = "SIGNAL" if meta['signal_score'] > 0.5 else "NOISE"
        
        print(f"  [{signal_type}] {source:8s} | Score: {meta['signal_score']:.2f} | State: {state.name:10s}")
        print(f"    In:  {content[:50]}...")
        if result:
            print(f"    Out: {result[:50]}...")
        elif state.name == "REABSORB":
            print(f"    Out: [REABSORBED from waste]")
        else:
            print(f"    Out: [FILTERED → bladder]")
        print()
    
    # Force reabsorption
    print("-" * 70)
    print("\nForcing REABSORB mode (low signal detected)...\n")
    kidneys.signal_history = [0.1] * 15  # Simulate low signal period
    state, result, meta = kidneys.process("Low priority log entry", "system", {})
    
    print("=" * 70)
    print("  Kidney Status:")
    for k, v in kidneys.get_status().items():
        print(f"    {k}: {v}")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("  SIGNAL vs NOISE SUMMARY")
    print("=" * 70)
    print("""
    SIGNAL (Keep):
    - Novel patterns (never seen before)
    - Structured content (not random)
    - Actionable information (errors, alerts, completions)
    - Goal-relevant data
    - Low entropy (predictable patterns)
    
    NOISE (Filter/Reabsorb/Excrete):
    - Repetitive content (already seen)
    - Random/gibberish text
    - Irrelevant filler (lorem ipsum)
    - Excessive punctuation
    - High entropy (chaotic)
    """)
