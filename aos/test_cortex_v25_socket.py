#!/usr/bin/env python3
"""
Test cortex v2.5 socket commands
"""
import socket
import json
import time

def send_cmd(cmd, params=None):
    """Send command to brain socket"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect('/tmp/aos_brain.sock')
        
        request = json.dumps({"cmd": cmd, "params": params or {}})
        sock.sendall(request.encode())
        
        data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            if len(chunk) < 4096:
                break
        
        sock.close()
        return json.loads(data.decode())
    except Exception as e:
        return {"error": str(e)}

def main():
    print("=" * 70)
    print("  CORTEX v2.5 SOCKET TEST")
    print("=" * 70)
    
    # Wait for socket
    time.sleep(2)
    
    # Test 1: Cortex stats
    print("\n[Test 1] cortex_stats")
    result = send_cmd("cortex_stats")
    print(f"  Result: {json.dumps(result, indent=2)[:500]}...")
    
    # Test 2: Register agent
    print("\n[Test 2] cortex_register")
    result = send_cmd("cortex_register", {"agent_id": "test_agent_1"})
    print(f"  Result: {result}")
    
    # Test 3: Write to cortex
    print("\n[Test 3] cortex_write")
    # Create some activations (x, y, z, ternary_value)
    activations = [[i % 16, (i*2) % 16, (i*3) % 16, 1] for i in range(10)]
    result = send_cmd("cortex_write", {
        "agent_id": "test_agent_1",
        "regions": [0, 1, 2],
        "activations": activations,
        "priority": 0.9
    })
    print(f"  Written: {result}")
    
    # Test 4: Read from cortex
    print("\n[Test 4] cortex_read")
    result = send_cmd("cortex_read", {
        "agent_id": "test_agent_1",
        "regions": [0, 1, 2],
        "max_hotspots": 32
    })
    print(f"  Read: {len(result.get('hotspots', []))} hotspots")
    print(f"  Coherence: {result.get('coherence', 'N/A')}")
    
    # Test 5: Cortex tick
    print("\n[Test 5] cortex_tick")
    result = send_cmd("cortex_tick")
    print(f"  Tick result: {result}")
    
    # Test 6: Stats again
    print("\n[Test 6] cortex_stats (after activity)")
    result = send_cmd("cortex_stats")
    if 'performance' in result:
        perf = result['performance']
        for key, data in list(perf.items())[:3]:
            print(f"  {key}: mean={data.get('mean_ms', 0):.3f}ms")
    
    print("\n" + "=" * 70)
    print("  SOCKET TESTS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    # Can also be run standalone after brain is running
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--wait":
        import time
        time.sleep(3)
    main()