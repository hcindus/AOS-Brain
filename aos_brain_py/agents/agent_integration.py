#!/usr/bin/env python3
"""
Hermes & Mini-Agent Integration Module.

Connects external agent platforms to the 7-Region Ternary Brain.

Features:
- Hermes API adapter (state-based, similar to OpenClaw)
- Mini-Agent adapter (MiniMax API-based)
- Unified brain interface for all agents
- Cross-agent memory sharing
"""

import os
import json
import time
import requests
from typing import Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path


class HermesAdapter:
    """
    Adapter for Hermes agent platform.
    
    Hermes uses a state-based architecture similar to OpenClaw:
    - State files in ~/.local/state/hermes/
    - Gateway locks for coordination
    - Lock-based concurrency control
    """
    
    def __init__(self, brain_client=None):
        self.hermes_state_dir = Path.home() / ".local" / "state" / "hermes"
        self.locks_dir = self.hermes_state_dir / "gateway-locks"
        self.brain = brain_client
        
    def read_state(self) -> Optional[Dict]:
        """Read current Hermes state."""
        # Look for state files
        state_files = list(self.hermes_state_dir.glob("*.json"))
        if not state_files:
            return None
        
        # Read most recent
        latest = max(state_files, key=lambda p: p.stat().st_mtime)
        try:
            with open(latest) as f:
                return json.load(f)
        except:
            return None
    
    def write_intent(self, intent: str, payload: Dict = None):
        """Write intent to Hermes input queue."""
        intent_file = self.hermes_state_dir / "intent.json"
        data = {
            "intent": intent,
            "payload": payload or {},
            "timestamp": time.time(),
            "source": "brain_adapter",
        }
        with open(intent_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def check_locks(self) -> bool:
        """Check if any locks are active."""
        if not self.locks_dir.exists():
            return False
        locks = list(self.locks_dir.glob("*.lock"))
        return len(locks) > 0
    
    def feed_to_brain(self, message: str) -> Dict:
        """Feed Hermes message to 7-region brain."""
        if self.brain:
            return self.brain.process(message, source="hermes")
        return {"error": "No brain client"}


class MiniAgentAdapter:
    """
    Adapter for Mini-Agent platform.
    
    Mini-Agent uses MiniMax API (anthropic-compatible):
    - Config in ~/.mini-agent/config/
    - API-based agent with tool support
    - MCP (Model Context Protocol) integration
    """
    
    MINIMAX_BASE = "https://api.minimax.io"
    
    def __init__(self, brain_client=None):
        self.config_dir = Path.home() / ".mini-agent" / "config"
        self.config_file = self.config_dir / "config.yaml"
        self.brain = brain_client
        self.api_key = self._load_api_key()
    
    def _load_api_key(self) -> Optional[str]:
        """Load MiniMax API key from config."""
        if not self.config_file.exists():
            return None
        
        # Simple YAML parsing (not full parser)
        try:
            with open(self.config_file) as f:
                for line in f:
                    if line.startswith("api_key:"):
                        key = line.split(":", 1)[1].strip().strip('"').strip("'")
                        if key != "YOUR_API_KEY_HERE":
                            return key
        except:
            pass
        return None
    
    def is_configured(self) -> bool:
        """Check if Mini-Agent is properly configured."""
        return self.api_key is not None
    
    def query_minimax(self, prompt: str, model: str = "MiniMax-M2.5") -> Optional[str]:
        """Query MiniMax API directly."""
        if not self.api_key:
            return None
        
        try:
            resp = requests.post(
                f"{self.MINIMAX_BASE}/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                },
                timeout=30,
            )
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"
    
    def feed_to_brain(self, message: str) -> Dict:
        """Feed Mini-Agent message to 7-region brain."""
        if self.brain:
            return self.brain.process(message, source="mini-agent")
        return {"error": "No brain client"}


class UnifiedAgentInterface:
    """
    Unified interface for all agent platforms.
    
    Routes messages between:
    - OpenClaw (main)
    - Hermes (state-based)
    - Mini-Agent (API-based)
    - 7-Region Brain (cognition)
    """
    
    def __init__(self, brain_path: str = "http://localhost:5000"):
        self.brain_path = brain_path
        self.hermes = HermesAdapter(self)
        self.mini = MiniAgentAdapter(self)
        
    def process(self, message: str, source: str = "unified") -> Dict:
        """Process message through unified interface."""
        # Route to brain
        try:
            resp = requests.post(
                f"{self.brain_path}/think",
                json={"text": message, "source": source},
                timeout=10,
            )
            return resp.json()
        except Exception as e:
            return {"error": str(e), "action": "error"}
    
    def route_to_hermes(self, message: str):
        """Route message to Hermes."""
        self.hermes.write_intent("process", {"message": message})
    
    def route_to_mini(self, message: str):
        """Route message to Mini-Agent."""
        if self.mini.is_configured():
            return self.mini.query_minimax(message)
        return {"error": "Mini-Agent not configured"}
    
    def get_status(self) -> Dict:
        """Get status of all agent platforms."""
        return {
            "hermes": {
                "state_dir": str(self.hermes.hermes_state_dir),
                "has_state": self.hermes.read_state() is not None,
                "locked": self.hermes.check_locks(),
            },
            "mini_agent": {
                "config_dir": str(self.mini.config_dir),
                "configured": self.mini.is_configured(),
            },
            "brain": {
                "endpoint": self.brain_path,
            },
        }


def main():
    """CLI for agent integration."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Platform Integration")
    parser.add_argument("--status", action="store_true", help="Check status")
    parser.add_argument("--hermes", action="store_true", help="Test Hermes")
    parser.add_argument("--mini", action="store_true", help="Test Mini-Agent")
    parser.add_argument("--message", "-m", help="Message to process")
    args = parser.parse_args()
    
    iface = UnifiedAgentInterface()
    
    if args.status:
        print(json.dumps(iface.get_status(), indent=2))
        return
    
    if args.hermes and args.message:
        result = iface.hermes.feed_to_brain(args.message)
        print(json.dumps(result, indent=2))
        return
    
    if args.mini and args.message:
        result = iface.mini.feed_to_brain(args.message)
        print(json.dumps(result, indent=2))
        return
    
    if args.message:
        result = iface.process(args.message)
        print(json.dumps(result, indent=2))
        return
    
    print("Usage:")
    print("  python agent_integration.py --status")
    print("  python agent_integration.py -m 'Hello brain'")
    print("  python agent_integration.py --hermes -m 'Hello from Hermes'")
    print("  python agent_integration.py --mini -m 'Hello from Mini'")


if __name__ == "__main__":
    main()
