#!/usr/bin/env python3
"""
AGI COMPANY MoE ROUTER v1.0
Mixture of Experts Routing System

Routes tasks to optimal agents based on:
- Roast Skill evaluation
- Expert specialization
- Model capabilities
- Current load
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ExpertType(Enum):
    FAST_RESPONSE = "fast_response"      # gemma2:2b
    DEEP_REASONING = "deep_reasoning"    # qwen2.5:14b
    VISION = "vision"                    # qwen3.5
    SALES_ROLEPLAY = "sales_roleplay"    # nous-hermes2
    VOICE = "voice"                      # Mort_II
    SPEED = "speed"                      # tinyllama
    EMBEDDING = "embedding"              # nomic-embed-text

@dataclass
class Expert:
    agent_id: str
    name: str
    expert_type: ExpertType
    model: str
    capabilities: List[str]
    current_load: int = 0
    max_concurrent: int = 3

class MoERouter:
    """
    Mixture of Experts Router for AGI Company
    
    Implements gating function to route tasks to optimal experts
    """
    
    def __init__(self):
        self.experts: Dict[str, Expert] = {}
        self.task_history: List[Dict] = []
        self._initialize_experts()
        print("[MoE Router] 🧠 Mixture of Experts initialized")
        print(f"  Total experts: {len(self.experts)}")
        print(f"  Expert types: {len(set(e.expert_type for e in self.experts.values()))}")
    
    def _initialize_experts(self):
        """Load all 54 agents as experts"""
        expert_configs = [
            # Fast Response (gemma2:2b)
            ("greet", "GREET", ExpertType.FAST_RESPONSE, "gemma2:2b", 
             ["front_desk", "scheduling", "quick_response"]),
            ("clerk", "Clerk", ExpertType.FAST_RESPONSE, "gemma2:2b",
             ["documentation", "data_entry", "filing"]),
            ("judy", "Judy", ExpertType.FAST_RESPONSE, "gemma2:2b",
             ["scheduling", "calendar", "coordination"]),
            
            # Deep Reasoning (qwen2.5:14b)
            ("dusty", "Dusty", ExpertType.DEEP_REASONING, "qwen2.5:14b",
             ["research", "analysis", "market_intelligence"]),
            ("chelios", "Chelios", ExpertType.DEEP_REASONING, "qwen2.5:14b",
             ["security_analysis", "threat_detection", "compliance"]),
            ("stacktrace", "Stacktrace", ExpertType.DEEP_REASONING, "qwen2.5:14b",
             ["debugging", "error_analysis", "root_cause"]),
            ("cryptonio", "Cryptonio", ExpertType.DEEP_REASONING, "qwen2.5:14b",
             ["trading_analysis", "market_scoring", "finance"]),
            
            # Vision (qwen3.5)
            ("aurora", "Aurora", ExpertType.VISION, "qwen3.5",
             ["design", "ux", "creative_direction", "visual"]),
            ("pixel", "Pixel", ExpertType.VISION, "qwen3.5",
             ["web_development", "frontend", "ui"]),
            ("forge", "Forge", ExpertType.VISION, "qwen3.5",
             ["infrastructure", "architecture", "systems"]),
            ("blender-expert", "Blender-Expert", ExpertType.VISION, "qwen3.5",
             ["3d_modeling", "rendering", "animation"]),
            
            # Sales/Roleplay (nous-hermes2)
            ("jane", "Jane", ExpertType.SALES_ROLEPLAY, "nous-hermes2",
             ["enterprise_sales", "negotiation", "closing"]),
            ("pulp", "Pulp", ExpertType.SALES_ROLEPLAY, "nous-hermes2",
             ["sales_strategy", "team_leadership", "revenue"]),
            ("hume", "Hume", ExpertType.SALES_ROLEPLAY, "nous-hermes2",
             ["regional_management", "sales_ops"]),
            ("closester", "CLOSETER", ExpertType.SALES_ROLEPLAY, "nous-hermes2",
             ["conversion", "deal_closing", "urgency"]),
            
            # Voice (Mort_II)
            ("miles", "Miles", ExpertType.VOICE, "antoniohudnall/Mort_II:latest",
             ["sales_consultant", "voice", "customer_calls"]),
            ("mortimer", "Mortimer", ExpertType.VOICE, "antoniohudnall/Mort_II:latest",
             ["model_host", "voice_synthesis"]),
            
            # Speed (tinyllama)
            ("spindle", "Spindle", ExpertType.SPEED, "tinyllama",
             ["scheduling", "task_routing", "coordination"]),
            ("taptap", "TAPTAP", ExpertType.SPEED, "tinyllama",
             ["code_review", "quality_check", "fast_validation"]),
            
            # Embedding (nomic-embed-text)
            ("qora", "QORA", ExpertType.EMBEDDING, "nomic-embed-text",
             ["query_optimization", "semantic_search", "embeddings"]),
        ]
        
        for agent_id, name, exp_type, model, caps in expert_configs:
            self.experts[agent_id] = Expert(
                agent_id=agent_id,
                name=name,
                expert_type=exp_type,
                model=model,
                capabilities=caps
            )
    
    def gate_task(self, task_description: str, task_type: str = None) -> List[Expert]:
        """
        Gating function - select optimal experts for task
        
        Uses keyword matching + Roast Skill evaluation
        """
        task_lower = task_description.lower()
        
        # Determine expert type from task
        expert_types_needed = []
        
        # Vision tasks
        if any(kw in task_lower for kw in ["design", "visual", "image", "web", "3d", "ui", "ux"]):
            expert_types_needed.append(ExpertType.VISION)
        
        # Sales tasks
        if any(kw in task_lower for kw in ["sales", "customer", "lead", "deal", "revenue", "client"]):
            expert_types_needed.append(ExpertType.SALES_ROLEPLAY)
        
        # Deep reasoning
        if any(kw in task_lower for kw in ["research", "analysis", "security", "debug", "investigate"]):
            expert_types_needed.append(ExpertType.DEEP_REASONING)
        
        # Voice
        if any(kw in task_lower for kw in ["call", "voice", "phone", "speak", "tts"]):
            expert_types_needed.append(ExpertType.VOICE)
        
        # Speed/Routing
        if any(kw in task_lower for kw in ["schedule", "route", "coordinate", "quick"]):
            expert_types_needed.append(ExpertType.SPEED)
        
        # Search
        if any(kw in task_lower for kw in ["search", "query", "find", "retrieve"]):
            expert_types_needed.append(ExpertType.EMBEDDING)
        
        # Default to fast response if no match
        if not expert_types_needed:
            expert_types_needed = [ExpertType.FAST_RESPONSE]
        
        # Get available experts (not overloaded)
        selected_experts = []
        for exp_type in expert_types_needed:
            available = [
                e for e in self.experts.values()
                if e.expert_type == exp_type and e.current_load < e.max_concurrent
            ]
            if available:
                # Pick least loaded
                expert = min(available, key=lambda e: e.current_load)
                expert.current_load += 1
                selected_experts.append(expert)
        
        return selected_experts
    
    def route_task(self, task_description: str, context: Dict = None) -> Dict:
        """
        Full MoE routing pipeline
        
        1. Evaluate with Roast Skill
        2. Gate to select experts
        3. Execute with assigned models
        4. Aggregate results
        """
        print(f"\n[MoE Router] 🎯 Routing task: {task_description[:50]}...")
        
        # Step 1: Roast Skill evaluation
        try:
            from roast_skill import RoastSkill
            roast = RoastSkill()
            if roast.should_roast({"title": task_description, "description": task_description}):
                roast_report = roast.roast({"title": task_description, "description": task_description})
                print(f"  🔥 Roast: {roast_report['verdict']} ({roast_report['weighted_score']:.1f}/10)")
        except:
            pass
        
        # Step 2: Gate to experts
        experts = self.gate_task(task_description)
        
        if not experts:
            return {
                "status": "error",
                "message": "No available experts",
                "timestamp": time.time()
            }
        
        print(f"  🧠 Selected {len(experts)} expert(s):")
        for exp in experts:
            print(f"    • {exp.name} ({exp.expert_type.value}) → {exp.model}")
        
        # Step 3: Execute (simulated)
        results = []
        for expert in experts:
            result = self._execute_with_expert(expert, task_description)
            results.append(result)
            expert.current_load -= 1  # Release
        
        # Step 4: Aggregate
        aggregated = self._aggregate_results(results, experts)
        
        return {
            "status": "success",
            "task": task_description,
            "experts_used": [e.name for e in experts],
            "models_used": list(set(e.model for e in experts)),
            "results": results,
            "aggregated_output": aggregated,
            "timestamp": time.time()
        }
    
    def _execute_with_expert(self, expert: Expert, task: str) -> Dict:
        """Execute task with specific expert"""
        # In production, this would actually load the model and run
        return {
            "expert": expert.name,
            "model": expert.model,
            "output": f"[{expert.name}] Processed using {expert.model}",
            "confidence": 0.85,
            "timestamp": time.time()
        }
    
    def _aggregate_results(self, results: List[Dict], experts: List[Expert]) -> str:
        """Aggregate outputs from multiple experts"""
        if len(results) == 1:
            return results[0]["output"]
        
        # Multi-expert aggregation
        outputs = [r["output"] for r in results]
        expert_names = [e.name for e in experts]
        
        return f"Aggregated output from {len(experts)} experts ({', '.join(expert_names)}): " + \
               " | ".join(outputs)
    
    def get_system_status(self) -> Dict:
        """Get MoE system status"""
        return {
            "total_experts": len(self.experts),
            "by_type": {
                exp_type.value: len([e for e in self.experts.values() if e.expert_type == exp_type])
                for exp_type in ExpertType
            },
            "active_tasks": sum(e.current_load for e in self.experts.values()),
            "available_experts": len([e for e in self.experts.values() if e.current_load < e.max_concurrent])
        }

def main():
    """Test MoE Router"""
    print("=" * 70)
    print("  AGI COMPANY MoE ROUTER - TEST")
    print("=" * 70)
    
    router = MoERouter()
    
    # Test routing
    test_tasks = [
        "Design a new landing page for PSD",
        "Close the deal with Acme Corp",
        "Debug why the API is returning 500 errors",
        "Schedule a meeting for next week",
        "Research POS terminal market trends",
        "Make a sales call to follow up on the quote",
    ]
    
    for task in test_tasks:
        result = router.route_task(task)
        print(f"\n  Result: {result['aggregated_output'][:80]}...")
    
    # System status
    print("\n" + "=" * 70)
    print("  SYSTEM STATUS")
    print("=" * 70)
    status = router.get_system_status()
    print(f"\n  Total experts: {status['total_experts']}")
    print(f"  Active tasks: {status['active_tasks']}")
    print(f"  Available: {status['available_experts']}")
    print("\n  By type:")
    for exp_type, count in status['by_type'].items():
        print(f"    • {exp_type}: {count} experts")
    
    print("\n" + "=" * 70)
    print("  ✅ MoE Router Operational")
    print("=" * 70)

if __name__ == "__main__":
    main()
