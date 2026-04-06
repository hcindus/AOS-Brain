"""Scheduler for agent and world tick coordination."""
from __future__ import annotations

from typing import List, Any, Optional
from dataclasses import dataclass


@dataclass
class AgentTask:
    """A task for an agent to execute."""
    agent: Any
    priority: int = 0
    completed: bool = False


class Scheduler:
    """Schedules agent ticks and coordinates with world pipeline."""
    
    def __init__(self, world: Any, world_pipeline: Any):
        self.world = world
        self.world_pipeline = world_pipeline
        self.agents: List[Any] = []
        self.tasks: List[AgentTask] = []
        self.current_tick: int = 0
    
    def add_agent(self, agent: Any) -> None:
        """Add an agent to the scheduler."""
        self.agents.append(agent)
        self.tasks.append(AgentTask(agent=agent))
    
    def remove_agent(self, agent: Any) -> None:
        """Remove an agent from the scheduler."""
        self.agents = [a for a in self.agents if a != agent]
        self.tasks = [t for t in self.tasks if t.agent != agent]
    
    def tick(self) -> None:
        """Execute one tick: world pipeline then all agents."""
        self.current_tick = getattr(self.world, 'turn', 0)
        
        # Run world pipeline first
        self.world_pipeline.tick()
        
        # Then run all agents
        for agent in self.agents:
            if hasattr(agent, 'tick'):
                agent.tick()
        
        # Update tasks
        for task in self.tasks:
            task.completed = True
    
    def get_active_agents(self) -> List[Any]:
        """Get list of active agents."""
        return [a for a in self.agents if hasattr(a, 'active') and a.active]
    
    def get_agent_count(self) -> int:
        """Get total number of agents."""
        return len(self.agents)
    
    def reset_tasks(self) -> None:
        """Reset all tasks for a new tick cycle."""
        for task in self.tasks:
            task.completed = False
