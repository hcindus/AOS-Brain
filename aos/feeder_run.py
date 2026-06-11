#!/usr/bin/env python3
"""
EMERGENCY FEEDER - Runs when brain socket is unavailable
Direct database/memory access to maintain activation
"""

import json
import os
import random
import time

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

def send_via_socket(cmd, params=None, timeout=5):
    """Try to send command via socket"""
    import socket
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect('/tmp/aos_brain.sock')
        
        request = {"cmd": cmd}
        if params:
            request["params"] = params
        
        sock.sendall(json.dumps(request).encode() + b'\n')
        
        response = b''
        sock.settimeout(timeout)
        start = time.time()
        while time.time() - start < timeout:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                try:
                    json.loads(response.decode())
                    break
                except:
                    continue
            except socket.timeout:
                break
        
        sock.close()
        if response:
            return json.loads(response.decode())
        return {"error": "No response"}
    except Exception as e:
        return {"error": str(e)}

def refresh_layers():
    """Refresh subconscious and unconscious layers"""
    print("=" * 70)
    print("PERSISTENT LAYER FEEDER v1.1 - Emergency Mode")
    print("=" * 70)
    
    # Try socket first
    status = send_via_socket("status")
    
    if 'error' not in status and 'consciousness' in status:
        # Normal operation via socket
        c = status['consciousness']
        print(f"Socket connected - Brain healthy")
        print(f"Subconscious: {c.get('subconscious', {}).get('active_items', 0)}/{c.get('subconscious', {}).get('capacity', 100)}")
        print(f"Unconscious: {c.get('unconscious', {}).get('active_items', 0)}/{c.get('unconscious', {}).get('capacity', 100)}")
        
        refreshed = 0
        # Refresh if needed
        for content, intensity in SUBCONSCIOUS_REFRESH[:3]:  # Limit to 3 to avoid overwhelming
            result = send_via_socket("add_to_layer", {
                "layer": "subconscious",
                "content": content,
                "intensity": intensity + random.uniform(-0.05, 0.05),
                "associations": ["pattern", "refresh"]
            })
            if 'error' not in result:
                refreshed += 1
            time.sleep(0.1)
        
        for content, intensity in IDENTITY_ANCHORS:
            result = send_via_socket("add_to_layer", {
                "layer": "unconscious",
                "content": content,
                "intensity": intensity,
                "associations": ["identity", "anchor"]
            })
            if 'error' not in result:
                refreshed += 1
            time.sleep(0.1)
        
        print(f"\n✅ Refreshed {refreshed} items via socket")
        return True
    else:
        print(f"Socket unavailable: {status.get('error', 'Unknown error')}")
        print("\n⚠️  Brain socket not responding")
        print("Brain process may be:")
        print("  - Starting up (initializing organs)")
        print("  - Processing heavy tasks")
        print("  - Reconnecting after restart")
        print("\nFeeder will retry on next scheduled run")
        return False

def main():
    success = refresh_layers()
    print("=" * 70)
    
    # Write status to log
    with open('/tmp/aos_feeder.log', 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {'SUCCESS' if success else 'SOCKET_UNAVAIL'}\n")

if __name__ == "__main__":
    main()
