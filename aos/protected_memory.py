#!/usr/bin/env python3
"""
Protected Memory Segments v1.0
Prevents Brain from modifying critical identity files

Like write-protected firmware - the Brain can read but cannot overwrite
core identity without elevated authorization.
"""

import os
import hashlib
import json
from pathlib import Path
from typing import Set, Optional
from datetime import datetime


class ProtectedMemory:
    """
    Hardware-enforced (convention-enforced) protected zones
    
    Protects:
    - SOUL.md (core identity)
    - IDENTITY.md (who we are)
    - HEARTBEAT.md (system status)
    - AGENTS.md (behavioral rules)
    
    Access Levels:
    - READ: Always allowed
    - WRITE: Requires elevated permissions
    - DELETE: Never allowed (immutable)
    """
    
    # Core protected files
    PROTECTED_FILES = [
        "SOUL.md",
        "IDENTITY.md", 
        "HEARTBEAT.md",
        "AGENTS.md",
        "USER.md"
    ]
    
    # Immutable files (read-only forever)
    IMMUTABLE_FILES = [
        "SOUL.md",
        "IDENTITY.md"
    ]
    
    def __init__(self, workspace_path: str = "/root/.openclaw/workspace"):
        self.workspace = Path(workspace_path)
        self.protected_hashes: dict = {}
        self.access_log: list = []
        
        # Calculate hashes of protected files
        self._calculate_hashes()
        
        print(f"[Protected Memory v1.0] Initialized")
        print(f"  🛡️  {len(self.PROTECTED_FILES)} files protected")
        print(f"  🔒 {len(self.IMMUTABLE_FILES)} files immutable")
        self._print_status()
    
    def _calculate_hashes(self):
        """Calculate hashes of protected files for integrity checking"""
        for filename in self.PROTECTED_FILES:
            filepath = self.workspace / filename
            if filepath.exists():
                with open(filepath, 'rb') as f:
                    content = f.read()
                    self.protected_hashes[filename] = hashlib.sha256(content).hexdigest()
    
    def _print_status(self):
        """Print current protection status"""
        for filename in self.PROTECTED_FILES:
            filepath = self.workspace / filename
            status = "✅ Protected" if filepath.exists() else "⚠️  Missing"
            immutable = " (IMMUTABLE)" if filename in self.IMMUTABLE_FILES else ""
            print(f"    {filename}: {status}{immutable}")
    
    def is_protected(self, filepath: str) -> bool:
        """Check if a file is protected"""
        path = Path(filepath)
        filename = path.name
        return filename in self.PROTECTED_FILES
    
    def is_immutable(self, filepath: str) -> bool:
        """Check if a file is immutable (read-only)"""
        path = Path(filepath)
        filename = path.name
        return filename in self.IMMUTABLE_FILES
    
    def verify_integrity(self, filepath: str) -> bool:
        """Verify file hasn't been modified"""
        path = Path(filepath)
        filename = path.name
        
        if filename not in self.protected_hashes:
            return True  # Not a protected file
        
        if not path.exists():
            return False  # File missing!
        
        with open(path, 'rb') as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()
        
        return current_hash == self.protected_hashes[filename]
    
    def request_write(self, filepath: str, reason: str, 
                       elevated: bool = False) -> tuple:
        """
        Request write access to protected file
        
        Returns: (granted: bool, message: str)
        """
        path = Path(filepath)
        filename = path.name
        
        # Log the request
        self.access_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'file': filename,
            'reason': reason,
            'elevated': elevated,
            'granted': False
        })
        
        # Check if protected
        if not self.is_protected(filepath):
            return True, "File not protected"
        
        # Check if immutable
        if self.is_immutable(filepath):
            return False, f"{filename} is IMMUTABLE - cannot be modified"
        
        # Protected but not immutable - requires elevation
        if not elevated:
            return False, f"{filename} is PROTECTED - requires elevated permissions"
        
        # Elevated access granted for non-immutable files
        self.access_log[-1]['granted'] = True
        return True, f"Elevated access granted for {filename}"
    
    def get_protection_status(self) -> dict:
        """Get full protection status"""
        status = {
            'protected_files': {},
            'integrity_check': {},
            'recent_access': self.access_log[-10:]  # Last 10 requests
        }
        
        for filename in self.PROTECTED_FILES:
            filepath = self.workspace / filename
            status['protected_files'][filename] = {
                'exists': filepath.exists(),
                'immutable': filename in self.IMMUTABLE_FILES,
                'integrity': self.verify_integrity(filepath)
            }
        
        return status
    
    def create_elevated_session(self, password: str) -> bool:
        """
        Create elevated session for protected writes
        
        In production, this would use proper auth
        """
        # Simple password check (in production use proper auth)
        expected = "AOS_PROTECTED_2026"
        if password == expected:
            return True
        return False


# Test
def test_protected_memory():
    """Test protected memory system"""
    print("\n" + "=" * 70)
    print("  Testing Protected Memory v1.0")
    print("=" * 70)
    
    pm = ProtectedMemory()
    
    # Test 1: Check protection
    print("\n1. Checking protection status...")
    assert pm.is_protected("/root/.openclaw/workspace/SOUL.md")
    assert pm.is_immutable("/root/.openclaw/workspace/SOUL.md")
    print("  ✅ SOUL.md is protected and immutable")
    
    # Test 2: Write request (should fail)
    print("\n2. Testing write request to immutable file...")
    granted, msg = pm.request_write(
        "/root/.openclaw/workspace/SOUL.md",
        "Test modification",
        elevated=False
    )
    assert not granted
    assert "IMMUTABLE" in msg
    print(f"  ✅ Write correctly denied: {msg}")
    
    # Test 3: Integrity check
    print("\n3. Testing integrity verification...")
    intact = pm.verify_integrity("/root/.openclaw/workspace/SOUL.md")
    print(f"  SOUL.md integrity: {intact}")
    
    # Test 4: Status report
    print("\n4. Protection status report...")
    status = pm.get_protection_status()
    print(f"  Protected files: {len(status['protected_files'])}")
    print(f"  Integrity violations: {sum(1 for f, s in status['integrity_check'].items() if not s)}")
    
    print("\n✅ Protected Memory v1.0 tests passed!")
    return True


if __name__ == "__main__":
    test_protected_memory()
