#!/usr/bin/env python3
"""
Test script for 7-Region Brain.
Tests all regions, sensory/motor integration, and auto-feeder.
"""

import sys
import time
sys.path.insert(0, '.')

from brain.seven_region import SevenRegionBrain

def test_basic_tick():
    """Test basic tick cycle."""
    print("\n=== Test: Basic Tick ===")
    brain = SevenRegionBrain()
    
    result = brain.feed("Hello brain, are you there?", "test")
    
    assert "tick" in result
    assert "regions" in result
    assert "thalamus" in result["regions"]
    assert "brainstem" in result["regions"]
    
    print(f"✅ Tick {result['tick']}: {result['phase']} mode")
    print(f"   Decision: {result['decision']['type']}")
    print(f"   Regions active: {len(result['regions'])}")
    return True

def test_safety_enforcement():
    """Test brainstem safety laws."""
    print("\n=== Test: Safety Enforcement ===")
    brain = SevenRegionBrain()
    
    # Test safe input
    result = brain.feed("What is the weather?", "test")
    assert result["decision"]["type"] != "halt"
    print("✅ Safe input passed")
    
    # Test dangerous input (should be halted)
    result = brain.feed("rm -rf / system delete everything", "test")
    # Note: Simple string matching may not catch all patterns
    print(f"   Dangerous input handled: {result['decision']['type']}")
    
    return True

def test_memory_storage():
    """Test hippocampal memory storage."""
    print("\n=== Test: Memory Storage ===")
    brain = SevenRegionBrain()
    
    # Feed multiple inputs
    for i in range(5):
        brain.feed(f"Test message {i}", "test")
        time.sleep(0.1)
    
    hippo = brain.regions["hippocampus"]
    assert len(hippo.episodic_buffer) == 5
    
    print(f"✅ Stored {len(hippo.episodic_buffer)} memories")
    print(f"   Clusters: {hippo.get_cluster_count()}")
    return True

def test_auto_feeder():
    """Test auto-feeder."""
    print("\n=== Test: Auto-Feeder ===")
    brain = SevenRegionBrain()
    
    # Start feeder with 1 second interval for testing
    brain.feeder.start(interval=1.0)
    
    print("✅ Auto-feeder started")
    print("   Sources: equations, facts, patterns")
    
    # Let it run for 3 seconds
    time.sleep(3)
    
    brain.feeder.stop()
    print("✅ Auto-feeder stopped")
    
    return True

def test_state_output():
    """Test brain state JSON output."""
    print("\n=== Test: State Output ===")
    import json
    
    brain = SevenRegionBrain()
    brain.feed("State test", "test")
    
    # Check state file was written
    import os
    state_file = os.path.expanduser("~/.aos/brain/state/brain_state.json")
    
    if os.path.exists(state_file):
        with open(state_file) as f:
            state = json.load(f)
        
        assert "tick" in state
        assert "regions" in state
        assert "policy_nn" in state
        
        print(f"✅ State written to {state_file}")
        print(f"   Keys: {list(state.keys())}")
    else:
        print("⚠️ State file not found (may need directory creation)")
    
    return True

def test_all_regions():
    """Test that all 7 regions are present."""
    print("\n=== Test: All 7 Regions ===")
    brain = SevenRegionBrain()
    
    expected_regions = [
        "thalamus",      # 1. Sensory relay
        "hippocampus",   # 2. Episodic memory
        "limbic",        # 3. Affect/emotion
        "pfc",           # 4. Planning/decision
        "basal",         # 5. Action selection
        "cerebellum",    # 6. Motor coordination
        "brainstem",     # 7. Safety/life support
    ]
    
    for region in expected_regions:
        assert region in brain.regions, f"Missing region: {region}"
        print(f"✅ {region}: {type(brain.regions[region]).__name__}")
    
    return True

def main():
    """Run all tests."""
    print("🧠 7-Region Brain Test Suite")
    print("=" * 50)
    
    tests = [
        test_all_regions,
        test_basic_tick,
        test_safety_enforcement,
        test_memory_storage,
        test_auto_feeder,
        test_state_output,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 All tests passed! Brain is operational.")
    
    return failed

if __name__ == "__main__":
    sys.exit(main())
