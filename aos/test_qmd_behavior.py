#!/usr/bin/env python3
"""
QMD Behavior Test: LOCAL vs OLLAMA
Shows how decisions change when the Thyroid coughs between modes
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

import json
import time
from qmd_loop import QMDLoop

print("=" * 70)
print("  🧠 QMD BEHAVIOR TEST: LOCAL vs OLLAMA")
print("=" * 70)

test_contexts = [
    {
        "name": "High Novelty Situation",
        "phase": "Observe",
        "observation": "Unknown pattern detected in environment",
        "limbic": {"novelty": 0.85, "reward": 0.4}
    },
    {
        "name": "Low Reward Recovery", 
        "phase": "Decide",
        "observation": "Previous action yielded minimal results",
        "limbic": {"novelty": 0.3, "reward": 0.2}
    },
    {
        "name": "Stable Exploitation",
        "phase": "Act", 
        "observation": "System stable, good rewards incoming",
        "limbic": {"novelty": 0.2, "reward": 0.8}
    },
    {
        "name": "Greeting Scenario",
        "phase": "Observe",
        "observation": "User said 'hi' to initiate interaction",
        "limbic": {"novelty": 0.6, "reward": 0.5}
    }
]

results = []

# Test LOCAL mode
print("\n" + "=" * 70)
print("  📍 TEST 1: LOCAL MODE (Rule-based decisions)")
print("=" * 70)

qmd_local = QMDLoop(use_ollama=False)
print(f"\nQMD initialized: {qmd_local.model}")
print(f"Mode: LOCAL (rule-based)")
print(f"Decision rules: {list(qmd_local.decision_rules.keys())}")

for ctx in test_contexts:
    print(f"\n--- {ctx['name']} ---")
    print(f"Context: {ctx['observation'][:50]}...")
    print(f"Limbic: novelty={ctx['limbic']['novelty']}, reward={ctx['limbic']['reward']}")
    
    start = time.time()
    result = qmd_local.cycle(ctx)
    latency = (time.time() - start) * 1000  # ms
    
    print(f"→ Decision: {result['action']} (confidence: {result['confidence']:.2f})")
    print(f"  Reasoning: {result['reasoning']}")
    print(f"  Latency: {latency:.1f}ms")
    print(f"  Query: {result.get('query', 'N/A')[:60]}...")
    
    results.append({
        "test": ctx['name'],
        "mode": "LOCAL",
        "action": result['action'],
        "confidence": result['confidence'],
        "reasoning": result['reasoning'],
        "latency_ms": latency
    })

print(f"\nQMD Stats: {qmd_local.stats}")

# Test OLLAMA mode
print("\n" + "=" * 70)
print("  🤖 TEST 2: OLLAMA MODE (Mort_II LLM decisions)")
print("=" * 70)

qmd_ollama = QMDLoop(use_ollama=True)
print(f"\nQMD initialized: {qmd_ollama.model}")
print(f"Mode: OLLAMA (LLM-powered)")
print(f"Model: antoniohudnall/Mortimer:latest")

for ctx in test_contexts:
    print(f"\n--- {ctx['name']} ---")
    print(f"Context: {ctx['observation'][:50]}...")
    print(f"Limbic: novelty={ctx['limbic']['novelty']}, reward={ctx['limbic']['reward']}")
    
    start = time.time()
    try:
        result = qmd_ollama.cycle(ctx)
        latency = (time.time() - start) * 1000  # ms
        
        print(f"→ Decision: {result['action']} (confidence: {result['confidence']:.2f})")
        print(f"  Reasoning: {result['reasoning']}")
        print(f"  Latency: {latency:.1f}ms")
        if result['reasoning'] != 'local_rules':
            print(f"  LLM Response: (see prompt below)")
        print(f"  Query: {result.get('query', 'N/A')[:60]}...")
        
        results.append({
            "test": ctx['name'],
            "mode": "OLLAMA",
            "action": result['action'],
            "confidence": result['confidence'],
            "reasoning": result['reasoning'],
            "latency_ms": latency
        })
    except Exception as e:
        print(f"  ⚠️  ERROR: {e}")
        print(f"  (This is what triggers the Thyroid cough back to LOCAL)")
        results.append({
            "test": ctx['name'],
            "mode": "OLLAMA",
            "error": str(e)
        })

# Summary comparison
print("\n" + "=" * 70)
print("  📊 COMPARISON SUMMARY")
print("=" * 70)

print("\n{:<25} {:<10} {:<10} {:<12} {:<15}".format(
    "Test", "LOCAL", "OLLAMA", "Difference", "Latency"
))
print("-" * 70)

local_results = [r for r in results if r['mode'] == 'LOCAL']
ollama_results = [r for r in results if r['mode'] == 'OLLAMA']

for i, local in enumerate(local_results):
    ollama = ollama_results[i] if i < len(ollama_results) else {}
    
    test_name = local['test'][:23] + ".." if len(local['test']) > 25 else local['test']
    local_action = local['action'][:8]
    ollama_action = ollama.get('action', 'ERROR')[:8]
    diff = "SAME" if local_action == ollama_action else "DIFF"
    latency = f"{local['latency_ms']:.0f}ms / {ollama.get('latency_ms', 0):.0f}ms"
    
    print(f"{test_name:<25} {local_action:<10} {ollama_action:<10} {diff:<12} {latency:<15}")

print("\n" + "=" * 70)
print("  🧠 KEY INSIGHTS")
print("=" * 70)

print("""
LOCAL Mode (Rule-based):
  ✅ Fast (< 1ms)
  ✅ Deterministic (same input → same output)
  ✅ Cheap (no API calls)
  ❌ Simple (4 hardcoded rules)
  ❌ No nuance (can't adapt to new situations)

OLLAMA Mode (LLM-powered):
  ✅ Smart (reasons about context)
  ✅ Flexible (can handle novel situations)
  ✅ Natural language understanding
  ❌ Slower (2-4 seconds)
  ❌ Variable (LLM may respond differently)
  ❌ Costs (compute/resources)

Thyroid's Role:
  • Uses LOCAL for routine decisions (fast, cheap)
  • 🤧 COUGHS to OLLAMA for important/complex decisions
  • 🤧 COUGHS back to LOCAL if Ollama fails
  • Prevents flip-flopping with hysteresis

This is like your brain's reflex arc:
  • Touch hot stove → Pull hand back (LOCAL, fast)
  • Complex moral dilemma → Think carefully (OLLAMA, slow)
""")

print("=" * 70)
print("  ✅ QMD Behavior Test Complete")
print("=" * 70)
