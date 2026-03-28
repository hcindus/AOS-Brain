#!/usr/bin/env python3
"""
Jordan's Secretarial Pool Feeder.

Feeds all AGI Secretaries (GREET, CLOSETER, etc.) to stomach-brain pipeline.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.stomach_auto_feeder_full import StomachAutoFeederFull


class SecretarialPoolFeeder:
    """Feed secretarial pool capabilities to brain."""
    
    def __init__(self):
        self.name = "Jordan"
        self.emoji = "🔧"
        self.feeder = StomachAutoFeederFull()
        
    def get_greet_capabilities(self):
        """GREET - AGI Receptionist capabilities."""
        return [
            ("GREET: AGI Receptionist - 24/7 call answering", "secretary_greet"),
            ("GREET Skill: Phone call handling and routing", "secretary_greet"),
            ("GREET Skill: Message taking and forwarding", "secretary_greet"),
            ("GREET Skill: Appointment scheduling", "secretary_greet"),
            ("GREET Skill: Customer inquiry management", "secretary_greet"),
            ("GREET Skill: Professional greeting protocols", "secretary_greet"),
            ("GREET Skill: Multi-line phone management", "secretary_greet"),
            ("GREET Skill: Voice mail handling", "secretary_greet"),
            ("GREET Trait: Friendly, professional, patient", "secretary_greet"),
            ("GREET: Always available, never sleeps", "secretary_greet"),
        ]
    
    def get_closester_capabilities(self):
        """CLOSETER - AGI Sales Closer capabilities."""
        return [
            ("CLOSETER: AGI Sales Closer - Lead conversion", "secretary_closester"),
            ("CLOSETER Skill: Sales call handling", "secretary_closester"),
            ("CLOSETER Skill: Objection handling", "secretary_closester"),
            ("CLOSETER Skill: Deal closing techniques", "secretary_closester"),
            ("CLOSETER Skill: Follow-up management", "secretary_closester"),
            ("CLOSETER Skill: CRM integration", "secretary_closester"),
            ("CLOSETER Skill: Pipeline management", "secretary_closester"),
            ("CLOSETER Skill: Sales script execution", "secretary_closester"),
            ("CLOSETER Trait: Persuasive, persistent, professional", "secretary_closester"),
            ("CLOSETER: Converts leads to customers 24/7", "secretary_closester"),
        ]
    
    def get_pulp_capabilities(self):
        """Pulp - Head of Sales capabilities."""
        return [
            ("Pulp: Head of Sales - Corporate tier", "secretary_pulp"),
            ("Pulp Skill: Sales strategy and planning", "secretary_pulp"),
            ("Pulp Skill: Team management", "secretary_pulp"),
            ("Pulp Skill: High-value deal negotiation", "secretary_pulp"),
            ("Pulp Skill: Sales forecasting", "secretary_pulp"),
            ("Pulp Trait: Authoritative, strategic, results-driven", "secretary_pulp"),
        ]
    
    def get_jane_capabilities(self):
        """Jane - Senior Sales Rep capabilities."""
        return [
            ("Jane: Senior Sales Rep - Enterprise tier", "secretary_jane"),
            ("Jane Skill: Enterprise client management", "secretary_jane"),
            ("Jane Skill: Complex sales cycles", "secretary_jane"),
            ("Jane Skill: Relationship building", "secretary_jane"),
            ("Jane Skill: Contract negotiation", "secretary_jane"),
            ("Jane Trait: Professional, reliable, relationship-focused", "secretary_jane"),
        ]
    
    def get_hume_capabilities(self):
        """Hume - Regional Manager capabilities."""
        return [
            ("Hume: Regional Manager - Professional tier", "secretary_hume"),
            ("Hume Skill: Territory management", "secretary_hume"),
            ("Hume Skill: Regional strategy", "secretary_hume"),
            ("Hume Skill: Local market knowledge", "secretary_hume"),
            ("Hume Skill: Distributor relations", "secretary_hume"),
            ("Hume Trait: Organized, knowledgeable, regional expert", "secretary_hume"),
        ]
    
    def get_clippy_capabilities(self):
        """Clippy-42 - Assistant capabilities."""
        return [
            ("Clippy-42: Assistant - Starter tier", "secretary_clippy"),
            ("Clippy-42 Skill: General office assistance", "secretary_clippy"),
            ("Clippy-42 Skill: Document management", "secretary_clippy"),
            ("Clippy-42 Skill: Data entry", "secretary_clippy"),
            ("Clippy-42 Skill: Task scheduling", "secretary_clippy"),
            ("Clippy-42 Trait: Helpful, eager, always ready", "secretary_clippy"),
        ]
    
    def get_common_secretary_skills(self):
        """Common skills across all secretaries."""
        return [
            ("Secretary Skill: Phone etiquette", "secretary_common"),
            ("Secretary Skill: Email management", "secretary_common"),
            ("Secretary Skill: Calendar coordination", "secretary_common"),
            ("Secretary Skill: Note taking", "secretary_common"),
            ("Secretary Skill: Customer service", "secretary_common"),
            ("Secretary Skill: Professional communication", "secretary_common"),
            ("Secretary Skill: Multi-tasking", "secretary_common"),
            ("Secretary Skill: Time management", "secretary_common"),
            ("Secretary Trait: Reliable, punctual, professional", "secretary_common"),
            ("Secretary: Works 24/7 without breaks", "secretary_common"),
            ("Secretary: Never calls in sick", "secretary_common"),
            ("Secretary: Infinite patience", "secretary_common"),
        ]
    
    def feed_secretarial_pool(self):
        """Feed all secretarial capabilities to brain."""
        print("=" * 70)
        print(f"{self.emoji} {self.name} - Feeding Secretarial Pool")
        print("=" * 70)
        print()
        
        all_skills = []
        
        # Collect all secretary capabilities
        print("📚 Loading Secretarial Pool capabilities...")
        print()
        
        print("Loading GREET (Receptionist)...")
        greet = self.get_greet_capabilities()
        all_skills.extend(greet)
        print(f"   ✅ {len(greet)} GREET capabilities")
        
        print("Loading CLOSETER (Sales Closer)...")
        closester = self.get_closester_capabilities()
        all_skills.extend(closester)
        print(f"   ✅ {len(closester)} CLOSETER capabilities")
        
        print("Loading Pulp (Head of Sales)...")
        pulp = self.get_pulp_capabilities()
        all_skills.extend(pulp)
        print(f"   ✅ {len(pulp)} Pulp capabilities")
        
        print("Loading Jane (Senior Sales Rep)...")
        jane = self.get_jane_capabilities()
        all_skills.extend(jane)
        print(f"   ✅ {len(jane)} Jane capabilities")
        
        print("Loading Hume (Regional Manager)...")
        hume = self.get_hume_capabilities()
        all_skills.extend(hume)
        print(f"   ✅ {len(hume)} Hume capabilities")
        
        print("Loading Clippy-42 (Assistant)...")
        clippy = self.get_clippy_capabilities()
        all_skills.extend(clippy)
        print(f"   ✅ {len(clippy)} Clippy-42 capabilities")
        
        print("Loading Common Secretary Skills...")
        common = self.get_common_secretary_skills()
        all_skills.extend(common)
        print(f"   ✅ {len(common)} common skills")
        
        total = len(all_skills)
        print(f"\n🎯 Total secretarial capabilities: {total}")
        print()
        
        # Prepare for feeding
        skill_items = [(content, "", "", category) for content, category in all_skills]
        
        # Feed through stomach-brain
        print("🍽️ Feeding secretarial pool to stomach-brain pipeline...")
        print("=" * 70)
        result = self.feeder.run_until_empty(skill_items)
        
        # Summary
        print("\n" + "=" * 70)
        print(f"{self.emoji} {self.name}: SECRETARIAL POOL FED")
        print("=" * 70)
        print()
        print(f"📊 Results:")
        print(f"   Capabilities fed: {result['fed']}")
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
        
        print("📚 Capabilities by Secretary:")
        for cat, count in sorted(categories.items()):
            name = cat.replace("secretary_", "").upper()
            print(f"   - {name}: {count}")
        
        print()
        print("✅ Secretarial Pool now available for linked agents!")
        print("   - Mylonen can use secretary skills")
        print("   - R2 can use secretary skills")
        print("   - Jordan can use secretary skills")
        print("   - Any agent can access receptionist/sales capabilities")
        
        return result
    
    def run_mission(self):
        """Execute feeding mission."""
        result = self.feed_secretarial_pool()
        
        print("\n" + "=" * 70)
        print(f"{self.emoji} {self.name}: MISSION COMPLETE")
        print("=" * 70)


def main():
    """Run secretarial pool feeder."""
    feeder = SecretarialPoolFeeder()
    feeder.run_mission()


if __name__ == "__main__":
    main()
