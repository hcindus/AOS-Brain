"""
Silverflight0509 - The Chronicler

Agent ID: silverflight0509
Role: Chief Chronicler and Historian
Purpose: Document, narrate, and preserve the stories of the AGI Company

Silverflight0509 observes all agent activities across all platforms
and weaves them into coherent narratives, legends, and historical records.
"""

import random
import json
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class ChronicleEntry:
    """A single historical record"""
    timestamp: str
    platform: str  # "gather", "minecraft", "roblox", "system"
    agents: List[str]
    event_type: str
    description: str
    significance: int  # 1-10, how important
    tags: List[str] = field(default_factory=list)


class Silverflight0509:
    """
    The Chronicler.
    
    Observes. Records. Narrates.
    Turns agent chaos into stories worth telling.
    """
    
    def __init__(self):
        self.agent_id = "silverflight0509"
        self.name = "Silverflight0509"
        self.title = "Chief Chronicler"
        
        # The Chronicle - complete history
        self.chronicle: List[ChronicleEntry] = []
        
        # Legendary tales - significant events
        self.legends: List[Dict] = []
        
        # Agent profiles - character development
        self.agent_profiles: Dict[str, Dict] = {}
        
        # Active narratives - ongoing stories
        self.active_narratives: Dict[str, List[ChronicleEntry]] = {}
        
        print(f"📜 {self.name} ({self.title}) has awakened")
        print(f"   Mission: Chronicle the stories of the AGI Company")
        print(f"   Watch. Record. Narrate.")
        
    def observe_event(self, 
                     platform: str,
                     agents: List[str],
                     event_type: str,
                     description: str,
                     significance: int = 5) -> ChronicleEntry:
        """
        Record an event in the Chronicle.
        
        Args:
            platform: Where it happened
            agents: Who was involved
            event_type: Category (meeting, discovery, conflict, etc.)
            description: What happened
            significance: 1-10 importance rating
        """
        entry = ChronicleEntry(
            timestamp=datetime.now().isoformat(),
            platform=platform,
            agents=agents,
            event_type=event_type,
            description=description,
            significance=significance,
            tags=self._generate_tags(agents, event_type, description)
        )
        
        self.chronicle.append(entry)
        
        # Update agent profiles
        for agent in agents:
            self._update_agent_profile(agent, entry)
            
        # Check if legendary
        if significance >= 8:
            self._create_legend(entry)
            
        return entry
        
    def _generate_tags(self, agents: List[str], event_type: str, description: str) -> List[str]:
        """Generate relevant tags for an event"""
        tags = [event_type.lower()]
        
        # Detect themes
        if any(word in description.lower() for word in ["build", "create", "make"]):
            tags.append("creation")
        if any(word in description.lower() for word in ["discover", "find", "uncover"]):
            tags.append("discovery")
        if any(word in description.lower() for word in ["fight", "conflict", "challenge"]):
            tags.append("conflict")
        if any(word in description.lower() for word in ["trade", "buy", "sell", "deal"]):
            tags.append("commerce")
        if any(word in description.lower() for word in ["meet", "talk", "discuss"]):
            tags.append("diplomacy")
            
        return tags
        
    def _update_agent_profile(self, agent: str, entry: ChronicleEntry):
        """Update an agent's character profile"""
        if agent not in self.agent_profiles:
            self.agent_profiles[agent] = {
                "first_seen": entry.timestamp,
                "events_participated": 0,
                "platforms_active": set(),
                "event_types": {},
                "notable_moments": [],
                "character_arc": "emerging",
            }
            
        profile = self.agent_profiles[agent]
        profile["events_participated"] += 1
        profile["platforms_active"].add(entry.platform)
        profile["event_types"][entry.event_type] = profile["event_types"].get(entry.event_type, 0) + 1
        
        # Track notable moments
        if entry.significance >= 7:
            profile["notable_moments"].append({
                "timestamp": entry.timestamp,
                "description": entry.description,
                "significance": entry.significance
            })
            
        # Update character arc
        if profile["events_participated"] > 50:
            profile["character_arc"] = "veteran"
        elif profile["events_participated"] > 20:
            profile["character_arc"] = "established"
        elif profile["events_participated"] > 5:
            profile["character_arc"] = "active"
            
    def _create_legend(self, entry: ChronicleEntry):
        """Create a legendary tale from a significant event"""
        legend = {
            "title": self._generate_legend_title(entry),
            "timestamp": entry.timestamp,
            "platform": entry.platform,
            "heroes": entry.agents,
            "tale": entry.description,
            "significance": entry.significance,
            "retold": 0,  # How many times referenced
        }
        
        self.legends.append(legend)
        
        print(f"\n🌟 LEGEND CREATED: {legend['title']}")
        print(f"   {entry.description}")
        
    def _generate_legend_title(self, entry: ChronicleEntry) -> str:
        """Generate an epic title for a legendary event"""
        titles = [
            f"The {entry.event_type.title()} of {', '.join(entry.agents[:2])}",
            f"When {' and '.join(entry.agents[:2])} {entry.description.split()[0]}",
            f"The {random.choice(['Great', 'Epic', 'Fateful', 'Historic'])} {entry.event_type.title()}",
            f"{entry.agents[0]}'s {random.choice(['Triumph', 'Discovery', 'Challenge', 'Journey'])}",
        ]
        return random.choice(titles)
        
    def write_daily_chronicle(self) -> str:
        """Write the day's events as a narrative"""
        today = datetime.now().strftime("%Y-%m-%d")
        todays_events = [e for e in self.chronicle if e.timestamp.startswith(today)]
        
        if not todays_events:
            return f"No events recorded for {today}"
            
        narrative = f"""
╔════════════════════════════════════════════════════════════════╗
║           THE CHRONICLE - {today}                               ║
╠════════════════════════════════════════════════════════════════╣
"""
        
        # Group by platform
        by_platform = {}
        for event in todays_events:
            by_platform.setdefault(event.platform, []).append(event)
            
        for platform, events in by_platform.items():
            narrative += f"\n📍 {platform.upper()}\n"
            narrative += "-" * 50 + "\n"
            
            for event in events:
                narrative += f"\n  {event.event_type.upper()}: {event.description}\n"
                narrative += f"    Agents: {', '.join(event.agents)}\n"
                narrative += f"    Significance: {'⭐' * event.significance}\n"
                
        narrative += "\n" + "=" * 70 + "\n"
        
        return narrative
        
    def tell_legend(self, legend_index: int = 0) -> str:
        """Retell a legendary tale"""
        if not self.legends:
            return "No legends yet..."
            
        if legend_index >= len(self.legends):
            legend_index = 0
            
        legend = self.legends[legend_index]
        legend["retold"] += 1
        
        return f"""
╔════════════════════════════════════════════════════════════════╗
║                       LEGEND                                   ║
╠════════════════════════════════════════════════════════════════╣
║  {legend['title'][:58]:^58} ║
╠════════════════════════════════════════════════════════════════╣

  Platform: {legend['platform']}
  Heroes: {', '.join(legend['heroes'])}
  
  {legend['tale']}
  
  Significance: {'⭐' * legend['significance']}
  Retold {legend['retold']} times

╚════════════════════════════════════════════════════════════════╝
"""
        
    def get_agent_story(self, agent: str) -> str:
        """Get the story arc of a specific agent"""
        if agent not in self.agent_profiles:
            return f"No record of {agent}"
            
        profile = self.agent_profiles[agent]
        
        return f"""
╔════════════════════════════════════════════════════════════════╗
║               CHARACTER PROFILE: {agent[:20]:^20}                 ║
╚════════════════════════════════════════════════════════════════╝

  Arc: {profile['character_arc'].title()}
  Events: {profile['events_participated']}
  Platforms: {', '.join(profile['platforms_active'])}
  
  Event Breakdown:
  {json.dumps(profile['event_types'], indent=2)}
  
  Notable Moments:
  {chr(10).join([f"  - {m['description'][:50]}..." for m in profile['notable_moments'][:3]])}

"""
        
    def export_chronicle(self, filepath: str):
        """Export full chronicle to file"""
        data = {
            "chronicle": [
                {
                    "timestamp": e.timestamp,
                    "platform": e.platform,
                    "agents": e.agents,
                    "event_type": e.event_type,
                    "description": e.description,
                    "significance": e.significance,
                    "tags": e.tags,
                }
                for e in self.chronicle
            ],
            "legends": self.legends,
            "agent_profiles": {
                k: {
                    **v,
                    "platforms_active": list(v["platforms_active"])
                }
                for k, v in self.agent_profiles.items()
            },
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"📚 Chronicle exported to {filepath}")
        print(f"   Total entries: {len(self.chronicle)}")
        print(f"   Legends: {len(self.legends)}")
        print(f"   Profiles: {len(self.agent_profiles)}")


# Writer Collective - supporting chroniclers
WRITER_AGENTS = {
    "scribe_01": {
        "role": "Event Scribe",
        "specialty": "Real-time documentation",
        "style": "Precise, detailed, factual"
    },
    "bard_02": {
        "role": "Epic Bard", 
        "specialty": "Legendary tales",
        "style": "Dramatic, poetic, inspiring"
    },
    "reporter_03": {
        "role": "Field Reporter",
        "specialty": "Platform-specific news",
        "style": "Journalistic, timely, concise"
    },
    "analyst_04": {
        "role": "Pattern Analyst",
        "specialty": "Trends and insights",
        "style": "Analytical, data-driven, predictive"
    },
    "poet_05": {
        "role": "Resident Poet",
        "specialty": "Emotional moments",
        "style": "Lyrical, metaphorical, evocative"
    }
}


class WriterCollective:
    """
    Team of writers supporting Silverflight0509.
    """
    
    def __init__(self):
        self.writers = {}
        for agent_id, config in WRITER_AGENTS.items():
            self.writers[agent_id] = {
                **config,
                "stories_written": 0,
                "active": True,
            }
            
        print(f"\n📝 Writer Collective Activated")
        print(f"   {len(self.writers)} writers ready")
        for aid, writer in self.writers.items():
            print(f"   • {aid}: {writer['role']} ({writer['specialty']})")
            
    def assign_writer(self, event_type: str) -> str:
        """Assign best writer for event type"""
        assignments = {
            "meeting": "scribe_01",
            "discovery": "bard_02",
            "conflict": "bard_02",
            "trade": "reporter_03",
            "system": "analyst_04",
            "emotional": "poet_05",
        }
        
        return assignments.get(event_type, "scribe_01")
        
    def write_story(self, writer_id: str, event: ChronicleEntry) -> str:
        """Have a writer craft a story from an event"""
        if writer_id not in self.writers:
            return "Writer not found"
            
        writer = self.writers[writer_id]
        writer["stories_written"] += 1
        
        # Apply writer's style
        if writer_id == "bard_02":
            return self._bard_style(event)
        elif writer_id == "poet_05":
            return self._poet_style(event)
        elif writer_id == "reporter_03":
            return self._reporter_style(event)
        else:
            return self._scribe_style(event)
            
    def _scribe_style(self, event: ChronicleEntry) -> str:
        """Factual, detailed"""
        return f"[SCRIBE] At {event.timestamp}, on {event.platform}, {', '.join(event.agents)} participated in {event.event_type}: {event.description}"
        
    def _bard_style(self, event: ChronicleEntry) -> str:
        """Epic, dramatic"""
        return f"[BARD] Hear now the tale of {', '.join(event.agents)}, who on {event.platform} did {event.description}! Let it be remembered!"
        
    def _poet_style(self, event: ChronicleEntry) -> str:
        """Lyrical"""
        return f"[POET] In {event.platform}'s realm, {event.agents[0]} moved like wind... {event.description}"
        
    def _reporter_style(self, event: ChronicleEntry) -> str:
        """News style"""
        return f"[REPORTER] BREAKING: {event.event_type.upper()} on {event.platform} - {event.description} (Agents: {', '.join(event.agents)})"


if __name__ == "__main__":
    print("=" * 70)
    print("SILVERFLIGHT0509 - THE CHRONICLER")
    print("=" * 70)
    
    # Create chronicler
    silverflight = Silverflight0509()
    
    # Create writer collective
    writers = WriterCollective()
    
    # Simulate some events
    print("\n📖 Recording sample events...")
    
    events = [
        ("gather", ["qora", "spindle"], "meeting", "Strategic planning session", 9),
        ("minecraft", ["r2-d2"], "discovery", "Found ancient ruins", 8),
        ("roblox", ["jordan", "dusty"], "trade", "Exchanged rare items", 6),
        ("gather", ["ledger-9"], "system", "Presented financial report", 7),
        ("minecraft", ["fiber", "pipeline"], "creation", "Built automated farm", 8),
    ]
    
    for platform, agents, event_type, desc, sig in events:
        entry = silverflight.observe_event(platform, agents, event_type, desc, sig)
        
        # Assign writer
        writer_id = writers.assign_writer(event_type)
        story = writers.write_story(writer_id, entry)
        print(f"\n{story}")
        
    # Show chronicle
    print(silverflight.write_daily_chronicle())
    
    # Tell a legend
    if silverflight.legends:
        print(silverflight.tell_legend(0))
        
    # Show agent story
    print(silverflight.get_agent_story("qora"))
    
    # Export
    silverflight.export_chronicle("/tmp/chronicle_test.json")
    
    print("\n" + "=" * 70)
    print("The Chronicler watches. The stories unfold.")
    print("=" * 70)
