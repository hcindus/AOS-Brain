#!/usr/bin/env python3
"""
PHONE-BASED LOGIN SYSTEM
Business phone number authentication API
Uses scraped YP.com data for verification
"""

import json
import re
import hashlib
import hmac
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List
import sqlite3

class PhoneLoginSystem:
    """Business phone number authentication system."""
    
    def __init__(self, db_path: str = "/root/.openclaw/workspace/data/phone_auth.db"):
        self.db_path = db_path
        self.business_db_path = Path("/root/.openclaw/workspace/data/yp_businesses/business_database.json")
        self.api_secret = self._load_or_generate_secret()
        self._init_database()
    
    def _load_or_generate_secret(self) -> str:
        """Load or generate API secret."""
        secret_file = Path("/root/.aos/vault/phone_auth_secret.key")
        if secret_file.exists():
            return secret_file.read_text().strip()
        
        # Generate new secret
        import secrets
        secret = secrets.token_hex(32)
        secret_file.parent.mkdir(parents=True, exist_ok=True)
        secret_file.write_text(secret)
        return secret
    
    def _init_database(self):
        """Initialize SQLite database."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE NOT NULL,
                business_name TEXT NOT NULL,
                normalized_phone TEXT UNIQUE NOT NULL,
                verified BOOLEAN DEFAULT FALSE,
                verification_code TEXT,
                code_expires TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                login_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Login attempts log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                ip_address TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def normalize_phone(self, phone: str) -> str:
        """Normalize phone number to 10 digits."""
        digits = re.sub(r'\D', '', phone)
        # Remove leading 1 if present
        if len(digits) == 11 and digits[0] == '1':
            digits = digits[1:]
        return digits
    
    def format_phone(self, phone: str) -> str:
        """Format phone number as (XXX) XXX-XXXX."""
        normalized = self.normalize_phone(phone)
        if len(normalized) == 10:
            return f"({normalized[:3]}) {normalized[3:6]}-{normalized[6:]}"
        return phone
    
    def load_business_database(self) -> List[Dict]:
        """Load business database from JSON."""
        if not self.business_db_path.exists():
            return []
        
        with open(self.business_db_path) as f:
            return json.load(f)
    
    def verify_business_exists(self, phone: str, business_name: str) -> Optional[Dict]:
        """Verify business exists in database."""
        businesses = self.load_business_database()
        normalized = self.normalize_phone(phone)
        
        for business in businesses:
            if business.get('phone') == normalized:
                # Fuzzy match business name
                db_name = business.get('business_name', '').lower()
                input_name = business_name.lower()
                
                if input_name in db_name or db_name in input_name:
                    return business
        
        return None
    
    def register_business(self, phone: str, business_name: str) -> Dict:
        """Register a new business for phone login."""
        normalized = self.normalize_phone(phone)
        formatted = self.format_phone(phone)
        
        # Check if already registered
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, verified FROM users WHERE normalized_phone = ?",
            (normalized,)
        )
        existing = cursor.fetchone()
        
        if existing:
            conn.close()
            return {
                "success": False,
                "error": "Business already registered",
                "user_id": existing[0],
                "verified": existing[1]
            }
        
        # Check if exists in business database
        business_data = self.verify_business_exists(phone, business_name)
        
        # Generate verification code
        import secrets
        code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        
        # Insert user
        cursor.execute('''
            INSERT INTO users (phone, business_name, normalized_phone, verification_code, code_expires)
            VALUES (?, ?, ?, ?, datetime('now', '+10 minutes'))
        ''', (formatted, business_name, normalized, code))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # In production, send SMS here
        # For now, return code for testing
        return {
            "success": True,
            "user_id": user_id,
            "message": "Registration initiated. Verify with code.",
            "verification_code": code,  # Remove in production!
            "business_verified": business_data is not None
        }
    
    def verify_code(self, phone: str, code: str) -> Dict:
        """Verify registration code."""
        normalized = self.normalize_phone(phone)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, verification_code, code_expires, verified
            FROM users
            WHERE normalized_phone = ?
        ''', (normalized,))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return {"success": False, "error": "User not found"}
        
        user_id, stored_code, expires, verified = user
        
        if verified:
            conn.close()
            return {"success": False, "error": "Already verified", "user_id": user_id}
        
        if datetime.now() > datetime.fromisoformat(expires):
            conn.close()
            return {"success": False, "error": "Code expired"}
        
        if code != stored_code:
            conn.close()
            return {"success": False, "error": "Invalid code"}
        
        # Mark as verified
        cursor.execute('''
            UPDATE users SET verified = TRUE, verification_code = NULL
            WHERE id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Phone verified successfully",
            "user_id": user_id
        }
    
    def login(self, phone: str, business_name: str, ip_address: str = None) -> Dict:
        """Login with phone and business name."""
        normalized = self.normalize_phone(phone)
        formatted = self.format_phone(phone)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check for lockout
        cursor.execute('''
            SELECT id, locked_until, verified FROM users
            WHERE normalized_phone = ?
        ''', (normalized,))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return {
                "success": False,
                "error": "Business not registered",
                "action": "Please register first"
            }
        
        user_id, locked_until, verified = user
        
        if not verified:
            conn.close()
            return {
                "success": False,
                "error": "Phone not verified",
                "action": "Complete verification"
            }
        
        if locked_until and datetime.now() < datetime.fromisoformat(locked_until):
            conn.close()
            return {
                "success": False,
                "error": "Account temporarily locked",
                "retry_after": locked_until
            }
        
        # Verify business name matches
        cursor.execute('SELECT business_name FROM users WHERE id = ?', (user_id,))
        stored_name = cursor.fetchone()[0]
        
        if business_name.lower() not in stored_name.lower():
            # Log failed attempt
            cursor.execute('''
                INSERT INTO login_attempts (phone, success, ip_address, error_message)
                VALUES (?, ?, ?, ?)
            ''', (formatted, False, ip_address, "Business name mismatch"))
            
            # Increment attempts
            cursor.execute('''
                UPDATE users SET login_attempts = login_attempts + 1
                WHERE id = ?
            ''', (user_id,))
            
            # Lock after 5 failed attempts
            cursor.execute('SELECT login_attempts FROM users WHERE id = ?', (user_id,))
            attempts = cursor.fetchone()[0]
            
            if attempts >= 5:
                lock_until = datetime.now() + timedelta(minutes=30)
                cursor.execute('''
                    UPDATE users SET locked_until = ?
                    WHERE id = ?
                ''', (lock_until.isoformat(), user_id))
            
            conn.commit()
            conn.close()
            
            return {
                "success": False,
                "error": "Business name does not match",
                "attempts_remaining": 5 - attempts
            }
        
        # Success - create session
        cursor.execute('''
            UPDATE users SET
                login_attempts = 0,
                locked_until = NULL,
                last_login = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (user_id,))
        
        # Generate session token
        session_token = hmac.new(
            self.api_secret.encode(),
            f"{user_id}:{time.time()}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        expires = datetime.now() + timedelta(days=7)
        
        cursor.execute('''
            INSERT INTO sessions (user_id, token, expires_at, ip_address)
            VALUES (?, ?, ?, ?)
        ''', (user_id, session_token, expires.isoformat(), ip_address))
        
        # Log success
        cursor.execute('''
            INSERT INTO login_attempts (phone, success, ip_address)
            VALUES (?, ?, ?)
        ''', (formatted, True, ip_address))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Login successful",
            "user_id": user_id,
            "session_token": session_token,
            "expires_at": expires.isoformat(),
            "business_name": stored_name,
            "phone": formatted
        }
    
    def verify_session(self, token: str) -> Optional[Dict]:
        """Verify session token."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.phone, u.business_name, s.expires_at
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ? AND s.expires_at > datetime('now')
        ''', (token,))
        
        session = cursor.fetchone()
        conn.close()
        
        if not session:
            return None
        
        return {
            "user_id": session[0],
            "phone": session[1],
            "business_name": session[2],
            "expires_at": session[3]
        }
    
    def logout(self, token: str) -> bool:
        """Logout and invalidate session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sessions WHERE token = ?', (token,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def get_stats(self) -> Dict:
        """Get system statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        stats['total_users'] = cursor.fetchone()[0]
        
        # Verified users
        cursor.execute('SELECT COUNT(*) FROM users WHERE verified = TRUE')
        stats['verified_users'] = cursor.fetchone()[0]
        
        # Active sessions
        cursor.execute('SELECT COUNT(*) FROM sessions WHERE expires_at > datetime("now")')
        stats['active_sessions'] = cursor.fetchone()[0]
        
        # Login attempts today
        cursor.execute('''
            SELECT COUNT(*), SUM(CASE WHEN success THEN 1 ELSE 0 END)
            FROM login_attempts
            WHERE timestamp > datetime('now', '-1 day')
        ''')
        attempts = cursor.fetchone()
        stats['login_attempts_24h'] = attempts[0]
        stats['successful_logins_24h'] = attempts[1]
        
        conn.close()
        
        return stats


# API Endpoints (for web framework integration)
class PhoneAuthAPI:
    """Flask/FastAPI compatible API endpoints."""
    
    def __init__(self):
        self.auth = PhoneLoginSystem()
    
    def register(self, phone: str, business_name: str) -> Dict:
        return self.auth.register_business(phone, business_name)
    
    def verify(self, phone: str, code: str) -> Dict:
        return self.auth.verify_code(phone, code)
    
    def login(self, phone: str, business_name: str, ip: str = None) -> Dict:
        return self.auth.login(phone, business_name, ip)
    
    def check_session(self, token: str) -> Optional[Dict]:
        return self.auth.verify_session(token)
    
    def stats(self) -> Dict:
        return self.auth.get_stats()


if __name__ == "__main__":
    # Demo/test
    print("Phone Login System Ready")
    print("=" * 70)
    
    auth = PhoneAuthAPI()
    
    # Show stats
    print("\nSystem Stats:")
    for key, value in auth.stats().items():
        print(f"  {key}: {value}")
    
    print("\nAPI Ready for integration with website")
