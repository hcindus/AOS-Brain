#!/usr/bin/env python3
"""
TAPTAP AGENT v2.0
Code Review Specialist with MiniMax-M2.5 + Hermes State
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'aos_brain_py'))

from integration.hermes_brain_adapter import HermesBrainAdapter
from integration.mini_agent_minimax import MiniAgentMiniMax
from config.rationed_api_manager import get_ration_manager


class TaptapAgent:
    """
    Code Review Specialist
    Combines: Fast local brain + Hermes state + MiniMax-M2.5
    """
    
    def __init__(self):
        print("=" * 70)
        print("🔍 TAPTAP v2.0 - Code Review Specialist")
        print("=" * 70)
        print()
        
        self.hermes = HermesBrainAdapter()
        self.mini_agent = MiniAgentMiniMax(daily_limit=100)
        self.ration = get_ration_manager(100)
        
        print("✅ Taptap activated")
        print("   - Hermes state tracking")
        print("   - MiniMax-M2.5 deep analysis")
        print("   - API rationing: 100 calls/day")
        print()
    
    def review_code(self, code: str, language: str = "python", deep_analysis: bool = False):
        """Review code with MiniMax enhancement."""
        print(f"[Taptap] Reviewing {language} code...")
        
        # Hermes context
        context = self.hermes.read_hermes_state("taptap_context") or {}
        
        # Fast local review
        local_issues = self._local_review(code, language)
        print(f"   Local analysis: {len(local_issues)} issues")
        
        # MiniMax deep analysis
        minimax_result = None
        if deep_analysis and self.ration.can_make_call("Taptap"):
            print("   Deep analysis via MiniMax-M2.5...")
            
            query = f"""Review this {language} code for security, performance, and best practices:
```{language}
{code[:1000]}
```"""
            
            minimax_result = self.mini_agent.process(query)
            self.ration.record_call("Taptap", 100)
            print(f"   MiniMax complete")
        
        # Update Hermes
        self.hermes.write_hermes_state("taptap_context", {
            "last_review": "2026-03-28",
            "files_reviewed": context.get("files_reviewed", 0) + 1,
            "issues_found": len(local_issues)
        })
        
        return {
            "agent": "Taptap",
            "version": "2.0",
            "local_issues": local_issues,
            "minimax_analysis": minimax_result,
            "language": language
        }
    
    def _local_review(self, code: str, language: str):
        """Fast local pattern matching."""
        issues = []
        if "TODO" in code:
            issues.append({"type": "todo", "message": "TODO found"})
        if "FIXME" in code:
            issues.append({"type": "fixme", "message": "FIXME found"})
        if "print(" in code and language == "python":
            issues.append({"type": "debug", "message": "Debug print found"})
        return issues
    
    def test_activation(self):
        """Test Taptap activation."""
        print("\n🧪 Testing Taptap v2.0")
        print("=" * 70)
        
        test_code = '''
def calculate_sum(numbers):
    # TODO: optimize this
    total = 0
    for n in numbers:
        total += n
    print(f"Sum: {total}")
    return total
'''
        
        print("Test 1: Local review")
        result1 = self.review_code(test_code, "python", deep_analysis=False)
        print(f"   Result: {len(result1['local_issues'])} issues\n")
        
        print("Test 2: Deep analysis")
        result2 = self.review_code(test_code, "python", deep_analysis=True)
        if result2['minimax_analysis']:
            print(f"   MiniMax: Analysis received\n")
        
        print("=" * 70)
        print("✅ TAPTAP v2.0 ACTIVATION COMPLETE")
        print("=" * 70)


def main():
    taptap = TaptapAgent()
    taptap.test_activation()


if __name__ == "__main__":
    main()
