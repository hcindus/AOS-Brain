#!/usr/bin/env python3
"""
CONSCIOUSNESS DIRECT INSPECTOR
Bypasses status API to see actual layer contents
"""

import socket
import json

def send_raw(cmd, params=None):
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

# Get full status
print("=" * 70)
print("CONSCIOUSNESS DIRECT INSPECTOR")
print("=" * 70)

status = send_raw("status")

print(f"\nTick: {status.get('tick')}")
print(f"Phase: {status.get('phase')}")

if 'consciousness' in status:
    c = status['consciousness']
    print(f"\n--- Conscious Layer ---")
    print(f"  Active: {c['conscious']['active_items']}/{c['conscious']['capacity']}")
    
    print(f"\n--- Subconscious Layer ---")
    print(f"  Active: {c['subconscious']['active_items']}/{c['subconscious']['capacity']}")
    
    print(f"\n--- Unconscious Layer ---")
    print(f"  Active: {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")
    
    print(f"\n--- Cross-Talk ---")
    print(f"  Events: {c['cross_talk_events']}")
    
    # Check if there's raw data
    print(f"\n--- Raw Keys in Status ---")
    for key in status.keys():
        print(f"  {key}")
else:
    print("No consciousness data in status")

# Try to stimulate with high importance and check
print("\n" + "=" * 70)
print("TESTING STIMULATION -> PERCEPTION PIPELINE")
print("=" * 70)

# Stimulate thyroid to get high intensity
test_phrases = [
    ("Miles dreaming Miles dreaming Miles", 0.95),
    ("Recursive identity is identity of recursion", 0.9),
    ("The dream dreams the dreamer", 0.92),
]

for phrase, imp in test_phrases:
    print(f"\nStimulating: {phrase[:40]}... (importance {imp})")
    result = send_raw("stimulate", {"importance": imp, "content": phrase})
    print(f"  Result: {result}")

# Check status again
print("\n" + "=" * 70)
print("POST-STIMULATION STATUS")
print("=" * 70)

status = send_raw("status")
if 'consciousness' in status:
    c = status['consciousness']
    print(f"\nConscious: {c['conscious']['active_items']}/10")
    print(f"Subconscious: {c['subconscious']['active_items']}/100")
    print(f"Unconscious: {c['unconscious']['active_items']}/1000")
    print(f"Cross-talk: {c['cross_talk_events']}")

print("\n" + "=" * 70)
print("Inspection complete.")
print("=" * 70)
