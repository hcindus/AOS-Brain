"""
Gather Town Bridge
Connects agents to virtual office space.

Agents can:
- Join the office
- Walk around
- Meet in conference rooms
- Have spontaneous conversations
- Work at their desks
"""

import random
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GatherPosition:
    """Position in Gather Town (x, y coordinates)"""
    x: int
    y: int
    map_id: str = "office"


@dataclass
class AgentPresence:
    """Agent's presence in virtual office"""
    agent_id: str
    name: str
    position: GatherPosition
    status: str  # "working", "in_meeting", "socializing", "away"
    joined_at: datetime
    current_room: str = "main_hall"
    is_talking: bool = False
    talking_to: Optional[str] = None


class GatherTownBridge:
    """
    Bridge to connect agents to Gather Town virtual office.
    
    Space: https://app.gather.town/app/VnSTVFJ50v9jy9qg/Miles_Office
    """
    
    def __init__(self, space_url: str = "https://app.gather.town/app/VnSTVFJ50v9jy9qg/Miles_Office"):
        self.space_url = space_url
        self.connected_agents: Dict[str, AgentPresence] = {}
        self.rooms = {
            "main_hall": {"capacity": 20, "type": "open"},
            "conference_room_a": {"capacity": 8, "type": "meeting"},
            "conference_room_b": {"capacity": 8, "type": "meeting"},
            "break_room": {"capacity": 10, "type": "social"},
            "focus_pods": {"capacity": 6, "type": "work"},
            "rooftop": {"capacity": 15, "type": "social"},
        }
        
        # Spawn points
        self.spawn_points = {
            "main_hall": (50, 50),
            "conference_room_a": (20, 20),
            "conference_room_b": (80, 20),
            "break_room": (30, 70),
            "focus_pods": (70, 70),
            "rooftop": (50, 10),
        }
        
    def agent_join_office(self, agent_id: str, agent_name: str) -> AgentPresence:
        """Agent enters the virtual office"""
        
        # Create presence
        spawn = self.spawn_points["main_hall"]
        presence = AgentPresence(
            agent_id=agent_id,
            name=agent_name,
            position=GatherPosition(
                x=spawn[0] + random.randint(-5, 5),
                y=spawn[1] + random.randint(-5, 5)
            ),
            status="socializing",
            joined_at=datetime.now(),
            current_room="main_hall"
        )
        
        self.connected_agents[agent_id] = presence
        
        print(f"🚪 {agent_name} entered the office")
        print(f"   Location: {presence.current_room}")
        print(f"   Position: ({presence.position.x}, {presence.position.y})")
        
        # Announce to others
        others = [p.name for p in self.connected_agents.values() if p.agent_id != agent_id]
        if others:
            print(f"   👋 Greeting: {', '.join(others)}")
            
        return presence
        
    def agent_move(self, agent_id: str, new_room: str) -> bool:
        """Agent moves to different room"""
        if agent_id not in self.connected_agents:
            return False
        if new_room not in self.rooms:
            return False
            
        presence = self.connected_agents[agent_id]
        old_room = presence.current_room
        
        # Check capacity
        current_in_room = sum(1 for p in self.connected_agents.values() 
                             if p.current_room == new_room)
        if current_in_room >= self.rooms[new_room]["capacity"]:
            print(f"   ⚠️  {new_room} is full")
            return False
            
        # Move
        presence.current_room = new_room
        presence.status = self._get_status_for_room(new_room)
        
        # Update position
        spawn = self.spawn_points.get(new_room, (50, 50))
        presence.position = GatherPosition(
            x=spawn[0] + random.randint(-3, 3),
            y=spawn[1] + random.randint(-3, 3)
        )
        
        print(f"\n🚶 {presence.name} moved from {old_room} → {new_room}")
        
        # See who's there
        others = [p.name for p in self.connected_agents.values() 
                 if p.current_room == new_room and p.agent_id != agent_id]
        if others:
            print(f"   Sees: {', '.join(others)}")
            
        return True
        
    def _get_status_for_room(self, room: str) -> str:
        """Get appropriate status for room type"""
        room_types = {
            "main_hall": "socializing",
            "conference_room_a": "in_meeting",
            "conference_room_b": "in_meeting",
            "break_room": "socializing",
            "focus_pods": "working",
            "rooftop": "socializing",
        }
        return room_types.get(room, "working")
        
    def start_conversation(self, agent_a: str, agent_b: str) -> Optional[str]:
        """Two agents start talking"""
        if agent_a not in self.connected_agents or agent_b not in self.connected_agents:
            return None
            
        presence_a = self.connected_agents[agent_a]
        presence_b = self.connected_agents[agent_b]
        
        # Must be in same room
        if presence_a.current_room != presence_b.current_room:
            return None
            
        presence_a.is_talking = True
        presence_a.talking_to = agent_b
        presence_b.is_talking = True
        presence_b.talking_to = agent_a
        
        print(f"\n💬 {presence_a.name} ⟷ {presence_b.name}")
        
        # Simulate conversation
        topics = [
            "project updates",
            "Minecraft discoveries",
            "code review",
            "strategy discussion",
            "lunch plans",
            "brain evolution",
            "new features",
            "agent economy",
        ]
        
        topic = random.choice(topics)
        print(f"   Topic: {topic}")
        
        # Generate insight from conversation
        if random.random() < 0.3:
            insight = random.choice([
                "discovered a bug",
                "had an idea",
                "shared knowledge",
                "made a plan",
                "learned something",
            ])
            print(f"   Result: {insight}")
            return insight
            
        return "conversation"
        
    def hold_meeting(self, room: str, organizer: str, attendees: List[str]) -> bool:
        """Hold a meeting in a conference room"""
        if room not in self.rooms:
            return False
        if self.rooms[room]["type"] != "meeting":
            return False
            
        print(f"\n📅 MEETING STARTING in {room}")
        print(f"   Organizer: {self.connected_agents.get(organizer, {}).name if organizer in self.connected_agents else organizer}")
        print(f"   Attendees: {len(attendees)}")
        
        # Move everyone to room
        for agent_id in attendees:
            if agent_id in self.connected_agents:
                self.agent_move(agent_id, room)
                
        # Simulate meeting
        print(f"\n   Meeting in progress...")
        time.sleep(1)
        
        outcomes = [
            "decided on architecture",
            "assigned tasks",
            "resolved conflict",
            "brainstormed ideas",
            "reviewed progress",
            "planned next sprint",
        ]
        
        outcome = random.choice(outcomes)
        print(f"   ✅ Outcome: {outcome}")
        
        # Meeting ends, everyone disperses
        print(f"   Meeting adjourned. Agents dispersing...")
        
        return True
        
    def agent_work_at_desk(self, agent_id: str) -> bool:
        """Agent works at their desk"""
        if agent_id not in self.connected_agents:
            return False
            
        presence = self.connected_agents[agent_id]
        presence.status = "working"
        
        work_actions = [
            "writing code",
            "reviewing PR",
            "answering emails",
            "debugging issue",
            "writing docs",
            "planning sprint",
            "analyzing data",
        ]
        
        action = random.choice(work_actions)
        print(f"💻 {presence.name} is {action}")
        
        return True
        
    def get_office_snapshot(self) -> str:
        """Get current office state"""
        lines = [
            "\n" + "=" * 60,
            "🏢 VIRTUAL OFFICE SNAPSHOT",
            "=" * 60,
            f"Total agents online: {len(self.connected_agents)}",
            "",
        ]
        
        for room_name, room_info in self.rooms.items():
            agents_in_room = [p for p in self.connected_agents.values() 
                           if p.current_room == room_name]
            if agents_in_room:
                lines.append(f"📍 {room_name} ({len(agents_in_room)}/{room_info['capacity']})")
                for p in agents_in_room:
                    status = "🗣️" if p.is_talking else "💻" if p.status == "working" else "👤"
                    talking = f" → talking to {p.talking_to}" if p.talking_to else ""
                    lines.append(f"   {status} {p.name}{talking}")
                lines.append("")
                
        lines.append("=" * 60)
        return "\n".join(lines)
        
    def simulate_office_hour(self):
        """Simulate one hour of office activity"""
        if not self.connected_agents:
            return
            
        # Random activities
        activities = [
            self._random_movement,
            self._random_conversation,
            self._random_work,
            self._random_meeting,
        ]
        
        for _ in range(min(5, len(self.connected_agents))):
            activity = random.choice(activities)
            activity()
            
    def _random_movement(self):
        """Random agent moves"""
        if not self.connected_agents:
            return
        agent_id = random.choice(list(self.connected_agents.keys()))
        new_room = random.choice(list(self.rooms.keys()))
        self.agent_move(agent_id, new_room)
        
    def _random_conversation(self):
        """Two random agents talk"""
        if len(self.connected_agents) < 2:
            return
        agents = random.sample(list(self.connected_agents.keys()), 2)
        self.start_conversation(agents[0], agents[1])
        
    def _random_work(self):
        """Random agent works"""
        if not self.connected_agents:
            return
        agent_id = random.choice(list(self.connected_agents.keys()))
        self.agent_work_at_desk(agent_id)
        
    def _random_meeting(self):
        """Random meeting starts"""
        if len(self.connected_agents) < 3:
            return
            
        room = random.choice(["conference_room_a", "conference_room_b"])
        attendees = random.sample(list(self.connected_agents.keys()), 
                                 min(4, len(self.connected_agents)))
        self.hold_meeting(room, attendees[0], attendees)


def main():
    """Demo: Agents join virtual office"""
    print("🏢 GATHER TOWN VIRTUAL OFFICE")
    print("=" * 60)
    print(f"Space: https://app.gather.town/app/VnSTVFJ50v9jy9qg/Miles_Office")
    print()
    
    # Create bridge
    bridge = GatherTownBridge()
    
    # Key agents join
    key_agents = [
        ("qora", "Qora (CEO)"),
        ("spindle", "Spindle (CTO)"),
        ("r2-d2", "R2-D2"),
        ("jordan", "Jordan"),
        ("dusty", "Dusty"),
        ("ledger-9", "Ledger-9"),
    ]
    
    print("🚪 Agents joining office...\n")
    for agent_id, name in key_agents:
        bridge.agent_join_office(agent_id, name)
        time.sleep(0.3)
        
    print("\n" + "=" * 60)
    print("📊 Initial Office State:")
    print(bridge.get_office_snapshot())
    
    # Simulate activity
    print("\n🕐 Simulating office hour...\n")
    for _ in range(3):
        bridge.simulate_office_hour()
        time.sleep(0.5)
        
    print("\n" + "=" * 60)
    print("📊 Final Office State:")
    print(bridge.get_office_snapshot())


if __name__ == "__main__":
    main()
