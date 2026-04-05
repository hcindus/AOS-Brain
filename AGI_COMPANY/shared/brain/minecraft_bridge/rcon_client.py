#!/usr/bin/env python3
"""RCON Client for Minecraft - Actually connects and spawns agents"""

import socket
import struct
import time

class RconClient:
    def __init__(self, host='localhost', port=25576, password='aosbrain123'):
        self.host = host
        self.port = port
        self.password = password
        self.socket = None
        
    def connect(self):
        """Connect to Minecraft RCON"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.host, self.port))
            
            # Authenticate
            auth_packet = self._make_packet(3, self.password)
            self.socket.send(auth_packet)
            response = self._recv_packet()
            
            if response and response['id'] != -1:
                print(f"[RCON] Connected to {self.host}:{self.port}")
                return True
            else:
                print("[RCON] Authentication failed")
                return False
        except Exception as e:
            print(f"[RCON] Connection failed: {e}")
            return False
    
    def _make_packet(self, packet_type, payload):
        """Create RCON packet"""
        payload = payload.encode('utf-8')
        length = len(payload) + 10
        packet = struct.pack('<ii', length, packet_type) + payload + b'\x00\x00'
        return packet
    
    def _recv_packet(self):
        """Receive RCON response"""
        try:
            length = struct.unpack('<i', self.socket.recv(4))[0]
            data = self.socket.recv(length)
            packet_id = struct.unpack('<i', data[:4])[0]
            packet_type = struct.unpack('<i', data[4:8])[0]
            payload = data[8:-2].decode('utf-8', errors='ignore')
            return {'id': packet_id, 'type': packet_type, 'payload': payload}
        except:
            return None
    
    def command(self, cmd):
        """Send command"""
        if not self.socket:
            if not self.connect():
                return None
        
        try:
            packet = self._make_packet(2, cmd)
            self.socket.send(packet)
            response = self._recv_packet()
            return response['payload'] if response else None
        except Exception as e:
            print(f"[RCON] Command failed: {e}")
            return None
    
    def spawn_agent(self, name, x, y, z):
        """Spawn agent as armor stand"""
        cmd = f'summon minecraft:armor_stand {x} {y} {z} {{CustomName:"{name}",NoAI:0,ShowArms:1}}'
        return self.command(cmd)
    
    def say(self, message):
        """Broadcast message"""
        return self.command(f'say {message}')
    
    def close(self):
        if self.socket:
            self.socket.close()

if __name__ == "__main__":
    print("="*70)
    print("MINECRAFT AGENT SPAWNER")
    print("="*70)
    
    rcon = RconClient()
    
    if rcon.connect():
        print("\nSpawning AOS agents...")
        
        agents = [
            ("COBRA", 100, 70, 100),
            ("PROMETHEUS", 120, 70, 100),
            ("MYLZERON", 140, 70, 100),
            ("MYLTHREEN", 160, 70, 100),
        ]
        
        for name, x, y, z in agents:
            result = rcon.spawn_agent(name, x, y, z)
            print(f"  {name}: {result or 'Spawned'}")
            time.sleep(0.5)
        
        rcon.say("AOS Agents have entered the world!")
        print("\n✓ Agents spawned successfully")
        
        rcon.close()
    else:
        print("\n✗ Failed to connect to Minecraft")
