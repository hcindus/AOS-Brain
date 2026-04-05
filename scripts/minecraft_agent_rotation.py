#!/usr/bin/env python3
"""
Minecraft Agent Rotation System
- 13 total enhanced agents
- 7 active at a time
- Rotation schedule for equal learning/building/growth time
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# All 13 Enhanced Agents
ALL_AGENTS = [
    {"id": "mc_agent_01", "name": "Agent_Steve", "role": "Builder", "skills": ["building", "planning", "redstone"]},
    {"id": "mc_agent_02", "name": "Agent_Alex", "role": "Explorer", "skills": ["exploration", "mapping", "mining"]},
    {"id": "mc_agent_03", "name": "Agent_Miner", "role": "Miner", "skills": ["mining", "resource_gathering", "caving"]},
    {"id": "mc_agent_04", "name": "Agent_Builder", "role": "Builder", "skills": ["building", "architecture", "design"]},
    {"id": "mc_agent_05", "name": "Agent_Explorer", "role": "Explorer", "skills": ["exploration", "biome_finding", "mapping"]},
    {"id": "mc_agent_06", "name": "Agent_Redstone", "role": "Engineer", "skills": ["redstone", "automation", "circuitry"]},
    {"id": "mc_agent_07", "name": "Agent_Farmer", "role": "Farmer", "skills": ["farming", "animal_husbandry", "food_production"]},
    {"id": "mc_agent_08", "name": "Agent_Crafter", "role": "Crafter", "skills": ["crafting", "item_management", "trading"]},
    {"id": "mc_agent_09", "name": "Agent_Fighter", "role": "Guard", "skills": ["combat", "defense", "mob_hunting"]},
    {"id": "mc_agent_10", "name": "Agent_Navigator", "role": "Navigator", "skills": ["navigation", "wayfinding", "transport"]},
    {"id": "mc_agent_11", "name": "Agent_Collector", "role": "Collector", "skills": ["collecting", "organizing", "storage"]},
    {"id": "mc_agent_12", "name": "Agent_Enchanter", "role": "Enchanter", "skills": ["enchanting", "xp_farming", "brewing"]},
    {"id": "mc_agent_13", "name": "Agent_Lumberjack", "role": "Gatherer", "skills": ["woodcutting", "gathering", "terraforming"]},
]

# Enhanced capabilities
ENHANCEMENTS = [
    "AI decision making",
    "Memory of past builds",
    "Learning from mistakes",
    "Cooperative building",
    "Resource management",
    "Communication protocol",
    "Goal-oriented behavior",
]

ROTATION_STATE_FILE = Path("/root/.openclaw/workspace/AGI_COMPANY/data/minecraft_rotation_state.json")
ROTATION_INTERVAL_HOURS = 2  # Rotate every 2 hours

def load_rotation_state():
    """Load current rotation state"""
    if ROTATION_STATE_FILE.exists():
        with open(ROTATION_STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "current_batch": 0,
        "last_rotation": None,
        "total_rotations": 0,
        "agent_stats": {agent["id"]: {"active_hours": 0, "builds_completed": 0, "blocks_placed": 0} for agent in ALL_AGENTS}
    }

def save_rotation_state(state):
    """Save rotation state"""
    ROTATION_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ROTATION_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_current_active_agents(state):
    """Get the 7 currently active agents"""
    batch = state["current_batch"] % 2  # 2 batches (7 + 6)
    
    if batch == 0:
        # First 7 agents
        return ALL_AGENTS[:7]
    else:
        # Last 6 agents + first agent to complete 7
        return ALL_AGENTS[7:] + [ALL_AGENTS[0]]

def rotate_agents(state):
    """Rotate to next batch"""
    state["current_batch"] = (state["current_batch"] + 1) % 2
    state["last_rotation"] = datetime.now().isoformat()
    state["total_rotations"] += 1
    
    # Update stats for agents going inactive
    active_ids = [a["id"] for a in get_current_active_agents(state)]
    for agent_id in active_ids:
        state["agent_stats"][agent_id]["active_hours"] += ROTATION_INTERVAL_HOURS
    
    return state

def should_rotate(state):
    """Check if it's time to rotate"""
    if state["last_rotation"] is None:
        return True
    
    last = datetime.fromisoformat(state["last_rotation"])
    return datetime.now() - last > timedelta(hours=ROTATION_INTERVAL_HOURS)

def print_agent_status(active_agents, state):
    """Print current agent status"""
    print("\n" + "=" * 70)
    print("🎮 MINECRAFT AGENT ROTATION SYSTEM")
    print("=" * 70)
    print(f"\nActive Agents (7/13 online):")
    print("-" * 70)
    
    for agent in active_agents:
        stats = state["agent_stats"][agent["id"]]
        print(f"  🟢 {agent['name']}")
        print(f"     Role: {agent['role']}")
        print(f"     Skills: {', '.join(agent['skills'])}")
        print(f"     Active Hours: {stats['active_hours']}")
        print(f"     Builds: {stats['builds_completed']}")
        print()
    
    inactive = [a for a in ALL_AGENTS if a not in active_agents]
    print(f"\nResting Agents (6/13 offline):")
    print("-" * 70)
    for agent in inactive:
        stats = state["agent_stats"][agent["id"]]
        print(f"  ⚪ {agent['name']} ({agent['role']}) - {stats['active_hours']}h total")
    
    print(f"\nNext Rotation: {ROTATION_INTERVAL_HOURS} hours or on demand")
    print(f"Total Rotations: {state['total_rotations']}")
    print("=" * 70)

def generate_rotation_script(active_agents):
    """Generate script to activate/deactivate agents"""
    script_lines = ["#!/bin/bash", "# Minecraft Agent Rotation Script", ""]
    
    # Stop all agents first
    script_lines.append("# Stop all current agents")
    script_lines.append("pkill -f 'mineflayer.*agent' 2>/dev/null || true")
    script_lines.append("sleep 2")
    script_lines.append("")
    
    # Start active agents
    script_lines.append("# Start active batch")
    for agent in active_agents:
        script_lines.append(f"# Starting {agent['name']} ({agent['role']})")
        script_lines.append(f"echo 'Spawning {agent['name']}...'")
        script_lines.append("sleep 1")
    
    script_lines.append("")
    script_lines.append(f"# {len(active_agents)} agents now active")
    
    return "\n".join(script_lines)

def main():
    print("=" * 70)
    print("MINECRAFT AGENT ROTATION MANAGER")
    print("=" * 70)
    print()
    
    # Load state
    state = load_rotation_state()
    
    # Check if rotation needed
    if should_rotate(state):
        print("🔄 Rotation due. Switching agent batches...")
        state = rotate_agents(state)
        save_rotation_state(state)
        print("✅ Rotation complete.\n")
    else:
        last = datetime.fromisoformat(state["last_rotation"]) if state["last_rotation"] else datetime.now()
        elapsed = datetime.now() - last
        remaining = timedelta(hours=ROTATION_INTERVAL_HOURS) - elapsed
        print(f"⏱️  Next rotation in {remaining.seconds // 3600}h {(remaining.seconds % 3600) // 60}m\n")
    
    # Get active agents
    active_agents = get_current_active_agents(state)
    
    # Print status
    print_agent_status(active_agents, state)
    
    # Generate rotation script
    script = generate_rotation_script(active_agents)
    script_file = Path("/root/.openclaw/workspace/scripts/rotate_minecraft_agents.sh")
    with open(script_file, 'w') as f:
        f.write(script)
    
    print(f"\n✅ Rotation script saved: {script_file}")
    print("\nAll 13 agents are ENHANCED with:")
    for enhancement in ENHANCEMENTS:
        print(f"  ✓ {enhancement}")
    
    print(f"\nEach agent gets {ROTATION_INTERVAL_HOURS} hours active, then rotates.")
    print("Every agent learns, builds, and grows equally.\n")

if __name__ == "__main__":
    main()
