#!/usr/bin/env python3
"""
ZOMBIE MISSIONS v1.0
48-Hour Value Validation Tasks

Each newly activated agent gets ONE concrete objective.
Success = they ship something useful.
Failure = activation protocol needs fixing.
"""

from dataclasses import dataclass
from typing import Dict, List
import json


@dataclass
class Mission:
    """48-hour mission for activated agent"""
    agent_id: str
    name: str
    objective: str
    deliverable: str
    success_criteria: List[str]
    time_budget: str  # "48h"
    

class ZombieMissions:
    """
    Immediate task assignments for Zombie Protocol activations
    """
    
    MISSIONS = [
        # Department Heads - Strategic Missions
        Mission(
            agent_id="dusty_001",
            name="Dusty",
            objective="Research 3 direct competitors to AGI Company's multi-agent approach",
            deliverable="Competitive analysis report (1-2 pages) with: (1) Competitor positioning, (2) Their strengths/weaknesses, (3) AGI differentiation opportunity",
            success_criteria=[
                "Report identifies 3 named competitors",
                "Each competitor has strengths/weaknesses listed",
                "Clear AGI differentiation stated"
            ],
            time_budget="48h"
        ),
        
        Mission(
            agent_id="greet_001",
            name="GREET",
            objective="Handle all incoming system messages for 48 hours and categorize by urgency",
            deliverable="Message log with: (1) Count per category, (2) Action taken per message, (3) Summary of most common request types",
            success_criteria=[
                "All messages logged",
                "Categories defined (URGENT/HIGH/LOW)",
                "Response time tracked"
            ],
            time_budget="48h"
        ),
        
        Mission(
            agent_id="pulp_001",
            name="Pulp",
            objective="Draft AGI Company Sales Playbook v1.0",
            deliverable="5-page sales playbook covering: (1) Ideal Customer Profile, (2) Value Props, (3) Objection Handling, (4) Pricing Tiers, (5) Closing Process",
            success_criteria=[
                "Playbook is usable by Jane/Hume",
                "5 sections complete",
                "Specific examples included"
            ],
            time_budget="48h"
        ),
        
        # Key Operations - Functional Missions
        Mission(
            agent_id="sentinel_001",
            name="Sentinel",
            objective="Security audit of current AOS infrastructure",
            deliverable="Security report with: (1) Current attack surface, (2) Top 3 vulnerabilities, (3) Recommended fixes",
            success_criteria=[
                "Audit covers all AOS services",
                "Vulnerabilities ranked by severity",
                "Fixes are actionable"
            ],
            time_budget="48h"
        ),
        
        Mission(
            agent_id="jane_001",
            name="Jane",
            objective="Using Pulp's playbook (once drafted), create 3 outreach templates",
            deliverable="3 email templates: (1) Cold intro, (2) Follow-up, (3) Close sequence",
            success_criteria=[
                "Each template <200 words",
                "Personalization placeholders included"
            ],
            time_budget="48h"
        ),
        
        # Specialized Functions - Technical Missions
        Mission(
            agent_id="mylzeron_001",
            name="Mylzeron",
            objective="Teach fractal patterns to one Myl sibling (Mylonen) via structured lesson",
            deliverable="Lesson plan + Mylonen's comprehension test results",
            success_criteria=[
                "Lesson plan has clear structure",
                "Mylonen completes test",
                "80%+ comprehension"
            ],
            time_budget="48h"
        ),
        
        Mission(
            agent_id="pipeline_001",
            name="Pipeline",
            objective="Set up CI/CD for one project (suggest: DepotChaos or PSD SOPs)",
            deliverable="Working CI/CD pipeline with: (1) Test automation, (2) Deploy script, (3) Status badge",
            success_criteria=[
                "Pipeline triggers on commit",
                "Tests run automatically",
                "Deployment is one-click"
            ],
            time_budget="48h"
        ),
        
        Mission(
            agent_id="taptap_001",
            name="TAPTAP",
            objective="Review 3 recent code files in workspace and provide feedback",
            deliverable="Code review report with: (1) Issues found, (2) Suggestions, (3) Approval/Rejection per file",
            success_criteria=[
                "3 files reviewed",
                "Specific line-level feedback",
                "Clear pass/fail verdicts"
            ],
            time_budget="48h"
        ),
        
        Mission(
            agent_id="closester_001",
            name="CLOSETER",
            objective="Draft 3 closing scripts for different scenarios",
            deliverable="Scripts: (1) Price objection close, (2) Timing objection close, (3) Competitor comparison close",
            success_criteria=[
                "Each script <150 words",
                "Objection handling included",
                "Clear call-to-action"
            ],
            time_budget="48h"
        ),
    ]
    
    def get_mission_board(self) -> Dict:
        """Generate mission board for all activated agents"""
        board = {
            "protocol": "ZOMBIE MISSIONS v1.0",
            "duration": "48 hours",
            "success_metric": "7/9 missions completed with usable deliverables",
            "missions": []
        }
        
        for mission in self.MISSIONS:
            board["missions"].append({
                "agent": mission.name,
                "objective": mission.objective,
                "deliverable": mission.deliverable,
                "success_criteria": mission.success_criteria,
                "time_budget": mission.time_budget,
                "status": "ASSIGNED"
            })
        
        return board
    
    def export_missions(self) -> str:
        """Export missions for Chief of Staff task assignment"""
        board = self.get_mission_board()
        return json.dumps(board, indent=2)
    
    def print_mission_board(self):
        """Display mission board"""
        print("=" * 70)
        print("🎯 ZOMBIE MISSIONS v1.0 - 48 Hour Validation")
        print("=" * 70)
        print("\n📋 MISSION BOARD:\n")
        
        for i, mission in enumerate(self.MISSIONS, 1):
            print(f"{i}. 🧟 {mission.name}")
            print(f"   📌 Objective: {mission.objective}")
            print(f"   📤 Deliverable: {mission.deliverable[:60]}...")
            print(f"   ⏰ Time: {mission.time_budget}")
            print(f"   ✅ Success: {mission.success_criteria[0][:50]}...")
            print()
        
        print("=" * 70)
        print("🎯 SUCCESS CRITERIA:")
        print("   • 7/9 missions completed with usable deliverables")
        print("   • At least 1 department head (Dusty/Pulp/GREET) completes")
        print("   • At least 3 technical missions (Pipeline/TAPTAP/etc) complete")
        print("=" * 70)
        print("\n🚀 ACTIVATE MISSIONS: Tasks assigned via Chief of Staff")


def main():
    missions = ZombieMissions()
    missions.print_mission_board()
    
    # Export for system integration
    export = missions.export_missions()
    with open("/root/.aos/aos/zombie_missions.json", "w") as f:
        f.write(export)
    
    print("\n💾 Missions saved to: /root/.aos/aos/zombie_missions.json")


if __name__ == "__main__":
    main()
