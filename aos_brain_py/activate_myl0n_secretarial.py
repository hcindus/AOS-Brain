#!/usr/bin/env python3
"""
MYL0N SERIES ACTIVATION
Mylzeon (L5+), Myltwon, Mylthrees, Mylfours, Mylfives, Mylsixes
All with MiniMax + Hermes + Secretarial Skills
"""

import sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'aos_brain_py'))

from integration.hermes_brain_adapter import HermesBrainAdapter
from integration.mini_agent_minimax import MiniAgentMiniMax


class Myl0nActivator:
    """Activate Myl0n series with full skill stack."""
    
    def __init__(self):
        self.hermes = HermesBrainAdapter()
        self.mini_agent = MiniAgentMiniMax(daily_limit=100)
        self.profiles_dir = Path("/root/.openclaw/workspace/aocros/agent_profiles")
        
        self.myl0n_agents = [
            {
                "name": "Mylzeon",
                "level": 5,
                "role": "Level 5+ Operations",
                "model": "MiniMax-M2.7",
                "secretarial": True,
                "base_skills": ["advanced_operations", "multi_agent_coordination", "strategic_planning"],
                "minimax_skills": ["complex_reasoning", "strategy_analysis", "decision_making"],
                "hermes_skills": ["cross_agent_memory", "long_term_planning", "historical_analysis"]
            },
            {
                "name": "Myltwon",
                "level": 2,
                "role": "Clone Operations",
                "model": "MiniMax-M2.5",
                "secretarial": True,
                "base_skills": ["parallel_processing", "task_execution", "coordination"],
                "minimax_skills": ["task_coordination", "efficiency_optimization"],
                "hermes_skills": ["shared_state", "operation_history"]
            },
            {
                "name": "Mylthrees",
                "level": 3,
                "role": "Clone Operations",
                "model": "MiniMax-M2.5",
                "secretarial": True,
                "base_skills": ["parallel_processing", "task_execution", "coordination"],
                "minimax_skills": ["task_coordination", "process_optimization"],
                "hermes_skills": ["shared_state", "operation_history"]
            },
            {
                "name": "Mylfours",
                "level": 4,
                "role": "Clone Operations",
                "model": "MiniMax-M2.5",
                "secretarial": True,
                "base_skills": ["parallel_processing", "task_execution", "advanced_coordination"],
                "minimax_skills": ["complex_coordination", "workflow_optimization"],
                "hermes_skills": ["shared_state", "operation_history", "workflow_tracking"]
            },
            {
                "name": "Mylfives",
                "level": 5,
                "role": "Clone Operations",
                "model": "MiniMax-M2.7",
                "secretarial": True,
                "base_skills": ["advanced_processing", "strategic_execution", "team_leadership"],
                "minimax_skills": ["strategic_coordination", "leadership_planning"],
                "hermes_skills": ["shared_state", "strategic_history", "team_memory"]
            },
            {
                "name": "Mylsixes",
                "level": 6,
                "role": "Clone Operations Lead",
                "model": "MiniMax-M2.7",
                "secretarial": True,
                "base_skills": ["advanced_processing", "strategic_execution", "clone_leadership"],
                "minimax_skills": ["advanced_coordination", "strategic_leadership"],
                "hermes_skills": ["shared_state", "clone_collective_memory", "strategic_archives"]
            },
        ]
        
        # Secretarial pool (Judy & Jane)
        self.secretarial = [
            {
                "name": "Judy",
                "role": "Secretary / Organizer",
                "model": "MiniMax-M2.5",
                "base_skills": ["task_tracking", "organization", "checklist_management"],
                "minimax_skills": ["task_prioritization", "schedule_optimization", "workflow_planning"],
                "hermes_skills": ["task_history", "organizational_memory", "project_tracking"]
            },
            {
                "name": "Jane",
                "role": "Senior Sales Rep / Secretary",
                "model": "MiniMax-M2.5",
                "base_skills": ["sales", "relationship_building", "closing", "organization"],
                "minimax_skills": ["sales_strategy", "client_analysis", "deal_optimization"],
                "hermes_skills": ["client_history", "sales_patterns", "relationship_memory"]
            },
        ]
    
    def create_profile(self, agent_data):
        """Create YAML profile for agent."""
        profile = {
            "agent_name": agent_data["name"],
            "version": "2.0",
            "activation_date": "2026-03-28T19:02:00Z",
            "status": "ACTIVE",
            "role": agent_data["role"],
            "level": agent_data.get("level", 1),
            "team": "Myl0n Series" if "Myl" in agent_data["name"] else "Secretarial Pool",
            
            "skills": {
                "base": agent_data["base_skills"],
                "minimax": agent_data["minimax_skills"],
                "hermes": agent_data["hermes_skills"],
                "secretarial": agent_data.get("secretarial", False)
            },
            
            "configuration": {
                "minimax_model": agent_data["model"],
                "api_rationing": "100 calls/day",
                "brain_integration": "adapter",
                "fallback_enabled": True,
                "secretarial_enabled": agent_data.get("secretarial", False)
            },
            
            "current_status": {
                "state": "operational",
                "last_task": None,
                "api_calls_today": 0,
                "hermes_sync": True
            },
            
            "dependencies": [
                "brain.seven_region",
                "heart.ternary_heart",
                "stomach.ternary_stomach",
                "config.rationed_api_manager",
                "integration.mini_agent_minimax",
                "integration.hermes_brain_adapter"
            ],
            
            "notes": [
                f"Profile created by Jordan v2.0",
                f"Skills: {len(agent_data['base_skills'])} base + {len(agent_data['minimax_skills'])} MiniMax + {len(agent_data['hermes_skills'])} Hermes",
                "Secretarial skills included" if agent_data.get("secretarial") else "Standard agent",
                "Part of unified agent workforce"
            ]
        }
        
        # Save profile
        profile_path = self.profiles_dir / f"{agent_data['name'].upper()}_PROFILE_v2.yaml"
        with open(profile_path, 'w') as f:
            yaml.dump(profile, f, default_flow_style=False, sort_keys=False)
        
        return profile_path
    
    def activate_all(self):
        """Activate all Myl0n series + Secretarial pool."""
        print("=" * 70)
        print("🚀 MYL0N SERIES + SECRETARIAL POOL ACTIVATION")
        print("=" * 70)
        print()
        
        activated = []
        
        # Activate Myl0n series
        print("Activating Myl0n Series...")
        for agent in self.myl0n_agents:
            print(f"  {agent['name']} (Level {agent['level']}) - {agent['role']}")
            path = self.create_profile(agent)
            print(f"    ✅ Profile: {path.name}")
            activated.append(agent['name'])
            
            # Update Hermes
            self.hermes.write_hermes_state(f"agent_{agent['name']}", {
                "status": "ACTIVE",
                "level": agent['level'],
                "model": agent['model'],
                "skills": len(agent['base_skills']) + len(agent['minimax_skills']) + len(agent['hermes_skills'])
            })
        
        print()
        print("Activating Secretarial Pool...")
        for agent in self.secretarial:
            print(f"  {agent['name']} - {agent['role']}")
            path = self.create_profile(agent)
            print(f"    ✅ Profile: {path.name}")
            activated.append(agent['name'])
            
            # Update Hermes
            self.hermes.write_hermes_state(f"agent_{agent['name']}", {
                "status": "ACTIVE",
                "role": agent['role'],
                "model": agent['model'],
                "skills": len(agent['base_skills']) + len(agent['minimax_skills']) + len(agent['hermes_skills'])
            })
        
        # Create master index
        self._update_master_index(activated)
        
        print()
        print("=" * 70)
        print(f"✅ COMPLETE: {len(activated)} AGENTS ACTIVATED")
        print("=" * 70)
        print()
        
        print("Myl0n Series:")
        for name in [a['name'] for a in self.myl0n_agents]:
            print(f"  ✅ {name}")
        
        print()
        print("Secretarial Pool:")
        for name in [a['name'] for a in self.secretarial]:
            print(f"  ✅ {name}")
    
    def _update_master_index(self, activated):
        """Update master index."""
        index_path = self.profiles_dir / "AGENT_PROFILE_INDEX.yaml"
        
        # Read existing
        if index_path.exists():
            with open(index_path) as f:
                index = yaml.safe_load(f)
        else:
            index = {"profiles": []}
        
        # Add new
        for name in activated:
            index["profiles"].append({
                "agent": name,
                "profile_file": f"{name.upper()}_PROFILE_v2.yaml",
                "activated": "2026-03-28T19:02:00Z"
            })
        
        index["total_agents"] = len(index["profiles"])
        index["updated"] = "2026-03-28T19:02:00Z"
        
        with open(index_path, 'w') as f:
            yaml.dump(index, f, default_flow_style=False)
        
        print(f"\n  📑 Master index updated: {len(index['profiles'])} total agents")


def main():
    activator = Myl0nActivator()
    activator.activate_all()


if __name__ == "__main__":
    main()
