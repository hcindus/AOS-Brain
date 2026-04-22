#!/usr/bin/env python3
"""
VERIFY LAYERS - Check if subconscious/unconscious actually seeded
"""

import socket
import json

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

print("=" * 70)
print("LAYER VERIFICATION")
print("=" * 70)

# Get full status
status = send("status")
print("\nFull Status:")
print(json.dumps(status, indent=2))

# Check consciousness specifically
if 'consciousness' in status:
    c = status['consciousness']
    print(f"\n--- Consciousness Status ---")
    print(f"  Conscious:    {c['conscious']['active_items']}/{c['conscious']['capacity']}")
    print(f"  Subconscious: {c['subconscious']['active_items']}/{c['subconscious']['capacity']}")
    print(f"  Unconscious:  {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")
    print(f"  Cross-talk:   {c['cross_talk_events']}")

# Re-seed if needed
if c['subconscious']['active_items'] == 0:
    print("\n" + "=" * 70)
    print("RE-SEEDING LAYERS")
    print("=" * 70)
    result = send("seed_layers")
    print(json.dumps(result, indent=2))

# Check again
status = send("status")
if 'consciousness' in status:
    c = status['consciousness']
    print(f"\n--- After Re-Seed ---")
    print(f"  Conscious:    {c['conscious']['active_items']}/10")
    print(f"  Subconscious: {c['subconscious']['active_items']}/100")
    print(f"  Unconscious:  {c['unconscious']['active_items']}/1000")

print("\n" + "=" * 70)
