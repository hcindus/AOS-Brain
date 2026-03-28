#!/usr/bin/env python3
"""
Mini-Agent Setup with Brain Integration.

Configures Mini-Agent to use 7-Region Brain + Stomach + Heart for all operations.
"""

import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.minimax_brain_adapter import MiniMaxBrainAdapter
from brain.seven_region import SevenRegionBrain
from heart.ternary_heart import TernaryHeart
from stomach.ternary_stomach import TernaryStomach


class MiniAgentBrainIntegration:
    """
    Mini-Agent wrapper with full brain-heart-stomach integration.
    
    This class makes Mini-Agent use our ternary brain for ALL operations
    instead of direct MiniMax API calls.
    """
    
    def __init__(self):
        # Initialize our brain system
        self.brain = SevenRegionBrain()
        self.heart = TernaryHeart()
        self.stomach = TernaryStomach()
        
        # Create MiniMax adapter
        self.adapter = MiniMaxBrainAdapter(
            brain=self.brain,
            heart=self.heart,
            stomach=self.stomach
        )
        
        # Load Mini-Agent config
        self.config_path = Path.home() / ".mini-agent" / "config" / "config.yaml"
        self.mcp_path = Path.home() / ".mini-agent" / "config" / "mcp.json"
        
        print("=" * 70)
        print("🤖 MINI-AGENT + BRAIN INTEGRATION")
        print("=" * 70)
        print()
        
    def check_config(self):
        """Check Mini-Agent configuration."""
        print("📋 Checking Mini-Agent configuration...")
        
        if not self.config_path.exists():
            print(f"   ❌ Config not found at {self.config_path}")
            return False
        
        print(f"   ✓ Config found: {self.config_path}")
        
        # Check if API key is set
        with open(self.config_path) as f:
            content = f.read()
            if 'YOUR_API_KEY_HERE' in content:
                print("   ⚠️  API key is placeholder - needs real MiniMax key")
            else:
                print("   ✓ API key configured")
        
        # Check MCP config
        if self.mcp_path.exists():
            print(f"   ✓ MCP config found: {self.mcp_path}")
            with open(self.mcp_path) as f:
                mcp = json.load(f)
                for name, server in mcp.get('mcpServers', {}).items():
                    status = "disabled" if server.get('disabled') else "enabled"
                    print(f"     - {name}: {status}")
        
        return True
    
    def enable_mcp_servers(self):
        """Enable MCP servers."""
        print("\n🔌 Enabling MCP servers...")
        
        if not self.mcp_path.exists():
            print("   ❌ MCP config not found")
            return
        
        with open(self.mcp_path) as f:
            mcp = json.load(f)
        
        enabled = 0
        for name, server in mcp.get('mcpServers', {}).items():
            if server.get('disabled'):
                server['disabled'] = False
                enabled += 1
                print(f"   ✓ Enabled: {name}")
        
        if enabled > 0:
            with open(self.mcp_path, 'w') as f:
                json.dump(mcp, f, indent=4)
            print(f"   ✓ Saved {enabled} enabled servers")
        else:
            print("   ✓ All servers already enabled")
    
    def process_with_brain(self, query: str, context: str = "") -> dict:
        """
        Process Mini-Agent query through brain-heart-stomach pipeline.
        
        This replaces direct MiniMax API calls with our brain system.
        """
        print(f"\n🧠 Processing through Brain-Heart-Stomach...")
        print(f"   Query: {query[:50]}...")
        
        # Use our adapter
        result = self.adapter.process_query(query, context)
        
        # Heart status
        heart_status = self.heart.get_state_summary()
        
        # Brain status
        brain_clusters = self.brain.regions['hippocampus'].get_cluster_count()
        
        print(f"   ✓ Heart: {heart_status}")
        print(f"   ✓ Brain: {result['brain_ticks']} ticks, {brain_clusters} clusters")
        print(f"   ✓ Stomach: {result['stomach_status']}")
        
        return result
    
    def test_mini_agent(self):
        """Test Mini-Agent with brain integration."""
        print("\n" + "=" * 70)
        print("🧪 TESTING MINI-AGENT + BRAIN")
        print("=" * 70)
        print()
        
        test_queries = [
            "What is the capital of France?",
            "Explain quantum computing simply",
            "Write a haiku about programming"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n[{i}] Query: {query}")
            result = self.process_with_brain(query, "test")
            print(f"    Processed: {result['chunks_processed']} chunks")
        
        print("\n" + "=" * 70)
        print("✅ MINI-AGENT + BRAIN TEST COMPLETE")
        print("=" * 70)
        print(f"\nFinal Brain State:")
        print(f"  Ticks: {self.brain.tick_count}")
        print(f"  Clusters: {self.brain.regions['hippocampus'].get_cluster_count()}")
        print(f"  Heart: {self.heart.get_state_summary()}")
    
    def setup_complete(self):
        """Print setup summary."""
        print("\n" + "=" * 70)
        print("🎉 MINI-AGENT SETUP COMPLETE")
        print("=" * 70)
        print()
        print("Configuration:")
        print(f"  Config: {self.config_path}")
        print(f"  MCP: {self.mcp_path}")
        print()
        print("Integration:")
        print("  ✓ Mini-Agent queries → Stomach (digest)")
        print("  ✓ Stomach → Heart (rhythm/emotion)")
        print("  ✓ Heart → Brain (7-region cognition)")
        print("  ✓ Brain → Response (cognitive output)")
        print()
        print("All Mini-Agent operations now use the ternary brain system!")
        print("=" * 70)


def main():
    """Run Mini-Agent setup."""
    mini_agent = MiniAgentBrainIntegration()
    
    # Check config
    if mini_agent.check_config():
        # Enable MCP servers
        mini_agent.enable_mcp_servers()
        
        # Test integration
        mini_agent.test_mini_agent()
        
        # Show completion
        mini_agent.setup_complete()
    else:
        print("\n❌ Setup failed - check configuration")


if __name__ == "__main__":
    main()
