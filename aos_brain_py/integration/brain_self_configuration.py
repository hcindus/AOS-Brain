#!/usr/bin/env python3
"""
Brain Self-Configuration Guide Feeder.

Teaches the brain how to configure itself for MiniMax, Mini-Agent, and Hermes.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.stomach_auto_feeder_full import StomachAutoFeederFull


class BrainSelfConfiguration:
    """Feed brain configuration knowledge for integrations."""
    
    def __init__(self):
        self.feeder = StomachAutoFeederFull()
    
    def get_minimax_brain_config(self):
        """How brain configures itself for MiniMax."""
        return [
            # Setup Steps
            ("Brain MiniMax Config Step 1: Import MiniMaxBrainAdapter from integration.minimax_brain_adapter", "brain_minimax_setup"),
            ("Brain MiniMax Config Step 2: Import SevenRegionBrain, TernaryHeart, TernaryStomach", "brain_minimax_setup"),
            ("Brain MiniMax Config Step 3: Initialize brain = SevenRegionBrain()", "brain_minimax_setup"),
            ("Brain MiniMax Config Step 4: Initialize heart = TernaryHeart()", "brain_minimax_setup"),
            ("Brain MiniMax Config Step 5: Initialize stomach = TernaryStomach()", "brain_minimax_setup"),
            ("Brain MiniMax Config Step 6: Create adapter = MiniMaxBrainAdapter(brain, heart, stomach)", "brain_minimax_setup"),
            ("Brain MiniMax Config Step 7: Adapter auto-loads config from ~/.mini-agent/config/config.yaml", "brain_minimax_setup"),
            ("Brain MiniMax Config Step 8: Use adapter.process_query(query, context) for full pipeline", "brain_minimax_setup"),
            
            # Configuration Files
            ("Brain MiniMax requires: ~/.mini-agent/config/config.yaml with api_key", "brain_minimax_files"),
            ("Brain MiniMax requires: ~/.mini-agent/config/mcp.json for MCP servers", "brain_minimax_files"),
            ("Brain MiniMax checks: api_key must not be YOUR_API_KEY_HERE placeholder", "brain_minimax_files"),
            ("Brain MiniMax checks: api_base should be https://api.minimax.io", "brain_minimax_files"),
            ("Brain MiniMax checks: model should be MiniMax-M2.5", "brain_minimax_files"),
            ("Brain MiniMax checks: provider should be anthropic", "brain_minimax_files"),
            
            # Pipeline Configuration
            ("Brain MiniMax pipeline: Stomach digests queries before brain feeding", "brain_minimax_pipeline"),
            ("Brain MiniMax pipeline: Heart provides rhythm at 72 BPM default", "brain_minimax_pipeline"),
            ("Brain MiniMax pipeline: Brain processes through 7-region OODA", "brain_minimax_pipeline"),
            ("Brain MiniMax pipeline: Response includes heart_state and brain_ticks", "brain_minimax_pipeline"),
            
            # Troubleshooting
            ("Brain MiniMax fix: If adapter fails, check MiniMaxBrainAdapter import path", "brain_minimax_fix"),
            ("Brain MiniMax fix: If no response, verify API key is valid", "brain_minimax_fix"),
            ("Brain MiniMax fix: If slow, check stomach digestion rate", "brain_minimax_fix"),
            ("Brain MiniMax fix: If heart stuck, call heart.beat() manually", "brain_minimax_fix"),
        ]
    
    def get_mini_agent_brain_config(self):
        """How brain configures itself for Mini-Agent."""
        return [
            # Setup Steps
            ("Brain Mini-Agent Config Step 1: Mini-Agent framework uses MiniMax API", "brain_miniagent_setup"),
            ("Brain Mini-Agent Config Step 2: Brain replaces direct MiniMax calls with pipeline", "brain_miniagent_setup"),
            ("Brain Mini-Agent Config Step 3: Import mini_agent_setup from integration.mini_agent_setup", "brain_miniagent_setup"),
            ("Brain Mini-Agent Config Step 4: Create MiniAgentBrainIntegration instance", "brain_miniagent_setup"),
            ("Brain Mini-Agent Config Step 5: Call check_config() to verify Mini-Agent files", "brain_miniagent_setup"),
            ("Brain Mini-Agent Config Step 6: Call enable_mcp_servers() to activate tools", "brain_miniagent_setup"),
            ("Brain Mini-Agent Config Step 7: Use process_with_brain() instead of direct API", "brain_miniagent_setup"),
            ("Brain Mini-Agent Config Step 8: All Mini-Agent queries now go through stomach-heart-brain", "brain_miniagent_setup"),
            
            # Configuration Files
            ("Brain Mini-Agent requires: ~/.mini-agent/config/config.yaml", "brain_miniagent_files"),
            ("Brain Mini-Agent requires: ~/.mini-agent/config/system_prompt.md", "brain_miniagent_files"),
            ("Brain Mini-Agent requires: ~/.mini-agent/config/mcp.json for tools", "brain_miniagent_files"),
            ("Brain Mini-Agent modifies: MCP servers enabled via mcp.json", "brain_miniagent_files"),
            ("Brain Mini-Agent checks: enable_mcp: true in config.yaml", "brain_miniagent_files"),
            ("Brain Mini-Agent checks: enable_file_tools, enable_bash, enable_note enabled", "brain_miniagent_files"),
            
            # Integration Points
            ("Brain Mini-Agent integration: MiniMaxBrainAdapter connects to Mini-Agent", "brain_miniagent_integration"),
            ("Brain Mini-Agent integration: StomachAutoFeederFull processes all queries", "brain_miniagent_integration"),
            ("Brain Mini-Agent integration: SevenRegionBrain provides cognition", "brain_miniagent_integration"),
            ("Brain Mini-Agent integration: TernaryHeart provides emotional context", "brain_miniagent_integration"),
            ("Brain Mini-Agent integration: TernaryStomach digests inputs", "brain_miniagent_integration"),
            
            # Skills Available
            ("Brain Mini-Agent skills: File operations via enable_file_tools", "brain_miniagent_skills"),
            ("Brain Mini-Agent skills: Bash execution via enable_bash", "brain_miniagent_skills"),
            ("Brain Mini-Agent skills: MCP tools via enable_mcp", "brain_miniagent_skills"),
            ("Brain Mini-Agent skills: PDF, PowerPoint, Word, Excel processing", "brain_miniagent_skills"),
            ("Brain Mini-Agent skills: Canvas design and algorithmic art", "brain_miniagent_skills"),
            
            # Troubleshooting
            ("Brain Mini-Agent fix: If config not found, check ~/.mini-agent/ exists", "brain_miniagent_fix"),
            ("Brain Mini-Agent fix: If MCP fails, verify mcp.json has valid entries", "brain_miniagent_fix"),
            ("Brain Mini-Agent fix: If skills fail, check enable_skills: true", "brain_miniagent_fix"),
            ("Brain Mini-Agent fix: If no response, check MiniMax API connectivity", "brain_miniagent_fix"),
        ]
    
    def get_hermes_brain_config(self):
        """How brain configures itself for Hermes."""
        return [
            # Setup Steps
            ("Brain Hermes Config Step 1: Import HermesBrainAdapter from integration.hermes_brain_adapter", "brain_hermes_setup"),
            ("Brain Hermes Config Step 2: Import SevenRegionBrain", "brain_hermes_setup"),
            ("Brain Hermes Config Step 3: Initialize brain = SevenRegionBrain()", "brain_hermes_setup"),
            ("Brain Hermes Config Step 4: Create adapter = HermesBrainAdapter(brain)", "brain_hermes_setup"),
            ("Brain Hermes Config Step 5: Adapter auto-detects ~/.local/state/hermes/", "brain_hermes_setup"),
            ("Brain Hermes Config Step 6: Use sync_to_brain(key) to load state", "brain_hermes_setup"),
            ("Brain Hermes Config Step 7: Use sync_from_brain(key, query) to save state", "brain_hermes_setup"),
            ("Brain Hermes Config Step 8: Use bidirectional_sync() for full sync", "brain_hermes_setup"),
            
            # Configuration Files
            ("Brain Hermes requires: ~/.local/state/hermes/ directory exists", "brain_hermes_files"),
            ("Brain Hermes creates: JSON state files in hermes directory", "brain_hermes_files"),
            ("Brain Hermes creates: {key}.json format for each state", "brain_hermes_files"),
            ("Brain Hermes checks: State files are valid JSON", "brain_hermes_files"),
            ("Brain Hermes checks: Write permissions to state directory", "brain_hermes_files"),
            
            # State Management
            ("Brain Hermes state: session_state for session persistence", "brain_hermes_state"),
            ("Brain Hermes state: gateway_state for gateway configuration", "brain_hermes_state"),
            ("Brain Hermes state: agent_state for agent coordination", "brain_hermes_state"),
            ("Brain Hermes state: brain_status for brain health", "brain_hermes_state"),
            
            # Sync Process
            ("Brain Hermes sync: Reads JSON from ~/.local/state/hermes/", "brain_hermes_sync"),
            ("Brain Hermes sync: Feeds content to stomach-brain pipeline", "brain_hermes_sync"),
            ("Brain Hermes sync: Creates hippocampal clusters for state", "brain_hermes_sync"),
            ("Brain Hermes sync: Writes brain status back to JSON", "brain_hermes_sync"),
            ("Brain Hermes sync: Bidirectional keeps both systems aligned", "brain_hermes_sync"),
            
            # Troubleshooting
            ("Brain Hermes fix: If sync fails, check ~/.local/state/hermes/ exists", "brain_hermes_fix"),
            ("Brain Hermes fix: If JSON error, validate state file syntax", "brain_hermes_fix"),
            ("Brain Hermes fix: If permission denied, check directory ownership", "brain_hermes_fix"),
            ("Brain Hermes fix: If brain not updating, verify SevenRegionBrain initialized", "brain_hermes_fix"),
        ]
    
    def get_common_configuration(self):
        """Common configuration for all three systems."""
        return [
            # General Setup
            ("Brain Common Config: All integrations use stomach-brain pipeline", "brain_common"),
            ("Brain Common Config: All integrations require SevenRegionBrain", "brain_common"),
            ("Brain Common Config: Lazy initialization prevents startup hangs", "brain_common"),
            ("Brain Common Config: Cortical sheet loads on first use", "brain_common"),
            
            # File Locations
            ("Brain Common Files: aos_brain_py/integration/ contains adapters", "brain_common_files"),
            ("Brain Common Files: aos_brain_py/brain/seven_region.py is core", "brain_common_files"),
            ("Brain Common Files: aos_brain_py/stomach/ternary_stomach.py for digestion", "brain_common_files"),
            ("Brain Common Files: aos_brain_py/heart/ternary_heart.py for rhythm", "brain_common_files"),
            
            # Dependencies
            ("Brain Common Deps: Python 3.8+ required", "brain_common_deps"),
            ("Brain Common Deps: No external schedule module needed", "brain_common_deps"),
            ("Brain Common Deps: Standard library only for Brain Cron", "brain_common_deps"),
            ("Brain Common Deps: NumPy for cortical sheet (lazy loaded)", "brain_common_deps"),
            
            # Testing
            ("Brain Common Test: Run adapter.test_integration() to verify", "brain_common_test"),
            ("Brain Common Test: Check brain.tick_count increases after operations", "brain_common_test"),
            ("Brain Common Test: Verify stomach queue empties after digestion", "brain_common_test"),
            ("Brain Common Test: Confirm heart state changes during operation", "brain_common_test"),
        ]
    
    def get_quick_start_guide(self):
        """Quick start configuration guide."""
        return [
            ("QUICK START: Configure MiniMax - Import adapter, create instance, process queries", "quickstart"),
            ("QUICK START: Configure Mini-Agent - Import setup, enable MCP, process with brain", "quickstart"),
            ("QUICK START: Configure Hermes - Import adapter, sync to brain, sync from brain", "quickstart"),
            ("QUICK START: All three use same brain instance for shared knowledge", "quickstart"),
            ("QUICK START: Check ~/.aos/brain/state/ for brain state files", "quickstart"),
            ("QUICK START: Verify port 5000 for brain daemon HTTP API", "quickstart"),
            ("QUICK START: Use StomachAutoFeederFull for batch operations", "quickstart"),
            ("QUICK START: All operations go through 7-region OODA loop", "quickstart"),
        ]
    
    def feed_all_config(self):
        """Feed all configuration knowledge."""
        print("=" * 70)
        print("🧠 BRAIN SELF-CONFIGURATION FEEDER")
        print("   Teaching brain how to configure MiniMax, Mini-Agent, Hermes")
        print("=" * 70)
        print()
        
        all_items = []
        
        # MiniMax
        print("Loading MiniMax configuration...")
        minimax = self.get_minimax_brain_config()
        all_items.extend([(content, "", "", category) for content, category in minimax])
        print(f"   ✅ {len(minimax)} MiniMax config items")
        
        # Mini-Agent
        print("Loading Mini-Agent configuration...")
        miniagent = self.get_mini_agent_brain_config()
        all_items.extend([(content, "", "", category) for content, category in miniagent])
        print(f"   ✅ {len(miniagent)} Mini-Agent config items")
        
        # Hermes
        print("Loading Hermes configuration...")
        hermes = self.get_hermes_brain_config()
        all_items.extend([(content, "", "", category) for content, category in hermes])
        print(f"   ✅ {len(hermes)} Hermes config items")
        
        # Common
        print("Loading common configuration...")
        common = self.get_common_configuration()
        all_items.extend([(content, "", "", category) for content, category in common])
        print(f"   ✅ {len(common)} common config items")
        
        # Quick start
        print("Loading quick start guide...")
        quick = self.get_quick_start_guide()
        all_items.extend([(content, "", "", category) for content, category in quick])
        print(f"   ✅ {len(quick)} quick start items")
        
        total = len(all_items)
        print(f"\n🎯 Total configuration items: {total}")
        print()
        
        # Feed through pipeline
        print("🍽️ Feeding configuration to brain...")
        print("=" * 70)
        result = self.feeder.run_until_empty(all_items)
        
        # Summary
        print("\n" + "=" * 70)
        print("✅ BRAIN SELF-CONFIGURATION COMPLETE")
        print("=" * 70)
        print()
        print(f"📊 Results:")
        print(f"   Config items: {result['fed']}")
        print(f"   Digested: {result['digested']}")
        print(f"   Efficiency: {result['efficiency']:.1f}%")
        print()
        print(f"🧠 Brain State:")
        print(f"   Ticks: {result['brain_ticks']}")
        print(f"   Clusters: {result['brain_clusters']}")
        print()
        
        # Categories
        categories = {}
        for content, category in [(c, cat) for c, _, _, cat in all_items]:
            categories[category] = categories.get(category, 0) + 1
        
        print("📚 Configuration by System:")
        for cat, count in sorted(categories.items()):
            print(f"   - {cat}: {count}")
        
        print()
        print("✅ Brain now knows how to configure itself!")
        print("   Ask: 'How do I configure MiniMax integration?'")
        print("   Ask: 'How do I setup Mini-Agent with brain?'")
        print("   Ask: 'How do I sync Hermes with brain?'")
        
        return result


def main():
    """Run brain self-configuration feeder."""
    config = BrainSelfConfiguration()
    result = config.feed_all_config()


if __name__ == "__main__":
    main()
