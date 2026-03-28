#!/usr/bin/env python3
"""
Auto-Feeder v2: Fill stomach to FULL → Digest all → Feed brain.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from stomach.ternary_stomach import TernaryStomach, StomachState
from brain.seven_region import SevenRegionBrain
from agents.century_dictionary import get_20th_century_dictionary


class StomachAutoFeederV2:
    """
    Auto-feeder: Fill stomach to FULL, then digest everything to brain.
    """
    
    def __init__(self):
        self.stomach = TernaryStomach()
        self.brain = SevenRegionBrain()
        
        # Stats
        self.total_fed = 0
        self.total_digested = 0
        
    def feed_until_full(self, words):
        """Feed words until stomach is FULL."""
        print("🍽️ Feeding stomach until FULL...")
        
        fed = 0
        for word, pos, definition, category in words:
            self.stomach.consume(
                item=f"{word}: {definition}",
                complexity=0.2,  # Low complexity for faster digestion
                nutrition=0.5
            )
            fed += 1
            
            if self.stomach.state == StomachState.FULL:
                print(f"   ✓ Stomach FULL after {fed} words")
                break
        
        self.total_fed += fed
        return fed
    
    def digest_all(self):
        """Digest all items in stomach and feed to brain."""
        print("🔄 Digesting all items...")
        
        digested_count = 0
        cycle = 0
        
        while len(self.stomach.stomach_queue) > 0 and cycle < 200:
            # Get current batch from stomach
            batch = []
            for _ in range(min(5, len(self.stomach.stomach_queue))):
                if self.stomach.stomach_queue:
                    task = self.stomach.stomach_queue.popleft()
                    batch.append(task)
            
            # Process batch: reduce complexity
            for task in batch:
                task.complexity -= 0.3  # Fast digestion
                
                if task.complexity <= 0:
                    # Ready for brain - feed immediately
                    self.brain.feed(task.content, source="stomach_auto")
                    digested_count += 1
                else:
                    # Not ready - back to stomach
                    self.stomach.stomach_queue.append(task)
            
            cycle += 1
            
            if cycle % 20 == 0:
                print(f"   Cycle {cycle}: {len(self.stomach.stomach_queue)} items remaining, {digested_count} to brain")
        
        self.total_digested += digested_count
        print(f"   ✓ Digested {digested_count} items in {cycle} cycles")
        return digested_count
    
    def run(self, words, rounds=3):
        """Run auto-feeder for multiple rounds."""
        print("=" * 70)
        print("🤖 STOMACH AUTO-FEEDER v2")
        print("=" * 70)
        print(f"Dictionary: {len(words)} words")
        print(f"Rounds: {rounds}")
        print(f"Pattern: Fill to FULL → Digest all → Feed brain\n")
        
        word_idx = 0
        
        for round_num in range(1, rounds + 1):
            print(f"\n{'='*70}")
            print(f"🔄 ROUND {round_num}/{rounds}")
            print(f"{'='*70}")
            
            remaining = words[word_idx:]
            if not remaining:
                print("No more words!")
                break
            
            # Fill
            fed = self.feed_until_full(remaining)
            word_idx += fed
            
            # Digest all
            self.digest_all()
            
            print(f"\n   Round {round_num} complete!")
            print(f"   Stomach: {len(self.stomach.stomach_queue)} items remaining")
            print(f"   Brain: {self.brain.tick_count} ticks, {self.brain.regions['hippocampus'].get_cluster_count()} clusters")
            
            time.sleep(0.3)
        
        return self.get_final_report()
    
    def get_final_report(self):
        """Get final status report."""
        print("\n" + "=" * 70)
        print("📊 FINAL REPORT")
        print("=" * 70)
        
        print(f"\nAuto-Feeder Performance:")
        print(f"  Total fed to stomach: {self.total_fed}")
        print(f"  Total digested to brain: {self.total_digested}")
        print(f"  Efficiency: {(self.total_digested/self.total_fed*100):.1f}%" if self.total_fed > 0 else "  N/A")
        
        print(f"\nStomach Status:")
        print(f"  Queue: {len(self.stomach.stomach_queue)} items")
        print(f"  Energy: {self.stomach.energy_level:.2f}")
        print(f"  State: {self.stomach.state.name}")
        
        print(f"\nBrain Status:")
        print(f"  Ticks: {self.brain.tick_count}")
        print(f"  Clusters: {self.brain.regions['hippocampus'].get_cluster_count()}")
        
        if self.total_fed == self.total_digested and self.total_fed > 0:
            print(f"\n✅ PERFECT AUTO-FEED: 100% digestion!")
        
        return {
            "fed": self.total_fed,
            "digested": self.total_digested,
            "brain_ticks": self.brain.tick_count,
            "brain_clusters": self.brain.regions['hippocampus'].get_cluster_count(),
            "stomach_remaining": len(self.stomach.stomach_queue)
        }


if __name__ == "__main__":
    feeder = StomachAutoFeederV2()
    words = get_20th_century_dictionary()
    feeder.run(words, rounds=3)
