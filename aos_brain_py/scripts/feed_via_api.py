#!/usr/bin/env python3
"""
Feed dictionary via HTTP API to running brain daemon.
"""

import requests
import json
import time
import sys

API_URL = "http://localhost:5000"

def check_brain():
    try:
        resp = requests.get(f"{API_URL}/health", timeout=3)
        return resp.status_code == 200
    except:
        return False

def feed_word(text, source):
    try:
        resp = requests.post(
            f"{API_URL}/think",
            json={"text": text, "agent": source, "source": "dictionary_feed"},
            timeout=5
        )
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

print("="*70)
print("FEEDING DICTIONARY VIA HTTP API")
print("="*70)

# Check if brain is running
if not check_brain():
    print("❌ Brain not running. Start brain_daemon.py first.")
    print("   python3 brain_daemon.py foreground")
    sys.exit(1)

print("✅ Brain API responding")
print()

# Load dictionary
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.century_dictionary import get_20th_century_dictionary

words = get_20th_century_dictionary()
print(f"Feeding {len(words)} words...")
print()

fed = 0
for i, (word, pos, definition, category) in enumerate(words):
    result = feed_word(f"{word}: {definition}", f"century_{category}")
    fed += 1
    
    if (i + 1) % 50 == 0:
        tick = result.get('tick', '?')
        print(f"  Progress: {i+1}/{len(words)} words | Tick: {tick}")
        time.sleep(0.1)  # Small delay

print()
print("="*70)
print(f"✅ FED {fed} WORDS TO BRAIN")
print("="*70)
