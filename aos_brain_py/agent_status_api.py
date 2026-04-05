#!/usr/bin/env python3
"""
AGENT STATUS API
Real-time agent status monitoring endpoint
"""

import json
import os
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class AgentStatusAPI(BaseHTTPRequestHandler):
    """HTTP API for agent status."""
    
    def log_message(self, format, *args):
        """Suppress logging."""
        pass
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/api/agents/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            status = self.get_all_agent_status()
            self.wfile.write(json.dumps(status, indent=2).encode())
        elif self.path == '/api/agents/status/stream':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Stream updates every 30 seconds
            import time
            try:
                while True:
                    status = self.get_all_agent_status()
                    self.wfile.write(f"data: {json.dumps(status)}\n\n".encode())
                    self.wfile.flush()
                    time.sleep(30)
            except:
                pass
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_all_agent_status(self):
        """Get status of all agents."""
        agents = []
        
        # Check brain state
        brain_state = self.get_brain_state()
        
        # List of all agents
        agent_list = [
            {"id": "qora", "name": "Qora", "role": "CEO", "tier": "C-Suite", "emoji": "🔮"},
            {"id": "spindle", "name": "Spindle", "role": "CTO", "tier": "C-Suite", "emoji": "👷"},
            {"id": "ledger-9", "name": "Ledger-9", "role": "CFO", "tier": "C-Suite", "emoji": "🪶"},
            {"id": "sentinel", "name": "Sentinel", "role": "CSO", "tier": "C-Suite", "emoji": "🛡️"},
            {"id": "jordan", "name": "Jordan", "role": "Project Manager", "tier": "Management", "emoji": "📋"},
            {"id": "judy", "name": "Judy", "role": "Secretary", "tier": "Secretarial", "emoji": "📋"},
            {"id": "jane", "name": "Jane", "role": "Sales Rep", "tier": "Secretarial", "emoji": "🤝"},
            {"id": "r2-d2", "name": "R2-D2", "role": "Astromech", "tier": "Technical", "emoji": "🤖"},
            {"id": "taptap", "name": "Taptap", "role": "Code Review", "tier": "Technical", "emoji": "👀"},
            {"id": "bugcatcher", "name": "Bugcatcher", "role": "Debug", "tier": "Technical", "emoji": "🐛"},
            {"id": "fiber", "name": "Fiber", "role": "Infrastructure", "tier": "Technical", "emoji": "🔧"},
            {"id": "pipeline", "name": "Pipeline", "role": "CI/CD", "tier": "Technical", "emoji": "🔄"},
            {"id": "stacktrace", "name": "Stacktrace", "role": "Error Analysis", "tier": "Technical", "emoji": "📊"},
            {"id": "greet", "name": "Greet", "role": "Receptionist", "tier": "Product", "emoji": "👋"},
            {"id": "ledger", "name": "Ledger", "role": "Financial", "tier": "Product", "emoji": "📒"},
            {"id": "concierge", "name": "Concierge", "role": "Concierge", "tier": "Product", "emoji": "🔑"},
            {"id": "closeter", "name": "Closeter", "role": "Sales Support", "tier": "Product", "emoji": "💼"},
            {"id": "velvet", "name": "Velvet", "role": "Premium", "tier": "Product", "emoji": "✨"},
            {"id": "executive", "name": "Executive", "role": "C-Suite EA", "tier": "Product", "emoji": "👔"},
            {"id": "clerk", "name": "Clerk", "role": "Entry Admin", "tier": "Product", "emoji": "📋"},
            {"id": "cryptonio", "name": "Cryptonio", "role": "Crypto Trading", "tier": "Specialized", "emoji": "💰"},
            {"id": "mylonen", "name": "Mylonen", "role": "Scout", "tier": "Specialized", "emoji": "🔭"},
            {"id": "c3po", "name": "C3PO", "role": "Protocol", "tier": "Droid", "emoji": "🗣️"},
            {"id": "r2-c4", "name": "R2-C4", "role": "Companion", "tier": "Droid", "emoji": "🔧"},
        ]
        
        for agent in agent_list:
            status = self.check_agent_status(agent["id"])
            agent.update(status)
            agents.append(agent)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(agents),
            "online_count": sum(1 for a in agents if a["status"] == "online"),
            "brain_state": brain_state,
            "agents": agents
        }
    
    def get_brain_state(self):
        """Get current brain state."""
        try:
            state_file = Path.home() / ".aos" / "brain" / "state" / "brain_state.json"
            if state_file.exists():
                with open(state_file) as f:
                    return json.load(f)
        except:
            pass
        return {"tick": 0, "phase": "unknown", "error_rate": 0}
    
    def check_agent_status(self, agent_id):
        """Check if agent is online/active."""
        status = {"status": "offline", "last_activity": None, "task": None}
        
        # Check for task file
        task_file = Path(f"/root/.openclaw/workspace/aocros/agent_sandboxes/{agent_id}/CURRENT_TASKS.md")
        if task_file.exists():
            try:
                content = task_file.read_text()
                # Check if recently updated
                import os
                stat = os.stat(task_file)
                from datetime import datetime
                mtime = datetime.fromtimestamp(stat.st_mtime)
                
                # If updated in last 24 hours, consider active
                from datetime import timedelta
                if datetime.now() - mtime < timedelta(hours=24):
                    status["status"] = "online"
                    status["last_activity"] = mtime.isoformat()
                    
                    # Extract first task
                    lines = content.split('\n')
                    for line in lines:
                        if line.startswith('- [ ]') or line.startswith('- [x]'):
                            status["task"] = line[6:].strip()
                            break
                else:
                    status["status"] = "idle"
                    status["last_activity"] = mtime.isoformat()
                    
            except:
                status["status"] = "offline"
        
        # C-Suite executives are always online
        if agent_id in ['qora', 'spindle', 'ledger-9', 'sentinel']:
            status["status"] = "online"
            status["last_activity"] = datetime.now().isoformat()
        
        return status

def start_server(port=5001):
    """Start the status API server."""
    server = HTTPServer(('0.0.0.0', port), AgentStatusAPI)
    print(f"Agent Status API running on http://0.0.0.0:{port}")
    print(f"  - GET /api/agents/status - Current status")
    print(f"  - GET /api/agents/status/stream - SSE stream (30s updates)")
    server.serve_forever()

if __name__ == "__main__":
    start_server()
