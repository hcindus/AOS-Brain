#!/usr/bin/env python3
"""
Mylonen + R2 GitHub Log Cleanup Mission.

Fetch logs from GitHub, consume through stomach-brain pipeline, consolidate.
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.mylonen_adapter import MylonenAdapter
from agents.droid_r2 import R2DroidInterface
from integration.stomach_auto_feeder_full import StomachAutoFeederFull


class GitHubLogCleanupMission:
    """Mylonen + R2 mission to consume and clean up GitHub logs."""
    
    def __init__(self):
        self.mylonen = MylonenAdapter()
        self.r2 = R2DroidInterface()
        self.feeder = StomachAutoFeederFull()
        
        # Mission log
        self.mission_log = []
        
    def fetch_git_logs(self):
        """Fetch git commit logs."""
        print("🛸 R2: Fetching GitHub logs...")
        
        # Scan for logs
        self.r2.scan_environment()
        
        try:
            # Get git log
            result = subprocess.run(
                ['git', 'log', '--oneline', '-30', '--pretty=format:%h %s'],
                capture_output=True,
                text=True,
                cwd='/root/.openclaw/workspace/aos_brain_py'
            )
            
            logs = result.stdout.strip().split('\n')
            print(f"   ✓ Found {len(logs)} commits")
            
            return logs
        except Exception as e:
            print(f"   ⚠️ Error fetching logs: {e}")
            return []
    
    def process_logs_with_stomach(self, logs):
        """Process logs through stomach-brain pipeline."""
        print("\n🍽️ Consuming logs through stomach-brain pipeline...")
        
        # Prepare logs for consumption
        log_items = []
        for log in logs:
            if log.strip():
                log_items.append((log.strip(), "", "", "git_log"))
        
        # Feed through stomach-brain pipeline
        if log_items:
            result = self.feeder.run_until_empty(log_items)
            return result
        
        return None
    
    def consolidate_logs(self, logs):
        """R2 consolidates logs into summary."""
        print("\n🛸 R2: Consolidating logs...")
        
        # Deploy data processing tool
        self.r2.deploy_tool("data_processor")
        
        # Categorize logs
        categories = {
            "brain_fixes": [],
            "integrations": [],
            "feeders": [],
            "agents": [],
            "infrastructure": []
        }
        
        for log in logs:
            log_lower = log.lower()
            if "fix" in log_lower or "brain" in log_lower:
                categories["brain_fixes"].append(log)
            elif "integrat" in log_lower or "hermes" in log_lower or "minimax" in log_lower:
                categories["integrations"].append(log)
            elif "feed" in log_lower or "stomach" in log_lower or "digest" in log_lower:
                categories["feeders"].append(log)
            elif "agent" in log_lower or "mylonen" in log_lower or "r2" in log_lower or "droid" in log_lower:
                categories["agents"].append(log)
            else:
                categories["infrastructure"].append(log)
        
        # Create summary
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_commits": len(logs),
            "categories": {k: len(v) for k, v in categories.items()},
            "recent_activity": logs[:5]
        }
        
        print(f"   ✓ Consolidated into {len(categories)} categories")
        for cat, count in summary["categories"].items():
            print(f"     - {cat}: {count} commits")
        
        return summary
    
    def save_consolidated_log(self, summary):
        """Save consolidated log to file."""
        print("\n💾 Saving consolidated log...")
        
        log_file = Path("/root/.openclaw/workspace/aos_brain_py/logs/consolidated_github_log.json")
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"   ✓ Saved to: {log_file}")
        
        return str(log_file)
    
    def cleanup_dusty_logs(self):
        """Clean up old/temp log files."""
        print("\n🧹 Cleaning up dusty logs...")
        
        log_dir = Path("/root/.openclaw/workspace/aos_brain_py/logs")
        if not log_dir.exists():
            print("   ✓ No dusty logs found")
            return 0
        
        cleaned = 0
        for log_file in log_dir.glob("*.tmp"):
            log_file.unlink()
            cleaned += 1
        
        for log_file in log_dir.glob("*backup*"):
            log_file.unlink()
            cleaned += 1
        
        print(f"   ✓ Cleaned up {cleaned} dusty log files")
        return cleaned
    
    def run_mission(self):
        """Execute complete log cleanup mission."""
        print("=" * 70)
        print("🤖🛸 MYLONEN + R2: GITHUB LOG CLEANUP MISSION")
        print("=" * 70)
        print()
        
        # Step 1: Fetch logs
        logs = self.fetch_git_logs()
        if not logs:
            print("❌ No logs to process")
            return
        
        # Step 2: Process through stomach-brain
        result = self.process_logs_with_stomach(logs)
        
        # Step 3: Consolidate
        summary = self.consolidate_logs(logs)
        
        # Step 4: Save
        log_path = self.save_consolidated_log(summary)
        
        # Step 5: Cleanup
        cleaned = self.cleanup_dusty_logs()
        
        # Final report
        print("\n" + "=" * 70)
        print("📊 MISSION COMPLETE")
        print("=" * 70)
        print()
        print(f"🤖 Mylonen processed {len(logs)} logs")
        print(f"🍽️ Stomach digested: {result['digested'] if result else 0} items")
        print(f"🧠 Brain clusters: {result['brain_clusters'] if result else 0}")
        print(f"🛸 R2 consolidated into {len(summary['categories'])} categories")
        print(f"💾 Saved to: {log_path}")
        print(f"🧹 Cleaned up {cleaned} dusty files")
        
        # Commit to GitHub
        print("\n📤 Committing to GitHub...")
        try:
            subprocess.run(['git', 'add', 'logs/'], cwd='/root/.openclaw/workspace/aos_brain_py', check=True)
            subprocess.run(['git', 'commit', '-m', '[2026-03-28] Consolidated GitHub logs by Mylonen+R2'], 
                         cwd='/root/.openclaw/workspace/aos_brain_py', check=True)
            subprocess.run(['git', 'push', 'origin', 'master'], 
                         cwd='/root/.openclaw/workspace/aos_brain_py', check=True)
            print("   ✓ Committed and pushed to GitHub")
        except Exception as e:
            print(f"   ⚠️ Git commit issue: {e}")
        
        print("\n✅ GITHUB LOG CLEANUP MISSION COMPLETE")
        print("=" * 70)


if __name__ == "__main__":
    mission = GitHubLogCleanupMission()
    mission.run_mission()
