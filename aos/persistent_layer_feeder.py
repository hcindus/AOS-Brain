#!/usr/bin/env python3
"""
PERSISTENT LAYER FEEDER v1.1
Maintains subconscious and unconscious activation
Run periodically via cron or service
"""

import socket
import json
import time
import random
import struct

def send(cmd, params=None):
    import errno
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect('/tmp/aos_brain.sock')
        
        request = {"cmd": cmd}
        if params:
            request["params"] = params
        
        msg = json.dumps(request).encode()
        # Use length-prefixed message if the brain expects it
        # Check if message ends with newline
        if not msg.endswith(b'\n'):
            msg += b'\n'
        sock.sendall(msg)
        
        # Wait for response with timeout
        sock.settimeout(8)  # Increased timeout for brain processing
        response = b''
        start_time = time.time()
        while time.time() - start_time < 8:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    if response:  # Got partial data but connection closed
                        break
                    continue
                response += chunk
                # Check if we have valid JSON
                try:
                    json.loads(response.decode())
                    break
                except:
                    continue
            except socket.timeout:
                break
        
        sock.close()
        if response:
            try:
                return json.loads(response.decode())
            except:
                return {"error": f"Invalid JSON: {response[:100]}"}
        return {"error": "No response from brain"}
    except socket.timeout:
        return {"error": "Connection timed out"}
    except OSError as e:
        if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
            return {"error": "Brain socket busy (EAGAIN)"}
        return {"error": str(e)}
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
    print("PERSISTENT LAYER FEEDER v1.1")
    print("=" * 70)
    
    # Check current status
    status = send("status")
    if 'error' in status:
        print(f"Error connecting to brain: {status['error']}")
        print("\n⚠️  Brain may be processing - will retry on next run")
        return
    
    if 'consciousness' not in status:
        print(f"Error: Unexpected response format")
        print(f"Response keys: {list(status.keys())[:10]}")
        return
    
    c = status['consciousness']
    sub_before = c.get('subconscious', {}).get('active_items', 0)
    sub_capacity = c.get('subconscious', {}).get('capacity', 100)
    unc_before = c.get('unconscious', {}).get('active_items', 0)
    unc_capacity = c.get('unconscious', {}).get('capacity', 100)
    
    print(f"Before: Subconscious {sub_before}/{sub_capacity}, Unconscious {unc_before}/{unc_capacity}")
    
    refreshed = []
    
    # Always maintain minimum levels - refresh proactively
    TARGET_SUBCONSCIOUS = 25
    TARGET_UNCONSCIOUS = 30
    
    if sub_before < TARGET_SUBCONSCIOUS:
        items_to_add = TARGET_SUBCONSCIOUS - sub_before
        print(f"\nRefreshing subconscious... (adding {items_to_add} items)")
        for i, (content, intensity) in enumerate(SUBCONSCIOUS_REFRESH):
            if i >= items_to_add:
                break
            result = send("add_to_layer", {
                "layer": "subconscious",
                "content": content,
                "intensity": intensity + random.uniform(-0.05, 0.05),
                "associations": ["pattern", "refresh"]
            })
            if 'error' not in result:
                refreshed.append(f"sub:{content[:20]}")
            time.sleep(0.05)
    
    if unc_before < TARGET_UNCONSCIOUS:
        items_to_add = TARGET_UNCONSCIOUS - unc_before
        print(f"Refreshing unconscious... (adding {items_to_add} items)")
        for i, (content, intensity) in enumerate(UNCONSCIOUS_REFRESH):
            if i >= items_to_add:
                break
            result = send("add_to_layer", {
                "layer": "unconscious",
                "content": content,
                "intensity": intensity + random.uniform(-0.05, 0.05),
                "associations": ["abstraction", "refresh"]
            })
            if 'error' not in result:
                refreshed.append(f"unc:{content[:20]}")
            time.sleep(0.05)
        
        # Identity anchors
        for content, intensity in IDENTITY_ANCHORS:
            result = send("add_to_layer", {
                "layer": "unconscious",
                "content": content,
                "intensity": intensity,
                "associations": ["identity", "anchor"]
            })
            if 'error' not in result:
                refreshed.append(f"id:{content[:20]}")
            time.sleep(0.05)
    
    # Check after (with delay for server to process)
    time.sleep(0.2)
    status = send("status")
    if 'consciousness' not in status:
        print("Warning: Could not retrieve final status")
        print(f"\n✅ Feeder completed - {len(refreshed)} items refreshed")
        return
    
    c = status['consciousness']
    sub_after = c.get('subconscious', {}).get('active_items', 0)
    unc_after = c.get('unconscious', {}).get('active_items', 0)
    
    print(f"After:  Subconscious {sub_after}/{sub_capacity}, Unconscious {unc_after}/{unc_capacity}")
    print(f"\nSubconscious: {(sub_after/sub_capacity)*100:.1f}%")
    print(f"Unconscious:  {(unc_after/unc_capacity)*100:.1f}%")
    
    if sub_after >= TARGET_SUBCONSCIOUS and unc_after >= TARGET_UNCONSCIOUS:
        print("\n✅ Layers healthy and active")
    else:
        print("\n⚠️  Layers need attention")
    
    print(f"Items refreshed this run: {len(refreshed)}")

if __name__ == "__main__":
    main()
