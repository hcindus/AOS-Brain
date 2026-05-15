#!/usr/bin/env python3
"""
The Key Master - Vault Core v1.0.0
Keeper of Thresholds - Secrets Management System
"""

import os
import sys
import json
import hashlib
import base64
import logging
import sqlite3
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from pathlib import Path
from cryptography.fernet import Fernet
import secrets

# Configuration
VAULT_DIR = Path("/root/.openclaw/workspace/agents/keymaster/storage/vault")
LOGS_DIR = Path("/root/.openclaw/workspace/agents/keymaster/storage/logs")
BACKUP_DIR = Path("/root/.openclaw/workspace/agents/keymaster/storage/backups")
DB_PATH = VAULT_DIR / "vault.db"
MASTER_KEY_FILE = VAULT_DIR / ".master_key"

class VaultError(Exception):
    """Vault operation error"""
    pass

class UnauthorizedError(VaultError):
    """Access denied"""
    pass

class SecretNotFoundError(VaultError):
    """Secret does not exist"""
    pass

@dataclass
class Secret:
    """A stored secret"""
    secret_id: str
    service: str
    secret_type: str  # 'api_key', 'token', 'certificate', 'password', 'encryption_key'
    encrypted_value: bytes
    classification: str  # 'critical', 'high', 'standard', 'legacy'
    created_at: datetime
    expires_at: Optional[datetime]
    last_rotated: datetime
    rotation_interval_days: int
    metadata: Dict[str, Any]
    active: bool = True
    
    def to_dict(self) -> dict:
        return {
            'secret_id': self.secret_id,
            'service': self.service,
            'secret_type': self.secret_type,
            'classification': self.classification,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'last_rotated': self.last_rotated.isoformat(),
            'rotation_interval_days': self.rotation_interval_days,
            'metadata': self.metadata,
            'active': self.active
        }

class VaultCore:
    """Core vault operations - The threshold itself"""
    
    def __init__(self):
        self._ensure_directories()
        self._init_database()
        self._master_key = self._load_or_create_master_key()
        self._fernet = Fernet(self._master_key)
        self._setup_logging()
        
    def _ensure_directories(self):
        """Ensure vault directories exist"""
        VAULT_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        os.chmod(VAULT_DIR, 0o700)
        
    def _init_database(self):
        """Initialize SQLite database for vault metadata"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS secrets (
                secret_id TEXT PRIMARY KEY,
                service TEXT NOT NULL,
                secret_type TEXT NOT NULL,
                encrypted_value BLOB NOT NULL,
                classification TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                last_rotated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rotation_interval_days INTEGER DEFAULT 90,
                metadata TEXT,
                active BOOLEAN DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                secret_id TEXT,
                reason TEXT,
                success BOOLEAN,
                details TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_grants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                service TEXT NOT NULL,
                secret_id TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                audit_id TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def _load_or_create_master_key(self) -> bytes:
        """Load or create the master encryption key"""
        if MASTER_KEY_FILE.exists():
            with open(MASTER_KEY_FILE, 'rb') as f:
                return f.read()
        else:
            # Generate new master key
            key = Fernet.generate_key()
            with open(MASTER_KEY_FILE, 'wb') as f:
                f.write(key)
            os.chmod(MASTER_KEY_FILE, 0o400)
            return key
            
    def _setup_logging(self):
        """Setup vault audit logging"""
        log_file = LOGS_DIR / f"vault_{datetime.now().strftime('%Y%m')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('keymaster')
        
    def _log_audit(self, actor: str, action: str, secret_id: str = None, 
                   reason: str = None, success: bool = True, details: dict = None):
        """Log vault access to audit trail"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO audit_log (actor, action, secret_id, reason, success, details)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (actor, action, secret_id, reason, success, json.dumps(details) if details else None))
        conn.commit()
        conn.close()
        
        self.logger.info(f"[AUDIT] {actor} {action} {secret_id or ''} - {reason or ''}")
        
    def store_secret(self, secret_id: str, value: str, service: str, 
                     secret_type: str, classification: str = 'standard',
                     rotation_days: int = 90, metadata: dict = None) -> Secret:
        """Store a new secret in the vault"""
        encrypted = self._fernet.encrypt(value.encode())
        
        now = datetime.now()
        expires = now + timedelta(days=rotation_days) if rotation_days else None
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO secrets 
            (secret_id, service, secret_type, encrypted_value, classification,
             expires_at, rotation_interval_days, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (secret_id, service, secret_type, encrypted, classification,
              expires, rotation_days, json.dumps(metadata) if metadata else '{}'))
        conn.commit()
        conn.close()
        
        self._log_audit('KeyMaster', 'STORE', secret_id, 
                       f"New {classification} secret for {service}")
        
        return Secret(
            secret_id=secret_id,
            service=service,
            secret_type=secret_type,
            encrypted_value=encrypted,
            classification=classification,
            created_at=now,
            expires_at=expires,
            last_rotated=now,
            rotation_interval_days=rotation_days,
            metadata=metadata or {}
        )
        
    def retrieve_secret(self, secret_id: str, requester: str, reason: str,
                        time_bound_minutes: int = 60) -> Optional[str]:
        """Retrieve a secret (with audit logging)"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT encrypted_value, active FROM secrets WHERE secret_id = ?', (secret_id,))
        row = cursor.fetchone()
        
        if not row:
            self._log_audit(requester, 'RETRIEVE_DENIED', secret_id, 
                           f"Secret not found: {reason}", success=False)
            conn.close()
            raise SecretNotFoundError(f"Secret '{secret_id}' not found in vault")
            
        encrypted_value, active = row
        
        if not active:
            self._log_audit(requester, 'RETRIEVE_DENIED', secret_id,
                           f"Secret revoked: {reason}", success=False)
            conn.close()
            raise UnauthorizedError(f"Secret '{secret_id}' has been revoked")
        
        # Decrypt and log access
        decrypted = self._fernet.decrypt(encrypted_value).decode()
        audit_id = f"req_{datetime.now().strftime('%Y%m%d%H%M%S')}_{requester.lower()}"
        
        expires_at = datetime.now() + timedelta(minutes=time_bound_minutes)
        cursor.execute('''
            INSERT INTO access_grants (service, secret_id, expires_at, audit_id)
            VALUES (?, ?, ?, ?)
        ''', (requester, secret_id, expires_at, audit_id))
        conn.commit()
        conn.close()
        
        self._log_audit(requester, 'RETRIEVE', secret_id, reason, 
                       details={'audit_id': audit_id, 'expires': expires_at.isoformat()})
        
        return decrypted
        
    def rotate_secret(self, secret_id: str, new_value: str, rotated_by: str,
                      reason: str) -> Secret:
        """Rotate a secret to a new value"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM secrets WHERE secret_id = ?', (secret_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            raise SecretNotFoundError(f"Secret '{secret_id}' not found")
        
        # Encrypt new value
        encrypted = self._fernet.encrypt(new_value.encode())
        now = datetime.now()
        rotation_days = row[8]  # rotation_interval_days
        expires = now + timedelta(days=rotation_days) if rotation_days else None
        
        cursor.execute('''
            UPDATE secrets SET 
            encrypted_value = ?,
            last_rotated = ?,
            expires_at = ?
            WHERE secret_id = ?
        ''', (encrypted, now, expires, secret_id))
        conn.commit()
        conn.close()
        
        self._log_audit(rotated_by, 'ROTATE', secret_id, reason,
                       details={'old_expires': row[6], 'new_expires': expires.isoformat() if expires else None})
        
        return self.get_secret_metadata(secret_id)
        
    def revoke_secret(self, secret_id: str, revoked_by: str, reason: str):
        """Revoke a secret immediately"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE secrets SET active = 0 WHERE secret_id = ?', (secret_id,))
        conn.commit()
        conn.close()
        
        self._log_audit(revoked_by, 'REVOKE', secret_id, reason)
        
    def get_secret_metadata(self, secret_id: str) -> Optional[Secret]:
        """Get metadata for a secret (not the value)"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT secret_id, service, secret_type, classification,
                   created_at, expires_at, last_rotated, rotation_interval_days,
                   metadata, active
            FROM secrets WHERE secret_id = ?
        ''', (secret_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
            
        return Secret(
            secret_id=row[0],
            service=row[1],
            secret_type=row[2],
            encrypted_value=b'',  # Don't expose encrypted value
            classification=row[3],
            created_at=datetime.fromisoformat(row[4]),
            expires_at=datetime.fromisoformat(row[5]) if row[5] else None,
            last_rotated=datetime.fromisoformat(row[6]),
            rotation_interval_days=row[7],
            metadata=json.loads(row[8]) if row[8] else {},
            active=bool(row[9])
        )
        
    def list_secrets(self, service: str = None, active_only: bool = True) -> List[Secret]:
        """List all secrets (metadata only)"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        query = '''
            SELECT secret_id, service, secret_type, classification,
                   created_at, expires_at, last_rotated, rotation_interval_days,
                   metadata, active
            FROM secrets WHERE 1=1
        '''
        params = []
        
        if service:
            query += ' AND service = ?'
            params.append(service)
        if active_only:
            query += ' AND active = 1'
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Secret(
                secret_id=row[0],
                service=row[1],
                secret_type=row[2],
                encrypted_value=b'',
                classification=row[3],
                created_at=datetime.fromisoformat(row[4]),
                expires_at=datetime.fromisoformat(row[5]) if row[5] else None,
                last_rotated=datetime.fromisoformat(row[6]),
                rotation_interval_days=row[7],
                metadata=json.loads(row[8]) if row[8] else {},
                active=bool(row[9])
            )
            for row in rows
        ]
        
    def get_rotation_queue(self) -> List[Secret]:
        """Get secrets due for rotation"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT secret_id, service, secret_type, classification,
                   created_at, expires_at, last_rotated, rotation_interval_days,
                   metadata, active
            FROM secrets 
            WHERE active = 1 AND (
                expires_at IS NULL OR expires_at <= datetime('now', '+7 days')
            )
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Secret(
                secret_id=row[0],
                service=row[1],
                secret_type=row[2],
                encrypted_value=b'',
                classification=row[3],
                created_at=datetime.fromisoformat(row[4]),
                expires_at=datetime.fromisoformat(row[5]) if row[5] else None,
                last_rotated=datetime.fromisoformat(row[6]),
                rotation_interval_days=row[7],
                metadata=json.loads(row[8]) if row[8] else {},
                active=bool(row[9])
            )
            for row in rows
        ]
        
    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        """Get recent audit log entries"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, actor, action, secret_id, reason, success, details
            FROM audit_log ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'timestamp': row[0],
                'actor': row[1],
                'action': row[2],
                'secret_id': row[3],
                'reason': row[4],
                'success': bool(row[5]),
                'details': json.loads(row[6]) if row[6] else None
            }
            for row in rows
        ]
        
    def vault_status(self) -> Dict:
        """Get vault health status"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM secrets WHERE active = 1')
        active_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM secrets WHERE active = 0')
        revoked_count = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM secrets 
            WHERE active = 1 AND expires_at <= datetime('now', '+7 days')
        ''')
        due_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM audit_log WHERE date(timestamp) = date("now")')
        today_access = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'status': 'healthy',
            'active_secrets': active_count,
            'revoked_secrets': revoked_count,
            'rotations_due': due_count,
            'access_today': today_access,
            'vault_path': str(VAULT_DIR),
            'timestamp': datetime.now().isoformat()
        }

# Singleton instance
_vault = None

def get_vault() -> VaultCore:
    """Get or create vault instance"""
    global _vault
    if _vault is None:
        _vault = VaultCore()
    return _vault

if __name__ == '__main__':
    # Test the vault
    vault = get_vault()
    print(f"Vault initialized at {VAULT_DIR}")
    print(json.dumps(vault.vault_status(), indent=2))