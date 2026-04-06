"""X-Lock style visualizer for cosmic simulation."""
from __future__ import annotations

import random
from typing import List, Any, Dict, Optional, Tuple


class XLockStyleVisualizer:
    """X-Lock style ASCII visualizer for the cosmic simulation."""
    
    SYMBOLS = {
        "agent": ["☀", "☽", "★", "✦", "✧", "⊙", "◉"],
        "cosmic": ["✴", "✷", "✸", "✹", "✻", "✼", "❋"],
        "void": ["·", "˖", "‧", "∘", "○", "◌", "◯"],
        "event": ["⚡", "✧", "✦", "◈", "◇"],
    }
    
    def __init__(self, world: Any, agents: List[Any]):
        self.world = world
        self.agents = agents
        self.width = 40
        self.height = 12
        self.frame_count = 0
    
    def render(self) -> str:
        """Render a cosmic visualization frame."""
        self.frame_count += 1
        
        lines = []
        lines.append("┌" + "─" * self.width + "┐")
        lines.append("│" + " COSMIC FIELD ".center(self.width) + "│")
        lines.append("├" + "─" * self.width + "┤")
        
        # Generate starfield
        grid = self._generate_starfield()
        
        # Add agents
        self._add_agents_to_grid(grid)
        
        # Add cosmic events
        self._add_events_to_grid(grid)
        
        # Render grid
        for row in grid:
            lines.append("│" + "".join(row) + "│")
        
        lines.append("└" + "─" * self.width + "┘")
        
        output = "\n".join(lines)
        print(output)
        return output
    
    def _generate_starfield(self) -> List[List[str]]:
        """Generate a random starfield."""
        grid = []
        for y in range(self.height - 4):  # Account for borders
            row = []
            for x in range(self.width):
                if random.random() < 0.15:
                    symbol = random.choice(self.SYMBOLS["void"])
                    row.append(symbol)
                else:
                    row.append(" ")
            grid.append(row)
        return grid
    
    def _add_agents_to_grid(self, grid: List[List[str]]) -> None:
        """Add agent symbols to the grid."""
        for i, agent in enumerate(self.agents[:7]):  # Limit to 7 agents
            y = (i * 2 + self.frame_count) % len(grid)
            x = (i * 5 + self.frame_count // 2) % self.width
            
            symbol = self.SYMBOLS["agent"][i % len(self.SYMBOLS["agent"])]
            
            if 0 <= y < len(grid) and 0 <= x < self.width:
                grid[y][x] = symbol
    
    def _add_events_to_grid(self, grid: List[List[str]]) -> None:
        """Add recent cosmic events to the grid."""
        recent_events = []
        if hasattr(self.world, 'events'):
            recent_events = self.world.events[-3:]
        
        for i, event in enumerate(recent_events):
            y = random.randint(0, len(grid) - 1)
            x = random.randint(0, self.width - 1)
            
            symbol = random.choice(self.SYMBOLS["event"])
            
            if 0 <= y < len(grid) and 0 <= x < self.width:
                grid[y][x] = symbol
    
    def get_frame_info(self) -> Dict[str, Any]:
        """Get information about the current frame."""
        return {
            "frame": self.frame_count,
            "agents_rendered": min(len(self.agents), 7),
            "grid_size": f"{self.width}x{self.height}",
        }
