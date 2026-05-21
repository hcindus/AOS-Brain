#!/usr/bin/env python3
"""
AOS Brain Academy Feeder v4.3
Feed curriculum from aos-brain-academy-v2-mortimer-enhanced.json
"""

import json
import socket
import time
import random
import sys
import os

CURRICULUM_FILE = "/root/.aos/aos/curriculum/aos-brain-academy-v2-mortimer-enhanced.json"
FEED_INTERVAL = 5  # seconds between items

def load_curriculum():
    """Load the academy curriculum"""
    with open(CURRICULUM_FILE, 'r') as f:
        return json.load(f)

def extract_all_content(academy):
    """Extract all learning content from academy"""
    items = []
    
    for stage in academy.get('stages', []):
        stage_num = stage.get('stage', 0)
        stage_name = stage.get('name', 'Unknown')
        
        for module in stage.get('modules', []):
            content = module.get('content', '')
            if content:
                items.append({
                    'stage': stage_num,
                    'stage_name': stage_name,
                    'module': module.get('module_id', 'UNK'),
                    'name': module.get('name', 'Unknown'),
                    'content': content[:300] if len(content) > 300 else content,
                    'type': module.get('name', 'General').split()[0].lower(),
                    'importance': random.uniform(0.6, 0.95)
                })
    
    return items

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

def feed_item(item, index, total):
    """Feed a single curriculum item"""
    print(f"\n[{index+1}/{total}] Stage {item['stage']}: {item['stage_name']}")
    print(f"    Module: {item['module']} - {item['name']}")
    print(f"    Content: {item['content'][:80]}...")
    print(f"    Importance: {item['importance']:.2f}")
    
    # Stimulate thyroid
    result = send_to_brain("stimulate", {"importance": item['importance']})
    if result.get('stimulated'):
        print(f"    🫁 THYROID SECRETING → OLLAMA hormone released!")
    else:
        print(f"    🫁 Thyroid: BASELINE (no stimulation)")
    
    # Get status
    status = send_to_brain("status")
    thyroid = status.get('thyroid', {})
    
    print(f"    State: {thyroid.get('state', 'unknown')} | "
          f"Ollama: {thyroid.get('ollama_level', 0):.2f} | "
          f"Tick: {status.get('tick', 0)}")

def main():
    print("=" * 70)
    print("  📚 AOS BRAIN ACADEMY FEEDER v4.3")
    print("  Streaming Mortimer Enhanced Curriculum")
    print("=" * 70)
    
    if not os.path.exists(CURRICULUM_FILE):
        print(f"\n❌ Curriculum file not found: {CURRICULUM_FILE}")
        sys.exit(1)
    
    # Load curriculum
    academy = load_curriculum()
    items = extract_all_content(academy)
    
    print(f"\n📖 Academy: {academy.get('academy_name', 'Unknown')}")
    print(f"   Version: {academy.get('version', '1.0')}")
    print(f"   Philosophy: {academy.get('philosophy', '')[:60]}...")
    print(f"   Total learning items: {len(items)}")
    
    # Check brain
    ping = send_to_brain("ping")
    if ping.get('error'):
        print(f"\n❌ Brain not responding: {ping['error']}")
        sys.exit(1)
    
    print(f"\n✅ Brain connected (tick: {ping.get('tick', 0)})")
    print(f"⏱️  Feed interval: {FEED_INTERVAL}s")
    print("\nStarting academy feed... (Ctrl+C to stop)\n")
    
    try:
        for i, item in enumerate(items):
            feed_item(item, i, len(items))
            time.sleep(FEED_INTERVAL)
        
        print("\n" + "=" * 70)
        print("  ✅ Academy feed complete!")
        print("=" * 70)
        
        # Final status
        final = send_to_brain("status")
        thyroid = final.get('thyroid', {})
        print(f"\nFinal Thyroid State:")
        print(f"  State: {thyroid.get('state', 'unknown')}")
        print(f"  Ollama hormone: {thyroid.get('ollama_level', 0):.2f}")
        print(f"  Local hormone: {thyroid.get('local_level', 0):.2f}")
        print(f"  Secretions today: {thyroid.get('secretions_today', 0)}")
        print(f"  Total ticks: {final.get('tick', 0)}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Academy feed stopped by user")

if __name__ == "__main__":
    main()
