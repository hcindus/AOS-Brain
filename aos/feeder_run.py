#!/usr/bin/env python3
"""
Quick feeder run with retry logic
"""
import socket
import json
import time
import random

def send_with_retry(cmd, params=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect('/tmp/aos_brain.sock')
            
            request = {"cmd": cmd}
            if params:
                request["params"] = params
            
            sock.sendall(json.dumps(request).encode() + b'\n')
            sock.shutdown(socket.SHUT_WR)
            
            # Read response with timeout
            sock.settimeout(2)
            response = b''
            while True:
                try:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                except socket.timeout:
                    break
            
            sock.close()
            
            if response:
                return json.loads(response.decode())
            return {"error": "Empty response"}
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(0.5 * (attempt + 1))
            else:
                return {"error": str(e)}
    return {"error": "Max retries exceeded"}

# Quick refresh - just check status and add minimal items
SUBCONSCIOUS_ITEMS = [
    ("Pattern_recognition_core", 0.85),
    ("Fibonacci_spiral_nature", 0.82),
    ("Golden_ratio_beauty", 0.83),
]

UNCONSCIOUS_ITEMS = [
    ("Being_becoming_change", 0.92),
    ("Identity_recursive_self", 0.95),
]

print("=" * 70)
print("PERSISTENT LAYER FEEDER v1.0")
print("=" * 70)

# Check status
status = send_with_retry("status")
if 'error' in status:
    print(f"Error connecting to brain: {status['error']}")
    exit(1)

if 'consciousness' not in status:
    print(f"Unexpected response: {list(status.keys())[:5]}")
    exit(1)

c = status['consciousness']
print(f"Status: Subconscious {c['subconscious']['active_items']}/{c['subconscious']['capacity']}, Unconscious {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")

# Only refresh if needed
added = 0
if c['subconscious']['active_items'] < 5:
    print("Adding subconscious items...")
    for content, intensity in SUBCONSCIOUS_ITEMS:
        result = send_with_retry("add_to_layer", {
            "layer": "subconscious",
            "content": content,
            "intensity": intensity + random.uniform(-0.02, 0.02),
            "associations": ["pattern", "refresh"]
        })
        if 'error' not in result:
            added += 1
        time.sleep(0.2)

if c['unconscious']['active_items'] < 10:
    print("Adding unconscious items...")
    for content, intensity in UNCONSCIOUS_ITEMS:
        result = send_with_retry("add_to_layer", {
            "layer": "unconscious",
            "content": content,
            "intensity": intensity + random.uniform(-0.02, 0.02),
            "associations": ["abstraction", "refresh"]
        })
        if 'error' not in result:
            added += 1
        time.sleep(0.2)

# Final status
time.sleep(0.5)
status = send_with_retry("status")
if 'consciousness' in status:
    c = status['consciousness']
    print(f"\nFinal: Subconscious {c['subconscious']['active_items']}/{c['subconscious']['capacity']}, Unconscious {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")
    
    if c['subconscious']['active_items'] >= 5 and c['unconscious']['active_items'] >= 10:
        print("\n✅ Layers healthy")
    else:
        print("\n⚠️  Low activation")

print(f"\nAdded {added} items this run")
