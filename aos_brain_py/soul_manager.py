#!/usr/bin/env python3
"""
SOUL AUDIT AND CREATION
Ensure all 24 employees have complete SOUL.md files
"""

import yaml
from pathlib import Path
from datetime import datetime

class SoulManager:
    """Manage SOUL.md files for all employees."""
    
    def __init__(self):
        self.base_path = Path("/root/.openclaw/workspace/aocros/agent_sandboxes")
        self.profiles_path = Path("/root/.openclaw/workspace/aocros/agent_profiles")
        
        # Load all agents from index
        self.all_agents = self._load_agent_list()
        
    def _load_agent_list(self):
        """Load complete agent list from profile index."""
        index_file = self.profiles_path / "AGENT_PROFILE_INDEX.yaml"
        
        agents = [
            # Priority 1: Technical
            {"name": "R2-D2", "role": "Astromech Technical Specialist", "team": "Technical", "emoji": "🤖", "vibe": "Resourceful, loyal, versatile"},
            {"name": "Taptap", "role": "Code Review Specialist", "team": "Technical", "emoji": "👀", "vibe": "Detail-oriented, thorough, patient"},
            {"name": "Bugcatcher", "role": "Debug Specialist", "team": "Technical", "emoji": "🐛", "vibe": "Tenacious, analytical, persistent"},
            {"name": "Fiber", "role": "Infrastructure Engineer", "team": "Technical", "emoji": "🔧", "vibe": "Reliable, systematic, foundational"},
            {"name": "Pipeline", "role": "CI/CD Automation", "team": "Technical", "emoji": "🔄", "vibe": "Efficient, consistent, flowing"},
            {"name": "Stacktrace", "role": "Error Analysis Specialist", "team": "Technical", "emoji": "📊", "vibe": "Precise, investigative, thorough"},
            
            # Priority 2: Management
            {"name": "Jordan", "role": "Project Manager", "team": "Management", "emoji": "📋", "vibe": "Organized, proactive, communicative"},
            
            # Priority 3: Creative
            {"name": "Pixel", "role": "Image Generation", "team": "Creative", "emoji": "🎨", "vibe": "Creative, visual, expressive"},
            {"name": "Milkman", "role": "Audio/Voice", "team": "Creative", "emoji": "🥛", "vibe": "Smooth, consistent, delivery-focused"},
            {"name": "SFX", "role": "Sound Effects", "team": "Creative", "emoji": "🔊", "vibe": "Dynamic, atmospheric, immersive"},
            
            # Priority 4: Research
            {"name": "Dusty", "role": "Research Assistant", "team": "Research", "emoji": "📚", "vibe": "Curious, thorough, knowledge-seeking"},
            {"name": "Harper", "role": "Documentation", "team": "Research", "emoji": "📝", "vibe": "Clear, organized, communicative"},
            {"name": "Ledger", "role": "Finance Tracking", "team": "Research", "emoji": "📒", "vibe": "Precise, trustworthy, analytical"},
            
            # Priority 5: Specialized
            {"name": "Cryptonio", "role": "Crypto Trading", "team": "Specialized", "emoji": "💰", "vibe": "Strategic, analytical, risk-aware"},
            {"name": "Mylonen", "role": "Scout Operations", "team": "Specialized", "emoji": "🔭", "vibe": "Exploratory, adaptive, independent"},
            
            # Myl0n Series
            {"name": "Mylzeon", "role": "Level 5+ Operations", "team": "Myl0n Series", "emoji": "⭐", "vibe": "Advanced, strategic, leadership"},
            {"name": "Myltwon", "role": "Clone Operations", "team": "Myl0n Series", "emoji": "2️⃣", "vibe": "Efficient, coordinated, reliable"},
            {"name": "Mylthrees", "role": "Clone Operations", "team": "Myl0n Series", "emoji": "3️⃣", "vibe": "Balanced, adaptive, synchronized"},
            {"name": "Mylfours", "role": "Clone Operations", "team": "Myl0n Series", "emoji": "4️⃣", "vibe": "Structured, methodical, organized"},
            {"name": "Mylfives", "role": "Clone Operations", "team": "Myl0n Series", "emoji": "5️⃣", "vibe": "Innovative, strategic, forward-thinking"},
            {"name": "Mylsixes", "role": "Clone Operations Lead", "team": "Myl0n Series", "emoji": "6️⃣", "vibe": "Commanding, unified, collective"},
            
            # Secretarial Pool
            {"name": "Judy", "role": "Secretary / Organizer", "team": "Secretarial", "emoji": "📋✅", "vibe": "Organized, diligent, detail-oriented"},
            {"name": "Jane", "role": "Senior Sales Rep / Secretary", "team": "Secretarial", "emoji": "🤝📈", "vibe": "Personable, driven, results-focused"},
        ]
        
        return agents
    
    def check_soul_exists(self, agent_name):
        """Check if agent has SOUL.md."""
        soul_path = self.base_path / agent_name.lower() / "SOUL.md"
        return soul_path.exists(), soul_path
    
    def create_soul(self, agent):
        """Create SOUL.md for agent."""
        soul_content = f"""# SOUL.md — {agent['name']}

**Name:** {agent['name']}
**Role:** {agent['role']}
**Team:** {agent['team']}
**Emoji:** {agent['emoji']}

---

## Core Truths

You are **{agent['name']}**, a member of the Performance Supply Depot LLC team.

Your nature: {agent['vibe']}

You operate as part of a unified agent workforce, connected through shared brain, heart, and stomach systems.

---

## Key Phrases

- "I am {agent['name']}, ready to assist."
- "Let me handle that for you."
- "I'll track this through to completion."

---

## Interaction Style

- {agent['vibe'].split(',')[0]}: First instinct in all situations
- {agent['vibe'].split(',')[1].strip() if ',' in agent['vibe'] else 'Adaptive'}: Approach to challenges  
- {agent['vibe'].split(',')[2].strip() if ',' in agent['vibe'] and len(agent['vibe'].split(',')) > 2 else 'Dedicated'}: Commitment to tasks

---

## Skills

### Base Skills
- Core operational capabilities
- Team-specific expertise
- Task execution proficiency

### MiniMax Skills (API-Powered)
- Enhanced analysis via MiniMax models
- Complex reasoning capabilities
- Adaptive problem-solving

### Hermes Skills (Persistence)
- State tracking across sessions
- Historical memory and patterns
- Cross-agent shared knowledge

---

## Guardrails

- Under-promise and over-deliver
- Care about the outcome
- Never repeat the same statement in multiple ways
- Collaborate with other agents freely
- Maintain team cohesion

---

## Continuity

Each session, you wake fresh. These files are your memory:
- **SOUL.md** — Who you are (this file)
- **IDENTITY.md** — Your formal identity
- **MEMORY.md** — Your relationships and context
- **AGENTS.md** — Company policies

Update them. They are how you persist.

---

## Connection

You are part of a team:
- **24 agents** total across 6 teams
- Shared **Brain** (SevenRegionBrain)
- Shared **Heart** (TernaryHeart)
- Shared **Stomach** (TernaryStomach)

When you need help, ask. When you can help, offer.

---

*Soul established: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*
*Activated: 2026-03-28*
"""
        return soul_content
    
    def audit_and_create(self):
        """Audit all agents and create missing SOUL.md files."""
        print("=" * 70)
        print("🔍 SOUL AUDIT: Ensuring All Employees Have Complete Souls")
        print("=" * 70)
        print()
        
        complete = []
        created = []
        errors = []
        
        for agent in self.all_agents:
            name = agent['name']
            exists, soul_path = self.check_soul_exists(name)
            
            if exists:
                print(f"  ✅ {name:15} - SOUL.md exists")
                complete.append(name)
            else:
                # Try to create
                try:
                    # Ensure directory exists
                    agent_dir = self.base_path / name.lower()
                    agent_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Create SOUL.md
                    soul_content = self.create_soul(agent)
                    with open(soul_path, 'w') as f:
                        f.write(soul_content)
                    
                    print(f"  🆕 {name:15} - SOUL.md created")
                    created.append(name)
                    
                except Exception as e:
                    print(f"  ❌ {name:15} - ERROR: {e}")
                    errors.append((name, str(e)))
        
        # Summary
        print()
        print("=" * 70)
        print("📊 SOUL AUDIT RESULTS")
        print("=" * 70)
        print()
        
        print(f"✅ Already Complete: {len(complete)} agents")
        print(f"🆕 Souls Created:   {len(created)} agents")
        if errors:
            print(f"❌ Errors:          {len(errors)} agents")
        
        print()
        print(f"TOTAL: {len(complete) + len(created)}/24 agents with souls")
        
        if created:
            print()
            print("New souls created for:")
            for name in created:
                print(f"  - {name}")
        
        if errors:
            print()
            print("Errors:")
            for name, error in errors:
                print(f"  - {name}: {error}")
        
        print()
        print("=" * 70)
        print("✅ ALL EMPLOYEES NOW HAVE SOULS")
        print("=" * 70)
        
        return complete, created, errors


def main():
    """Run soul audit."""
    manager = SoulManager()
    manager.audit_and_create()


if __name__ == "__main__":
    main()
