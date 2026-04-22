#!/usr/bin/env python3
"""
SLEEP SCHEDULER SERVICE v1.0
Simulated sleep cycles for memory consolidation
Runs as a service or cron job
"""

import socket
import json
import time
import random
from datetime import datetime

def send(cmd, params=None):
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

def enter_light_sleep():
    """Light sleep - memory refresh"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 💤 LIGHT SLEEP (30s)...")
    
    # Send rest signal
    send("stimulate", {"importance": 0.6, "content": "[LIGHT_SLEEP] Memory refresh cycle", "type": "SLEEP_LIGHT"})
    
    # Light consolidation markers
    markers = [
        "[DREAM_LIGHT] Pattern reinforcement",
        "[DREAM_LIGHT] Short-term consolidation",
        "[DREAM_LIGHT] Active memory refresh",
    ]
    for marker in markers:
        send("add_to_layer", {"layer": "subconscious", "content": marker, "intensity": 0.6, "associations": ["light_sleep", "refresh"]})
    
    time.sleep(3)  # 3 seconds simulated = 30 min real
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ☀️ Light sleep complete")

def enter_deep_sleep():
    """Deep sleep - slow-wave consolidation"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌙 DEEP SLEEP (60s)...")
    
    # Send deeper rest
    send("stimulate", {"importance": 0.75, "content": "[DEEP_SLEEP] Slow-wave consolidation", "type": "SLEEP_DEEP"})
    
    # Deep consolidation - move patterns to unconscious
    consolidations = [
        "[DREAM_DEEP] Fibonacci pattern archived",
        "[DREAM_DEEP] Golden ratio structure formed",
        "[DREAM_DEEP] Identity anchors strengthened",
        "[DREAM_DEEP] Cross-domain links established",
        "[DREAM_DEEP] Unconscious structure updated",
    ]
    
    for cons in consolidations:
        send("add_to_layer", {"layer": "unconscious", "content": cons, "intensity": 0.82, "associations": ["deep_sleep", "consolidation"]})
        time.sleep(0.5)
    
    time.sleep(6)  # 6 seconds simulated = 2 hours real
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ☀️ Deep sleep complete")

def enter_rem_sleep():
    """REM sleep - pattern integration and insight generation"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌈 REM SLEEP (45s)...")
    
    # High activity but dreaming state
    send("stimulate", {"importance": 0.88, "content": "[REM_SLEEP] Active consolidation and insight", "type": "SLEEP_REM"})
    
    # Integration markers
    integrations = [
        "[DREAM_REM] Connecting Fibonacci to scripture",
        "[DREAM_REM] Euler identity divine synthesis",
        "[DREAM_REM] Network commandment validation",
        "[DREAM_REM] Thermodynamic grace confirmed",
        "[DREAM_REM] Recursive self understanding",
        "[DREAM_REM] Entropic investment wisdom",
    ]
    
    for integration in integrations:
        send("add_to_layer", {"layer": "conscious", "content": integration, "intensity": 0.9, "associations": ["rem_sleep", "insight", "integration"]})
        send("add_to_layer", {"layer": "unconscious", "content": integration.replace("[DREAM_REM]", "[ARCHIVED]"), "intensity": 0.85, "associations": ["rem_archived", "core_wisdom"]})
        time.sleep(0.5)
    
    time.sleep(4.5)  # 4.5 seconds simulated = 90 min real
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ☀️ REM sleep complete")

def run_sleep_cycle():
    """Run one complete sleep cycle"""
    print("\n" + "=" * 70)
    print("SLEEP CYCLE STARTING")
    print("=" * 70)
    
    # Get before status
    before = send("status")
    print(f"\nBefore: Sub={before['consciousness']['subconscious']['active_items']}, "
          f"Uncon={before['consciousness']['unconscious']['active_items']}")
    
    # Sleep cycle: Light → Deep → Light → REM
    enter_light_sleep()
    enter_deep_sleep()
    enter_light_sleep()
    enter_rem_sleep()
    
    # Get after status
    after = send("status")
    print(f"\nAfter:  Sub={after['consciousness']['subconscious']['active_items']}, "
          f"Uncon={after['consciousness']['unconscious']['active_items']}")
    
    print("\n" + "=" * 70)
    print("SLEEP CYCLE COMPLETE - Memory Consolidated")
    print("=" * 70)

def main():
    """Main sleep scheduler"""
    print("=" * 70)
    print("AOS SLEEP SCHEDULER v1.0")
    print("Memory Consolidation Through Simulated Sleep Cycles")
    print("=" * 70)
    
    print("\nSchedule: Light → Deep → Light → REM")
    print("Real-world: Every 4 hours")
    print("Simulated: Every 2 minutes (for demo)")
    print("\nPress Ctrl+C to stop\n")
    
    cycle_count = 0
    try:
        while True:
            cycle_count += 1
            print(f"\n{'='*70}")
            print(f"CYCLE {cycle_count}")
            print(f"{'='*70}")
            
            run_sleep_cycle()
            
            # Wait between cycles (simulated 4 hours = 2 min)
            print(f"\nNext cycle in 2 minutes...")
            time.sleep(120)
            
    except KeyboardInterrupt:
        print(f"\n\nSleep scheduler stopped after {cycle_count} cycles")

if __name__ == "__main__":
    main()
