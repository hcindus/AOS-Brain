#!/usr/bin/env python3
"""
LEAN SUPPORT POOL v1.0
Post-Roast Implementation: Cut 10 → 4 agents

KEPT (4):
- GREET: Dispatcher/Triage (already active)
- Clerk: Records/Documentation  
- R2-D2: Technical Support
- Executive: C-Suite Support

CUT (6):
- C3PO: No use case
- Personal: Overlap with Judy/Executive
- Velvet: No scope
- Judy: Overlap with GREET/Clerk
- Concierge: Overlap with Executive (VIP=C-Suite at current scale)
- CLOSETER: Already in Sales dept under Pulp

Dispatch Protocol:
GREET receives ALL requests → routes to tier:
- General admin → Clerk
- Technical → R2-D2  
- C-Suite only → Executive
- Sales → Pulp/Jane (Sales dept)
- Unknown/Complex → Patricia (escalation)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import json


class SupportTier(Enum):
    TRIAGE = "triage"        # GREET - receives all
    GENERAL = "general"    # Clerk - admin/docs
    TECHNICAL = "technical" # R2-D2 - systems/tech
    EXECUTIVE = "executive" # Executive - C-Suite only
    ESCALATION = "escalation" # Patricia - unknown/complex


@dataclass
class SupportAgent:
    """Lean support pool agent"""
    agent_id: str
    name: str
    tier: SupportTier
    scope: str  # What they handle
    status: str  # ACTIVE / CUT
    reason: str  # Why kept or cut


class LeanSupportPool:
    """
    Consolidated 4-agent support structure
    GREET as dispatcher + 3 execution agents
    """
    
    def __init__(self):
        self.agents: Dict[str, SupportAgent] = {}
        self.dispatcher = "greet_001"
        self._build_lean_pool()
    
    def _build_lean_pool(self):
        """Build the 4-agent lean support pool"""
        
        # === KEPT: Dispatcher ===
        self.agents["greet_001"] = SupportAgent(
            agent_id="greet_001",
            name="GREET",
            tier=SupportTier.TRIAGE,
            scope="Receives ALL requests. Routes: general→Clerk, tech→R2-D2, C-Suite→Executive, sales→Pulp, unknown→Patricia",
            status="ACTIVE",
            reason="Already activated in Zombie Protocol. Natural dispatcher role."
        )
        
        # === KEPT: General Admin ===
        self.agents["clerk_001"] = SupportAgent(
            agent_id="clerk_001",
            name="Clerk",
            tier=SupportTier.GENERAL,
            scope="Records, documentation, filing, data entry. Non-technical, non-executive admin.",
            status="ACTIVE",
            reason="Core function. No overlap with other roles."
        )
        
        # === KEPT: Technical Support ===
        self.agents["r2-d2_001"] = SupportAgent(
            agent_id="r2-d2_001",
            name="R2-D2",
            tier=SupportTier.TECHNICAL,
            scope="Systems access, data retrieval, technical support. Bridge between users and Forge's infrastructure team.",
            status="ACTIVE",
            reason="Unique function. Distinct from Forge's infrastructure work."
        )
        
        # === KEPT: Executive Support ===
        self.agents["executive_001"] = SupportAgent(
            agent_id="executive_001",
            name="Executive",
            tier=SupportTier.EXECUTIVE,
            scope="C-Suite ONLY (Captain, Patricia, Chelios, Forge, Aurora, Jordan). Calendar, gatekeeping, high-touch exec support.",
            status="ACTIVE",
            reason="High-value function. Strict scope prevents overlap."
        )
        
        # === CUT: No Use Case ===
        self.agents["c3po_001"] = SupportAgent(
            agent_id="c3po_001",
            name="C3PO",
            tier=None,
            scope="Protocol/Translation/Etiquette",
            status="CUT",
            reason="No use case for internal AGI Company. All agents speak English. Movie nostalgia, not operational value."
        )
        
        # === CUT: Overlap ===
        self.agents["judy_001"] = SupportAgent(
            agent_id="judy_001",
            name="Judy",
            tier=None,
            scope="Administrative Assistant (scheduling, filing, correspondence)",
            status="CUT",
            reason="Overlap with GREET (scheduling) and Clerk (filing/correspondence). Redundant."
        )
        
        self.agents["personal_001"] = SupportAgent(
            agent_id="personal_001",
            name="Personal",
            tier=None,
            scope="Personal Assistant (personal scheduling, life management, errands)",
            status="CUT",
            reason="Overlap with Executive. No clear distinction between 'personal' and 'executive' at AGI Company scale."
        )
        
        self.agents["concierge_001"] = SupportAgent(
            agent_id="concierge_001",
            name="Concierge",
            tier=None,
            scope="VIP Services (travel coordination, special requests)",
            status="CUT",
            reason="VIP tier unnecessary at current scale. C-Suite is only 'VIP' and handled by Executive."
        )
        
        self.agents["velvet_001"] = SupportAgent(
            agent_id="velvet_001",
            name="Velvet",
            tier=None,
            scope="Specialized Support (discretion, sensitive matters, private tasks)",
            status="CUT",
            reason="No scope defined. 'Sensitive matters' for AI company = what exactly? Invented problem."
        )
        
        # Note: CLOSETER moved to Sales dept (Pulp's team) - not cut, just relocated
    
    def get_dispatch_protocol(self) -> Dict:
        """GREET dispatch protocol - decision tree"""
        return {
            "dispatcher": "GREET",
            "protocol": {
                "Step 1": "GREET receives ALL incoming requests",
                "Step 2": "Classify request type:",
                "routing": {
                    "General admin (filing, records, data entry)": "→ Clerk",
                    "Technical (system access, data retrieval, tech support)": "→ R2-D2",
                    "C-Suite specific (Captain/Patricia/Chelios/Forge/Aurora/Jordan)": "→ Executive",
                    "Sales related (leads, prospects, closing)": "→ Pulp/Jane (Sales dept)",
                    "Unknown / Complex / Escalation needed": "→ Patricia (Chief of Staff)"
                },
                "Step 3": "Log routing decision for accuracy tracking",
                "Step 4": "Follow up: Did recipient resolve? If no → escalate"
            },
            "metrics": {
                "first_route_accuracy": "Target >80%",
                "escalation_rate": "Target <10%",
                "resolution_time": "Track by tier"
            }
        }
    
    def get_comparison(self) -> Dict:
        """Before/After comparison"""
        return {
            "before": {
                "total_agents": 10,
                "active": 2,  # GREET, CLOSETER
                "monthly_cost": "10 × $50/day = $15,000/mo",
                "dispatcher": "None - fragmented",
                "overlap_issues": "Judy/Personal/Executive all do scheduling",
                "use_case_gaps": "C3PO no purpose, Velvet no scope"
            },
            "after": {
                "total_agents": 4,
                "active": 1,  # GREET (activate Clerk, R2-D2, Executive as needed)
                "monthly_cost": "4 × $50/day = $6,000/mo (60% savings)",
                "dispatcher": "GREET - centralized",
                "overlap_issues": "None - clear scope per tier",
                "use_case_gaps": "None - every agent has clear purpose"
            },
            "savings": {
                "agents_cut": 6,
                "monthly_savings": "$9,000/mo",
                "annual_savings": "$108,000/yr",
                "complexity_reduction": "60% fewer handoffs"
            }
        }
    
    def export_structure(self) -> str:
        """Export for Chief of Staff integration"""
        export = {
            "version": "lean_support_v1.0",
            "dispatch_protocol": self.get_dispatch_protocol(),
            "agents": {},
            "cut_agents": [],
            "comparison": self.get_comparison()
        }
        
        for agent_id, agent in self.agents.items():
            if agent.status == "ACTIVE":
                export["agents"][agent_id] = {
                    "name": agent.name,
                    "tier": agent.tier.value if agent.tier else None,
                    "scope": agent.scope
                }
            else:
                export["cut_agents"].append({
                    "agent_id": agent_id,
                    "name": agent.name,
                    "reason": agent.reason
                })
        
        return json.dumps(export, indent=2)
    
    def print_summary(self):
        """Display lean support pool summary"""
        print("=" * 70)
        print("LEAN SUPPORT POOL v1.0 - Post-Roast Implementation")
        print("=" * 70)
        
        print("\n✅ KEPT AGENTS (4):")
        for agent in self.agents.values():
            if agent.status == "ACTIVE":
                print(f"\n  {agent.name}")
                print(f"    Tier: {agent.tier.value.upper()}")
                print(f"    Scope: {agent.scope}")
                print(f"    Reason: {agent.reason}")
        
        print("\n" + "-" * 70)
        print("❌ CUT AGENTS (6):")
        for agent in self.agents.values():
            if agent.status == "CUT":
                print(f"\n  {agent.name}")
                print(f"    Scope: {agent.scope}")
                print(f"    Reason: {agent.reason}")
        
        print("\n" + "=" * 70)
        print("📊 DISPATCH PROTOCOL")
        print("=" * 70)
        protocol = self.get_dispatch_protocol()
        for step, rule in protocol["protocol"].items():
            if isinstance(rule, dict):
                print(f"\n{step}:")
                for key, value in rule.items():
                    print(f"  {key}: {value}")
            else:
                print(f"\n{step}: {rule}")
        
        print("\n" + "=" * 70)
        print("💰 COST SAVINGS")
        print("=" * 70)
        comp = self.get_comparison()
        print(f"  Before: {comp['before']['total_agents']} agents, {comp['before']['monthly_cost']}")
        print(f"  After:  {comp['after']['total_agents']} agents, {comp['after']['monthly_cost']}")
        print(f"  Savings: {comp['savings']['monthly_savings']}/mo ({comp['savings']['annual_savings']}/yr)")
        
        print("\n" + "=" * 70)
        print("🎯 ACTIVATION ORDER")
        print("=" * 70)
        print("  Phase 1: GREET (already active) - dispatcher")
        print("  Phase 2: Clerk - when documentation volume >10 items/day")
        print("  Phase 3: R2-D2 - when technical requests >5/day")
        print("  Phase 4: Executive - when C-Suite time savings >10hrs/week")
        print("=" * 70)


def main():
    pool = LeanSupportPool()
    pool.print_summary()
    
    # Export for system integration
    export = pool.export_structure()
    with open("/root/.aos/aos/lean_support_pool.json", "w") as f:
        f.write(export)
    
    print("\n💾 Structure saved to: /root/.aos/aos/lean_support_pool.json")


if __name__ == "__main__":
    main()
