#!/usr/bin/env python3
"""Spawn AOS agents into Minecraft using RCON"""

import socket
import struct
import time

def rcon_auth(sock, password):
    """Authenticate RCON connection"""
    # Packet: length (4) + id (4) + type (4) + payload + nulls
    payload = password.encode('utf-8')
    length = len(payload) + 10
    packet = length.to_bytes(4, 'little', signed=True) + (1).to_bytes(4, 'little', signed=True) + (3).to_bytes(4, 'little', signed=True) + payload + b'\x00\x00'
    
    sock.send(packet)
    
    # Receive response
    resp_len = int.from_bytes(sock.recv(4), 'little')
    resp = sock.recv(resp_len)
    packet_id = int.from_bytes(resp[4:8], 'little')
    
    return packet_id != -1

def rcon_command(sock, cmd):
    """Send command"""
    payload = cmd.encode('utf-8')
    length = len(payload) + 10
    packet = length.to_bytes(4, 'little') + (0).to_bytes(4, 'little') + (2).to_bytes(4, 'little') + payload + b'\x00\x00'
    
    sock.send(packet)
    
    # Receive response
    resp_len = int.from_bytes(sock.recv(4), 'little')
    resp = sock.recv(resp_len)
    return resp[10:-2].decode('utf-8', errors='ignore')

def main():
    print("Connecting to Minecraft RCON...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect(('localhost', 25576))
    
    if not rcon_auth(sock, 'aosbrain123'):
        print("Auth failed")
        return
    
    print("Authenticated! Spawning agents...")
    
    # Spawn agents
    agents = [
        ("COBRA", 100, 70, 100),
        ("PROMETHEUS", 120, 70, 100),
        ("MYLZERON", 140, 70, 100),
    ]
    
    for name, x, y, z in agents:
        cmd = f'summon armor_stand {x} {y} {z} {{CustomName:"\\"{name}\\"",ShowArms:1}}'
        result = rcon_command(sock, cmd)
        print(f"  {name}: {result or 'OK'}")
        time.sleep(0.5)
    
    # Broadcast message
    rcon_command(sock, 'say AOS Agents have entered the world!')
    print("\nAgents spawned!")
    sock.close()

if __name__ == "__main__":
    main()
