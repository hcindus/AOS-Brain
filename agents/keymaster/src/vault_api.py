#!/usr/bin/env python3
"""
The Key Master - API Server v1.0.0
RESTful interface for vault operations
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))
from vault_core import get_vault, VaultError, UnauthorizedError, SecretNotFoundError

# Configuration
API_PORT = int(os.environ.get('KEYMASTER_PORT', 8472))
API_HOST = os.environ.get('KEYMASTER_HOST', '127.0.0.1')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('keymaster-api')

class VaultAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for vault API"""
    
    def log_message(self, format, *args):
        """Custom logging"""
        logger.info(f"{self.address_string()} - {format % args}")
    
    def _send_json(self, status: int, data: dict):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, default=str).encode())
        
    def _send_error(self, status: int, error: str, details: str = None):
        """Send error response"""
        data = {'error': error}
        if details:
            data['details'] = details
        self._send_json(status, data)
        
    def _get_body(self) -> dict:
        """Parse request body"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length:
            body = self.rfile.read(content_length).decode()
            return json.loads(body)
        return {}
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/status':
            self._handle_status()
        elif path == '/secrets':
            self._handle_list_secrets(parsed.query)
        elif path.startswith('/secrets/'):
            secret_id = path.split('/')[-1]
            self._handle_get_secret(secret_id)
        elif path == '/rotation-queue':
            self._handle_rotation_queue()
        elif path == '/audit':
            self._handle_audit_log(parsed.query)
        else:
            self._send_error(404, 'Not Found')
            
    def do_POST(self):
        """Handle POST requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        try:
            body = self._get_body()
        except json.JSONDecodeError:
            self._send_error(400, 'Invalid JSON')
            return
        
        if path == '/request':
            self._handle_request(body)
        elif path == '/store':
            self._handle_store(body)
        elif path == '/rotate':
            self._handle_rotate(body)
        elif path == '/revoke':
            self._handle_revoke(body)
        else:
            self._send_error(404, 'Not Found')
            
    def _handle_status(self):
        """GET /status - Vault health"""
        vault = get_vault()
        status = vault.vault_status()
        self._send_json(200, status)
        
    def _handle_list_secrets(self, query: str):
        """GET /secrets - List all secrets"""
        vault = get_vault()
        params = parse_qs(query)
        service = params.get('service', [None])[0]
        active_only = params.get('active', ['true'])[0].lower() == 'true'
        
        secrets = vault.list_secrets(service=service, active_only=active_only)
        self._send_json(200, {
            'count': len(secrets),
            'secrets': [s.to_dict() for s in secrets]
        })
        
    def _handle_get_secret(self, secret_id: str):
        """GET /secrets/{id} - Get secret metadata"""
        vault = get_vault()
        secret = vault.get_secret_metadata(secret_id)
        if secret:
            self._send_json(200, secret.to_dict())
        else:
            self._send_error(404, 'Secret not found')
            
    def _handle_request(self, body: dict):
        """POST /request - Retrieve a secret"""
        required = ['secret_id', 'requester', 'reason']
        if not all(k in body for k in required):
            self._send_error(400, 'Missing required fields', 
                           f"Required: {', '.join(required)}")
            return
            
        vault = get_vault()
        try:
            time_bound = body.get('time_bound_minutes', 60)
            secret_value = vault.retrieve_secret(
                body['secret_id'],
                body['requester'],
                body['reason'],
                time_bound
            )
            self._send_json(200, {
                'status': 'granted',
                'secret_id': body['secret_id'],
                'expires': (datetime.now() + timedelta(minutes=time_bound)).isoformat(),
                'value': secret_value  # In production, encrypt this response
            })
        except SecretNotFoundError as e:
            self._send_error(404, str(e))
        except UnauthorizedError as e:
            self._send_error(403, str(e))
        except Exception as e:
            logger.error(f"Error retrieving secret: {e}")
            self._send_error(500, 'Internal error')
            
    def _handle_store(self, body: dict):
        """POST /store - Store a new secret"""
        required = ['secret_id', 'value', 'service', 'secret_type']
        if not all(k in body for k in required):
            self._send_error(400, 'Missing required fields',
                           f"Required: {', '.join(required)}")
            return
            
        vault = get_vault()
        try:
            secret = vault.store_secret(
                body['secret_id'],
                body['value'],
                body['service'],
                body['secret_type'],
                classification=body.get('classification', 'standard'),
                rotation_days=body.get('rotation_days', 90),
                metadata=body.get('metadata', {})
            )
            self._send_json(201, {
                'status': 'stored',
                'secret': secret.to_dict()
            })
        except Exception as e:
            logger.error(f"Error storing secret: {e}")
            self._send_error(500, 'Internal error')
            
    def _handle_rotate(self, body: dict):
        """POST /rotate - Rotate a secret"""
        required = ['secret_id', 'new_value', 'rotated_by', 'reason']
        if not all(k in body for k in required):
            self._send_error(400, 'Missing required fields',
                           f"Required: {', '.join(required)}")
            return
            
        vault = get_vault()
        try:
            secret = vault.rotate_secret(
                body['secret_id'],
                body['new_value'],
                body['rotated_by'],
                body['reason']
            )
            self._send_json(200, {
                'status': 'rotated',
                'secret': secret.to_dict()
            })
        except SecretNotFoundError as e:
            self._send_error(404, str(e))
        except Exception as e:
            logger.error(f"Error rotating secret: {e}")
            self._send_error(500, 'Internal error')
            
    def _handle_revoke(self, body: dict):
        """POST /revoke - Revoke a secret"""
        required = ['secret_id', 'revoked_by', 'reason']
        if not all(k in body for k in required):
            self._send_error(400, 'Missing required fields',
                           f"Required: {', '.join(required)}")
            return
            
        vault = get_vault()
        try:
            vault.revoke_secret(body['secret_id'], body['revoked_by'], body['reason'])
            self._send_json(200, {
                'status': 'revoked',
                'secret_id': body['secret_id'],
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Error revoking secret: {e}")
            self._send_error(500, 'Internal error')
            
    def _handle_rotation_queue(self):
        """GET /rotation-queue - Get secrets due for rotation"""
        vault = get_vault()
        secrets = vault.get_rotation_queue()
        self._send_json(200, {
            'count': len(secrets),
            'secrets': [s.to_dict() for s in secrets]
        })
        
    def _handle_audit_log(self, query: str):
        """GET /audit - Get audit log"""
        params = parse_qs(query)
        limit = int(params.get('limit', ['100'])[0])
        
        vault = get_vault()
        logs = vault.get_audit_log(limit=limit)
        self._send_json(200, {
            'count': len(logs),
            'logs': logs
        })

class VaultAPIServer:
    """Key Master API Server"""
    
    def __init__(self, host: str = API_HOST, port: int = API_PORT):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
        
    def start(self):
        """Start the API server"""
        self.server = HTTPServer((self.host, self.port), VaultAPIHandler)
        logger.info(f"Key Master API server starting on {self.host}:{self.port}")
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        """Stop the API server"""
        if self.server:
            self.server.shutdown()
            logger.info("Key Master API server stopped")
            
    def wait(self):
        """Wait for server thread"""
        if self.thread:
            self.thread.join()

def main():
    """Run the API server"""
    server = VaultAPIServer()
    server.start()
    logger.info("Press Ctrl+C to stop")
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        server.stop()

if __name__ == '__main__':
    main()