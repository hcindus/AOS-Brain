#!/usr/bin/env python3
"""
AGENT MODEL LOADER v1.0
Loads appropriate model for each AGI Company agent
"""

import json
import os
from typing import Optional, Dict

class AgentModelLoader:
    """Manages model assignments for all AGI Company agents"""
    
    def __init__(self):
        self.config_path = "/root/.aos/aos/model_assignments.json"
        self.assignments = self._load_assignments()
    
    def _load_assignments(self) -> Dict:
        """Load model assignments from JSON"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Model Loader] Error loading config: {e}")
            return {}
    
    def get_agent_model(self, agent_id: str) -> Optional[str]:
        """Get assigned model for agent"""
        agent_data = self.assignments.get("agent_assignments", {})
        agent_config = agent_data.get(agent_id.lower())
        
        if agent_config:
            return agent_config.get("primary")
        return None
    
    def get_agent_info(self, agent_id: str) -> Dict:
        """Get full agent model configuration"""
        agent_data = self.assignments.get("agent_assignments", {})
        return agent_data.get(agent_id.lower(), {})
    
    def get_model_info(self, model_name: str) -> Dict:
        """Get model capabilities and info"""
        registry = self.assignments.get("registry", {})
        return registry.get(model_name, {})
    
    def load_model_for_agent(self, agent_id: str) -> str:
        """
        Load and return the ollama command for agent's assigned model
        
        Returns command string or default
        """
        model = self.get_agent_model(agent_id)
        
        if model:
            if model == "cloud_routed":
                return "[Cloud API - routing via OpenClaw]"
            return f"ollama run {model}"
        
        # Default fallback
        return "ollama run gemma2:2b"
    
    def list_all_assignments(self) -> Dict:
        """List all agent-model assignments"""
        return self.assignments.get("agent_assignments", {})
    
    def get_agents_by_model(self, model_name: str) -> list:
        """Get all agents assigned to a specific model"""
        agents = []
        for agent_id, config in self.assignments.get("agent_assignments", {}).items():
            if config.get("primary") == model_name:
                agents.append(agent_id)
        return agents
    
    def print_status(self):
        """Print model assignment status"""
        print("=" * 70)
        print("  AGI COMPANY - MODEL ASSIGNMENTS")
        print("=" * 70)
        print(f"\nVersion: {self.assignments.get('version', 'unknown')}")
        print(f"Updated: {self.assignments.get('updated', 'unknown')}")
        print(f"Total Agents: {len(self.assignments.get('agent_assignments', {}))}")
        print(f"Models Available: {len(self.assignments.get('registry', {}))}")
        print("\n" + "=" * 70)
        print("  MODELS IN REGISTRY")
        print("=" * 70)
        
        for model_name, info in self.assignments.get("registry", {}).items():
            agents = self.get_agents_by_model(model_name)
            print(f"\n  {model_name}")
            print(f"    Size: {info.get('size', 'unknown')}")
            print(f"    Best for: {info.get('best_for', 'general')}")
            print(f"    Agents assigned: {len(agents)}")

def main():
    """Test model loader"""
    loader = AgentModelLoader()
    loader.print_status()
    
    # Test specific agent lookups
    print("\n" + "=" * 70)
    print("  SAMPLE AGENT LOOKUPS")
    print("=" * 70)
    
    test_agents = ["patricia", "miles", "dusty", "pixel", "greet"]
    for agent in test_agents:
        model = loader.get_agent_model(agent)
        info = loader.get_agent_info(agent)
        print(f"\n  {agent.upper()}")
        print(f"    Model: {model}")
        print(f"    Use case: {info.get('use_case', 'unknown')}")
        print(f"    Command: {loader.load_model_for_agent(agent)}")
    
    print("\n" + "=" * 70)
    print("  ✅ Model Loader Ready")
    print("=" * 70)

if __name__ == "__main__":
    main()
