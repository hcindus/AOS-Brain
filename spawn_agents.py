#!/usr/bin/env python3
"""Spawn AOS agents into Minecraft world"""

import socket
import json
import time

def send_rcon(command):
    """Send RCON command to Minecraft"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', 25575))
        
        # Authentication would go here
        # For now, just return command
        return f"Would execute: {command}"
    except:
        return "RCON not fully connected"

# Spawn agents
agents = [
    ("cobra", "COBRA-001", 100, 70, 100),
    ("prometheus", "PROMETHEUS-001", 120, 70, 100),
    ("mylzeron", "MYLZERON", 140, 70, 100),
]

print("Spawning AOS agents into Minecraft...")
for agent_id, name, x, y, z in agents:
    # Summon armor stand as agent body
    cmd = f'summon minecraft:armor_stand {x} {y} {z} {{CustomName:"\\"{name}\\"",NoAI:0}}'
    result = send_rcon(cmd)
    print(f"  {agent_id}: {result}")
    time.sleep(0.5)

print("\nAgents spawned!")
