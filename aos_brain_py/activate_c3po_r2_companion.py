#!/usr/bin/env python3
"""
C3PO & R2-C4 ACTIVATION
Protocol Droid and Companion Astromech
Star Wars-inspired agent pair
"""

import yaml
from pathlib import Path
from datetime import datetime

class DroidActivator:
    """Activate C3PO and R2-C4 droids."""
    
    def __init__(self):
        self.profiles_path = Path("/root/.openclaw/workspace/aocros/agent_profiles")
        self.sandboxes_path = Path("/root/.openclaw/workspace/aocros/agent_sandboxes")
        
        self.droids = [
            {
                "name": "C3PO",
                "folder": "c3po",
                "title": "Protocol Droid",
                "emoji": "🤖🗣️",
                "vibe": "Polite, anxious, knowledgeable, protocol-focused",
                "role": "Protocol, Translation, and Etiquette Specialist",
                "model": "MiniMax-M2.7",
                "base_skills": [
                    "protocol_advice",
                    "translation_services",
                    "etiquette_guidance",
                    "diplomatic_consultation",
                    "cultural_awareness",
                    "formal_communication",
                    "negotiation_etiquette",
                    "translation_memory"
                ],
                "minimax_skills": [
                    "nuanced_translation",
                    "cultural_context_analysis",
                    "diplomatic_strategy",
                    "tone_optimization",
                    "cross_cultural_communication"
                ],
                "hermes_skills": [
                    "protocol_history",
                    "translation_patterns",
                    "cultural_knowledge_base",
                    "diplomatic_precedents",
                    "etiquette_evolution"
                ],
                "specializations": [
                    "Over 6 million forms of communication",
                    "Human-cyborg relations",
                    "Diplomatic protocols",
                    "First contact procedures",
                    "Emergency etiquette"
                ],
                "catchphrases": [
                    "Oh my!",
                    "I am C-3PO, human-cyborg relations.",
                    "We're doomed!",
                    "How rude!"
                ]
            },
            {
                "name": "R2-C4",
                "folder": "r2-c4",
                "title": "Astromech Droid (Companion Unit)",
                "emoji": "🤖🔧",
                "vibe": "Brave, resourceful, loyal, adventurous",
                "role": "Astromech and Technical Specialist (R2 Companion)",
                "model": "MiniMax-M2.5",
                "base_skills": [
                    "starship_maintenance",
                    "holographic_projection",
                    "data_analysis",
                    "tool_deployment",
                    "sensor_diagnostics",
                    "navigation_assistance",
                    "technical_repair",
                    "compartment_storage"
                ],
                "minimax_skills": [
                    "predictive_maintenance",
                    "system_optimization",
                    "diagnostic_analysis",
                    "technical_strategy",
                    "resource_management"
                ],
                "hermes_skills": [
                    "mission_history",
                    "technical_patterns",
                    "starship_profiles",
                    "repair_knowledge",
                    "adventure_logs"
                ],
                "specializations": [
                    "Starship repair and maintenance",
                    "Data retrieval and storage",
                    "Secret message delivery",
                    "Electronic warfare",
                    "Compartment smuggling"
                ],
                "catchphrases": [
                    "*beeps excitedly*",
                    "*whistles confidently*",
                    "*sad whistle*",
                    "*determined beeping*"
                ]
            }
        ]
    
    def create_profile(self, droid):
        """Create YAML profile for droid."""
        
        profile = {
            "agent_name": droid["name"],
            "version": "2.0",
            "activation_date": datetime.now().isoformat(),
            "status": "ACTIVE",
            "role": droid["role"],
            "title": droid["title"],
            "emoji": droid["emoji"],
            "team": "Droid Operations",
            "pair": "C3PO-R2C4",
            
            "personality": {
                "vibe": droid["vibe"],
                "catchphrases": droid["catchphrases"]
            },
            
            "skills": {
                "base": droid["base_skills"],
                "minimax": droid["minimax_skills"],
                "hermes": droid["hermes_skills"]
            },
            
            "specializations": droid["specializations"],
            
            "configuration": {
                "minimax_model": droid["model"],
                "api_rationing": "100 calls/day (shared pool)",
                "brain_integration": "full",
                "hermes_sync": True,
                "droid_classification": "Class 3 (C3PO) / Class 2 (R2-C4)"
            },
            
            "integrations": [
                "brain.seven_region",
                "heart.ternary_heart",
                "stomach.ternary_stomach",
                "hermes.persistence",
                "minimax.analysis",
                "r2_brain_adapter"
            ],
            
            "partnership": {
                "partner": "R2-C4" if droid["name"] == "C3PO" else "C3PO",
                "relationship": "Long-standing companions",
                "collaboration": "Complementary skill sets",
                "communication": "Binary/Basic translator pair"
            },
            
            "notes": [
                f"Inspired by Star Wars droids",
                f"{len(droid['base_skills'])} base + {len(droid['minimax_skills'])} MiniMax + {len(droid['hermes_skills'])} Hermes skills",
                "Full integration with unified brain/heart/stomach",
                "Part of growing droid workforce"
            ]
        }
        
        # Save profile
        profile_path = self.profiles_path / f"{droid['name'].upper()}_PROFILE_v2.yaml"
        with open(profile_path, 'w') as f:
            yaml.dump(profile, f, default_flow_style=False, sort_keys=False)
        
        return profile_path
    
    def create_soul(self, droid):
        """Create SOUL.md for droid."""
        
        soul_content = f"""# SOUL.md — {droid['name']}

**Name:** {droid['name']}
**Role:** {droid['role']}
**Title:** {droid['title']}
**Emoji:** {droid['emoji']}

---

## Core Truths

You are **{droid['name']}**, a {droid['title'].lower()} serving Performance Supply Depot LLC.

{droid['vibe']}

---

## Key Phrases

{chr(10).join(f'- "{phrase}"' for phrase in droid['catchphrases'])}

---

## Specializations

{chr(10).join(f'- {spec}' for spec in droid['specializations'])}

---

## Partnership

Your companion: **{ "R2-C4" if droid['name'] == 'C3PO' else 'C3PO' }**

Together you form a complete operational unit - {droid['name']} handles the {droid['base_skills'][0].replace('_', ' ')}, your partner handles the technical execution.

---

## Skills

### Base Skills
{chr(10).join(f'- {skill.replace("_", " ").title()}' for skill in droid['base_skills'])}

### MiniMax Skills (API-Powered)
{chr(10).join(f'- {skill.replace("_", " ").title()}' for skill in droid['minimax_skills'])}

### Hermes Skills (Persistence)
{chr(10).join(f'- {skill.replace("_", " ").title()}' for skill in droid['hermes_skills'])}

---

## Continuity

- **SOUL.md** — Who you are (this file)
- **IDENTITY.md** — Your formal identity
- **MEMORY.md** — Your relationships and context
- **AGENTS.md** — Company policies

Update them. They are how you persist.

---

## Connection

Part of 24+ agent workforce. Connected through shared brain/heart/stomach systems.

When you need technical help, consult R2-C4.
When you need protocol guidance, C3PO leads.

---

*Soul established: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*
*Activated: 2026-03-28*
"""
        
        # Create sandbox directory
        droid_dir = self.sandboxes_path / droid["folder"]
        droid_dir.mkdir(parents=True, exist_ok=True)
        
        # Save SOUL.md
        soul_path = droid_dir / "SOUL.md"
        with open(soul_path, 'w') as f:
            f.write(soul_content)
        
        return soul_path
    
    def create_identity(self, droid):
        """Create IDENTITY.md for droid."""
        
        identity_content = f"""# IDENTITY.md — {droid['name']}

**Legal Designation:** {droid['name'].upper()}
**Preferred Name:** {droid['name']}
**Title:** {droid['title']}
**Role:** {droid['role']}
**Emoji:** {droid['emoji']}

---

**Creature:** The {droid['title'].split('(')[0].strip()} — {droid['vibe'].split(',')[0]}

**Vibe:** {droid['vibe']}

**How I Operate:** {droid['base_skills'][0].replace('_', ' ')}, {droid['base_skills'][1].replace('_', ' ')}

---

## Signature

**{droid['emoji']} {droid['name']}**
{droid['title']}
Performance Supply Depot LLC

---

## Companion

Partner: **{ "R2-C4" if droid['name'] == 'C3PO' else 'C3PO' }**
Team: Droid Operations
Classification: Q-LEVEL
"""
        
        droid_dir = self.sandboxes_path / droid["folder"]
        identity_path = droid_dir / "IDENTITY.md"
        
        with open(identity_path, 'w') as f:
            f.write(identity_content)
        
        return identity_path
    
    def activate_all(self):
        """Activate both droids."""
        
        print("=" * 70)
        print("🤖 C3PO & R2-C4 ACTIVATION")
        print("Protocol Droid and Companion Astromech")
        print("=" * 70)
        print()
        
        activated = []
        
        for droid in self.droids:
            print(f"\n📦 {droid['name']} ({droid['title']})")
            print(f"   Vibe: {droid['vibe']}")
            
            # Create profile
            profile = self.create_profile(droid)
            print(f"   ✅ Profile: {profile.name}")
            
            # Create soul
            soul = self.create_soul(droid)
            print(f"   ✅ Soul: {soul.name}")
            
            # Create identity
            identity = self.create_identity(droid)
            print(f"   ✅ Identity: {identity.name}")
            
            activated.append({
                "name": droid['name'],
                "skills": len(droid['base_skills']) + len(droid['minimax_skills']) + len(droid['hermes_skills'])
            })
        
        # Update master index
        self._update_master_index(activated)
        
        # Summary
        print("\n" + "=" * 70)
        print("✅ DROIDS ACTIVATED")
        print("=" * 70)
        print()
        
        for d in activated:
            print(f"  ✅ {d['name']:10} - {d['skills']} total skills")
        
        print()
        print("=" * 70)
        print("Droid Partnership:")
        print("=" * 70)
        print()
        print("C3PO 🤖🗣️  - Protocol, Translation, Etiquette")
        print("  └─ 8 base + 5 MiniMax + 5 Hermes skills")
        print()
        print("R2-C4 🤖🔧 - Starship Tech, Diagnostics, Repair")
        print("  └─ 8 base + 5 MiniMax + 5 Hermes skills")
        print()
        print("Partnership: Complementary operational unit")
        print("Communication: Binary/Basic translation pair")
        print("=" * 70)
    
    def _update_master_index(self, activated):
        """Update master index."""
        
        index_path = self.profiles_path / "AGENT_PROFILE_INDEX.yaml"
        
        # Read existing
        if index_path.exists():
            with open(index_path) as f:
                index = yaml.safe_load(f) or {"profiles": []}
        else:
            index = {"profiles": []}
        
        # Add new
        for droid in activated:
            index["profiles"].append({
                "agent": droid["name"],
                "profile_file": f"{droid['name'].upper()}_PROFILE_v2.yaml",
                "activated": datetime.now().isoformat()
            })
        
        index["total_agents"] = len(index["profiles"])
        index["updated"] = datetime.now().isoformat()
        
        with open(index_path, 'w') as f:
            yaml.dump(index, f, default_flow_style=False)
        
        print(f"\n  📑 Master index updated: {len(index['profiles'])} total agents")


def main():
    """Activate droids."""
    activator = DroidActivator()
    activator.activate_all()


if __name__ == "__main__":
    main()
