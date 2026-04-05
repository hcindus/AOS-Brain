#!/usr/bin/env python3
"""
Skill Consumer - Consume skills from Hermes and Mini-Agent.

Reads skill definitions and feeds them to stomach-brain pipeline.
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.stomach_auto_feeder_full import StomachAutoFeederFull


class SkillConsumer:
    """Consume skills and feed to brain."""
    
    def __init__(self):
        self.feeder = StomachAutoFeederFull()
        
        # Hermes skills (state-based)
        self.hermes_skills = self._load_hermes_skills()
        
        # Mini-Agent skills (from system prompt)
        self.mini_agent_skills = self._load_mini_agent_skills()
        
    def _load_hermes_skills(self) -> List[Tuple[str, str]]:
        """Load Hermes skills from memory/state."""
        # Hermes provides state persistence skills
        skills = [
            ("Hermes: State Persistence", "hermes_skill"),
            ("Hermes: Session Management", "hermes_skill"),
            ("Hermes: Agent Coordination", "hermes_skill"),
            ("Hermes: Gateway Locking", "hermes_skill"),
            ("Hermes: Distributed State", "hermes_skill"),
            ("Hermes: JSON State Files", "hermes_skill"),
            ("Hermes: Bidirectional Sync", "hermes_skill"),
            ("Hermes: State Mirroring", "hermes_skill"),
        ]
        return skills
    
    def _load_mini_agent_skills(self) -> List[Tuple[str, str]]:
        """Load Mini-Agent skills from configuration."""
        # From system_prompt.md analysis
        skills = [
            # Basic Tools
            ("Mini-Agent: File Operations - Read/Write/Edit files", "miniagent_skill"),
            ("Mini-Agent: Bash Execution - Run commands, manage git", "miniagent_skill"),
            ("Mini-Agent: MCP Tools - Access Model Context Protocol servers", "miniagent_skill"),
            
            # Specialized Skills
            ("Mini-Agent: PDF Processing - Extract text, analyze documents", "miniagent_skill"),
            ("Mini-Agent: PowerPoint - Create presentations, slides", "miniagent_skill"),
            ("Mini-Agent: Word Documents - Docx creation, editing", "miniagent_skill"),
            ("Mini-Agent: Excel - Spreadsheets, data analysis", "miniagent_skill"),
            ("Mini-Agent: Canvas Design - Visual layouts, graphics", "miniagent_skill"),
            ("Mini-Agent: Algorithmic Art - Generative art creation", "miniagent_skill"),
            
            # Web Search
            ("Mini-Agent: MiniMax Search - Web search and browsing", "miniagent_skill"),
            ("Mini-Agent: Memory MCP - Knowledge graph memory", "miniagent_skill"),
            
            # Task Management
            ("Mini-Agent: Task Analysis - Break down complex tasks", "miniagent_skill"),
            ("Mini-Agent: Skill Loading - Progressive skill disclosure", "miniagent_skill"),
            ("Mini-Agent: Python Environment - Setup and management", "miniagent_skill"),
            
            # API Integration
            ("Mini-Agent: MiniMax API - AI model integration", "miniagent_skill"),
            ("Mini-Agent: Retry Logic - Exponential backoff", "miniagent_skill"),
        ]
        return skills
    
    def _load_aocros_skills(self) -> List[Tuple[str, str]]:
        """Load existing AOCROS agent skills from their skill directories."""
        skills = []
        
        # Scan aocros skills
        aocros_skills_dir = Path("/root/.openclaw/workspace/aocros/skills")
        if aocros_skills_dir.exists():
            for skill_file in aocros_skills_dir.glob("*.py"):
                skill_name = skill_file.stem
                skills.append((f"AOCROS Skill: {skill_name}", "aocros_skill"))
        
        return skills
    
    def consume_all_skills(self):
        """Consume all skills through stomach-brain pipeline."""
        print("=" * 70)
        print("🍽️ SKILL CONSUMER - Hermes + Mini-Agent")
        print("=" * 70)
        print()
        
        # Collect all skills
        all_skills = []
        
        print("📚 Loading Hermes skills...")
        hermes = self.hermes_skills
        all_skills.extend(hermes)
        print(f"   ✓ {len(hermes)} Hermes skills loaded")
        
        print("📚 Loading Mini-Agent skills...")
        mini = self.mini_agent_skills
        all_skills.extend(mini)
        print(f"   ✓ {len(mini)} Mini-Agent skills loaded")
        
        print("📚 Loading AOCROS skills...")
        aocros = self._load_aocros_skills()
        all_skills.extend(aocros)
        print(f"   ✓ {len(aocros)} AOCROS skills loaded")
        
        total = len(all_skills)
        print(f"\n🎯 Total skills to consume: {total}")
        print()
        
        # Prepare for feeding
        skill_items = [(content, "", "", category) for content, category in all_skills]
        
        # Feed through stomach-brain pipeline
        print("🍽️ Consuming skills through stomach-brain pipeline...")
        print("=" * 70)
        result = self.feeder.run_until_empty(skill_items)
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 SKILL CONSUMPTION COMPLETE")
        print("=" * 70)
        print()
        print(f"Skills consumed: {result['fed']}")
        print(f"Digested to brain: {result['digested']}")
        print(f"Efficiency: {result['efficiency']:.1f}%")
        print()
        print(f"Brain state:")
        print(f"  Ticks: {result['brain_ticks']}")
        print(f"  Clusters: {result['brain_clusters']}")
        print()
        
        # Show by category
        categories = {}
        for content, category in all_skills:
            categories[category] = categories.get(category, 0) + 1
        
        print("📚 Skills by Source:")
        for cat, count in sorted(categories.items()):
            print(f"  - {cat}: {count} skills")
        
        print()
        if result['efficiency'] == 100.0:
            print("✅ PERFECT CONSUMPTION: All skills learned!")
        
        return result


def main():
    """Run skill consumer."""
    consumer = SkillConsumer()
    result = consumer.consume_all_skills()
    
    print("\n" + "=" * 70)
    print("🎓 SKILL CONSUMER COMPLETE")
    print("=" * 70)
    print()
    print("The brain has now learned:")
    print("  ✅ Hermes state persistence skills")
    print("  ✅ Mini-Agent tool capabilities")
    print("  ✅ MCP server integrations")
    print("  ✅ AOCROS agent specializations")
    print()
    print("Ready to use these skills in future operations!")


if __name__ == "__main__":
    main()
