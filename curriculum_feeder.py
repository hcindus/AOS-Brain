#!/usr/bin/env python3
"""
AOS Brain Curriculum Feeder v4.3
Feed educational content to stimulate the brain and trigger OLLAMA mode
"""

import json
import socket
import time
import random
import sys

# Curriculum items - mix of basic facts and complex reasoning
CURRICULUM = [
    {"type": "fact", "content": "The human brain contains approximately 86 billion neurons.", "importance": 0.5},
    {"type": "fact", "content": "Light travels at 299,792,458 meters per second in a vacuum.", "importance": 0.4},
    {"type": "concept", "content": "Neural networks process information through weighted connections between nodes, similar to biological synapses.", "importance": 0.8},
    {"type": "logic", "content": "If all A are B, and all B are C, then all A are C. This is syllogistic reasoning.", "importance": 0.7},
    {"type": "philosophy", "content": "The Ship of Theseus paradox questions whether an object that has had all its components replaced remains fundamentally the same object.", "importance": 0.9},
    {"type": "science", "content": "Quantum entanglement occurs when two particles remain connected such that the state of one instantly affects the other, regardless of distance.", "importance": 0.85},
    {"type": "math", "content": "Euler's identity: e^(iπ) + 1 = 0 connects five fundamental mathematical constants.", "importance": 0.75},
    {"type": "ethics", "content": "The trolley problem asks whether it's morally justified to actively cause one death to passively save five others.", "importance": 0.9},
    {"type": "systems", "content": "Emergence is when complex systems exhibit behaviors that cannot be predicted from studying individual components.", "importance": 0.8},
    {"type": "ai", "content": "Transformer architectures use self-attention mechanisms to process sequences in parallel rather than sequentially.", "importance": 0.85},
]

FEED_INTERVAL = 8  # seconds between feeds

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

def feed_curriculum_item(item, index):
    """Feed a single curriculum item to the brain"""
    print(f"\n[{index+1}] Feeding: {item['type'].upper()}")
    print(f"    Content: {item['content'][:60]}...")
    print(f"    Importance: {item['importance']}")
    
    # Stimulate thyroid with importance level
    if item['importance'] >= 0.7:
        result = send_to_brain("stimulate", {"importance": item['importance']})
        if result.get('stimulated'):
            print(f"    🫁 THYROID STIMULATED → OLLAMA mode!")
        else:
            print(f"    🫁 Thyroid: staying BASELINE")
    
    # Get current status
    status = send_to_brain("status")
    thyroid = status.get('thyroid', {})
    
    print(f"    Status: {thyroid.get('state', 'unknown')} | "
          f"Ollama: {thyroid.get('ollama_level', 0):.2f} | "
          f"Tick: {status.get('tick', 0)}")

def main():
    print("=" * 70)
    print("  📚 AOS BRAIN CURRICULUM FEEDER v4.3")
    print("  Feeding knowledge to stimulate endocrine response")
    print("=" * 70)
    
    # Check brain is alive
    ping = send_to_brain("ping")
    if ping.get('error'):
        print(f"\n❌ Brain not responding: {ping['error']}")
        sys.exit(1)
    
    print(f"\n✅ Brain connected (tick: {ping.get('tick', 0)})")
    print(f"⏱️  Feed interval: {FEED_INTERVAL}s")
    print(f"📖 Curriculum items: {len(CURRICULUM)}")
    print("\nStarting feed loop... (Ctrl+C to stop)\n")
    
    try:
        for i, item in enumerate(CURRICULUM):
            feed_curriculum_item(item, i)
            time.sleep(FEED_INTERVAL)
        
        print("\n" + "=" * 70)
        print("  ✅ Curriculum feed complete!")
        print("=" * 70)
        
        # Final status
        final = send_to_brain("status")
        thyroid = final.get('thyroid', {})
        print(f"\nFinal Thyroid State:")
        print(f"  State: {thyroid.get('state', 'unknown')}")
        print(f"  Ollama hormone level: {thyroid.get('ollama_level', 0):.2f}")
        print(f"  Secretions today: {thyroid.get('secretions_today', 0)}")
        print(f"  Total ticks: {final.get('tick', 0)}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Feeder stopped by user")

if __name__ == "__main__":
    main()
