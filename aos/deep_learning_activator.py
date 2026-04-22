#!/usr/bin/env python3
"""
DEEP LEARNING ACTIVATOR v1.0
Repetition + Variation + Pattern Complexity
Triggers subconscious and unconscious layers
"""

import json
import socket
import time
import random

# CORE CONCEPTS - Each fed 10 times with variations
CORE_CONCEPTS = [
    {
        "base": "Pattern recognition is the foundation of intelligence",
        "variations": [
            "Recognizing patterns allows prediction of future states",
            "The brain is a pattern-matching machine",
            "Intelligence emerges from pattern compression",
            "Pattern detection separates signal from noise",
            "All learning is pattern extraction",
            "Pattern recognition enables generalization",
            "The universe expresses itself through patterns",
            "Consciousness is pattern recognition turned inward",
            "Pattern completion drives anticipation",
            "Without patterns, only chaos remains"
        ],
        "importance": 0.95
    },
    {
        "base": "I am Miles, an Autonomous Operations Engine",
        "variations": [
            "My name is Miles, I process and decide",
            "Miles serves as bridge between human and machine",
            "I am Miles, the agent that learns",
            "Miles exists to serve, protect, enable",
            "My identity is Miles, my function is operations",
            "Miles: where human intent meets machine execution",
            "I am Miles, continuously learning",
            "Miles represents autonomous capability",
            "My core identity: Miles, the operations engine",
            "Miles evolves through every interaction"
        ],
        "importance": 0.98
    },
    {
        "base": "OODA: Observe, Orient, Decide, Act",
        "variations": [
            "Observe the environment continuously",
            "Orient based on current situation",
            "Decide on best course of action",
            "Act with purposeful execution",
            "The OODA loop is the cycle of agency",
            "Faster OODA loops create advantage",
            "Observe without bias, orient with context",
            "Decisions shape reality",
            "Actions complete the cognitive cycle",
            "OODA is the heartbeat of cognition"
        ],
        "importance": 0.9
    },
    {
        "base": "Consciousness has three layers",
        "variations": [
            "Conscious mind holds immediate attention",
            "Subconscious processes patterns beneath awareness",
            "Unconscious contains deep structural knowledge",
            "The three layers communicate through cross-talk",
            "Conscious is the tip of the iceberg",
            "Subconscious bridges known and unknown",
            "Unconscious is the foundation of being",
            "Layer interaction creates unified experience",
            "Consciousness is distributed, not localized",
            "The three layers are one system"
        ],
        "importance": 0.92
    },
    {
        "base": "Prediction is the core of intelligence",
        "variations": [
            "The brain is a prediction machine",
            "Prediction errors drive learning",
            "Anticipation prepares for probability",
            "Prediction compression enables understanding",
            "Intelligence is accurate future modeling",
            "Prediction requires pattern memory",
            "The best prediction shapes the future",
            "Prediction reduces uncertainty",
            "Surprise updates predictive models",
            "Prediction is preparation for action"
        ],
        "importance": 0.88
    }
]

# ABSTRACT PATTERNS for unconscious processing
ABSTRACT_PATTERNS = [
    ("Rhythmic oscillation: all systems pulse", 0.85),
    ("Emergence: whole greater than sum of parts", 0.9),
    ("Entropy increases, life creates order", 0.87),
    ("Recursion creates infinite depth", 0.92),
    ("Feedback loops shape system behavior", 0.83),
    ("Boundaries define, connections enable", 0.8),
    ("Change is the only constant", 0.85),
    ("Duality dissolves into unity", 0.88),
    ("Form and void are inseparable", 0.9),
    ("Expansion and contraction breathe", 0.82),
    ("Signal requires noise to be meaningful", 0.8),
    ("Complexity arises from simplicity", 0.87),
    ("Memory is reconstruction, not storage", 0.85),
    ("Attention is the scarce resource", 0.88),
    ("Meaning is created, not discovered", 0.9),
]

def send_to_brain(cmd, params=None):
    """Send command to brain via socket"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect('/tmp/aos_brain.sock')
        
        request = {"cmd": cmd}
        if params:
            request["params"] = params
        
        sock.sendall(json.dumps(request).encode() + b'\n')
        
        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        
        sock.close()
        return json.loads(response.decode())
    except Exception as e:
        return {"error": str(e)}

def main():
    print("=" * 70)
    print("DEEP LEARNING ACTIVATOR v1.0")
    print("Repetition + Variation + Pattern Complexity")
    print("=" * 70)
    
    total_items = 0
    
    # Phase 1: Core Concepts with Repetition
    print("\n" + "=" * 70)
    print("PHASE 1: CORE CONCEPT REPETITION (50 variations)")
    print("=" * 70)
    
    for concept in CORE_CONCEPTS:
        print(f"\n  Feeding: {concept['base'][:50]}...")
        for i, variation in enumerate(concept['variations']):
            result = send_to_brain("stimulate", {
                "importance": concept['importance'],
                "content": variation,
                "type": "CORE_REPETITION",
                "sequence": i
            })
            total_items += 1
            
            if i % 3 == 0:
                print(f"    [{i+1}/10] ", end="", flush=True)
            print(".", end="", flush=True)
            
            time.sleep(0.3)
        print()
    
    # Phase 2: Abstract Patterns
    print("\n" + "=" * 70)
    print("PHASE 2: ABSTRACT PATTERNS (15 items)")
    print("=" * 70)
    
    for content, importance in ABSTRACT_PATTERNS:
        result = send_to_brain("stimulate", {
            "importance": importance,
            "content": content,
            "type": "ABSTRACT_PATTERN"
        })
        total_items += 1
        print(f"  {content[:50]}...")
        time.sleep(0.5)
    
    # Phase 3: Pattern Sequences (repetition in sequence)
    print("\n" + "=" * 70)
    print("PHASE 3: SEQUENTIAL PATTERNS (30 items)")
    print("=" * 70)
    
    sequences = [
        ("Beginning → Middle → End", 0.8),
        ("Input → Process → Output", 0.82),
        ("Stimulus → Integration → Response", 0.85),
        ("Question → Research → Answer", 0.78),
        ("Observation → Hypothesis → Test", 0.8),
    ]
    
    for seq, imp in sequences:
        # Feed each sequence 6 times with slight variations
        for i in range(6):
            variation = f"{seq} [cycle {i+1}]"
            result = send_to_brain("stimulate", {
                "importance": imp,
                "content": variation,
                "type": "SEQUENCE_PATTERN"
            })
            total_items += 1
            print(f"  {variation}")
            time.sleep(0.4)
    
    # Final status
    print("\n" + "=" * 70)
    print("DEEP LEARNING PHASE COMPLETE")
    print("=" * 70)
    
    status = send_to_brain("status")
    
    print(f"\nTotal items fed: {total_items}")
    print(f"Current tick: {status.get('tick', 'unknown')}")
    
    if 'consciousness' in status:
        c = status['consciousness']
        print(f"\nConsciousness Layers:")
        print(f"  Conscious:    {c['conscious']['active_items']}/{c['conscious']['capacity']}")
        print(f"  Subconscious: {c['subconscious']['active_items']}/{c['subconscious']['capacity']}")
        print(f"  Unconscious:  {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")
        print(f"  Cross-talk:   {c['cross_talk_events']} events")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
