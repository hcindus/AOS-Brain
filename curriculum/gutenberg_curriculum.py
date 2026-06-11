#!/usr/bin/env python3
"""
Project Gutenberg Curriculum Feeder for AGI Company
Extracts foundational texts from priority categories
"""

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Priority reading list - 67 categories committed
CURRICULUM = {
    "tier_1_critical": [
        {
            "category": "Engineering & Technology",
            "priority": 1,
            "focus": ["Mechanical design", "Manufacturing", "Materials science", "Robotics"],
            "sources": [
                {"title": "The Elements of Mechanical Engineering", "author": "Various", "id": "TBD"},
                {"title": "Mechanical Movements and Novelties of Construction", "author": "Gardner D. Hiscox", "id": "TBD"},
                {"title": "Kinematics of Machinery", "author": "Franz Reuleaux", "id": "TBD"},
            ]
        },
        {
            "category": "Philosophy & Ethics",
            "priority": 1,
            "focus": ["AI ethics", "Governance", "Constraints", "Prime Directives"],
            "sources": [
                {"title": "The Republic", "author": "Plato", "id": "150"},
                {"title": "Nicomachean Ethics", "author": "Aristotle", "id": "8438"},
                {"title": "Frankenstein", "author": "Mary Shelley", "id": "84"},
                {"title": "Utilitarianism", "author": "John Stuart Mill", "id": "11224"},
            ]
        },
        {
            "category": "Business/Management",
            "priority": 1,
            "focus": ["Operations", "Leadership", "Organization"],
            "sources": [
                {"title": "The Art of War", "author": "Sun Tzu", "id": "132"},
                {"title": "The Practice of Management", "author": "Peter Drucker", "id": "TBD"},
            ]
        },
        {
            "category": "Mathematics",
            "priority": 1,
            "focus": ["Fractals", "Topology", "Systems"],
            "sources": [
                {"title": "Flatland", "author": "Edwin Abbott", "id": "201"},
                {"title": "The Mathematical Principles of Natural Philosophy", "author": "Isaac Newton", "id": "28233"},
            ]
        },
        {
            "category": "Science - Biology",
            "priority": 1,
            "focus": ["Immune system", "Neural networks", "Biomimicry"],
            "sources": [
                {"title": "On the Origin of Species", "author": "Charles Darwin", "id": "1228"},
                {"title": "The Expression of the Emotions in Man and Animals", "author": "Charles Darwin", "id": "1227"},
            ]
        },
        {
            "category": "Science - Physics",
            "priority": 1,
            "focus": ["Mechanics", "Thermodynamics", "Power systems"],
            "sources": [
                {"title": "The Experimental Physics", "author": "Various", "id": "TBD"},
            ]
        },
        {
            "category": "Psychiatry/Psychology",
            "priority": 1,
            "focus": ["Behavior", "Motivation", "Cognition"],
            "sources": [
                {"title": "The Interpretation of Dreams", "author": "Sigmund Freud", "id": "66048"},
            ]
        },
    ],
    "tier_2_foundation": [
        {
            "category": "Economics",
            "priority": 2,
            "focus": ["Markets", "Resources", "Value"],
            "sources": [
                {"title": "The Wealth of Nations", "author": "Adam Smith", "id": "3300"},
            ]
        },
        {
            "category": "Science-Fiction & Fantasy",
            "priority": 2,
            "focus": ["AI themes", "Utopia/Dystopia", "Future tech"],
            "sources": [
                {"title": "The Time Machine", "author": "H.G. Wells", "id": "35"},
                {"title": "The War of the Worlds", "author": "H.G. Wells", "id": "36"},
                {"title": "R.U.R. (Rossum's Universal Robots)", "author": "Karel Čapek", "id": "TBD"},
            ]
        },
    ]
}

class GutenbergCurriculum:
    """Manages reading curriculum for AGI Company"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.progress_file = output_dir / "reading_progress.json"
        self.progress = self._load_progress()
    
    def _load_progress(self) -> Dict:
        if self.progress_file.exists():
            return json.loads(self.progress_file.read_text())
        return {
            "started": datetime.now().isoformat(),
            "categories_completed": [],
            "texts_read": [],
            "insights_extracted": [],
            "last_update": datetime.now().isoformat()
        }
    
    def _save_progress(self):
        self.progress["last_update"] = datetime.now().isoformat()
        self.progress_file.write_text(json.dumps(self.progress, indent=2))
    
    def get_reading_list(self) -> List[Dict]:
        """Get prioritized reading list"""
        readings = []
        for tier_name, tier in CURRICULUM.items():
            for category in tier:
                readings.append({
                    "tier": tier_name,
                    "category": category["category"],
                    "priority": category["priority"],
                    "focus": category["focus"],
                    "texts": category["sources"]
                })
        return readings
    
    def extract_insights(self, text_info: Dict, content: str) -> List[str]:
        """Extract mission-relevant insights from text"""
        insights = []
        
        # Category-specific extraction
        if text_info["category"] == "Philosophy & Ethics":
            if "govern" in content.lower():
                insights.append("Governance principle found")
            if "constraint" in content.lower():
                insights.append("Constraint concept found")
            if "limit" in content.lower():
                insights.append("Limit concept found")
        
        elif text_info["category"] == "Engineering & Technology":
            if "mechanism" in content.lower():
                insights.append("Mechanical principle found")
            if "material" in content.lower():
                insights.append("Materials science found")
        
        elif text_info["category"] == "Science-Fiction & Fantasy":
            if "robot" in content.lower() or "machine" in content.lower():
                insights.append("AI/robotics theme found")
            if "future" in content.lower():
                insights.append("Future technology concept found")
        
        return insights
    
    def mark_complete(self, text_info: Dict, insights: List[str]):
        """Mark text as read"""
        self.progress["texts_read"].append({
            "title": text_info.get("title", "Unknown"),
            "author": text_info.get("author", "Unknown"),
            "completed": datetime.now().isoformat(),
            "insights": insights
        })
        self.progress["insights_extracted"].extend(insights)
        self._save_progress()
    
    def export_curriculum(self):
        """Export curriculum to workspace"""
        curriculum_file = self.output_dir / "gutenberg_curriculum.json"
        curriculum_file.write_text(json.dumps(CURRICULUM, indent=2))
        
        summary = {
            "total_categories": sum(len(tier) for tier in CURRICULUM.values()),
            "total_texts": sum(len(cat["sources"]) for tier in CURRICULUM.values() for cat in tier),
            "tier_1_texts": sum(len(cat["sources"]) for cat in CURRICULUM["tier_1_critical"]),
            "tier_2_texts": sum(len(cat["sources"]) for cat in CURRICULUM["tier_2_foundation"]),
        }
        
        summary_file = self.output_dir / "curriculum_summary.json"
        summary_file.write_text(json.dumps(summary, indent=2))
        
        return summary

if __name__ == "__main__":
    output = Path("/root/.openclaw/workspace/curriculum/gutenberg")
    curriculum = GutenbergCurriculum(output)
    
    print("="*60)
    print("PROJECT GUTENBERG CURRICULUM FOR AGI COMPANY")
    print("="*60)
    
    # Export curriculum
    summary = curriculum.export_curriculum()
    
    print(f"\n[Summary]")
    print(f"Total categories: {summary['total_categories']}")
    print(f"Total texts: {summary['total_texts']}")
    print(f"Tier 1 (Critical): {summary['tier_1_texts']} texts")
    print(f"Tier 2 (Foundation): {summary['tier_2_texts']} texts")
    
    print(f"\n[Reading List]")
    for reading in curriculum.get_reading_list():
        print(f"\n{reading['category']} (Priority {reading['priority']})")
        print(f"  Focus: {', '.join(reading['focus'][:2])}")
        for text in reading['texts'][:3]:  # Show first 3
            print(f"  - {text['title']} ({text['author']})")
    
    print(f"\n[Output]")
    print(f"  Curriculum: {output / 'gutenberg_curriculum.json'}")
    print(f"  Progress: {output / 'reading_progress.json'}")
    print(f"  Summary: {output / 'curriculum_summary.json'}")
    
    print("\n" + "="*60)
    print("Curriculum established. Ready for ingestion.")
    print("="*60)
