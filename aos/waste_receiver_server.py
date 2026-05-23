#!/usr/bin/env python3
"""
WASTE RECEIVER SERVER
Runs alongside Miles' brain to consume waste data
"""

import json
import time
import threading
import os
import sys
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request

class WasteReceiverBrain:
    """
    Receiver brain that:
    1. Receives waste from Miles via HTTP
    2. Stores waste data
    3. Extracts patterns
    4. Feeds local learning
    """
    
    def __init__(self, data_dir="/root/.aos/waste_receiver_data", port=7474):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        (self.data_dir / "patterns").mkdir(exist_ok=True)
        
        self.port = port
        self.tick = 0
        self.running = False
        self.waste_received = 0
        self.patterns_extracted = 0
        
        self.waste_queues = {
            "kidneys": [],
            "qmd": [],
            "consciousness": [],
            "noise": [],
            "patterns": []
        }
        
        print(f"[WasteReceiverBrain] Initialized on port {port}")
        print(f"  Data directory: {self.data_dir}")
    
    def start(self):
        """Start HTTP server and processing loop"""
        self.running = True
        
        # Start HTTP server
        server_thread = threading.Thread(target=self._run_server, daemon=True)
        server_thread.start()
        
        # Start processing loop
        process_thread = threading.Thread(target=self._process_loop, daemon=True)
        process_thread.start()
        
        print(f"[WasteReceiverBrain] Running on port {self.port}")
        print(f"  Endpoints: http://localhost:{self.port}/waste (POST)")
        print(f"            http://localhost:{self.port}/status (GET)")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the receiver"""
        self.running = False
        self._save_state()
        print("[WasteReceiverBrain] Stopped")
    
    def _run_server(self):
        """HTTP server to receive waste"""
        brain = self
        
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass
            
            def do_POST(self):
                if self.path == "/waste":
                    content_length = int(self.headers.get('Content-Length', 0))
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        waste_data = json.loads(post_data.decode())
                        brain.receive_waste(waste_data)
                        
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "status": "received",
                            "waste_count": brain.waste_received
                        }).encode())
                    except Exception as e:
                        self.send_response(400)
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_GET(self):
                if self.path == "/status":
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    status = {
                        "status": "running",
                        "tick": brain.tick,
                        "waste_received": brain.waste_received,
                        "patterns_extracted": brain.patterns_extracted,
                        "queues": {k: len(v) for k, v in brain.waste_queues.items()}
                    }
                    self.wfile.write(json.dumps(status).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
        
        server = HTTPServer(('0.0.0.0', self.port), Handler)
        print(f"[HTTP Server] Listening on port {self.port}")
        server.serve_forever()
    
    def _process_loop(self):
        """Background processing of waste"""
        while self.running:
            self.tick += 1
            self._process_waste_queues()
            
            if self.tick % 100 == 0:
                self._report_status()
            
            time.sleep(0.1)
    
    def receive_waste(self, waste_data):
        """Receive waste from Miles"""
        timestamp = datetime.now().isoformat()
        
        # Save raw waste
        waste_file = self.data_dir / f"waste_{timestamp.replace(':', '-')}.json"
        with open(waste_file, 'w') as f:
            json.dump(waste_data, f, indent=2)
        
        self.waste_received += 1
        
        # Categorize
        if "kidneys" in waste_data:
            self.waste_queues["kidneys"].append(waste_data["kidneys"])
        if "qmd" in waste_data:
            self.waste_queues["qmd"].append(waste_data["qmd"])
        if "consciousness" in waste_data:
            self.waste_queues["consciousness"].append(waste_data["consciousness"])
        if waste_data.get("signal_quality", 1.0) < 0.8:
            self.waste_queues["noise"].append({
                "timestamp": timestamp,
                "quality": waste_data.get("signal_quality"),
                "source": "miles_low_quality"
            })
        
        print(f"[Waste] Received #{self.waste_received}")
    
    def _process_waste_queues(self):
        """Extract patterns from waste"""
        # Process kidneys
        while self.waste_queues["kidneys"]:
            kidneys = self.waste_queues["kidneys"].pop(0)
            if kidneys.get("bladder_level", 0) > 400:
                self._add_pattern("high_bladder", kidneys)
            if kidneys.get("noise_estimate", 0) > 0.5:
                self._add_pattern("high_noise", kidneys)
        
        # Process QMD
        while self.waste_queues["qmd"]:
            qmd = self.waste_queues["qmd"].pop(0)
            if qmd.get("avg_latency_ms", 0) > 5000:
                self._add_pattern("high_qmd_latency", qmd)
        
        # Save patterns batch
        if len(self.waste_queues["patterns"]) >= 10:
            self._save_patterns()
    
    def _add_pattern(self, pattern_type, data):
        """Add extracted pattern"""
        self.waste_queues["patterns"].append({
            "type": pattern_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        self.patterns_extracted += 1
    
    def _save_patterns(self):
        """Save patterns to file"""
        patterns = self.waste_queues["patterns"][:10]
        self.waste_queues["patterns"] = self.waste_queues["patterns"][10:]
        
        pattern_file = self.data_dir / "patterns" / f"patterns_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(pattern_file, 'w') as f:
            json.dump(patterns, f, indent=2)
        
        print(f"[Patterns] Saved {len(patterns)} to {pattern_file.name}")
    
    def _save_state(self):
        """Save state"""
        state = {
            "tick": self.tick,
            "waste_received": self.waste_received,
            "patterns_extracted": self.patterns_extracted,
            "timestamp": datetime.now().isoformat()
        }
        with open(self.data_dir / "receiver_state.json", 'w') as f:
            json.dump(state, f, indent=2)
    
    def _report_status(self):
        """Print status"""
        print(f"[Status] Tick {self.tick} | Waste: {self.waste_received} | Patterns: {self.patterns_extracted}")

if __name__ == "__main__":
    import signal
    
    brain = WasteReceiverBrain()
    
    def signal_handler(sig, frame):
        brain.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    brain.start()
