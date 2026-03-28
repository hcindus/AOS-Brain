#!/usr/bin/env python3
"""
BULK AGENT ACTIVATION
Priority 3-5: Creative, Research, Specialized
All with MiniMax + Hermes (overlapping skills)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'aos_brain_py'))

from integration.hermes_brain_adapter import HermesBrainAdapter
from integration.mini_agent_minimax import MiniAgentMiniMax


class BulkActivator:
    """Activate multiple agents with shared capabilities."""
    
    def __init__(self):
        self.hermes = HermesBrainAdapter()
        self.mini_agent = MiniAgentMiniMax(daily_limit=100)
        
        self.agents = [
            # Priority 3: Creative
            {"name": "Pixel", "role": "Image Generation", "model": "MiniMax-M2.5"},
            {"name": "Milkman", "role": "Audio/Voice", "model": "MiniMax-M2.5"},
            {"name": "SFX", "role": "Sound Effects", "model": "MiniMax-M2.5"},
            
            # Priority 4: Research
            {"name": "Dusty", "role": "Research Assistant", "model": "MiniMax-M2.7"},
            {"name": "Harper", "role": "Documentation", "model": "MiniMax-M2.5"},
            {"name": "Ledger", "role": "Finance Tracking", "model": "MiniMax-M2.5"},
            
            # Priority 5: Specialized
            {"name": "Cryptonio", "role": "Crypto Trading", "model": "MiniMax-M2.7"},
            {"name": "Myl0n-1", "role": "Clone Operations", "model": "MiniMax-M2.5"},
            {"name": "Myl0n-2", "role": "Clone Operations", "model": "MiniMax-M2.5"},
        ]
    
    def activate_all(self):
        """Activate all remaining agents."""
        print("=" * 70)
        print("🚀 BULK AGENT ACTIVATION")
        print("=" * 70)
        print()
        
        activated = []
        
        for agent in self.agents:
            print(f"Activating: {agent['name']}")
            print(f"  Role: {agent['role']}")
            print(f"  Model: {agent['model']}")
            print(f"  Skills: MiniMax + Hermes (overlapping)")
            print(f"  ✅ Activated")
            print()
            
            # Update Hermes
            self.hermes.write_hermes_state(f"agent_{agent['name']}", {
                "status": "ACTIVE",
                "version": "2.0",
                "model": agent['model'],
                "skills": ["minimax", "hermes"],
                "activated": "2026-03-28"
            })
            
            activated.append(agent)
        
        print("=" * 70)
        print(f"✅ ACTIVATED {len(activated)} AGENTS")
        print("=" * 70)
        print()
        
        for a in activated:
            print(f"  ✅ {a['name']} - {a['role']}")
        
        return activated


if __name__ == "__main__":
    activator = BulkActivator()
    activator.activate_all()
