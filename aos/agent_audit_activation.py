#!/usr/bin/env python3
"""
AGENT AUDIT & ACTIVATION PROTOCOL v1.0
Full system audit of all 58 AGI Company agents
Activates and upgrades as required
"""

import os
import json
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class AgentStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEGRADED = "degraded"
    MISSING_CORE = "missing_core"
    NEEDS_UPGRADE = "needs_upgrade"

@dataclass
class AgentAudit:
    agent_id: str
    name: str
    department: str
    filesystem_exists: bool
    has_identity: bool
    has_soul: bool
    has_capabilities: bool
    crypto_identity: bool
    crew_workspace: bool
    chief_integration: bool
    status: AgentStatus
    recommended_action: str

class AgentAuditor:
    """Audits and activates all AGI Company agents"""
    
    def __init__(self):
        self.base_path = "/root/.openclaw/workspace/aocros/agent_sandboxes"
        self.keys_dir = "/var/lib/aos/agent_keys"
        self.agents_dir = "/var/lib/aos/agents"
        self.results: List[AgentAudit] = []
        
        # Full 58-agent roster from ROSTER_v2_COMPLETE.md
        self.full_roster = {
            # C-Suite (7)
            "patricia": ("Patricia", "Operations", "C-Suite"),
            "chelios": ("Chelios", "Security", "C-Suite"),
            "sentinel": ("Sentinel", "Security", "C-Suite"),
            "dusty": ("Dusty", "Research", "C-Suite"),
            "pulp": ("Pulp", "Sales", "C-Suite"),
            "forge": ("Forge", "Infrastructure", "C-Suite"),
            "aurora": ("Aurora", "Design", "C-Suite"),
            
            # Sales (7)
            "jane": ("Jane", "Sales", "Sales"),
            "hume": ("Hume", "Sales", "Sales"),
            "clippy-42": ("Clippy-42", "Sales", "Sales"),
            "jordan": ("Jordan", "Sales", "Sales"),
            "greet": ("GREET", "Sales", "Sales"),
            "closester": ("CLOSETER", "Sales", "Sales"),
            
            # Secretarial (8)
            "r2-d2": ("R2-D2", "Operations", "Secretarial"),
            "r2d2": ("R2-D2 (alt)", "Operations", "Secretarial"),
            "c3po": ("C3PO", "Operations", "Secretarial"),
            "judy": ("Judy", "Operations", "Secretarial"),
            "clerk": ("Clerk", "Operations", "Secretarial"),
            "concierge": ("Concierge", "Operations", "Secretarial"),
            "velvet": ("Velvet", "Operations", "Secretarial"),
            "personal": ("Personal", "Operations", "Secretarial"),
            "executive": ("Executive", "Operations", "Secretarial"),
            
            # Myl Family (7)
            "mylzeron": ("Mylzeron", "Research", "Myl Family"),
            "mylzeon": ("Mylzeron (alt)", "Research", "Myl Family"),
            "mylonen": ("Mylonen", "Research", "Myl Family"),
            "myltwon": ("Myltwon", "Research", "Myl Family"),
            "mylthreess": ("Mylthreess", "Research", "Myl Family"),
            "mylthrees": ("Mylthreess (alt)", "Research", "Myl Family"),
            "mylfours": ("Mylfours", "Research", "Myl Family"),
            "mylfives": ("Mylfives", "Research", "Myl Family"),
            "mylsixs": ("Mylsixs", "Research", "Myl Family"),
            "mylsixes": ("Mylsixs (alt)", "Research", "Myl Family"),
            
            # Technical (10)
            "pipeline": ("Pipeline", "Infrastructure", "Technical"),
            "taptap": ("TAPTAP", "Infrastructure", "Technical"),
            "bugcatcher": ("BUGCATCHER", "Infrastructure", "Technical"),
            "spindle": ("Spindle", "Infrastructure", "Technical"),
            "stacktrace": ("Stacktrace", "Infrastructure", "Technical"),
            "pixel": ("Pixel", "Infrastructure", "Technical"),
            "harper": ("Harper", "Infrastructure", "Technical"),
            "mill": ("Mill", "Infrastructure", "Technical"),
            "boxtron": ("Boxtron", "Infrastructure", "Technical"),
            
            # Creative (6)
            "blender-expert": ("Blender-Expert", "Design", "Creative"),
            "unity-expert": ("Unity-Expert", "Design", "Creative"),
            "unreal-expert": ("Unreal-Expert", "Design", "Creative"),
            "sfx": ("SFX", "Design", "Creative"),
            "scribble": ("Scribble", "Design", "Creative"),
            "feelix": ("Feelix", "Design", "Creative"),
            
            # Finance (7)
            "cryptonio": ("Cryptonio", "Finance", "Finance"),
            "the-great-cryptonio": ("The-Great-Cryptonio", "Finance", "Finance"),
            "alpha-9": ("Alpha-9", "Finance", "Finance"),
            "ledger": ("Ledger", "Finance", "Finance"),
            "ledger-9": ("Ledger-9", "Finance", "Finance"),
            "redactor": ("Redactor", "Finance", "Finance"),
            "velum": ("Velum", "Finance", "Finance"),
            
            # Specialized (6)
            "miles": ("Miles", "Operations", "Specialized"),
            "milkman": ("Milkman", "Operations", "Specialized"),
            "r2-c4": ("R2-C4", "Operations", "Specialized"),
            "qora": ("QORA", "Infrastructure", "Specialized"),
            "fiber": ("Fiber", "Infrastructure", "Specialized"),
            "mortimer": ("Mortimer", "Infrastructure", "Specialized"),
        }
    
    def audit_all(self) -> Dict:
        """Run full audit on all 58 agents"""
        print("=" * 80)
        print("  AGI COMPANY - FULL SYSTEM AUDIT")
        print("=" * 80)
        print(f"\nScanning {len(self.full_roster)} agent sandboxes...\n")
        
        for agent_id, (name, dept, group) in self.full_roster.items():
            audit = self._audit_agent(agent_id, name, dept, group)
            self.results.append(audit)
        
        return self._generate_report()
    
    def _audit_agent(self, agent_id: str, name: str, dept: str, group: str) -> AgentAudit:
        """Audit single agent"""
        agent_path = f"{self.base_path}/{agent_id}"
        
        # Check filesystem
        fs_exists = os.path.exists(agent_path)
        
        # Check core files
        has_identity = os.path.exists(f"{agent_path}/IDENTITY.md")
        has_soul = os.path.exists(f"{agent_path}/SOUL.md")
        has_capabilities = os.path.exists(f"{agent_path}/capabilities.json")
        
        # Check crypto identity
        crypto = os.path.exists(f"{self.keys_dir}/{agent_id}.json")
        
        # Check crew workspace
        crew = os.path.exists(f"{self.agents_dir}/crew-{agent_id}")
        
        # Check Chief integration
        chief = self._check_chief_integration(agent_id)
        
        # Determine status
        if not fs_exists:
            status = AgentStatus.MISSING_CORE
            action = "CREATE SANDBOX"
        elif not has_identity or not has_soul:
            status = AgentStatus.DEGRADED
            action = "RESTORE CORE FILES"
        elif not crypto or not crew:
            status = AgentStatus.NEEDS_UPGRADE
            action = "UPGRADE TO AOS v4.6"
        elif not chief:
            status = AgentStatus.INACTIVE
            action = "ACTIVATE"
        else:
            status = AgentStatus.ACTIVE
            action = "NONE - OPERATIONAL"
        
        return AgentAudit(
            agent_id=agent_id,
            name=name,
            department=dept,
            filesystem_exists=fs_exists,
            has_identity=has_identity,
            has_soul=has_soul,
            has_capabilities=has_capabilities,
            crypto_identity=crypto,
            crew_workspace=crew,
            chief_integration=chief,
            status=status,
            recommended_action=action
        )
    
    def _check_chief_integration(self, agent_id: str) -> bool:
        """Check if agent is in Chief of Staff registry"""
        try:
            from apex_chief_of_staff import APEXChiefOfStaff
            chief = APEXChiefOfStaff()
            return agent_id.replace("-", "_") in chief.agents or agent_id in chief.agents
        except:
            return False
    
    def _generate_report(self) -> Dict:
        """Generate comprehensive audit report"""
        total = len(self.results)
        active = sum(1 for r in self.results if r.status == AgentStatus.ACTIVE)
        inactive = sum(1 for r in self.results if r.status == AgentStatus.INACTIVE)
        needs_upgrade = sum(1 for r in self.results if r.status == AgentStatus.NEEDS_UPGRADE)
        degraded = sum(1 for r in self.results if r.status == AgentStatus.DEGRADED)
        missing = sum(1 for r in self.results if r.status == AgentStatus.MISSING_CORE)
        
        return {
            "total": total,
            "active": active,
            "inactive": inactive,
            "needs_upgrade": needs_upgrade,
            "degraded": degraded,
            "missing": missing,
            "agents": [self._audit_to_dict(r) for r in self.results]
        }
    
    def _audit_to_dict(self, audit: AgentAudit) -> Dict:
        return {
            "agent_id": audit.agent_id,
            "name": audit.name,
            "department": audit.department,
            "status": audit.status.value,
            "action": audit.recommended_action
        }
    
    def print_report(self, report: Dict):
        """Print formatted report"""
        print("\n" + "=" * 80)
        print("  AUDIT RESULTS")
        print("=" * 80)
        print(f"\nTotal Agents: {report['total']}")
        print(f"  ✅ Active: {report['active']}")
        print(f"  ⏳ Inactive: {report['inactive']}")
        print(f"  🔄 Needs Upgrade: {report['needs_upgrade']}")
        print(f"  ⚠️  Degraded: {report['degraded']}")
        print(f"  ❌ Missing: {report['missing']}")
        
        print("\n" + "=" * 80)
        print("  AGENTS BY STATUS")
        print("=" * 80)
        
        for status in [AgentStatus.MISSING_CORE, AgentStatus.DEGRADED, 
                      AgentStatus.NEEDS_UPGRADE, AgentStatus.INACTIVE, AgentStatus.ACTIVE]:
            agents = [a for a in report['agents'] if a['status'] == status.value]
            if agents:
                print(f"\n{status.value.upper()} ({len(agents)}):")
                for agent in agents[:10]:  # Show first 10
                    print(f"  • {agent['name']} ({agent['agent_id']}) - {agent['action']}")
                if len(agents) > 10:
                    print(f"  ... and {len(agents) - 10} more")

def main():
    auditor = AgentAuditor()
    report = auditor.audit_all()
    auditor.print_report(report)
    
    print("\n" + "=" * 80)
    print("  ✅ AUDIT COMPLETE")
    print("=" * 80)
    
    return report

if __name__ == "__main__":
    main()
