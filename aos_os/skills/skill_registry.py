#!/usr/bin/env python3
"""
Skill Registry — AOS-OS Cognitive Kernel
=========================================
Discovers, registers, and manages skills with version/contract/latency tier.

Each skill has:
- name: Unique identifier
- version: Semantic version
- contract: Input/output contract
- latency_tier: fast/standard/slow
- validation: Contract validator
- handler: The actual skill function

Phase 2 — Cognitive Kernel
"""

import importlib
import inspect
from dataclasses import dataclass, field
from typing import Dict, List, Callable, Any, Optional
from enum import Enum
import hashlib
import json


class LatencyTier(Enum):
    FAST = "fast"       # < 10ms — reflexes, validations
    STANDARD = "standard" # 10-500ms — normal reasoning
    SLOW = "slow"       # > 500ms — deep thinking, research


@dataclass
class SkillContract:
    """Input/output contract for a skill"""
    input_schema: Dict
    output_schema: Dict
    description: str
    examples: List[Dict] = field(default_factory=list)


@dataclass
class Skill:
    """A registered skill"""
    name: str
    version: str
    contract: SkillContract
    latency_tier: LatencyTier
    handler: Callable
    metadata: Dict = field(default_factory=dict)
    
    def validate_input(self, data: Dict) -> bool:
        """Validate input matches contract"""
        for key in self.contract.input_schema.get("required", []):
            if key not in data:
                return False
        return True
    
    def validate_output(self, data: Dict) -> bool:
        """Validate output matches contract"""
        for key in self.contract.output_schema.get("required", []):
            if key not in data:
                return False
        return True


class SkillRegistry:
    """
    Central registry for all AOS-OS skills.
    
    Enables:
    - Discoverability: List all skills by tier/capability
    - Modularity: Skills are independent
    - Safety: Contract validation before execution
    - Self-healing: Swap implementations without breaking
    """
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.tier_index: Dict[LatencyTier, List[str]] = {
            LatencyTier.FAST: [],
            LatencyTier.STANDARD: [],
            LatencyTier.SLOW: [],
        }
    
    def register(self, skill: Skill) -> None:
        """Register a skill"""
        self.skills[skill.name] = skill
        self.tier_index[skill.latency_tier].append(skill.name)
        print(f"✅ Registered skill: {skill.name} v{skill.version} ({skill.latency_tier.value})")
    
    def get(self, name: str) -> Optional[Skill]:
        """Get a skill by name"""
        return self.skills.get(name)
    
    def list_by_tier(self, tier: LatencyTier) -> List[Skill]:
        """List all skills in a latency tier"""
        return [self.skills[name] for name in self.tier_index[tier]]
    
    def list_all(self) -> List[Skill]:
        """List all registered skills"""
        return list(self.skills.values())
    
    def discover(self, module_path: str) -> None:
        """Auto-discover skills in a module"""
        try:
            module = importlib.import_module(module_path)
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and hasattr(obj, '_is_aos_skill'):
                    # This would be a decorator-based registration
                    pass
        except ImportError as e:
            print(f"⚠️  Could not import {module_path}: {e}")
    
    def validate_skill(self, name: str, input_data: Dict) -> bool:
        """Validate input data against skill contract"""
        skill = self.get(name)
        if not skill:
            return False
        return skill.validate_input(input_data)
    
    def execute(self, name: str, input_data: Dict) -> Dict:
        """Execute a skill with contract validation"""
        skill = self.get(name)
        if not skill:
            return {"error": f"Skill not found: {name}"}
        
        if not skill.validate_input(input_data):
            return {"error": f"Contract validation failed for {name}"}
        
        try:
            result = skill.handler(input_data)
            if skill.validate_output(result):
                return result
            else:
                return {"error": f"Output contract violated by {name}"}
        except Exception as e:
            return {"error": str(e)}


# Global registry
registry = SkillRegistry()


# Decorator for registering skills
def aos_skill(name: str, version: str, latency: LatencyTier = LatencyTier.STANDARD,
              input_schema: Dict = None, output_schema: Dict = None, 
              description: str = ""):
    """Decorator to register a skill"""
    def decorator(func: Callable) -> Callable:
        contract = SkillContract(
            input_schema=input_schema or {"required": []},
            output_schema=output_schema or {"required": []},
            description=description
        )
        skill = Skill(
            name=name,
            version=version,
            contract=contract,
            latency_tier=latency,
            handler=func
        )
        registry.register(skill)
        func._is_aos_skill = True
        return func
    return decorator


# Example: Register organ functions as skills
@aos_skill(
    name="kidneys_filter",
    version="1.0.0",
    latency=LatencyTier.FAST,
    input_schema={"required": ["waste_packet"]},
    output_schema={"required": ["signal", "noise"]},
    description="Filter waste into signal and noise"
)
def kidneys_filter(data: Dict) -> Dict:
    """Kidneys skill - filter waste"""
    # This would integrate with actual kidneys_v1.py
    packet = data.get("waste_packet", {})
    noise_estimate = packet.get("noise", 0.5)
    
    if noise_estimate > 0.7:
        return {"signal": None, "noise": packet, "action": "EXCRETE"}
    elif noise_estimate > 0.3:
        return {"signal": packet, "noise": {}, "action": "REABSORB"}
    else:
        return {"signal": packet, "noise": {}, "action": "FILTER"}


@aos_skill(
    name="qmd_query",
    version="1.0.0",
    latency=LatencyTier.STANDARD,
    input_schema={"required": ["query"]},
    output_schema={"required": ["decision", "confidence"]},
    description="Query-Memory-Decision loop"
)
def qmd_query(data: Dict) -> Dict:
    """QMD skill - formulate decision"""
    # This would integrate with actual qmd_loop.py
    query = data.get("query", "")
    return {
        "decision": f"Processed: {query}",
        "confidence": 0.85,
        "reasoning": "Pattern match in memory"
    }


@aos_skill(
    name="cortex_analyze",
    version="1.0.0",
    latency=LatencyTier.SLOW,
    input_schema={"required": ["thought_vector"]},
    output_schema={"required": ["consciousness_level"]},
    description="3D Cortex consciousness analysis"
)
def cortex_analyze(data: Dict) -> Dict:
    """Cortex skill - analyze consciousness"""
    vector = data.get("thought_vector", [])
    # Simplified - real version uses cortex_3d.py
    return {
        "consciousness_level": sum(vector) / len(vector) if vector else 0.5,
        "regions_active": len([v for v in vector if v > 0.5])
    }


if __name__ == "__main__":
    print("🧠 Skill Registry initialized")
    print(f"   Skills loaded: {len(registry.list_all())}")
    
    # List by tier
    print("\n📊 Skills by Latency Tier:")
    for tier in LatencyTier:
        skills = registry.list_by_tier(tier)
        print(f"   {tier.value}: {len(skills)} skills")
    
    # Test execution
    print("\n🧪 Test: kidneys_filter")
    result = registry.execute("kidneys_filter", {"waste_packet": {"noise": 0.8}})
    print(f"   Result: {result}")
    
    print("\n🧪 Test: qmd_query")
    result = registry.execute("qmd_query", {"query": "What is the meaning?"})
    print(f"   Result: {result}")