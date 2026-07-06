"""
AOS Socket Client for Brain Integration
Connects AOS Brain (Unix socket) to PM01 gRPC Bridge
"""

import asyncio
import json
import logging
import socket
from pathlib import Path
from typing import Optional

import grpc

from bridge.secure_bridge import BridgeConfig, CertificateManager
import aos_pm01_pb2
import aos_pm01_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aos_client")


class AOSBrainClient:
    """Client connecting AOS Brain Unix socket to PM01 gRPC bridge."""
    
    def __init__(self, brain_socket: str = "/tmp/aos_brain.sock", 
                 bridge_host: str = "localhost", 
                 bridge_port: int = 50051,
                 cert_dir: Path = Path("./certs")):
        self.brain_socket = brain_socket
        self.bridge_host = bridge_host
        self.bridge_port = bridge_port
        self.cert_dir = cert_dir
        self.grpc_channel: Optional[grpc.Channel] = None
        self.stub: Optional[aos_pm01_pb2_grpc.AOSPM01BridgeStub] = None
        
    def _create_secure_channel(self) -> grpc.Channel:
        """Create mTLS-secured gRPC channel."""
        # Load client certificate
        client_cert = self.cert_dir / "client_cert.pem"
        client_key = self.cert_dir / "client_key.pem"
        ca_cert = self.cert_dir / "ca_cert.pem"
        
        if not all(p.exists() for p in [client_cert, client_key, ca_cert]):
            raise FileNotFoundError("Client certificates not found. Run generate_client_certs.py first.")
        
        credentials = grpc.ssl_channel_credentials(
            root_certificates=ca_cert.read_bytes(),
            private_key=client_key.read_bytes(),
            certificate_chain=client_cert.read_bytes()
        )
        
        target = f"{self.bridge_host}:{self.bridge_port}"
        return grpc.secure_channel(target, credentials)
    
    async def connect_brain(self) -> None:
        """Connect to AOS Brain Unix socket."""
        self.brain_reader, self.brain_writer = await asyncio.open_unix_connection(self.brain_socket)
        logger.info(f"Connected to AOS Brain at {self.brain_socket}")
        
    async def connect_bridge(self) -> None:
        """Connect to PM01 gRPC bridge."""
        self.grpc_channel = self._create_secure_channel()
        self.stub = aos_pm01_pb2_grpc.AOSPM01BridgeStub(self.grpc_channel)
        logger.info(f"Connected to PM01 bridge at {self.bridge_host}:{self.bridge_port}")
        
    async def brain_to_bridge_loop(self) -> None:
        """Forward commands from AOS Brain to PM01."""
        while True:
            try:
                # Read from brain socket
                data = await self.brain_reader.readline()
                if not data:
                    break
                    
                message = json.loads(data.decode())
                
                # Convert brain command to intent
                intent = self._brain_to_intent(message)
                
                # Send to PM01
                response = await self.stub.SendCommand(intent)
                
                if not response.success:
                    logger.warning(f"Command failed: {response.error_message}")
                    
            except Exception as e:
                logger.error(f"Brain-to-bridge error: {e}")
                await asyncio.sleep(1)
                
    async def bridge_to_brain_loop(self) -> None:
        """Forward state from PM01 to AOS Brain."""
        request = aos_pm01_pb2.StateRequest(
            agent_id="miles",  # TODO: dynamic
            update_rate_hz=50
        )
        
        try:
            async for state in self.stub.StreamState(request):
                # Convert state to brain format
                brain_message = self._state_to_brain(state)
                
                # Send to brain
                self.brain_writer.write(json.dumps(brain_message).encode() + b'\n')
                await self.brain_writer.drain()
                
        except Exception as e:
            logger.error(f"Bridge-to-brain error: {e}")
            
    def _brain_to_intent(self, message: dict) -> aos_pm01_pb2.IntentCommand:
        """Convert AOS Brain message to IntentCommand."""
        return aos_pm01_pb2.IntentCommand(
            agent_id=message.get("agent_id", "miles"),
            command_type=message.get("command", "navigate"),
            target=aos_pm01_pb2.Target(
                location=aos_pm01_pb2.Location(
                    x=message.get("x", 0.0),
                    y=message.get("y", 0.0),
                    z=message.get("z", 0.0),
                    frame_id=message.get("frame", "map")
                )
            ),
            context=aos_pm01_pb2.Context(
                scene_description=message.get("scene", "")
            ),
            timestamp=int(asyncio.get_event_loop().time() * 1000)
        )
        
    def _state_to_brain(self, state: aos_pm01_pb2.RobotState) -> dict:
        """Convert RobotState to AOS Brain format."""
        return {
            "type": "robot_state",
            "agent_id": state.agent_id,
            "pose": {
                "x": state.robot_pose.linear_x,
                "y": state.robot_pose.linear_y,
                "z": state.robot_pose.linear_z,
            },
            "battery": state.battery.percentage,
            "behavior": state.behavior_state,
            "timestamp": state.timestamp
        }
        
    async def run(self) -> None:
        """Main run loop."""
        await self.connect_brain()
        await self.connect_bridge()
        
        # Run both directions concurrently
        await asyncio.gather(
            self.brain_to_bridge_loop(),
            self.bridge_to_brain_loop()
        )


async def main():
    client = AOSBrainClient()
    await client.run()


if __name__ == "__main__":
    asyncio.run(main())
