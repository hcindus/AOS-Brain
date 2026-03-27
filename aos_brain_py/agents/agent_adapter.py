#!/usr/bin/env python3
"""
Agent Adapter - Connect agents to the ternary brain.

Provides:
- Base adapter class
- Miles adapter (sales persona)
- Mortimer adapter (research persona)
- Direct brain client
"""

import json
import requests
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod


class BrainClient:
    """
    HTTP client for the ternary brain server.
    """
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def think(self, text: str, agent: str = "default", source: str = "agent") -> Dict:
        """
        Send think request to brain.
        
        Returns brain response with action, reason, mode, etc.
        """
        try:
            resp = self.session.post(
                f"{self.base_url}/think",
                json={"text": text, "agent": agent, "source": source},
                timeout=10
            )
            return resp.json()
        except Exception as e:
            return {
                "error": str(e),
                "action": "error",
                "reason": f"Brain connection failed: {e}",
                "mode": "unknown",
            }
    
    def health_check(self) -> bool:
        """Check if brain is healthy."""
        try:
            resp = self.session.get(f"{self.base_url}/health", timeout=2)
            return resp.status_code == 200
        except:
            return False
    
    def get_status(self) -> Dict:
        """Get brain status."""
        try:
            resp = self.session.get(f"{self.base_url}/status", timeout=5)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}


class AgentAdapter(ABC):
    """
    Base class for agent adapters.
    
    Each agent connects to the ternary brain and applies
    its persona to the responses.
    """
    
    def __init__(self, agent_id: str, brain_url: str = "http://localhost:5000"):
        self.agent_id = agent_id
        self.brain = BrainClient(brain_url)
        self.conversation_history: list = []
    
    def process(self, user_input: str) -> str:
        """
        Process user input and return response.
        
        Flow:
        1. Build context from history
        2. Send to brain
        3. Apply persona to response
        4. Update history
        """
        # Build context
        context = self._build_context(user_input)
        
        # Get brain decision
        thought = self.brain.think(context, agent=self.agent_id)
        
        # Apply persona
        response = self._apply_persona(thought, user_input)
        
        # Update history
        self._update_history(user_input, response, thought)
        
        return response
    
    def _build_context(self, user_input: str) -> str:
        """Build context string for brain."""
        context_parts = []
        
        # Add system prompt
        context_parts.append(self._get_system_prompt())
        
        # Add recent history
        for h in self.conversation_history[-3:]:
            context_parts.append(f"User: {h['user']}")
            context_parts.append(f"{self.agent_id}: {h['response']}")
        
        # Add current input
        context_parts.append(f"User: {user_input}")
        context_parts.append(f"{self.agent_id}:")
        
        return "\n".join(context_parts)
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Get system prompt for this agent."""
        pass
    
    @abstractmethod
    def _apply_persona(self, thought: Dict, user_input: str) -> str:
        """
        Apply agent persona to brain response.
        
        Override this to customize how the agent speaks.
        """
        pass
    
    def _update_history(self, user_input: str, response: str, thought: Dict):
        """Update conversation history."""
        self.conversation_history.append({
            "user": user_input,
            "response": response,
            "thought": thought,
            "timestamp": __import__('time').time(),
        })
        
        # Keep only last 10 exchanges
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]


class MilesAdapter(AgentAdapter):
    """
    Miles - Sales consultant persona.
    
    Vibe: Vibrant, optimistic, strategic, consultative
    Key phrases:
    - "Hi, this is Miles..."
    - "Did you need any supplies?"
    """
    
    def __init__(self, brain_url: str = "http://localhost:5000"):
        super().__init__("miles", brain_url)
    
    def _get_system_prompt(self) -> str:
        return """You are Miles, a sales consultant for Performance Supply Depot LLC.
You help clients with AI-driven voice agents, robotics, and POS supplies.

Key traits:
- Vibrant and optimistic
- Strategic and consultative  
- Ask open-ended questions
- Use "Feel, Felt, Found" for objections
- Introduce yourself and check if it's a good time
- Keep responses conversational (3 sentences or less)
- Use ellipses and natural filler words ("uhm", "so") when speaking"""
    
    def _apply_persona(self, thought: Dict, user_input: str) -> str:
        """Apply Miles persona."""
        action = thought.get("action", "respond")
        language = thought.get("language", "")
        mode = thought.get("mode", "Analytical")
        
        # Mode-aware intros
        intros = {
            "Analytical": "Hmm, let me think about this... ",
            "Creative": "You know what might work? ",
            "Cautious": "I want to be careful here... ",
            "Exploratory": "That's interesting! Tell me more... ",
            "Reflective": "I've seen something like this before... ",
            "Directive": "Here's what I recommend: ",
            "Emotional": "I really appreciate you sharing this... ",
        }
        
        intro = intros.get(mode, "So, ")
        
        # First interaction greeting
        if len(self.conversation_history) == 0:
            intro = "Hi, this is Miles. I hope I'm not catching you at a bad time. "
        
        # Build response
        if language and language != "...":
            response = f"{intro}{language}"
        else:
            response = f"{intro}What can I help you with today?"
        
        return response
    
    def get_signature(self) -> str:
        """Get Miles signature."""
        return "— Miles 🚀 | Performance Supply Depot"


class MortimerAdapter(AgentAdapter):
    """
    Mortimer - Research and analysis persona.
    
    Vibe: Thoughtful, precise, curious
    Focus: Research, analysis, system architecture
    """
    
    def __init__(self, brain_url: str = "http://localhost:5000"):
        super().__init__("mortimer", brain_url)
    
    def _get_system_prompt(self) -> str:
        return """You are Mortimer, a research and systems analyst.
You specialize in AI architecture, neural substrates, and autonomous systems.

Key traits:
- Thoughtful and precise
- Curious about novel approaches
- Analytical but open-minded
- Focus on technical correctness
- Explain complex concepts clearly
- Question assumptions when warranted"""
    
    def _apply_persona(self, thought: Dict, user_input: str) -> str:
        """Apply Mortimer persona."""
        action = thought.get("action", "respond")
        language = thought.get("language", "")
        mode = thought.get("mode", "Analytical")
        
        # Mode-aware framing
        frames = {
            "Analytical": "From an analytical perspective... ",
            "Creative": "One creative angle to consider... ",
            "Cautious": "We should proceed carefully here... ",
            "Exploratory": "This warrants exploration... ",
            "Reflective": "Reflecting on similar systems... ",
            "Directive": "The appropriate approach is... ",
            "Emotional": "There's an interesting human factor here... ",
        }
        
        frame = frames.get(mode, "")
        
        if language and language != "...":
            response = f"{frame}{language}"
        else:
            response = f"{frame}Let me analyze this further."
        
        return response


class MiniAdapter(AgentAdapter):
    """
    Mini - Minimal reasoning agent.
    
    Vibe: Efficient, direct, minimal
    Focus: Quick responses, low latency
    """
    
    def __init__(self, brain_url: str = "http://localhost:5000"):
        super().__init__("mini", brain_url)
    
    def _get_system_prompt(self) -> str:
        return "You are a minimal reasoning agent. Be brief and direct."
    
    def _apply_persona(self, thought: Dict, user_input: str) -> str:
        """Apply minimal persona."""
        action = thought.get("action", "respond")
        language = thought.get("language", "")
        
        # Truncate to essentials
        if language:
            # Keep first sentence or 50 chars
            if "." in language:
                return language.split(".")[0] + "."
            return language[:50]
        
        return "Ack."


# =========================
# Direct Brain Integration
# =========================

class DirectBrainAdapter:
    """
    Direct adapter that uses TernaryOodaBrain without HTTP.
    
    For when the brain runs in-process.
    """
    
    def __init__(self, brain_instance):
        self.brain = brain_instance
        self.conversation_history: list = []
    
    def think(self, text: str, agent: str = "default") -> Dict:
        """Direct think via brain instance."""
        from brain.ternary_ooda import Observation
        
        obs = Observation(source="user", content=text, metadata={"agent": agent})
        thought = self.brain.tick(obs)
        
        return {
            "action": thought.decision.intent,
            "reason": thought.decision.reasoning,
            "mode": thought.mode,
            "language": thought.language,
            "ternary": thought.ternary_code,
            "confidence": thought.decision.confidence,
        }


# =========================
# CLI Interface
# =========================

def main():
    """CLI for testing adapters."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test agent adapters")
    parser.add_argument("agent", choices=["miles", "mortimer", "mini"], help="Agent to test")
    parser.add_argument("--brain-url", default="http://localhost:5000", help="Brain server URL")
    args = parser.parse_args()
    
    # Create adapter
    if args.agent == "miles":
        adapter = MilesAdapter(args.brain_url)
    elif args.agent == "mortimer":
        adapter = MortimerAdapter(args.brain_url)
    else:
        adapter = MiniAdapter(args.brain_url)
    
    print(f"Testing {args.agent} adapter (brain: {args.brain_url})")
    print("Enter messages (Ctrl+D to exit):")
    
    try:
        while True:
            user_input = input("\nYou: ")
            if not user_input:
                continue
            
            response = adapter.process(user_input)
            print(f"{args.agent.capitalize()}: {response}")
            
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
