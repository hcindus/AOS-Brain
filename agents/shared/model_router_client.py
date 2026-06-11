"""Aurora Lite v3.1 - Model Router Integration Patch
Adds Bonsai/tinyllama/Mort_II support via Model Router"""

import json
import time
import requests
from typing import Dict, Tuple, Optional

class ModelRouterClient:
    """Client for AOS Model Router (Bonsai Bridge on port 11435)"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 11435):
        self.base_url = f"http://{host}:{port}"
        self.models = {
            "decision": "bonsai-8b-q1_0:latest",
            "decision_fallback": "tinyllama:latest",
            "voice": "antoniohudnall/Mort_II:latest",
            "embedding": "nomic-embed-text:latest",
            "reasoning": "qwen2.5:14b",
            "coding": "phi3:medium",
            "general": "llama3.1:latest",
            "mixture": "mistral:latest"
        }
    
    def decide(self, context: Dict) -> Tuple[str, float]:
        """Make decision using Bonsai (fallback to tinyllama)"""
        model = self.models["decision"]
        prompt = self._format_decision_prompt(context)
        
        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1, "num_predict": 15}
                },
                timeout=60
            )
            
            if resp.status_code == 200:
                text = resp.json().get("response", "").strip().upper()
                action, confidence = self._parse_action(text)
                return action, confidence
            else:
                # Fallback
                return self._decide_fallback(context)
                
        except Exception as e:
            return self._decide_fallback(context)
    
    def _decide_fallback(self, context: Dict) -> Tuple[str, float]:
        """Fallback to tinyllama"""
        model = self.models["decision_fallback"]
        prompt = self._format_decision_prompt(context)
        
        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1, "num_predict": 15}
                },
                timeout=10
            )
            
            if resp.status_code == 200:
                text = resp.json().get("response", "").strip().upper()
                action, confidence = self._parse_action(text)
                return f"{action} (fallback)", confidence
            return "ERROR", 0.0
        except:
            return "ERROR", 0.0
    
    def speak(self, message: str, context: Dict = None) -> str:
        """Generate voice response using Mort_II"""
        model = self.models["voice"]
        
        prompt = f"""You are Aurora, a helpful AI assistant. Respond naturally.

Context: {context.get('situation', 'general') if context else 'general'}
Message: {message}

Your response:"""
        
        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 100}
                },
                timeout=15
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "").strip()
            return f"[Voice error: HTTP {resp.status_code}]"
        except Exception as e:
            return f"[Voice error: {str(e)[:30]}]"
    
    def get_status(self) -> Dict:
        """Get available models from bridge"""
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                return {
                    "status": "connected",
                    "models_available": len(models),
                    "model_names": [m["name"] for m in models[:5]]
                }
            return {"status": "error", "code": resp.status_code}
        except Exception as e:
            return {"status": "disconnected", "error": str(e)[:40]}
    
    def _format_decision_prompt(self, context: Dict) -> str:
        """Format context for decision model"""
        return f"""Choose ONE word: EXPLORE, EXPLOIT, REST, or CONTINUE

Novelty: {context.get('novelty', 0.5):.2f}
Reward: {context.get('reward', 0.5):.2f}
Phase: {context.get('phase', 'unknown')}
Observation: {context.get('observation', 'none')[:50]}

DECISION:"""
    
    def _parse_action(self, text: str) -> Tuple[str, float]:
        """Extract action from response"""
        actions = ["EXPLORE", "EXPLOIT", "REST", "CONTINUE"]
        text_upper = text.upper()
        
        for action in actions:
            if action in text_upper:
                confidence = 0.95 if text_upper.startswith(action) else 0.75
                return action, confidence
        
        return "CONTINUE", 0.30

    # ═══════════════════════════════════════════════════════════════════
    # EXTENDED MODEL METHODS (NEW v3.1 - 8 MODELS)
    # ═══════════════════════════════════════════════════════════════════
    
    def reason(self, prompt: str, max_tokens: int = 500) -> str:
        """Complex reasoning using qwen2.5:14b"""
        model = self.models["reasoning"]
        full_prompt = f"""Analyze this problem carefully and provide detailed reasoning:

{prompt}

Your detailed analysis:"""
        
        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": max_tokens}
                },
                timeout=30
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "").strip()
            return f"[Reasoning error: HTTP {resp.status_code}]"
        except Exception as e:
            return f"[Reasoning error: {str(e)[:30]}]"
    
    def code(self, prompt: str, language: str = "python", max_tokens: int = 300) -> str:
        """Code generation using phi3:medium"""
        model = self.models["coding"]
        full_prompt = f"""Generate {language} code for the following:

{prompt}

Your code:"""
        
        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {"temperature": 0.3, "num_predict": max_tokens}
                },
                timeout=20
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "").strip()
            return f"[Code error: HTTP {resp.status_code}]"
        except Exception as e:
            return f"[Code error: {str(e)[:30]}]"
    
    def ask(self, question: str, max_tokens: int = 200) -> str:
        """General questions using llama3.1:latest"""
        model = self.models["general"]
        full_prompt = f"""Answer the following question concisely:

{question}

Your answer:"""
        
        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": max_tokens}
                },
                timeout=15
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "").strip()
            return f"[Ask error: HTTP {resp.status_code}]"
        except Exception as e:
            return f"[Ask error: {str(e)[:30]}]"
    
    def analyze(self, text: str, task: str = "summarize", max_tokens: int = 300) -> str:
        """Analysis using mistral:latest (Mixture of Experts)"""
        model = self.models["mixture"]
        full_prompt = f"""{task.capitalize()} the following text:

{text}

Your {task}:"""
        
        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {"temperature": 0.5, "num_predict": max_tokens}
                },
                timeout=20
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "").strip()
            return f"[Analyze error: HTTP {resp.status_code}]"
        except Exception as e:
            return f"[Analyze error: {str(e)[:30]}]"


# Test function
def test_model_router():
    """Test Model Router client"""
    print("=" * 60)
    print("🧠 AURORA MODEL ROUTER TEST")
    print("=" * 60)
    
    client = ModelRouterClient()
    
    # Status check
    print("\n1. Bridge Status:")
    status = client.get_status()
    print(f"   Status: {status['status']}")
    if 'models_available' in status:
        print(f"   Models: {status['models_available']} available")
    
    # Decision test
    print("\n2. Decision Test (Bonsai/tinyllama):")
    test_cases = [
        {"novelty": 0.9, "reward": 0.3, "phase": "Explore", "observation": "New pattern detected"},
        {"novelty": 0.2, "reward": 0.8, "phase": "Act", "observation": "System stable"},
    ]
    
    for ctx in test_cases:
        print(f"\n   Context: {ctx['observation']}")
        action, conf = client.decide(ctx)
        print(f"   Decision: {action} (confidence: {conf:.2f})")
        time.sleep(0.5)
    
    # Voice test
    print("\n3. Voice Test (Mort_II):")
    response = client.speak("Hello Aurora, system check complete.", {"situation": "status_report"})
    print(f"   Response: '{response[:80]}...'" if len(response) > 80 else f"   Response: '{response}'")
    
    print("\n" + "=" * 60)
    print("✅ Aurora Model Router Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    test_model_router()
