"""
Ternary Brain Client for Agents
Provides access to the Ternary Brain (Bonsai GGUF + Quantum Dice)
"""

import urllib.request
import json


class TernaryClient:
    """
    Client for accessing Ternary Brain services.
    
    Usage:
        brain = TernaryClient()
        response = brain.think("Hello")
        result = brain.dice.roll(["A", "B", "C"])
    """
    
    BRIDGE_URL = "http://localhost:11435"
    
    def __init__(self, bridge_url=None):
        self.bridge_url = bridge_url or self.BRIDGE_URL
    
    def think(self, prompt, max_tokens=100, temperature=0.7):
        """
        Send a prompt to the Ternary Brain (Bonsai).
        
        Args:
            prompt: Input text
            max_tokens: Max tokens to generate
            temperature: Creativity (0.0-1.0)
            
        Returns:
            dict: {"response": "...", "source": "prism|ollama", ...}
        """
        payload = json.dumps({
            "prompt": prompt,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }).encode()
        
        try:
            req = urllib.request.Request(
                f"{self.bridge_url}/api/generate",
                data=payload,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.loads(response.read())
        except Exception as e:
            return {"error": str(e), "source": "failed"}
    
    def chat(self, message, max_tokens=100, temperature=0.7):
        """
        Chat with the Ternary Brain.
        
        Args:
            message: User message
            max_tokens: Max tokens
            temperature: Creativity
            
        Returns:
            dict: {"message": {"role": "assistant", "content": "..."}}
        """
        payload = json.dumps({
            "messages": [{"role": "user", "content": message}],
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }).encode()
        
        try:
            req = urllib.request.Request(
                f"{self.bridge_url}/api/chat",
                data=payload,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.loads(response.read())
        except Exception as e:
            return {"error": str(e)}
    
    @property
    def dice(self):
        """Access Quantum Dice."""
        return TernaryDice(self.bridge_url)
    
    def get_status(self):
        """Get brain status."""
        try:
            req = urllib.request.Request(f"{self.bridge_url}/api/status")
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read())
        except Exception as e:
            return {"error": str(e)}


class TernaryDice:
    """Quantum Dice client."""
    
    def __init__(self, bridge_url):
        self.bridge_url = bridge_url
    
    def roll(self, options):
        """
        Pure quantum random selection.
        
        Args:
            options: List of options to choose from
            
        Returns:
            dict: {"type": "roll", "result": {"A": 25.1, "B": 24.6, "C": 23.9}}
        """
        payload = json.dumps({
            "mode": "roll",
            "options": options
        }).encode()
        
        try:
            req = urllib.request.Request(
                f"{self.bridge_url}/api/dice",
                data=payload,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read())
        except Exception as e:
            return {"error": str(e)}
    
    def consult(self, question, options, gut=None):
        """
        Consult quantum dice with a gut feeling.
        
        Args:
            question: Question to ask
            options: Options to choose from
            gut: Index of gut feeling (0-indexed)
            
        Returns:
            dict: Probability distribution + recommendation
        """
        payload = json.dumps({
            "mode": "consult",
            "question": question,
            "options": options,
            "gut": gut
        }).encode()
        
        try:
            req = urllib.request.Request(
                f"{self.bridge_url}/api/dice",
                data=payload,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read())
        except Exception as e:
            return {"error": str(e)}
    
    def oracle(self, question, options):
        """
        Oracle mode - deep quantum exploration.
        """
        payload = json.dumps({
            "mode": "oracle",
            "question": question,
            "options": options
        }).encode()
        
        try:
            req = urllib.request.Request(
                f"{self.bridge_url}/api/dice",
                data=payload,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read())
        except Exception as e:
            return {"error": str(e)}


# Quick test
if __name__ == "__main__":
    print("🧠 Testing Ternary Client...")
    
    brain = TernaryClient()
    
    # Test status
    print("\n📊 Status:")
    status = brain.get_status()
    print(f"   Operational: {status.get('ternary', {}).get('operational')}")
    
    # Test Dice
    print("\n🎲 Dice Roll:")
    result = brain.dice.roll(["Attack", "Defend", "Flee"])
    print(f"   Result: {result.get('result')}")
    
    # Test Consult
    print("\n🔮 Dice Consult (gut=0):")
    result = brain.dice.consult("Priority?", ["Attack", "Defend", "Flee"], gut=0)
    print(f"   Recommendation: {result.get('recommendation')}")
    print(f"   Distribution: {result.get('result')}")
    
    print("\n✅ Ternary Client ready for agents!")