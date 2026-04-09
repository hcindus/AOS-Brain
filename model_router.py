#!/usr/bin/env python3
"""
AOS Model Router v1.0
Routes different tasks to optimal models:
  - Decisions: tinyllama (fast, structured)
  - Voice/Chat: Mort_II (natural, conversational)
  - Embeddings: nomic-embed-text
"""

import requests
import time
from typing import Dict, Tuple


class AOSModelRouter:
    """
    Intelligent model selection for different task types
    Like the Thyroid but for model choice, not mode
    """
    
    MODELS = {
        "decision": "tinyllama:latest",      # Fast, structured output
        "voice": "antoniohudnall/Mort_II:latest",  # Natural conversation
        "embedding": "nomic-embed-text:latest",    # Vector embeddings
        "reasoning": "qwen2.5:3b",           # Complex reasoning
    }
    
    def __init__(self):
        self.stats = {
            "decision": {"calls": 0, "avg_latency": 0},
            "voice": {"calls": 0, "avg_latency": 0},
            "embedding": {"calls": 0, "avg_latency": 0},
        }
        print("[ModelRouter] Initialized")
        print(f"  Decision: {self.MODELS['decision']}")
        print(f"  Voice: {self.MODELS['voice']}")
        print(f"  Embedding: {self.MODELS['embedding']}")
    
    def decide(self, context: Dict) -> Tuple[str, float]:
        """Make a decision using tinyllama"""
        model = self.MODELS["decision"]
        
        prompt = self._format_decision_prompt(context)
        
        start = time.time()
        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 15
                    }
                },
                timeout=10
            )
            latency = (time.time() - start) * 1000
            
            if resp.status_code == 200:
                text = resp.json().get("response", "").strip().upper()
                action, confidence = self._parse_action(text)
                
                self._update_stats("decision", latency)
                return action, confidence
            else:
                return "ERROR", 0.0
        except Exception as e:
            return f"ERROR: {str(e)[:20]}", 0.0
    
    def speak(self, message: str, context: Dict = None) -> str:
        """Generate natural voice response using Mort_II"""
        model = self.MODELS["voice"]
        
        prompt = f"""You are a helpful AI assistant. Respond naturally and conversationally.

Context: {context.get('situation', 'general') if context else 'general'}
Message to respond to: {message}

Your response:"""
        
        start = time.time()
        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 100
                    }
                },
                timeout=15
            )
            latency = (time.time() - start) * 1000
            
            if resp.status_code == 200:
                text = resp.json().get("response", "").strip()
                self._update_stats("voice", latency)
                return text
            else:
                return f"[Voice error: HTTP {resp.status_code}]"
        except Exception as e:
            return f"[Voice error: {str(e)[:30]}]"
    
    def _format_decision_prompt(self, context: Dict) -> str:
        """Format context for decision model"""
        return f"""Choose ONE word: EXPLORE, EXPLOIT, REST, or CONTINUE

Novelty: {context.get('novelty', 0.5):.2f}
Reward: {context.get('reward', 0.5):.2f}
Phase: {context.get('phase', 'unknown')}
Observation: {context.get('observation', 'none')[:50]}

DECISION:"""
    
    def _parse_action(self, text: str) -> Tuple[str, float]:
        """Extract action from model response"""
        actions = ["EXPLORE", "EXPLOIT", "REST", "CONTINUE"]
        text_upper = text.upper()
        
        for action in actions:
            if action in text_upper:
                # Check if it's a clean match
                if text_upper.startswith(action) or text_upper == action:
                    return action, 0.95
                else:
                    return action, 0.75
        
        return "CONTINUE", 0.30
    
    def _update_stats(self, task_type: str, latency: float):
        """Update latency stats"""
        self.stats[task_type]["calls"] += 1
        n = self.stats[task_type]["calls"]
        old_avg = self.stats[task_type]["avg_latency"]
        self.stats[task_type]["avg_latency"] = (old_avg * (n-1) + latency) / n
    
    def get_stats(self) -> Dict:
        """Get router statistics"""
        return self.stats


# Test function
def test_model_router():
    """Test the model router"""
    print("=" * 70)
    print("  🧠 AOS MODEL ROUTER TEST")
    print("  tinyllama → decisions, Mort_II → voice")
    print("=" * 70)
    
    router = AOSModelRouter()
    
    # Test 1: Decision making
    print("\n" + "=" * 70)
    print("  TEST 1: Decision Making (tinyllama)")
    print("=" * 70)
    
    test_decisions = [
        {"novelty": 0.85, "reward": 0.4, "phase": "Observe", "observation": "Unknown pattern", "expected": "EXPLORE"},
        {"novelty": 0.2, "reward": 0.8, "phase": "Act", "observation": "System stable", "expected": "EXPLOIT"},
        {"novelty": 0.6, "reward": 0.5, "phase": "Decide", "observation": "User greeting", "expected": "CONTINUE"},
    ]
    
    for test in test_decisions:
        print(f"\n  Scenario: {test['observation']}")
        print(f"    Expected: {test['expected']}")
        
        action, confidence = router.decide(test)
        
        match = "✅" if action == test['expected'] else "❌"
        print(f"    Result: {action} (confidence: {confidence:.2f}) {match}")
    
    # Test 2: Voice generation
    print("\n" + "=" * 70)
    print("  TEST 2: Voice Generation (Mort_II)")
    print("=" * 70)
    
    voice_tests = [
        {"message": "Hello, how are you?", "context": {"situation": "greeting"}},
        {"message": "The system is now operational.", "context": {"situation": "status_update"}},
    ]
    
    for test in voice_tests:
        print(f"\n  Input: '{test['message']}'")
        
        response = router.speak(test['message'], test['context'])
        
        print(f"    Response: '{response[:80]}...'")
    
    # Summary
    print("\n" + "=" * 70)
    print("  📊 ROUTER STATISTICS")
    print("=" * 70)
    
    stats = router.get_stats()
    for task_type, data in stats.items():
        if data["calls"] > 0:
            print(f"\n  {task_type.upper()}:")
            print(f"    Calls: {data['calls']}")
            print(f"    Avg Latency: {data['avg_latency']:.0f}ms")
    
    print("\n" + "=" * 70)
    print("  ✅ Model Router Test Complete")
    print("=" * 70)
    print("\n  Integration with Thyroid:")
    print("    Thyroid decides WHEN to use LLM (LOCAL vs OLLAMA)")
    print("    ModelRouter decides WHICH LLM to use")
    print("    → Optimal decisions + Natural voice")


if __name__ == "__main__":
    test_model_router()
