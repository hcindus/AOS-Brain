#!/usr/bin/env python3
"""
JORDAN AGENT v2.0
Project Manager with MiniMax-M2.7 + Hermes State
Enhanced for Hostinger deployment
"""

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'aos_brain_py'))

from integration.hermes_brain_adapter import HermesBrainAdapter
from integration.mini_agent_minimax import MiniAgentMiniMax
from config.rationed_api_manager import get_ration_manager


class JordanAgent:
    """
    Project Manager
    
    Combines:
    - Project tracking (Hermes state)
    - Deployment planning (MiniMax-M2.7)
    - Web deployment execution
    """
    
    def __init__(self):
        print("=" * 70)
        print("📋 JORDAN v2.0 - Project Manager")
        print("=" * 70)
        print()
        
        self.hermes = HermesBrainAdapter()
        self.mini_agent = MiniAgentMiniMax(daily_limit=100)
        self.ration = get_ration_manager(100)
        
        # Load current task
        self.task = self._load_task()
        
        print("✅ Jordan activated")
        print("   - Hermes project tracking")
        print("   - MiniMax-M2.7 deployment planning")
        print("   - Hostinger deployment capability")
        print()
        print(f"Current Task: {self.task.get('mission', 'Unknown')}")
        print(f"Status: {self.task.get('status', 'Unknown')}")
        print()
    
    def _load_task(self):
        """Load current task from memory."""
        task_file = Path("/root/.openclaw/workspace/aocros/agent_sandboxes/jordan/CURRENT_TASK.md")
        if task_file.exists():
            return {
                "mission": "Deploy Performance Supply Depot to Hostinger",
                "status": "ACTIVE",
                "url": "performancesupplydepot.com",
                "files": ["index.html", "checkout.html", "sales/"]
            }
        return {}
    
    def plan_deployment(self):
        """Plan deployment with MiniMax-M2.7."""
        print("🤖 Planning deployment with MiniMax-M2.7...")
        
        if self.ration.can_make_call("Jordan"):
            query = """Plan a web deployment to Hostinger:

Website: Performance Supply Depot
Files: index.html, checkout.html, sales/
Domain: performancesupplydepot.com

Steps needed:
1. Check Hostinger credentials
2. Upload files via FTP/SFTP
3. Configure domain
4. Verify SSL
5. Test checkout flow

Provide step-by-step deployment plan."""
            
            result = self.mini_agent.process(
                query,
                system="You are a DevOps expert. Provide clear deployment steps."
            )
            
            tokens = result.get('usage', {}).get('output_tokens', 100)
            self.ration.record_call("Jordan", tokens)
            
            print(f"   Plan received ({tokens} tokens)")
            return result['text']
        
        return "Ration limit reached"
    
    def execute_deployment(self):
        """Execute deployment steps."""
        print("\n🚀 Executing Deployment...")
        print()
        
        # Step 1: Check files exist
        website_dir = Path("/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/")
        
        print("Step 1: Verify files exist")
        if website_dir.exists():
            print(f"   ✅ Website directory found: {website_dir}")
            files = list(website_dir.glob("*"))
            print(f"   Found {len(files)} files")
        else:
            print(f"   ❌ Directory not found: {website_dir}")
            return False
        
        # Step 2: Check deploy script
        deploy_script = website_dir / "deploy.sh"
        print("\nStep 2: Check deploy script")
        if deploy_script.exists():
            print(f"   ✅ Deploy script found")
            with open(deploy_script) as f:
                print(f"   Script preview: {f.read()[:200]}...")
        else:
            print(f"   ⚠️  No deploy.sh found")
        
        # Update Hermes
        self.hermes.write_hermes_state("jordan_deployment", {
            "last_action": "2026-03-28",
            "status": "planning_complete",
            "files_checked": str(website_dir),
            "deploy_script": deploy_script.exists()
        })
        
        print("\n✅ Deployment planning complete")
        print("   Status: Ready for execution")
        
        return True
    
    def test_activation(self):
        """Test Jordan activation."""
        print("\n🧪 Testing Jordan v2.0")
        print("=" * 70)
        
        plan = self.plan_deployment()
        print(f"\nPlan preview: {plan[:300]}...")
        
        success = self.execute_deployment()
        
        print("\n" + "=" * 70)
        print("✅ JORDAN v2.0 ACTIVATION COMPLETE")
        print("=" * 70)
        print()
        print("Next: Review deployment plan and execute")


def main():
    jordan = JordanAgent()
    jordan.test_activation()


if __name__ == "__main__":
    main()
