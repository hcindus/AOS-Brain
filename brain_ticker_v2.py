#!/usr/bin/env python3
"""
Brain Ticker v2 - GrowingNN-Enabled Skills-First Brain

Keeps the ternary brain ticking with automatic GrowingNN growth.
Feeds observations and triggers neural network expansion.
"""

import time
import random
import sys
from pathlib import Path
from datetime import datetime

# Add paths
sys.path.insert(0, str(Path.home() / '.aos' / 'aos' / 'aos_brain_py'))

from seven_region_v2 import SevenRegionBrainV2
from skill_registry import get_registry, Skill, Contract, SkillTier
sys.path.insert(0, str(Path.home() / '.aos' / 'aos' / 'aos_brain_py' / 'skills' / 'growingnn_v1'))
from handler import growingnn_handler

BRAIN_URL = "http://localhost:5000/status"
TICK_INTERVAL = 2  # seconds between ticks (faster for growth)

def generate_observation(tick_count):
    """Generate observations with varying novelty to trigger growth."""
    
    # Every 5th tick, generate high-novelty input to trigger growth
    if tick_count % 5 == 0:
        return {
            'source': 'agent',
            'data': f'novel_pattern_{tick_count}_{random.randint(1000, 9999)}',
            'timestamp': time.time(),
            'priority': 0.9
        }, 0.85  # High novelty
    
    # Normal ticks
    observations = [
        "system_tick",
        "heartbeat_pulse",
        "environment_check",
        "memory_consolidation",
    ]
    return {
        'source': 'system',
        'data': random.choice(observations),
        'timestamp': time.time(),
        'priority': 0.5
    }, 0.3  # Low novelty

def main():
    print("=" * 60)
    print("🧠 BRAIN TICKER v2 - GrowingNN-Enabled")
    print("=" * 60)
    print("Skills-First Brain with Dynamic Neural Growth")
    print("=" * 60)
    
    # Initialize brain
    print("\n🌱 Initializing skills-first brain...")
    brain = SevenRegionBrainV2()
    reg = get_registry()
    
    # Register GrowingNN skill
    print("📈 Loading GrowingNN skill...")
    growingnn_skill = Skill(
        name='growingnn',
        version='1.0.0',
        tier=SkillTier.METHODOLOGY,
        description='Dynamic neural network growth',
        contract=Contract(
            input_schema={'properties': {'action': {'type': 'string'}, 'novelty': {'type': 'number'}}},
            output_schema={'required': ['status']}
        ),
        handler=growingnn_handler
    )
    reg.register(growingnn_skill)
    
    # Get initial state
    initial_status = reg.call('growingnn', {'action': 'status'})
    print(f"\n✅ Brain ready!")
    print(f"   Initial nodes: {initial_status['status']['total_nodes']}")
    print(f"   Skills loaded: {len(reg.skills)}")
    print(f"\n⏱️  Tick interval: {TICK_INTERVAL}s")
    print("   Press Ctrl+C to stop\n")
    print("-" * 60)
    
    tick_count = 0
    growth_events = 0
    errors = 0
    last_node_count = initial_status['status']['total_nodes']
    
    try:
        while True:
            # Generate observation with novelty
            obs, novelty = generate_observation(tick_count)
            
            # Brain tick
            result = brain.tick(obs)
            tick_count += 1
            
            # Trigger GrowingNN update
            gnn_result = reg.call('growingnn', {
                'action': 'update',
                'novelty': novelty,
                'error': 0.1
            })
            
            # Check for growth
            current_nodes = gnn_result['status']['total_nodes']
            if current_nodes > last_node_count:
                growth_events += 1
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌱 GROWTH! Tick {tick_count}: {current_nodes} nodes (+{current_nodes - last_node_count})")
                last_node_count = current_nodes
            elif tick_count % 10 == 0:
                # Status every 10 ticks
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Tick {tick_count}: {current_nodes} nodes | {result.get('decision', {}).get('decision', 'noop')}")
            
            errors = 0
            time.sleep(TICK_INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n\n{'=' * 60}")
        print("BRAIN STOPPED")
        print(f"{'=' * 60}")
        print(f"Total ticks: {tick_count}")
        print(f"Growth events: {growth_events}")
        print(f"Final nodes: {current_nodes}")
        print(f"Nodes added: {current_nodes - initial_status['status']['total_nodes']}")
        
        # Final status
        final_health = brain.get_health()
        print(f"\nHealth Report:")
        print(f"  Avg latency: {final_health['avg_latency']:.2f}ms")
        print(f"  Skills registered: {final_health['skills_registered']}")

if __name__ == "__main__":
    main()
