#!/usr/bin/env python3
"""
AGI Auth System Bridge
Integrates with existing AGI Company authentication infrastructure
"""

import os
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class AuthContext:
    user_id: str
    email: str
    permissions: list
    session_token: str
    expires_at: datetime
    mfa_verified: bool = False
    
class AGIAuthBridge:
    """
    Bridge to AGI Company authentication system
    - Validates sessions from existing auth infrastructure
    - Generates service-specific tokens
    - Handles MFA requirements
    - Manages consent tracking
    """
    
    def __init__(self, auth_endpoint: str = None, secret_key: str = None):
        self.auth_endpoint = auth_endpoint or os.getenv('AGI_AUTH_ENDPOINT')
        self.secret_key = secret_key or os.getenv('AGI_AUTH_SECRET')
        self.service_name = 'identity-platform'
        
    def validate_session(self, agi_token: str) -> Optional[AuthContext]:
        """
        Validate token from AGI auth system
        Returns AuthContext if valid, None if invalid/expired
        """
        try:
            # Decode and validate JWT from AGI auth
            payload = jwt.decode(
                agi_token, 
                self.secret_key, 
                algorithms=['HS256'],
                audience=self.service_name
            )
            
            return AuthContext(
                user_id=payload['sub'],
                email=payload['email'],
                permissions=payload.get('permissions', []),
                session_token=agi_token,
                expires_at=datetime.fromtimestamp(payload['exp']),
                mfa_verified=payload.get('mfa_verified', False)
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def generate_service_token(self, auth_context: AuthContext, 
                              consent_scopes: list) -> str:
        """
        Generate service-specific JWT for identity platform
        Includes consent scopes for data access
        """
        payload = {
            'sub': auth_context.user_id,
            'email': auth_context.email,
            'service': self.service_name,
            'consent_scopes': consent_scopes,
            'permissions': auth_context.permissions,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=1),
            'jti': secrets.token_hex(16)  # Unique token ID for revocation
        }
        
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def check_permission(self, auth_context: AuthContext, 
                         required_permission: str) -> bool:
        """
        Check if user has required permission
        """
        return required_permission in auth_context.permissions
    
    def require_mfa(self, auth_context: AuthContext) -> bool:
        """
        Check if MFA is verified for sensitive operations
        """
        return auth_context.mfa_verified
    
    def create_consent_challenge(self, user_id: str, 
                                 consent_type: str) -> Dict[str, Any]:
        """
        Create cryptographic challenge for consent verification
        """
        challenge = secrets.token_urlsafe(32)
        challenge_hash = hashlib.sha256(challenge.encode()).hexdigest()
        
        return {
            'challenge': challenge,
            'challenge_hash': challenge_hash,
            'user_id': user_id,
            'consent_type': consent_type,
            'expires_at': datetime.utcnow() + timedelta(minutes=5)
        }
    
    def verify_consent(self, challenge: str, 
                      signed_response: str) -> bool:
        """
        Verify user consent via cryptographic signature
        """
        # Implementation depends on AGI auth signing mechanism
        # Placeholder for signature verification
        expected_hash = hashlib.sha256(challenge.encode()).hexdigest()
        return secrets.compare_digest(
            hashlib.sha256(signed_response.encode()).hexdigest(),
            expected_hash
        )

class ConsentManager:
    """
    Manages user consent for data collection and analytics contribution
    """
    
    CONSENT_TYPES = [
        'data_collection',           # Basic footprint collection
        'analytics_contribution',   # Anonymized aggregate contribution
        'broker_optout',           # Automated opt-out from data brokers
        'third_party_sharing',     # Sharing with partner services
        'marketing_communications' # Contact for product updates
    ]
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_consent_status(self, user_id: str) -> Dict[str, Any]:
        """
        Get current consent status for all types
        """
        # Query from database
        return {
            'user_id': user_id,
            'consents': {},
            'last_updated': datetime.utcnow()
        }
    
    def update_consent(self, user_id: str, consent_type: str, 
                      granted: bool, metadata: dict = None) -> bool:
        """
        Update consent status with audit trail
        """
        # Validate consent_type
        if consent_type not in self.CONSENT_TYPES:
            raise ValueError(f"Invalid consent type: {consent_type}")
        
        # Log to audit trail
        self._log_consent_change(user_id, consent_type, granted, metadata)
        
        # Update database
        return True
    
    def _log_consent_change(self, user_id: str, consent_type: str,
                           granted: bool, metadata: dict):
        """
        Log consent change for compliance
        """
        audit_record = {
            'user_id': user_id,
            'action': 'consent_update',
            'consent_type': consent_type,
            'granted': granted,
            'timestamp': datetime.utcnow(),
            'ip_address': metadata.get('ip_address'),
            'user_agent': metadata.get('user_agent'),
            'legal_basis': 'consent' if granted else 'withdrawal'
        }
        # Write to audit_log table
        
    def can_contribute_analytics(self, user_id: str) -> bool:
        """
        Check if user has consented to analytics contribution
        """
        consent = self.get_consent_status(user_id)
        return consent.get('consents', {}).get('analytics_contribution', False)

# FastAPI dependency for protected routes
from fastapi import HTTPException, Header, Depends

async def get_current_user(
    authorization: str = Header(...),
    auth_bridge: AGIAuthBridge = Depends()
) -> AuthContext:
    """
    FastAPI dependency to get authenticated user
    """
    if not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization[7:]  # Remove 'Bearer ' prefix
    auth_context = auth_bridge.validate_session(token)
    
    if not auth_context:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return auth_context

async def require_mfa(
    auth_context: AuthContext = Depends(get_current_user)
) -> AuthContext:
    """
    Require MFA for sensitive operations
    """
    if not auth_context.mfa_verified:
        raise HTTPException(status_code=403, detail="MFA required")
    return auth_context
