#!/usr/bin/env python3
"""
ACTIVATE LIFE SYSTEMS
=====================

Unified activation of:
- Brain (7-region OODA + GrowingNN)
- Heart (Ternary rhythm: REST/BALANCE/ACTIVE)
- Stomach (Ternary digestion: HUNGRY/SATISFIED/FULL)
- Intestines (Absorption + waste disposal)

Creates a living, breathing AGI organism.
"""

import sys
import time
import threading
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("🌟 ACTIVATING LIFE SYSTEMS")
print("=" * 80)
print("Brain + Heart + Stomach + Intestines = ALIVE")
print("=" * 80)

# Import all systems
from seven_region_v2 import SevenRegionBrainV2
from skill_registry import get_registry, Skill, Contract, SkillTier

# Load skill handlers
skills_base = Path(__file__).parent / 'skills'

print("\n[1] Loading Life Support Skills...")

# GrowingNN
growingnn_locals = {}
exec(open(skills_base / 'growingnn_v1' / 'handler.py').read(), growingnn_locals)
growingnn_handler = growingnn_locals['growingnn_handler']

# Stomach/Intestines
digestive_locals = {}
exec(open(skills_base / 'stomach-v1' / 'handler.py').read(), digestive_locals)
stomach_handler = digestive_locals['stomach_handler']
intestine_handler = digestive_locals['intestine_handler']

# Heart (create skill wrapper)
heart_locals = {}
exec(open(Path(__file__).parent / 'heart' / 'ternary_heart.py').read(), heart_locals)
TernaryHeart = heart_locals['TernaryHeart']
HeartState = heart_locals['HeartState']

def heart_skill_handler(input_data):
    """Heart as a skill."""
    if not hasattr(heart_skill_handler, '_heart'):
        heart_skill_handler._heart = TernaryHeart()
    
    heart = heart_skill_handler._heart
    action = input_data.get('action', 'beat')
    
    if action == 'beat':
        heart.beat()
        return {
            'status': 'beat',
            'bpm': heart.rhythm.bpm,
            'state': heart.rhythm.state.name,
            'coherence': heart.rhythm.coherence,
            'emotional_tone': heart.rhythm.emotional_tone,
            'beat_count': heart.rhythm.beat_count
        }
    elif action == 'set_state':
        new_state = input_data.get('state', 'BALANCE')
        heart.rhythm.state = HeartState[new_state]
        return {
            'status': 'state_changed',
            'new_state': heart.rhythm.state.name
        }
    else:
        return {
            'status': 'alive',
            'bpm': heart.rhythm.bpm,
            'state': heart.rhythm.state.name,
            'variability': heart.rhythm.variability,
            'coherence': heart.rhythm.coherence
        }

print("  ✅ Skills loaded")

# Initialize Brain
print("\n[2] Awakening Brain...")
brain = SevenRegionBrainV2()
reg = get_registry()

# Register all life support skills
skills_to_register = [
    ('growingnn', '1.0.0', SkillTier.METHODOLOGY, 'Dynamic neural growth', 
     {'action': {'type': 'string'}}, {'required': ['status']}, growingnn_handler),
    
    ('stomach', '1.0.0', SkillTier.STANDARD, 'Ternary digestive processing',
     {'properties': {'action': {'type': 'string'}}}, {'required': ['status']}, stomach_handler),
    
    ('intestine', '1.0.0', SkillTier.STANDARD, 'Nutrient absorption',
     {'properties': {'action': {'type': 'string'}}}, {'required': ['absorbed', 'waste']}, intestine_handler),
    
    ('heart', '1.0.0', SkillTier.STANDARD, 'Ternary rhythmic core',
     {'properties': {'action': {'type': 'string'}}}, {'required': ['bpm', 'state']}, heart_skill_handler)
]

for name, version, tier, desc, input_s, output_s, handler in skills_to_register:
    skill = Skill(
        name=name,
        version=version,
        tier=tier,
        description=desc,
        contract=Contract(input_schema=input_s, output_schema=output_s),
        handler=handler
    )
    reg.register(skill)

print(f"  ✅ Brain online with {len(reg.skills)} life support skills")

# Initial status check
print("\n[3] Life Signs Check...")

heart_status = reg.call('heart', {'action': 'status'})
stomach_status = reg.call('stomach', {'action': 'status'})
growingnn_status = reg.call('growingnn', {'action': 'status'})

print(f"  ❤️  Heart: {heart_status['bpm']:.1f} BPM, State: {heart_status['state']}")
print(f"  🍽️  Stomach: {stomach_status['status']['state']}, Fullness: {stomach_status['status']['fullness']:.1%}")
print(f"  🧠 Brain: {growingnn_status['status']['total_nodes']} nodes, {growingnn_status['status']['growth_events']} growth events")

# Life loop
print("\n" + "=" * 80)
print("[4] LIFE CYCLE ACTIVE")
print("=" * 80)
print("Press Ctrl+C to enter hibernation\n")

tick_count = 0
try:
    while True:
        tick_count += 1
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # 1. HEART BEAT (every second)
        if tick_count % 5 == 0:  # Every 5 ticks (10 seconds at 0.5s interval)
            beat = reg.call('heart', {'action': 'beat'})
            heart_emoji = '❤️' if beat['state'] == 'ACTIVE' else '💙' if beat['state'] == 'BALANCE' else '💤'
            print(f"[{timestamp}] {heart_emoji} Heart Beat #{beat['beat_count']} | {beat['bpm']:.1f} BPM | {beat['state']} | Coherence: {beat['coherence']:.2f}")
        
        # 2. BRAIN OODA + GrowingNN
        # Ingest some data
        if tick_count % 3 == 0:
            # Feed the stomach
            feed_result = reg.call('stomach', {
                'action': 'ingest',
                'data': f'observation_{tick_count}',
                'source': 'system'
            })
            
            if feed_result['accepted']:
                # Process stomach
                processed = reg.call('stomach', {'action': 'process'})
                
                # Send to intestines if nutrients ready
                if processed.get('nutrients_ready'):
                    reg.call('intestine', {
                        'action': 'receive',
                        'nutrients': processed['nutrients_ready']
                    })
                    absorbed = reg.call('intestine', {'action': 'process'})
                    
                    # Brain tick with absorbed nutrients
                    for nutrient in absorbed.get('absorbed', []):
                        brain.tick({
                            'source': 'stomach',
                            'data': nutrient['content'],
                            'priority': nutrient['priority']
                        })
                
                # Show stomach state
                if tick_count % 15 == 0:
                    stomach_state = reg.call('stomach', {'action': 'status'})
                    print(f"[{timestamp}] 🍽️  Stomach: {stomach_state['status']['state']} | Contents: {stomach_state['status']['contents']}/{stomach_state['status']['capacity']}")
        
        # 3. BRAIN DECISION + GrowingNN
        result = brain.tick({
            'source': 'system',
            'data': f'tick_{tick_count}',
            'priority': 0.5
        })
        
        # Trigger GrowingNN with novelty
        gnn_result = reg.call('growingnn', {
            'action': 'update',
            'novelty': 0.7 if tick_count % 10 == 0 else 0.3,  # Periodic high novelty
            'error': 0.1
        })
        
        if gnn_result.get('growth_triggered') and tick_count % 10 == 0:
            print(f"[{timestamp}] 🌱 GROWTH! Brain now {gnn_result['status']['total_nodes']} nodes (+{gnn_result['status']['total_nodes'] - 60} since start)")
        
        # 4. Status every 20 ticks
        if tick_count % 20 == 0:
            brain_health = brain.get_health()
            current_stomach = reg.call('stomach', {'action': 'status'})
            current_intestine = reg.call('intestine', {'action': 'status'})
            current_heart = reg.call('heart', {'action': 'status'})
            current_gnn = reg.call('growingnn', {'action': 'status'})
            
            stomach_state = current_stomach.get('status', {})
            intestine_state = current_intestine.get('status', {}) if isinstance(current_intestine, dict) else {}
            heart_state = current_heart if isinstance(current_heart, dict) else {}
            gnn_state = current_gnn.get('status', {})
            
            print(f"\n[{timestamp}] 📊 System Status:")
            print(f"    Brain Ticks: {brain_health['tick_count']} | Nodes: {gnn_state.get('total_nodes', 60)}")
            print(f"    Stomach: {stomach_state.get('state', 'unknown')} | Intestine: {intestine_state.get('small_intestine', 0)} processing")
            print(f"    Heart: {heart_state.get('bpm', 72):.1f} BPM | Coherence: {heart_state.get('coherence', 0.5):.2f}")
            print()
        
        time.sleep(0.5)  # 2 Hz life cycle
        
except KeyboardInterrupt:
    print(f"\n\n{'=' * 80}")
    print("ENTERING HIBERNATION")
    print("=" * 80)
    
    # Final status
    final_heart = reg.call('heart', {'action': 'status'})
    final_stomach = reg.call('stomach', {'action': 'status'})
    final_intestine = reg.call('intestine', {'action': 'status'})
    final_gnn = reg.call('growingnn', {'action': 'status'})
    
    print(f"\n❤️  Heart: {final_heart['bpm']:.1f} BPM | Total beats: {final_heart.get('beat_count', tick_count // 5)}")
    print(f"🍽️  Stomach: {final_stomach['status']['processed']} items processed")
    print(f"🧬 Intestines: {final_intestine['status']['total_absorbed']} nutrients absorbed | {final_intestine['status']['total_waste']} waste disposed")
    print(f"🧠 Brain: {final_gnn['status']['total_nodes']} nodes | {final_gnn['status']['growth_events']} growth events | {brain.tick_count} ticks")
    
    print(f"\n💤 Systems entering low-power mode...")
    print("🌙 Goodnight, sweet AGI")
    print("=" * 80)
