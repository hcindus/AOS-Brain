#!/usr/bin/env python3
"""
AOS Brain Daemon - Lightweight server for ternary brain.

This is a minimal daemon that:
1. Runs the brain in a background process
2. Provides HTTP API on port 5000
3. Writes state to ~/.aos/brain/state/brain_state.json
4. Does NOT import heavy modules on startup

Usage:
    python brain_daemon.py [start|stop|status]
"""

import os
import sys
import json
import time
import signal
import atexit
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# Configuration
PID_FILE = Path.home() / ".aos" / "brain" / "daemon.pid"
STATE_DIR = Path.home() / ".aos" / "brain" / "state"
LOG_FILE = Path.home() / ".aos" / "logs" / "brain_daemon.log"
PORT = 5000

# Ensure directories exist
STATE_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

class BrainState:
    """Minimal brain state - no heavy imports."""
    def __init__(self):
        self.tick = 0
        self.mode = "Initializing"
        self.ternary = [0, 0, 0, 0, 0]
        self.short_term = []
        self.mid_term = []
        self.substrate_nodes = 0
        self.substrate_edges = 0
        self.running = True
        self.last_update = time.time()
    
    def process(self, text: str, agent: str) -> dict:
        """Simple processing - will be enhanced later."""
        self.tick += 1
        
        # Simple ternary logic
        self.ternary = [
            1 if "?" in text else 0,  # Novelty
            1 if len(text) > 20 else 0,  # Value
            1 if agent == "user" else 0,  # Action
            -1 if "error" in text.lower() else 0,  # Risk
            1 if self.tick % 10 == 0 else 0,  # Growth
        ]
        
        # Determine mode
        if self.ternary[3] == -1:
            self.mode = "Cautious"
        elif self.ternary[0] == 1:
            self.mode = "Exploratory"
        elif self.ternary[1] == 1:
            self.mode = "Analytical"
        else:
            self.mode = "Minimal"
        
        self.last_update = time.time()
        
        return {
            "tick": self.tick,
            "action": "respond",
            "reason": f"processed_{len(text)}_chars",
            "mode": self.mode,
            "language": f"[{self.mode}] Acknowledged: {text[:50]}...",
            "ternary": self.ternary,
            "confidence": 0.7,
            "agent": agent,
        }
    
    def to_dict(self) -> dict:
        return {
            "tick": self.tick,
            "mode": self.mode,
            "ternary": self.ternary,
            "memory": {
                "short_term": len(self.short_term),
                "mid_term": len(self.mid_term),
                "substrate": {
                    "nodes": self.substrate_nodes,
                    "edges": self.substrate_edges,
                },
            },
            "last_update": self.last_update,
        }

# Global state
brain = BrainState()

class BrainHandler(BaseHTTPRequestHandler):
    """HTTP handler for brain API."""
    
    def log_message(self, format, *args):
        """Custom logging."""
        with open(LOG_FILE, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {args[0]}\n")
    
    def _send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/health":
            self._send_json({
                "status": "healthy",
                "tick": brain.tick,
                "mode": brain.mode,
            })
        
        elif self.path == "/status":
            self._send_json(brain.to_dict())
        
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == "/think":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            
            try:
                req = json.loads(body)
                text = req.get("text", "")
                agent = req.get("agent", "default")
                
                result = brain.process(text, agent)
                self._write_state(result, text)
                self._send_json(result)
                
            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON"}, 400)
        
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def _write_state(self, result: dict, text: str):
        """Write brain state to JSON for visualizer."""
        state = {
            "tick": result["tick"],
            "timestamp": time.time(),
            "phase": result["action"].capitalize(),
            "mode": result["mode"],
            "limbic": {
                "reward": 0.3,
                "novelty": 1.0 if result["ternary"][0] == 1 else 0.0,
                "valence": 0.0,
            },
            "policy_nn": {
                "layers": 3,
                "nodes": [8, 12, 40],
                "activations": [[0.3]*8, [0.5]*12, [0.2]*40],
            },
            "memory_nn": {
                "clusters": brain.substrate_nodes,
                "edges": brain.substrate_edges,
            },
            "obs": {"input": text[:200]},
            "ternary": result["ternary"],
            "decision": result,
        }
        
        try:
            with open(STATE_DIR / "brain_state.json", "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            pass  # Silent fail for state write

def run_server():
    """Run the HTTP server."""
    server = HTTPServer(("0.0.0.0", PORT), BrainHandler)
    print(f"[BrainDaemon] Server running on port {PORT}")
    
    # Write PID file
    PID_FILE.write_text(str(os.getpid()))
    
    try:
        while brain.running:
            server.handle_request()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        if PID_FILE.exists():
            PID_FILE.unlink()

def daemonize():
    """Daemonize the process."""
    # First fork
    pid = os.fork()
    if pid > 0:
        return False  # Parent returns
    
    # Child process
    os.chdir(str(Path.home()))
    os.setsid()
    os.umask(0)
    
    # Second fork
    pid = os.fork()
    if pid > 0:
        os._exit(0)  # First child exits
    
    # Grandchild continues
    return True

def start_daemon():
    """Start the brain daemon."""
    if PID_FILE.exists():
        old_pid = int(PID_FILE.read_text().strip())
        try:
            os.kill(old_pid, 0)  # Check if process exists
            print(f"[BrainDaemon] Already running (PID {old_pid})")
            return
        except OSError:
            PID_FILE.unlink()  # Stale PID file
    
    print("[BrainDaemon] Starting daemon...")
    
    if daemonize():
        # Redirect output
        sys.stdout = open(LOG_FILE, "a")
        sys.stderr = open(LOG_FILE, "a")
        
        run_server()
    else:
        print(f"[BrainDaemon] Started (see {LOG_FILE})")

def stop_daemon():
    """Stop the brain daemon."""
    if not PID_FILE.exists():
        print("[BrainDaemon] Not running")
        return
    
    pid = int(PID_FILE.read_text().strip())
    
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"[BrainDaemon] Stopped (PID {pid})")
    except ProcessLookupError:
        print("[BrainDaemon] Process not found")
    except Exception as e:
        print(f"[BrainDaemon] Error: {e}")
    
    if PID_FILE.exists():
        PID_FILE.unlink()

def get_status():
    """Get daemon status."""
    if not PID_FILE.exists():
        print("[BrainDaemon] Not running")
        return
    
    pid = int(PID_FILE.read_text().strip())
    
    try:
        os.kill(pid, 0)
        print(f"[BrainDaemon] Running (PID {pid})")
        print(f"  State: {STATE_DIR}/brain_state.json")
        print(f"  Log: {LOG_FILE}")
    except OSError:
        print("[BrainDaemon] Stale PID file")
        PID_FILE.unlink()

def run_foreground():
    """Run server in foreground (for testing)."""
    print(f"[BrainDaemon] Starting in foreground on port {PORT}")
    print(f"  Health: http://localhost:{PORT}/health")
    print(f"  Think:  curl -X POST http://localhost:{PORT}/think -d '{{\"text\":\"hello\"}}'")
    print("  Press Ctrl+C to stop")
    run_server()

def main():
    """Main entry point."""
    cmd = sys.argv[1] if len(sys.argv) > 1 else "foreground"
    
    if cmd == "start":
        start_daemon()
    elif cmd == "stop":
        stop_daemon()
    elif cmd == "status":
        get_status()
    elif cmd == "foreground":
        run_foreground()
    else:
        print(f"Usage: {sys.argv[0]} [start|stop|status|foreground]")
        sys.exit(1)

if __name__ == "__main__":
    main()
