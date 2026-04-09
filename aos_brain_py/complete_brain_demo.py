#!/usr/bin/env python3
"""
Complete Brain-Body Integration Demo

Shows the full stack:
1. Brain decides to move (Cerebellum/OODA)
2. Motor control skill calculates kinematics
3. BCSA V4 commands generated
4. Robot executes movement
5. GrowingNN grows during learning
"""

import sys
import time
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from seven_region_v2 import SevenRegionBrainV2
from skill_registry import get_registry, Skill, Contract, SkillTier

print("=" * 80)
print("🧠 COMPLETE BRAIN-BODY INTEGRATION DEMO")
print("=" * 80)
print("Skills-First Brain + GrowingNN + Motor Control + BCSA V4 Actuators")
print("=" * 80)

# Initialize brain
print("\n[1] Initializing Brain...")
brain = SevenRegionBrainV2()
reg = get_registry()

# Load and register all skills
print("[2] Loading Skills...")
skills_base = Path(__file__).parent / 'skills'

# GrowingNN
growingnn_locals = {}
exec(open(skills_base / 'growingnn_v1' / 'handler.py').read(), growingnn_locals)
growingnn_skill = Skill(
    name='growingnn',
    version='1.0.0',
    tier=SkillTier.METHODOLOGY,
    description='Dynamic neural growth',
    contract=Contract(
        input_schema={'properties': {'action': {'type': 'string'}, 'novelty': {'type': 'number'}}},
        output_schema={'required': ['status']}
    ),
    handler=growingnn_locals['growingnn_handler']
)
reg.register(growingnn_skill)

# Motor Control
motor_locals = {}
exec(open(skills_base / 'motor_control_v1' / 'handler.py').read(), motor_locals)
motor_skill = Skill(
    name='motor-control',
    version='1.0.0',
    tier=SkillTier.METHODOLOGY,
    description='Brain-to-body interface',
    contract=Contract(
        input_schema={'properties': {'action': {'type': 'string'}}},
        output_schema={'required': ['success', 'body_state']}
    ),
    handler=motor_locals['motor_control_handler']
)
reg.register(motor_skill)

print(f"    ✅ {len(reg.skills)} skills registered")

# Initial state
print("\n[3] Initial State:")
initial_gnn = reg.call('growingnn', {'action': 'status'})
print(f"    Brain nodes: {initial_gnn['status']['total_nodes']}")
print(f"    Joints: 20 (AOS-H1 humanoid)")

# Demo: Brain decides to wave
print("\n[4] Brain Decision: Wave Right Hand")
print("-" * 80)

for tick in range(1, 6):
    print(f"\n--- Tick {tick} ---")
    
    # 1. Brain OODA
    obs = {
        'source': 'user',
        'data': f'Wave hand, tick {tick}',
        'priority': 0.8
    }
    result = brain.tick(obs)
    print(f"Brain: {result['decision']['decision']} ({result['decision']['mode']})")
    
    # 2. Trigger GrowingNN (high novelty while learning)
    gnn_result = reg.call('growingnn', {
        'action': 'update',
        'novelty': 0.85 if tick < 4 else 0.3,  # High novelty initially
        'error': 0.1
    })
    
    if gnn_result.get('growth_triggered'):
        print(f"🌱 GrowingNN: GROWTH! Now {gnn_result['status']['total_nodes']} nodes")
    
    # 3. Motor Control: Calculate wave trajectory
    # Wave = sinusoidal motion
    angle = math.sin(tick * 0.5) * 0.5  # -0.5 to 0.5 rad
    
    motor_result = reg.call('motor-control', {
        'action': 'set_joint',
        'joint': 'right_shoulder_pitch',
        'joint_position': angle,
        'velocity': 1.0
    })
    
    if motor_result['success']:
        shoulder = motor_result['body_state']['joints']['right_shoulder_pitch']
        print(f"Motor: Right shoulder → {math.degrees(shoulder['target_position']):.1f}°")
    
    # 4. Generate BCSA V4 commands
    update_result = reg.call('motor-control', {'action': 'update'})
    if update_result['success']:
        cmd_count = update_result['command_count']
        print(f"BCSA V4: {cmd_count} actuator commands generated")

# Final state
print("\n" + "=" * 80)
print("[5] Final State:")
final_gnn = reg.call('growingnn', {'action': 'status'})
final_motor = reg.call('motor-control', {'action': 'status'})

print(f"    Brain nodes: {final_gnn['status']['total_nodes']} "
      f"(+{final_gnn['status']['total_nodes'] - initial_gnn['status']['total_nodes']})")
print(f"    Growth events: {final_gnn['status']['growth_events']}")
print(f"    Brain ticks: {brain.tick_count}")
print(f"    Commands sent: {final_motor['body_state']['commands_sent']}")

# Sample joint positions
print("\n[6] Joint Positions (sample):")
for joint_name in ['right_shoulder_pitch', 'right_elbow_pitch', 'neck_yaw']:
    joint = final_motor['body_state']['joints'][joint_name]
    print(f"    {joint_name}: {math.degrees(joint['position']):.1f}° "
          f"(target: {math.degrees(joint['target_position']):.1f}°)")

print("\n" + "=" * 80)
print("✅ DEMO COMPLETE")
print("=" * 80)
print("""
Integration Stack:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 Brain (Cerebellum/OODA)
   └─ Decides: "Wave hand"
   
📈 GrowingNN Skill
   └─ Grows network while learning (novelty > 0.8)
   
🤖 Motor Control Skill
   └─ Calculates: Inverse kinematics
   └─ Controls: 20 joints
   
⚙️ BCSA V4 Actuators
   └─ Executes: Torque/velocity commands
   └─ Precision: ≤10 arcmin backlash
   
🦾 AOS-H1 Robot Body
   └─ Moves: Right arm waves
   
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# Save integration report
report = {
    'timestamp': time.time(),
    'skills': len(reg.skills),
    'brain_ticks': brain.tick_count,
    'nodes_start': initial_gnn['status']['total_nodes'],
    'nodes_end': final_gnn['status']['total_nodes'],
    'growth_events': final_gnn['status']['growth_events'],
    'joints_controlled': len(final_motor['body_state']['joints']),
    'commands_generated': final_motor['body_state']['commands_sent'],
    'status': 'complete'
}

report_path = Path.home() / '.aos' / 'brain' / 'integration_demo_report.json'
report_path.parent.mkdir(parents=True, exist_ok=True)
import json
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)

print(f"📄 Report saved: {report_path}")
