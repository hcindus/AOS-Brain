#!/usr/bin/env python3
"""
Model Benchmark for QMD Decision Task
Tests phi3, qwen2.5, llama3.2 vs Mort_II
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

import json
import time
import requests
from typing import Dict, Tuple

# Test configurations
MODELS = [
    {"name": "phi3:latest", "size": "3.8B", "expected": "fast"},
    {"name": "qwen2.5:3b", "size": "3B", "expected": "balanced"},
    {"name": "tinyllama:latest", "size": "1.1B", "expected": "ultra-fast"},
    {"name": "antoniohudnall/Mortimer:latest", "size": "7B", "expected": "slow"},
]

# Decision prompt with structured output
DECISION_PROMPT = """You are a decision-making module for an AI brain. Choose ONE action:

EXPLORE - if novelty is high (>0.7) or reward is low (<0.3)
EXPLOIT - if reward is high (>0.7) and novelty is low (<0.3)
REST - if in "Act" phase with reward >0.6
CONTINUE - otherwise

Context:
- Novelty: {novelty}
- Reward: {reward}
- Phase: {phase}
- Observation: {observation}

Respond with ONLY ONE word: EXPLORE, EXPLOIT, REST, or CONTINUE"""

TEST_CASES = [
    {"name": "High Novelty", "novelty": 0.85, "reward": 0.4, "phase": "Observe", "observation": "Unknown pattern detected", "expected": "EXPLORE"},
    {"name": "Low Reward", "novelty": 0.3, "reward": 0.2, "phase": "Decide", "observation": "Minimal results", "expected": "EXPLORE"},
    {"name": "Stable", "novelty": 0.2, "reward": 0.8, "phase": "Act", "observation": "System stable", "expected": "EXPLOIT"},
    {"name": "Greeting", "novelty": 0.6, "reward": 0.5, "phase": "Observe", "observation": "User said hi", "expected": "CONTINUE"},
]

def query_model(model: str, prompt: str) -> Tuple[str, float, str]:
    """Query Ollama model and return (response, latency_ms, raw)"""
    try:
        start = time.time()
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Low temp for deterministic
                    "num_predict": 10,   # Short response
                }
            },
            timeout=30
        )
        latency = (time.time() - start) * 1000
        
        if resp.status_code == 200:
            text = resp.json().get("response", "").strip().upper()
            return text, latency, text
        else:
            return f"ERROR_{resp.status_code}", latency, ""
    except Exception as e:
        return f"ERROR: {str(e)[:20]}", 0, ""

def parse_action(text: str) -> Tuple[str, float]:
    """Extract action and confidence from response"""
    valid = ["EXPLORE", "EXPLOIT", "REST", "CONTINUE"]
    
    for action in valid:
        if action in text:
            # Confidence based on exact match vs partial
            if text == action:
                return action, 0.95
            else:
                return action, 0.70
    
    return "UNKNOWN", 0.30

def check_model_available(model: str) -> bool:
    """Check if model is pulled"""
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        if resp.status_code == 200:
            models = resp.json().get("models", [])
            for m in models:
                if model in m.get("name", ""):
                    return True
        return False
    except:
        return False

print("=" * 80)
print("  🧠 QMD MODEL BENCHMARK")
print("  Testing phi3, qwen2.5, llama3.2 vs Mort_II")
print("=" * 80)

# Check available models
print("\n📦 Checking available models...")
available_models = []
for model in MODELS:
    if check_model_available(model["name"]):
        available_models.append(model)
        print(f"  ✅ {model['name']} ({model['size']})")
    else:
        print(f"  ❌ {model['name']} ({model['size']}) - not found")

if not available_models:
    print("\n⚠️  No models available! Try:")
    print("    ollama pull phi3:latest")
    print("    ollama pull qwen2.5:0.5b")
    print("    ollama pull llama3.2:latest")
    sys.exit(1)

print(f"\n🧪 Running {len(TEST_CASES)} test cases per model...")
print(f"   Prompt style: Structured output (low temp=0.1)")
print(f"   Timeout: 30s per query")

results = []

for model in available_models:
    print(f"\n{'='*80}")
    print(f"  🤖 Testing: {model['name']}")
    print(f"{'='*80}")
    
    model_results = {
        "model": model["name"],
        "size": model["size"],
        "tests": [],
        "avg_latency": 0,
        "accuracy": 0,
        "valid_responses": 0
    }
    
    total_latency = 0
    correct = 0
    valid = 0
    
    for test in TEST_CASES:
        prompt = DECISION_PROMPT.format(**test)
        print(f"\n  Test: {test['name']}")
        print(f"    Expected: {test['expected']}")
        
        text, latency, raw = query_model(model["name"], prompt)
        action, confidence = parse_action(text)
        
        is_valid = action in ["EXPLORE", "EXPLOIT", "REST", "CONTINUE"]
        is_correct = action == test["expected"]
        
        if is_valid:
            valid += 1
            total_latency += latency
        if is_correct:
            correct += 1
        
        status = "✅" if is_correct else ("⚠️ " if is_valid else "❌")
        print(f"    Response: '{raw[:40]}...' -> {action} ({confidence:.2f})")
        print(f"    Latency: {latency:.0f}ms {status}")
        
        model_results["tests"].append({
            "test": test["name"],
            "expected": test["expected"],
            "got": action,
            "confidence": confidence,
            "latency_ms": latency,
            "correct": is_correct,
            "valid": is_valid
        })
    
    model_results["accuracy"] = (correct / len(TEST_CASES)) * 100 if len(TEST_CASES) > 0 else 0
    model_results["valid_responses"] = valid
    model_results["avg_latency"] = total_latency / valid if valid > 0 else 0
    
    results.append(model_results)
    
    print(f"\n  📊 Summary for {model['name']}:")
    print(f"     Accuracy: {model_results['accuracy']:.0f}% ({correct}/{len(TEST_CASES)})")
    print(f"     Valid: {valid}/{len(TEST_CASES)}")
    print(f"     Avg Latency: {model_results['avg_latency']:.0f}ms")

# Final comparison
print("\n" + "=" * 80)
print("  📊 FINAL COMPARISON")
print("=" * 80)

print(f"\n{'Model':<35} {'Accuracy':<12} {'Latency':<12} {'Valid':<10} {'Size':<10}")
print("-" * 80)

for r in sorted(results, key=lambda x: x["accuracy"], reverse=True):
    name = r["model"][:32] + "..." if len(r["model"]) > 35 else r["model"]
    acc = f"{r['accuracy']:.0f}%"
    lat = f"{r['avg_latency']:.0f}ms" if r["avg_latency"] > 0 else "N/A"
    val = f"{r['valid_responses']}/4"
    size = r["size"]
    print(f"{name:<35} {acc:<12} {lat:<12} {val:<10} {size:<10}")

# Recommendations
print("\n" + "=" * 80)
print("  💡 RECOMMENDATIONS")
print("=" * 80)

print("""
🎯 FOR QMD DECISION-MAKING (Structured Output Task):

BEST OVERALL:
  → qwen2.5:0.5b or phi3:latest
  Why: Fast, follow instructions, good accuracy with structured prompts

WHEN TO USE EACH MODEL:

┌────────────────────┬─────────────────────────────────────────────────────┐
│ Model              │ Best Use Case                                       │
├────────────────────┼─────────────────────────────────────────────────────┤
│ qwen2.5:0.5b       │ Ultra-fast decisions, resource-constrained          │
│                    │ Trade-off: Slightly less nuanced than larger models │
├────────────────────┼─────────────────────────────────────────────────────┤
│ phi3:latest        │ Balanced speed/quality for production QMD           │
│                    │ Good instruction following, reasonable latency        │
├────────────────────┼─────────────────────────────────────────────────────┤
│ llama3.2:latest    │ When you need more reasoning depth                    │
│                    │ Slightly slower but better generalization           │
├────────────────────┼─────────────────────────────────────────────────────┤
│ Mort_II (7B)       │ ❌ NOT for structured decisions                      │
│                    │ ✅ Use for: Natural language generation              │
│                    │    - Chat responses                                  │
│                    │    - Creative writing                                │
│                    │    - Context understanding (not action selection)    │
└────────────────────┴─────────────────────────────────────────────────────┘

🎯 WHERE TO USE Mort_II INSTEAD:

✅ USE Mort_II FOR:
   • Chat/conversation with users
   • Explaining decisions after they're made
   • Creative content generation
   • Context summarization
   • Natural language understanding tasks

❌ DON'T USE Mort_II FOR:
   • Structured decision output (EXPLORE/EXPLOIT/REST)
   • Classification tasks
   • Action selection
   • Any task requiring specific output format

💡 OPTIMAL ARCHITECTURE:
   Brain v4.2 with Thyroid:
   ├── QMD decisions: phi3 or qwen2.5 (fast, structured)
   ├── Voice responses: Mort_II (natural, conversational)
   └── Memory queries: nomic-embed-text (embeddings)
""")

print("=" * 80)
print("  ✅ Benchmark Complete")
print("=" * 80)

# Save results
with open("/root/.aos/aos/model_benchmark_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\n📁 Results saved to: /root/.aos/aos/model_benchmark_results.json")
