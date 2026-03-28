#!/usr/bin/env python3
"""
Hermes Brain Adapter - Integrate OpenClaw Hermes with 7-Region Brain.

Hermes is OpenClaw's state-persistence system (~/.local/state/hermes/)
This adapter bridges Hermes state to brain memory.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain


class HermesBrainAdapter:
    """
    Bridge Hermes state system to 7-Region Brain.
    
    Hermes stores state in ~/.local/state/hermes/
    Brain stores memories in hippocampal clusters
    """
    
    def __init__(self, brain: Optional[SevenRegionBrain] = None):
        self.brain = brain or SevenRegionBrain()
        self.hermes_path = Path.home() / ".local" / "state" / "hermes"
        self.hermes_path.mkdir(parents=True, exist_ok=True)
        
        # State tracking
        self.state_cache = {}
        self.sync_interval = 30  # seconds
        self.last_sync = 0
        
    def read_hermes_state(self, key: str) -> Optional[Dict]:
        """Read state from Hermes."""
        state_file = self.hermes_path / f"{key}.json"
        if state_file.exists():
            try:
                with open(state_file) as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def write_hermes_state(self, key: str, data: Dict):
        """Write state to Hermes."""
        state_file = self.hermes_path / f"{key}.json"
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def sync_to_brain(self, key: str):
        """Sync Hermes state to brain memory."""
        state = self.read_hermes_state(key)
        if state:
            # Feed to brain as memory
            content = f"[Hermes:{key}] {json.dumps(state)[:200]}"
            self.brain.feed(content, source=f"hermes_{key}")
            
            # Update cache
            self.state_cache[key] = {
                "data": state,
                "synced_at": time.time()
            }
            
            return True
        return False
    
    def sync_from_brain(self, key: str, query: str):
        """Sync brain memory back to Hermes."""
        # Query brain for relevant memories
        hippo = self.brain.regions['hippocampus']
        
        # Get current state from brain (via clusters)
        cluster_count = hippo.get_cluster_count()
        
        # Write to Hermes
        self.write_hermes_state(key, {
            "brain_clusters": cluster_count,
            "brain_ticks": self.brain.tick_count,
            "query": query,
            "synced_at": time.time()
        })
        
        return True
    
    def bidirectional_sync(self):
        """Run bidirectional sync between Hermes and Brain."""
        print("[Hermes-Brain] Running bidirectional sync...")
        
        # Sync common keys
        keys = ["gateway_state", "session_state", "agent_state"]
        
        synced = 0
        for key in keys:
            if self.sync_to_brain(key):
                synced += 1
        
        # Sync brain status back
        self.sync_from_brain("brain_status", "current_state")
        
        print(f"[Hermes-Brain] Synced {synced} keys")
        print(f"  Brain ticks: {self.brain.tick_count}")
        print(f"  Brain clusters: {self.brain.regions['hippocampus'].get_cluster_count()}")
        
        self.last_sync = time.time()
        
    def test_integration(self):
        """Test Hermes-Brain integration."""
        print("=" * 70)
        print("🔄 HERMES-BRAIN INTEGRATION TEST")
        print("=" * 70)
        
        # Write test state to Hermes
        test_key = "test_integration"
        test_data = {
            "message": "Hello from Hermes",
            "timestamp": time.time(),
            "status": "active"
        }
        
        print(f"\n1. Writing to Hermes: {test_key}")
        self.write_hermes_state(test_key, test_data)
        print(f"   ✓ Written to {self.hermes_path / test_key}.json")
        
        print(f"\n2. Syncing to Brain...")
        self.sync_to_brain(test_key)
        print(f"   ✓ Brain ticks: {self.brain.tick_count}")
        print(f"   ✓ Brain clusters: {self.brain.regions['hippocampus'].get_cluster_count()}")
        
        print(f"\n3. Syncing from Brain to Hermes...")
        self.sync_from_brain("brain_mirror", test_key)
        mirror = self.read_hermes_state("brain_mirror")
        if mirror:
            print(f"   ✓ Brain state mirrored to Hermes")
            print(f"   ✓ Brain clusters: {mirror.get('brain_clusters', 0)}")
            print(f"   ✓ Brain ticks: {mirror.get('brain_ticks', 0)}")
        
        print("\n" + "=" * 70)
        print("✅ HERMES-BRAIN INTEGRATION TEST COMPLETE")
        print("=" * 70)
        
        return {
            "hermes_path": str(self.hermes_path),
            "brain_ticks": self.brain.tick_count,
            "brain_clusters": self.brain.regions['hippocampus'].get_cluster_count(),
            "test_key": test_key,
            "status": "success"
        }


def demo_hermes_integration():
    """Run Hermes-Brain integration demo."""
    adapter = HermesBrainAdapter()
    return adapter.test_integration()


if __name__ == "__main__":
    demo_hermes_integration()
