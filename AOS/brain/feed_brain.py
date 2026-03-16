#!/usr/bin/env python3
"""
Feed input to AOS Brain via file queue
"""

import json
import os
import time
import sys

INPUT_FILE = os.path.expanduser("~/.aos/brain/input/queue.jsonl")

def ensure_dir():
    os.makedirs(os.path.dirname(INPUT_FILE), exist_ok=True)

def feed_input(text, source="cli"):
    """Add input to brain queue"""
    ensure_dir()
    
    input_data = {
        "text": text,
        "source": source,
        "timestamp": time.time(),
        "type": "user_input"
    }
    
    with open(INPUT_FILE, 'a') as f:
        f.write(json.dumps(input_data) + '\n')
    
    print(f"✅ Fed to brain: {text[:50]}...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 feed_brain.py 'Your input here'")
        sys.exit(1)
    
    text = ' '.join(sys.argv[1:])
    feed_input(text)
    print(f"Brain will process on next tick (200ms)")
