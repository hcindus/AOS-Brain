"""Runtime and pipeline management for V3 Cosmic Engine."""
from __future__ import annotations

import time
from typing import List, Any, Optional, Dict
from dataclasses import dataclass

from config import TICK_DELAY, DASHBOARD_REFRESH_RATE, VISUALIZATION_ENABLED


@dataclass
class TickMetrics:
    """Metrics for a single tick."""
    tick_number: int
    agent_actions: int
    cosmic_events: int
    duration_ms: float


class WorldTickPipeline:
    """Pipeline for world-level updates each tick."""
    
    def __init__(self, world: Any, cosmology: Any, cosmic_events: Any, era_engine: Any):
        self.world = world
        self.cosmology = cosmology
        self.cosmic_events = cosmic_events
        self.era_engine = era_engine
    
    def tick(self) -> None:
        """Execute one world tick through the pipeline."""
        # Advance world time
        self.world.tick()
        
        # Check for cosmic events
        self.cosmic_events.tick()
        
        # Advance era timing
        self.era_engine.tick()


class MultiAgentRuntime:
    """The main runtime orchestrating the simulation."""
    
    def __init__(self, world: Any, scheduler: Any, dashboard: Any, 
                 visualizer: Any, history: Any):
        self.world = world
        self.scheduler = scheduler
        self.dashboard = dashboard
        self.visualizer = visualizer
        self.history = history
        
        self.running: bool = False
        self.tick_count: int = 0
        self.metrics: List[TickMetrics] = []
        self._should_stop: bool = False
    
    def start(self, max_ticks: int = 1000) -> None:
        """Start the simulation runtime."""
        self.running = True
        self._should_stop = False
        
        print("✨ Cosmic simulation running...")
        print(f"   Agents: {self.scheduler.get_agent_count()}")
        print(f"   Max ticks: {max_ticks}")
        print("\nPress Ctrl+C to stop.\n")
        
        # Initial render
        if self.dashboard:
            self.dashboard.render()
        
        try:
            while self.tick_count < max_ticks and not self._should_stop:
                self._tick()
                
                # Periodic dashboard update
                if self.tick_count % DASHBOARD_REFRESH_RATE == 0:
                    if self.dashboard:
                        self.dashboard.update()
                    if VISUALIZATION_ENABLED and self.visualizer:
                        self.visualizer.render()
                
                # Small delay between ticks
                if TICK_DELAY > 0:
                    time.sleep(TICK_DELAY)
                    
        except KeyboardInterrupt:
            self._should_stop = True
        finally:
            self.running = False
            self._print_summary()
    
    def _tick(self) -> None:
        """Execute a single simulation tick."""
        start_time = time.time()
        
        # Run scheduler (world + agents)
        self.scheduler.tick()
        
        self.tick_count += 1
        
        # Collect metrics
        duration_ms = (time.time() - start_time) * 1000
        metrics = TickMetrics(
            tick_number=self.tick_count,
            agent_actions=len(self.scheduler.agents),
            cosmic_events=len(self.cosmology.events) if hasattr(self.cosmology, 'events') else 0,
            duration_ms=duration_ms,
        )
        self.metrics.append(metrics)
        
        # Check for stop condition
        if hasattr(self.world, 'events') and len(self.world.events) > 1000:
            print("Event limit reached. Stopping.")
            self._should_stop = True
    
    def stop(self) -> None:
        """Signal the runtime to stop."""
        self._should_stop = True
    
    def _print_summary(self) -> None:
        """Print simulation summary."""
        print("\n" + "="*50)
        print("📊 SIMULATION SUMMARY")
        print("="*50)
        print(f"Total ticks: {self.tick_count}")
        print(f"Active agents: {self.scheduler.get_agent_count()}")
        print(f"Current era: {getattr(self.world, 'era', 'unknown')}")
        print(f"Total events: {len(self.world.events) if hasattr(self.world, 'events') else 0}")
        
        if self.metrics:
            avg_duration = sum(m.duration_ms for m in self.metrics) / len(self.metrics)
            print(f"Avg tick duration: {avg_duration:.2f}ms")
        
        print("="*50)
    
    @property
    def cosmology(self) -> Any:
        """Get cosmology from world pipeline if available."""
        if hasattr(self.scheduler, 'world_pipeline'):
            return getattr(self.scheduler.world_pipeline, 'cosmology', None)
        return None
