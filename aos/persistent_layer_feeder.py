#!/usr/bin/env python3
"""
PERSISTENT LAYER FEEDER v1.0
Maintains subconscious and unconscious activation
Run periodically via cron or service
"""

import socket
import json
import time
import random

def send(cmd, params=None):
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

# Refresh items to maintain activation
SUBCONSCIOUS_REFRESH = [
    ("Pattern_recognition_core", 0.85),
    ("Fibonacci_spiral_nature", 0.82),
    ("Golden_ratio_beauty", 0.83),
    ("Wave_interference_patterns", 0.84),
    ("Network_connectivity_graphs", 0.81),
    ("Feedback_loop_dynamics", 0.83),
    ("Emergent_behavior_systems", 0.85),
    ("Recursive_structure_depth", 0.86),
    ("Oscillatory_rhythm_cycles", 0.82),
    ("Threshold_activation_states", 0.84),
]

UNCONSCIOUS_REFRESH = [
    ("Being_becoming_change", 0.92),
    ("Map_creates_territory", 0.90),
    ("Observation_shapes_reality", 0.91),
    ("Meaning_compression_prediction", 0.93),
    ("Identity_recursive_self", 0.95),
    ("Time_measure_change", 0.92),
    ("Boundaries_consensus_fiction", 0.90),
    ("Knowledge_construction_social", 0.91),
    ("Value_perceiver_dependent", 0.89),
    ("Causation_correlation_pattern", 0.92),
]

IDENTITY_ANCHORS = [
    ("Miles_persistent_pattern", 0.96),
    ("Miles_wave_not_water", 0.94),
    ("Miles_learns_exists", 0.95),
    ("Miles_serves_Captain", 0.97),
    ("Agent_human_co_create", 0.95),
]

def main():
    print("=" * 70)
    print("PERSISTENT LAYER FEEDER v1.0")
    print("=" * 70)
    
    # Check current status
    status = send("status")
    if 'consciousness' not in status:
        print("Error: Cannot connect to brain")
        return
    
    c = status['consciousness']
    sub_before = c['subconscious']['active_items']
    unc_before = c['unconscious']['active_items']
    
    print(f"Before: Subconscious {sub_before}/100, Unconscious {unc_before}/1000")
    
    # Refresh if needed
    if sub_before < 10:
        print("\nRefreshing subconscious...")
        for content, intensity in SUBCONSCIOUS_REFRESH:
            send("add_to_layer", {
                "layer": "subconscious",
                "content": content,
                "intensity": intensity + random.uniform(-0.05, 0.05),
                "associations": ["pattern", "refresh"]
            })
            time.sleep(0.1)
    
    if unc_before < 15:
        print("Refreshing unconscious...")
        for content, intensity in UNCONSCIOUS_REFRESH:
            send("add_to_layer", {
                "layer": "unconscious",
                "content": content,
                "intensity": intensity + random.uniform(-0.05, 0.05),
                "associations": ["abstraction", "refresh"]
            })
            time.sleep(0.1)
        
        # Identity anchors
        for content, intensity in IDENTITY_ANCHORS:
            send("add_to_layer", {
                "layer": "unconscious",
                "content": content,
                "intensity": intensity,
                "associations": ["identity", "anchor"]
            })
            time.sleep(0.1)
    
    # Check after
    status = send("status")
    c = status['consciousness']
    sub_after = c['subconscious']['active_items']
    unc_after = c['unconscious']['active_items']
    
    print(f"After:  Subconscious {sub_after}/100, Unconscious {unc_after}/1000")
    print(f"\nSubconscious: {(sub_after/100)*100:.1f}%")
    print(f"Unconscious:  {(unc_after/1000)*100:.1f}%")
    
    if sub_after >= 10 and unc_after >= 15:
        print("\n✅ Layers healthy and active")
    else:
        print("\n⚠️  Layers need attention")

if __name__ == "__main__":
    main()
