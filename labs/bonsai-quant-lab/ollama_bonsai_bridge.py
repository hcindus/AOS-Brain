#!/usr/bin/env python3
"""
OLLAMA-BONSAI BRIDGE v1.0
Routes Ollama API requests:
  - Bonsai models → PrismML llama.cpp fork
  - Other models  → Standard Ollama

Provides Ollama-compatible API on port 11435
Configure Brain to use: http://localhost:11435
"""

import json
import subprocess
import threading
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
BRIDGE_PORT = 11435          # Bridge listens here
OLLAMA_PORT = 11434          # Real Ollama port
PRISM_LLAMA = "/tmp/prism-llama.cpp/build/bin/llama-cli"
BONSAI_MODELS = {
    "bonsai-8b-q1_0": "/root/bonsai-8b-q1_0.gguf",
    "ternary-bonsai-q2:8b": "/root/Ternary-Bonsai-8B-Q2_0.gguf",
    "bonsai-1bit-test": "/tmp/bonsai-test/Bonsai-8B-Q1_0.gguf",
}

# ═══════════════════════════════════════════════════════════════════
# REQUEST HANDLER
# ═══════════════════════════════════════════════════════════════════

class BridgeHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[Bridge] {self.client_address[0]} - {format % args}")
    
    def do_GET(self):
        """Handle GET requests (tags, ps)"""
        if self.path == "/api/tags":
            self._forward_to_ollama()
        elif self.path == "/api/ps":
            self._forward_to_ollama()
        else:
            self._send_error(404, "Not found")
    
    def do_POST(self):
        """Handle POST requests (generate, chat, pull)"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
            return
        
        # Route based on model name
        model = data.get('model', '')
        
        if any(bonsai in model.lower() for bonsai in BONSAI_MODELS.keys()):
            self._handle_bonsai(data)
        else:
            self._forward_to_ollama_post(data)
    
    def _handle_bonsai(self, data):
        """Process Bonsai requests via PrismML fork"""
        model = data.get('model', '')
        prompt = data.get('prompt', '')
        
        # Map model name to GGUF path
        gguf_path = None
        for key, path in BONSAI_MODELS.items():
            if key in model.lower():
                gguf_path = path
                break
        
        if not gguf_path:
            self._send_error(404, f"Bonsai model '{model}' not configured")
            return
        
        # Get parameters
        opts = data.get('options', {})
        max_tokens = opts.get('num_predict', 100)
        temperature = opts.get('temperature', 0.7)
        top_k = opts.get('top_k', 20)
        
        print(f"[Bridge] Routing to PrismML: {model}")
        
        try:
            # Build llama-cli command
            cmd = [
                PRISM_LLAMA,
                "-m", gguf_path,
                "-p", prompt,
                "-n", str(max_tokens),
                "--temp", str(temperature),
                "--top-k", str(top_k),
                "--no-display-prompt",
            ]
            
            # Execute
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"[Bridge] PrismML error: {result.stderr[:200]}")
                self._send_error(500, f"PrismML execution failed: {result.stderr[:100]}")
                return
            
            # Extract response (llama-cli outputs prompt+response, remove prompt)
            output = result.stdout
            # Remove the echoed prompt from output
            if output.startswith(prompt):
                output = output[len(prompt):].strip()
            
            # Send Ollama-compatible response
            response = {
                "model": model,
                "created_at": "2026-04-22T02:20:00Z",
                "response": output,
                "done": True,
                "context": [],
                "total_duration": 0,
                "load_duration": 0,
                "prompt_eval_count": len(prompt.split()),
                "prompt_eval_duration": 0,
                "eval_count": len(output.split()),
                "eval_duration": 0
            }
            
            self._send_json(200, response)
            
        except subprocess.TimeoutExpired:
            self._send_error(504, "PrismML execution timeout")
        except Exception as e:
            print(f"[Bridge] Error: {e}")
            self._send_error(500, str(e))
    
    def _forward_to_ollama(self):
        """Forward GET to real Ollama"""
        try:
            with urlopen(f"http://127.0.0.1:{OLLAMA_PORT}{self.path}", timeout=10) as resp:
                self.send_response(resp.status)
                for header, value in resp.headers.items():
                    if header.lower() not in ('transfer-encoding', 'content-length'):
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(resp.read())
        except URLError as e:
            self._send_error(502, f"Ollama unreachable: {e}")
    
    def _forward_to_ollama_post(self, data):
        """Forward POST to real Ollama"""
        try:
            req = Request(
                f"http://127.0.0.1:{OLLAMA_PORT}{self.path}",
                data=json.dumps(data).encode(),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urlopen(req, timeout=120) as resp:
                self.send_response(resp.status)
                for header, value in resp.headers.items():
                    if header.lower() not in ('transfer-encoding', 'content-length'):
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(resp.read())
        except URLError as e:
            self._send_error(502, f"Ollama unreachable: {e}")
    
    def _send_json(self, status, data):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_error(self, status, message):
        """Send error response"""
        self._send_json(status, {"error": message})


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    server = HTTPServer(('127.0.0.1', BRIDGE_PORT), BridgeHandler)
    print(f"═══════════════════════════════════════════════════════════")
    print(f"  OLLAMA-BONSAI BRIDGE v1.0")
    print(f"═══════════════════════════════════════════════════════════")
    print(f"  Listening:  http://127.0.0.1:{BRIDGE_PORT}")
    print(f"  Ollama:     http://127.0.0.1:{OLLAMA_PORT}")
    print(f"  PrismML:    {PRISM_LLAMA}")
    print(f"═══════════════════════════════════════════════════════════")
    print(f"  Configure Brain with:")
    print(f"    OLLAMA_HOST=127.0.0.1:{BRIDGE_PORT}")
    print(f"═══════════════════════════════════════════════════════════\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Bridge] Shutting down...")
        server.shutdown()

if __name__ == "__main__":
    main()
