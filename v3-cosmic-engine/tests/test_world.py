"""Tests for world module."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.world import SharedWorld, Region, WorldEvent


def test_world_creation():
    """Test world initialization."""
    world = SharedWorld()
    assert world.turn == 0
    assert world.era == "dawn"
    assert len(world.regions) > 0
    print("✓ World creation test passed")


def test_region_access():
    """Test region access and creation."""
    world = SharedWorld()
    
    # Get existing region
    heartlands = world.get_region("Heartlands")
    assert heartlands.name == "Heartlands"
    
    # Create new region
    new_region = world.get_region("NewPlace")
    assert new_region.name == "NewPlace"
    print("✓ Region access test passed")


def test_world_tick():
    """Test world tick advancement."""
    world = SharedWorld()
    initial_turn = world.turn
    
    world.tick()
    assert world.turn == initial_turn + 1
    print("✓ World tick test passed")


def test_event_logging():
    """Test event logging."""
    world = SharedWorld()
    
    event = WorldEvent(
        turn=0,
        type="test_event",
        description="A test event",
        impact="Testing"
    )
    
    world.add_event(event)
    assert len(world.events) == 1
    print("✓ Event logging test passed")


if __name__ == "__main__":
    test_world_creation()
    test_region_access()
    test_world_tick()
    test_event_logging()
    print("\nAll world tests passed!")
