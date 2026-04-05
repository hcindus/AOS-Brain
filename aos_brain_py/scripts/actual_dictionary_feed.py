#!/usr/bin/env python3
"""
ACTUAL Dictionary Feed - Load 20th Century Dictionary into Brain.

This is NOT a simulation - it actually feeds the dictionary to the brain.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from brain.seven_region import SevenRegionBrain
from agents.century_dictionary import get_20th_century_dictionary


def feed_dictionary_to_brain():
    """Actually feed the dictionary to the brain."""
    print("=" * 70)
    print("📚 LOADING 20TH CENTURY DICTIONARY INTO BRAIN")
    print("=" * 70)
    print()
    
    # Create brain
    brain = SevenRegionBrain()
    
    # Get dictionary
    words = get_20th_century_dictionary()
    print(f"Dictionary size: {len(words)} words")
    print()
    
    # Feed all words
    print("Feeding words to brain...")
    for i, word_data in enumerate(words):
        word, pos, definition, category = word_data
        
        # Feed to brain
        brain.feed(
            f"[DICTIONARY] {word} ({pos}): {definition}",
            source=f"century_{category}"
        )
        
        if (i + 1) % 50 == 0:
            print(f"  Progress: {i+1}/{len(words)} words fed")
    
    print()
    print("=" * 70)
    print("✅ DICTIONARY LOADED")
    print("=" * 70)
    
    # Report actual state
    hippo = brain.regions['hippocampus']
    print(f"\nBrain Memory State:")
    print(f"  Total ticks: {brain.tick_count}")
    print(f"  Hippocampal clusters: {hippo.get_cluster_count()}")
    print(f"  Episodic buffer: {len(hippo.episodic_buffer)} experiences")
    print(f"  Brain mode: {brain.current_mode}")
    
    # Save state
    state_file = Path.home() / ".aos" / "brain" / "state" / "dictionary_loaded.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    
    import json
    with open(state_file, 'w') as f:
        json.dump({
            "dictionary_size": len(words),
            "brain_ticks": brain.tick_count,
            "hippocampal_clusters": hippo.get_cluster_count(),
            "timestamp": __import__('time').time(),
            "status": "loaded"
        }, f, indent=2)
    
    print(f"\nState saved to: {state_file}")
    print("=" * 70)
    
    return brain


if __name__ == "__main__":
    brain = feed_dictionary_to_brain()
