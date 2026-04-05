#!/usr/bin/env python3
"""
Stomach-to-Brain Auto-Feed Pipeline.

Feeds ALL data to stomach first, then auto-feeds digested chunks to brain.
"""

import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from stomach.ternary_stomach import TernaryStomach
from brain.seven_region import SevenRegionBrain


class StomachBrainPipeline:
    """
    Complete pipeline: Data → Stomach → Digest → Brain.
    
    All data flows through stomach first for optimal digestion
    before feeding to brain. Stomach auto-feeds brain as chunks
    become ready.
    """
    
    def __init__(self, brain: Optional[SevenRegionBrain] = None):
        self.stomach = TernaryStomach()
        self.brain = brain or SevenRegionBrain()
        
        # Auto-feed settings
        self.auto_feed_enabled = True
        self.chunks_per_cycle = 3
        
        # Stats
        self.items_fed_to_stomach = 0
        self.items_digested = 0
        self.items_fed_to_brain = 0
        
        # Buffer for brain-ready chunks (intercepted before absorption)
        self.brain_ready_buffer = []
        
    def feed_to_stomach(self, data: Any, complexity: float = 0.5, 
                       nutrition: float = 0.5, source: str = "pipeline") -> Dict:
        """Feed any data to stomach first (never direct to brain)."""
        
        # Convert data to digestible format
        if isinstance(data, str):
            content = data
        elif isinstance(data, dict):
            import json
            content = json.dumps(data)
        elif isinstance(data, list):
            content = "\n".join(str(item) for item in data)
        else:
            content = str(data)
        
        # Always feed to stomach first
        result = self.stomach.consume(
            item=content,
            complexity=complexity,
            nutrition=nutrition
        )
        
        self.items_fed_to_stomach += 1
        
        # Auto-digest and feed to brain
        if self.auto_feed_enabled:
            self._auto_digest_and_feed(source)
        
        return {
            "stomach_result": result,
            "stomach_status": self.stomach.get_status(),
            "brain_ticks": self.brain.tick_count,
            "brain_clusters": self.brain.regions['hippocampus'].get_cluster_count()
        }
    
    def _auto_digest_and_feed(self, source: str):
        """Auto-digest stomach and feed ready items to brain."""
        # Process items in stomach that are ready (low complexity)
        items_to_brain = []
        
        for _ in range(min(self.chunks_per_cycle, len(self.stomach.stomach_queue))):
            if not self.stomach.stomach_queue:
                break
            
            task = self.stomach.stomach_queue[0]  # Peek
            
            # If complexity is low enough, it's ready for brain
            if task.complexity <= 0.2:
                task = self.stomach.stomach_queue.popleft()
                items_to_brain.append({
                    'content': task.content,
                    'nutrition': task.nutrition,
                    'ready': True
                })
                self.items_digested += 1
            else:
                # Reduce complexity (digest)
                task.complexity -= self.stomach.digestion_rate
                break  # Only process front items
        
        # Feed to brain
        for item in items_to_brain:
            self.brain.feed(item['content'], source=f"stomach_{source}")
            self.items_fed_to_brain += 1
    
    def run_full_digestion_cycle(self, source: str = "manual"):
        """Run complete digestion cycle and feed all to brain."""
        print("[Pipeline] Running full digestion cycle...")
        
        initial_stomach = len(self.stomach.stomach_queue)
        initial_brain = self.brain.tick_count
        
        # Digest until stomach is empty
        cycles = 0
        max_cycles = 50  # Safety limit
        
        while len(self.stomach.stomach_queue) > 0 and cycles < max_cycles:
            self._auto_digest_and_feed(source)
            cycles += 1
            time.sleep(0.1)  # Brief pause
        
        final_stomach = len(self.stomach.stomach_queue)
        final_brain = self.brain.tick_count
        
        return {
            "cycles": cycles,
            "items_digested": self.items_digested,
            "items_fed_to_brain": self.items_fed_to_brain,
            "stomach_remaining": final_stomach,
            "brain_ticks_gained": final_brain - initial_brain
        }
    
    def feed_dictionary(self, words: List[tuple]):
        """Feed entire dictionary through stomach → brain pipeline."""
        print(f"[Pipeline] Feeding {len(words)} words to stomach...")
        
        for i, (word, pos, definition, category) in enumerate(words):
            self.feed_to_stomach(
                data=f"{word}: {definition}",
                complexity=0.3,
                nutrition=0.5,
                source=f"dictionary_{category}"
            )
            
            if (i + 1) % 50 == 0:
                print(f"  Fed {i+1}/{len(words)} words to stomach")
        
        print(f"\n[Pipeline] Running full digestion...")
        result = self.run_full_digestion_cycle("dictionary")
        
        return result
    
    def feed_large_data(self, data: str, chunk_size: int = 500):
        """Feed large data (like periodic table) through pipeline."""
        print(f"[Pipeline] Feeding large data ({len(data)} chars)...")
        
        # Split into chunks and feed
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            self.feed_to_stomach(
                data=chunk,
                complexity=0.6,
                nutrition=0.7,
                source="large_data"
            )
        
        print(f"  Fed {len(data)//chunk_size + 1} chunks to stomach")
        
        # Digest all
        result = self.run_full_digestion_cycle("large_data")
        
        return result
    
    def get_status(self) -> Dict:
        """Get full pipeline status."""
        return {
            "stomach": {
                "queue_size": len(self.stomach.stomach_queue),
                "intestine_size": len(self.stomach.intestine_queue),
                "energy": self.stomach.energy_level,
                "state": self.stomach.get_status()
            },
            "brain": {
                "ticks": self.brain.tick_count,
                "clusters": self.brain.regions['hippocampus'].get_cluster_count()
            },
            "pipeline": {
                "fed_to_stomach": self.items_fed_to_stomach,
                "digested": self.items_digested,
                "fed_to_brain": self.items_fed_to_brain
            }
        }


def demo_stomach_brain_pipeline():
    """Demo the complete stomach-brain pipeline."""
    from agents.century_dictionary import get_20th_century_dictionary
    
    print("=" * 70)
    print("🍽️🧠 STOMACH-BRAIN AUTO-FEED PIPELINE")
    print("=" * 70)
    
    pipeline = StomachBrainPipeline()
    
    # Feed dictionary
    words = get_20th_century_dictionary()
    print(f"\nFeeding {len(words)} dictionary words...\n")
    
    result = pipeline.feed_dictionary(words)
    
    print("\n" + "=" * 70)
    print("✅ FEED COMPLETE")
    print("=" * 70)
    
    status = pipeline.get_status()
    
    print(f"\nPipeline Stats:")
    print(f"  Fed to stomach: {status['pipeline']['fed_to_stomach']}")
    print(f"  Digested: {status['pipeline']['digested']}")
    print(f"  Fed to brain: {status['pipeline']['fed_to_brain']}")
    
    print(f"\nBrain State:")
    print(f"  Ticks: {status['brain']['ticks']}")
    print(f"  Clusters: {status['brain']['clusters']}")
    
    print(f"\nStomach State:")
    print(f"  {status['stomach']['state']}")
    print(f"  Energy: {status['stomach']['energy']:.2f}")
    
    return pipeline


if __name__ == "__main__":
    demo_stomach_brain_pipeline()
