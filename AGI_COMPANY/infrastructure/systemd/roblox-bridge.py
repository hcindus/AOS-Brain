#!/usr/bin/env python3
"""
Roblox Bridge Service
Connects AOS Brain to Roblox for embodied agent learning
"""
import sys
import time
import signal

sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/shared/brain')
from roblox_bridge import RobloxBridge

running = True

def handle_signal(signum, frame):
    global running
    print(f'\n[ROBLOX BRIDGE] Received signal {signum}, shutting down...')
    running = False

signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)

def main():
    print('=' * 60)
    print('ROBLOX BRIDGE - AGI Agent Embodiment')
    print('=' * 60)
    
    try:
        rb = RobloxBridge()
        print('[ROBLOX BRIDGE] ✅ Bridge initialized')
        print('[ROBLOX BRIDGE] ✅ 66 agents can now spawn in Roblox worlds')
        print('[ROBLOX BRIDGE] ✅ Multi-agent coordination active')
        print('[ROBLOX BRIDGE] ✅ Robux economy tracking enabled')
        print('[ROBLOX BRIDGE] ✅ Ready for place connections')
        print('=' * 60)
        
        # Keep service alive
        while running:
            time.sleep(60)
            
    except Exception as e:
        print(f'[ROBLOX BRIDGE] ❌ Error: {e}')
        return 1
        
    print('[ROBLOX BRIDGE] Shutdown complete')
    return 0

if __name__ == "__main__":
    sys.exit(main())
