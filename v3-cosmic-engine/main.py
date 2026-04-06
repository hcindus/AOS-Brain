#!/usr/bin/env python3
"""Main entry point for the V3 Multi-Agent Cosmic Simulation Engine."""
from __future__ import annotations

import random
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.world import SharedWorld
from core.history import History
from core.cosmology import Cosmology, CosmicEvents, EraEngine
from core.scheduler import Scheduler
from core.runtime import WorldTickPipeline, MultiAgentRuntime
from agents.agent import Agent
from agents.archetype import ARCHETYPES
from agents.dreams import DreamEngine
from agents.lineage import Lineage
from ui.dashboard import MultiAgentDashboard
from ui.visualizer import XLockStyleVisualizer
from config import SEED, MAX_TICKS, SAVE_HISTORY, INITIAL_AGENTS


def build_system() -> MultiAgentRuntime:
    """Build and wire the entire simulation system."""
    # Core world state
    world = SharedWorld()
    history = History(world)
    history.load_if_exists()
    
    # Cosmic / Mythic layer
    cosmology = Cosmology(world)
    cosmology.generate_creation_myth()
    cosmic_events = CosmicEvents(world, cosmology)
    era_engine = EraEngine(world)
    
    # World simulation pipeline
    world_pipeline = WorldTickPipeline(
        world=world,
        cosmology=cosmology,
        cosmic_events=cosmic_events,
        era_engine=era_engine,
    )
    scheduler = Scheduler(world, world_pipeline)
    
    # Spawn initial agents
    agents = []
    for name in INITIAL_AGENTS:
        agent = Agent(name=name, world=world)
        agent.archetype = random.choice(list(ARCHETYPES.keys()))
        
        # Attach cosmic / inner layers
        agent.dream_engine = DreamEngine(agent)
        agent.lineage = Lineage(agent)
        
        # Attach to scheduler
        scheduler.add_agent(agent)
        agents.append(agent)
    
    # UI & Visualization layers (presentation only)
    dashboard = MultiAgentDashboard(world, agents)
    visualizer = XLockStyleVisualizer(world, agents)
    
    # Final runtime
    runtime = MultiAgentRuntime(
        world=world,
        scheduler=scheduler,
        dashboard=dashboard,
        visualizer=visualizer,
        history=history,
    )
    return runtime


def main() -> None:
    """Run the cosmic simulation."""
    random.seed(SEED)
    print("🌌 Awakening the Cosmic Simulation...")
    print(f"   Seed: {SEED}")
    print(f"   Max Ticks: {MAX_TICKS}")
    print(f"   Initial Agents: {', '.join(INITIAL_AGENTS)}")
    print()
    
    system = build_system()
    
    try:
        system.start(max_ticks=MAX_TICKS)
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
    finally:
        if SAVE_HISTORY:
            system.history.save()
        print("World history archived. Goodbye.")


if __name__ == "__main__":
    main()
