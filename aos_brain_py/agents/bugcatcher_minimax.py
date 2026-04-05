#!/usr/bin/env python3
"""
BUGCATCHER AGENT v2.0
Debug Specialist with MiniMax-M2.5/M2.7 + Hermes State
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'aos_brain_py'))

from integration.hermes_brain_adapter import HermesBrainAdapter
from integration.mini_agent_minimax import MiniAgentMiniMax
from config.rationed_api_manager import get_ration_manager


class BugcatcherAgent:
    """
    Debug Specialist
    Combines: Error pattern recognition + Hermes history + MiniMax reasoning
    """
    
    def __init__(self):
        print("=" * 70)
        print("🐛 BUGCATCHER v2.0 - Debug Specialist")
        print("=" * 70)
        print()
        
        self.hermes = HermesBrainAdapter()
        self.mini_agent = MiniAgentMiniMax(daily_limit=100)
        self.ration = get_ration_manager(100)
        
        print("✅ Bugcatcher activated")
        print("   - Hermes error history")
        print("   - MiniMax-M2.5/M2.7 debugging")
        print("   - Stack trace analysis")
        print()
    
    def debug_error(self, error: str, stack_trace: str = "", code: str = ""):
        """Debug error with MiniMax reasoning."""
        print(f"[Bugcatcher] Debugging error...")
        
        # Check Hermes for similar errors
        history = self.hermes.read_hermes_state("bug_history") or {}
        similar = history.get("similar_errors", [])
        
        if similar:
            print(f"   Found {len(similar)} similar errors in history")
        
        # Use MiniMax-M2.7 for complex debugging
        if self.ration.can_make_call("Bugcatcher"):
            print("   Deep analysis via MiniMax-M2.7...")
            
            query = f"""Debug this error:

Error: {error}

Stack trace:
{stack_trace[:500]}

Code context:
{code[:300]}

Analyze:
1. Root cause
2. Fix approach
3. Prevention"""
            
            result = self.mini_agent.process(
                query,
                system="You are an expert debugger. Analyze thoroughly."
            )
            
            self.ration.record_call("Bugcatcher", result.get('usage', {}).get('output_tokens', 100))
            
            # Update Hermes
            self.hermes.write_hermes_state("bug_history", {
                "similar_errors": similar + [{"error": error[:100], "date": "2026-03-28"}]
            })
            
            return result
        
        return {"text": "Ration limit reached", "source": "local"}
    
    def test_activation(self):
        """Test Bugcatcher activation."""
        print("\n🧪 Testing Bugcatcher v2.0")
        print("=" * 70)
        
        error = "TypeError: Cannot read property 'length' of undefined"
        stack = """TypeError: Cannot read property 'length' of undefined
    at processData (data.js:42)
    at main (app.js:15)"""
        
        result = self.debug_error(error, stack)
        
        print(f"\nAnalysis received")
        tokens = result.get('usage', {}).get('output_tokens', 100)
        print(f"Tokens: {tokens}")
        
        print("\n" + "=" * 70)
        print("✅ BUGCATCHER v2.0 ACTIVATION COMPLETE")
        print("=" * 70)


def main():
    bugcatcher = BugcatcherAgent()
    bugcatcher.test_activation()


if __name__ == "__main__":
    main()
