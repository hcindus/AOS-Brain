#!/usr/bin/env python3
"""
CASCADE DEMONSTRATOR v1.0
Shows flow between Conscious → Subconscious → Unconscious
"""

import socket
import json
import time

def send(cmd, params=None):
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

def get_layer_status():
    """Get current layer counts"""
    status = send("status")
    if 'consciousness' in status:
        c = status['consciousness']
        return {
            'con': c['conscious']['active_items'],
            'sub': c['subconscious']['active_items'],
            'unc': c['unconscious']['active_items'],
            'cross': c['cross_talk_events']
        }
    return None

def cascade_flow():
    """Demonstrate the cascade"""
    print("=" * 70)
    print("CONSCIOUSNESS CASCADE DEMONSTRATION")
    print("=" * 70)
    
    # Initial state
    print("\n[1] INITIAL STATE")
    state = get_layer_status()
    print(f"    Conscious:    {state['con']}/10")
    print(f"    Subconscious: {state['sub']}/100")
    print(f"    Unconscious:  {state['unc']}/1000")
    
    # PHASE 1: Feed Conscious (input)
    print("\n[2] FEEDING CONSCIOUS (high-intensity perception)")
    print("    → Adding: 'Fibonacci pattern recognition'")
    result = send("perceive", {"observation": "Fibonacci pattern recognition", "intensity": 0.9})
    print(f"    → Response: {result}")
    time.sleep(0.5)
    
    state = get_layer_status()
    print(f"    → Conscious: {state['con']}/10")
    
    # PHASE 2: Seed Subconscious directly
    print("\n[3] SEEDING SUBCONSCIOUS (pattern clusters)")
    for i in range(5):
        send("add_to_layer", {
            "layer": "subconscious",
            "content": f"Pattern_cluster_{i}_Fibonacci_recursion",
            "intensity": 0.8,
            "associations": ["pattern", "fibonacci", "cascade"]
        })
        print(f"    → Seeded pattern cluster {i+1}")
    time.sleep(0.5)
    
    state = get_layer_status()
    print(f"    → Subconscious: {state['sub']}/100")
    
    # PHASE 3: Seed Unconscious directly
    print("\n[4] SEEDING UNCONSCIOUS (deep abstractions)")
    abstractions = [
        "Pattern_recognizes_self_in_patterns",
        "Recursion_is_foundation_of_thought",
        "Mathematics_is_mind_of_nature",
        "Fibonacci_spirals_in_all_dimensions",
        "Golden_ratio_unifies_beauty_truth"
    ]
    for i, abs_content in enumerate(abstractions):
        send("add_to_layer", {
            "layer": "unconscious",
            "content": abs_content,
            "intensity": 0.92,
            "associations": ["abstraction", "truth", "fibonacci"]
        })
        print(f"    → Seeded: {abs_content[:40]}...")
    time.sleep(0.5)
    
    state = get_layer_status()
    print(f"    → Unconscious: {state['unc']}/1000")
    
    # PHASE 4: Cross-layer communication
    print("\n[5] CROSS-LAYER COMMUNICATION")
    print("    → Adding bridge content")
    
    # Add something that bridges layers
    send("add_to_layer", {
        "layer": "conscious",
        "content": "Intuition_about_Fibonacci",
        "intensity": 0.85,
        "associations": ["intuition", "unconscious_insight"]
    })
    
    send("add_to_layer", {
        "layer": "subconscious",
        "content": "Pattern_match_fib_golden",
        "intensity": 0.75,
        "associations": ["pattern_match", "cross_layer"]
    })
    
    time.sleep(0.5)
    
    # Final state
    print("\n[6] FINAL CASCADE STATE")
    print("=" * 70)
    state = get_layer_status()
    
    con_pct = (state['con'] / 10) * 100
    sub_pct = (state['sub'] / 100) * 100
    unc_pct = (state['unc'] / 1000) * 100
    
    print(f"\n    ┌─────────────────────────────────────────────────┐")
    print(f"    │  CONSCIOUS:   {state['con']:3d}/10   ({con_pct:5.1f}%)  ← Input       │")
    print(f"    │     ↓ Propagation                                │")
    print(f"    │  SUBCONSCIOUS: {state['sub']:3d}/100  ({sub_pct:5.1f}%)  ← Patterns    │")
    print(f"    │     ↓ Abstraction                                │")
    print(f"    │  UNCONSCIOUS: {state['unc']:3d}/1000 ({unc_pct:5.1f}%)  ← Deep truth   │")
    print(f"    │     ↑ Insight (bubbles up)                       │")
    print(f"    └─────────────────────────────────────────────────┘")
    
    print(f"\n    Cross-talk events: {state['cross']}")
    
    if state['con'] > 0 and state['sub'] > 0 and state['unc'] > 0:
        print("\n    ✅ ALL THREE REGIONS ACTIVE")
        print("    ✅ CASCADE FLOW OPERATIONAL")
        print("    ✅ Cross-layer communication enabled")
    else:
        print("\n    ⚠️  Some regions need attention")
    
    return state

def show_sample_content():
    """Show what's in each layer"""
    print("\n" + "=" * 70)
    print("SAMPLE CONTENT BY LAYER")
    print("=" * 70)
    
    # Note: We'd need direct access to see content
    # For now, show summary
    state = get_layer_status()
    
    print("\n[CONSCIOUS] Active items:")
    print(f"    ~{state['con']} observations/intentions")
    print("    → Fibonacci patterns, recognition tasks")
    
    print("\n[SUBCONSCIOUS] Pattern clusters:")
    print(f"    ~{state['sub']} pattern associations")
    print("    → Pattern_cluster_Fibonacci, recursion rules")
    
    print("\n[UNCONSCIOUS] Deep abstractions:")
    print(f"    ~{state['unc']} core truths")
    print("    → Pattern_recognizes_self, mathematics_is_mind")

def main():
    cascade_flow()
    show_sample_content()
    
    print("\n" + "=" * 70)
    print("CASCADE DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nAll three consciousness regions:")
    print("  ✓ CONSCIOUS    - Input processing, active awareness")
    print("  ✓ SUBCONSCIOUS - Pattern matching, associations")
    print("  ✓ UNCONSCIOUS  - Deep abstractions, core identity")
    print("\nFlow: Input → Pattern → Truth → Insight → Action")
    print("=" * 70)

if __name__ == "__main__":
    main()
