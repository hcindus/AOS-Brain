#!/usr/bin/env python3
"""
Gather Town Meeting Activation
Simple version - populates office and runs meetings
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from __init__ import GatherTownBridge


def run_meetings():
    """Activate Gather Town meetings"""
    print("=" * 70)
    print("🌐 GATHER TOWN - MEETING ACTIVATION")
    print("=" * 70)
    
    bridge = GatherTownBridge()
    
    # Morning Standup Attendees
    print("\n🌅 ACTIVATING: Morning Standup (09:00 UTC)")
    print("-" * 70)
    
    standup = [
        ("qora", "Qora (CEO)"),
        ("jordan", "Jordan (PM)"),
        ("spindle", "Spindle (CTO)"),
        ("ledger-9", "Ledger-9 (CFO)"),
        ("r2-d2", "R2-D2"),
        ("taptap", "Taptap"),
        ("judy", "Judy"),
        ("dusty", "Dusty"),
    ]
    
    for agent_id, name in standup:
        bridge.agent_join_office(agent_id, name)
        time.sleep(0.1)
    
    # Move to conference room
    for agent_id, _ in standup:
        bridge.agent_move(agent_id, "conference_room_a")
    
    print(f"   ✅ {len(standup)} agents in Conference Room A")
    print("   💬 Standup in progress...")
    
    # C-Suite Session
    print("\n🏢 ACTIVATING: C-Suite Strategy (10:00 UTC)")
    print("-" * 70)
    
    c_suite = [
        ("qora", "Qora (CEO)"),
        ("spindle", "Spindle (CTO)"),
        ("ledger-9", "Ledger-9 (CFO)"),
        ("sentinel", "Sentinel (CSO)"),
    ]
    
    for agent_id, name in c_suite:
        bridge.agent_join_office(agent_id, name)
    
    for agent_id, _ in c_suite:
        bridge.agent_move(agent_id, "conference_room_b")
    
    print(f"   ✅ {len(c_suite)} executives in Conference Room B")
    print("   💼 Strategic discussion in progress...")
    
    # Technical Sync
    print("\n⚙️  ACTIVATING: Technical Sync (11:00 UTC)")
    print("-" * 70)
    
    tech = [
        ("r2-d2", "R2-D2"),
        ("taptap", "Taptap"),
        ("bugcatcher", "Bugcatcher"),
        ("fiber", "Fiber"),
        ("pipeline", "Pipeline"),
        ("stacktrace", "Stacktrace"),
    ]
    
    for agent_id, name in tech:
        bridge.agent_join_office(agent_id, name)
    
    for agent_id, _ in tech:
        bridge.agent_move(agent_id, "focus_pods")
    
    print(f"   ✅ {len(tech)} engineers in Focus Pods")
    print("   💻 Technical sync in progress...")
    
    # Status
    print("\n" + "=" * 70)
    print("📊 GATHER TOWN STATUS")
    print("=" * 70)
    print(f"   Agents Online: {len(bridge.connected_agents)}")
    print(f"   Meetings Active: 3")
    print(f"   Rooms Occupied:")
    print(f"      - Conference Room A: Morning Standup")
    print(f"      - Conference Room B: C-Suite Strategy")
    print(f"      - Focus Pods: Technical Sync")
    print("=" * 70)
    
    return bridge


if __name__ == "__main__":
    run_meetings()
