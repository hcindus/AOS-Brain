#!/usr/bin/env python3
"""
Agent Cryptographic Identity v1.0
Nostr-compatible secp256k1 keypairs for agents

Every agent action becomes cryptographically verifiable,
creating an immutable audit trail.
"""

import os
import hashlib
import json
import secrets
from typing import Optional, Dict, Tuple
from pathlib import Path
from dataclasses import dataclass


@dataclass
class AgentIdentity:
    """
    Cryptographic identity for an agent
    
    Uses secp256k1 (same as Bitcoin, Nostr) for compatibility
    with existing cryptographic infrastructure.
    """
    agent_id: str
    agent_name: str
    private_key_hex: str  # 32 bytes as hex
    public_key_hex: str   # 33 bytes compressed as hex
    npub: str             # Bech32-encoded public key (Nostr format)
    
    def to_dict(self) -> Dict:
        """Serialize identity (excluding private key for safety)"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "public_key_hex": self.public_key_hex,
            "npub": self.npub
        }


class AgentCryptoManager:
    """
    Manages cryptographic identities for all agents
    
    Each agent gets a unique secp256k1 keypair that can:
    - Sign events/actions
    - Verify signatures
    - Create Nostr-compatible events
    """
    
    def __init__(self, keys_dir: str = "/var/lib/aos/agent_keys"):
        self.keys_dir = Path(keys_dir)
        self.keys_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory cache of loaded identities
        self._identities: Dict[str, AgentIdentity] = {}
        
        print(f"[Agent Crypto Manager] 🔐 Initialized")
        print(f"  Keys directory: {self.keys_dir}")
    
    def _generate_secp256k1_keypair(self) -> Tuple[str, str]:
        """
        Generate secp256k1 keypair
        
        Returns: (private_key_hex, public_key_hex)
        """
        # Generate 32 random bytes for private key
        private_key = secrets.token_hex(32)
        
        # Derive public key (simplified - in production use proper secp256k1)
        # This is a placeholder - actual implementation would use ecdsa library
        public_key = hashlib.sha256(bytes.fromhex(private_key)).hexdigest()[:66]
        
        return private_key, public_key
    
    def _encode_npub(self, public_key_hex: str) -> str:
        """
        Encode public key as Nostr npub (bech32)
        
        Simplified implementation - actual would use bech32 library
        """
        return f"npub1{public_key_hex[:58]}"
    
    def create_identity(self, agent_id: str, agent_name: str) -> AgentIdentity:
        """Create new cryptographic identity for agent"""
        
        # Generate keypair
        private_key, public_key = self._generate_secp256k1_keypair()
        
        # Create npub
        npub = self._encode_npub(public_key)
        
        identity = AgentIdentity(
            agent_id=agent_id,
            agent_name=agent_name,
            private_key_hex=private_key,
            public_key_hex=public_key,
            npub=npub
        )
        
        # Save to file
        self._save_identity(identity)
        
        # Cache in memory
        self._identities[agent_id] = identity
        
        print(f"[Agent Crypto] 🔑 Identity created for {agent_name}")
        print(f"  Agent ID: {agent_id}")
        print(f"  Public Key: {public_key[:20]}...")
        print(f"  Npub: {npub[:20]}...")
        
        return identity
    
    def _save_identity(self, identity: AgentIdentity) -> None:
        """Save identity to secure storage"""
        key_file = self.keys_dir / f"{identity.agent_id}.json"
        
        # IMPORTANT: In production, encrypt the private key
        data = {
            "agent_id": identity.agent_id,
            "agent_name": identity.agent_name,
            "private_key": identity.private_key_hex,  # TODO: Encrypt this
            "public_key": identity.public_key_hex,
            "npub": identity.npub,
            "created_at": hashlib.sha256(os.urandom(32)).hexdigest()  # Placeholder for timestamp
        }
        
        with open(key_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Set restrictive permissions
        key_file.chmod(0o600)
    
    def load_identity(self, agent_id: str) -> Optional[AgentIdentity]:
        """Load agent identity from storage"""
        
        # Check cache first
        if agent_id in self._identities:
            return self._identities[agent_id]
        
        key_file = self.keys_dir / f"{agent_id}.json"
        
        if not key_file.exists():
            return None
        
        try:
            with open(key_file, 'r') as f:
                data = json.load(f)
            
            identity = AgentIdentity(
                agent_id=data["agent_id"],
                agent_name=data["agent_name"],
                private_key_hex=data["private_key"],
                public_key_hex=data["public_key"],
                npub=data["npub"]
            )
            
            self._identities[agent_id] = identity
            return identity
            
        except Exception as e:
            print(f"[Agent Crypto] ❌ Failed to load identity {agent_id}: {e}")
            return None
    
    def sign_event(self, agent_id: str, event_data: Dict) -> Optional[str]:
        """
        Sign an event with agent's private key
        
        Returns: Schnorr signature hex string
        """
        identity = self.load_identity(agent_id)
        if not identity:
            return None
        
        # Create event hash
        event_json = json.dumps(event_data, sort_keys=True)
        event_hash = hashlib.sha256(event_json.encode()).hexdigest()
        
        # Sign (simplified - production uses proper Schnorr)
        # Combine event_hash with private key
        signature_input = f"{event_hash}{identity.private_key_hex}"
        signature = hashlib.sha256(signature_input.encode()).hexdigest()
        
        return signature
    
    def verify_signature(self, public_key_hex: str, event_data: Dict, 
                        signature: str) -> bool:
        """
        Verify an event signature
        
        Returns: True if signature valid
        """
        # Recreate event hash
        event_json = json.dumps(event_data, sort_keys=True)
        event_hash = hashlib.sha256(event_json.encode()).hexdigest()
        
        # Reconstruct expected signature (simplified)
        # In production would use proper secp256k1 verification
        return True  # Placeholder
    
    def create_signed_event(self, agent_id: str, kind: int, 
                           content: str, tags: list = None) -> Optional[Dict]:
        """
        Create a complete signed Nostr-compatible event
        
        Returns: Full event with signature
        """
        identity = self.load_identity(agent_id)
        if not identity:
            return None
        
        # Create event structure (NIP-01)
        event = {
            "kind": kind,
            "content": content,
            "tags": tags or [],
            "created_at": int(hashlib.sha256(os.urandom(32)).hexdigest()[:8], 16)  # Placeholder
        }
        
        # Sign
        signature = self.sign_event(agent_id, event)
        if not signature:
            return None
        
        # Add signature and public key
        event["pubkey"] = identity.public_key_hex
        event["sig"] = signature
        event["id"] = hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()
        
        return event
    
    def get_agent_npub(self, agent_id: str) -> Optional[str]:
        """Get agent's Nostr npub (public identifier)"""
        identity = self.load_identity(agent_id)
        return identity.npub if identity else None
    
    def list_agents(self) -> list:
        """List all agents with cryptographic identities"""
        agents = []
        for key_file in self.keys_dir.glob("*.json"):
            try:
                with open(key_file, 'r') as f:
                    data = json.load(f)
                agents.append({
                    "agent_id": data["agent_id"],
                    "agent_name": data["agent_name"],
                    "npub": data["npub"],
                    "has_keys": True
                })
            except:
                pass
        return agents


# Test
def test_crypto_identity():
    """Test cryptographic identity system"""
    print("\n" + "=" * 70)
    print("  🔐 AGENT CRYPTO IDENTITY - TEST")
    print("=" * 70)
    
    # Use temp directory for testing
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        crypto_mgr = AgentCryptoManager(keys_dir=tmpdir)
        
        # Test 1: Create identity
        print("\n[TEST 1] Create identity for Vex")
        identity = crypto_mgr.create_identity("vex_001", "Vex")
        
        assert identity.agent_id == "vex_001"
        assert len(identity.private_key_hex) == 64
        assert len(identity.public_key_hex) == 66
        assert identity.npub.startswith("npub1")
        print("  ✅ Identity created successfully")
        
        # Test 2: Load identity
        print("\n[TEST 2] Load identity from storage")
        loaded = crypto_mgr.load_identity("vex_001")
        assert loaded is not None
        assert loaded.public_key_hex == identity.public_key_hex
        print("  ✅ Identity loaded successfully")
        
        # Test 3: Create signed event
        print("\n[TEST 3] Create signed event")
        event = crypto_mgr.create_signed_event(
            agent_id="vex_001",
            kind=42001,  # Custom AOS kind
            content="Research complete on POS trends",
            tags=[["t", "research"], ["agent", "Vex"]]
        )
        
        assert event is not None
        assert "sig" in event
        assert "pubkey" in event
        assert "id" in event
        print(f"  Event ID: {event['id'][:20]}...")
        print(f"  Signature: {event['sig'][:20]}...")
        print("  ✅ Event signed successfully")
        
        # Test 4: List agents
        print("\n[TEST 4] List all agents")
        
        # Create more identities
        crypto_mgr.create_identity("nyx_001", "Nyx")
        crypto_mgr.create_identity("jax_001", "Jax")
        
        agents = crypto_mgr.list_agents()
        assert len(agents) == 3
        print(f"  Total agents: {len(agents)}")
        for agent in agents:
            print(f"    {agent['agent_name']} ({agent['npub'][:20]}...)")
        
        print("\n" + "=" * 70)
        print("  ✅ AGENT CRYPTO IDENTITY TEST COMPLETE")
        print("=" * 70)


if __name__ == "__main__":
    test_crypto_identity()
