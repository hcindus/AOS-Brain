#!/usr/bin/env python3
"""
AOS SLEEP SCHEDULER v1.0
Simulates sleep cycles for memory consolidation
"""

import json
import socket
import time
import subprocess
from datetime import datetime

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

def trigger_sleep_cycle():
    """Trigger a sleep cycle for consolidation"""
    print("  [SLEEP] Entering consolidation mode...")
    
    # Send rest signal to SuperiorHeart
    result = send_to_brain("command", {
        "action": "rest",
        "duration": 5
    })
    
    # Simulate slow-wave sleep (memory consolidation)
    print("  [SLEEP] Slow-wave phase: consolidating memories...")
    
    # Feed consolidation markers
    consolidation_items = [
        ("[DREAM] Pattern recognition strengthening", 0.9),
        ("[DREAM] OODA loop optimizing", 0.88),
        ("[DREAM] Identity anchors reinforcing", 0.95),
        ("[DREAM] Cross-layer communication enhancing", 0.85),
        ("[DREAM] Subconscious connections forming", 0.87),
    ]
    
    for content, importance in consolidation_items:
        send_to_brain("stimulate", {
            "importance": importance,
            "content": content,
            "type": "SLEEP_CONSOLIDATION"
        })
        time.sleep(0.5)
    
    # Wake up
    print("  [WAKE] Returning to active mode...")
    send_to_brain("command", {"action": "wake"})
    
    return True

def main():
    print("=" * 70)
    print("AOS SLEEP SCHEDULER v1.0")
    print("Memory Consolidation Through Simulated Sleep")
    print("=" * 70)
    
    print("\n[SCHEDULE] Creating sleep schedule...")
    print("  - Light sleep: Every 30 minutes (2 min)" )
    print("  - Deep sleep: Every 2 hours (5 min)")
    print("  - REM consolidation: Every 4 hours (3 min)")
    print("\n  Pattern: Light → Deep → Light → REM → Light → Deep → Light → REM")
    print("  Total cycle: 8 hours")
    
    print("\n" + "=" * 70)
    print("Starting first sleep cycle (press Ctrl+C to stop)...")
    print("=" * 70)
    
    cycle_count = 0
    schedule = [
        ("light", 2, 30 * 60),     # 2 min light, 30 min gap
        ("deep", 5, 2 * 60 * 60),   # 5 min deep, 2 hour gap  
        ("light", 2, 30 * 60),     # 2 min light, 30 min gap
        ("rem", 3, 4 * 60 * 60),   # 3 min REM, 4 hour gap
    ]
    
    try:
        while True:
            for sleep_type, duration_min, gap_seconds in schedule:
                cycle_count += 1
                now = datetime.now().strftime("%H:%M:%S")
                
                print(f"\n[{now}] CYCLE {cycle_count}: {sleep_type.upper()} SLEEP")
                print("-" * 50)
                
                if sleep_type == "light":
                    print("  [LIGHT] Quick memory refresh...")
                    send_to_brain("stimulate", {
                        "importance": 0.6,
                        "content": "[LIGHT SLEEP] Refreshing active memories",
                        "type": "LIGHT_SLEEP"
                    })
                    time.sleep(duration_min)
                    
                elif sleep_type == "deep":
                    print("  [DEEP] Entering slow-wave consolidation...")
                    trigger_sleep_cycle()
                    time.sleep(duration_min)
                    
                elif sleep_type == "rem":
                    print("  [REM] Active consolidation, pattern integration...")
                    for i in range(3):
                        send_to_brain("stimulate", {
                            "importance": 0.85,
                            "content": f"[REM] Integration phase {i+1}",
                            "type": "REM_SLEEP"
                        })
                        time.sleep(60)
                
                # Check status after each cycle
                status = send_to_brain("status")
                if 'consciousness' in status:
                    c = status['consciousness']
                    print(f"\n  Status after {sleep_type}:")
                    print(f"    Tick: {status.get('tick', 'N/A')}")
                    print(f"    Phase: {status.get('phase', 'N/A')}")
                    print(f"    Subconscious: {c['subconscious']['active_items']}/100")
                    print(f"    Unconscious: {c['unconscious']['active_items']}/1000")
                
                print(f"\n  Next cycle in {gap_seconds//60} minutes...")
                print(f"  (Press Ctrl+C to stop)")
                time.sleep(gap_seconds)
                
    except KeyboardInterrupt:
        print("\n\n[SCHEDULE] Sleep cycle interrupted by user.")
    
    print("\n" + "=" * 70)
    print(f"Completed {cycle_count} sleep cycles")
    print("=" * 70)
    
    # Final status
    status = send_to_brain("status")
    print(f"\nFinal Brain Status:")
    print(f"  Tick: {status.get('tick', 'N/A')}")
    print(f"  Thyroid: {status.get('thyroid', {}).get('state', 'N/A')}")
    
    if 'consciousness' in status:
        c = status['consciousness']
        print(f"\n  Consciousness Layers:")
        print(f"    Conscious:    {c['conscious']['active_items']}/{c['conscious']['capacity']}")
        print(f"    Subconscious: {c['subconscious']['active_items']}/{c['subconscious']['capacity']}")
        print(f"    Unconscious:  {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")
    
    print("\n[SCHEDULE] Sleep scheduler ready for background execution.")
    print("To run continuously, use: systemctl enable aos-sleep-scheduler")

if __name__ == "__main__":
    main()
