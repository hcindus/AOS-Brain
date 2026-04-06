"""Tests for cosmology module."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.world import SharedWorld
from core.cosmology import Cosmology, CosmicEvents, EraEngine


def test_cosmology_creation():
    """Test cosmology initialization."""
    world = SharedWorld()
    cosmology = Cosmology(world)
    
    assert cosmology.creation_myth == ""
    assert len(cosmology.events) == 0
    print("✓ Cosmology creation test passed")


def test_creation_myth():
    """Test creation myth generation."""
    world = SharedWorld()
    cosmology = Cosmology(world)
    
    cosmology.generate_creation_myth()
    assert len(cosmology.creation_myth) > 0
    assert "primordial" in cosmology.creation_myth
    print("✓ Creation myth test passed")


def test_cosmic_events():
    """Test cosmic events system."""
    world = SharedWorld()
    cosmology = Cosmology(world)
    cosmic_events = CosmicEvents(world, cosmology)
    
    # Trigger manually to test
    cosmic_events.trigger_event("comet")
    
    assert len(cosmology.events) == 1
    assert cosmology.events[0].type == "comet"
    print("✓ Cosmic events test passed")


def test_era_engine():
    """Test era engine."""
    world = SharedWorld()
    era_engine = EraEngine(world)
    
    assert world.era == "dawn"
    assert era_engine.era_index == 0
    
    # Test tick progression
    era_engine.tick()
    assert era_engine.era_duration == 1
    print("✓ Era engine test passed")


if __name__ == "__main__":
    test_cosmology_creation()
    test_creation_myth()
    test_cosmic_events()
    test_era_engine()
    print("\nAll cosmology tests passed!")
