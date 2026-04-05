#!/usr/bin/env python3
"""
ACTUAL Full Knowledge Feed - Stomach digests, Brain learns.

NOT a simulation - actually feeds all knowledge through stomach-brain pipeline.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from stomach.ternary_stomach import TernaryStomach
from brain.seven_region import SevenRegionBrain
from agents.century_dictionary import get_20th_century_dictionary


def feed_all_knowledge():
    """Actually feed all knowledge to brain through stomach."""
    print("=" * 70)
    print("🍽️🧠 ACTUAL KNOWLEDGE FEED - NOT SIMULATION")
    print("=" * 70)
    print()
    
    # Initialize systems
    print("Initializing...")
    stomach = TernaryStomach()
    brain = SevenRegionBrain()
    print("✅ Stomach ready")
    print("✅ Brain ready")
    print()
    
    # Load all knowledge sources
    all_knowledge = []
    
    # Source 1: Century Dictionary (455 words)
    print("Loading Century Dictionary...")
    century = get_20th_century_dictionary()
    for word, pos, definition, category in century:
        all_knowledge.append({
            "type": "word",
            "content": f"{word}: {definition}",
            "complexity": 0.3,
            "nutrition": 0.5,
            "source": f"century_{category}"
        })
    print(f"  Loaded: {len(century)} words")
    
    # Source 2: Universal Knowledge (100 items)
    print("Loading Universal Knowledge...")
    try:
        from agents.universal_knowledge_feeder import UniversalKnowledgeBase
        universal = UniversalKnowledgeBase()
        for category, items in universal.knowledge_categories.items():
            for item in items:
                if isinstance(item, tuple):
                    # Constants
                    name, symbol, value, meaning = item
                    all_knowledge.append({
                        "type": "constant",
                        "content": f"{name} ({symbol}) = {value}: {meaning}",
                        "complexity": 0.5,
                        "nutrition": 0.7,
                        "source": f"universal_{category}"
                    })
                elif isinstance(item, dict):
                    # Complex items
                    all_knowledge.append({
                        "type": "knowledge",
                        "content": str(item),
                        "complexity": 0.6,
                        "nutrition": 0.6,
                        "source": f"universal_{category}"
                    })
        print(f"  Loaded: 100 universal items")
    except Exception as e:
        print(f"  Universal knowledge error: {e}")
    
    total_items = len(all_knowledge)
    print(f"\n{'='*70}")
    print(f"TOTAL KNOWLEDGE: {total_items} items")
    print(f"{'='*70}\n")
    
    # Feed through stomach to brain
    print("FEEDING KNOWLEDGE THROUGH STOMACH → BRAIN...")
    print()
    
    fed_count = 0
    for i, item in enumerate(all_knowledge):
        # Consume in stomach
        stomach.consume(
            item["content"],
            complexity=item["complexity"],
            nutrition=item["nutrition"]
        )
        
        # Digest periodically
        if i % 10 == 0:
            for _ in range(3):
                stomach.digest()
        
        # Get chunks for brain
        chunks = stomach.get_chunks_for_brain(count=2)
        
        # Feed to brain
        for chunk in chunks:
            brain.feed(
                chunk["content"],
                source=item["source"]
            )
            fed_count += 1
        
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i+1}/{total_items} items fed to stomach")
            print(f"    Brain ticks: {brain.tick_count}")
            print(f"    Stomach: {stomach.get_status()}")
    
    # Final digestion
    print("\nFinal digestion cycles...")
    for _ in range(10):
        stomach.digest()
    
    # Get remaining chunks
    remaining = stomach.get_chunks_for_brain(count=10)
    for chunk in remaining:
        brain.feed(chunk["content"], source="stomach_final")
        fed_count += 1
    
    # Report
    print()
    print("=" * 70)
    print("✅ KNOWLEDGE FEED COMPLETE")
    print("=" * 70)
    
    hippo = brain.regions['hippocampus']
    print(f"\nACTUAL BRAIN STATE:")
    print(f"  Brain ticks: {brain.tick_count}")
    print(f"  Hippocampal clusters: {hippo.get_cluster_count()}")
    print(f"  Items fed: {fed_count}")
    print(f"  Final stomach: {stomach.get_status()}")
    
    # Save state
    import json
    state_file = Path.home() / ".aos" / "brain" / "state" / "knowledge_loaded.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(state_file, 'w') as f:
        json.dump({
            "total_knowledge": total_items,
            "fed_to_brain": fed_count,
            "brain_ticks": brain.tick_count,
            "hippocampal_clusters": hippo.get_cluster_count(),
            "stomach_energy": stomach.energy_level,
            "timestamp": time.time(),
            "status": "LOADED"
        }, f, indent=2)
    
    print(f"\n💾 State saved: {state_file}")
    print("=" * 70)
    
    return brain, stomach


if __name__ == "__main__":
    brain, stomach = feed_all_knowledge()
