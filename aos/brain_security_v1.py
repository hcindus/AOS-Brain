#!/usr/bin/env python3
"""
AOS BRAIN SECURITY v1.0 - Input Sanitization & Attack Prevention
Immune system hardening for the Complete Brain v4.5

Patches:
- Command allowlisting (prevents unknown commands)
- Rate limiting per connection (prevents flooding)
- Liver pre-filtering (closes ingest/add_to_layer bypasses)
- Audit logging (detects attack patterns)
- Content validation (sanitizes all inputs)
"""

import time
import json
import hashlib
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum, auto

# Import MNIAS for advanced input validation
try:
    from mnias_v1 import MNIASValidator
    MNIAS_AVAILABLE = True
except ImportError:
    MNIAS_AVAILABLE = False

# Import security monitor for continuous monitoring
try:
    from security_monitor_v1 import SecurityMonitor
    MONITOR_AVAILABLE = True
except ImportError:
    MONITOR_AVAILABLE = False


class SecurityLevel(Enum):
    SAFE = auto()      # Command allowed, no restrictions
    FILTERED = auto()  # Command allowed, content must pass Liver
    RESTRICTED = auto()  # Command allowed, rate limited
    BLOCKED = auto()   # Command denied


@dataclass
class ConnectionContext:
    """Tracks per-connection state for security decisions"""
    client_id: str
    connected_at: float
    command_history: List[Tuple[str, float]] = field(default_factory=list)
    violations: int = 0
    blocked_until: float = 0.0
    
    def is_blocked(self) -> bool:
        return time.time() < self.blocked_until
    
    def record_command(self, cmd: str):
        now = time.time()
        self.command_history.append((cmd, now))
        # Keep last 100 commands
        if len(self.command_history) > 100:
            self.command_history = self.command_history[-100:]
    
    def command_count_last_minute(self) -> int:
        cutoff = time.time() - 60
        return sum(1 for _, t in self.command_history if t > cutoff)
    
    def specific_command_count_last_minute(self, cmd: str) -> int:
        cutoff = time.time() - 60
        return sum(1 for c, t in self.command_history if c == cmd and t > cutoff)


class BrainSecurityLayer:
    """
    Security layer for Brain Socket Server
    
    Implements defense-in-depth:
    1. Command validation (is this command known?)
    2. Rate limiting (are we being flooded?)
    3. Content filtering (does this pass the Liver?)
    4. Pattern detection (is this an attack signature?)
    """
    
    # Commands that are safe to execute without restrictions
    SAFE_COMMANDS: Set[str] = {
        'status', 'ping', 'get_phase', 'get_heart',
        'thyroid', 'liver', 'kidneys', 'lungs',
        'router', 'save', 'load', 'tick', 'security'
    }
    
    # Commands that require content filtering (must pass Liver)
    FILTERED_COMMANDS: Set[str] = {
        'ingest', 'add_to_layer', 'perceive', 'filter',
        'breathe', 'seed_layers', 'cortex_write', 'speak', 'decide'
    }
    
    # Commands that are rate-limited (expensive operations)
    RESTRICTED_COMMANDS: Set[str] = {
        'stimulate', 'cortex_tick', 'cortex_register',
        'cortex_read', 'cortex_stats', 'hold_breath', 'release_breath'
    }
    
    # Commands that are completely blocked (too dangerous)
    BLOCKED_COMMANDS: Set[str] = {
        'eval', 'exec', '__import__', 'os.system', 'subprocess',
        'open', 'file', 'compile', 'execfile'
    }
    
    # All known commands (for validation)
    ALL_KNOWN_COMMANDS = SAFE_COMMANDS | FILTERED_COMMANDS | RESTRICTED_COMMANDS
    
    def __init__(self, 
                 max_commands_per_minute: int = 60,
                 max_restricted_per_minute: int = 10,
                 max_violations_before_block: int = 5,
                 block_duration_seconds: float = 300.0):
        
        self.max_commands = max_commands_per_minute
        self.max_restricted = max_restricted_per_minute
        self.max_violations = max_violations_before_block
        self.block_duration = block_duration_seconds
        
        # Initialize MNIAS for advanced input validation
        if MNIAS_AVAILABLE:
            self.mnias = MNIASValidator()
            print("[Security v1.0] MNIAS integration: ENABLED")
        else:
            self.mnias = None
            print("[Security v1.0] MNIAS integration: DISABLED (mnias_v1.py not found)")
        
        # Connection tracking
        self.connections: Dict[str, ConnectionContext] = {}
        self.connections_lock = threading.Lock()
        
        # Global rate limiting (system-wide flood protection)
        self.global_command_times: List[float] = []
        self.global_lock = threading.Lock()
        
        # Audit log
        self.audit_log: List[dict] = []
        self.audit_lock = threading.Lock()
        self.max_audit_entries = 10000
        
        print("[Security v1.0] Defense layer initialized")
        print(f"  Safe commands: {len(self.SAFE_COMMANDS)}")
        print(f"  Filtered commands: {len(self.FILTERED_COMMANDS)}")
        print(f"  Restricted commands: {len(self.RESTRICTED_COMMANDS)}")
        print(f"  Rate limit: {max_commands_per_minute}/min general, {max_restricted_per_minute}/min restricted")
    
    def validate_command(self, cmd: str, params: dict, client_id: str) -> Tuple[bool, SecurityLevel, Optional[str]]:
        """
        Validate a command before execution
        
        Returns: (is_allowed, security_level, reason_if_blocked)
        """
        now = time.time()
        
        # 1. Check if client is blocked
        with self.connections_lock:
            if client_id in self.connections:
                if self.connections[client_id].is_blocked():
                    return False, SecurityLevel.BLOCKED, f"Client blocked for {self.block_duration}s"
        
        # 2. Check for known blocked commands
        if cmd in self.BLOCKED_COMMANDS:
            self._log_violation(client_id, cmd, params, "BLOCKED_COMMAND")
            return False, SecurityLevel.BLOCKED, "Command is permanently blocked"
        
        # 3. Check for command injection patterns
        if self._detect_injection(cmd, params):
            self._log_violation(client_id, cmd, params, "INJECTION_DETECTED")
            return False, SecurityLevel.BLOCKED, "Potential command injection detected"
        
        # 4. Check if command is known
        if cmd not in self.ALL_KNOWN_COMMANDS:
            self._log_violation(client_id, cmd, params, "UNKNOWN_COMMAND")
            return False, SecurityLevel.BLOCKED, f"Unknown command: {cmd}"
        
        # 5. Rate limiting check
        if not self._check_rate_limits(client_id, cmd):
            self._log_violation(client_id, cmd, params, "RATE_LIMIT")
            return False, SecurityLevel.BLOCKED, "Rate limit exceeded"
        
        # 6. Determine security level
        if cmd in self.FILTERED_COMMANDS:
            return True, SecurityLevel.FILTERED, None
        elif cmd in self.RESTRICTED_COMMANDS:
            return True, SecurityLevel.RESTRICTED, None
        else:
            return True, SecurityLevel.SAFE, None
    
    def _detect_injection(self, cmd: str, params: dict) -> bool:
        """Detect potential injection attacks"""
        # Check command name for injection
        dangerous_patterns = [
            '__', 'import', 'eval', 'exec', 'compile',
            'os.', 'sys.', 'subprocess', 'open(', 'file(',
            '${', '`', '||', '&&', ';', '|', '>', '<'
        ]
        
        cmd_lower = cmd.lower()
        for pattern in dangerous_patterns:
            if pattern in cmd_lower:
                return True
        
        # Check parameters for injection
        def check_value(val):
            if isinstance(val, str):
                val_lower = val.lower()
                for pattern in dangerous_patterns:
                    if pattern in val_lower:
                        return True
                # Check for excessive length (DoS)
                if len(val) > 10000:
                    return True
            elif isinstance(val, dict):
                for v in val.values():
                    if check_value(v):
                        return True
            elif isinstance(val, list):
                for item in val:
                    if check_value(item):
                        return True
            return False
        
        return check_value(params)
    
    def _check_rate_limits(self, client_id: str, cmd: str) -> bool:
        """Check rate limits for this client and globally"""
        now = time.time()
        
        with self.connections_lock:
            if client_id not in self.connections:
                self.connections[client_id] = ConnectionContext(
                    client_id=client_id,
                    connected_at=now
                )
            
            ctx = self.connections[client_id]
            
            # Check general rate limit
            if ctx.command_count_last_minute() >= self.max_commands:
                return False
            
            # Check restricted command rate limit
            if cmd in self.RESTRICTED_COMMANDS:
                if ctx.specific_command_count_last_minute(cmd) >= self.max_restricted:
                    return False
        
        # Global flood protection
        with self.global_lock:
            cutoff = now - 60
            self.global_command_times = [t for t in self.global_command_times if t > cutoff]
            self.global_command_times.append(now)
            
            # If system-wide commands exceed 10x per-client limit, throttle
            if len(self.global_command_times) > self.max_commands * 10:
                return False
        
        return True
    
    def _log_violation(self, client_id: str, cmd: str, params: dict, violation_type: str):
        """Log a security violation"""
        with self.connections_lock:
            if client_id in self.connections:
                self.connections[client_id].violations += 1
                
                # Block client if too many violations
                if self.connections[client_id].violations >= self.max_violations:
                    self.connections[client_id].blocked_until = time.time() + self.block_duration
                    print(f"[SECURITY] Client {client_id} blocked for {self.block_duration}s (too many violations)")
        
        self._audit_log({
            'type': 'VIOLATION',
            'violation': violation_type,
            'client': client_id,
            'command': cmd,
            'params_hash': hashlib.sha256(json.dumps(params, sort_keys=True).encode()).hexdigest()[:16],
            'timestamp': time.time()
        })
    
    def record_command(self, client_id: str, cmd: str):
        """Record successful command execution"""
        with self.connections_lock:
            if client_id in self.connections:
                self.connections[client_id].record_command(cmd)
        
        self._audit_log({
            'type': 'COMMAND',
            'client': client_id,
            'command': cmd,
            'timestamp': time.time()
        })
    
    def _audit_log(self, entry: dict):
        """Add entry to audit log"""
        with self.audit_lock:
            self.audit_log.append(entry)
            if len(self.audit_log) > self.max_audit_entries:
                self.audit_log = self.audit_log[-self.max_audit_entries:]
    
    def get_client_id(self, addr) -> str:
        """Generate unique client ID from connection address"""
        # For Unix sockets, addr is empty, use timestamp + thread id
        import threading
        return hashlib.sha256(
            f"{time.time()}-{threading.current_thread().ident}".encode()
        ).hexdigest()[:16]
    
    def get_security_status(self) -> dict:
        """Get current security status"""
        with self.connections_lock:
            active_connections = len(self.connections)
            blocked_connections = sum(
                1 for c in self.connections.values() if c.is_blocked()
            )
            total_violations = sum(c.violations for c in self.connections.values())
        
        with self.audit_lock:
            recent_violations = sum(
                1 for e in self.audit_log[-100:]
                if e.get('type') == 'VIOLATION'
            )
        
        return {
            'active_connections': active_connections,
            'blocked_connections': blocked_connections,
            'total_violations': total_violations,
            'recent_violations': recent_violations,
            'commands_last_minute': len(self.global_command_times),
            'audit_entries': len(self.audit_log)
        }
    
    def filter_content(self, content: str, liver) -> Tuple[bool, str, dict]:
        """
        Filter content through the Liver
        
        Returns: (is_clean, filtered_content_or_reason, metadata)
        """
        from liver_v1 import BloodSample, LiverState
        
        sample = BloodSample(
            source='security_filter',
            content=content,
            timestamp=time.time(),
            flow_rate=1.0
        )
        
        state, result, meta = liver.process(sample)
        
        if state == LiverState.TOXIC:
            return False, "Content flagged as TOXIC by Liver", meta
        elif state == LiverState.PURIFY:
            return True, result if result else content, meta
        else:
            return True, content, meta
    
    def validate_with_mnias(self, content: str, source: str = "socket") -> Tuple[bool, str, float, str]:
        """
        Validate content with MNIAS (Multi-Layer Neural Input Sanitization)
        
        Returns: (is_safe, reason, risk_score, sanitized_text)
        """
        if not self.mnias:
            return True, "MNIAS not available", 0.0, content
        
        is_safe, detections, risk_score, sanitized = self.mnias.validate(content, source=source)
        
        if not is_safe:
            reasons = [f"{d.severity.name}:{d.pattern}" for d in detections]
            return False, f"MNIAS blocked: {', '.join(reasons[:3])}", risk_score, sanitized
        
        return True, "MNIAS validated", risk_score, sanitized


class SecureBrainSocketServer:
    """
    Security-hardened version of BrainSocketServer
    Wraps the original with input validation and rate limiting
    """
    
    def __init__(self, brain, socket_path='/tmp/aos_brain.sock'):
        self.brain = brain
        self.socket_path = socket_path
        self.security = BrainSecurityLayer()
        self.running = False
        self.server_thread = None
        
        if os.path.exists(socket_path):
            try:
                os.remove(socket_path)
            except:
                pass
    
    def start(self):
        """Start the secure socket server"""
        self.running = True
        self.server_thread = threading.Thread(target=self._serve, daemon=True)
        self.server_thread.start()
        print(f"[Secure Socket Server] Started on {self.socket_path}")
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if os.path.exists(self.socket_path):
            try:
                os.remove(self.socket_path)
            except:
                pass
    
    def _serve(self):
        """Serve requests with security filtering"""
        import socket
        
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.bind(self.socket_path)
            sock.listen(5)
            sock.settimeout(1.0)
            
            while self.running:
                try:
                    conn, addr = sock.accept()
                    client_id = self.security.get_client_id(addr)
                    self._handle_connection(conn, client_id)
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"[Secure Socket Server] Error: {e}")
        except Exception as e:
            print(f"[Secure Socket Server] Fatal error: {e}")
        finally:
            sock.close()
    
    def _handle_connection(self, conn, client_id: str):
        """Handle a single secure connection"""
        try:
            conn.settimeout(5.0)
            
            data = b''
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b'\n' in data:
                    break
            
            if not data:
                return
            
            request = json.loads(data.decode().strip())
            cmd = request.get('cmd')
            params = request.get('params', {})
            
            # SECURITY CHECK
            is_allowed, level, reason = self.security.validate_command(cmd, params, client_id)
            
            if not is_allowed:
                response = {
                    'error': 'SECURITY_VIOLATION',
                    'reason': reason,
                    'command': cmd
                }
                conn.sendall(json.dumps(response).encode())
                return
            
            # For FILTERED commands, run content through MNIAS first, then Liver
            if level == SecurityLevel.FILTERED:
                content_fields = self._extract_content_fields(params)
                for field, content in content_fields.items():
                    # Layer 1: MNIAS validation (Patricia's advanced detection)
                    is_mnias_safe, mnias_reason, risk_score, mnias_sanitized = self.security.validate_with_mnias(
                        content, source="socket"
                    )
                    if not is_mnias_safe:
                        response = {
                            'error': 'MNIAS_SECURITY_VIOLATION',
                            'reason': mnias_reason,
                            'field': field,
                            'risk_score': risk_score
                        }
                        conn.sendall(json.dumps(response).encode())
                        return
                    
                    # Layer 2: Liver filtering (ternary signal/noise)
                    is_clean, filtered, meta = self.security.filter_content(
                        mnias_sanitized, self.brain.liver
                    )
                    if not is_clean:
                        response = {
                            'error': 'CONTENT_REJECTED',
                            'reason': filtered,
                            'field': field,
                            'liver_metadata': meta
                        }
                        conn.sendall(json.dumps(response).encode())
                        return
                    
                    # Replace with fully sanitized content
                    params = self._update_content_field(params, field, filtered)
            
            # Execute the command
            response = self._execute_command(cmd, params)
            
            # Record successful execution
            self.security.record_command(client_id, cmd)
            
            conn.sendall(json.dumps(response).encode())
            
        except json.JSONDecodeError as e:
            response = {'error': 'INVALID_JSON', 'details': str(e)}
            conn.sendall(json.dumps(response).encode())
        except Exception as e:
            response = {'error': 'INTERNAL_ERROR', 'details': str(e)}
            try:
                conn.sendall(json.dumps(response).encode())
            except:
                pass
        finally:
            conn.close()
    
    def _extract_content_fields(self, params: dict) -> dict:
        """Extract fields that need content filtering"""
        content_fields = {}
        
        # Common content fields
        if 'content' in params:
            content_fields['content'] = params['content']
        if 'message' in params:
            content_fields['message'] = params['message']
        if 'observation' in params:
            content_fields['observation'] = params['observation']
        
        return content_fields
    
    def _update_content_field(self, params: dict, field: str, value: str) -> dict:
        """Update a content field in params"""
        params = params.copy()
        if field in params:
            params[field] = value
        return params
    
    def _execute_command(self, cmd: str, params: dict) -> dict:
        """Execute a brain command (same as original BrainSocketServer)"""
        # Import here to avoid circular dependency
        from brain_socket_commands import execute_command
        return execute_command(self.brain, cmd, params)


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("  🔒 BRAIN SECURITY v1.0 - Test Suite")
    print("=" * 70)
    
    security = BrainSecurityLayer(
        max_commands_per_minute=10,
        max_restricted_per_minute=3,
        block_duration_seconds=5.0
    )
    
    # Test command validation
    test_cases = [
        ('status', {}, 'should pass'),
        ('ping', {}, 'should pass'),
        ('stimulate', {'importance': 0.8}, 'should pass (restricted)'),
        ('ingest', {'content': 'test'}, 'should pass (filtered)'),
        ('eval', {'code': 'print(1)'}, 'should block'),
        ('__import__', {}, 'should block'),
        ('unknown_cmd', {}, 'should block'),
        ('stimulate', {'importance': 0.8}, 'should pass'),
        ('stimulate', {'importance': 0.8}, 'should pass'),
        ('stimulate', {'importance': 0.8}, 'should pass'),
        ('stimulate', {'importance': 0.8}, 'should block (rate limit)'),
    ]
    
    client_id = "test_client"
    
    print("\nTesting command validation...\n")
    for cmd, params, expected in test_cases:
        is_allowed, level, reason = security.validate_command(cmd, params, client_id)
        if is_allowed:
            security.record_command(client_id, cmd)
            status = "✅ ALLOWED"
        else:
            status = "❌ BLOCKED"
        print(f"  {status} {cmd:20s} | {expected}")
        if not is_allowed:
            print(f"      Reason: {reason}")
    
    print("\n" + "=" * 70)
    print("Security Status:")
    for k, v in security.get_security_status().items():
        print(f"  {k}: {v}")
    print("=" * 70)
