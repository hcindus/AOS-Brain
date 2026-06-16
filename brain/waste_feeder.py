#!/usr/bin/env python3
"""
WASTE FEEDER - Monitors queue and feeds brain
Runs as daemon to process waste from Miles
All 3 integration methods:
1. API call to brain to update internal state
2. Write directly to brain's memory/state files
3. Update MEMORY.md with insights
"""

import json
import os
import time
import sys
import signal
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

QUEUE_FILE = "/root/.aos/brain/input/queue.jsonl"
PROCESSED_DIR = "/root/.aos/brain/input/processed"
LOG_FILE = "/root/.aos/brain/input/feeder.log"
MEMORY_FILE = "/root/.openclaw/workspace/MEMORY.md"
BRAIN_STATE_FILE = "/root/.aos/brain/state/miles_sync.json"
BRAIN_API_URL = "http://localhost:11435/api/status"

class WasteFeeder:
    def __init__(self):
        self.running = True
        self.processed_count = 0
        Path(PROCESSED_DIR).mkdir(parents=True, exist_ok=True)
        Path("/root/.aos/brain/state").mkdir(parents=True, exist_ok=True)
        
    def log(self, msg):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    
    def signal_handler(self, signum, frame):
        self.log("🛑 Received shutdown signal")
        self.running = False
    
    # ============================================================
    # METHOD 1: API call to brain to update internal state
    # ============================================================
    def update_brain_api(self, data):
        """Try to update brain via API (if endpoint exists)"""
        try:
            # Try various endpoints
            endpoints = [
                "http://localhost:11435/api/ingest",
                "http://localhost:11435/api/waste",
                "http://localhost:11435/api/sync",
            ]
            
            payload = json.dumps(data).encode('utf-8')
            
            for endpoint in endpoints:
                try:
                    req = urllib.request.Request(
                        endpoint,
                        data=payload,
                        headers={'Content-Type': 'application/json'}
                    )
                    urllib.request.urlopen(req, timeout=2)
                    self.log(f"✅ API updated: {endpoint}")
                    return True
                except urllib.error.HTTPError as e:
                    if e.code == 404:
                        continue  # Try next endpoint
                    self.log(f"⚠️ API error {e.code}: {e.reason}")
                except Exception as e:
                    continue  # Try next endpoint
            
            self.log(f"⚠️ No ingest API available (all endpoints returned 404)")
            return False
            
        except Exception as e:
            self.log(f"❌ API update failed: {e}")
            return False
    
    # ============================================================
    # METHOD 2: Write directly to brain's memory/state files
    # ============================================================
    def update_brain_state_file(self, data):
        """Write waste data to brain state file"""
        try:
            state = {
                "timestamp": data.get('timestamp'),
                "source": data.get('source'),
                "kidneys": data.get('kidneys'),
                "qmd": data.get('qmd'),
                "router": data.get('router'),
                "thyroid": data.get('thyroid'),
                "consciousness": data.get('consciousness'),
                "cortex": data.get('cortex'),
                "liver": data.get('liver'),
                "signal_quality": data.get('signal_quality'),
                "last_update": datetime.now().isoformat()
            }
            
            with open(BRAIN_STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
            
            self.log(f"✅ State file updated: {BRAIN_STATE_FILE}")
            return True
            
        except Exception as e:
            self.log(f"❌ State file update failed: {e}")
            return False
    
    # ============================================================
    # METHOD 3: Update MEMORY.md with insights
    # ============================================================
    def update_memory_md(self, data):
        """Extract insights and append to MEMORY.md"""
        try:
            kidneys = data.get('kidneys', {})
            qmd = data.get('qmd', {})
            router = data.get('router', {}).get('models', {})
            consciousness = data.get('consciousness', {})
            cortex = data.get('cortex', {})
            
            # Format insights
            insights = f"""
## 🧠 Miles Waste Ingest ({data.get('timestamp')})

### Kidneys
- State: {kidneys.get('state')}
- Total Processed: {kidneys.get('total_processed'):,}
- Noise Estimate: {kidneys.get('noise_estimate', 0):.4f}
- Unique Patterns: {kidneys.get('unique_patterns_seen'):,}

### QMD
- Total Cycles: {qmd.get('total_cycles'):,}
- Avg Latency: {qmd.get('avg_latency_ms', 0):.1f}ms

### Router Models
- Decision: {router.get('decision')}
- Voice: {router.get('voice')}
- Embedding: {router.get('embedding')}

### Consciousness
- Conscious: {consciousness.get('conscious',{}).get('active_items')}/{consciousness.get('conscious',{}).get('capacity')}
- Subconscious: {consciousness.get('subconscious',{}).get('active_items')}/{consciousness.get('subconscious',{}).get('capacity')}
- Unconscious: {consciousness.get('unconscious',{}).get('active_items')}/{consciousness.get('unconscious',{}).get('capacity')}

### Cortex
- Conscious Mean: {cortex.get('conscious_mean', 0):.4f}
- Subconscious Mean: {cortex.get('subconscious_mean', 0):.4f}

---
"""
            # Append to MEMORY.md
            with open(MEMORY_FILE, 'a') as f:
                f.write(insights)
            
            self.log(f"✅ MEMORY.md updated with insights")
            return True
            
        except Exception as e:
            self.log(f"❌ MEMORY.md update failed: {e}")
            return False
    
    def process_queue(self):
        """Read and process queue items"""
        if not os.path.exists(QUEUE_FILE):
            return 0
            
        processed_now = 0
        
        with open(QUEUE_FILE, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            return 0
        
        for i, line in enumerate(lines):
            try:
                item = json.loads(line.strip())
                self.process_item(item)
                processed_now += 1
                
                # Move to processed
                timestamp = item.get('timestamp', str(time.time()))
                processed_file = os.path.join(PROCESSED_DIR, f"processed_{timestamp.replace(':','-')}.json")
                with open(processed_file, 'w') as f:
                    f.write(line)
                    
            except json.JSONDecodeError as e:
                self.log(f"⚠️ JSON error: {e}")
                continue
        
        if processed_now > 0:
            with open(QUEUE_FILE, 'w') as f:
                f.write('')
            self.log(f"✅ Processed {processed_now} items, cleared queue")
        
        return processed_now
    
    def process_item(self, item):
        """Process a single queue item - apply all 3 methods"""
        self.processed_count += 1
        
        item_type = item.get('type', 'unknown')
        source = item.get('source', 'unknown')
        
        if item_type == 'waste_ingest':
            data = json.loads(item['text'])
            kidneys = data.get('kidneys', {})
            
            self.log(f"🧠 Waste: kidneys={kidneys.get('state')}, processed={kidneys.get('total_processed')}, noise={kidneys.get('noise_estimate', 0):.3f}")
            
            # METHOD 1: Try API update
            self.update_brain_api(data)
            
            # METHOD 2: Write state file
            self.update_brain_state_file(data)
            
            # METHOD 3: Update MEMORY.md
            self.update_memory_md(data)
            
        else:
            self.log(f"📥 {item_type} from {source}")
    
    def run(self):
        self.log("🚀 WasteFeeder starting (3 methods)...")
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        while self.running:
            try:
                processed = self.process_queue()
                time.sleep(2)
                
            except Exception as e:
                self.log(f"❌ Error: {e}")
                time.sleep(5)
        
        self.log(f"🛑 Stopped. Total processed: {self.processed_count}")

if __name__ == "__main__":
    feeder = WasteFeeder()
    feeder.run()