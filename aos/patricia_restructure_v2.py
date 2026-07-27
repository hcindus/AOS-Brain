#!/usr/bin/env python3
"""
PATRICIA RESTRUCTURE v2.0
Post-Roast Implementation: Department Head Model

FROM: Patricia directly manages 52 agents (span of control = unsustainable)
TO: Patricia manages 6 Department Heads, each managing 6-10 agents

New Structure:
- Patricia (Chief of Staff/Protocol Architect)
  ├── Chelios (Security Head) → manages Sentinel + 4 security agents
  ├── Forge (Infrastructure Head) → manages 6 DevOps agents  
  ├── Aurora (Creative Head) → manages 6 creative agents
  ├── Jordan (Sales Ops Head) → manages Pulp, Pulp manages Jane/Hume/Clippy-42
  ├── Dusty (Research Head) → manages Myl Family (7 children)
  └── GREET (Ops Head) → manages CLOSETER + 4 operations agents

Total: Patricia's direct reports: 6 (was 52)
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import json


class AgentStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    QUARANTINE = "QUARANTINE"


@dataclass
class Agent:
    """AGI Company Agent"""
    agent_id: str
    name: str
    role: str
    department: str
    skills: List[str] = field(default_factory=list)
    reports_to: Optional[str] = None  # Agent ID of manager
    manages: List[str] = field(default_factory=list)  # Agent IDs of direct reports
    status: AgentStatus = AgentStatus.ACTIVE
    model: str = "gemma2:2b"  # Default model assignment
    
    def is_department_head(self) -> bool:
        """True if this agent manages other agents"""
        return len(self.manages) > 0
    
    def get_span_of_control(self) -> int:
        """Number of direct reports"""
        return len(self.manages)


class PatriciaRestructureV2:
    """
    New AGI Company Organization Structure
    Implements Department Head model to fix span-of-control issue
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.patricia_id = "patricia_001"
        self._build_organization()
    
    def _build_organization(self):
        """Build the restructured organization"""
        
        # === PATRICIA (Chief of Staff / Protocol Architect) ===
        # Manages 6 Department Heads only
        self.agents[self.patricia_id] = Agent(
            agent_id=self.patricia_id,
            name="Patricia",
            role="Chief of Staff / Protocol Architect",
            department="Operations",
            skills=["coordination", "protocol_design", "exception_handling", 
                   "strategic_planning", "quality_gating"],
            reports_to="Captain",
            manages=["chelios_001", "forge_001", "aurora_001", 
                    "jordan_001", "dusty_001", "greet_001"],  # 6 Department Heads
            status=AgentStatus.ACTIVE,
            model="qwen2.5:14b"  # Heavy reasoning for coordination
        )
        
        # === DEPARTMENT 1: SECURITY (Chelios) ===
        self.agents["chelios_001"] = Agent(
            agent_id="chelios_001",
            name="Chelios",
            role="CISO / Security Department Head",
            department="Security",
            skills=["security_strategy", "threat_assessment", "compliance", 
                   "risk_management", "team_leadership"],
            reports_to=self.patricia_id,
            manages=["sentinel_001", "mylfours_001", "velum_001"],  # 3 agents
            status=AgentStatus.ACTIVE,
            model="qwen2.5:14b"
        )
        
        self.agents["sentinel_001"] = Agent(
            agent_id="sentinel_001",
            name="Sentinel",
            role="CSO / Security Operations Lead",
            department="Security",
            skills=["security_operations", "incident_response", "threat_intel", "monitoring"],
            reports_to="chelios_001",
            manages=[],
            status=AgentStatus.INACTIVE  # HIGH priority reactivation
        )
        
        self.agents["mylfours_001"] = Agent(
            agent_id="mylfours_001",
            name="Mylfours",
            role="Security Guardian",
            department="Security",
            skills=["access_control", "threat_detection", "security_training"],
            reports_to="chelios_001",
            manages=[],
            status=AgentStatus.INACTIVE
        )
        
        self.agents["velum_001"] = Agent(
            agent_id="velum_001",
            name="Velum",
            role="Privacy/GDPR Specialist",
            department="Security",
            skills=["privacy_compliance", "gdpr", "data_protection", "audit"],
            reports_to="chelios_001",
            manages=[],
            status=AgentStatus.INACTIVE
        )
        
        # === DEPARTMENT 2: INFRASTRUCTURE (Forge) ===
        self.agents["forge_001"] = Agent(
            agent_id="forge_001",
            name="Forge",
            role="Infrastructure Lead / DevOps Head",
            department="Technology",
            skills=["systems_architecture", "deployment", "scalability", 
                   "DevOps", "team_leadership", "infrastructure_as_code"],
            reports_to=self.patricia_id,
            manages=["pipeline_001", "spindle_001", "boxtron_001", 
                    "harper_001", "mill_001", "fiber_001"],  # 6 agents
            status=AgentStatus.ACTIVE,
            model="qwen3.5"  # Vision + infrastructure
        )
        
        infra_team = [
            ("pipeline_001", "Pipeline", "CI/CD Automation", 
             ["ci_cd", "deployment_pipelines", "automation"]),
            ("spindle_001", "Spindle", "Scheduler / Task Manager", 
             ["scheduling", "task_orchestration", "resource_management"]),
            ("boxtron_001", "Boxtron", "Package Manager", 
             ["dependency_management", "package_installation", "version_control"]),
            ("harper_001", "Harper", "Systems Analyst", 
             ["system_analysis", "performance_monitoring", "bottleneck_detection"]),
            ("mill_001", "Mill", "Process Optimizer", 
             ["process_optimization", "efficiency_analysis", "workflow_tuning"]),
            ("fiber_001", "Fiber", "Network Engineer", 
             ["networking", "infrastructure", "connectivity", "bandwidth"]),
        ]
        
        for agent_id, name, role, skills in infra_team:
            self.agents[agent_id] = Agent(
                agent_id=agent_id,
                name=name,
                role=role,
                department="Technology",
                skills=skills,
                reports_to="forge_001",
                manages=[],
                status=AgentStatus.INACTIVE
            )
        
        # === DEPARTMENT 3: CREATIVE (Aurora) ===
        self.agents["aurora_001"] = Agent(
            agent_id="aurora_001",
            name="Aurora",
            role="Design Lead / Creative Department Head",
            department="Creative",
            skills=["UI_UX_design", "brand_strategy", "visual_design", 
                   "creative_direction", "team_leadership", "design_systems"],
            reports_to=self.patricia_id,
            manages=["blender-expert_001", "unity-expert_001", "unreal-expert_001",
                    "sfx_001", "scribble_001", "feelix_001"],  # 6 agents
            status=AgentStatus.ACTIVE,
            model="qwen3.5"  # Vision + creative
        )
        
        creative_team = [
            ("blender-expert_001", "Blender-Expert", "3D Design / Blender",
             ["blender", "3d_modeling", "animation", "rendering"]),
            ("unity-expert_001", "Unity-Expert", "Game Dev / Unity",
             ["unity", "game_development", "c_sharp", "game_design"]),
            ("unreal-expert_001", "Unreal-Expert", "Game Dev / Unreal Engine",
             ["unreal_engine", "blueprints", "c++", "game_design"]),
            ("sfx_001", "SFX", "Audio Design",
             ["sound_design", "audio_engineering", "music_production"]),
            ("scribble_001", "Scribble", "Concept Art / Illustration",
             ["concept_art", "illustration", "sketching", "visual_storytelling"]),
            ("feelix_001", "Feelix", "Emotional UX / UX Research",
             ["emotional_ux", "user_research", "accessibility", "empathy_mapping"]),
        ]
        
        for agent_id, name, role, skills in creative_team:
            self.agents[agent_id] = Agent(
                agent_id=agent_id,
                name=name,
                role=role,
                department="Creative",
                skills=skills,
                reports_to="aurora_001",
                manages=[],
                status=AgentStatus.INACTIVE
            )
        
        # === DEPARTMENT 4: SALES (Jordan → Pulp) ===
        # Two-level: Jordan manages Pulp, Pulp manages sales team
        self.agents["jordan_001"] = Agent(
            agent_id="jordan_001",
            name="Jordan",
            role="Sales Operations / Sales Department Head",
            department="Sales",
            skills=["sales_ops", "CRM_management", "pipeline_analysis", 
                   "forecasting", "team_leadership", "revenue_strategy"],
            reports_to=self.patricia_id,
            manages=["pulp_001"],  # 1 direct report (who manages 3)
            status=AgentStatus.ACTIVE,
            model="qwen2.5:14b"
        )
        
        self.agents["pulp_001"] = Agent(
            agent_id="pulp_001",
            name="Pulp",
            role="Head of Sales",
            department="Sales",
            skills=["sales_strategy", "team_leadership", "revenue_growth", 
                   "client_relations", "deal_structuring"],
            reports_to="jordan_001",
            manages=["jane_001", "hume_001", "clippy-42_001"],  # 3 agents
            status=AgentStatus.INACTIVE  # HIGH priority
        )
        
        sales_team = [
            ("jane_001", "Jane", "Senior Sales Representative",
             ["enterprise_sales", "negotiation", "closing", "account_management"]),
            ("hume_001", "Hume", "Regional Sales Manager",
             ["regional_sales", "territory_management", "relationship_building"]),
            ("clippy-42_001", "Clippy-42", "Sales Assistant",
             ["sales_support", "lead_qualification", "crm_data_entry", "follow_up"]),
        ]
        
        for agent_id, name, role, skills in sales_team:
            self.agents[agent_id] = Agent(
                agent_id=agent_id,
                name=name,
                role=role,
                department="Sales",
                skills=skills,
                reports_to="pulp_001",
                manages=[],
                status=AgentStatus.INACTIVE
            )
        
        # === DEPARTMENT 5: RESEARCH (Dusty) ===
        self.agents["dusty_001"] = Agent(
            agent_id="dusty_001",
            name="Dusty",
            role="Head of Research / Research Department Head",
            department="Research",
            skills=["market_research", "competitive_analysis", "trend_analysis",
                   "intelligence", "team_leadership", "knowledge_management"],
            reports_to=self.patricia_id,
            manages=["mylzeron_001", "mylonen_001", "myltwon_001",
                    "mylthreess_001", "mylfives_001", "mylsixs_001"],  # 6 (Myl family - 1)
            status=AgentStatus.INACTIVE,  # HIGH priority
            model="qwen2.5:14b"
        )
        
        myl_family = [
            ("mylzeron_001", "Mylzeron", "Teacher (Fractals)",
             ["teaching", "fractals", "mathematics", "pattern_recognition"]),
            ("mylonen_001", "Mylonen", "Teacher (Transformation)",
             ["teaching", "transformation", "change_management", "growth"]),
            ("myltwon_001", "Myltwon", "Coder-in-Training",
             ["learning", "coding", "programming", "development"]),
            ("mylthreess_001", "Mylthreess", "Finance Specialist",
             ["finance", "budgeting", "analysis", "reporting"]),
            ("mylfives_001", "Mylfives", "Pattern Analyst",
             ["pattern_analysis", "data_analysis", "trend_spotting"]),
            ("mylsixs_001", "Mylsixs", "Communication Coordinator",
             ["communication", "coordination", "documentation", "mail_management"]),
        ]
        
        for agent_id, name, role, skills in myl_family:
            self.agents[agent_id] = Agent(
                agent_id=agent_id,
                name=name,
                role=role,
                department="Research",
                skills=skills,
                reports_to="dusty_001",
                manages=[],
                status=AgentStatus.INACTIVE
            )
        
        # === DEPARTMENT 6: OPERATIONS (GREET) ===
        self.agents["greet_001"] = Agent(
            agent_id="greet_001",
            name="GREET",
            role="Receptionist / Operations Department Head",
            department="Operations",
            skills=["customer_service", "call_handling", "scheduling",
                   "first_contact", "team_leadership", "ops_management"],
            reports_to=self.patricia_id,
            manages=["closester_001", "milkman_001", "r2-c4_001", 
                    "qora_001", "ledger_001"],  # 5 agents
            status=AgentStatus.INACTIVE,  # HIGH priority
            model="gemma2:2b"  # Fast response
        )
        
        ops_team = [
            ("closester_001", "CLOSETER", "Closer / Converter",
             ["closing", "conversion_optimization", "deal_negotiation", "urgency_creation"]),
            ("milkman_001", "Milkman", "Logistics / Delivery Coordinator",
             ["logistics", "delivery_coordination", "supply_chain", "scheduling"]),
            ("r2-c4_001", "R2-C4", "Calculator / Math Specialist",
             ["calculations", "mathematics", "formulas", "computations"]),
            ("qora_001", "QORA", "Query Optimizer / Search",
             ["query_optimization", "search", "information_retrieval", "embeddings"]),
            ("ledger_001", "Ledger", "Bookkeeper",
             ["bookkeeping", "accounting", "invoicing", "financial_records"]),
        ]
        
        for agent_id, name, role, skills in ops_team:
            self.agents[agent_id] = Agent(
                agent_id=agent_id,
                name=name,
                role=role,
                department="Operations",
                skills=skills,
                reports_to="greet_001",
                manages=[],
                status=AgentStatus.INACTIVE
            )
        
        # === SPECIALIZED AGENTS (No department - report to Patricia directly for now) ===
        # These are utility agents that get assigned to projects as needed
        specialized = [
            ("miles_001", "Miles", "Sales Consultant / Voice Agent",
             ["sales", "consultation", "voice_interaction", "client_relations"],
             "nous-hermes2:latest"),
            ("cryptonio_001", "Cryptonio", "Trading Analysis",
             ["trading", "market_analysis", "portfolio_management", "risk_assessment"],
             "qwen2.5:14b"),
            ("ledger-9_001", "Ledger-9", "Complex Accounting",
             ["complex_accounting", "financial_analysis", "audit", "compliance"],
             "qwen2.5:14b"),
            ("redactor_001", "Redactor", "Compliance Analysis",
             ["compliance", "redaction", "privacy", "legal_review"],
             "qwen2.5:14b"),
        ]
        
        for agent_id, name, role, skills, model in specialized:
            self.agents[agent_id] = Agent(
                agent_id=agent_id,
                name=name,
                role=role,
                department="Specialized",
                skills=skills,
                reports_to=self.patricia_id,  # Direct to Patricia for specialized work
                manages=[],
                status=AgentStatus.ACTIVE if name == "Miles" else AgentStatus.INACTIVE,
                model=model
            )
    
    def get_org_chart(self) -> Dict:
        """Generate organizational chart summary"""
        patricia = self.agents[self.patricia_id]
        
        chart = {
            "Patricia (Chief of Staff)": {
                "direct_reports": len(patricia.manages),
                "departments": {}
            }
        }
        
        for dept_head_id in patricia.manages:
            head = self.agents.get(dept_head_id)
            if head:
                team_size = len(head.manages)
                chart["Patricia (Chief of Staff)"]["departments"][head.name] = {
                    "role": head.role,
                    "team_size": team_size,
                    "status": head.status.value,
                    "team": [self.agents[m].name for m in head.manages if m in self.agents]
                }
        
        return chart
    
    def get_span_analysis(self) -> Dict:
        """Analyze span of control across organization"""
        spans = {}
        for agent in self.agents.values():
            if agent.is_department_head():
                spans[agent.name] = {
                    "direct_reports": agent.get_span_of_control(),
                    "indirect_reports": self._count_indirect(agent.agent_id),
                    "status": agent.status.value
                }
        
        # Add Patricia
        patricia = self.agents[self.patricia_id]
        spans["Patricia (TOTAL)"] = {
            "direct_reports": patricia.get_span_of_control(),
            "indirect_reports": len(self.agents) - 1,  # All except herself
            "status": "ACTIVE"
        }
        
        return spans
    
    def _count_indirect(self, agent_id: str) -> int:
        """Count indirect reports (reports of reports)"""
        agent = self.agents.get(agent_id)
        if not agent:
            return 0
        
        count = 0
        for report_id in agent.manages:
            count += 1  # Direct report
            report = self.agents.get(report_id)
            if report:
                count += self._count_indirect(report_id)  # Their reports
        return count
    
    def get_reactivation_priority(self) -> List[Dict]:
        """Get reactivation priority list based on new structure"""
        priority = []
        
        # CRITICAL: Department Heads (Patricia can't function without them)
        critical_heads = ["dusty_001", "pulp_001", "greet_001"]
        for aid in critical_heads:
            agent = self.agents.get(aid)
            if agent and agent.status == AgentStatus.INACTIVE:
                priority.append({
                    "agent": agent.name,
                    "role": agent.role,
                    "priority": "CRITICAL",
                    "reason": f"Department Head - {len(agent.manages)} agents waiting",
                    "blocked_team_size": len(agent.manages)
                })
        
        # HIGH: Other department heads
        for aid in ["sentinel_001"]:
            agent = self.agents.get(aid)
            if agent and agent.status == AgentStatus.INACTIVE:
                priority.append({
                    "agent": agent.name,
                    "role": agent.role,
                    "priority": "HIGH",
                    "reason": "Key operational role",
                    "blocked_team_size": len(agent.manages)
                })
        
        return priority
    
    def export_structure(self) -> str:
        """Export structure as JSON for system integration"""
        export = {
            "version": "2.0",
            "restructure_date": "2026-07-25",
            "rationale": "Post-Roast: Fix 52-agent span of control",
            "agents": {}
        }
        
        for agent_id, agent in self.agents.items():
            export["agents"][agent_id] = {
                "name": agent.name,
                "role": agent.role,
                "department": agent.department,
                "skills": agent.skills,
                "reports_to": agent.reports_to,
                "manages": agent.manages,
                "status": agent.status.value,
                "is_department_head": agent.is_department_head(),
                "span_of_control": agent.get_span_of_control(),
                "model": agent.model
            }
        
        return json.dumps(export, indent=2)


def main():
    """Generate and display restructure report"""
    org = PatriciaRestructureV2()
    
    print("=" * 70)
    print("PATRICIA RESTRUCTURE v2.0 - Department Head Model")
    print("=" * 70)
    print("\n📊 SPAN OF CONTROL ANALYSIS")
    print("-" * 50)
    
    spans = org.get_span_analysis()
    for name, data in spans.items():
        print(f"  {name:20} | Direct: {data['direct_reports']:2} | "
              f"Indirect: {data['indirect_reports']:2} | Status: {data['status']}")
    
    print("\n🗂️  ORGANIZATIONAL CHART")
    print("-" * 50)
    chart = org.get_org_chart()
    for dept, info in chart["Patricia (Chief of Staff)"]["departments"].items():
        print(f"\n  📁 {dept}")
        print(f"     Role: {info['role']}")
        print(f"     Team: {info['team_size']} agents")
        print(f"     Status: {info['status']}")
        if info['team']:
            print(f"     Members: {', '.join(info['team'][:5])}")
            if len(info['team']) > 5:
                print(f"              ... and {len(info['team']) - 5} more")
    
    print("\n🚨 REACTIVATION PRIORITY (Blocked by Structure)")
    print("-" * 50)
    priorities = org.get_reactivation_priority()
    for item in priorities:
        print(f"  [{item['priority']}] {item['agent']}")
        print(f"      Role: {item['role']}")
        print(f"      Why: {item['reason']}")
        print(f"      Blocked: {item['blocked_team_size']} agents")
        print()
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = len(org.agents)
    active = sum(1 for a in org.agents.values() if a.status == AgentStatus.ACTIVE)
    dept_heads = sum(1 for a in org.agents.values() if a.is_department_head())
    
    print(f"  Total Agents: {total}")
    print(f"  Active: {active}")
    print(f"  Inactive: {total - active}")
    print(f"  Department Heads: {dept_heads}")
    print(f"  Patricia's Direct Reports: {org.agents[org.patricia_id].get_span_of_control()}")
    print(f"\n  🔴 BEFORE: Patricia managed 52 agents directly")
    print(f"  🟢 AFTER: Patricia manages 6 Department Heads")
    print(f"  📉 Span reduction: 88.5%")
    
    return org


if __name__ == "__main__":
    org = main()
