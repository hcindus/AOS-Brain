"""
Secure gRPC Bridge for AOS Brain ↔ PM01 Robot
Implements mutual TLS, short-lived certs, and action validation.

Author: Performance Supply Depot LLC
Security Level: P0 Hardened (per Jordan requirements)
"""

import asyncio
import logging
import ssl
import time
from dataclasses import dataclass
from typing import AsyncIterator, Optional
from pathlib import Path

import grpc
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

# Import generated protobuf
import sys
sys.path.insert(0, str(Path(__file__).parent))
import aos_pm01_pb2
import aos_pm01_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aos_pm01_bridge")


@dataclass
class BridgeConfig:
    """Bridge configuration with security parameters."""
    listen_host: str = "0.0.0.0"
    listen_port: int = 50051
    cert_dir: Path = Path("./certs")
    cert_validity_hours: int = 24  # Short-lived certs per Jordan's requirement
    max_action_rate: int = 100  # Hz - rate limiting
    action_timeout_ms: int = 50  # Max latency for action validation
    enable_mutual_tls: bool = True
    require_client_cert: bool = True


class CertificateManager:
    """Manages short-lived mTLS certificates."""
    
    def __init__(self, config: BridgeConfig):
        self.config = config
        self.cert_dir = config.cert_dir
        self.cert_dir.mkdir(parents=True, exist_ok=True)
        self._private_key: Optional[rsa.RSAPrivateKey] = None
        self._cert: Optional[x509.Certificate] = None
        self._ca_cert: Optional[x509.Certificate] = None
        
    def generate_ca(self) -> tuple[bytes, bytes]:
        """Generate CA certificate for signing client certs."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096
        )
        
        subject = issuer = x509.Name([
            x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, "Performance Supply Depot"),
            x509.NameAttribute(x509.NameOID.COMMON_NAME, "AOS-PM01-CA"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True
        ).sign(private_key, hashes.SHA256())
        
        # Save CA
        ca_key_path = self.cert_dir / "ca_key.pem"
        ca_cert_path = self.cert_dir / "ca_cert.pem"
        
        ca_key_path.write_bytes(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
        
        ca_cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        
        self._ca_cert = cert
        logger.info(f"CA certificate generated: {ca_cert_path}")
        
        return cert.public_bytes(serialization.Encoding.PEM), private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    
    def generate_server_cert(self, ca_key: rsa.RSAPrivateKey, ca_cert: x509.Certificate) -> tuple[bytes, bytes]:
        """Generate server certificate signed by CA."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096
        )
        
        subject = x509.Name([
            x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, "Performance Supply Depot"),
            x509.NameAttribute(x509.NameOID.COMMON_NAME, "aos-pm01-bridge"),
            x509.NameAttribute(x509.NameOID.DNS_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            ca_cert.subject
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(hours=self.config.cert_validity_hours)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
                x509.IPAddress(ipaddress.ip_address("::1")),
            ]),
            critical=False
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=False,
                crl_sign=False,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False
            ),
            critical=True
        ).sign(ca_key, hashes.SHA256())
        
        self._private_key = private_key
        self._cert = cert
        
        # Save server cert
        server_key_path = self.cert_dir / "server_key.pem"
        server_cert_path = self.cert_dir / "server_cert.pem"
        
        server_key_path.write_bytes(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
        
        server_cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        
        logger.info(f"Server certificate generated (valid {self.config.cert_validity_hours}h): {server_cert_path}")
        
        return cert.public_bytes(serialization.Encoding.PEM), private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    
    def get_ssl_context(self) -> ssl.SSLContext:
        """Create SSL context with mTLS."""
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        
        # Load server cert and key
        server_cert = self.cert_dir / "server_cert.pem"
        server_key = self.cert_dir / "server_key.pem"
        ca_cert = self.cert_dir / "ca_cert.pem"
        
        context.load_cert_chain(str(server_cert), str(server_key))
        
        if self.config.require_client_cert:
            context.load_verify_locations(str(ca_cert))
            context.verify_mode = ssl.CERT_REQUIRED
        
        return context


class ActionValidator:
    """Validates RL actions before sending to robot controller."""
    
    # Safety limits (tunable per deployment)
    MAX_JOINT_VELOCITY = 10.0  # rad/s
    MAX_LINEAR_VELOCITY = 2.0  # m/s
    MAX_ANGULAR_VELOCITY = 3.0  # rad/s
    
    def __init__(self, config: BridgeConfig):
        self.config = config
        self._last_action_time = 0
        self._action_count = 0
        
    def validate(self, action: aos_pm01_pb2.RLAction) -> tuple[bool, str]:
        """
        Validate RL action against safety constraints.
        Returns (is_valid, error_message)
        """
        # Rate limiting check
        current_time = time.time_ns() // 1_000_000  # ms
        if current_time - self._last_action_time < (1000 / self.config.max_action_rate):
            return False, f"Action rate exceeded: {self.config.max_action_rate}Hz max"
        
        # Validate joint targets
        for i, target in enumerate(action.joint_targets):
            if abs(target) > self.MAX_JOINT_VELOCITY:
                return False, f"Joint {i} velocity {target} exceeds limit {self.MAX_JOINT_VELOCITY}"
        
        # Validate base velocity
        base = action.base_velocity
        linear_speed = (base.linear_x**2 + base.linear_y**2 + base.linear_z**2) ** 0.5
        if linear_speed > self.MAX_LINEAR_VELOCITY:
            return False, f"Linear velocity {linear_speed} exceeds limit {self.MAX_LINEAR_VELOCITY}"
        
        angular_speed = (base.angular_x**2 + base.angular_y**2 + base.angular_z**2) ** 0.5
        if angular_speed > self.MAX_ANGULAR_VELOCITY:
            return False, f"Angular velocity {angular_speed} exceeds limit {self.MAX_ANGULAR_VELOCITY}"
        
        self._last_action_time = current_time
        self._action_count += 1
        
        return True, ""


class AgentPersonality:
    """Base class for agent personalities."""
    
    def __init__(self, agent_id: str, config: dict):
        self.agent_id = agent_id
        self.config = config
        self.state = {}
        
    async def process_intent(self, intent: aos_pm01_pb2.IntentCommand) -> aos_pm01_pb2.RLAction:
        """Convert high-level intent to RL action."""
        raise NotImplementedError
    
    async def observe(self, state: aos_pm01_pb2.RobotState) -> None:
        """Process incoming robot state."""
        self.state.update({
            'pose': state.robot_pose,
            'battery': state.battery.percentage,
            'timestamp': state.timestamp
        })


class AOSPM01Servicer(aos_pm01_pb2_grpc.AOSPM01BridgeServicer):
    """gRPC service implementing secure brain-robot bridge."""
    
    def __init__(self, config: BridgeConfig):
        self.config = config
        self.validator = ActionValidator(config)
        self.agents: dict[str, AgentPersonality] = {}
        self._state_streams: dict[str, asyncio.Queue] = {}
        
    async def SendCommand(self, request: aos_pm01_pb2.IntentCommand, context: grpc.ServicerContext) -> aos_pm01_pb2.CommandAck:
        """Receive high-level intent command from AOS Brain."""
        logger.info(f"Received command for agent {request.agent_id}: {request.command_type}")
        
        # Validate agent exists
        if request.agent_id not in self.agents:
            return aos_pm01_pb2.CommandAck(
                success=False,
                error_message=f"Unknown agent: {request.agent_id}",
                processed_timestamp=time.time_ns() // 1_000_000
            )
        
        # Process intent (async)
        agent = self.agents[request.agent_id]
        try:
            action = await agent.process_intent(request)
            
            # Validate action
            is_valid, error = self.validator.validate(action)
            if not is_valid:
                return aos_pm01_pb2.CommandAck(
                    success=False,
                    error_message=f"Action validation failed: {error}",
                    processed_timestamp=time.time_ns() // 1_000_000
                )
            
            # Forward to robot (implementation pending)
            # await self._send_to_robot(action)
            
            return aos_pm01_pb2.CommandAck(
                success=True,
                error_message="",
                processed_timestamp=time.time_ns() // 1_000_000
            )
            
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            return aos_pm01_pb2.CommandAck(
                success=False,
                error_message=str(e),
                processed_timestamp=time.time_ns() // 1_000_000
            )
    
    async def StreamState(self, request: aos_pm01_pb2.StateRequest, context: grpc.ServicerContext) -> AsyncIterator[aos_pm01_pb2.RobotState]:
        """Stream robot state to AOS Brain."""
        logger.info(f"State stream requested for agent {request.agent_id} at {request.update_rate_hz}Hz")
        
        queue = asyncio.Queue()
        self._state_streams[request.agent_id] = queue
        
        try:
            while context.is_active():
                try:
                    state = await asyncio.wait_for(queue.get(), timeout=1.0)
                    yield state
                except asyncio.TimeoutError:
                    continue
        finally:
            del self._state_streams[request.agent_id]
    
    async def AgentLoop(self, request_iterator: AsyncIterator[aos_pm01_pb2.IntentCommand], 
                       context: grpc.ServicerContext) -> AsyncIterator[aos_pm01_pb2.RLAction]:
        """Bidirectional streaming: intent in, actions out."""
        logger.info("Agent loop started")
        
        async for intent in request_iterator:
            if intent.agent_id in self.agents:
                agent = self.agents[intent.agent_id]
                action = await agent.process_intent(intent)
                
                is_valid, error = self.validator.validate(action)
                if is_valid:
                    yield action
                else:
                    logger.warning(f"Action rejected: {error}")


class SecureBridge:
    """Main bridge server with security hardening."""
    
    def __init__(self, config: BridgeConfig = None):
        self.config = config or BridgeConfig()
        self.cert_manager = CertificateManager(self.config)
        self.servicer = AOSPM01Servicer(self.config)
        self.server = None
        
    def initialize(self) -> None:
        """Generate certificates and initialize server."""
        import ipaddress
        
        # Generate CA
        ca_cert_pem, ca_key_pem = self.cert_manager.generate_ca()
        
        # Load CA key for signing
        ca_key = serialization.load_pem_private_key(ca_key_pem, password=None)
        ca_cert = x509.load_pem_x509_certificate(ca_cert_pem)
        
        # Generate server cert
        self.cert_manager.generate_server_cert(ca_key, ca_cert)
        
        logger.info("Certificate initialization complete")
        
    async def start(self) -> None:
        """Start secure gRPC server."""
        self.initialize()
        
        # Create server with TLS
        ssl_context = self.cert_manager.get_ssl_context()
        
        self.server = grpc.aio.server()
        aos_pm01_pb2_grpc.add_AOSPM01BridgeServicer_to_server(self.servicer, self.server)
        
        listen_addr = f"{self.config.listen_host}:{self.config.listen_port}"
        self.server.add_secure_port(listen_addr, grpc.ssl_server_credentials(
            private_key_certificate_chain_pairs=[(
                (self.cert_manager.cert_dir / "server_key.pem").read_bytes(),
                (self.cert_manager.cert_dir / "server_cert.pem").read_bytes()
            )],
            root_certificates=(self.cert_manager.cert_dir / "ca_cert.pem").read_bytes(),
            require_client_auth=self.config.require_client_tls
        ))
        
        await self.server.start()
        logger.info(f"Secure bridge listening on {listen_addr} (mTLS enabled)")
        
        await self.server.wait_for_termination()
        
    async def stop(self) -> None:
        """Graceful shutdown."""
        if self.server:
            await self.server.stop(grace_period=5)
            logger.info("Bridge server stopped")


# Example agent implementations
class MilesAgent(AgentPersonality):
    """Sales consultant personality."""
    
    async def process_intent(self, intent: aos_pm01_pb2.IntentCommand) -> aos_pm01_pb2.RLAction:
        """Miles prioritizes social navigation."""
        # Simple example: move toward target
        action = aos_pm01_pb2.RLAction(
            agent_id=self.agent_id,
            joint_targets=[],
            base_velocity=aos_pm01_pb2.Pose(
                linear_x=0.5,  # Walk forward
                linear_y=0.0,
                linear_z=0.0,
                angular_x=0.0,
                angular_y=0.0,
                angular_z=0.0
            ),
            timestamp=time.time_ns() // 1_000_000
        )
        return action


async def main():
    """Main entry point."""
    config = BridgeConfig(
        listen_port=50051,
        cert_validity_hours=24,
        require_client_cert=True
    )
    
    bridge = SecureBridge(config)
    
    # Register agents
    bridge.servicer.agents["miles"] = MilesAgent("miles", {})
    
    try:
        await bridge.start()
    except KeyboardInterrupt:
        await bridge.stop()


if __name__ == "__main__":
    asyncio.run(main())
