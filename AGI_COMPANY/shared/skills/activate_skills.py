#!/usr/bin/env python3
"""
Activate Hermes and Mini-Agent Skills for All Team Members
Distribute skills to agents with overlap allowed
"""

import os
import json
from pathlib import Path

AGENTS_DIR = "/root/.openclaw/workspace/AGI_COMPANY/agents"
SKILLS_DIR = "/root/.openclaw/workspace/AGI_COMPANY/shared/skills"

def activate_skills_for_agent(agent_path: str, agent_type: str):
    """Activate skills for an agent"""
    
    skills_config = {
        "hermes": {
            "active": True,
            "channels": ["slack", "discord", "email"],
            "priority": "high"
        },
        "mini-agent": {
            "active": True,
            "max_concurrent": 10,
            "autonomy": "high" if agent_type in ["technical", "tier1"] else "medium"
        },
        "minimax-m2": {
            "active": agent_type in ["technical", "tier1"],
            "model": "MiniMax-M2",
            "access": "full" if agent_type in ["technical", "tier1"] else "limited"
        }
    }
    
    # Create skills directory for agent
    agent_skills_dir = os.path.join(agent_path, "skills")
    os.makedirs(agent_skills_dir, exist_ok=True)
    
    # Write skills config
    config_path = os.path.join(agent_skills_dir, "active_skills.json")
    with open(config_path, "w") as f:
        json.dump(skills_config, f, indent=2)
    
    # Create skill loaders
    for skill_name in ["hermes", "mini-agent"]:
        loader_path = os.path.join(agent_skills_dir, f"{skill_name}_loader.py")
        loader_code = f'''#!/usr/bin/env python3
"""
{skill_name.upper()} Skill Loader for Agent
Auto-generated skill activation
"""

import sys
sys.path.insert(0, "{SKILLS_DIR}/{skill_name}")

from {skill_name.replace("-", "_")}_skill import {skill_name.title().replace("-", "")}Skill

# Activate skill
{skill_name.replace("-", "")}_instance = {skill_name.title().replace("-", "")}Skill()
print(f"[{skill_name.upper()}] Skill activated for agent")

# Export for agent use
skill = {skill_name.replace("-", "")}_instance
'''
        with open(loader_path, "w") as f:
            f.write(loader_code)
        os.chmod(loader_path, 0o755)
    
    return True

def main():
    """Activate skills for all agents"""
    print("=" * 70)
    print("ACTIVATING SKILLS FOR ALL AGENTS")
    print("=" * 70)
    
    # Map agents to types
    agent_types = {
        "cobra": "embodied",
        "prometheus": "embodied",
        "myl_cobra_001": "embodied",
        "myl_cobra_002": "embodied",
        "myl_prometheus_001": "embodied",
        "myl_dual_001": "embodied",
        "mylzeron": "embodied",
        "mylonen": "embodied",
        "myltwon": "embodied",
        "mylthreen": "embodied",
        "mylforon": "embodied",
        "mylfivon": "embodied",
        "mylsixon": "embodied",
        "technical": "technical",
        "tier1": "tier1",
        "secretarial": "secretarial",
    }
    
    activated = []
    
    for agent_name, agent_type in agent_types.items():
        agent_path = os.path.join(AGENTS_DIR, agent_name)
        if os.path.exists(agent_path):
            print(f"\nActivating for: {agent_name} ({agent_type})")
            
            if activate_skills_for_agent(agent_path, agent_type):
                activated.append({
                    "agent": agent_name,
                    "type": agent_type,
                    "skills": ["hermes", "mini-agent"] + (["minimax-m2"] if agent_type in ["technical", "tier1"] else [])
                })
                print(f"  ✓ Skills activated")
            else:
                print(f"  ✗ Failed")
    
    # Summary
    print("\n" + "=" * 70)
    print("SKILL ACTIVATION COMPLETE")
    print("=" * 70)
    print(f"\nTotal agents activated: {len(activated)}")
    
    # Group by type
    by_type = {}
    for a in activated:
        t = a["type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(a["agent"])
    
    for agent_type, agents in by_type.items():
        print(f"\n{agent_type.upper()}:")
        for agent in agents:
            print(f"  • {agent}")
    
    # Technical team MiniMax M2 access
    print("\n" + "=" * 70)
    print("MINIMAX M2 ACCESS (Technical Team)")
    print("=" * 70)
    tech_agents = [a for a in activated if a["type"] in ["technical", "tier1"]]
    for a in tech_agents:
        print(f"  ✓ {a['agent']}: Full MiniMax M2 access")

if __name__ == "__main__":
    main()
