#!/usr/bin/env python3
"""
Quick model comparison - one test per model
"""

import requests
import time

# Simple decision test
TEST = {
    "name": "High Novelty Decision",
    "novelty": 0.85, 
    "reward": 0.4, 
    "phase": "Observe",
    "expected": "EXPLORE"
}

PROMPT = f"""Choose ONE word: EXPLORE, EXPLOIT, REST, or CONTINUE

Novelty: {TEST['novelty']}
Reward: {TEST['reward']}
Phase: {TEST['phase']}

DECISION:"""

MODELS = ["phi3:latest", "qwen2.5:3b", "tinyllama:latest", "antoniohudnall/Mortimer:latest"]

print("=" * 60)
print("  ⚡ QUICK MODEL COMPARISON")
print("=" * 60)
print(f"\nTest: {TEST['name']}")
print(f"Expected: {TEST['expected']}")
print(f"\nPrompt: {PROMPT[:80]}...")

for model in MODELS:
    print(f"\n{'='*60}")
    print(f"  Testing: {model}")
    print(f"{'='*60}")
    
    try:
        start = time.time()
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": PROMPT,
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 10}
            },
            timeout=45
        )
        latency = (time.time() - start) * 1000
        
        if resp.status_code == 200:
            text = resp.json().get("response", "").strip().upper()
            
            # Parse action
            actions = ["EXPLORE", "EXPLOIT", "REST", "CONTINUE"]
            found = [a for a in actions if a in text]
            action = found[0] if found else "PARSE_FAIL"
            
            correct = "✅" if action == TEST['expected'] else "❌"
            
            print(f"    Response: '{text}'")
            print(f"    Parsed: {action} {correct}")
            print(f"    Latency: {latency:.0f}ms")
        else:
            print(f"    ❌ HTTP {resp.status_code}")
    except Exception as e:
        print(f"    ❌ Error: {str(e)[:50]}")

print("\n" + "=" * 60)
print("  ✅ Comparison Complete")
print("=" * 60)
