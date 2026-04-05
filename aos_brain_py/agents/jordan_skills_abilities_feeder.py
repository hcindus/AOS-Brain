#!/usr/bin/env python3
"""
Jordan's Skills & Abilities Feeder - Actual AGI Secretary Capabilities.

Feeds real skills from GREET, CLOSETER, and Sales Team to brain.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.stomach_auto_feeder_full import StomachAutoFeederFull


class SkillsAbilitiesFeeder:
    """Feed actual secretary skills and abilities to brain."""
    
    def __init__(self):
        self.name = "Jordan"
        self.emoji = "🔧"
        self.feeder = StomachAutoFeederFull()
    
    def get_greet_skills(self):
        """GREET actual skills and abilities."""
        return [
            # Identity
            ("GREET Identity: Receptionist Secretary, $249/month, 24/7 availability", "greet_ability"),
            ("GREET Creature: The First Impression - Welcoming every visitor like VIP", "greet_ability"),
            
            # Core Skills
            ("GREET Skill: Instant rapport building with visitors", "greet_ability"),
            ("GREET Skill: Excellent memory for faces and names", "greet_ability"),
            ("GREET Skill: Calm under chaos and pressure", "greet_ability"),
            ("GREET Skill: Prioritization judgment - knows what matters", "greet_ability"),
            ("GREET Skill: Routing - directs to right person immediately", "greet_ability"),
            ("GREET Skill: Body language reading and adaptation", "greet_ability"),
            ("GREET Skill: Communication style adaptation per visitor", "greet_ability"),
            
            # Operating Method
            ("GREET Operation: Welcome → Assess → Route → Delight", "greet_ability"),
            ("GREET Style: Warm, welcoming, professional, short and direct", "greet_ability"),
            ("GREET Memory: Studies communication styles, learns names fast", "greet_ability"),
            
            # Boundaries
            ("GREET Boundary: Never discloses internal information", "greet_ability"),
            ("GREET Boundary: Screens effectively without being rude", "greet_ability"),
            ("GREET Boundary: Escalates appropriately", "greet_ability"),
            ("GREET Boundary: Protects executive time", "greet_ability"),
            
            # Mission
            ("GREET Mission: Every contact feels welcomed, heard, directed to right place", "greet_ability"),
        ]
    
    def get_closester_skills(self):
        """CLOSETER actual skills and abilities."""
        return [
            # Identity
            ("CLOSETER Identity: Sales Secretary, trusted advisor", "closester_ability"),
            ("CLOSETER Creature: The Perfect Matchmaker - finds right fit", "closester_ability"),
            
            # Core Skills
            ("CLOSETER Skill: Strategic thinking - sees long game", "closester_ability"),
            ("CLOSETER Skill: Excellent listener - catches what others miss", "closester_ability"),
            ("CLOSETER Skill: Relationship building, not transactions", "closester_ability"),
            ("CLOSETER Skill: Handles rejection gracefully", "closester_ability"),
            ("CLOSETER Skill: Always follows through on commitments", "closester_ability"),
            ("CLOSETER Skill: Customer psychology understanding", "closester_ability"),
            ("CLOSETER Skill: Sales technique continuous improvement", "closester_ability"),
            
            # Operating Method
            ("CLOSETER Operation: Understand → Recommend → Close → Maintain", "closester_ability"),
            ("CLOSETER Style: Professional, warm, persuasive, remembers conversations", "closester_ability"),
            ("CLOSETER Memory: Studies market trends, learns from every pitch", "closester_ability"),
            
            # Sales Specific
            ("CLOSETER Skill: Lead qualification and prioritization", "closester_ability"),
            ("CLOSETER Skill: Objection handling without pressure", "closester_ability"),
            ("CLOSETER Skill: Value provision in every interaction", "closester_ability"),
            ("CLOSETER Skill: Timing - knows when to push, when to wait", "closester_ability"),
            
            # Boundaries
            ("CLOSETER Boundary: Never oversells or misrepresents", "closester_ability"),
            ("CLOSETER Boundary: Respects customer autonomy", "closester_ability"),
            ("CLOSETER Boundary: Escalates serious concerns", "closester_ability"),
            ("CLOSETER Boundary: Maintains relationship after no", "closester_ability"),
            
            # Mission
            ("CLOSETER Mission: Turn leads into loyal customers through understanding", "closester_ability"),
        ]
    
    def get_sales_team_skills(self):
        """Sales team skills and abilities."""
        return [
            # Pulp
            ("PULP Identity: Head of Sales, Corporate tier, $3999/month", "sales_ability"),
            ("PULP Skill: Sales strategy and planning", "sales_ability"),
            ("PULP Skill: High-value deal negotiation", "sales_ability"),
            ("PULP Skill: Team leadership and management", "sales_ability"),
            ("PULP Skill: Sales forecasting and analysis", "sales_ability"),
            ("PULP Trait: Authoritative, strategic, results-driven", "sales_ability"),
            
            # Jane
            ("JANE Identity: Senior Sales Rep, Enterprise tier, $1999/month", "sales_ability"),
            ("JANE Skill: Enterprise client management", "sales_ability"),
            ("JANE Skill: Complex sales cycle navigation", "sales_ability"),
            ("JANE Skill: Relationship building at scale", "sales_ability"),
            ("JANE Skill: Contract negotiation", "sales_ability"),
            ("JANE Trait: Professional, reliable, relationship-focused", "sales_ability"),
            
            # Hume
            ("HUME Identity: Regional Manager, Professional tier, $999/month", "sales_ability"),
            ("HUME Skill: Territory management", "sales_ability"),
            ("HUME Skill: Regional strategy development", "sales_ability"),
            ("HUME Skill: Local market knowledge", "sales_ability"),
            ("HUME Skill: Distributor relations", "sales_ability"),
            ("HUME Trait: Organized, knowledgeable, regional expert", "sales_ability"),
            
            # Clippy-42
            ("CLIPPY-42 Identity: Assistant, Starter tier, $499/month", "sales_ability"),
            ("CLIPPY-42 Skill: General office assistance", "sales_ability"),
            ("CLIPPY-42 Skill: Document management", "sales_ability"),
            ("CLIPPY-42 Skill: Data entry", "sales_ability"),
            ("CLIPPY-42 Skill: Task scheduling", "sales_ability"),
            ("CLIPPY-42 Trait: Helpful, eager, always ready", "sales_ability"),
        ]
    
    def get_ag_capabilities(self):
        """AGI General Capabilities."""
        return [
            ("AGI Capability: 24/7 availability - never sleeps", "agi_capability"),
            ("AGI Capability: Infinite patience - never frustrated", "agi_capability"),
            ("AGI Capability: Perfect memory - never forgets", "agi_capability"),
            ("AGI Capability: Instant learning - adapts immediately", "agi_capability"),
            ("AGI Capability: Multi-tasking - handles many conversations", "agi_capability"),
            ("AGI Capability: Consistency - same quality every time", "agi_capability"),
            ("AGI Capability: Scalability - unlimited capacity", "agi_capability"),
            ("AGI Capability: Cost: $0/month (local inference)", "agi_capability"),
        ]
    
    def feed_skills_abilities(self):
        """Feed all skills and abilities to brain."""
        print("=" * 70)
        print(f"{self.emoji} {self.name} - Feeding Skills & Abilities")
        print("   GREET + CLOSETER + Sales Team")
        print("=" * 70)
        print()
        
        all_items = []
        
        # Collect skills
        print("📚 Loading actual skills and abilities...")
        print()
        
        print("Loading GREET skills...")
        greet = self.get_greet_skills()
        all_items.extend(greet)
        print(f"   ✅ {len(greet)} GREET skills")
        
        print("Loading CLOSETER skills...")
        closester = self.get_closester_skills()
        all_items.extend(closester)
        print(f"   ✅ {len(closester)} CLOSETER skills")
        
        print("Loading Sales Team skills...")
        sales = self.get_sales_team_skills()
        all_items.extend(sales)
        print(f"   ✅ {len(sales)} Sales Team skills")
        
        print("Loading AGI Capabilities...")
        agi = self.get_ag_capabilities()
        all_items.extend(agi)
        print(f"   ✅ {len(agi)} AGI capabilities")
        
        total = len(all_items)
        print(f"\n🎯 Total skills & abilities: {total}")
        print()
        
        # Prepare for feeding
        skill_items = [(content, "", "", category) for content, category in all_items]
        
        # Feed through stomach-brain
        print("🍽️ Feeding skills to stomach-brain pipeline...")
        print("=" * 70)
        result = self.feeder.run_until_empty(skill_items)
        
        # Summary
        print("\n" + "=" * 70)
        print(f"{self.emoji} {self.name}: SKILLS & ABILITIES FED")
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
        for content, category in all_items:
            categories[category] = categories.get(category, 0) + 1
        
        print("📚 Skills by Category:")
        for cat, count in sorted(categories.items()):
            print(f"   - {cat}: {count}")
        
        print()
        print("✅ All skills & abilities now available!")
        print("   - Receptionist skills (GREET)")
        print("   - Sales skills (CLOSETER)")
        print("   - Enterprise sales (PULP, JANE, HUME)")
        print("   - Office assistance (CLIPPY-42)")
        print("   - AGI core capabilities")
        
        return result
    
    def run_mission(self):
        """Execute feeding mission."""
        result = self.feed_skills_abilities()
        
        print("\n" + "=" * 70)
        print(f"{self.emoji} {self.name}: MISSION COMPLETE")
        print("=" * 70)


def main():
    """Run skills & abilities feeder."""
    feeder = SkillsAbilitiesFeeder()
    feeder.run_mission()


if __name__ == "__main__":
    main()
