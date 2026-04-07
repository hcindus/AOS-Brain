#!/usr/bin/env python3
"""
Minecraft Dual-Port Monitor
Checks both 25565 (MC server) and 25566 (backup/agents)
Auto-starts server on 25565 if down, alerts if 25566 in use
"""

import subprocess
import socket
import time
import os
from datetime import datetime

LOG_FILE = "/root/.openclaw/workspace/logs/mc_port_monitor.log"
MC_DIR = "/opt/minecraft-server"
AGENT_ROTATION = "/root/.openclaw/workspace/scripts/minecraft_agent_rotation.py"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def check_port(port, host="localhost"):
    """Check if a port is listening"""
    try:
        result = subprocess.run(
            ["ss", "-tlnp"],
            capture_output=True, text=True, timeout=5
        )
        return f":{port}" in result.stdout
    except Exception as e:
        log(f"Port check error for {port}: {e}")
        return False

def get_mc_process():
    """Get Minecraft server process info"""
    try:
        result = subprocess.run(
            ["pgrep", "-a", "java"],
            capture_output=True, text=True
        )
        for line in result.stdout.split("\n"):
            if "paper" in line.lower() or "server.jar" in line.lower():
                return line
        return None
    except:
        return None

def start_minecraft_server():
    """Start the Minecraft server on 25565"""
    log("Starting Minecraft server on port 25565...")
    try:
        os.chdir(MC_DIR)
        subprocess.Popen(
            ["nohup", "java", "-Xmx4G", "-Xms1G", "-jar", "paper-1.20.4-496.jar", "nogui"],
            stdout=open("/dev/null", "w"),
            stderr=subprocess.STDOUT,
            cwd=MC_DIR
        )
        log("Minecraft server starting...")
        return True
    except Exception as e:
        log(f"Failed to start MC server: {e}")
        return False

def restart_agents():
    """Restart the Mineflayer agents"""
    log("Restarting Mineflayer agents...")
    try:
        subprocess.run(["pkill", "-f", "node.*simple_agent"], capture_output=True)
        time.sleep(2)
        subprocess.Popen(
            ["python3", AGENT_ROTATION],
            stdout=open("/dev/null", "w"),
            stderr=subprocess.STDOUT
        )
        log("Agent rotation triggered")
        return True
    except Exception as e:
        log(f"Failed to restart agents: {e}")
        return False

def main():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    log("=" * 50)
    log("DUAL-PORT MINECRAFT MONITOR")
    log("=" * 50)
    
    # Check port 25565 (Minecraft server)
    mc_running = check_port(25565)
    
    # Check port 25566 (usually agents or alternate)
    alt_running = check_port(25566)
    
    log(f"Port 25565 (MC Server): {'✅ UP' if mc_running else '❌ DOWN'}")
    log(f"Port 25566 (Alternate): {'✅ IN USE' if alt_running else '⚪ FREE'}")
    
    actions = []
    
    if not mc_running:
        log("⚠️  Minecraft server not responding on 25565")
        mc_proc = get_mc_process()
        
        if mc_proc:
            log(f"Found stale process: {mc_proc[:60]}...")
            log("Killing stale process...")
            subprocess.run(["pkill", "-9", "-f", "paper-1.20"], capture_output=True)
            time.sleep(2)
        
        if start_minecraft_server():
            actions.append("Started MC server on 25565")
            time.sleep(10)  # Wait for server to initialize
    else:
        log("✅ Minecraft server healthy on 25565")
    
    # Check agents if MC is up
    if check_port(25565):
        agent_count = subprocess.run(
            ["pgrep", "-c", "-f", "node.*simple_agent"],
            capture_output=True, text=True
        )
        try:
            count = int(agent_count.stdout.strip()) if agent_count.returncode == 0 else 0
            log(f"Mineflayer agents: {count}/7")
            
            if count < 3:  # Threshold to restart agents
                log("⚠️  Low agent count, triggering rotation...")
                restart_agents()
                actions.append("Restarted agents")
        except:
            pass
    
    if alt_running:
        log("ℹ️  Port 25566 in use - may be conflicting service")
    
    log("=" * 50)
    if actions:
        log(f"Actions taken: {', '.join(actions)}")
    else:
        log("All systems nominal - no action needed")
    log("=" * 50)

if __name__ == "__main__":
    main()
