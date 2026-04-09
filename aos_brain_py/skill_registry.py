#!/usr/bin/env python3
"""
SkillRegistry - Central registry for brain skills.
Phase 1: Foundation

Manages skill registration, versioning, and contract validation.
"""

import os
import re
import yaml
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

class SkillTier(Enum):
    STANDARD = "standard"      # 5ms execution, internal
    METHODOLOGY = "methodology"  # 50ms, may use Ollama
    PERSONAL = "personal"      # 200ms, agent-specific
    DIAGNOSTIC = "diagnostic"  # 10ms, system health

@dataclass
class Contract:
    """Input/output contract for a skill."""
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    
    def validate_input(self, data: Dict) -> tuple[bool, str]:
        """Validate input against schema."""
        return self._validate(data, self.input_schema)
    
    def validate_output(self, data: Dict) -> tuple[bool, str]:
        """Validate output against schema."""
        return self._validate(data, self.output_schema)
    
    def _validate(self, data: Dict, schema: Dict) -> tuple[bool, str]:
        """Basic schema validation."""
        required = schema.get('required', [])
        for field in required:
            if field not in data:
                return False, f"Missing required field: {field}"
        return True, "valid"

@dataclass
class Skill:
    """Represents a registered skill."""
    name: str
    version: str
    tier: SkillTier
    description: str
    contract: Contract
    handler: Callable[[Dict], Dict]  # Function that implements skill
    metadata: Dict = field(default_factory=dict)
    
    @property
    def full_name(self) -> str:
        return f"{self.name}@{self.version}"
    
    def call(self, input_data: Dict, timeout_ms: int = 100) -> Dict:
        """Execute skill with contract validation."""
        start = time.time()
        
        # Validate input
        valid, error = self.contract.validate_input(input_data)
        if not valid:
            return {"error": error, "status": "input_validation_failed"}
        
        try:
            # Execute
            result = self.handler(input_data)
            
            # Validate output
            valid, error = self.contract.validate_output(result)
            if not valid:
                return {"error": error, "status": "output_validation_failed"}
            
            # Add metadata
            result['_meta'] = {
                'skill': self.full_name,
                'tier': self.tier.value,
                'latency_ms': (time.time() - start) * 1000
            }
            
            return result
            
        except Exception as e:
            return {"error": str(e), "status": "execution_failed"}

class SkillRegistry:
    """
    Central registry for brain skills.
    
    Usage:
        registry = SkillRegistry()
        registry.register(skill)
        result = registry.call("thalamus@1.0.0", input_data)
    """
    
    def __init__(self, skills_dir: Optional[str] = None):
        self.skills: Dict[str, Skill] = {}
        self.versions: Dict[str, List[str]] = {}  # name -> [versions]
        self.call_history: List[Dict] = []
        self.skills_dir = skills_dir or self._default_skills_dir()
        
        # Load built-in skills
        self._load_builtin_skills()
    
    def _default_skills_dir(self) -> str:
        """Get default skills directory."""
        return str(Path.home() / ".aos" / "aos" / "aos_brain_py" / "skills")
    
    def register(self, skill: Skill) -> bool:
        """Register a skill."""
        self.skills[skill.full_name] = skill
        
        if skill.name not in self.versions:
            self.versions[skill.name] = []
        if skill.version not in self.versions[skill.name]:
            self.versions[skill.name].append(skill.version)
            self.versions[skill.name].sort()  # Keep versions sorted
        
        return True
    
    def get(self, name: str, version: Optional[str] = None) -> Optional[Skill]:
        """Get skill by name (and optional version)."""
        if version:
            return self.skills.get(f"{name}@{version}")
        
        # Get latest version
        versions = self.versions.get(name, [])
        if versions:
            return self.skills.get(f"{name}@{versions[-1]}")
        return None
    
    def call(self, name: str, input_data: Dict, version: Optional[str] = None, timeout_ms: int = 100) -> Dict:
        """Call skill with optional version."""
        skill = self.get(name, version)
        if not skill:
            return {"error": f"Skill not found: {name}", "status": "not_found"}
        
        result = skill.call(input_data, timeout_ms)
        
        # Log call
        self.call_history.append({
            'skill': skill.full_name,
            'input': input_data,
            'output': result,
            'timestamp': time.time()
        })
        
        return result
    
    def list_skills(self, tier: Optional[SkillTier] = None) -> List[Skill]:
        """List all registered skills, optionally filtered by tier."""
        skills = list(self.skills.values())
        if tier:
            skills = [s for s in skills if s.tier == tier]
        return skills
    
    def health_check(self) -> Dict:
        """Check registry health."""
        return {
            "status": "healthy",
            "skills_registered": len(self.skills),
            "unique_names": len(self.versions),
            "by_tier": {
                tier.value: len([s for s in self.skills.values() if s.tier == tier])
                for tier in SkillTier
            }
        }
    
    def _load_builtin_skills(self):
        """Load built-in diagnostic and region skills."""
        # These will be implemented in Phase 2
        pass

# Singleton instance for brain
_registry: Optional[SkillRegistry] = None

def get_registry() -> SkillRegistry:
    """Get or create singleton registry."""
    global _registry
    if _registry is None:
        _registry = SkillRegistry()
    return _registry
