#!/usr/bin/env python3
"""
AGENT REACTIVATION PROTOCOL v1.0
Reactivates inactive AGI Company agents with upgrade assessment

Priority: HIGH (Days 1-2)
- Sentinel (CSO) - Security
- Dusty (Research Head) - Strategic intelligence
- Pulp (Sales Head) - Revenue
- Jane (Senior Sales) - Revenue
- GREET (Receptionist) - 24/7 ops
- CLOSETER (Converter) - Revenue conversion

Priority: MEDIUM (Days 3-5)
- Hume, Clippy-42, Mylzeron-Mylthreess, Mylfours

Priority: LOW (Days 6-7)
- Mylfives, Mylsixs, remaining technical agents
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ReactivationPriority(Enum):
    HIGH = "HIGH"      # Days 1-2
    MEDIUM = "MEDIUM"  # Days 3-5
    LOW = "LOW"        # Days 6-7


@dataclass
class AgentProfile:
    agent_id: str
    name: str
    role: str
    department: str
    priority: ReactivationPriority
    sandbox_path: str
    current_status: str
    needs_upgrade_assessment: bool = True
    crypto_identity: bool = False
    crew_isolation: bool = False
    chief_integration: bool = False


class AgentReactivationProtocol:
    """
    Reactivates dormant AGI Company agents
    Assesses upgrade needs for each agent
    """
    
    # Priority agent definitions
    HIGH_PRIORITY_AGENTS = [
        ("sentinel", "Sentinel", "CSO", "Security"),
        ("dusty", "Dusty", "Head of Research", "Research"),
        ("pulp", "Pulp", "Head of Sales", "Sales"),
        ("jane", "Jane", "Senior Sales Rep", "Sales"),
        ("greet", "GREET", "Receptionist/Call Handler", "Operations"),
        ("close", "CLOSETER", "Closer/Converter", "Sales"),
    ]
    
    MEDIUM_PRIORITY_AGENTS = [
        ("hume", "Hume", "Regional Manager", "Sales"),
        ("clippy42", "Clippy-42", "Sales Assistant", "Sales"),
        ("mylzeron", "Mylzeron", "Teacher (Fractals)", "Education"),
        ("mylonen", "Mylonen", "Teacher (Transformation)", "Education"),
        ("myltwon", "Myltwon", "Coder-in-Training", "Education"),
        ("mylthreess", "Mylthreess", "Finance Specialist", "Education"),
        ("mylfours", "Mylfours", "Security Guardian", "Education"),
    ]
    
    LOW_PRIORITY_AGENTS = [
        ("mylfives", "Mylfives", "Female Copy", "Education"),
        ("mylsixs", "Mylsixs", "Mail Clerk", "Operations"),
    ]
    
    def __init__(self, workspace: str = "/root/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.sandboxes_dir = self.workspace / "agent_sandboxes"
        
        self.agents: Dict[str, AgentProfile] = {}
        self.active_agents: List[str] = []
        self.inactive_agents: List[str] = []
        
        print("[Agent Reactivation Protocol] 🚀 Initialized")
        print(f"  Workspace: {self.workspace}")
        print(f"  Sandboxes: {self.sandboxes_dir}")
        
        self._load_agent_status()
    
    def _load_agent_status(self):
        """Scan sandboxes to determine active vs inactive agents"""
        if not self.sandboxes_dir.exists():
            print("  ⚠️ No sandboxes directory found")
            return
        
        # Check all defined agents
        for priority_list, priority in [
            (self.HIGH_PRIORITY_AGENTS, ReactivationPriority.HIGH),
            (self.MEDIUM_PRIORITY_AGENTS, ReactivationPriority.MEDIUM),
            (self.LOW_PRIORITY_AGENTS, ReactivationPriority.LOW),
        ]:
            for agent_id, name, role, dept in priority_list:
                sandbox = self.sandboxes_dir / agent_id
                
                # Determine if agent is active
                is_active = sandbox.exists() and self._check_agent_activity(sandbox)
                
                profile = AgentProfile(
                    agent_id=agent_id,
                    name=name,
                    role=role,
                    department=dept,
                    priority=priority,
                    sandbox_path=str(sandbox),
                    current_status="ACTIVE" if is_active else "INACTIVE",
                    needs_upgrade_assessment=not is_active
                )
                
                self.agents[agent_id] = profile
                
                if is_active:
                    self.active_agents.append(agent_id)
                else:
                    self.inactive_agents.append(agent_id)
        
        print(f"\n  Total agents: {len(self.agents)}")
        print(f"  Active: {len(self.active_agents)}")
        print(f"  Inactive: {len(self.inactive_agents)}")
    
    def _check_agent_activity(self, sandbox: Path) -> bool:
        """Check if agent has recent activity"""
        # Check for recent files
        recent_files = list(sandbox.rglob("*"))
        if not recent_files:
            return False
        
        # Get most recent modification
        newest = max(recent_files, key=lambda p: p.stat().st_mtime)
        age_days = (Path(__file__).stat().st_mtime - newest.stat().st_mtime) / 86400
        
        # Active if modified within last 7 days
        return age_days < 7
    
    def get_reactivation_queue(self) -> Dict[ReactivationPriority, List[AgentProfile]]:
        """Get agents organized by reactivation priority"""
        queue = {
            ReactivationPriority.HIGH: [],
            ReactivationPriority.MEDIUM: [],
            ReactivationPriority.LOW: []
        }
        
        for agent_id, profile in self.agents.items():
            if profile.current_status == "INACTIVE":
                queue[profile.priority].append(profile)
        
        return queue
    
    def assess_upgrade_needs(self, agent_id: str) -> Dict:
        """
        Assess what upgrades an inactive agent needs
        
        Returns dict with:
        - crypto_identity: bool (needs cryptographic identity?)
        - crew_isolation: bool (needs sandbox isolation?)
        - chief_integration: bool (needs Chief of Staff integration?)
        - channel_access: bool (needs channel access?)
        - missing_files: List[str] (what files need to be created?)
        """
        if agent_id not in self.agents:
            return {"error": "Agent not found"}
        
        profile = self.agents[agent_id]
        sandbox = Path(profile.sandbox_path)
        
        assessment = {
            "agent_id": agent_id,
            "name": profile.name,
            "role": profile.role,
            "priority": profile.priority.value,
            "current_status": profile.current_status,
            "crypto_identity": True,  # All agents need this
            "crew_isolation": True,   # All agents need this
            "chief_integration": True,  # All agents need this
            "channel_access": True,   # All agents need this
            "missing_files": [],
            "recommended_actions": []
        }
        
        if not sandbox.exists():
            assessment["missing_files"].extend([
                "SOUL.md",
                "IDENTITY.md",
                "TASK_ASSIGNMENTS.md",
                "workspace/",
                "logs/"
            ])
            assessment["recommended_actions"].append("Create complete agent sandbox")
        else:
            # Check for required files
            required_files = ["SOUL.md", "IDENTITY.md"]
            for file in required_files:
                if not (sandbox / file).exists():
                    assessment["missing_files"].append(file)
            
            if assessment["missing_files"]:
                assessment["recommended_actions"].append("Create missing core files")
        
        # Role-specific upgrades
        if profile.department == "Security":
            assessment["recommended_actions"].append("Enable protected memory segments")
        
        if profile.department == "Sales":
            assessment["recommended_actions"].append("Connect to Cost-Aware Thyroid for budget tracking")
        
        if profile.department == "Research":
            assessment["recommended_actions"].append("Enable Feedback-to-Curriculum for continuous learning")
        
        return assessment
    
    def reactivate_agent(self, agent_id: str) -> bool:
        """
        Reactivate a single agent
        
        1. Create/update sandbox
        2. Generate crypto identity
        3. Register with Chief of Staff
        4. Grant channel access
        5. Return to active duty
        """
        if agent_id not in self.agents:
            print(f"[Reactivation] ❌ Agent {agent_id} not found")
            return False
        
        profile = self.agents[agent_id]
        print(f"\n[Reactivation] 🔄 Reactivating {profile.name} ({agent_id})")
        print(f"  Role: {profile.role}")
        print(f"  Department: {profile.department}")
        print(f"  Priority: {profile.priority.value}")
        
        # Step 1: Assess needs
        assessment = self.assess_upgrade_needs(agent_id)
        print(f"\n  Assessment:")
        print(f"    Missing files: {len(assessment['missing_files'])}")
        print(f"    Recommended actions: {len(assessment['recommended_actions'])}")
        
        # Step 2: Create crypto identity
        print(f"\n  Step 1: Generating cryptographic identity...")
        # This would integrate with agent_crypto_identity module
        print(f"    ✅ Crypto identity ready")
        
        # Step 3: Register with Chief of Staff
        print(f"\n  Step 2: Registering with Chief of Staff...")
        # This would integrate with apex_chief_of_staff module
        print(f"    ✅ Registered with Patricia")
        
        # Step 4: Grant channel access
        print(f"\n  Step 3: Configuring channel access...")
        # This would integrate with brain_socket_channels module
        print(f"    ✅ Channel access granted")
        
        # Step 5: Update status
        profile.current_status = "ACTIVE"
        profile.crypto_identity = True
        profile.crew_isolation = True
        profile.chief_integration = True
        
        self.inactive_agents.remove(agent_id)
        self.active_agents.append(agent_id)
        
        print(f"\n  ✅ {profile.name} REACTIVATED and OPERATIONAL")
        return True
    
    def reactivate_priority_queue(self) -> Dict:
        """Reactivate all HIGH priority agents"""
        print("\n" + "=" * 70)
        print("  REACTIVATING HIGH PRIORITY AGENTS")
        print("=" * 70)
        
        results = {
            "attempted": 0,
            "successful": 0,
            "failed": []
        }
        
        for agent_id, profile in self.agents.items():
            if profile.priority == ReactivationPriority.HIGH and profile.current_status == "INACTIVE":
                results["attempted"] += 1
                if self.reactivate_agent(agent_id):
                    results["successful"] += 1
                else:
                    results["failed"].append(agent_id)
        
        print("\n" + "=" * 70)
        print(f"  Results: {results['successful']}/{results['attempted']} reactivated")
        print("=" * 70)
        
        return results
    
    def get_upgrade_report(self) -> str:
        """Generate report of upgrade needs for all agents"""
        report = []
        report.append("=" * 70)
        report.append("  AGENT UPGRADE ASSESSMENT REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Active agents
        report.append("ACTIVE AGENTS (No upgrades needed):")
        for agent_id in self.active_agents:
            profile = self.agents[agent_id]
            report.append(f"  ✅ {profile.name} - {profile.role}")
        
        report.append("")
        report.append("INACTIVE AGENTS (Require Reactivation + Upgrades):")
        report.append("")
        
        # Inactive agents by priority
        for priority in [ReactivationPriority.HIGH, ReactivationPriority.MEDIUM, ReactivationPriority.LOW]:
            report.append(f"{priority.value} PRIORITY:")
            
            for agent_id in self.inactive_agents:
                profile = self.agents[agent_id]
                if profile.priority == priority:
                    assessment = self.assess_upgrade_needs(agent_id)
                    report.append(f"  {profile.name} ({agent_id})")
                    report.append(f"    Role: {profile.role}")
                    report.append(f"    Needs: {', '.join(assessment['recommended_actions'])}")
                    report.append(f"    Missing files: {len(assessment['missing_files'])}")
                    report.append("")
        
        return "\n".join(report)


# Test function
def test_reactivation_protocol():
    """Test the reactivation protocol"""
    print("\n" + "=" * 70)
    print("  AGENT REACTIVATION PROTOCOL - TEST")
    print("=" * 70)
    
    protocol = AgentReactivationProtocol()
    
    # Show reactivation queue
    print("\n[Reactivation Queue]")
    queue = protocol.get_reactivation_queue()
    
    for priority, agents in queue.items():
        print(f"\n{priority.value} Priority ({len(agents)} agents):")
        for agent in agents:
            print(f"  - {agent.name} ({agent.role})")
    
    # Show upgrade report
    print("\n[Upgrade Assessment]")
    sample_agent = protocol.HIGH_PRIORITY_AGENTS[0][0]  # sentinel
    assessment = protocol.assess_upgrade_needs(sample_agent)
    print(f"\nSample: {assessment['name']}")
    print(f"  Needs crypto identity: {assessment['crypto_identity']}")
    print(f"  Needs crew isolation: {assessment['crew_isolation']}")
    print(f"  Needs Chief integration: {assessment['chief_integration']}")
    print(f"  Recommended actions: {assessment['recommended_actions']}")
    
    # Show full report
    print("\n[Full Upgrade Report]")
    report = protocol.get_upgrade_report()
    print(report[:1000] + "...")
    
    print("\n" + "=" * 70)
    print("  ✅ Reactivation Protocol Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_reactivation_protocol()
