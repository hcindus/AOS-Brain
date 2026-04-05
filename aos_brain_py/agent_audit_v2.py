#!/usr/bin/env python3
"""
AGENT AUDIT TOOL - Fixed Path
Verify brain integration and fallback hierarchy
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

class AgentAuditor:
    """Audit all agents for proper brain/fallback configuration."""
    
    def __init__(self):
        self.issues = []
        self.verified = []
        self.base_path = Path(__file__).parent
        
    def audit_agent(self, name, file_path, expected_brain=True):
        """Audit a single agent."""
        print(f"\n🔍 Auditing: {name}")
        print(f"   File: {file_path}")
        
        checks = {
            "has_brain_import": False,
            "has_fallback": False,
            "uses_local_first": False,
            "has_rationing": False
        }
        
        try:
            # Read source
            full_path = self.base_path / file_path
            if not full_path.exists():
                print(f"   ❌ File not found: {full_path}")
                self.issues.append({"name": name, "error": f"File not found: {file_path}"})
                return
                
            with open(full_path) as f:
                source = f.read()
            
            # Check 1: Brain import
            if "SevenRegionBrain" in source or "from brain" in source or "brain =" in source.lower():
                checks["has_brain_import"] = True
                print("  ✅ Brain integration")
            else:
                print("  ⚠️  No brain import")
            
            # Check 2: Fallback mechanism
            if "fallback" in source.lower() or "can_make_call" in source or "ration" in source.lower():
                checks["has_fallback"] = True
                print("  ✅ Fallback/rationing")
            else:
                print("  ⚠️  No fallback mechanism")
            
            # Check 3: Local first
            if "local" in source.lower() or "brain.tick" in source or "Hermes" in source:
                checks["uses_local_first"] = True
                print("  ✅ Local/Hermes usage")
            else:
                print("  ⚠️  May not use local first")
            
            # Check 4: Rationing
            if "ration" in source.lower() or "daily_limit" in source:
                checks["has_rationing"] = True
                print("  ✅ API rationing")
            else:
                print("  ⚠️  No rationing")
            
            # Verify
            score = sum(checks.values())
            if score >= 3:
                self.verified.append({
                    "name": name,
                    "checks": checks,
                    "score": score
                })
                print(f"  ✅ {name} VERIFIED ({score}/4)")
            else:
                self.issues.append({
                    "name": name,
                    "checks": checks,
                    "score": score,
                    "missing": [k for k, v in checks.items() if not v]
                })
                print(f"  ⚠️  {name} needs work ({score}/4)")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            self.issues.append({"name": name, "error": str(e)})
    
    def run_full_audit(self):
        """Run audit on all agents."""
        print("=" * 70)
        print("🔍 AGENT AUDIT: Brain Integration & Fallback")
        print("=" * 70)
        print(f"Base path: {self.base_path}")
        print()
        
        agents = [
            ("R2-D2", "agents/r2_brain_adapter.py"),
            ("Taptap", "agents/taptap_minimax.py"),
            ("Bugcatcher", "agents/bugcatcher_minimax.py"),
            ("Jordan", "agents/jordan_minimax.py"),
            ("Mylonen", "agents/mylonen_adapter.py"),
            ("Cryptonio", "agents/cryptonio_brain_adapter.py"),
            ("Mini-Agent", "integration/mini_agent_minimax.py"),
        ]
        
        for name, file in agents:
            self.audit_agent(name, file)
        
        # Report
        print("\n" + "=" * 70)
        print("📊 AUDIT RESULTS")
        print("=" * 70)
        print()
        
        print(f"✅ VERIFIED ({len(self.verified)}):")
        for v in self.verified:
            print(f"   {v['name']} ({v['score']}/4 checks)")
        
        if self.issues:
            print(f"\n⚠️  NEEDS ATTENTION ({len(self.issues)}):")
            for i in self.issues:
                if "error" in i:
                    print(f"   {i['name']}: {i['error']}")
                else:
                    print(f"   {i['name']}: {i['score']}/4 - Missing: {', '.join(i['missing'])}")
        
        print()
        print("=" * 70)
        print("✅ AUDIT COMPLETE")
        print("=" * 70)


def main():
    auditor = AgentAuditor()
    auditor.run_full_audit()


if __name__ == "__main__":
    main()
