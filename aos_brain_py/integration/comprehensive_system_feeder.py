#!/usr/bin/env python3
"""
Comprehensive System Feeder - MiniMax, Mini-Agent, Hermes.

Feeds ALL system information to brain for help/support mode.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.stomach_auto_feeder_full import StomachAutoFeederFull


class ComprehensiveSystemFeeder:
    """Feed comprehensive system information to brain."""
    
    def __init__(self):
        self.feeder = StomachAutoFeederFull()
        
    def get_minimax_comprehensive(self):
        """Comprehensive MiniMax information."""
        return [
            # Company Info
            ("MiniMax is a Chinese AI company founded in 2021", "minimax_info"),
            ("MiniMax headquarters: Shanghai, China", "minimax_info"),
            ("MiniMax focus: Large language models and multimodal AI", "minimax_info"),
            ("MiniMax valuation: Over $1 billion (unicorn status)", "minimax_info"),
            
            # Models
            ("MiniMax-M2.5: Flagship LLM with 3.2B parameters", "minimax_models"),
            ("MiniMax-M2.5 capabilities: Text generation, code, reasoning", "minimax_models"),
            ("MiniMax API: https://api.minimax.io (global)", "minimax_api"),
            ("MiniMax API China: https://api.minimaxi.com", "minimax_api"),
            ("MiniMax platform: https://platform.minimax.io", "minimax_api"),
            
            # API Details
            ("MiniMax authentication: API key in Authorization header", "minimax_api"),
            ("MiniMax pricing: Pay per token usage", "minimax_api"),
            ("MiniMax rate limits: Varies by tier", "minimax_api"),
            ("MiniMax context window: Up to 8K tokens", "minimax_api"),
            ("MiniMax temperature: 0.0 to 2.0 control", "minimax_api"),
            
            # Endpoints
            ("MiniMax chat endpoint: POST /v1/chat/completions", "minimax_endpoints"),
            ("MiniMax embeddings: POST /v1/embeddings", "minimax_endpoints"),
            ("MiniMax provider: anthropic or openai format", "minimax_endpoints"),
            
            # MCP Integration
            ("MiniMax MCP: Model Context Protocol for tool access", "minimax_mcp"),
            ("MiniMax search MCP: Web search and browsing capability", "minimax_mcp"),
            ("MiniMax memory MCP: Knowledge graph persistence", "minimax_mcp"),
            
            # Troubleshooting
            ("MiniMax error 429: Rate limit exceeded - wait and retry", "minimax_errors"),
            ("MiniMax error 401: Invalid API key - check configuration", "minimax_errors"),
            ("MiniMax error 500: Server error - check status page", "minimax_errors"),
            ("MiniMax timeout: Check network, increase timeout", "minimax_errors"),
            
            # Best Practices
            ("MiniMax best practice: Use exponential backoff for retries", "minimax_best_practices"),
            ("MiniMax best practice: Stream responses for long outputs", "minimax_best_practices"),
            ("MiniMax best practice: Cache embeddings for reuse", "minimax_best_practices"),
            ("MiniMax best practice: Batch requests when possible", "minimax_best_practices"),
        ]
    
    def get_mini_agent_comprehensive(self):
        """Comprehensive Mini-Agent information."""
        return [
            # Overview
            ("Mini-Agent: AI assistant framework using MiniMax", "miniagent_overview"),
            ("Mini-Agent location: ~/.mini-agent/", "miniagent_config"),
            ("Mini-Agent config file: config.yaml", "miniagent_config"),
            ("Mini-Agent system prompt: system_prompt.md", "miniagent_config"),
            ("Mini-Agent MCP config: mcp.json", "miniagent_config"),
            
            # Configuration
            ("Mini-Agent api_key: Set in config.yaml", "miniagent_config"),
            ("Mini-Agent api_base: https://api.minimax.io", "miniagent_config"),
            ("Mini-Agent model: MiniMax-M2.5", "miniagent_config"),
            ("Mini-Agent provider: anthropic (default)", "miniagent_config"),
            
            # Tools
            ("Mini-Agent file tools: Read, Write, Edit files", "miniagent_tools"),
            ("Mini-Agent bash tool: Execute shell commands", "miniagent_tools"),
            ("Mini-Agent MCP tools: External tool integration", "miniagent_tools"),
            ("Mini-Agent note tool: Session persistence", "miniagent_tools"),
            
            # Skills
            ("Mini-Agent skills: PDF, PowerPoint, Word, Excel processing", "miniagent_skills"),
            ("Mini-Agent skills: Canvas design, Algorithmic art", "miniagent_skills"),
            ("Mini-Agent skills: Web search via minimax_search", "miniagent_skills"),
            ("Mini-Agent skills: Memory via knowledge graph", "miniagent_skills"),
            
            # Usage
            ("Mini-Agent max_steps: 100 (configurable)", "miniagent_usage"),
            ("Mini-Agent workspace_dir: ./workspace", "miniagent_usage"),
            ("Mini-Agent retry: Enabled with exponential backoff", "miniagent_usage"),
            ("Mini-Agent retry max: 3 attempts", "miniagent_usage"),
            
            # Common Issues
            ("Mini-Agent error: Check api_key is not placeholder", "miniagent_troubleshooting"),
            ("Mini-Agent error: Verify MCP servers installed", "miniagent_troubleshooting"),
            ("Mini-Agent error: Check network connectivity", "miniagent_troubleshooting"),
            ("Mini-Agent error: Review system_prompt.md", "miniagent_troubleshooting"),
            
            # Commands
            ("Mini-Agent: Start with 'mini-agent' command", "miniagent_commands"),
            ("Mini-Agent: Configuration in ~/.mini-agent/config/", "miniagent_commands"),
        ]
    
    def get_hermes_comprehensive(self):
        """Comprehensive Hermes information."""
        return [
            # Overview
            ("Hermes: OpenClaw state persistence system", "hermes_overview"),
            ("Hermes purpose: Maintain state across sessions", "hermes_overview"),
            ("Hermes location: ~/.local/state/hermes/", "hermes_location"),
            
            # Components
            ("Hermes state files: JSON format", "hermes_components"),
            ("Hermes gateway locks: Coordination mechanism", "hermes_components"),
            ("Hermes sessions: Persistent agent state", "hermes_components"),
            
            # Usage
            ("Hermes read: Read state with read_hermes_state(key)", "hermes_usage"),
            ("Hermes write: Write state with write_hermes_state(key, data)", "hermes_usage"),
            ("Hermes sync: Bidirectional sync with brain", "hermes_usage"),
            
            # Integration
            ("Hermes brain adapter: Bridges Hermes to 7-region brain", "hermes_integration"),
            ("Hermes to brain: Sync state to hippocampal memory", "hermes_integration"),
            ("Hermes from brain: Sync brain status to JSON", "hermes_integration"),
            
            # Best Practices
            ("Hermes: Use for state that must survive restarts", "hermes_best_practices"),
            ("Hermes: Sync frequently for critical state", "hermes_best_practices"),
            ("Hermes: Clean up old state files periodically", "hermes_best_practices"),
            
            # Troubleshooting
            ("Hermes error: Check ~/.local/state/hermes/ exists", "hermes_troubleshooting"),
            ("Hermes error: Verify JSON files are valid", "hermes_troubleshooting"),
            ("Hermes error: Check file permissions", "hermes_troubleshooting"),
        ]
    
    def get_troubleshooting_guide(self):
        """Troubleshooting help information."""
        return [
            # General Help
            ("HELP: Check system status with openclaw status", "help_general"),
            ("HELP: Review logs in ~/.aos/logs/", "help_general"),
            ("HELP: Check brain health at localhost:5000/health", "help_general"),
            
            # Brain Issues
            ("HELP: Brain not responding - Check port 5000", "help_brain"),
            ("HELP: Brain init hangs - Lazy cortical sheet loaded", "help_brain"),
            ("HELP: Brain ticks not increasing - Check stomach queue", "help_brain"),
            
            # Stomach Issues  
            ("HELP: Stomach not digesting - Reduce complexity", "help_stomach"),
            ("HELP: Stomach queue full - Run auto-digest", "help_stomach"),
            ("HELP: Stomach energy low - Feed high nutrition items", "help_stomach"),
            
            # Heart Issues
            ("HELP: Heart stuck - Force beat with heart.beat()", "help_heart"),
            ("HELP: Heart coherence low - Check brain feedback", "help_heart"),
            ("HELP: Heart BPM irregular - Normal in adaptive mode", "help_heart"),
            
            # Integration Issues
            ("HELP: Hermes sync failing - Check JSON validity", "help_integration"),
            ("HELP: MiniMax API error - Verify API key", "help_integration"),
            ("HELP: Mini-Agent not starting - Check config.yaml", "help_integration"),
            
            # Git Issues
            ("HELP: Git push failed - Check credentials", "help_git"),
            ("HELP: Git commit error - Stage files first", "help_git"),
            ("HELP: Merge conflict - Resolve manually", "help_git"),
            
            # Agent Issues
            ("HELP: Mylonen not responding - Reconnect to brain", "help_agents"),
            ("HELP: R2 battery low - Recharge position", "help_agents"),
            ("HELP: Jordan push failed - Check git status", "help_agents"),
        ]
    
    def feed_all_systems(self):
        """Feed all comprehensive information."""
        print("=" * 70)
        print("📚 COMPREHENSIVE SYSTEM FEEDER")
        print("   MiniMax + Mini-Agent + Hermes + Troubleshooting")
        print("=" * 70)
        print()
        
        all_items = []
        
        # MiniMax
        print("Loading MiniMax information...")
        minimax = self.get_minimax_comprehensive()
        all_items.extend([(content, "", "", category) for content, category in minimax])
        print(f"   ✅ {len(minimax)} MiniMax items")
        
        # Mini-Agent
        print("Loading Mini-Agent information...")
        miniagent = self.get_mini_agent_comprehensive()
        all_items.extend([(content, "", "", category) for content, category in miniagent])
        print(f"   ✅ {len(miniagent)} Mini-Agent items")
        
        # Hermes
        print("Loading Hermes information...")
        hermes = self.get_hermes_comprehensive()
        all_items.extend([(content, "", "", category) for content, category in hermes])
        print(f"   ✅ {len(hermes)} Hermes items")
        
        # Troubleshooting
        print("Loading troubleshooting guide...")
        help_items = self.get_troubleshooting_guide()
        all_items.extend([(content, "", "", category) for content, category in help_items])
        print(f"   ✅ {len(help_items)} help items")
        
        total = len(all_items)
        print(f"\n🎯 Total knowledge items: {total}")
        print()
        
        # Feed through pipeline
        print("🍽️ Feeding to stomach-brain pipeline...")
        print("=" * 70)
        result = self.feeder.run_until_empty(all_items)
        
        # Summary
        print("\n" + "=" * 70)
        print("✅ COMPREHENSIVE FEED COMPLETE")
        print("=" * 70)
        print()
        print(f"📊 Results:")
        print(f"   Items fed: {result['fed']}")
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
        
        print("📚 Knowledge by Category:")
        for cat, count in sorted(categories.items()):
            print(f"   - {cat}: {count}")
        
        print()
        print("✅ Brain now has comprehensive knowledge!")
        print("   Ask me about MiniMax, Mini-Agent, or Hermes anytime!")
        print("   I can help troubleshoot issues too!")
        
        return result


def main():
    """Run comprehensive feeder."""
    feeder = ComprehensiveSystemFeeder()
    result = feeder.feed_all_systems()


if __name__ == "__main__":
    main()
