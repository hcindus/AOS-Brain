#!/usr/bin/env python3
"""
Minecraft Agent Rotation System
Manages 7 mineflayer agents with automatic failover
"""

import subprocess
import sys
import os
import time
import signal
from datetime import datetime

AGENT_DIR = "/root/.openclaw/workspace/scripts/minecraft_agents"
LOG_DIR = "/root/.openclaw/workspace/logs"

AGENTS = [
    {"name": "Forge", "username": "forge", "role": "builder", "port": 25566},
    {"name": "Patricia", "username": "patricia", "role": "explorer", "port": 25566},
    {"name": "Chelios", "username": "chelios", "role": "guard", "port": 25566},
    {"name": "Aurora", "username": "aurora", "role": "gatherer", "port": 25566},
    {"name": "Patricia2", "username": "patricia2", "role": "miner", "port": 25566},
    {"name": "Chelios2", "username": "chelios2", "role": "farmer", "port": 25566},
    {"name": "Forge2", "username": "forge2", "role": "crafter", "port": 25566},
]

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    with open(f"{LOG_DIR}/mc_rotation.log", "a") as f:
        f.write(log_msg + "\n")

def get_running_agents():
    """Get list of running agent processes"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "node.*mineflayer"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return len(result.stdout.strip().split("\n"))
        return 0
    except:
        return 0

def start_agent(agent):
    """Start a single agent"""
    log_file = f"{LOG_DIR}/{agent['username']}.log"
    
    cmd = [
        "node",
        f"{AGENT_DIR}/simple_agent.js",
        agent["username"],
        "localhost",
        str(agent["port"]),
        "ws://localhost:8767"
    ]
    
    try:
        with open(log_file, "a") as f:
            subprocess.Popen(
                cmd,
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=AGENT_DIR
            )
        log(f"Started {agent['name']} ({agent['username']})")
        return True
    except Exception as e:
        log(f"Failed to start {agent['name']}: {e}")
        return False

def ensure_brain_server():
    """Ensure brain WebSocket server is running"""
    try:
        result = subprocess.run(
            ["ss", "-tlnp"],
            capture_output=True,
            text=True
        )
        if ":8767" not in result.stdout:
            log("Brain server not running, starting...")
            subprocess.Popen(
                ["python3", f"{AGENT_DIR}/simple_brain_server.py"],
                stdout=open(f"{LOG_DIR}/brain_server.log", "a"),
                stderr=subprocess.STDOUT,
                cwd=AGENT_DIR
            )
            time.sleep(2)
    except Exception as e:
        log(f"Brain server check failed: {e}")

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    
    log("=" * 50)
    log("MINECRAFT AGENT ROTATION STARTED")
    log("=" * 50)
    
    # Ensure brain server
    ensure_brain_server()
    
    # Check current agents
    running = get_running_agents()
    log(f"Currently running: {running}/{len(AGENTS)} agents")
    
    # Start missing agents
    if running < len(AGENTS):
        needed = len(AGENTS) - running
        log(f"Need to start {needed} agents")
        
        for i, agent in enumerate(AGENTS):
            if i < needed:
                start_agent(agent)
                time.sleep(3)  # Stagger starts
    else:
        log("All agents running")
    
    log("Rotation complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
