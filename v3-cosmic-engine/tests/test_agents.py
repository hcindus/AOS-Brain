"""Tests for agent modules."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.archetype import ARCHETYPES, get_archetype
from agents.agent import Agent, Personality, Memory
from agents.dreams import DreamEngine
from agents.lineage import Lineage
from core.world import SharedWorld


def test_archetypes():
    """Test archetype system."""
    assert "warrior" in ARCHETYPES
    assert "mystic" in ARCHETYPES
    
    warrior = get_archetype("warrior")
    assert warrior.aggression > 0
    print("✓ Archetype test passed")


def test_personality():
    """Test personality system."""
    personality = Personality(archetype="warrior")
    
    # Warrior should have higher aggression
    assert personality.get_trait("aggression") > 0.5
    assert personality.get_trait("courage") > 0.5
    print("✓ Personality test passed")


def test_agent_creation():
    """Test agent creation."""
    world = SharedWorld()
    agent = Agent(name="TestAgent", world=world)
    
    assert agent.name == "TestAgent"
    assert agent.age == 0
    assert agent.energy == 1.0
    print("✓ Agent creation test passed")


def test_memory():
    """Test memory system."""
    memory = Memory()
    
    memory.add("test_memory")
    assert len(memory.short_term) == 1
    
    recent = memory.get_recent(1)
    assert recent[0] == "test_memory"
    print("✓ Memory test passed")


def test_dream_engine():
    """Test dream engine."""
    world = SharedWorld()
    agent = Agent(name="Dreamer", world=world)
    agent.personality = Personality(archetype="mystic")
    
    dream_engine = DreamEngine(agent)
    dream = dream_engine.dream()
    
    assert len(dream_engine.dreams) == 1
    assert dream_engine.dream_intensity > 0
    print("✓ Dream engine test passed")


def test_lineage():
    """Test lineage system."""
    lineage = Lineage()
    
    lineage.record_birth("Parent", "Child", "Test birth")
    assert lineage.get_ancestry_depth() == 1
    
    summary = lineage.get_lineage_summary()
    assert "Child of Parent" in summary
    print("✓ Lineage test passed")


if __name__ == "__main__":
    test_archetypes()
    test_personality()
    test_agent_creation()
    test_memory()
    test_dream_engine()
    test_lineage()
    print("\nAll agent tests passed!")
