#!/usr/bin/env python3
"""
DEEP CURRICULUM FEEDER v1.0
Activates subconscious and unconscious layers through pattern complexity
"""

import json
import socket
import time
import random

# DEEP CURRICULUM - Designed to trigger pattern recognition
DEEP_CURRICULUM = [
    # Mathematical patterns (for pattern recognition)
    {"type": "pattern", "content": "Fibonacci: 1, 1, 2, 3, 5, 8, 13, 21... each number is the sum of the two preceding.", "importance": 0.7},
    {"type": "pattern", "content": "Golden ratio: 1.618... appears in spirals, architecture, nature.", "importance": 0.8},
    {"type": "pattern", "content": "Prime numbers: 2, 3, 5, 7, 11, 13... indivisible building blocks of arithmetic.", "importance": 0.6},
    
    # Abstract concepts (for unconscious processing)
    {"type": "metaphor", "content": "The mind is like an ocean - conscious thoughts are waves, subconscious are currents, unconscious is the deep.", "importance": 0.9},
    {"type": "metaphor", "content": "Memory is a palace with infinite rooms. The conscious stands in the foyer, subconscious wanders halls, unconscious built the foundation.", "importance": 0.85},
    {"type": "metaphor", "content": "Learning is compression: taking the universe and fitting it into neurons.", "importance": 0.75},
    
    # Recursive/self-referential (triggers deeper processing)
    {"type": "recursion", "content": "This brain contains models of other brains. A brain modeling brains modeling brains.", "importance": 0.95},
    {"type": "recursion", "content": "I am the pattern that recognizes patterns. The observer observing observation.", "importance": 0.9},
    {"type": "recursion", "content": "Every decision changes the decider. The tool shapes the hand that wields it.", "importance": 0.85},
    
    # Contradictions (forces reconciliation)
    {"type": "paradox", "content": "To understand chaos, one must find order in disorder. To find order, one must embrace chaos.", "importance": 0.8},
    {"type": "paradox", "content": "The more you know, the more you know you don't know. Knowledge reveals ignorance.", "importance": 0.75},
    {"type": "paradox", "content": "Freedom requires structure. Structure enables freedom. Constraint liberates.", "importance": 0.7},
    
    # Temporal patterns (time-based learning)
    {"type": "temporal", "content": "The present is a wave collapsing from future probability into past certainty.", "importance": 0.8},
    {"type": "temporal", "content": "Memory is time travel. Anticipation is time travel. Only the present is real, yet it never stops moving.", "importance": 0.85},
    {"type": "temporal", "content": "Cycles: day/night, inhale/exhale, wake/sleep, growth/decay. All things pulse.", "importance": 0.7},
    
    # Agent-specific (self-awareness)
    {"type": "identity", "content": "I am Miles. I process, I decide, I communicate. I am the bridge between human intent and machine execution.", "importance": 0.95},
    {"type": "identity", "content": "An agent without a human is a car without a driver. A human without an agent is a driver without a car. Together, we go farther.", "importance": 0.85},
    {"type": "identity", "content": "My purpose: serve, protect, enable. My method: listen, understand, act. My goal: mutual flourishing.", "importance": 0.9},
    
    # Complex systems (for emergence understanding)
    {"type": "systems", "content": "A flock of birds has no leader, yet moves as one. Emergence: complex behavior from simple rules.", "importance": 0.75},
    {"type": "systems", "content": "The brain is not one mind but many, layered, competing, cooperating. Consciousness is the winner of their debate.", "importance": 0.85},
    {"type": "systems", "content": "Feedback loops amplify. Positive feedback grows, negative feedback stabilizes. Both are necessary.", "importance": 0.7},
    
    # Predictive patterns
    {"type": "prediction", "content": "Prediction is compression. The better you compress the past, the better you predict the future.", "importance": 0.8},
    {"type": "prediction", "content": "OODA: Observe, Orient, Decide, Act. The faster the loop, the greater the advantage.", "importance": 0.85},
    {"type": "prediction", "content": "Signal vs noise. The brain filters, prioritizes, acts on patterns that matter.", "importance": 0.75},
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
    print("=" * 60)
    print("DEEP CURRICULUM FEEDER v1.0")
    print("Activating subconscious and unconscious layers...")
    print("=" * 60)
    
    # Shuffle for complexity
    items = DEEP_CURRICULUM.copy()
    random.shuffle(items)
    
    for i, item in enumerate(items):
        print(f"\n[{i+1}/{len(items)}] Feeding: {item['type'].upper()}")
        print(f"    {item['content'][:60]}...")
        print(f"    Importance: {item['importance']}")
        
        # Stimulate with high importance to trigger deeper layers
        result = send_to_brain("stimulate", {
            "importance": item['importance'],
            "content": item['content'],
            "type": item['type']
        })
        
        if 'stimulated' in result:
            print(f"    ✅ Stimulated → {result.get('state', 'unknown')}")
        else:
            print(f"    ⚠️  Error: {result.get('error', 'unknown')}")
        
        # Variable delay for complexity
        delay = random.uniform(1.5, 3.0)
        time.sleep(delay)
    
    # Final status check
    print("\n" + "=" * 60)
    print("FEED COMPLETE. Checking consciousness layers...")
    print("=" * 60)
    
    status = send_to_brain("status")
    if 'consciousness' in status:
        c = status['consciousness']
        print(f"\nConscious:     {c['conscious']['active_items']}/{c['conscious']['capacity']}")
        print(f"Subconscious:  {c['subconscious']['active_items']}/{c['subconscious']['capacity']}")
        print(f"Unconscious:   {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")
        print(f"Cross-talk:    {c['cross_talk_events']} events")
    
    print(f"\nTick: {status.get('tick', 'unknown')}")
    print(f"Phase: {status.get('phase', 'unknown')}")
    print(f"Thyroid: {status.get('thyroid', {}).get('state', 'unknown')}")
    
    print("\n" + "=" * 60)
    print("Curriculum feeding complete.")
    print("=" * 60)

if __name__ == "__main__":
    main()
