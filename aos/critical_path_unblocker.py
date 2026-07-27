#!/usr/bin/env python3
"""
CRITICAL PATH UNBLOCKER v1.0
Addressing 24h Checkpoint Blockers

PROBLEM:
- Z5 (Jane templates) BLOCKED → waiting Z3 (Pulp playbook)
- Z9 (CLOSETER scripts) BLOCKED → waiting Z3 (Pulp playbook)

SOLUTION:
1. Escalate Pulp (Z3) to priority
2. Enable partial delivery (v0.5 playbook) to unblock dependents
3. Establish handoff protocol for cross-dept workflows
4. Track ripple effects
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json


class UnblockStrategy(Enum):
    ESCALATE = "escalate"           # Priority boost + resources
    PARTIAL = "partial"             # Deliver MVP to unblock
    PARALLEL = "parallel"           # Start dependent work early
    REDIRECT = "redirect"           # Route around blocker


@dataclass
class BlockedMission:
    mission_id: str
    agent: str
    blocked_by: str
    blocker_agent: str
    impact: str
    strategy: UnblockStrategy
    action: str


class CriticalPathUnblocker:
    """
    Unblocks critical path dependencies
    """
    
    def __init__(self):
        self.blocked: List[BlockedMission] = []
        self.unblock_actions: Dict[str, Dict] = {}
        self._identify_blockers()
    
    def _identify_blockers(self):
        """Identify and categorize blockers"""
        
        self.blocked = [
            BlockedMission(
                mission_id="Z5",
                agent="Jane",
                blocked_by="Z3",
                blocker_agent="Pulp",
                impact="Sales outreach templates - revenue critical",
                strategy=UnblockStrategy.PARTIAL,
                action="Deliver playbook sections 1-3 (ICP, Value Props, Pricing) to unblock templates"
            ),
            BlockedMission(
                mission_id="Z9", 
                agent="CLOSETER",
                blocked_by="Z3",
                blocker_agent="Pulp",
                impact="Closing scripts - conversion critical",
                strategy=UnblockStrategy.PARTIAL,
                action="Deliver playbook closing section (section 5) to unblock scripts"
            )
        ]
        
        # Define unblock actions for Pulp
        self.unblock_actions = {
            "Pulp": {
                "priority": "CRITICAL",
                "current_eta": "48h (full playbook)",
                "accelerated_eta": "12h (MVP playbook)",
                "MVP_scope": "Sections 1,2,5 only (ICP, Value Props, Closing)",
                "resources": "Aurora (design support), Dusty (research input)",
                "handoff_protocol": {
                    "step1": "Pulp submits v0.5 playbook to shared workspace",
                    "step2": "Jane notified: sections 1-3 available",
                    "step3": "CLOSETER notified: section 5 available", 
                    "step4": "Pulp continues full playbook (48h target)",
                    "step5": "Jane/CLOSETER work in parallel on dependent missions"
                }
            }
        }
    
    def get_escalation_plan(self) -> Dict:
        """Full escalation plan"""
        return {
            "trigger": "24h checkpoint: 2 missions blocked on Z3",
            "priority": "CRITICAL",
            "blocker": "Pulp (Z3) - Sales Playbook",
            "dependents": ["Jane (Z5)", "CLOSETER (Z9)"],
            "business_impact": "Sales infrastructure delayed → revenue at risk",
            "plan": {
                "phase1": {
                    "name": "MVP Delivery",
                    "duration": "12 hours",
                    "deliverable": "Playbook sections 1,2,5 (ICP, Value Props, Closing)",
                    "unblocks": ["Z5 (Jane templates)", "Z9 (CLOSETER scripts)"]
                },
                "phase2": {
                    "name": "Parallel Execution", 
                    "duration": "36 hours",
                    "parallel_work": [
                        "Pulp: completes sections 3,4 (Objections, Process)",
                        "Jane: creates templates from sections 1-3",
                        "CLOSETER: drafts scripts from section 5"
                    ]
                },
                "phase3": {
                    "name": "Integration",
                    "duration": "End of 48h",
                    "deliverable": "Complete playbook + templates + scripts"
                }
            }
        }
    
    def get_cross_dept_handoff_protocol(self) -> Dict:
        """First cross-department workflow protocol"""
        return {
            "workflow_name": "Sales Playbook → Templates/Scripts",
            "departments": ["Sales (Pulp)", "Sales (Jane)", "Sales (CLOSETER)"],
            "handoff_type": "Document-based dependency",
            "protocol": {
                "step1_producer": {
                    "agent": "Pulp",
                    "action": "Publish MVP sections to /shared/sales/playbook_v0.5.md",
                    "notify": ["Jane", "CLOSETER", "Jordan"]
                },
                "step2_consumers": {
                    "agents": ["Jane", "CLOSETER"],
                    "action": "Pull relevant sections, begin parallel work",
                    "acknowledge": "Reply to Pulp with 'Sections received, starting work'"
                },
                "step3_tracking": {
                    "system": "Mission Control",
                    "action": "Update Z5, Z9 status to 'IN_PROGRESS'",
                    "note": "Blocked → Active (parallel phase)"
                },
                "step4_completion": {
                    "trigger": "All 3 missions complete",
                    "action": "Archive workflow as first cross-dept success",
                    "document": "Template for future dependencies"
                }
            },
            "success_criteria": [
                "Pulp delivers MVP within 12h",
                "Jane/CLOSETER acknowledge receipt within 1h",
                "All 3 missions complete by 48h",
                "Handoff latency <2h (Pulp delivery → Jane/CLOSETER start)"
            ]
        }
    
    def get_ripple_effect_analysis(self) -> Dict:
        """Analyze what unblocking enables"""
        return {
            "unblock_pulp": {
                "direct": ["Z5 (Jane)", "Z9 (CLOSETER)"],
                "indirect": [
                    "Sales dept reaches 4/4 missions complete",
                    "Sales infrastructure ready for 2,911 leads",
                    "Cross-dept workflow proven"
                ],
                "revenue_impact": "2,911 leads × scripts/templates = $X potential"
            },
            "if_not_unblocked": {
                "risk": "Sales missions fail (2/4 incomplete)",
                "validation": "Below 7/12 threshold",
                "consequence": "Reassess Zombie Protocol efficacy"
            }
        }
    
    def print_unblock_plan(self):
        """Print the full unblock plan"""
        print("=" * 70)
        print("🚨 CRITICAL PATH UNBLOCKER v1.0")
        print("=" * 70)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
        print(f"Trigger: 24h checkpoint - 2 missions blocked")
        print("=" * 70)
        
        print("\n🚧 BLOCKED MISSIONS")
        print("-" * 70)
        for b in self.blocked:
            print(f"\n  {b.mission_id}: {b.agent}")
            print(f"    ↳ Waiting for: {b.blocker_agent} ({b.blocked_by})")
            print(f"    ↳ Impact: {b.impact}")
            print(f"    ↳ Strategy: {b.strategy.value}")
            print(f"    ↳ Action: {b.action}")
        
        print("\n" + "=" * 70)
        print("🎯 ESCALATION PLAN")
        print("=" * 70)
        plan = self.get_escalation_plan()
        print(f"\nBlocker: {plan['blocker']}")
        print(f"Dependents: {', '.join(plan['dependents'])}")
        print(f"Business Impact: {plan['business_impact']}")
        
        for phase_name, phase in plan['plan'].items():
            print(f"\n  📍 {phase['name']} ({phase['duration']})")
            if 'deliverable' in phase:
                print(f"     Deliverable: {phase['deliverable']}")
            if 'parallel_work' in phase:
                print(f"     Parallel work:")
                for work in phase['parallel_work']:
                    print(f"       • {work}")
        
        print("\n" + "=" * 70)
        print("🔗 CROSS-DEPT HANDOFF PROTOCOL")
        print("=" * 70)
        protocol = self.get_cross_dept_handoff_protocol()
        print(f"\nWorkflow: {protocol['workflow_name']}")
        print(f"Participants: {', '.join(protocol['departments'])}")
        
        for step_name, step in protocol['protocol'].items():
            print(f"\n  {step_name.replace('_', ' ').title()}:")
            if isinstance(step, dict):
                for k, v in step.items():
                    print(f"    {k}: {v}")
        
        print("\n  Success Criteria:")
        for criteria in protocol['success_criteria']:
            print(f"    ✅ {criteria}")
        
        print("\n" + "=" * 70)
        print("🌊 RIPPLE EFFECT ANALYSIS")
        print("=" * 70)
        ripple = self.get_ripple_effect_analysis()
        print("\n  If Pulp unblocked:")
        print(f"    Direct: {', '.join(ripple['unblock_pulp']['direct'])}")
        print(f"    Indirect:")
        for effect in ripple['unblock_pulp']['indirect']:
            print(f"      → {effect}")
        
        print("\n  If NOT unblocked:")
        print(f"    Risk: {ripple['if_not_unblocked']['risk']}")
        print(f"    Consequence: {ripple['if_not_unblocked']['consequence']}")
        
        print("\n" + "=" * 70)
        print("✅ IMMEDIATE ACTIONS")
        print("=" * 70)
        print("  1. Escalate Pulp to CRITICAL priority")
        print("  2. Aurora offers design support (playbook formatting)")
        print("  3. Dusty provides competitor intel (section 2 input)")
        print("  4. Pulp delivers v0.5 playbook in 12h")
        print("  5. Jane/CLOSETER acknowledge → begin parallel work")
        print("  6. Mission Control tracks handoff latency")
        print("=" * 70)


def main():
    """Run unblocker"""
    unblocker = CriticalPathUnblocker()
    unblocker.print_unblock_plan()
    
    # Export
    export = {
        "timestamp": datetime.now().isoformat(),
        "trigger": "24h checkpoint",
        "blocked_missions": [
            {"id": b.mission_id, "agent": b.agent, "blocked_by": b.blocked_by}
            for b in unblocker.blocked
        ],
        "escalation_plan": unblocker.get_escalation_plan(),
        "handoff_protocol": unblocker.get_cross_dept_handoff_protocol(),
        "ripple_effects": unblocker.get_ripple_effect_analysis()
    }
    
    with open("/root/.aos/aos/critical_path_unblocker.json", "w") as f:
        json.dump(export, f, indent=2)
    
    print("\n💾 Plan saved: /root/.aos/aos/critical_path_unblocker.json")


if __name__ == "__main__":
    main()
