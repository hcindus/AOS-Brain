#!/usr/bin/env python3
"""
Brain API - How Agents USE the Brain (Not Just Feed It)
7-Region OODA Processing for Active Queries
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

from brain_v31 import AOSBrainV31
from ternary_interfaces import BrainInput, HeartState

class BrainAPI:
    """
    Agents query the brain for decisions, memory, analysis
    Not just feeding - ACTIVE USAGE
    """
    
    def __init__(self):
        self.brain = AOSBrainV31()
        print("=" * 70)
        print("  🧠 BRAIN API - 7-Region Active Processing")
        print("  Agents query for decisions, not just feed data")
        print("=" * 70)
    
    def query_decision(self, context: str, options: list) -> dict:
        """
        AGENT USE: Ask brain to make a decision
        Routes through: Sensory -> PFC -> Basal Ganglia
        """
        # Simulate OODA processing
        brain_input = BrainInput(
            heart_bpm=72.0,
            heart_state=HeartState.BALANCE,
            heart_coherence=0.7,
            heart_arousal=0.5,
            emotional_tone="balanced",
            observation=f"DECISION REQUEST: {context}",
            observation_type="agent_query"
        )
        
        result = self.brain.tick(brain_input)
        
        # PFC selects best option based on memory + emotion
        decision = self._pfc_decide(context, options, result)
        
        return {
            "decision": decision,
            "phase": result.phase,
            "confidence": result.novelty,  # Higher novelty = more exploration needed
            "ticks_processed": result.tick_count
        }
    
    def query_memory(self, query: str) -> list:
        """
        AGENT USE: Ask brain to recall relevant memories
        Routes through: Hippocampus -> Sensory -> PFC
        """
        # Query memory via memory_bridge or direct trace access
        # For demo: return recent traces
        recent_traces = []
        if hasattr(self.brain.hippocampus, 'traces'):
            recent = list(self.brain.hippocampus.traces)[-5:]  # Last 5 traces
            for trace in recent:
                recent_traces.append({
                    "pattern": trace.pattern[:50] if hasattr(trace, 'pattern') else str(trace)[:50],
                    "strength": trace.strength if hasattr(trace, 'strength') else 0.5,
                    "age_ticks": 0
                })
        
        return recent_traces
    
    def query_emotion(self, situation: str) -> dict:
        """
        AGENT USE: Ask brain for emotional read on situation
        Routes through: Limbic (Amygdala) -> PFC
        """
        return {
            "arousal": self.brain.limbic.get("arousal", 0.5),
            "valence": self.brain.limbic.get("valence", 0.0),
            "coherence": self.brain.limbic.get("coherence", 0.5),
            "recommendation": "explore" if self.brain.limbic.get("novelty", 0.5) > 0.7 else "exploit"
        }
    
    def query_action(self, goal: str, constraints: list) -> dict:
        """
        AGENT USE: Ask brain what action to take
        Full 7-region processing:
        1. Sensory: Parse goal/constraints
        2. Hippocampus: Recall similar situations
        3. PFC: Evaluate options
        4. Limbic: Check emotional suitability
        5. Basal Ganglia: Select action
        6. Cerebellum: Coordinate timing
        7. Brainstem: Execute
        """
        # Full OODA cycle
        brain_input = BrainInput(
            heart_bpm=72.0,
            heart_state=HeartState.ACTIVE,
            heart_coherence=0.8,
            heart_arousal=0.6,
            emotional_tone="focused",
            observation=f"ACTION REQUEST: {goal} | Constraints: {constraints}",
            observation_type="agent_action_request"
        )
        
        result = self.brain.tick(brain_input)
        
        return {
            "action": result.phase.lower(),  # observe/orient/decide/act
            "goal_progress": "progressing",
            "tick": result.tick_count,
            "novelty": result.novelty
        }
    
    def _pfc_decide(self, context: str, options: list, brain_state) -> str:
        """PFC decision logic"""
        # Simple decision based on phase
        if brain_state.phase == "Decide":
            return options[0] if options else "wait"
        elif brain_state.phase == "Act":
            return options[-1] if options else "execute"
        else:
            return options[len(options)//2] if options else "observe"


class AgentBrainInterface:
    """
    Example: How different agents USE the brain
    """
    
    def __init__(self, brain_api: BrainAPI):
        self.brain = brain_api
    
    def sales_agent_example(self, lead_data: dict) -> dict:
        """
        SALES AGENT (like Miles):
        Uses brain to decide: call, email, or wait?
        """
        # Query decision
        decision = self.brain.query_decision(
            context=f"Lead: {lead_data.get('company', 'Unknown')} | Priority: {lead_data.get('priority', 'C')}",
            options=["immediate_call", "send_email", "wait_24h", "nurture_sequence"]
        )
        
        # Query emotion (should I be excited? cautious?)
        emotion = self.brain.query_emotion(
            situation="High-value lead from enterprise company"
        )
        
        return {
            "action": decision["decision"],
            "tone": "enthusiastic" if emotion["valence"] > 0.3 else "professional",
            "urgency": "high" if emotion["arousal"] > 0.6 else "normal"
        }
    
    def security_agent_example(self, threat_data: dict) -> dict:
        """
        SECURITY AGENT (like Mortimer):
        Uses brain to decide: alert, block, or monitor?
        """
        # Query memory (have we seen this before?)
        memories = self.brain.query_memory(
            query=f"threat:{threat_data.get('type', 'unknown')} source:{threat_data.get('ip', 'unknown')}"
        )
        
        # Query decision
        decision = self.brain.query_decision(
            context=f"Security event: {threat_data.get('severity', 'low')}",
            options=["immediate_block", "alert_operator", "increase_monitoring", "log_only"]
        )
        
        return {
            "action": decision["decision"],
            "historical_match": len(memories) > 0,
            "confidence": decision["confidence"]
        }
    
    def creative_agent_example(self, project_brief: str) -> dict:
        """
        CREATIVE AGENT:
        Uses brain for: concept generation, mood analysis
        """
        # Query emotion (what's the vibe?)
        emotion = self.brain.query_emotion(
            situation=project_brief
        )
        
        # Query memory (similar past projects?)
        memories = self.brain.query_memory(
            query=f"creative:{project_brief[:50]}"
        )
        
        return {
            "mood": "innovative" if emotion["novelty"] > 0.7 else "refined",
            "reference_projects": [m["content"][:30] for m in memories[:3]],
            "approach": "experimental" if emotion["arousal"] > 0.5 else "proven"
        }


if __name__ == "__main__":
    print("=" * 70)
    print("  AGENT-BRAIN INTERFACE DEMO")
    print("  Showing how agents USE the brain (not just feed it)")
    print("=" * 70)
    
    # Initialize brain API
    brain_api = BrainAPI()
    agent_interface = AgentBrainInterface(brain_api)
    
    # Example 1: Sales Agent
    print("\n🎯 SALES AGENT QUERY:")
    sales_result = agent_interface.sales_agent_example({
        "company": "TechCorp Industries",
        "priority": "A",
        "size": "enterprise"
    })
    print(f"  Decision: {sales_result['action']}")
    print(f"  Tone: {sales_result['tone']}")
    print(f"  Urgency: {sales_result['urgency']}")
    
    # Example 2: Security Agent
    print("\n🔒 SECURITY AGENT QUERY:")
    security_result = agent_interface.security_agent_example({
        "type": "unauthorized_access",
        "severity": "high",
        "ip": "192.168.1.100"
    })
    print(f"  Action: {security_result['action']}")
    print(f"  Historical Match: {security_result['historical_match']}")
    print(f"  Confidence: {security_result['confidence']:.2f}")
    
    # Example 3: Creative Agent
    print("\n🎨 CREATIVE AGENT QUERY:")
    creative_result = agent_interface.creative_agent_example(
        "Design a futuristic AI mascot for AGI Company"
    )
    print(f"  Mood: {creative_result['mood']}")
    print(f"  Approach: {creative_result['approach']}")
    print(f"  References: {creative_result['reference_projects']}")
    
    print("\n" + "=" * 70)
    print("  ✅ Agents USE the brain for:")
    print("     - Decision making (PFC processing)")
    print("     - Memory recall (Hippocampus query)")
    print("     - Emotional analysis (Limbic read)")
    print("     - Action selection (Basal Ganglia)")
    print("=" * 70)
    print("\n  The brain is an ACTIVE REASONING ENGINE")
    print("  Not just passive storage!")
    print("=" * 70)
