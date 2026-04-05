#!/usr/bin/env python3
"""
Auto-Feeder: Fill stomach to FULL → Auto-digest → Feed brain.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from stomach.ternary_stomach import TernaryStomach, StomachState
from brain.seven_region import SevenRegionBrain
from agents.century_dictionary import get_20th_century_dictionary


class StomachAutoFeeder:
    """
    Auto-feeder: Continuously feeds stomach until FULL, then auto-digests to brain.
    """
    
    def __init__(self):
        self.stomach = TernaryStomach()
        self.brain = SevenRegionBrain()
        
        # Stats
        self.total_fed = 0
        self.total_digested = 0
        self.total_to_brain = 0
        
        # Auto-feed settings
        self.batch_size = 5
        self.digest_cycles = 3
        
    def fill_stomach(self, words, target_state=StomachState.FULL):
        """Feed stomach until it reaches target state (FULL)."""
        print("=" * 70)
        print("🍽️ AUTO-FEEDER: FILLING STOMACH")
        print("=" * 70)
        print(f"\nTarget: Fill stomach until FULL (40+ items)")
        print(f"Available: {len(words)} words\n")
        
        fed = 0
        for i, (word, pos, definition, category) in enumerate(words):
            result = self.stomach.consume(
                item=f"{word}: {definition}",
                complexity=0.3,
                nutrition=0.5
            )
            fed += 1
            
            # Check if FULL
            if self.stomach.state == StomachState.FULL:
                print(f"\n🎉 STOMACH FULL!")
                print(f"   Items fed: {fed}")
                print(f"   Queue size: {len(self.stomach.stomach_queue)}")
                print(f"   State: {self.stomach.state.name}")
                break
            
            if (i + 1) % 10 == 0:
                print(f"  Fed {i+1} words... Stomach: {len(self.stomach.stomach_queue)} items, Energy: {self.stomach.energy_level:.2f}")
        
        self.total_fed = fed
        return fed
    
    def auto_digest_and_feed(self, max_cycles=100):
        """Auto-digest stomach and feed to brain continuously."""
        print("\n" + "=" * 70)
        print("🔄 AUTO-DIGEST → BRAIN FEED")
        print("=" * 70)
        print(f"Stomach: {len(self.stomach.stomach_queue)} items")
        print(f"Digesting automatically...\n")
        
        cycle = 0
        last_brain_ticks = self.brain.tick_count
        
        while len(self.stomach.stomach_queue) > 0 and cycle < max_cycles:
            # Digest one cycle
            self.stomach.digest()
            cycle += 1
            
            # Check for items ready to feed to brain (low complexity)
            items_for_brain = []
            temp_queue = []
            
            while self.stomach.stomach_queue:
                task = self.stomach.stomach_queue.popleft()
                
                # Reduce complexity each cycle
                task.complexity -= self.stomach.digestion_rate
                
                if task.complexity <= 0:
                    # Ready for brain
                    items_for_brain.append(task)
                else:
                    # Back to queue
                    temp_queue.append(task)
            
            # Restore undigested items
            self.stomach.stomach_queue.extend(temp_queue)
            
            # Feed ready items to brain
            for task in items_for_brain:
                self.brain.feed(task.content, source="stomach_auto")
                self.total_digested += 1
                self.total_to_brain += 1
            
            # Progress report
            if cycle % 10 == 0 or len(self.stomach.stomach_queue) == 0:
                new_ticks = self.brain.tick_count - last_brain_ticks
                print(f"  Cycle {cycle}: Stomach {len(self.stomach.stomach_queue)} items → Brain +{new_ticks} ticks")
                last_brain_ticks = self.brain.tick_count
        
        print(f"\n✅ Auto-digest complete!")
        print(f"   Cycles: {cycle}")
        print(f"   Digested to brain: {self.total_to_brain}")
        
        return cycle
    
    def run_continuous_feed(self, words, rounds=3):
        """
        Run continuous auto-feed:
        Fill → Digest → Fill → Digest → ...
        """
        print("\n" + "=" * 70)
        print("🔁 CONTINUOUS AUTO-FEED MODE")
        print("=" * 70)
        print(f"Rounds: {rounds}")
        print(f"Pattern: Fill stomach → Digest → Brain feed\n")
        
        word_idx = 0
        
        for round_num in range(1, rounds + 1):
            print(f"\n{'='*70}")
            print(f"🔄 ROUND {round_num}/{rounds}")
            print(f"{'='*70}")
            
            # Fill
            remaining = words[word_idx:]
            if not remaining:
                print("No more words to feed!")
                break
            
            fed = self.fill_stomach(remaining)
            word_idx += fed
            
            # Digest
            self.auto_digest_and_feed()
            
            # Brief pause
            time.sleep(0.5)
        
        return self.get_status()
    
    def get_status(self):
        """Get complete feeder status."""
        return {
            "fed_to_stomach": self.total_fed,
            "digested": self.total_digested,
            "fed_to_brain": self.total_to_brain,
            "stomach_queue": len(self.stomach.stomach_queue),
            "stomach_energy": self.stomach.energy_level,
            "stomach_state": self.stomach.state.name,
            "brain_ticks": self.brain.tick_count,
            "brain_clusters": self.brain.regions['hippocampus'].get_cluster_count()
        }


def demo_auto_feeder():
    """Demo the auto-feeder."""
    print("\n" + "=" * 70)
    print("🤖 STOMACH AUTO-FEEDER DEMO")
    print("=" * 70)
    print()
    
    feeder = StomachAutoFeeder()
    words = get_20th_century_dictionary()
    
    print(f"Dictionary: {len(words)} words available")
    print(f"Auto-feeder ready!\n")
    
    # Run continuous feed
    status = feeder.run_continuous_feed(words, rounds=2)
    
    # Final report
    print("\n" + "=" * 70)
    print("📊 FINAL STATUS")
    print("=" * 70)
    print(f"\nAuto-Feeder Stats:")
    print(f"  Total fed to stomach: {status['fed_to_stomach']}")
    print(f"  Total digested: {status['digested']}")
    print(f"  Total to brain: {status['fed_to_brain']}")
    print(f"\nStomach:")
    print(f"  Queue: {status['stomach_queue']} items")
    print(f"  Energy: {status['stomach_energy']:.2f}")
    print(f"  State: {status['stomach_state']}")
    print(f"\nBrain:")
    print(f"  Ticks: {status['brain_ticks']}")
    print(f"  Clusters: {status['brain_clusters']}")
    
    if status['fed_to_stomach'] == status['fed_to_brain']:
        print(f"\n✅ PERFECT AUTO-FEED: 100% digestion rate")
    
    return feeder


if __name__ == "__main__":
    demo_auto_feeder()
