#!/usr/bin/env python3
"""
Mineflayer Agent Supervisor
Manages multiple autonomous agents with Brain OODA integration

Usage: python supervisor.py [--agents AGENT1,AGENT2,...] [--count N]
"""

import subprocess
import sys
import os
import json
import time
import signal
import argparse
from typing import Dict, List
import threading

# Configuration
MINECRAFT_HOST = "localhost"
MINECRAFT_PORT = 25566
BRAIN_WS_PORT = 8767
AGENTS_DIR = "/root/.openclaw/workspace/AGI_COMPANY/agents"

# Default agent list (7 MYL agents)
DEFAULT_AGENTS = [
    "mylzeron",    # Male
    "mylonen",     # Male  
    "myltwon",     # Male
    "mylthreen",   # Female
    "mylforon",    # Male
    "mylfivon",    # Female
    "mylsixon",    # Female
]

class AgentSupervisor:
    """Manages agent processes"""
    
    def __init__(self):
        self.agents: Dict[str, subprocess.Popen] = {}
        self.agent_configs: Dict[str, dict] = {}
        self.running = False
        
    def load_agent_configs(self):
        """Load agent configurations from AGI_COMPANY/agents"""
        for agent_id in DEFAULT_AGENTS:
            agent_path = os.path.join(AGENTS_DIR, agent_id)
            config_path = os.path.join(agent_path, "config.json")
            
            if os.path.exists(config_path):
                with open(config_path) as f:
                    self.agent_configs[agent_id] = json.load(f)
            else:
                # Default config
                self.agent_configs[agent_id] = {
                    "name": agent_id,
                    "gender": "female" if agent_id in ["mylthreen", "mylfivon", "mylsixon"] else "male",
                    "skills": [],
                    "personality": "curious"
                }
    
    def spawn_agent(self, agent_id: str, x: float = 0, y: float = 100, z: float = 0) -> bool:
        """Spawn a Mineflayer agent"""
        if agent_id in self.agents:
            print(f"[Supervisor] {agent_id} already running")
            return False
        
        print(f"[Supervisor] Spawning {agent_id}...")
        
        # Build command
        cmd = [
            "node",
            "/root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge/mineflayer_agent.js",
            agent_id,
            MINECRAFT_HOST,
            str(MINECRAFT_PORT),
            f"ws://localhost:{BRAIN_WS_PORT}"
        ]
        
        # Set environment
        env = os.environ.copy()
        env["AGENT_SPAWN_X"] = str(x)
        env["AGENT_SPAWN_Y"] = str(y)
        env["AGENT_SPAWN_Z"] = str(z)
        
        try:
            process = subprocess.Popen(
                cmd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                preexec_fn=os.setsid
            )
            
            self.agents[agent_id] = process
            
            # Start log thread
            log_thread = threading.Thread(target=self._agent_logger, args=(agent_id, process))
            log_thread.daemon = True
            log_thread.start()
            
            print(f"[Supervisor] {agent_id} spawned (PID {process.pid})")
            return True
            
        except Exception as e:
            print(f"[Supervisor] Failed to spawn {agent_id}: {e}")
            return False
    
    def _agent_logger(self, agent_id: str, process: subprocess.Popen):
        """Log agent output"""
        for line in process.stdout:
            print(f"[{agent_id}] {line.strip()}")
    
    def kill_agent(self, agent_id: str):
        """Kill an agent process"""
        if agent_id not in self.agents:
            return
        
        process = self.agents[agent_id]
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait(timeout=5)
        except:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except:
                pass
        
        del self.agents[agent_id]
        print(f"[Supervisor] {agent_id} killed")
    
    def spawn_all(self):
        """Spawn all configured agents"""
        print(f"[Supervisor] Spawning {len(DEFAULT_AGENTS)} agents...")
        
        # Spawn in a circle around spawn
        import math
        radius = 10
        for i, agent_id in enumerate(DEFAULT_AGENTS):
            angle = (2 * math.pi * i) / len(DEFAULT_AGENTS)
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            y = 100
            
            self.spawn_agent(agent_id, x, y, z)
            time.sleep(2)  # Stagger spawns
    
    def status(self):
        """Print agent status"""
        print("\n" + "="*70)
        print("AGENT STATUS")
        print("="*70)
        
        for agent_id, process in self.agents.items():
            alive = process.poll() is None
            status = "RUNNING" if alive else "DEAD"
            print(f"  {agent_id:15s} PID {process.pid:6d} [{status}]")
        
        print("="*70 + "\n")
    
    def stop_all(self):
        """Stop all agents"""
        print("[Supervisor] Stopping all agents...")
        for agent_id in list(self.agents.keys()):
            self.kill_agent(agent_id)
    
    def run(self):
        """Main supervisor loop"""
        self.load_agent_configs()
        self.spawn_all()
        
        self.running = True
        
        print("\n[Supervisor] Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                self.status()
                
                # Check for dead agents and restart
                for agent_id in list(self.agents.keys()):
                    process = self.agents[agent_id]
                    if process.poll() is not None:
                        print(f"[Supervisor] {agent_id} died, respawning...")
                        del self.agents[agent_id]
                        self.spawn_agent(agent_id)
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n[Supervisor] Shutting down...")
        finally:
            self.stop_all()


def main():
    parser = argparse.ArgumentParser(description="Mineflayer Agent Supervisor")
    parser.add_argument("--agents", type=str, help="Comma-separated agent IDs")
    parser.add_argument("--count", type=int, default=7, help="Number of agents to spawn")
    parser.add_argument("--status", action="store_true", help="Show status and exit")
    args = parser.parse_args()
    
    supervisor = AgentSupervisor()
    
    if args.status:
        supervisor.status()
        return
    
    # Override default agents if specified
    global DEFAULT_AGENTS
    if args.agents:
        DEFAULT_AGENTS = args.agents.split(",")
    elif args.count:
        DEFAULT_AGENTS = DEFAULT_AGENTS[:args.count]
    
    # Check if node is available
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
    except:
        print("Error: Node.js not found. Install with: apt install nodejs npm")
        sys.exit(1)
    
    # Check if mineflayer is installed
    mineflayer_path = "/root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge/node_modules/mineflayer"
    if not os.path.exists(mineflayer_path):
        print("Installing Mineflayer...")
        os.chdir("/root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge")
        subprocess.run(["npm", "install", "mineflayer", "mineflayer-pathfinder", "mineflayer-collectblock", "ws", "vec3"], check=True)
    
    supervisor.run()

if __name__ == "__main__":
    main()
