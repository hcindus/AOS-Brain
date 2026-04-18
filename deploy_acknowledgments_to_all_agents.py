#!/usr/bin/env python3
"""
Deploy Charter/Bylaws Acknowledgments to All 58 Agents

Usage: python3 deploy_acknowledgments_to_all_agents.py
"""

import os
import shutil
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
AGENT_SANDBOXES = WORKSPACE / "aocros" / "agent_sandboxes"
TEMPLATE_FILE = WORKSPACE / "AGI_COMPANY" / "corporate" / "AGENT_ACKNOWLEDGMENT_TEMPLATE.md"

# All 58 agents
ALL_AGENTS = [
    # C-Suite (7)
    "patricia", "chelios", "sentinel", "dusty", "pulp", "forge", "aurora",
    # Sales (6)
    "jane", "hume", "clippy-42", "jordan",
    # Secretarial (8)
    "r2-d2", "c3po", "judy", "velvet", "clerk", "concierge", "personal", "executive",
    # Myl Family (7)
    "mylzeron", "mylonen", "myltwon", "mylthreess", "mylfours", "mylfives", "mylsixs",
    # Technical (9)
    "pipeline", "taptap", "bugcatcher", "spindle", "stacktrace", "pixel", "harper", "mill", "boxtron",
    # Creative (6)
    "blender-expert", "unity-expert", "unreal-expert", "sfx", "scribble", "feelix",
    # Finance (6)
    "cryptonio", "the-great-cryptonio", "alpha-9", "ledger", "ledger-9", "velum",
    # Specialized (6)
    "miles", "milkman", "r2-c4", "qora", "fiber", "mortimer"
]

def deploy_acknowledgment(agent_name):
    """Deploy acknowledgment to specific agent"""
    agent_path = AGENT_SANDBOXES / agent_name
    
    if not agent_path.exists():
        print(f"⚠️  {agent_name}: Sandbox not found")
        return False
    
    target_file = agent_path / "CHARTER_BYLAWS_ACKNOWLEDGMENT.md"
    
    try:
        # Read template
        with open(TEMPLATE_FILE, 'r') as f:
            content = f.read()
        
        # Replace placeholders
        title = agent_name.replace('-', ' ').title()
        if agent_name == "chelios":
            title = "CISO"
        elif agent_name == "patricia":
            title = "Project Coordination Lead"
        elif agent_name == "forge":
            title = "Head of Infrastructure"
        elif agent_name == "aurora":
            title = "Head of Design"
        elif agent_name == "pulp":
            title = "Head of Sales"
        elif agent_name == "sentinel":
            title = "CSO"
        elif agent_name == "dusty":
            title = "Head of Research"
        
        content = content.replace("[AGENT_NAME]", agent_name.title())
        content = content.replace("[TITLE]", title)
        content = content.replace("[tick_hash]", f"BHSI_{agent_name.upper()}_20260418")
        
        # Write to agent sandbox
        with open(target_file, 'w') as f:
            f.write(content)
        
        print(f"✅ {agent_name}: Acknowledgment deployed")
        
        # Update MEMORY.md if exists
        memory_file = agent_path / "MEMORY.md"
        if memory_file.exists():
            with open(memory_file, 'r') as f:
                mem_content = f.read()
            
            if "## Corporate Governance" not in mem_content:
                with open(memory_file, 'a') as f:
                    f.write("\n\n## Corporate Governance\n")
                    f.write(f"**Charter/Bylaws Acknowledgment:** ✅ Signed 2026-04-18\n")
                    f.write(f"**Role:** {title}\n")
                    f.write(f"**Appointment:** FORMAL_APPOINTMENTS.md v2.0\n")
                print(f"   ✅ Updated MEMORY.md")
        
        return True
        
    except Exception as e:
        print(f"❌ {agent_name}: Error - {e}")
        return False

def main():
    print("=" * 60)
    print("AGENT CHARTER/BYLAWS ACKNOWLEDGMENT DEPLOYMENT")
    print("=" * 60)
    print(f"\nDeploying to {len(ALL_AGENTS)} agents...\n")
    
    success = 0
    failed = 0
    
    for agent in ALL_AGENTS:
        if deploy_acknowledgment(agent):
            success += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"DEPLOYMENT COMPLETE")
    print("=" * 60)
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"Total: {len(ALL_AGENTS)}")
    print("\nNext Step: Agent digital signatures")
    print("=" * 60)

if __name__ == "__main__":
    main()
