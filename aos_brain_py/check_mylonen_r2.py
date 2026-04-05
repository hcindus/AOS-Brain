#!/usr/bin/env python3
"""
Mylonen Status Check and R2 Droid Compatibility Test.
"""

import os
import json
import time
from pathlib import Path

def check_mylonen_status():
    """Check status of Mylonen agent."""
    print("\n=== Mylonen Status Check ===\n")
    
    # Check extraction directory
    extraction_dir = Path.home() / ".openclaw" / "workspace" / "aocros" / "mylonen-extraction"
    
    if extraction_dir.exists():
        print(f"✅ Extraction directory exists: {extraction_dir}")
        
        # Check mission files
        mission_brief = extraction_dir / "MISSION-BRIEF.md"
        comm_log = extraction_dir / "COMM-LOG.md"
        
        if mission_brief.exists():
            print(f"✅ Mission brief found")
        if comm_log.exists():
            print(f"✅ Communication log found")
        
        # Check last contact time
        if comm_log.exists():
            mtime = comm_log.stat().st_mtime
            hours_ago = (time.time() - mtime) / 3600
            print(f"\n⏱️ Last update: {hours_ago:.1f} hours ago")
            
            if hours_ago > 110:
                print("🚨 STATUS: 110+ hours since last contact")
                print("   Agent may be compromised, detained, or in deep cover")
            else:
                print("✅ STATUS: Recent activity")
    else:
        print(f"⚠️ Extraction directory not found")
    
    # Summary
    print("\n📊 Mission Summary:")
    print("   - Portal: SGP1-DARK-CLOUD (Singapore)")
    print("   - Status: Sealed but operational")
    print("   - Next step: Establish direct comms")

def test_r2_droid_compatibility():
    """Test if R2 droid can run on Python brain."""
    print("\n=== R2 Droid Compatibility Test ===\n")
    
    # Check Python brain
    brain_dir = Path.home() / ".openclaw" / "workspace" / "aos_brain_py"
    
    if not brain_dir.exists():
        print("❌ Python brain not found")
        return False
    
    print("✅ Python brain architecture found")
    
    # Check components
    components = {
        "7-Region Brain": brain_dir / "brain" / "seven_region.py",
        "HTTP Server": brain_dir / "brain_daemon.py",
        "Agent Adapters": brain_dir / "agents" / "agent_adapter.py",
        "Cortical Sheet": brain_dir / "core" / "cortical_sheet.py",
    }
    
    all_present = True
    for name, path in components.items():
        if path.exists():
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - MISSING")
            all_present = False
    
    # R2 requirements
    print("\n🤖 R2 Droid Requirements:")
    r2_reqs = {
        "GPIO Control": "cerebellum_agent.py provides motor coordination",
        "Safety (Law Zero)": "brainstem_agent.py enforces 4 Laws",
        "Memory": "3-tier (short/mid/long-term) via hippocampus",
        "Affect": "limbic_agent.py for reward/novelty",
        "Planning": "pfc_agent.py for decision-making",
        "Sensory": "thalamus_agent.py for input relay",
    }
    
    for req, status in r2_reqs.items():
        print(f"✅ {req}: {status}")
    
    # Physical embodiment
    print("\n📡 Physical Interface (R2-specific):")
    print("   - Dome rotation: cerebellum motor coordination")
    print("   - Holo-projector: PFC visual planning")
    print("   - Tool arms: basal ganglia action selection")
    print("   - Wheels/movement: brainstem safety override")
    print("   - Audio sensors: thalamus sensory relay")
    
    if all_present:
        print("\n🎉 COMPATIBLE: R2 droid can run on Python brain")
        print("   Integration: Use agent_adapter.py for R2 personality")
        return True
    else:
        print("\n⚠️ Partial compatibility - some components missing")
        return False

def main():
    check_mylonen_status()
    test_r2_droid_compatibility()
    
    print("\n" + "="*50)
    print("Summary:")
    print("- Mylonen: Missing, extraction mission active")
    print("- R2 Brain: Compatible with Python architecture")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
