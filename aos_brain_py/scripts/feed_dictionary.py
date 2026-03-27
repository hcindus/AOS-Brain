#!/usr/bin/env python3
"""
Feed dictionary to running brain via HTTP API.
"""

import requests
import json
import time
import sys

API_URL = "http://localhost:5000"

def feed_dictionary():
    print("=" * 70)
    print("FEEDING DICTIONARY TO BRAIN")
    print("=" * 70)
    
    # Check brain
    try:
        resp = requests.get(f"{API_URL}/health", timeout=3)
        if resp.status_code != 200:
            print("❌ Brain not responding")
            return
        print("✅ Brain healthy")
    except Exception as e:
        print(f"❌ Brain error: {e}")
        return
    
    # Load dictionary
    sys.path.insert(0, '/root/.openclaw/workspace/aos_brain_py')
    from agents.century_dictionary import get_20th_century_dictionary
    
    words = get_20th_century_dictionary()
    print(f"\nLoaded {len(words)} words")
    print(f"Feeding via {API_URL}...")
    print()
    
    fed = 0
    errors = 0
    
    for i, (word, pos, definition, category) in enumerate(words):
        try:
            resp = requests.post(
                f"{API_URL}/think",
                json={"text": f"{word}: {definition}", "source": f"century_{category}"},
                timeout=2
            )
            if resp.status_code == 200:
                fed += 1
            else:
                errors += 1
        except Exception as e:
            errors += 1
            print(f"Error at {word}: {e}")
        
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i+1}/{len(words)} | Fed: {fed} | Errors: {errors}")
    
    print()
    print("=" * 70)
    print(f"✅ COMPLETE: {fed}/{len(words)} words fed")
    print(f"   Errors: {errors}")
    print("=" * 70)

if __name__ == "__main__":
    feed_dictionary()
