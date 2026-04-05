#!/usr/bin/env python3
"""
Auto-Feeder Full: Fill stomach to FULL → Digest → Repeat until ALL data fed.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from stomach.ternary_stomach import TernaryStomach, StomachState
from brain.seven_region import SevenRegionBrain
from agents.century_dictionary import get_20th_century_dictionary


class StomachAutoFeederFull:
    """
    Complete auto-feeder: Continuously fills stomach to FULL and digests
    until ALL available data is processed.
    """
    
    def __init__(self):
        self.stomach = TernaryStomach()
        self.brain = SevenRegionBrain()
        
        # Stats
        self.total_fed = 0
        self.total_digested = 0
        self.rounds_completed = 0
        
    def feed_batch(self, words_batch):
        """Feed a batch of words until stomach is FULL or batch exhausted."""
        fed = 0
        for word_data in words_batch:
            word, pos, definition, category = word_data
            
            result = self.stomach.consume(
                item=f"{word}: {definition}",
                complexity=0.2,  # Fast digestion
                nutrition=0.5
            )
            fed += 1
            
            # Stop if FULL
            if self.stomach.state == StomachState.FULL:
                break
        
        return fed
    
    def digest_all(self):
        """Digest all items in stomach and feed to brain."""
        digested = 0
        cycle = 0
        max_cycles = 200
        
        while len(self.stomach.stomach_queue) > 0 and cycle < max_cycles:
            # Process up to 5 items per cycle
            for _ in range(min(5, len(self.stomach.stomach_queue))):
                if not self.stomach.stomach_queue:
                    break
                
                task = self.stomach.stomach_queue.popleft()
                task.complexity -= 0.3
                
                if task.complexity <= 0:
                    # Feed to brain
                    self.brain.feed(task.content, source="stomach_auto")
                    digested += 1
                else:
                    # Back to stomach
                    self.stomach.stomach_queue.append(task)
            
            cycle += 1
        
        return digested, cycle
    
    def run_until_empty(self, words):
        """
        Run auto-feeder until ALL words are processed.
        
        Pattern:
        1. Fill stomach to FULL (40+ items)
        2. Digest all to brain
        3. Repeat until no words left
        """
        print("=" * 70)
        print("🤖 STOMACH AUTO-FEEDER (FULL MODE)")
        print("=" * 70)
        print(f"Total words available: {len(words)}")
        print(f"Stomach capacity: ~40 items until FULL")
        print(f"Digestion rate: Fast (complexity -0.3 per cycle)")
        print(f"Goal: Process ALL words through stomach → brain\n")
        
        word_idx = 0
        round_num = 0
        
        while word_idx < len(words):
            round_num += 1
            remaining = words[word_idx:]
            
            print(f"\n{'='*70}")
            print(f"🔄 ROUND {round_num} | Words remaining: {len(remaining)}")
            print(f"{'='*70}")
            
            # Step 1: Fill stomach
            print(f"\n1️⃣ FILLING STOMACH...")
            fed = self.feed_batch(remaining)
            word_idx += fed
            self.total_fed += fed
            
            print(f"   ✓ Fed {fed} words")
            print(f"   ✓ Stomach: {len(self.stomach.stomach_queue)} items")
            print(f"   ✓ State: {self.stomach.state.name}")
            print(f"   ✓ Energy: {self.stomach.energy_level:.2f}")
            
            # Step 2: Digest all
            print(f"\n2️⃣ DIGESTING...")
            digested, cycles = self.digest_all()
            self.total_digested += digested
            
            print(f"   ✓ Digested {digested} items in {cycles} cycles")
            print(f"   ✓ Brain: {self.brain.tick_count} ticks")
            print(f"   ✓ Brain: {self.brain.regions['hippocampus'].get_cluster_count()} clusters")
            
            self.rounds_completed = round_num
            time.sleep(0.2)
        
        return self.get_final_report()
    
    def get_final_report(self):
        """Get final report."""
        print("\n" + "=" * 70)
        print("📊 FINAL REPORT - AUTO-FEEDER COMPLETE")
        print("=" * 70)
        
        print(f"\n📈 Performance:")
        print(f"   Rounds completed: {self.rounds_completed}")
        print(f"   Total fed to stomach: {self.total_fed}")
        print(f"   Total digested to brain: {self.total_digested}")
        
        if self.total_fed > 0:
            efficiency = (self.total_digested / self.total_fed) * 100
            print(f"   Efficiency: {efficiency:.1f}%")
        
        print(f"\n🍽️ Stomach Final State:")
        print(f"   Queue: {len(self.stomach.stomach_queue)} items")
        print(f"   Energy: {self.stomach.energy_level:.2f}")
        print(f"   State: {self.stomach.state.name}")
        
        print(f"\n🧠 Brain Final State:")
        print(f"   Ticks: {self.brain.tick_count}")
        print(f"   Clusters: {self.brain.regions['hippocampus'].get_cluster_count()}")
        
        if self.total_fed == self.total_digested and self.total_fed > 0:
            print(f"\n✅ PERFECT AUTO-FEED: 100% of {self.total_fed} words digested!")
        
        return {
            "rounds": self.rounds_completed,
            "fed": self.total_fed,
            "digested": self.total_digested,
            "efficiency": (self.total_digested / self.total_fed * 100) if self.total_fed > 0 else 0,
            "brain_ticks": self.brain.tick_count,
            "brain_clusters": self.brain.regions['hippocampus'].get_cluster_count()
        }


if __name__ == "__main__":
    feeder = StomachAutoFeederFull()
    words = get_20th_century_dictionary()
    
    result = feeder.run_until_empty(words)
    
    print(f"\n{'='*70}")
    print("✅ AUTO-FEEDER COMPLETE - ALL WORDS PROCESSED")
    print(f"{'='*70}")
