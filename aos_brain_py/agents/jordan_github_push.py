#!/usr/bin/env python3
"""
Jordan's GitHub Push Mission.

Push all completed integration documents to GitHub.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


class JordanGitHubMission:
    """Jordan pushes integration docs to GitHub."""
    
    def __init__(self):
        self.name = "Jordan"
        self.emoji = "🔧"
        self.workspace = Path("/root/.openclaw/workspace")
        self.repo_path = self.workspace / "aos_brain_py"
        
    def identify(self):
        """Jordan introduces herself."""
        print("=" * 70)
        print(f"{self.emoji} {self.name} - Senior Systems Engineer")
        print("=" * 70)
        print()
        print("Mission: Push integration documents to GitHub")
        print("Status: Starting mission...")
        print()
    
    def check_documents(self):
        """Check which documents are ready to push."""
        print("📋 Checking completed documents...")
        print()
        
        docs = [
            ("docs/INTEGRATION_HUB.md", "Integration Hub - Central documentation"),
            ("docs/HERMES_INTEGRATION.md", "Hermes Integration Guide"),
            ("docs/MINIMAX_INTEGRATION.md", "MiniMax Integration Guide"),
            ("integration/mini_agent_setup.py", "Mini-Agent Setup Script"),
            ("agents/coding_curriculum.py", "Coding Curriculum"),
            ("integration/universal_knowledge_feeder.py", "Universal Knowledge Feeder"),
        ]
        
        found = []
        for doc, description in docs:
            full_path = self.repo_path / doc
            if full_path.exists():
                size = full_path.stat().st_size
                print(f"   ✅ {doc}")
                print(f"      Size: {size} bytes")
                print(f"      Desc: {description}")
                found.append(doc)
            else:
                print(f"   ❌ {doc} - Not found")
        
        print()
        print(f"Found {len(found)} documents ready to push")
        return found
    
    def stage_and_commit(self, documents):
        """Stage documents and commit."""
        print()
        print("📝 Staging documents...")
        
        try:
            # Stage all docs
            subprocess.run(
                ['git', 'add', '-A'],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            print("   ✅ All documents staged")
            
            # Commit
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            commit_msg = f"[{timestamp}] Jordan: Integration docs complete - Hermes, MiniMax, Mini-Agent"
            
            subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            print(f"   ✅ Committed: {commit_msg}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Git error: {e}")
            return False
    
    def push_to_github(self):
        """Push to GitHub."""
        print()
        print("🚀 Pushing to GitHub...")
        
        try:
            result = subprocess.run(
                ['git', 'push', 'origin', 'master'],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            print("   ✅ Successfully pushed to GitHub")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Push failed: {e}")
            if e.stderr:
                print(f"   Error: {e.stderr}")
            return False
    
    def verify_push(self):
        """Verify the push was successful."""
        print()
        print("🔍 Verifying push...")
        
        try:
            # Get latest commit
            result = subprocess.run(
                ['git', 'log', '-1', '--oneline'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                commit = result.stdout.strip()
                print(f"   ✅ Latest commit: {commit}")
                return True
            else:
                print("   ⚠️ Could not verify commit")
                return False
                
        except Exception as e:
            print(f"   ⚠️ Verification issue: {e}")
            return False
    
    def complete_mission(self):
        """Complete the mission."""
        print()
        print("=" * 70)
        print(f"{self.emoji} {self.name}: MISSION COMPLETE")
        print("=" * 70)
        print()
        print("✅ Documents pushed to GitHub:")
        print("   - Integration Hub documentation")
        print("   - Hermes Integration Guide")
        print("   - MiniMax Integration Guide")
        print("   - Mini-Agent Setup Script")
        print("   - Coding Curriculum")
        print("   - Universal Knowledge Feeder")
        print()
        print("Repository: https://github.com/hcindus/AOS-Brain")
        print()
        print(f"{self.emoji} {self.name} signing off.")
        print("=" * 70)
    
    def run_mission(self):
        """Execute complete mission."""
        self.identify()
        
        # Check documents
        documents = self.check_documents()
        
        if not documents:
            print("❌ No documents found to push")
            return
        
        # Stage and commit
        if self.stage_and_commit(documents):
            # Push to GitHub
            if self.push_to_github():
                # Verify
                self.verify_push()
                # Complete
                self.complete_mission()
            else:
                print("\n❌ Push failed - mission incomplete")
        else:
            print("\n❌ Commit failed - mission incomplete")


if __name__ == "__main__":
    jordan = JordanGitHubMission()
    jordan.run_mission()
