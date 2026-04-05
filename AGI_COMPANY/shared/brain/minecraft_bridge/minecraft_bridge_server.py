#!/usr/bin/env python3
"""
Minecraft Bridge Server
Connects AOS Brain to Minecraft server

Provides:
- Observer: Reads world state, sends to brain
- Actor: Receives brain actions, executes in Minecraft

Usage: python minecraft_bridge_server.py
"""

import socket
import json
import threading
import time
import logging
from typing import Dict, Optional
from datetime import datetime

# Configuration
MINECRAFT_RCON_HOST = "localhost"
MINECRAFT_RCON_PORT = 25575
MINECRAFT_RCON_PASSWORD = "aosbrain123"

OBSERVER_PORT = 8765
ACTOR_PORT = 8766

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MinecraftBridge")


class MinecraftRCON:
    """RCON client for Minecraft server"""
    
    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password
        self.socket = None
        self.request_id = 0
        self.connected = False
        
    def connect(self) -> bool:
        """Connect to Minecraft RCON"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.host, self.port))
            
            # Authenticate
            if self._send_packet(3, self.password):
                response = self._receive_packet()
                if response and response.get('id', -1) != -1:
                    self.connected = True
                    logger.info("Connected to Minecraft RCON")
                    return True
                    
            logger.error("RCON authentication failed")
            return False
            
        except Exception as e:
            logger.error(f"Failed to connect to RCON: {e}")
            return False
    
    def _send_packet(self, packet_type: int, payload: str) -> bool:
        """Send RCON packet"""
        try:
            self.request_id += 1
            packet_id = self.request_id
            
            # Build packet
            payload_bytes = payload.encode('utf-8')
            packet = (
                packet_id.to_bytes(4, 'little') +
                packet_type.to_bytes(4, 'little') +
                payload_bytes +
                b'\x00\x00'
            )
            length = len(packet)
            
            self.socket.send(length.to_bytes(4, 'little') + packet)
            return True
            
        except Exception as e:
            logger.error(f"Failed to send packet: {e}")
            return False
    
    def _receive_packet(self) -> Optional[Dict]:
        """Receive RCON packet"""
        try:
            # Read length
            length_data = self.socket.recv(4)
            if not length_data:
                return None
            length = int.from_bytes(length_data, 'little')
            
            # Read packet
            data = self.socket.recv(length)
            
            # Parse
            packet_id = int.from_bytes(data[0:4], 'little')
            packet_type = int.from_bytes(data[4:8], 'little')
            payload = data[8:-2].decode('utf-8')
            
            return {'id': packet_id, 'type': packet_type, 'payload': payload}
            
        except Exception as e:
            logger.error(f"Failed to receive packet: {e}")
            return None
    
    def command(self, cmd: str) -> str:
        """Send command and get response"""
        if not self.connected:
            return "Not connected"
        
        if self._send_packet(2, cmd):
            response = self._receive_packet()
            if response:
                return response.get('payload', '')
        
        return "Error"
    
    def close(self):
        """Close connection"""
        if self.socket:
            self.socket.close()
            self.connected = False


class ObserverServer:
    """
    Observer service - sends world state to brains
    """
    
    def __init__(self, rcon: MinecraftRCON, port: int = OBSERVER_PORT):
        self.rcon = rcon
        self.port = port
        self.socket = None
        self.running = False
        
    def start(self):
        """Start observer server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(5)
        self.running = True
        
        logger.info(f"Observer server listening on port {self.port}")
        
        while self.running:
            try:
                client, addr = self.socket.accept()
                logger.info(f"Observer client connected from {addr}")
                
                # Handle client in thread
                thread = threading.Thread(target=self._handle_client, args=(client,))
                thread.daemon = True
                thread.start()
                
            except Exception as e:
                if self.running:
                    logger.error(f"Observer error: {e}")
    
    def _handle_client(self, client: socket.socket):
        """Handle observer client"""
        try:
            while self.running:
                # Get world state from Minecraft
                world_state = self._get_world_state()
                
                # Send to client
                response = json.dumps(world_state) + '\n'
                client.send(response.encode())
                
                # Wait before next update (20 TPS)
                time.sleep(0.05)
                
        except Exception as e:
            logger.info(f"Observer client disconnected: {e}")
        finally:
            client.close()
    
    def _get_world_state(self) -> Dict:
        """Get current world state from Minecraft"""
        try:
            # Get time
            time_response = self.rcon.command("time query daytime")
            time_of_day = int(time_response.split()[-1]) if 'Day time' in time_response else 0
            
            # Get player list
            players_response = self.rcon.command("list")
            player_count = 0
            if 'players online' in players_response:
                player_count = int(players_response.split('of')[0].split()[-1])
            
            return {
                "timestamp": datetime.now().isoformat(),
                "time_of_day": time_of_day,
                "is_day": time_of_day < 12000,
                "players_online": player_count,
                "status": "active"
            }
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "status": "error"
            }
    
    def stop(self):
        """Stop observer server"""
        self.running = False
        if self.socket:
            self.socket.close()


class ActorServer:
    """
    Actor service - receives actions from brains, executes in Minecraft
    """
    
    def __init__(self, rcon: MinecraftRCON, port: int = ACTOR_PORT):
        self.rcon = rcon
        self.port = port
        self.socket = None
        self.running = False
        self.agents: Dict[str, Dict] = {}
        
    def start(self):
        """Start actor server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(5)
        self.running = True
        
        logger.info(f"Actor server listening on port {self.port}")
        
        while self.running:
            try:
                client, addr = self.socket.accept()
                logger.info(f"Actor client connected from {addr}")
                
                # Handle client
                thread = threading.Thread(target=self._handle_client, args=(client,))
                thread.daemon = True
                thread.start()
                
            except Exception as e:
                if self.running:
                    logger.error(f"Actor error: {e}")
    
    def _handle_client(self, client: socket.socket):
        """Handle actor client"""
        buffer = ""
        
        try:
            while self.running:
                data = client.recv(4096).decode()
                if not data:
                    break
                
                buffer += data
                
                # Process complete JSON lines
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self._process_action(line)
                    
        except Exception as e:
            logger.info(f"Actor client disconnected: {e}")
        finally:
            client.close()
    
    def _process_action(self, data: str):
        """Process action from brain"""
        try:
            action = json.loads(data)
            action_type = action.get('type')
            
            if action_type == 'spawn_agent':
                self._spawn_agent(action)
            elif action_type == 'agent_action':
                self._execute_action(action)
            else:
                logger.warning(f"Unknown action type: {action_type}")
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON: {data[:100]}")
        except Exception as e:
            logger.error(f"Error processing action: {e}")
    
    def _spawn_agent(self, action: Dict):
        """Spawn agent in Minecraft"""
        agent_id = action.get('agent_id', 'unknown')
        x = action.get('x', 0)
        y = action.get('y', 100)
        z = action.get('z', 0)
        
        # Summon player entity for agent
        cmd = f"summon minecraft:armor_stand {x} {y} {z} {{CustomName:'\"{agent_id}\"',NoAI:1}}"
        result = self.rcon.command(cmd)
        
        self.agents[agent_id] = {
            'position': [x, y, z],
            'spawned': datetime.now().isoformat()
        }
        
        logger.info(f"Spawned agent {agent_id} at ({x}, {y}, {z})")
    
    def _execute_action(self, action: Dict):
        """Execute agent action"""
        agent_id = action.get('agent_id')
        action_cmd = action.get('action')
        params = action.get('params', {})
        
        # Map to Minecraft commands
        if action_cmd == 'move':
            dx = params.get('dx', 0)
            dy = params.get('dy', 0)
            dz = params.get('dz', 0)
            cmd = f"execute as @e[type=armor_stand,name={agent_id}] run tp ~{dx} ~{dy} ~{dz}"
            
        elif action_cmd == 'look':
            yaw = params.get('yaw', 0)
            pitch = params.get('pitch', 0)
            cmd = f"execute as @e[type=armor_stand,name={agent_id}] run data merge entity @s {{Rotation:[{yaw}f,{pitch}f]}}"
            
        elif action_cmd == 'chat':
            message = params.get('message', '')
            cmd = f"say <{agent_id}> {message}"
            
        elif action_cmd == 'break_block':
            cmd = f"execute as @e[type=armor_stand,name={agent_id}] at @s run setblock ~ ~ ~ air"
            
        elif action_cmd == 'place_block':
            block_type = params.get('type', 'stone')
            cmd = f"execute as @e[type=armor_stand,name={agent_id}] at @s run setblock ~ ~ ~ {block_type}"
            
        else:
            cmd = f"say {agent_id} attempted {action_cmd}"
        
        result = self.rcon.command(cmd)
        logger.debug(f"Executed: {cmd} -> {result}")
    
    def stop(self):
        """Stop actor server"""
        self.running = False
        if self.socket:
            self.socket.close()


def main():
    """Run Minecraft Bridge Server"""
    print("=" * 70)
    print("MINECRAFT BRIDGE SERVER")
    print("=" * 70)
    print("\nConnecting to Minecraft server...")
    print(f"  RCON: {MINECRAFT_RCON_HOST}:{MINECRAFT_RCON_PORT}")
    print(f"  Observer: port {OBSERVER_PORT}")
    print(f"  Actor: port {ACTOR_PORT}")
    
    # Connect to Minecraft
    rcon = MinecraftRCON(MINECRAFT_RCON_HOST, MINECRAFT_RCON_PORT, MINECRAFT_RCON_PASSWORD)
    
    if not rcon.connect():
        print("\n❌ Failed to connect to Minecraft RCON")
        print("Make sure:")
        print("  1. Minecraft server is running")
        print("  2. RCON is enabled in server.properties")
        print("  3. Password is correct")
        return
    
    print("\n✅ Connected to Minecraft RCON")
    
    # Start servers
    observer = ObserverServer(rcon, OBSERVER_PORT)
    actor = ActorServer(rcon, ACTOR_PORT)
    
    observer_thread = threading.Thread(target=observer.start)
    actor_thread = threading.Thread(target=actor.start)
    
    observer_thread.daemon = True
    actor_thread.daemon = True
    
    observer_thread.start()
    actor_thread.start()
    
    print("\n✅ Bridge servers running:")
    print(f"  - Observer: localhost:{OBSERVER_PORT}")
    print(f"  - Actor: localhost:{ACTOR_PORT}")
    print("\nPress Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        observer.stop()
        actor.stop()
        rcon.close()
        print("Bridge server stopped")


if __name__ == "__main__":
    main()
