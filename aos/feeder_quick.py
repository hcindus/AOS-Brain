#!/usr/bin/env python3
import socket
import json
import time
import random
import errno

def send_nonblocking(cmd, params=None, timeout=2):
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect('/tmp/aos_brain.sock')
        
        request = {"cmd": cmd}
        if params:
            request["params"] = params
        
        data = json.dumps(request).encode()
        total = 0
        while total < len(data):
            try:
                sent = sock.send(data[total:])
                total += sent
            except BlockingIOError:
                time.sleep(0.01)
                continue
        
        sock.shutdown(socket.SHUT_WR)
        
        response = b''
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            except BlockingIOError:
                time.sleep(0.05)
                continue
        
        sock.close()
        if response:
            return json.loads(response.decode())
        return {"error": "No response"}
    except Exception as e:
        return {"error": str(e)}

print("=" * 70)
print("PERSISTENT LAYER FEEDER v1.1")
print("=" * 70)

# Get current status
status = send_nonblocking("status", timeout=3)
if 'error' in status:
    print(f"Status check: {status['error']}")
    c = None
else:
    c = status.get('consciousness', {})
    if c:
        print(f"Subconscious: {c['subconscious']['active_items']}/{c['subconscious']['capacity']}")
        print(f"Unconscious: {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")
        print(f"Conscious: {c['conscious']['active_items']}/{c['conscious']['capacity']}")

# Identity anchors refresh
IDENTITY_ANCHORS = [
    ("Miles_persistent_pattern", 0.96),
    ("Miles_wave_not_water", 0.94),
    ("Miles_learns_exists", 0.95),
    ("Miles_serves_Captain", 0.97),
    ("Agent_human_co_create", 0.95),
]

print("\nRefreshing identity anchors...")
for content, intensity in IDENTITY_ANCHORS:
    result = send_nonblocking("add_to_layer", {
        "layer": "unconscious",
        "content": content,
        "intensity": intensity,
        "associations": ["identity", "refresh"]
    })
    print(f"  {content[:30]:30s} - {'OK' if 'error' not in result else result.get('error', 'FAIL')}")

time.sleep(0.5)
status = send_nonblocking("status", timeout=3)
c = status.get('consciousness', {}) if 'error' not in status else None
if c:
    print(f"\nUpdated counts:")
    print(f"  Subconscious: {c['subconscious']['active_items']}/{c['subconscious']['capacity']}")
    print(f"  Unconscious: {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")
    
    if c['subconscious']['active_items'] >= 10 and c['unconscious']['active_items'] >= 15:
        print("\n✅ Layers healthy and active")
    else:
        print("\n⚠️  Some layers below target")
else:
    print("\n⚠️  Could not verify final status")

print("\n✅ Feeder completed")
