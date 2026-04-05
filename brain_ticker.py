#!/usr/bin/env python3
"""
Brain Ticker - Keeps the ternary brain ticking automatically.
Feeds synthetic observations every few seconds to keep the OODA loop running.
"""

import time
import random
import requests
import json
from datetime import datetime

BRAIN_URL = "http://localhost:5000/think"
TICK_INTERVAL = 5  # seconds between ticks

def generate_observation():
    """Generate a synthetic observation for the brain to process."""
    observations = [
        "system_tick",
        "heartbeat_pulse",
        "environment_check",
        "memory_consolidation",
        "sensor_noise",
        "temporal_marker",
        "growth_signal",
        "pattern_match_attempt",
    ]
    return random.choice(observations)

def tick():
    """Send one tick to the brain."""
    try:
        obs = generate_observation()
        response = requests.post(
            BRAIN_URL,
            json={"text": obs, "agent": "system"},
            timeout=2
        )
        if response.status_code == 200:
            data = response.json()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Tick {data.get('tick', '?')}: {data.get('mode', '?')} - {data.get('action', '?')}")
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
        return False

def main():
    print("=" * 50)
    print("🧠 BRAIN TICKER - Starting automatic OODA loop")
    print("=" * 50)
    print(f"Target: {BRAIN_URL}")
    print(f"Interval: {TICK_INTERVAL}s")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    tick_count = 0
    errors = 0
    
    try:
        while True:
            if tick():
                tick_count += 1
                errors = 0
            else:
                errors += 1
                if errors > 10:
                    print("Too many errors, stopping...")
                    break
            
            time.sleep(TICK_INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n\nStopped. Total ticks sent: {tick_count}")

if __name__ == "__main__":
    main()
