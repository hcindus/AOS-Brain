#!/usr/bin/env python3
"""
Skill Orchestrator — AOS-OS Cognitive Kernel
=============================================
Executes skills by latency tier, handles fallbacks, manages skill chains.

Phase 2 — Cognitive Kernel
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque

from skill_registry import SkillRegistry, LatencyTier, Skill


class OrchestrationMode(Enum):
    SEQUENTIAL = "sequential"     # One after another
    PARALLEL = "parallel"           # All at once
    CASCADE = "cascade"             # Output → input chain
    GUARDED = "guarded"             # With fallbacks


@dataclass
class SkillChain:
    """A chain of skills to execute"""
    name: str
    skills: List[str]  # Skill names
    mode: OrchestrationMode = OrchestrationMode.SEQUENTIAL
    timeout_ms: int = 5000


@dataclass
class OrchestrationResult:
    """Result of orchestration"""
    success: bool
    outputs: List[Dict]
    errors: List[str]
    total_time_ms: float
    tier_used: LatencyTier


class SkillOrchestrator:
    """
    Orchestrates skill execution.
    
    Responsibilities:
    - Select skills by latency tier
    - Handle fallbacks on failure
    - Manage skill chains (cascade, parallel, sequential)
    - Track execution metrics
    - Enforce timeouts
    """
    
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.chains: Dict[str, SkillChain] = {}
        self.execution_log: List[Dict] = []
        self.fallback_map: Dict[str, str] = {}  # skill → fallback_skill
    
    def register_fallback(self, skill: str, fallback: str) -> None:
        """Register a fallback skill"""
        self.fallback_map[skill] = fallback
    
    def register_chain(self, chain: SkillChain) -> None:
        """Register a skill chain"""
        self.chains[chain.name] = chain
    
    async def execute_skill(self, skill_name: str, input_data: Dict, 
                          timeout_ms: int = 5000) -> Dict:
        """Execute a single skill with timeout"""
        skill = self.registry.get(skill_name)
        if not skill:
            return {"error": f"Skill not found: {skill_name}"}
        
        start = time.time()
        try:
            # Run sync skills in executor to not block
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(None, skill.handler, input_data),
                timeout_ms / 1000
            )
            elapsed = (time.time() - start) * 1000
            
            self.execution_log.append({
                "skill": skill_name,
                "elapsed_ms": elapsed,
                "success": True
            })
            
            return result
            
        except asyncio.TimeoutError:
            elapsed = (time.time() - start) * 1000
            self.execution_log.append({
                "skill": skill_name,
                "elapsed_ms": elapsed,
                "success": False,
                "error": "Timeout"
            })
            # Try fallback
            if skill_name in self.fallback_map:
                return await self.execute_skill(
                    self.fallback_map[skill_name], input_data, timeout_ms
                )
            return {"error": f"Timeout on {skill_name}, no fallback"}
            
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            self.execution_log.append({
                "skill": skill_name,
                "elapsed_ms": elapsed,
                "success": False,
                "error": str(e)
            })
            # Try fallback
            if skill_name in self.fallback_map:
                return await self.execute_skill(
                    self.fallback_map[skill_name], input_data, timeout_ms
                )
            return {"error": str(e)}
    
    async def execute_chain(self, chain_name: str, input_data: Dict) -> OrchestrationResult:
        """Execute a skill chain"""
        chain = self.chains.get(chain_name)
        if not chain:
            return OrchestrationResult(
                success=False,
                outputs=[],
                errors=[f"Chain not found: {chain_name}"],
                total_time_ms=0,
                tier_used=LatencyTier.STANDARD
            )
        
        start = time.time()
        outputs = []
        errors = []
        
        if chain.mode == OrchestrationMode.SEQUENTIAL:
            data = input_data
            for skill_name in chain.skills:
                result = await self.execute_skill(skill_name, data, chain.timeout_ms)
                if "error" in result:
                    errors.append(result["error"])
                    break
                outputs.append(result)
                data = result  # Cascade output to input
        
        elif chain.mode == OrchestrationMode.PARALLEL:
            tasks = [
                self.execute_skill(skill_name, input_data, chain.timeout_ms)
                for skill_name in chain.skills
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for r in results:
                if isinstance(r, Exception):
                    errors.append(str(r))
                elif "error" in r:
                    errors.append(r["error"])
                else:
                    outputs.append(r)
        
        elif chain.mode == OrchestrationMode.CASCADE:
            data = input_data
            for skill_name in chain.skills:
                result = await self.execute_skill(skill_name, data, chain.timeout_ms)
                if "error" in result:
                    errors.append(result["error"])
                    outputs.append({"error": result["error"]})
                    break
                outputs.append(result)
                data = result
        
        elapsed = (time.time() - start) * 1000
        
        return OrchestrationResult(
            success=len(errors) == 0,
            outputs=outputs,
            errors=errors,
            total_time_ms=elapsed,
            tier_used=LatencyTier.STANDARD
        )
    
    async def execute_by_tier(self, query: str, max_latency_ms: int = 5000) -> Dict:
        """Execute skills by preferred latency tier"""
        # Try FAST first
        fast_skills = self.registry.list_by_tier(LatencyTier.FAST)
        if fast_skills:
            result = await self.execute_skill(
                fast_skills[0].name, 
                {"query": query},
                max_latency_ms
            )
            if "error" not in result:
                return result
        
        # Try STANDARD
        standard_skills = self.registry.list_by_tier(LatencyTier.STANDARD)
        if standard_skills:
            result = await self.execute_skill(
                standard_skills[0].name,
                {"query": query},
                max_latency_ms
            )
            if "error" not in result:
                return result
        
        # Try SLOW as fallback
        slow_skills = self.registry.list_by_tier(LatencyTier.SLOW)
        if slow_skills:
            return await self.execute_skill(
                slow_skills[0].name,
                {"query": query},
                max_latency_ms * 2  # Allow more time
            )
        
        return {"error": "No skills available"}
    
    def get_metrics(self) -> Dict:
        """Get execution metrics"""
        if not self.execution_log:
            return {"total_executions": 0, "success_rate": 0, "avg_latency_ms": 0}
        
        total = len(self.execution_log)
        successes = sum(1 for e in self.execution_log if e.get("success"))
        avg_latency = sum(e.get("elapsed_ms", 0) for e in self.execution_log) / total
        
        return {
            "total_executions": total,
            "success_rate": successes / total,
            "avg_latency_ms": avg_latency,
            "recent": self.execution_log[-10:]
        }


# Example chain: think → decide → act
THINK_DECIDE_CHAIN = SkillChain(
    name="think_decide_act",
    skills=["cortex_analyze", "qmd_query", "kidneys_filter"],
    mode=OrchestrationMode.CASCADE,
    timeout_ms=5000
)


if __name__ == "__main__":
    print("🎼 Skill Orchestrator initialized")
    
    # This would import from skill_registry
    # orchestrator = SkillOrchestrator(registry)
    # orchestrator.register_chain(THINK_DECIDE_CHAIN)
    
    print("   Ready to orchestrate skill chains")