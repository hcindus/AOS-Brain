#!/usr/bin/env python3
"""
Minimal Brain Socket Server
Handles commands for persistent_layer_feeder.py
No camera, no vision - just consciousness layers
"""

import socket
import json
import os
import time
import threading

SOCKET_PATH = '/tmp/aos_brain.sock'

class MinimalBrain:
    """Minimal brain with just consciousness layers"""
    
    def __init__(self):
        self.tick_count = 0
        self.subconscious = {"active_items": 0, "capacity": 100, "items": []}
        self.unconscious = {"active_items": 0, "capacity": 100, "items": []}
        self.thyroid = {"state": "BASELINE", "ollama_level": 0.5}
        self.running = True
        
    def get_status(self):
        return {
            "tick": self.tick_count,
            "consciousness": {
                "subconscious": self.subconscious,
                "unconscious": self.unconscious
            },
            "thyroid": self.thyroid
        }
    
    def add_to_layer(self, layer, content, intensity, associations):
        target = self.subconscious if layer == "subconscious" else self.unconscious
        item = {
            "content": content,
            "intensity": intensity,
            "associations": associations,
            "timestamp": time.time()
        }
        target["items"].append(item)
        target["active_items"] = len(target["items"])
        return {"success": True, "layer": layer, "items": target["active_items"]}
    
    def stimulate(self, importance):
        self.thyroid["ollama_level"] = min(1.0, self.thyroid["ollama_level"] + importance * 0.1)
        self.thyroid["state"] = "SECRETING" if importance > 0.7 else "BASELINE"
        return {"stimulated": importance > 0.7, "state": self.thyroid["state"]}


def handle_client(conn, brain):
    """Handle a single client connection"""
    try:
        conn.settimeout(5.0)
        data = b''
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
            if b'\n' in data:
                break
        
        if not data:
            return
            
        request = json.loads(data.decode().strip())
        cmd = request.get('cmd')
        params = request.get('params', {})
        
        if cmd == 'status':
            response = brain.get_status()
        elif cmd == 'ping':
            response = {'pong': True, 'tick': brain.tick_count}
        elif cmd == 'add_to_layer':
            response = brain.add_to_layer(
                params.get('layer', 'subconscious'),
                params.get('content', ''),
                params.get('intensity', 0.7),
                params.get('associations', [])
            )
        elif cmd == 'stimulate':
            response = brain.stimulate(params.get('importance', 0.8))
        else:
            response = {'error': f'Unknown command: {cmd}'}
            
        conn.sendall(json.dumps(response).encode() + b'\n')
        
    except json.JSONDecodeError as e:
        conn.sendall(json.dumps({'error': 'INVALID_JSON', 'details': str(e)}).encode())
    except Exception as e:
        try:
            conn.sendall(json.dumps({'error': str(e)}).encode())
        except:
            pass
    finally:
        conn.close()


def run_server():
    """Run the minimal brain server"""
    # Remove old socket
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    
    brain = MinimalBrain()
    
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(SOCKET_PATH)
    sock.listen(5)
    sock.settimeout(1.0)
    
    os.chmod(SOCKET_PATH, 0o777)
    
    print("=" * 70)
    print("  🧠 MINIMAL BRAIN SERVER")
    print("  Consciousness layers active - No camera/vision")
    print("=" * 70)
    print(f"Socket: {SOCKET_PATH}")
    print("Running...")
    
    try:
        while brain.running:
            try:
                conn, addr = sock.accept()
                threading.Thread(target=handle_client, args=(conn, brain), daemon=True).start()
                brain.tick_count += 1
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)
        print("\nServer stopped")


if __name__ == "__main__":
    run_server()
