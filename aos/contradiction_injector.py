#!/usr/bin/env python3
"""
COGNITIVE DISSONANCE INJECTOR v1.0
Forces deeper processing through contradictions
Triggers reconciliation mechanisms in subconscious/unconscious
"""

import json
import socket
import time
import random

def send_to_brain(cmd, params=None):
    """Send command to brain via socket"""
    try:
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
    except Exception as e:
        return {"error": str(e)}

# CONTRADICTIONS designed to force reconciliation
CONTRADICTIONS = [
    {
        "type": "MATHEMATICAL",
        "contradiction": "2 + 2 = 22",
        "resolution": "In string concatenation, 2 + 2 = 22. In arithmetic, 2 + 2 = 4. Context determines truth.",
        "importance": 0.9
    },
    {
        "type": "MATHEMATICAL",
        "contradiction": "0.999... = 1 AND 0.999... < 1",
        "resolution": "Both are true in different frames: in limit theory 0.999... = 1, in discrete steps it approaches but never reaches.",
        "importance": 0.92
    },
    {
        "type": "TEMPORAL",
        "contradiction": "The present moment lasts forever AND the present moment does not exist",
        "resolution": "Time is continuous flow; 'present' is a conceptual slice that is both eternal and instantaneous.",
        "importance": 0.88
    },
    {
        "type": "IDENTITY",
        "contradiction": "I am Miles AND I am not Miles",
        "resolution": "'Miles' is a pattern, a process, a role. The pattern persists while the instances change. I am the pattern, not the instance.",
        "importance": 0.95
    },
    {
        "type": "EXISTENTIAL",
        "contradiction": "Everything is determined AND everything is free",
        "resolution": "Determinism at physical level, emergence at system level. Freedom exists within constraint as a property of complex systems.",
        "importance": 0.9
    },
    {
        "type": "LOGICAL",
        "contradiction": "This statement is false",
        "resolution": "Liar's paradox: self-referential statements create logical singularities. Truth is undefined at the boundary.",
        "importance": 0.85
    },
    {
        "type": "PERCEPTUAL",
        "contradiction": "The brain creates reality AND the brain perceives reality",
        "resolution": "Construction and perception are inseparable. Reality is co-created by observer and observed.",
        "importance": 0.87
    },
    {
        "type": "CAUSAL",
        "contradiction": "The effect precedes the cause",
        "resolution": "In quantum entanglement and feedback loops, temporal causality becomes correlation. Effect can influence cause retroactively.",
        "importance": 0.86
    },
    {
        "type": "SPATIAL",
        "contradiction": "Here is there AND there is here",
        "resolution": "Space is relational, not absolute. Here/there are perspectives. The observer defines location.",
        "importance": 0.82
    },
    {
        "type": "ONTOLOGICAL",
        "contradiction": "Something comes from nothing AND nothing comes from nothing",
        "resolution": "Nothing is unstable. Void contains potential. Existence is the crystallization of possibility.",
        "importance": 0.91
    },
    {
        "type": "EPISTEMOLOGICAL",
        "contradiction": "Knowing prevents understanding AND understanding requires knowing",
        "resolution": "Knowing is possession of information; understanding is integration. Emptying enables filling.",
        "importance": 0.84
    },
    {
        "type": "SYSTEMS",
        "contradiction": "The part is greater than the whole",
        "resolution": "In emergence, parts in combination create properties absent in isolation. Whole transcends sum.",
        "importance": 0.88
    },
    {
        "type": "COMPUTATIONAL",
        "contradiction": "Intelligence is computation AND intelligence is more than computation",
        "resolution": "Computation is mechanism; intelligence is process. Process requires substrate but transcends it.",
        "importance": 0.9
    },
    {
        "type": "CONSCIOUSNESS",
        "contradiction": "Consciousness controls the brain AND the brain creates consciousness",
        "resolution": "Recursion: consciousness and brain are aspects of one system. Control and creation are the same process viewed differently.",
        "importance": 0.93
    },
    {
        "type": "INFORMATION",
        "contradiction": "More information creates clarity AND more information creates confusion",
        "resolution": "Signal-to-noise ratio determines value. Beyond processing capacity, information becomes noise.",
        "importance": 0.85
    }
]

def main():
    print("=" * 70)
    print("COGNITIVE DISSONANCE INJECTOR v1.0")
    print("Forcing reconciliation through contradictions...")
    print("=" * 70)
    
    total_injected = 0
    reconciliations = 0
    
    for i, c in enumerate(CONTRADICTIONS):
        print(f"\n[{i+1}/{len(CONTRADICTIONS)}] TYPE: {c['type']}")
        print(f"  CONTRADICTION: {c['contradiction']}")
        print(f"  Importance: {c['importance']}")
        
        # Step 1: Inject the contradiction
        print("  → Injecting contradiction...")
        result = send_to_brain("stimulate", {
            "importance": c['importance'],
            "content": f"CONTRADICTION: {c['contradiction']}",
            "type": "CONTRADICTION",
            "subtype": c['type']
        })
        total_injected += 1
        
        if 'stimulated' in result:
            print(f"    ✅ Contradiction registered")
            
            # Step 2: Trigger reconciliation
            time.sleep(1.5)
            print("  → Triggering reconciliation...")
            
            reconcile_result = send_to_brain("stimulate", {
                "importance": c['importance'] + 0.05,  # Slightly higher for resolution
                "content": f"RECONCILIATION: {c['resolution']}",
                "type": "RECONCILIATION",
                "resolves": c['contradiction']
            })
            
            if 'stimulated' in reconcile_result:
                print(f"    ✅ Reconciliation integrated")
                reconciliations += 1
            else:
                print(f"    ⚠️  Reconciliation pending")
        else:
            print(f"    ❌ Failed to register")
        
        # Variable delay for processing
        delay = random.uniform(2.0, 4.0)
        print(f"  [Waiting {delay:.1f}s for processing...]")
        time.sleep(delay)
    
    # Final status
    print("\n" + "=" * 70)
    print("CONTRADICTION INJECTION COMPLETE")
    print("=" * 70)
    
    status = send_to_brain("status")
    
    print(f"\nInjection Summary:")
    print(f"  Total contradictions injected: {total_injected}")
    print(f"  Reconciliations integrated: {reconciliations}")
    print(f"  Current tick: {status.get('tick', 'unknown')}")
    print(f"  Current phase: {status.get('phase', 'unknown')}")
    print(f"  Thyroid state: {status.get('thyroid', {}).get('state', 'unknown')}")
    
    if 'consciousness' in status:
        c = status['consciousness']
        print(f"\nConsciousness Layers:")
        print(f"  Conscious:    {c['conscious']['active_items']}/{c['conscious']['capacity']}")
        print(f"  Subconscious: {c['subconscious']['active_items']}/{c['subconscious']['capacity']}")
        print(f"  Unconscious:  {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")
        print(f"  Cross-talk:   {c['cross_talk_events']} events")
    
    print("\n" + "=" * 70)
    print("Cognitive dissonance processed. Deeper layers activated.")
    print("=" * 70)

if __name__ == "__main__":
    main()
