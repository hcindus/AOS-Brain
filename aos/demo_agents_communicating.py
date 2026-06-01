#!/usr/bin/env python3
"""
DEMO: Two Agents Communicating Through Shared Cortex

Shows emergent coordination without message passing.
Agent 1 writes observations → Cortex state changes → Agent 2 reads and responds
"""

import time
import json
import socket

def send(cmd, params=None):
    """Send command to brain"""
    params = params or {}
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect('/tmp/aos_brain.sock')
        
        request = json.dumps({'cmd': cmd, 'params': params})
        sock.sendall(request.encode() + b'\n')
        
        data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            if len(chunk) < 4096:
                break
        
        sock.close()
        return json.loads(data.decode()) if data else {'error': 'no response'}
    except Exception as e:
        return {'error': str(e)}

print("=" * 70)
print("  AGENT COMMUNICATION DEMO")
print("  Showing emergent coordination through shared cortical state")
print("=" * 70)

# Step 1: Register both agents
print("\n[Setup] Registering Agent Alpha (observer) and Agent Beta (responder)")
send('cortex_register', {'agent_id': 'agent_alpha'})
send('cortex_register', {'agent_id': 'agent_beta'})
print("  ✓ Both agents registered")

# Step 2: Agent Alpha writes "anomaly detected" pattern
print("\n[Agent Alpha] Writing observation to cortex regions 0-1...")
anomaly_pattern = [
    [2, 2, 2, 1], [3, 3, 3, 1], [4, 4, 4, 1],   # Signal cluster
    [2, 3, 2, 1], [3, 2, 3, 1],                   # Neighbors
    [5, 5, 5, -1], [6, 6, 6, -1],                 # Contrast (negatives)
] * 3  # Repeat for strength

result = send('cortex_write', {
    'agent_id': 'agent_alpha',
    'regions': [0, 1],
    'activations': anomaly_pattern,
    'priority': 0.9,
    'ephemeral': False
})
print(f"  ✓ Written {result.get('write_result', {}).get('written', 0)} activations")

# Step 3: Tick to propagate
print("\n[Brain] Propagating patterns through cortex...")
send('cortex_tick')
time.sleep(0.5)

# Step 4: Agent Beta reads regions 0-1 (what Alpha wrote)
print("\n[Agent Beta] Reading cortex regions 0-1...")
read_alpha = send('cortex_read', {
    'agent_id': 'agent_beta',
    'regions': [0, 1],
    'max_hotspots': 20
})

coherence = read_alpha.get('coherence', 0)
hotspots = read_alpha.get('hotspots', [])
print(f"  Coherence detected: {coherence:.3f}")
print(f"  Hotspots found: {len(hotspots)}")

# Step 5: Agent Beta responds based on what it read
print("\n[Agent Beta] Responding to detected pattern...")
if coherence > 0.05:  # Threshold for "something is there"
    response_pattern = [
        [20, 20, 20, 1], [21, 21, 21, 1],   # Different region (escalation)
        [22, 22, 22, 1], [20, 21, 20, 1],
        [25, 25, 25, 1],  # Flag for "action taken"
    ]
    
    send('cortex_write', {
        'agent_id': 'agent_beta',
        'regions': [4, 5],  # Escalation regions
        'activations': response_pattern,
        'priority': 0.85,
        'ephemeral': False
    })
    print(f"  ✓ Beta wrote escalation pattern to regions 4-5")
else:
    print("  ~ No significant pattern detected, no response")

# Step 6: Agent Gamma (decider) reads both
print("\n[Agent Gamma] Reading combined state from all regions...")
send('cortex_register', {'agent_id': 'agent_gamma'})

read_all = send('cortex_read', {
    'agent_id': 'agent_gamma',
    'regions': list(range(8)),
    'max_hotspots': 40
})

total_hotspots = len(read_all.get('hotspots', []))
combined_coherence = read_all.get('coherence', 0)

print(f"  Total cortical activity: {total_hotspots} hotspots")
print(f"  Global coherence: {combined_coherence:.3f}")

# Step 7: Check temporal memory
print("\n[Agent Gamma] Querying temporal buffer...")
stats = send('cortex_stats')
frames = stats.get('current_tick', 0)
print(f"  Temporal depth: {frames} frames in buffer")

# Summary
print("\n" + "=" * 70)
print("  COMMUNICATION FLOW SUMMARY")
print("=" * 70)
print("""
  Agent Alpha (Observer)
     ↓
  Writes pattern to regions 0-1 (anomaly signal)
     ↓
  Cortex propagates → coherence rises
     ↓
  Agent Beta (Responder) 
     ↓
  Reads regions 0-1 → detects coherence
     ↓
  Writes escalation to regions 4-5
     ↓
  Agent Gamma (Decider)
     ↓
  Reads all regions → sees combined evidence
     ↓
  Could trigger action based on convergence

  NO DIRECT MESSAGES EXCHANGED BETWEEN AGENTS.
  Only shared cortical state.
""")

print("=" * 70)
print("  DEMO COMPLETE")
print("=" * 70)

# Show final stats
print("\n[Final Stats]")
final_stats = send('cortex_stats')
if 'performance' in final_stats:
    perf = final_stats['performance']
    tick_times = [v for k, v in perf.items() if 'tick' in k or 'full' in k]
    if tick_times:
        avg_time = sum(t.get('mean_ms', 0) for t in tick_times) / len(tick_times)
        print(f"  Average tick time: {avg_time:.2f}ms")
print(f"  Total registered agents: {len(final_stats.get('agents', {}))}")
