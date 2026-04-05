#!/usr/bin/env python3
"""
Ternary Brain Server - Unix socket + REST API.

Combines:
- User's cortical sheet implementation (TernaryCorticalSheet3D)
- My ternary OODA brain (3-tier memory)
- Flask REST API for agent integration
- brain_state.json writer for visualizer compatibility

Ports:
- 5000: Main brain API (/think, /status)
- 6000: Health/metrics endpoint
"""

import os
import sys
import json
import math
import time
import threading
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.ternary_ooda import TernaryOodaBrain, Observation
from brain.cortex import QMDAwareCortex
from substrate.graph_store import GraphStore
from visualizer.brain_visualizer import BrainVisualizer


# =========================
# Ternary Neuron (from user code)
# =========================

class TernaryNeuron:
    """
    Ternary neuron: -1 (inhibit), 0 (rest), +1 (excite)
    """
    def __init__(self):
        self.state = 0
    
    def activate(self, x: float, pos_thresh: float = 0.3, neg_thresh: float = -0.3) -> int:
        """Activate based on weighted input."""
        if x > pos_thresh:
            self.state = +1
        elif x < neg_thresh:
            self.state = -1
        else:
            self.state = 0
        return self.state


# =========================
# 3D Cortical Sheet (from user code, enhanced)
# =========================

@dataclass
class TernaryCorticalSheet3D:
    """
    3D ternary cortical sheet with wave propagation.
    
    Dimensions: nx × ny × nz
    State: ternary values per cell
    Weights: Hebbian plasticity
    """
    nx: int = 12
    ny: int = 12
    nz: int = 6
    
    state: List[int] = field(init=False)
    next_state: List[int] = field(init=False)
    weight: List[float] = field(init=False)
    
    def __post_init__(self):
        n = self.nx * self.ny * self.nz
        self.state = [0] * n
        self.next_state = [0] * n
        self.weight = [1.0] * n
    
    def index(self, x: int, y: int, z: int) -> int:
        """Convert 3D coordinates to 1D index."""
        return x + self.nx * (y + self.ny * z)
    
    def in_bounds(self, x: int, y: int, z: int) -> bool:
        """Check if coordinates are within sheet bounds."""
        return 0 <= x < self.nx and 0 <= y < self.ny and 0 <= z < self.nz
    
    def excite_region(self, cx: int, cy: int, cz: int, radius: int, value: int = +1):
        """Excite/inhibit a spherical region."""
        for x in range(cx - radius, cx + radius + 1):
            for y in range(cy - radius, cy + radius + 1):
                for z in range(cz - radius, cz + radius + 1):
                    if not self.in_bounds(x, y, z):
                        continue
                    dx, dy, dz = x - cx, y - cy, z - cz
                    if dx*dx + dy*dy + dz*dz <= radius * radius:
                        self.state[self.index(x, y, z)] = value
    
    def hebbian_update(self, eta: float = 0.01):
        """Hebbian learning: cells that fire together, wire together."""
        for i, s in enumerate(self.state):
            if s == 0:
                continue
            self.weight[i] += eta * s
            self.weight[i] = max(-5.0, min(5.0, self.weight[i]))
    
    def step_wave(self, decay: float = 0.9):
        """
        Propagate waves through the sheet.
        
        Each cell receives input from neighbors and updates state.
        """
        # 6-connected neighborhood
        offsets = [
            ( 1, 0, 0), (-1, 0, 0),
            ( 0, 1, 0), ( 0,-1, 0),
            ( 0, 0, 1), ( 0, 0,-1),
        ]
        
        for x in range(self.nx):
            for y in range(self.ny):
                for z in range(self.nz):
                    idx = self.index(x, y, z)
                    
                    # Weighted self-activation
                    s = self.weight[idx] * self.state[idx]
                    
                    # Sum neighbor contributions
                    for ox, oy, oz in offsets:
                        nx_, ny_, nz_ = x + ox, y + oy, z + oz
                        if not self.in_bounds(nx_, ny_, nz_):
                            continue
                        nidx = self.index(nx_, ny_, nz_)
                        s += 0.5 * self.state[nidx]
                    
                    # Apply decay
                    s *= decay
                    
                    # Ternary threshold
                    if s > 0.3:
                        self.next_state[idx] = +1
                    elif s < -0.3:
                        self.next_state[idx] = -1
                    else:
                        self.next_state[idx] = 0
        
        # Swap buffers
        self.state, self.next_state = self.next_state, self.state
    
    def summarize(self) -> Dict:
        """Get summary statistics of sheet state."""
        pos = neg = 0
        sx = sy = sz = 0.0
        
        for x in range(self.nx):
            for y in range(self.ny):
                for z in range(self.nz):
                    idx = self.index(x, y, z)
                    v = self.state[idx]
                    if v == +1:
                        pos += 1
                        sx += x
                        sy += y
                        sz += z
                    elif v == -1:
                        neg += 1
        
        cx = sx / pos if pos > 0 else 0.0
        cy = sy / pos if pos > 0 else 0.0
        cz = sz / pos if pos > 0 else 0.0
        
        return {
            "pos_count": pos,
            "neg_count": neg,
            "center": [cx, cy, cz],
            "total_cells": self.nx * self.ny * self.nz,
            "activity_ratio": (pos + neg) / max(1, self.nx * self.ny * self.nz),
        }


# =========================
# Brain State Writer
# =========================

def write_brain_state(thought: Dict, text: str, mode: str = "adaptive"):
    """
    Write brain state to JSON for visualizer compatibility.
    
    Matches the format expected by the Node.js visualizer.
    """
    state = {
        "tick": thought.get("tick", 0),
        "timestamp": time.time(),
        "phase": thought.get("decision", {}).get("intent", "Decide").capitalize(),
        "mode": mode,
        "limbic": {
            "reward": thought.get("value", {}).get("importance", 0.3),
            "novelty": 1.0 if thought.get("ternary", [0]*5)[0] == 1 else 0.0,
            "valence": thought.get("value", {}).get("valence", 0.0),
        },
        "policy_nn": {
            "layers": 3,
            "nodes": [8, 12, 40],
            "activations": [
                [0.3] * 8,
                [0.5] * 12,
                [0.2] * 40,
            ],
        },
        "memory_nn": {
            "clusters": thought.get("substrate", {}).get("nodes", 0),
            "edges": thought.get("substrate", {}).get("edges", 0),
        },
        "obs": {
            "input": text[:200],
        },
        "ternary": thought.get("ternary", [0, 0, 0, 0, 0]),
        "decision": thought.get("decision", {}),
    }
    
    base = Path.home() / ".aos" / "brain" / "state"
    base.mkdir(parents=True, exist_ok=True)
    
    with open(base / "brain_state.json", "w") as f:
        json.dump(state, f, indent=2)
    
    return state


# =========================
# Flask API Application
# =========================

app = Flask("aos_brain")
CORS(app)

# Global brain instance
brain: Optional[TernaryOodaBrain] = None
sheet: Optional[TernaryCorticalSheet3D] = None
viz: Optional[BrainVisualizer] = None
tick_counter = 0


def get_brain() -> TernaryOodaBrain:
    """Get or create brain instance."""
    global brain
    if brain is None:
        brain = TernaryOodaBrain()
    return brain


def get_sheet() -> TernaryCorticalSheet3D:
    """Get or create cortical sheet."""
    global sheet
    if sheet is None:
        sheet = TernaryCorticalSheet3D(12, 12, 6)
    return sheet


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "brain": "operational",
        "timestamp": time.time(),
    })


@app.route('/status', methods=['GET'])
def get_status():
    """Get full brain status."""
    b = get_brain()
    s = get_sheet()
    
    return jsonify({
        "brain": b.get_status(),
        "cortical_sheet": s.summarize(),
        "tick_counter": tick_counter,
    })


@app.route('/think', methods=['POST'])
def think():
    """
    Main think endpoint.
    
    Request: {"text": "...", "agent": "miles", "source": "user"}
    Response: {"action": "...", "reason": "...", "mode": "...", ...}
    """
    global tick_counter
    
    data = request.get_json() or {}
    text = data.get("text", "")
    agent = data.get("agent", "default")
    source = data.get("source", "api")
    
    if not text:
        return jsonify({"error": "empty_text"}), 400
    
    # Create observation
    obs = Observation(source=source, content=text, metadata={"agent": agent})
    
    # Execute cognition cycle
    b = get_brain()
    s = get_sheet()
    
    tick_counter += 1
    
    # Excite cortical sheet based on agent
    if agent == "miles":
        s.excite_region(3, 3, 2, 2, +1)
    elif agent == "mortimer":
        s.excite_region(8, 8, 3, 2, +1)
    else:
        s.excite_region(6, 6, 2, 3, +1)
    
    # Step sheet (simulate temporal dynamics)
    for _ in range(3):
        s.step_wave(decay=0.9)
        s.hebbian_update(eta=0.01)
    
    # Run OODA cycle
    thought = b.tick(obs)
    
    # Build response
    response = {
        "tick": tick_counter,
        "action": thought.decision.intent,
        "reason": thought.decision.reasoning,
        "mode": thought.mode,
        "language": thought.language,
        "ternary": thought.ternary_code,
        "confidence": thought.decision.confidence,
        "agent": agent,
        "cortical": s.summarize(),
        "memory": {
            "short_term": len(b.short_term),
            "mid_term": len(b.mid_term),
            "substrate": b.substrate.get_stats(),
        },
    }
    
    # Write state for visualizer
    write_brain_state(response, text, thought.mode)
    
    # Console output
    print(f"[{tick_counter}] {agent}: {text[:50]}... -> {thought.decision.intent} ({thought.mode})")
    
    return jsonify(response)


@app.route('/memory', methods=['GET'])
def get_memory():
    """Get memory layer statistics."""
    b = get_brain()
    return jsonify({
        "short_term": [str(t.content)[:100] for t in b.short_term[-5:]],
        "mid_term_count": len(b.mid_term),
        "substrate": b.substrate.get_stats(),
    })


@app.route('/sheet', methods=['GET'])
def get_sheet_state():
    """Get cortical sheet state."""
    s = get_sheet()
    return jsonify(s.summarize())


# =========================
# Standalone Socket Server (optional)
# =========================

class BrainSocketServer:
    """
    Unix socket server for compatibility with existing TUI.
    """
    
    def __init__(self, socket_path: str = "/tmp/aos_brain.sock"):
        self.socket_path = socket_path
        self.running = True
    
    def start(self):
        """Start the socket server."""
        import socket
        
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
        
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.socket_path)
        server.listen(5)
        
        print(f"[BrainSocket] Listening on {self.socket_path}")
        
        try:
            while self.running:
                client, _ = server.accept()
                t = threading.Thread(target=self.handle_client, args=(client,))
                t.daemon = True
                t.start()
        finally:
            server.close()
            if os.path.exists(self.socket_path):
                os.remove(self.socket_path)
    
    def handle_client(self, client_sock):
        """Handle a client connection."""
        import socket
        
        buf = b""
        try:
            while True:
                chunk = client_sock.recv(4096)
                if not chunk:
                    break
                buf += chunk
                
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    if not line:
                        continue
                    
                    try:
                        req = json.loads(line.decode("utf-8"))
                        text = req.get("text", "")
                        agent = req.get("agent", "default")
                        
                        # Process via Flask app context
                        with app.test_client() as c:
                            resp = c.post('/think', json={
                                "text": text,
                                "agent": agent,
                                "source": "socket"
                            })
                            reply = resp.get_json()
                    except Exception as e:
                        reply = {"error": str(e)}
                    
                    out = (json.dumps(reply) + "\n").encode("utf-8")
                    client_sock.sendall(out)
        finally:
            client_sock.close()


# =========================
# Main
# =========================

def main():
    """Run the brain server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ternary Brain Server")
    parser.add_argument("--port", type=int, default=5000, help="HTTP port")
    parser.add_argument("--socket", type=str, default="/tmp/aos_brain.sock", help="Unix socket path")
    parser.add_argument("--socket-only", action="store_true", help="Only run socket server")
    args = parser.parse_args()
    
    if args.socket_only:
        # Run only socket server
        socket_server = BrainSocketServer(args.socket)
        socket_server.start()
    else:
        # Run Flask HTTP server + socket in background
        socket_server = BrainSocketServer(args.socket)
        socket_thread = threading.Thread(target=socket_server.start)
        socket_thread.daemon = True
        socket_thread.start()
        
        print(f"[Brain] Starting HTTP server on port {args.port}")
        print(f"[Brain] Socket server on {args.socket}")
        app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
