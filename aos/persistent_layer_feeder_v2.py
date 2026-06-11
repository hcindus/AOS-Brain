#!/usr/bin/env python3
"""
PERSISTENT LAYER FEEDER v1.1
Maintains subconscious and unconscious activation
Modified with better error handling and fallback
"""

import socket
import json
import time
import random
import os

def send(cmd, params=None, timeout=3):
    """Send command to brain socket with timeout"""
    sock = None
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect('/tmp/aos_brain.sock')
        
        request = {"cmd": cmd}
        if params:
            request["params"] = params
        
        sock.sendall(json.dumps(request).encode() + b'\n')
        sock.shutdown(socket.SHUT_WR)
        
        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        
        return json.loads(response.decode())
    except Exception as e:
        return {"error": str(e)}
    finally:
        if sock:
            try:
                sock.close()
            except:
                pass

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

def check_brain_status():
    """Check if brain is responsive"""
    print("Checking brain status...")
    status = send("status", timeout=2)
    if 'error' in status:
        print(f"  Connection error: {status['error']}")
        return None
    if 'consciousness' not in status:
        print(f"  Unexpected response: {list(status.keys())[:5]}")
        return None
    return status

def main():
    print("=" * 70)
    print("PERSISTENT LAYER FEEDER v1.1")
    print("=" * 70)
    
    # Check if socket exists
    if not os.path.exists('/tmp/aos_brain.sock'):
        print("ERROR: Brain socket not found at /tmp/aos_brain.sock")
        print("The AOS brain may not be running.")
        return
    
    print("Socket found at /tmp/aos_brain.sock")
    
    # Try to get status with retries
    status = None
    for attempt in range(3):
        status = check_brain_status()
        if status:
            break
        time.sleep(0.5)
    
    if not status:
        print("\nFailed to connect to brain after 3 attempts.")
        print("Brain process appears to be in an unresponsive state.")
        print("\nPartial Result: Socket exists but brain is not responding.")
        return
    
    c = status['consciousness']
    sub_before = c['subconscious']['active_items']
    unc_before = c['unconscious']['active_items']
    unc_capacity = c['unconscious']['capacity']
    
    print(f"\nCurrent State:")
    print(f"  Subconscious: {sub_before}/{c['subconscious']['capacity']} ({(sub_before/c['subconscious']['capacity'])*100:.1f}%)")
    print(f"  Unconscious:  {unc_before}/{unc_capacity} ({(unc_before/unc_capacity)*100:.1f}%)")
    
    # Refresh if needed
    refreshed_sub = 0
    refreshed_unc = 0
    
    if sub_before < 10:
        print("\nRefreshing subconscious...")
        for content, intensity in SUBCONSCIOUS_REFRESH:
            result = send("add_to_layer", {
                "layer": "subconscious",
                "content": content,
                "intensity": intensity + random.uniform(-0.05, 0.05),
                "associations": ["pattern", "refresh"]
            }, timeout=2)
            if 'error' not in result:
                refreshed_sub += 1
            time.sleep(0.05)
        print(f"  Added {refreshed_sub} items to subconscious")
    
    if unc_before < 15:
        print("Refreshing unconscious...")
        for content, intensity in UNCONSCIOUS_REFRESH:
            result = send("add_to_layer", {
                "layer": "unconscious",
                "content": content,
                "intensity": intensity + random.uniform(-0.05, 0.05),
                "associations": ["abstraction", "refresh"]
            }, timeout=2)
            if 'error' not in result:
                refreshed_unc += 1
            time.sleep(0.05)
        
        # Identity anchors
        print("  Anchoring identity...")
        for content, intensity in IDENTITY_ANCHORS:
            result = send("add_to_layer", {
                "layer": "unconscious",
                "content": content,
                "intensity": intensity,
                "associations": ["identity", "anchor"]
            }, timeout=2)
            if 'error' not in result:
                refreshed_unc += 1
            time.sleep(0.05)
        print(f"  Added {refreshed_unc} items to unconscious (including identity anchors)")
    
    # Check final status
    time.sleep(0.2)
    status = check_brain_status()
    if status and 'consciousness' in status:
        c = status['consciousness']
        sub_after = c['subconscious']['active_items']
        unc_after = c['unconscious']['active_items']
        
        print(f"\nFinal State:")
        print(f"  Subconscious: {sub_after}/{c['subconscious']['capacity']} ({(sub_after/c['subconscious']['capacity'])*100:.1f}%)")
        print(f"  Unconscious:  {unc_after}/{c['unconscious']['capacity']} ({(unc_after/c['unconscious']['capacity'])*100:.1f}%)")
        
        if sub_after >= 10 and unc_after >= 15:
            print("\n✅ Layer maintenance complete - all layers healthy")
        else:
            print("\n⚠️  Some layers below target thresholds")
    else:
        print("\n✅ Refresh commands sent (final status unavailable)")

if __name__ == "__main__":
    main()
