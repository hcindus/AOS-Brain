"""Dashboard for multi-agent cosmic simulation."""
from __future__ import annotations

from typing import List, Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class AgentStatus:
    """Status display for an agent."""
    name: str
    archetype: str
    energy: float
    age: int
    last_action: str = ""


class MultiAgentDashboard:
    """Dashboard for monitoring the cosmic simulation."""
    
    def __init__(self, world: Any, agents: List[Any]):
        self.world = world
        self.agents = agents
        self.tick_count = 0
    
    def update(self) -> None:
        """Update dashboard state."""
        self.tick_count = getattr(self.world, 'turn', 0)
    
    def render(self) -> str:
        """Render the dashboard as a string."""
        lines = []
        lines.append("╔" + "═" * 58 + "╗")
        lines.append("║" + " V3 COSMIC ENGINE ".center(58) + "║")
        lines.append("╠" + "═" * 58 + "╣")
        
        # World status
        era = getattr(self.world, 'era', 'unknown')
        turn = getattr(self.world, 'turn', 0)
        lines.append(f"║ Era: {era:<20} Tick: {turn:>30} ║")
        
        # Region count
        region_count = len(getattr(self.world, 'regions', {}))
        lines.append(f"║ Regions: {region_count:<17} Events: {len(getattr(self.world, 'events', [])):>27} ║")
        
        lines.append("╠" + "═" * 58 + "╣")
        lines.append("║ AGENTS" + " " * 50 + "║")
        lines.append("╠" + "─" * 58 + "╣")
        
        # Agent list
        for agent in self.agents[:5]:  # Show first 5 agents
            name = getattr(agent, 'name', 'Unknown')
            archetype = getattr(agent, 'archetype', 'none') or 'none'
            energy = getattr(agent, 'energy', 0.0)
            age = getattr(agent, 'age', 0)
            
            energy_bar = self._bar(energy, 8)
            lines.append(f"║ {name:<12} {archetype:<10} E[{energy_bar}] A:{age:>4} ║")
        
        lines.append("╚" + "═" * 58 + "╝")
        
        output = "\n".join(lines)
        print(output)
        return output
    
    def _bar(self, value: float, width: int) -> str:
        """Create a text bar representation."""
        filled = int(value * width)
        return "█" * filled + "░" * (width - filled)
    
    def get_agent_statuses(self) -> List[AgentStatus]:
        """Get status for all agents."""
        statuses = []
        for agent in self.agents:
            status = AgentStatus(
                name=getattr(agent, 'name', 'Unknown'),
                archetype=getattr(agent, 'archetype', 'none') or 'none',
                energy=getattr(agent, 'energy', 0.0),
                age=getattr(agent, 'age', 0),
            )
            statuses.append(status)
        return statuses
    
    def get_world_summary(self) -> Dict[str, Any]:
        """Get a summary of the world state."""
        return {
            "era": getattr(self.world, 'era', 'unknown'),
            "tick": getattr(self.world, 'turn', 0),
            "regions": len(getattr(self.world, 'regions', {})),
            "events": len(getattr(self.world, 'events', [])),
            "agents": len(self.agents),
        }
