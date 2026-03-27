#!/usr/bin/env python3
"""
Simple Knowledge Feed - Feed dictionary directly without complex stomach processing.
"""

import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Simple feed - no stomach, direct to brain
print("Loading...")
sys.stdout.flush()

from brain.seven_region import SevenRegionBrain
from agents.century_dictionary import get_20th_century_dictionary

print("Systems loaded")
sys.stdout.flush()

brain = SevenRegionBrain()
words = get_20th_century_dictionary()

print(f"\nFeeding {len(words)} words to brain...")
sys.stdout.flush()

for i, (word, pos, definition, category) in enumerate(words):
    brain.feed(f"{word}: {definition}", source=f"century_{category}")
    
    if (i + 1) % 50 == 0:
        print(f"  {i+1}/{len(words)} words fed")
        sys.stdout.flush()

hippo = brain.regions['hippocampus']

print(f"\n✅ COMPLETE")
print(f"Brain ticks: {brain.tick_count}")
print(f"Hippocampal clusters: {hippo.get_cluster_count()}")

# Save state
state_file = Path.home() / ".aos" / "brain" / "state" / "knowledge_loaded.json"
state_file.parent.mkdir(parents=True, exist_ok=True)

with open(state_file, 'w') as f:
    json.dump({
        "dictionary_size": len(words),
        "brain_ticks": brain.tick_count,
        "hippocampal_clusters": hippo.get_cluster_count(),
        "timestamp": time.time(),
        "status": "LOADED"
    }, f, indent=2)

print(f"Saved to: {state_file}")
