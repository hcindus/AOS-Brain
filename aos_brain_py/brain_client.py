#!/usr/bin/env python3
"""
Brain Skill Interface for Agents (Phase 4)

Agents can discover and use brain capabilities via unified interface.
"""

import json
import requests
from typing import Dict, List, Optional

class BrainClient:
    """
    Client for agents to interact with the skills-first brain.
    
    Agents discover brain capabilities as skills and call them.
    """
    
    def __init__(self, brain_url: str = "http://localhost:5000"):
        self.brain_url = brain_url
        self._skills_cache: Optional[Dict] = None
    
    def discover_skills(self) -> List[Dict]:
        """Discover available brain skills."""
        try:
            response = requests.get(f"{self.brain_url}/skills", timeout=2)
            if response.status_code == 200:
                self._skills_cache = response.json()
                return self._skills_cache.get('skills', [])
            return []
        except:
            return []
    
    def call_skill(self, skill_name: str, input_data: Dict) -> Dict:
        """Call a brain skill."""
        try:
            response = requests.post(
                f"{self.brain_url}/skills/{skill_name}",
                json=input_data,
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def get_brain_health(self) -> Dict:
        """Quick health check."""
        return self.call_skill('brain-health-check', {'detailed': False})
    
    def process_sensory(self, source: str, data: any, priority: float = 0.5) -> Dict:
        """Submit sensory input to brain."""
        return self.call_skill('thalamus', {
            'source': source,
            'data': data,
            'priority': priority,
            'timestamp': time.time()
        })
    
    def request_decision(self, context: Dict, options: List[Dict]) -> Dict:
        """Request PFC decision-making."""
        return self.call_skill('pfc', {
            'context': context,
            'options': options,
            'signature': context.get('signature', {}),
            'ollama_available': False
        })


# Agent skill assignment format (for active_skills.json)
AGENT_BRAIN_SKILLS_TEMPLATE = {
    "brain-sensory": {
        "active": True,
        "description": "Submit sensory data to brain",
        "call_pattern": "brain.process_sensory(source, data)"
    },
    "brain-decision": {
        "active": True,
        "description": "Request decision from PFC",
        "call_pattern": "brain.request_decision(context, options)"
    },
    "brain-health": {
        "active": True,
        "description": "Check brain health status",
        "call_pattern": "brain.get_brain_health()"
    },
    "brain-recovery": {
        "active": False,  # Only for privileged agents
        "description": "Trigger brain recovery",
        "call_pattern": "brain.call_skill('tick-recovery', {})"
    }
}


if __name__ == '__main__':
    import time
    
    # Example usage
    client = BrainClient()
    
    print("Brain Client Demo")
    print("=================")
    
    # Check health
    health = client.get_brain_health()
    print(f"\nBrain Health: {health.get('status', 'unknown')}")
    
    # Submit sensory input
    result = client.process_sensory('agent', 'explore_north', priority=0.8)
    print(f"\nSensory Processing:")
    print(f"  Routing: {result.get('routing', [])}")
    print(f"  Signature: {result.get('signature', {})}")
    
    print("\nAgent can now use brain skills via BrainClient!")
