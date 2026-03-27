#!/usr/bin/env python3
"""Batch feed dictionary in chunks to avoid hanging."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain
from agents.century_dictionary import get_20th_century_dictionary
import json

print("="*70)
print("BATCH FEEDING DICTIONARY")
print("="*70)

brain = SevenRegionBrain()
words = get_20th_century_dictionary()

print(f"Total words: {len(words)}")
print(f"Brain ticks: {brain.tick_count}")
print()

# Feed in batches of 50
batch_size = 50
total_batches = (len(words) + batch_size - 1) // batch_size

for batch_num in range(total_batches):
    start_idx = batch_num * batch_size
    end_idx = min(start_idx + batch_size, len(words))
    
    print(f"Batch {batch_num+1}/{total_batches} (words {start_idx+1}-{end_idx})...")
    
    for i in range(start_idx, end_idx):
        word, pos, definition, category = words[i]
        brain.feed(f"{word}: {definition}", f"century_{category}")
    
    hippo = brain.regions['hippocampus']
    print(f"  Complete: {brain.tick_count} ticks, {hippo.get_cluster_count()} clusters")
    time.sleep(0.5)  # Brief pause between batches

# Save final state
state_file = Path.home() / ".aos" / "brain" / "state" / "knowledge_loaded.json"
state_file.parent.mkdir(parents=True, exist_ok=True)

hippo = brain.regions['hippocampus']
with open(state_file, 'w') as f:
    json.dump({
        'dictionary_size': len(words),
        'brain_ticks': brain.tick_count,
        'hippocampal_clusters': hippo.get_cluster_count(),
        'timestamp': time.time(),
        'status': 'LOADED'
    }, f, indent=2)

print()
print("="*70)
print("✅ COMPLETE")
print(f"Fed {len(words)} words")
print(f"Brain: {brain.tick_count} ticks, {hippo.get_cluster_count()} clusters")
print(f"Saved to: {state_file}")
print("="*70)
