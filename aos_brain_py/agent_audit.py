#!/usr/bin/env python3
"""
AGENT AUDIT TOOL
Verify brain integration and fallback hierarchy
"""

import sys
from pathlib import Path
import inspect

sys.path.insert(0, str(Path(__file__).parent))

class AgentAuditor:
    """Audit all agents for proper brain/fallback configuration."""
    
    def __init__(self):
        self.issues = []
        self.verified = []
        
    def audit_agent(self, name, module_path, expected_brain=True):
        """Audit a single agent."""
        print(f"\n🔍 Auditing: {name}")
        
        checks = {
            "has_brain_import": False,
            "has_fallback": False,
            "uses_local_first": False,
            "has_rationing": False
        }
        
        try:
            # Read source
            with open(module_path) as f:
                source = f.read()
            
            # Check 1: Brain import
            if "SevenRegionBrain" in source or "from brain" in source:
                checks["has_brain_import"] = True
                print("  ✅ Brain import found")
            else:
                print("  ⚠️  No brain import")
            
            # Check 2: Fallback mechanism
            if "fallback" in source.lower() or "can_make_call" in source:
                checks["has_fallback"] = True
                print("  ✅ Fallback mechanism found")
            else:
                print("  ⚠️  No fallback mechanism")
            
            # Check 3: Local first
            if "local" in source.lower() or "brain.tick" in source:
                checks["uses_local_first"] = True
                print("  ✅ Local brain usage found")
            else:
                print("  ⚠️  May not use local brain first")
            
            # Check 4: Rationing
            if "ration" in source.lower():
                checks["has_rationing"] = True
                print("  ✅ API rationing found")
            else:
                print("  ⚠️  No rationing detected")
            
            # Verify
            if all(checks.values()):
                self.verified.append({
                    "name": name,
                    "checks": checks
                })
                print(f"  ✅ {name} FULLY VERIFIED")
            else:
                self.issues.append({
                    "name": name,
                    "checks": checks,
                    "missing": [k for k, v in checks.items() if not v]
                })
                print(f"  ⚠️  {name} needs attention")
                
        except Exception as e:
            print(f"  ❌ Error auditing {name}: {e}")
            self.issues.append({"name": name, "error": str(e)})
    
    def run_full_audit(self):
        """Run audit on all agents."""
        print("=" * 70)
        print("🔍 AGENT AUDIT: Brain Integration & Fallback Hierarchy")
        print("=" * 70)
        
        agents = [
            ("R2-D2", "r2_brain_adapter.py"),
            ("Taptap", "taptap_minimax.py"),
            ("Bugcatcher", "bugcatcher_minimax.py"),
            ("Jordan", "jordan_minimax.py"),
            ("Mylonen", "mylonen_adapter.py"),
            ("Cryptonio", "cryptonio_brain_adapter.py"),
        ]
        
        for name, file in agents:
            path = Path(__file__).parent / file
            if path.exists():
                self.audit_agent(name, path)
            else:
                print(f"\n⚠️  {name}: File not found ({file})")
        
        # Report
        print("\n" + "=" * 70)
        print("📊 AUDIT RESULTS")
        print("=" * 70)
        print()
        
        print(f"✅ VERIFIED ({len(self.verified)}):")
        for v in self.verified:
            print(f"   {v['name']}")
        
        if self.issues:
            print(f"\n⚠️  NEEDS ATTENTION ({len(self.issues)}):")
            for i in self.issues:
                if "error" in i:
                    print(f"   {i['name']}: ERROR - {i['error']}")
                else:
                    print(f"   {i['name']}: Missing {', '.join(i['missing'])}")
        else:
            print("\n✅ ALL AGENTS VERIFIED")


def main():
    auditor = AgentAuditor()
    auditor.run_full_audit()


if __name__ == "__main__":
    main()
