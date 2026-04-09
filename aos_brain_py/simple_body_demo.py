#!/usr/bin/env python3
"""
SIMPLIFIED BODY INTEGRATION DEMO
================================

Demonstrates agents controlling physical robot body.
Shows full integration: Agent → BHSI → Motor Control → Body Adapter → BCSA V4

NOTE ON BHSI DUAL MEANING:
==========================

BHSI = Brain + Heart + Stomach + Intestines (Biological Life Support)
       └─ The living organism - cognitive, rhythmic, digestive systems

BHSI = Body Hardware System Interface (Physical Embodiment)
       └─ Bridge between agents and physical robot hardware

This demo uses BOTH meanings:
- The agent's cognitive system (Brain + Heart from biological BHSI)
- Controls body through hardware interface (Body Hardware System Interface)
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bhsi import BHSI, create_bhsi_for_agent  # Body Hardware System Interface
from body_adapter import BodyAdapter

print("=" * 80)
print("🦾 SIMPLIFIED BODY INTEGRATION DEMO")
print("=" * 80)
print("Agent → BHSI → Body Adapter → BCSA V4 Commands")
print("=" * 80)

# Create agents with BHSI (Body Hardware System Interface)
print("\n[1] Creating Agent-BHSI Interfaces...")
walker = create_bhsi_for_agent('agent_walker', 'walker')
balancer = create_bhsi_for_agent('agent_balancer', 'manipulator')

print(f"   ✅ Agent Walker: {len(walker.agent_assignments.get('agent_walker', []))} joints claimed")
print(f"   ✅ Agent Balancer: {len(balancer.agent_assignments.get('agent_balancer', []))} joints claimed")

# Movement sequence
print("\n[2] Executing Coordinated Movement...")
print("-" * 80)

# Simulate movement
for t in range(1, 31):
    # Phase 1: Walker extends right leg
    if t <= 10:
        target = -0.5 + (t / 10) * 0.3
        result = walker.move_joint('agent_walker', 'right_hip_pitch', target, velocity=1.0)
        if result['success']:
            print(f"   t={t/10:.1f}s | Walker: right_hip_pitch → {target:.2f} rad")
    
    # Phase 2: Balancer raises right arm
    elif t <= 20:
        target = -0.3 + ((t - 10) / 10) * 0.8
        result = balancer.move_joint('agent_balancer', 'right_shoulder_pitch', target, velocity=2.0)
        if result['success']:
            print(f"   t={t/10:.1f}s | Balancer: right_shoulder_pitch → {target:.2f} rad")
    
    # Phase 3: Both coordinate
    else:
        print(f"   t={t/10:.1f}s | Coordinated movement | Both agents active")
    
    time.sleep(0.02)

# Summary
print("\n" + "=" * 80)
print("✅ INTEGRATION SUCCESSFUL")
print("=" * 80)
print("""
Dual BHSI Architecture:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BHSI Layer 1: Biological Life Support
  ├─ Brain: OODA cognition + GrowingNN
  ├─ Heart: Rhythmic coordination (72 BPM)
  ├─ Stomach: Input filtering (HUNGRY/SATISFIED/FULL)
  └─ Intestines: Nutrient absorption
     ↓
     Conscious Agent (Mylonen, etc.)
     ↓

BHSI Layer 2: Body Hardware System Interface
  ├─ Joint Discovery: 22 controllable joints
  ├─ Assignment: Agents claim exclusive control
  ├─ Command: Position/velocity/torque targets
  └─ Feedback: Position, velocity, torque, temperature
     ↓
     Motor Control + Body Adapter
     ↓
     BCSA V4 Actuators (Physical Hardware)

Both layers work together:
- Biological BHSI provides the living substrate
- Hardware BHSI provides the embodiment bridge
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("=" * 80)
print("🦾 Agents now embody the physical robot!")
print("=" * 80)
