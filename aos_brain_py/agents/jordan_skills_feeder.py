#!/usr/bin/env python3
"""
Jordan's GitHub Skills Feeder.

Feeds ALL skills from GitHub repository to stomach-brain pipeline.
Makes skills available for all linked agents.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.stomach_auto_feeder_full import StomachAutoFeederFull


class JordanSkillsFeeder:
    """Jordan feeds all GitHub skills to the brain."""
    
    def __init__(self):
        self.name = "Jordan"
        self.emoji = "🔧"
        self.feeder = StomachAutoFeederFull()
        self.workspace = Path("/root/.openclaw/workspace")
        
    def identify(self):
        """Jordan introduces herself."""
        print("=" * 70)
        print(f"{self.emoji} {self.name} - Feeding GitHub Skills to Brain")
        print("=" * 70)
        print()
        
    def collect_integration_skills(self) -> List[Tuple[str, str]]:
        """Collect skills from aos_brain_py integration."""
        skills = []
        
        integration_dir = self.workspace / "aos_brain_py" / "integration"
        if integration_dir.exists():
            for py_file in integration_dir.glob("*.py"):
                skill_name = py_file.stem
                skills.append((
                    f"Integration Skill: {skill_name} - "
                    f"Stomach-brain pipeline adapter for {skill_name}",
                    "integration_skill"
                ))
        
        return skills
    
    def collect_agent_skills(self) -> List[Tuple[str, str]]:
        """Collect skills from agents."""
        skills = []
        
        agents_dir = self.workspace / "aos_brain_py" / "agents"
        if agents_dir.exists():
            for py_file in agents_dir.glob("*.py"):
                skill_name = py_file.stem
                skills.append((
                    f"Agent Skill: {skill_name} - "
                    f"Autonomous agent capability: {skill_name}",
                    "agent_skill"
                ))
        
        return skills
    
    def collect_docs(self) -> List[Tuple[str, str]]:
        """Collect documentation as knowledge."""
        skills = []
        
        docs_dir = self.workspace / "aos_brain_py" / "docs"
        if docs_dir.exists():
            for md_file in docs_dir.glob("*.md"):
                doc_name = md_file.stem
                skills.append((
                    f"Documentation: {doc_name} - "
                    f"Integration guide for {doc_name}",
                    "documentation"
                ))
        
        return skills
    
    def collect_aocros_skills(self) -> List[Tuple[str, str]]:
        """Collect AOCROS skills."""
        skills = []
        
        aocros_dir = self.workspace / "aocros" / "skills"
        if aocros_dir.exists():
            for skill_file in aocros_dir.glob("*.py"):
                skill_name = skill_file.stem
                skills.append((
                    f"AOCROS Skill: {skill_name} - "
                    f"Company skill: {skill_name}",
                    "aocros_skill"
                ))
        
        return skills
    
    def feed_all_skills(self):
        """Feed all collected skills to stomach-brain."""
        self.identify()
        
        all_skills = []
        
        print("📚 Collecting skills from GitHub...")
        print()
        
        # Integration skills
        integration = self.collect_integration_skills()
        all_skills.extend(integration)
        print(f"   ✅ Integration skills: {len(integration)}")
        
        # Agent skills
        agents = self.collect_agent_skills()
        all_skills.extend(agents)
        print(f"   ✅ Agent skills: {len(agents)}")
        
        # Documentation
        docs = self.collect_docs()
        all_skills.extend(docs)
        print(f"   ✅ Documentation: {len(docs)}")
        
        # AOCROS skills
        aocros = self.collect_aocros_skills()
        all_skills.extend(aocros)
        print(f"   ✅ AOCROS skills: {len(aocros)}")
        
        total = len(all_skills)
        print(f"\n🎯 Total skills to feed: {total}")
        print()
        
        # Prepare for feeding
        skill_items = [(content, "", "", category) for content, category in all_skills]
        
        # Feed through stomach-brain
        print("🍽️ Feeding skills to stomach-brain pipeline...")
        print("=" * 70)
        result = self.feeder.run_until_empty(skill_items)
        
        # Summary
        print("\n" + "=" * 70)
        print(f"{self.emoji} {self.name}: SKILLS FEEDING COMPLETE")
        print("=" * 70)
        print()
        print(f"📊 Results:")
        print(f"   Skills fed: {result['fed']}")
        print(f"   Digested: {result['digested']}")
        print(f"   Efficiency: {result['efficiency']:.1f}%")
        print()
        print(f"🧠 Brain State:")
        print(f"   Ticks: {result['brain_ticks']}")
        print(f"   Clusters: {result['brain_clusters']}")
        print()
        
        # Categories
        categories = {}
        for content, category in all_skills:
            categories[category] = categories.get(category, 0) + 1
        
        print("📚 Skills by Category:")
        for cat, count in sorted(categories.items()):
            print(f"   - {cat}: {count}")
        
        print()
        print("✅ All skills now available for linked agents!")
        print("   - Mylonen can use these skills")
        print("   - R2 can use these skills")
        print("   - Any agent connected to brain has access")
        print()
        
        return result
    
    def commit_to_github(self):
        """Commit the skill feeding results."""
        print("📤 Committing to GitHub...")
        
        try:
            subprocess.run(
                ['git', 'add', '-A'],
                cwd=self.workspace / "aos_brain_py",
                check=True,
                capture_output=True
            )
            
            subprocess.run(
                ['git', 'commit', '-m', '[2026-03-28] Jordan: All GitHub skills fed to brain'],
                cwd=self.workspace / "aos_brain_py",
                check=True,
                capture_output=True
            )
            
            subprocess.run(
                ['git', 'push', 'origin', 'master'],
                cwd=self.workspace / "aos_brain_py",
                check=True,
                capture_output=True
            )
            
            print("   ✅ Committed and pushed to GitHub")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ Git status: {e}")
            return False
    
    def run_mission(self):
        """Execute complete feeding mission."""
        result = self.feed_all_skills()
        self.commit_to_github()
        
        print("=" * 70)
        print(f"{self.emoji} {self.name}: MISSION COMPLETE")
        print("=" * 70)


def main():
    """Run Jordan's skill feeding mission."""
    jordan = JordanSkillsFeeder()
    jordan.run_mission()


if __name__ == "__main__":
    main()
