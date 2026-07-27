#!/usr/bin/env python3
"""
ACTIVATION WAVE 2 v1.0
Post-Full-Org-Roast Implementation

ACTIVATING (3):
- Blender-Expert (Creative) - unblock Aurora
- Scribble (Creative) - concept art capacity  
- Hume (Sales) - regional coverage

GOAL: 15 → 18 ACTIVE (44% workforce)
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import os


@dataclass
class AgentActivation:
    """Agent activation state"""
    agent_id: str
    name: str
    role: str
    department: str
    model: str
    reports_to: str
    activation_reason: str
    immediate_task: str


class ActivationWave2:
    """
    Second wave activation: Critical path agents from full org roast
    """
    
    WAVE_2_TARGETS = [
        {
            "agent_id": "blender-expert_001",
            "name": "Blender-Expert",
            "role": "3D Design / Blender Specialist",
            "department": "Creative",
            "model": "qwen3.5",
            "reports_to": "aurora_001",
            "reason": "Creative dept 83% inactive - Aurora bottleneck. Need 3D capability for N'og nog game.",
            "task": "Create 3D voxel asset for N'og nog game (character model or environment piece)"
        },
        {
            "agent_id": "scribble_001", 
            "name": "Scribble",
            "role": "Concept Art / Illustration",
            "department": "Creative",
            "model": "qwen3.5",
            "reports_to": "aurora_001",
            "reason": "Creative capacity. Concept art for PSD website or game assets.",
            "task": "Create 3 concept art pieces: (1) AGI Company logo concept, (2) N'og nog character sketch, (3) PSD hero image concept"
        },
        {
            "agent_id": "hume_001",
            "name": "Hume", 
            "role": "Regional Sales Manager",
            "department": "Sales",
            "model": "nous-hermes2:latest",
            "reports_to": "pulp_001",
            "reason": "Sales dept lacks regional coverage. 2,911 leads need territory management.",
            "task": "Segment 2,911 leads by region. Identify top 3 territories with highest density."
        }
    ]
    
    def __init__(self):
        self.activations: Dict[str, AgentActivation] = {}
        self._init_activations()
    
    def _init_activations(self):
        """Initialize activation tracking"""
        for target in self.WAVE_2_TARGETS:
            self.activations[target["agent_id"]] = AgentActivation(
                agent_id=target["agent_id"],
                name=target["name"],
                role=target["role"],
                department=target["department"],
                model=target["model"],
                reports_to=target["reports_to"],
                activation_reason=target["reason"],
                immediate_task=target["task"]
            )
    
    def activate_agent(self, agent_id: str) -> Dict:
        """Activate single agent"""
        agent = self.activations.get(agent_id)
        if not agent:
            return {"error": "Agent not found"}
        
        print(f"\n🚀 Activating {agent.name}...")
        
        # Create workspace
        workspace_path = f"/var/lib/aos/agents/crew-{agent_id}/"
        os.makedirs(workspace_path, exist_ok=True)
        os.makedirs(f"{workspace_path}/tasks", exist_ok=True)
        os.makedirs(f"{workspace_path}/outputs", exist_ok=True)
        
        # Create config
        config = {
            "agent_id": agent_id,
            "name": agent.name,
            "role": agent.role,
            "department": agent.department,
            "model": agent.model,
            "reports_to": agent.reports_to,
            "activated_at": datetime.now().isoformat(),
            "status": "ACTIVE",
            "wave": 2,
            "immediate_task": agent.immediate_task
        }
        
        with open(f"{workspace_path}/config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        # Create task file
        with open(f"{workspace_path}/tasks/current_task.md", "w") as f:
            f.write(f"# Immediate Task\n\n{agent.immediate_task}\n\n")
            f.write(f"Assigned: {datetime.now().isoformat()}\n")
            f.write(f"ETA: 48 hours\n")
        
        print(f"  ✅ {agent.name} activated")
        print(f"     Role: {agent.role}")
        print(f"     Dept: {agent.department}")
        print(f"     Task: {agent.immediate_task[:50]}...")
        
        return {
            "agent": agent.name,
            "department": agent.department,
            "status": "ACTIVATED",
            "task": agent.immediate_task
        }
    
    def run_activation(self) -> Dict:
        """Run Wave 2 activation"""
        print("=" * 70)
        print("🚀 ACTIVATION WAVE 2 v1.0")
        print("=" * 70)
        print("Target: 3 agents → 18 ACTIVE total (44% workforce)")
        print("Source: Full Org Roast - unblock Creative + Sales")
        print("=" * 70)
        
        results = {
            "wave": 2,
            "started_at": datetime.now().isoformat(),
            "activations": []
        }
        
        for target in self.WAVE_2_TARGETS:
            result = self.activate_agent(target["agent_id"])
            results["activations"].append(result)
        
        results["completed_at"] = datetime.now().isoformat()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 WAVE 2 SUMMARY")
        print("=" * 70)
        print(f"Activated: {len(results['activations'])}/3")
        
        print("\n🟢 NEWLY ACTIVE:")
        for act in results["activations"]:
            print(f"  • {act['agent']} ({act['department']})")
        
        print(f"\n📈 WORKFORCE:")
        print(f"  Before: 15 ACTIVE / 41 total (36.6%)")
        print(f"  After:  18 ACTIVE / 41 total (43.9%)")
        print(f"  Target: 44%")
        
        return results
    
    def print_department_impact(self):
        """Show impact on departments"""
        print("\n" + "=" * 70)
        print("🎯 DEPARTMENT IMPACT")
        print("=" * 70)
        
        impact = {
            "Creative": {
                "before": "1/6 active (17%) - Aurora bottleneck",
                "after": "3/6 active (50%) - Aurora + Blender + Scribble",
                "unblocked": "3D capability, concept art capacity"
            },
            "Sales": {
                "before": "3/6 active (50%) - Jordan, Pulp, Jane",
                "after": "4/6 active (67%) - +Hume regional",
                "unblocked": "Territory management for 2,911 leads"
            }
        }
        
        for dept, data in impact.items():
            print(f"\n📁 {dept}")
            print(f"   Before: {data['before']}")
            print(f"   After:  {data['after']}")
            print(f"   Impact: {data['unblocked']}")
    
    def export_manifest(self) -> str:
        """Export activation manifest"""
        export = {
            "wave": 2,
            "name": "Activation Wave 2 - Post Full Org Roast",
            "generated_at": datetime.now().isoformat(),
            "rationale": "Unblock Creative (83% inactive) and Sales (no regional coverage)",
            "agents": {}
        }
        
        for agent_id, agent in self.activations.items():
            export["agents"][agent_id] = {
                "name": agent.name,
                "role": agent.role,
                "department": agent.department,
                "model": agent.model,
                "reports_to": agent.reports_to,
                "task": agent.immediate_task,
                "reason": agent.activation_reason
            }
        
        return json.dumps(export, indent=2)


def main():
    """Run Activation Wave 2"""
    wave = ActivationWave2()
    results = wave.run_activation()
    wave.print_department_impact()
    
    # Export
    export = wave.export_manifest()
    with open("/root/.aos/aos/activation_wave_2.json", "w") as f:
        f.write(export)
    
    print("\n💾 Manifest saved: /root/.aos/aos/activation_wave_2.json")
    print("=" * 70)
    print("🎯 WAVE 2 COMPLETE: 18 ACTIVE / 41 total (43.9%)")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    main()
