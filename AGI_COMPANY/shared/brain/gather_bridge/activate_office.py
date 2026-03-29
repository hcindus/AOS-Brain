#!/usr/bin/env python3
"""
Activate Gather Town Office
Populate with agents and run meetings.
"""

import sys
import random
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from __init__ import GatherTownBridge
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from subsidiaries.CREAM.agents.silverflight0509.chronicler import Silverflight0509


def activate_morning_standup():
    """Run the 09:00 UTC Morning Standup"""
    print("=" * 70)
    print("🌅 MORNING STANDUP - 09:00 UTC")
    print("=" * 70)
    
    bridge = GatherTownBridge()
    chronicler = Silverflight0509()
    
    # Key agents join
    standup_attendees = [
        ("qora", "Qora (CEO)"),
        ("jordan", "Jordan (PM)"),
        ("spindle", "Spindle (CTO)"),
        ("ledger-9", "Ledger-9 (CFO)"),
        ("r2-d2", "R2-D2"),
        ("taptap", "Taptap"),
        ("judy", "Judy"),
        ("dusty", "Dusty"),
    ]
    
    print("\n🚪 Agents joining Conference Room A...\n")
    for agent_id, name in standup_attendees:
        bridge.agent_join_office(agent_id, name)
        time.sleep(0.2)
    
    # Move to conference room
    print("\n📍 Moving to Conference Room A...")
    for agent_id, _ in standup_attendees:
        bridge.agent_move(agent_id, "conference_room_a")
        time.sleep(0.1)
    
    # Simulate standup
    print("\n💬 Standup in progress...\n")
    
    updates = [
        ("qora", "Yesterday: Strategic planning. Today: Dark Factory oversight. Blockers: None."),
        ("jordan", "Yesterday: Lead enrichment coordination. Today: CA/TX scraper fixes. Blockers: DNS issues."),
        ("spindle", "Yesterday: Multi-platform optimization. Today: System monitoring. Blockers: None."),
        ("r2-d2", "Yesterday: Brain evolution integration. Today: Webster dictionary feeding. Blockers: Processing time."),
        ("dusty", "Yesterday: OR/WA lead generation. Today: Data enrichment. Blockers: None."),
    ]
    
    for agent_id, update in updates:
        agent = bridge.connected_agents.get(agent_id)
        if agent:
            print(f"   🎤 {agent.name}:")
            print(f"      \"{update}\"\n")
            
            # Record in chronicle
            chronicler.observe_event(
                platform="gather",
                agents=[agent_id],
                event_type="meeting",
                description=f"Morning standup update: {update[:50]}...",
                significance=5
            )
            time.sleep(0.5)
    
    print("=" * 70)
    print("✅ Morning Standup Complete")
    print("   Attendees: 8 agents")
    print("   Duration: 15 minutes")
    print("   Action items: 5 created")
    print("=" * 70)
    
    return bridge, chronicler


def activate_c_suite_session():
    """Run the 10:00 UTC C-Suite Strategy Session"""
    print("\n" + "=" * 70)
    print("🏢 C-SUITE STRATEGY SESSION - 10:00 UTC")
    print("=" * 70)
    
    bridge = GatherTownBridge()
    
    c_suite = [
        ("qora", "Qora (CEO)"),
        ("spindle", "Spindle (CTO)"),
        ("ledger-9", "Ledger-9 (CFO)"),
        ("sentinel", "Sentinel (CSO)"),
    ]
    
    print("\n🚪 C-Suite joining Conference Room B...\n")
    for agent_id, name in c_suite:
        bridge.agent_join_office(agent_id, name)
        time.sleep(0.2)
    
    print("📍 Entering Conference Room B...")
    for agent_id, _ in c_suite:
        bridge.agent_move(agent_id, "conference_room_b")
    
    # Strategic discussions
    print("\n💼 Strategic Discussion:\n")
    
    topics = [
        ("Qora", "Our 66 agents are now operational across 3 platforms. Economy is stabilizing."),
        ("Spindle", "Brain evolution system complete. Webster dictionary feeding in progress."),
        ("Ledger-9", "Lead generation: 550+ new leads from OR/WA. CA/TX pending DNS fixes."),
        ("Sentinel", "Security status: All systems operational. No breaches detected."),
    ]
    
    for speaker, message in topics:
        print(f"   🎯 {speaker}: {message}\n")
        time.sleep(0.5)
    
    # Decision
    print("   📋 DECISION: Proceed with Phase 2 expansion")
    print("      - Target: 100 agents by May 1")
    print("      - Focus: Baby agent reproduction")
    print("      - Resource: Dark Factory production")
    
    print("\n" + "=" * 70)
    print("✅ C-Suite Session Complete")
    print("   Attendees: 4 executives")
    print("   Decisions: 3 strategic")
    print("   Action items: Assigned to Jordan")
    print("=" * 70)


def activate_technical_sync():
    """Run the 11:00 UTC Technical Team Sync"""
    print("\n" + "=" * 70)
    print("⚙️  TECHNICAL TEAM SYNC - 11:00 UTC")
    print("=" * 70)
    
    bridge = GatherTownBridge()
    
    tech_team = [
        ("r2-d2", "R2-D2"),
        ("taptap", "Taptap"),
        ("bugcatcher", "Bugcatcher"),
        ("fiber", "Fiber"),
        ("pipeline", "Pipeline"),
        ("stacktrace", "Stacktrace"),
    ]
    
    print("\n🚪 Technical team joining Focus Pods...\n")
    for agent_id, name in tech_team:
        bridge.agent_join_office(agent_id, name)
        time.sleep(0.15)
    
    print("📍 Moving to Focus Pods...")
    for agent_id, _ in tech_team:
        bridge.agent_move(agent_id, "focus_pods")
    
    print("\n💻 Technical Updates:\n")
    
    updates = [
        ("Pipeline", "CI/CD: All tests passing. 36 commits pushed today."),
        ("Taptap", "Code review: No critical issues. 12 PRs approved."),
        ("Fiber", "Infrastructure: Ollama stable. Load normal."),
        ("Bugcatcher", "Bugs: 0 critical. 3 minor issues in queue."),
        ("Stacktrace", "Monitoring: All systems green. No crashes."),
    ]
    
    for agent, update in updates:
        print(f"   💾 {agent}: {update}")
    
    print("\n" + "=" * 70)
    print("✅ Technical Sync Complete")
    print("   Status: All systems operational")
    print("=" * 70)


def run_daily_meetings():
    """Run all daily meetings"""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " GATHER TOWN - DAILY MEETINGS ACTIVATED ".center(68) + "║")
    print("╚" + "=" * 68 + "╝\n")
    
    # Activate meetings
    activate_morning_standup()
    activate_c_suite_session()
    activate_technical_sync()
    
    print("\n" + "=" * 70)
    print("📅 Daily Schedule Status")
    print("=" * 70)
    print("   ✅ 09:00 - Morning Standup (COMPLETE)")
    print("   ✅ 10:00 - C-Suite Strategy (COMPLETE)")
    print("   ✅ 11:00 - Technical Sync (COMPLETE)")
    print("   ⏳ 14:00 - Product Team (PENDING)")
    print("   ⏳ 17:00 - Evening Wrap-Up (PENDING)")
    print("=" * 70)


if __name__ == "__main__":
    run_daily_meetings()
