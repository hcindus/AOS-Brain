"""
AGENT MODEL ROUTER INTEGRATION v3.1
Quick integration for agents to access 8 models via Bonsai Bridge

Copy this file to any agent directory and import.
Usage:
    from agent_model_router import get_model_router
    
    router = get_model_router()
    
    # Decision making
    action, confidence = router.decide({"novelty": 0.8, "phase": "Explore"})
    
    # Voice/Chat
    response = router.speak("Hello", {"situation": "greeting"})
    
    # Other models
    analysis = router.reason("Explain quantum computing")
    code = router.code("Sort a list in Python", "python")
    answer = router.ask("What is the capital of France?")
    summary = router.analyze("Long text here...", "summarize")
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/agents/shared')

try:
    from model_router_client import ModelRouterClient
    _ROUTER = None
    
    def get_model_router(host: str = "127.0.0.1", port: int = 11435):
        """Get or create singleton Model Router client"""
        global _ROUTER
        if _ROUTER is None:
            _ROUTER = ModelRouterClient(host=host, port=port)
        return _ROUTER
    
    def check_router_status():
        """Quick status check of Model Router"""
        router = get_model_router()
        return router.get_status()
    
    MODEL_ROUTER_AVAILABLE = True
    
except ImportError:
    MODEL_ROUTER_AVAILABLE = False
    
    def get_model_router(*args, **kwargs):
        """Fallback when Model Router unavailable"""
        class DummyRouter:
            def decide(self, *a, **k): return "CONTINUE", 0.5
            def speak(self, *a, **k): return "[Router offline]"
            def reason(self, *a, **k): return "[Router offline]"
            def code(self, *a, **k): return "[Router offline]"
            def ask(self, *a, **k): return "[Router offline]"
            def analyze(self, *a, **k): return "[Router offline]"
            def get_status(self): return {"status": "unavailable"}
        return DummyRouter()
    
    def check_router_status():
        return {"status": "unavailable", "error": "model_router_client.py not found"}


# Self-test
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 AGENT MODEL ROUTER INTEGRATION TEST")
    print("=" * 60)
    
    router = get_model_router()
    status = router.get_status()
    
    print(f"\nStatus: {status['status']}")
    if status.get('status') == 'connected':
        print(f"Models Available: {status.get('models_available', 0)}")
        print("\n✅ Model Router ready for agents!")
        print("\nAvailable Methods:")
        print("  - router.decide(context)       → Bonsai/tinyllama")
        print("  - router.speak(msg, context)   → Mort_II")
        print("  - router.reason(prompt)        → qwen2.5:14b")
        print("  - router.code(prompt, lang)    → phi3:medium")
        print("  - router.ask(question)         → llama3.1:latest")
        print("  - router.analyze(text, task)   → mistral:latest")
    else:
        print(f"⚠️  Router unavailable: {status.get('error', 'unknown error')}")
    
    print("\n" + "=" * 60)
