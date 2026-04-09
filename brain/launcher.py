#!/usr/bin/env python3
"""
Brain Launcher with Watchdog
Ensures brain starts or fails fast
"""

import sys
import signal
import threading
import time

# Set a global timeout
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out")

signal.signal(signal.SIGALRM, timeout_handler)

# Add brain path
sys.path.insert(0, '/root/.aos/aos/brain')

print("=" * 60)
print("Brain Launcher with 30-second watchdog")
print("=" * 60)

try:
    signal.alarm(30)  # 30 second timeout
    
    print("\n1. Importing OODA...")
    from ooda import OODA
    print("   ✓ OODA imported")
    
    print("\n2. Loading config...")
    import yaml
    from pathlib import Path
    cfg = yaml.safe_load(open(Path.home() / '.aos' / 'config' / 'brain.yaml'))
    print(f"   ✓ Config loaded")
    
    print("\n3. Creating OODA instance...")
    ooda = OODA(cfg)
    print("   ✓ OODA created!")
    
    signal.alarm(0)  # Cancel timeout
    
    print("\n4. Starting OODA loop...")
    tick_ms = cfg["brain"]["ooda"]["tick_interval_ms"]
    
    while True:
        ooda.tick()
        time.sleep(tick_ms / 1000.0)
        
except TimeoutException:
    print("\n❌ FAILED: Brain initialization timed out after 30 seconds")
    print("Likely cause: Ollama not responding during MemoryBridge initialization")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
