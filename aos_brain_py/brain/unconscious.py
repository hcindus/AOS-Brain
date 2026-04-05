#!/usr/bin/env python3
"""
Unconscious processing module - sleep, dreams, and memory consolidation.

During sleep:
1. Replay recent memories
2. Consolidate short-term to long-term
3. Generate dream sequences
4. Prune weak connections
5. Strengthen important patterns
"""

import time
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import deque


@dataclass
class DreamSequence:
    """A dream sequence during sleep."""
    content: str
    source: str  # memory, imagination, noise
    vividness: float  # 0-1
    timestamp: float


class UnconsciousProcessor:
    """
    Unconscious mind - processes during sleep/rest cycles.
    
    Functions:
    - Memory replay and consolidation
    - Pattern recognition
    - Dream generation
    - Garbage collection of weak memories
    """
    
    def __init__(self, brain):
        self.brain = brain
        self.is_sleeping = False
        self.dream_log = deque(maxlen=100)
        self.consolidation_count = 0
        
        # Sleep parameters
        self.sleep_duration = 60.0  # seconds of processing per sleep cycle
        self.replay_probability = 0.7
        self.consolidation_threshold = 0.5
        
    def enter_sleep(self, duration: Optional[float] = None) -> Dict:
        """
        Enter sleep mode for unconscious processing.
        
        Args:
            duration: How long to sleep (seconds). Default: 60s
            
        Returns:
            Sleep report with dreams and consolidations
        """
        if duration:
            self.sleep_duration = duration
        
        print(f"[Unconscious] Entering sleep mode for {self.sleep_duration}s...")
        self.is_sleeping = True
        
        sleep_report = {
            "start_time": time.time(),
            "duration": self.sleep_duration,
            "dreams": [],
            "consolidations": 0,
            "pruned_memories": 0,
        }
        
        # Phase 1: Memory replay (first 30% of sleep)
        dreams_from_replay = self._replay_memories()
        sleep_report["dreams"].extend(dreams_from_replay)
        
        # Phase 2: Consolidation (next 40% of sleep)
        consolidations = self._consolidate_memories()
        sleep_report["consolidations"] = consolidations
        
        # Phase 3: Dream generation (last 30% of sleep)
        dreams_generated = self._generate_dreams()
        sleep_report["dreams"].extend(dreams_generated)
        
        # Phase 4: Garbage collection
        pruned = self._prune_weak_memories()
        sleep_report["pruned_memories"] = pruned
        
        sleep_report["end_time"] = time.time()
        sleep_report["actual_duration"] = sleep_report["end_time"] - sleep_report["start_time"]
        
        self.is_sleeping = False
        self.consolidation_count += consolidations
        
        print(f"[Unconscious] Waking up. Processed {consolidations} memories, {len(sleep_report['dreams'])} dreams.")
        
        return sleep_report
    
    def _replay_memories(self) -> List[DreamSequence]:
        """
        Replay recent memories during light sleep.
        Creates dreams from actual experiences.
        """
        dreams = []
        
        # Get recent short-term memories
        recent_memories = list(self.brain.short_term)[-10:]
        
        for memory in recent_memories:
            if random.random() < self.replay_probability:
                # Create dream from memory
                content = str(memory.get("content", ""))
                if len(content) > 50:
                    # Fragment and recombine
                    fragments = content.split()
                    random.shuffle(fragments)
                    dream_content = " ".join(fragments[:10]) + "..."
                else:
                    dream_content = content
                
                dream = DreamSequence(
                    content=dream_content,
                    source="memory_replay",
                    vividness=random.uniform(0.3, 0.8),
                    timestamp=time.time()
                )
                dreams.append(dream)
                self.dream_log.append(dream)
                
                time.sleep(0.5)  # Simulate processing time
        
        return dreams
    
    def _consolidate_memories(self) -> int:
        """
        Consolidate short-term memories to long-term.
        Move important traces from hippocampus to semantic graph.
        """
        consolidated = 0
        
        # Process short-term memories
        for trace in list(self.brain.short_term):
            importance = trace.get("importance", 0.5)
            
            if importance >= self.consolidation_threshold:
                # Move to mid-term
                self.brain.mid_term.append(trace)
                
                # Also add to semantic graph if substrate exists
                if hasattr(self.brain, 'substrate'):
                    thought = {
                        "language": str(trace.get("content", ""))[:100],
                        "ternary_code": trace.get("ternary", [0,0,0,0,0]),
                        "value": {"importance": importance},
                        "memories_used": [],
                    }
                    try:
                        self.brain.substrate.add_thought(thought)
                        self.brain.substrate.grow(thought)
                    except:
                        pass
                
                consolidated += 1
                time.sleep(0.2)  # Simulate consolidation time
        
        # Clear processed short-term memories
        self.brain.short_term.clear()
        
        return consolidated
    
    def _generate_dreams(self) -> List[DreamSequence]:
        """
        Generate novel dreams from patterns and imagination.
        Combines elements from different memories.
        """
        dreams = []
        
        # Get random elements from mid-term memory
        if len(self.brain.mid_term) >= 2:
            elements = random.sample(list(self.brain.mid_term), 
                                     min(3, len(self.brain.mid_term)))
            
            # Create surreal combinations
            dream_content = "In a dream: "
            for elem in elements:
                content = str(elem.get("content", ""))
                words = content.split()[:5]
                dream_content += " ".join(words) + "... "
            
            dream = DreamSequence(
                content=dream_content.strip(),
                source="imagination",
                vividness=random.uniform(0.1, 0.6),
                timestamp=time.time()
            )
            dreams.append(dream)
            self.dream_log.append(dream)
        
        time.sleep(1.0)  # Dream generation time
        
        return dreams
    
    def _prune_weak_memories(self) -> int:
        """
        Remove weak or redundant memories.
        Keeps the brain efficient.
        """
        pruned = 0
        
        # Check mid-term memories
        threshold = 0.2
        to_remove = []
        
        for trace in self.brain.mid_term:
            if trace.get("importance", 0.5) < threshold:
                if random.random() < 0.5:  # 50% chance to prune weak memories
                    to_remove.append(trace)
        
        for trace in to_remove:
            self.brain.mid_term.remove(trace)
            pruned += 1
        
        return pruned
    
    def get_dream_summary(self) -> str:
        """Get summary of recent dreams."""
        if not self.dream_log:
            return "No dreams recorded."
        
        recent_dreams = list(self.dream_log)[-5:]
        summary = f"Recent dreams ({len(recent_dreams)} total in log):\n"
        
        for i, dream in enumerate(recent_dreams, 1):
            summary += f"  {i}. [{dream.source}] {dream.content[:50]}... (vividness: {dream.vividness:.2f})\n"
        
        return summary
    
    def quick_nap(self, duration: float = 10.0) -> Dict:
        """Take a quick nap for brief consolidation."""
        return self.enter_sleep(duration)


def demo_unconscious():
    """Demo unconscious processing with sleep."""
    print("=" * 60)
    print("💤 UNCONSCIOUS PROCESSING DEMO")
    print("=" * 60)
    print()
    
    # Import brain
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from seven_region import SevenRegionBrain
    
    # Create brain
    brain = SevenRegionBrain()
    
    # Create unconscious processor
    unconscious = UnconsciousProcessor(brain)
    
    # Feed some memories first
    print("Feeding memories before sleep...")
    for i in range(10):
        brain.feed(f"Memory {i}: Learned about {'cats' if i % 2 == 0 else 'dogs'}", "learning")
    
    print(f"  Short-term: {len(brain.short_term)} memories")
    print()
    
    # Enter sleep
    print("Entering sleep mode...")
    report = unconscious.enter_sleep(duration=5.0)  # 5 seconds for demo
    
    print("\n" + "=" * 60)
    print("SLEEP REPORT")
    print("=" * 60)
    print(f"Duration: {report['actual_duration']:.2f}s")
    print(f"Dreams: {len(report['dreams'])}")
    print(f"Consolidations: {report['consolidations']}")
    print(f"Pruned memories: {report['pruned_memories']}")
    
    print("\nDreams:")
    for i, dream in enumerate(report['dreams'], 1):
        print(f"  {i}. [{dream.source}] {dream.content[:60]}...")
    
    print(f"\nAfter sleep:")
    print(f"  Short-term: {len(brain.short_term)} memories")
    print(f"  Mid-term: {len(brain.mid_term)} memories")
    
    print("\n" + "=" * 60)
    print("✅ Unconscious processing complete!")
    print("=" * 60)


if __name__ == "__main__":
    demo_unconscious()
