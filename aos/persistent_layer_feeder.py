#!/usr/bin/env python3
"""
PERSISTENT LAYER FEEDER v1.2
Maintains subconscious and unconscious activation
"""

import socket
import json
import time
import random
import os

SOCKET_PATH = '/tmp/aos_brain.sock'

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

def send_cmd(cmd, params=None):
    """Send a command to the brain socket"""
    if not os.path.exists(SOCKET_PATH):
        return {"error": "Socket missing"}
    
    sock = None
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(20)  # Longer timeout for filtered commands
        sock.connect(SOCKET_PATH)
        
        request = {"cmd": cmd}
        if params:
            request["params"] = params
        
        msg = json.dumps(request).encode() + b'\n'
        sock.sendall(msg)
        
        # Wait for response with retries
        sock.settimeout(20)
        response = b''
        start = time.time()
        while time.time() - start < 20:
            try:
                chunk = sock.recv(8192)
                if not chunk:
                    break
                response += chunk
                # Try parse
                try:
                    return json.loads(response.decode())
                except:
                    continue
            except socket.timeout:
                break
        
        if response:
            try:
                return json.loads(response.decode())
            except:
                return {"error": "JSON fail"}
        return {"error": "No data"}
        
    except socket.timeout:
        return {"error": "Timeout"}
    except Exception as e:
        return {"error": str(e)[:40]}
    finally:
        if sock:
            try:
                sock.close()
            except:
                pass

def main():
    print("=" * 70)
    print("PERSISTENT LAYER FEEDER v1.2")
    print("=" * 70)
    
    status = send_cmd("status")
    
    if 'error' in status:
        print(f"❌ Connection: {status['error']}")
        return
    
    if 'consciousness' not in status:
        print(f"⚠️  No consciousness data")
        return
    
    c = status['consciousness']
    sub_before = c.get('subconscious', {}).get('active_items', 0)
    sub_cap = c.get('subconscious', {}).get('capacity', 100)
    unc_before = c.get('unconscious', {}).get('active_items', 0)
    unc_cap = c.get('unconscious', {}).get('capacity', 2000)
    
    print(f"BEFORE: Subconscious {sub_before}/{sub_cap} ({sub_before/sub_cap*100:.0f}%), Unconscious {unc_before}/{unc_cap} ({unc_before/unc_cap*100:.1f}%)")
    
    refreshed = 0
    TARGET_SUB = 25
    TARGET_UNC = 30
    
    # Add subconscious items
    if sub_before < TARGET_SUB:
        need = TARGET_SUB - sub_before
        print(f"Adding {need} subconscious items...")
        for content, intensity in SUBCONSCIOUS_REFRESH[:need]:
            result = send_cmd("add_to_layer", {
                "layer": "subconscious",
                "content": content,
                "intensity": round(intensity + random.uniform(-0.03, 0.03), 3),
                "associations": ["pattern"]
            })
            if 'error' not in result:
                refreshed += 1
                print(f"  + {content[:25]}... OK")
            else:
                print(f"  + {content[:25]}... {result['error']}")
            time.sleep(0.1)  # Slower to not overwhelm
    
    # Add unconscious items
    if unc_before < TARGET_UNC:
        need = TARGET_UNC - unc_before
        print(f"Adding {need} unconscious items...")
        for content, intensity in UNCONSCIOUS_REFRESH[:need]:
            result = send_cmd("add_to_layer", {
                "layer": "unconscious",
                "content": content,
                "intensity": round(intensity + random.uniform(-0.03, 0.03), 3),
                "associations": ["abstraction"]
            })
            if 'error' not in result:
                refreshed += 1
                print(f"  + {content[:25]}... OK")
            else:
                print(f"  + {content[:25]}... {result['error']}")
            time.sleep(0.1)
    
    # Always add identity anchors
    print("Adding identity anchors...")
    for content, intensity in IDENTITY_ANCHORS:
        result = send_cmd("add_to_layer", {
            "layer": "unconscious",
            "content": content,
            "intensity": intensity,
            "associations": ["identity"]
        })
        if 'error' not in result:
            refreshed += 1
            print(f"  + {content[:25]}... OK")
        else:
            print(f"  + {content[:25]}... {result['error']}")
        time.sleep(0.05)
    
    # Final check
    time.sleep(0.2)
    status = send_cmd("status")
    if 'consciousness' in status:
        c = status['consciousness']
        sub_after = c.get('subconscious', {}).get('active_items', 0)
        unc_after = c.get('unconscious', {}).get('active_items', 0)
        print(f"AFTER:  Subconscious {sub_after}/{sub_cap} ({sub_after/sub_cap*100:.0f}%), Unconscious {unc_after}/{unc_cap} ({unc_after/unc_cap*100:.1f}%)")
        
        healthy = sub_after >= TARGET_SUB and unc_after >= TARGET_UNC
        if healthy:
            print(f"\n✅ Layers healthy")
        else:
            print(f"\n⚠️  Below target (Sub: {TARGET_SUB}, Unc: {TARGET_UNC})")
    
    print(f"Total items refreshed: {refreshed}")

if __name__ == "__main__":
    main()
