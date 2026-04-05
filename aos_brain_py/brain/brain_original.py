# brain/brain_original.py
"""
Original NN OODA brain - now powered by shared Cortex.
"""

from typing import Dict, Any
from brain.cortex import Cortex


class OriginalOodaBrain:
    """
    Original OODA loop with neural network style processing.
    Uses shared TinyLlama/Qwen cortex.
    """
    
    def __init__(self, model_path: str, use_qwen: bool = False):
        self.cortex = Cortex(model_path, use_qwen=use_qwen)
        self.tick_count = 0
        
    def observe(self, input_data: str) -> str:
        """Observation stage - capture raw input."""
        return input_data
    
    def orient(self, observation: str) -> str:
        """Orientation stage - analyze and contextualize."""
        prompt = f"""You are the orientation stage of an OODA loop.
Analyze this observation and highlight key factors, patterns, and context.

Observation: {observation}

Provide a concise orientation analysis:"""
        
        return self.cortex.activate(prompt, max_tokens=200)
    
    def decide(self, orientation: str) -> str:
        """Decision stage - choose action based on orientation."""
        prompt = f"""You are the decision stage of an OODA loop.
Based on this orientation analysis, decide the best next action.

Orientation: {orientation}

Decide and explain your reasoning:"""
        
        return self.cortex.activate(prompt, max_tokens=150)
    
    def act(self, decision: str) -> str:
        """Action stage - execute the decision."""
        # In this brain, action is the decision output
        # In a real system, this would trigger actual actions
        return decision
    
    def ooda(self, input_data: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Full OODA loop cycle.
        
        Returns complete trace of the cognitive process.
        """
        self.tick_count += 1
        
        # OODA stages
        obs = self.observe(input_data)
        ori = self.orient(obs)
        dec = self.decide(ori)
        act = self.act(dec)
        
        return {
            "tick": self.tick_count,
            "observation": obs,
            "orientation": ori,
            "decision": dec,
            "action": act,
            "brain_type": "original_ooda",
        }
