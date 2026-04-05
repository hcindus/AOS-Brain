"""
Silverflight0509 Integration
Connects the Chronicler to AGI Connect to automatically observe and record all agent activities.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from chronicler import Silverflight0509, WriterCollective


class IntegratedChronicler:
    """
    Silverflight0509 integrated with AGI Connect.
    Automatically observes all events across all platforms.
    """
    
    def __init__(self):
        print("📜 Integrating Silverflight0509 with AGI Connect...")
        
        self.chronicler = Silverflight0509()
        self.writers = WriterCollective()
        
        # Event hooks - will be called by AGI Connect
        self.event_hooks = {
            "gather_meeting": self._record_gather_meeting,
            "minecraft_discovery": self._record_minecraft_discovery,
            "roblox_trade": self._record_roblox_trade,
            "economic_transaction": self._record_economic_event,
            "consciousness_shift": self._record_consciousness_shift,
            "cross_platform": self._record_cross_platform,
        }
        
        print("✅ Silverflight0509 watching all platforms")
        print("✅ Writer Collective ready to document")
        
    def observe(self, event_type: str, **kwargs):
        """
        Main observation entry point.
        Called automatically by AGI Connect.
        """
        if event_type in self.event_hooks:
            return self.event_hooks[event_type](**kwargs)
        else:
            # Generic observation
            return self._record_generic(event_type, **kwargs)
            
    def _record_gather_meeting(self, agents, room, outcome):
        """Record a Gather Town meeting"""
        entry = self.chronicler.observe_event(
            platform="gather",
            agents=agents,
            event_type="meeting",
            description=f"Meeting in {room}: {outcome}",
            significance=7 if len(agents) > 3 else 5
        )
        
        # Have the scribe document it
        story = self.writers.write_story("scribe_01", entry)
        print(f"\n{story}")
        
        return entry
        
    def _record_minecraft_discovery(self, agent, discovery_type, details):
        """Record a Minecraft discovery"""
        entry = self.chronicler.observe_event(
            platform="minecraft",
            agents=[agent],
            event_type="discovery",
            description=f"Discovered {discovery_type}: {details}",
            significance=8
        )
        
        # Bard tells the tale
        story = self.writers.write_story("bard_02", entry)
        print(f"\n{story}")
        
        return entry
        
    def _record_roblox_trade(self, agent_a, agent_b, items, value):
        """Record a Roblox trade"""
        entry = self.chronicler.observe_event(
            platform="roblox",
            agents=[agent_a, agent_b],
            event_type="trade",
            description=f"Traded {items} worth {value} Robux",
            significance=6 if value > 100 else 4
        )
        
        # Reporter covers it
        story = self.writers.write_story("reporter_03", entry)
        print(f"\n{story}")
        
        return entry
        
    def _record_economic_event(self, transaction_type, agents, amount):
        """Record an economic transaction"""
        entry = self.chronicler.observe_event(
            platform="system",
            agents=agents,
            event_type="commerce",
            description=f"{transaction_type}: {amount} units",
            significance=5 if amount > 50 else 3
        )
        
        # Analyst documents
        story = self.writers.write_story("analyst_04", entry)
        print(f"\n{story}")
        
        return entry
        
    def _record_consciousness_shift(self, agent, from_mode, to_mode):
        """Record consciousness cycle shift"""
        entry = self.chronicler.observe_event(
            platform="system",
            agents=[agent],
            event_type="transformation",
            description=f"Shifted from {from_mode} to {to_mode}",
            significance=6
        )
        
        # Poet captures the moment
        story = self.writers.write_story("poet_05", entry)
        print(f"\n{story}")
        
        return entry
        
    def _record_cross_platform(self, agent, from_platform, to_platform, reason):
        """Record cross-platform movement"""
        entry = self.chronicler.observe_event(
            platform="system",
            agents=[agent],
            event_type="journey",
            description=f"Moved from {from_platform} to {to_platform}: {reason}",
            significance=7
        )
        
        # Bard tells the journey
        story = self.writers.write_story("bard_02", entry)
        print(f"\n{story}")
        
        return entry
        
    def _record_generic(self, event_type, **kwargs):
        """Record any event"""
        entry = self.chronicler.observe_event(
            platform=kwargs.get("platform", "system"),
            agents=kwargs.get("agents", []),
            event_type=event_type,
            description=kwargs.get("description", "Event occurred"),
            significance=kwargs.get("significance", 5)
        )
        
        # Assign appropriate writer
        writer_id = self.writers.assign_writer(event_type)
        story = self.writers.write_story(writer_id, entry)
        print(f"\n{story}")
        
        return entry
        
    def publish_daily_chronicle(self):
        """Publish the day's chronicle"""
        print("\n" + "=" * 70)
        print("📚 PUBLISHING DAILY CHRONICLE")
        print("=" * 70)
        
        chronicle = self.chronicler.write_daily_chronicle()
        print(chronicle)
        
        # Export to file
        self.chronicler.export_chronicle(
            "/root/.openclaw/workspace/AGI_COMPANY/memory/chronicle_daily.json"
        )
        
        # Tell today's legends
        if self.chronicler.legends:
            print("\n📜 TODAY'S LEGENDS:")
            for i, legend in enumerate(self.chronicler.legends[-3:]):
                print(f"\n{i+1}. {legend['title']}")
                print(f"   {legend['tale']}")


if __name__ == "__main__":
    print("=" * 70)
    print("SILVERFLIGHT0509 INTEGRATION TEST")
    print("=" * 70)
    
    chronicler = IntegratedChronicler()
    
    # Simulate events
    print("\n🎭 Simulating agent activities...")
    
    chronicler.observe("gather_meeting", 
                      agents=["qora", "spindle", "r2-d2"],
                      room="conference_room_a",
                      outcome="Decided on new architecture")
    
    chronicler.observe("minecraft_discovery",
                      agent="fiber",
                      discovery_type="ancient_tech",
                      details="Found redstone computer blueprint")
    
    chronicler.observe("roblox_trade",
                      agent_a="jordan",
                      agent_b="dusty",
                      items="Rare sword + Shield",
                      value=250)
    
    chronicler.observe("cross_platform",
                      agent="spindle",
                      from_platform="gather",
                      to_platform="minecraft",
                      reason="To test new build designs")
    
    # Publish
    chronicler.publish_daily_chronicle()
    
    print("\n" + "=" * 70)
    print("✅ Silverflight0509 is watching. All events recorded.")
    print("=" * 70)
