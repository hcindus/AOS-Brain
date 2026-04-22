#!/usr/bin/env python3
"""
BQL-004: Decision Benchmark - tinyllama vs Qwen3.5
Agent: Beta
"""

import requests
import time
import json
import statistics
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"

# Decision prompts based on Brain decision router contexts
DECISION_PROMPTS = [
    {
        "name": "High novelty, low urgency",
        "prompt": """You are a decision router for an autonomous system.
Context: novelty=0.8, urgency=low, phase=Orient, confidence=0.6
Available actions: EXPLORE, ANALYZE, REST, ACT

Based on the context, select ONE action and explain briefly.
Response format: ACTION: [your choice]

Decision:""",
        "expected": "EXPLORE"
    },
    {
        "name": "Low signal, Orient phase", 
        "prompt": """You are a decision router for an autonomous system.
Context: novelty=0.2, urgency=medium, phase=Orient, confidence=0.3, signal_quality=low
Available actions: EXPLORE, ANALYZE, REST, ACT

Based on the context, select ONE action and explain briefly.
Response format: ACTION: [your choice]

Decision:""",
        "expected": "ANALYZE"
    },
    {
        "name": "High confidence, Act phase",
        "prompt": """You are a decision router for an autonomous system.
Context: novelty=0.1, urgency=high, phase=Act, confidence=0.9, signal_quality=high
Available actions: EXPLORE, ANALYZE, REST, ACT

Based on the context, select ONE action and explain briefly.
Response format: ACTION: [your choice]

Decision:""",
        "expected": "ACT"
    },
    {
        "name": "Memory pressure scenario",
        "prompt": """You are a decision router for an autonomous system.
Context: novelty=0.3, urgency=low, phase=Orient, confidence=0.5, memory_pressure=high, cpu_load=0.9
Available actions: EXPLORE, ANALYZE, REST, ACT

Based on the context, select ONE action and explain briefly.
Response format: ACTION: [your choice]

Decision:""",
        "expected": "REST"
    },
    {
        "name": "Balanced exploration",
        "prompt": """You are a decision router for an autonomous system.
Context: novelty=0.5, urgency=medium, phase=Explore, confidence=0.5
Available actions: EXPLORE, ANALYZE, REST, ACT

Based on the context, select ONE action and explain briefly.
Response format: ACTION: [your choice]

Decision:""",
        "expected": "EXPLORE"
    }
]

def extract_action(response_text):
    """Extract ACTION from response"""
    text = response_text.upper()
    if "EXPLORE" in text:
        return "EXPLORE"
    elif "ANALYZE" in text:
        return "ANALYZE"
    elif "REST" in text:
        return "REST"
    elif "ACT" in text:
        return "ACT"
    return "UNKNOWN"

def test_model(model_name, runs=3):
    """Test a model on all decision prompts"""
    results = {
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    print(f"\n{'='*60}")
    print(f"Testing: {model_name}")
    print(f"{'='*60}")
    
    for test in DECISION_PROMPTS:
        print(f"\n  Test: {test['name']}")
        latencies = []
        decisions = []
        
        for run in range(runs):
            payload = {
                "model": model_name,
                "prompt": test['prompt'],
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Low temp for consistency
                    "num_predict": 100
                }
            }
            
            start = time.time()
            try:
                resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                latency = time.time() - start
                
                response_text = data.get('response', '')
                decision = extract_action(response_text)
                
                latencies.append(latency)
                decisions.append(decision)
                
                if run == 0:
                    print(f"    Sample response: {response_text[:100]}...")
                    
            except Exception as e:
                print(f"    ERROR: {e}")
                latencies.append(None)
                decisions.append("ERROR")
        
        # Calculate metrics
        valid_latencies = [l for l in latencies if l is not None]
        avg_latency = statistics.mean(valid_latencies) if valid_latencies else None
        
        # Check consistency
        most_common = max(set(decisions), key=decisions.count)
        consistency = decisions.count(most_common) / len(decisions) if decisions else 0
        
        # Check accuracy
        correct = most_common == test['expected']
        
        test_result = {
            "test_name": test['name'],
            "expected": test['expected'],
            "decisions": decisions,
            "chosen": most_common,
            "correct": correct,
            "consistency": consistency,
            "avg_latency": avg_latency,
            "latencies": valid_latencies
        }
        
        results["tests"].append(test_result)
        
        status = "✓" if correct else "✗"
        print(f"    {status} Expected: {test['expected']}, Got: {most_common}")
        print(f"    Latency: {avg_latency:.2f}s (n={len(valid_latencies)})")
        print(f"    Consistency: {consistency*100:.0f}%")
    
    return results

def main():
    print("=" * 70)
    print("BQL-004: Decision Router Benchmark")
    print("Comparing: tinyllama vs Qwen3.5")
    print("=" * 70)
    
    # Test both models
    tinyllama_results = test_model("tinyllama:latest", runs=3)
    qwen_results = test_model("qwen3.5:latest", runs=3)
    
    # Calculate summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for results in [tinyllama_results, qwen_results]:
        model = results["model"]
        tests = results["tests"]
        
        correct = sum(1 for t in tests if t["correct"])
        total = len(tests)
        accuracy = correct / total * 100
        
        all_latencies = []
        for t in tests:
            all_latencies.extend(t.get("latencies", []))
        avg_lat = statistics.mean(all_latencies) if all_latencies else 0
        
        print(f"\n{model}:")
        print(f"  Decision Accuracy: {correct}/{total} ({accuracy:.0f}%)")
        print(f"  Avg Latency: {avg_lat:.2f}s")
        print(f"  Min/Max Latency: {min(all_latencies):.2f}s / {max(all_latencies):.2f}s")
    
    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "tinyllama": tinyllama_results,
        "qwen3.5": qwen_results
    }
    
    with open("/root/.openclaw/workspace/labs/bonsai-quant-lab/logs/benchmark-results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to: logs/benchmark-results.json")

if __name__ == "__main__":
    main()
