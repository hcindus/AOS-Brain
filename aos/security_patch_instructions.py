#!/usr/bin/env python3
"""
AOS BRAIN SECURITY PATCH v1.0
Apply these changes to complete_brain_v45.py to enable security hardening

Usage:
1. Backup your current complete_brain_v45.py
2. Apply this patch by modifying the imports and BrainSocketServer class
3. Restart the brain service
"""

# === PATCH INSTRUCTIONS ===

# 1. ADD THESE IMPORTS at the top of complete_brain_v45.py (after existing imports):
"""
from brain_security_v1 import SecureBrainSocketServer, BrainSecurityLayer
"""

# 2. REPLACE the BrainSocketServer class entirely with this secured version:
"""
class BrainSocketServer:
    \"\"\"Security-hardened Unix socket server for diagnostic interface\"\"\"
    
    def __init__(self, brain, socket_path='/tmp/aos_brain.sock'):
        self.brain = brain
        self.socket_path = socket_path
        self.security = BrainSecurityLayer(
            max_commands_per_minute=60,
            max_restricted_per_minute=10,
            max_violations_before_block=5,
            block_duration_seconds=300.0
        )
        self.running = False
        self.server_thread = None
        
        if os.path.exists(socket_path):
            try:
                os.remove(socket_path)
            except:
                pass
    
    def start(self):
        \"\"\"Start the secure socket server in a thread\"\"\"
        self.running = True
        self.server_thread = threading.Thread(target=self._serve, daemon=True)
        self.server_thread.start()
        print(f"[Secure Socket Server] Started on {self.socket_path}")
    
    def stop(self):
        \"\"\"Stop the socket server\"\"\"
        self.running = False
        if os.path.exists(self.socket_path):
            try:
                os.remove(self.socket_path)
            except:
                pass
    
    def _serve(self):
        \"\"\"Serve socket requests with security filtering\"\"\"
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
        \"\"\"Handle a single secure connection\"\"\"
        try:
            conn.settimeout(5.0)
            
            data = b''
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b'\\n' in data:
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
            
            # For FILTERED commands, run content through Liver
            if level.name == 'FILTERED':
                from liver_v1 import BloodSample
                content_fields = self._extract_content_fields(params)
                for field, content in content_fields.items():
                    is_clean, filtered, meta = self._filter_content(content)
                    if not is_clean:
                        response = {
                            'error': 'CONTENT_REJECTED',
                            'reason': filtered,
                            'field': field,
                            'liver_metadata': meta
                        }
                        conn.sendall(json.dumps(response).encode())
                        return
                    # Replace with filtered content
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
        \"\"\"Extract fields that need content filtering\"\"\"
        content_fields = {}
        if 'content' in params:
            content_fields['content'] = params['content']
        if 'message' in params:
            content_fields['message'] = params['message']
        if 'observation' in params:
            content_fields['observation'] = params['observation']
        return content_fields
    
    def _update_content_field(self, params: dict, field: str, value: str) -> dict:
        \"\"\"Update a content field in params\"\"\"
        params = params.copy()
        if field in params:
            params[field] = value
        return params
    
    def _filter_content(self, content: str) -> tuple:
        \"\"\"Filter content through Liver\"\"\"
        from liver_v1 import BloodSample
        sample = BloodSample(
            source='security_filter',
            content=content,
            timestamp=time.time(),
            flow_rate=1.0
        )
        state, result, meta = self.brain.liver.process(sample)
        
        if state.name == 'TOXIC':
            return False, "Content flagged as TOXIC by Liver", meta
        elif state.name == 'PURIFY':
            return True, result if result else content, meta
        else:
            return True, content, meta
    
    def _execute_command(self, cmd: str, params: dict) -> dict:
        \"\"\"Execute a brain command\"\"\"
        from brain_socket_commands import execute_command
        return execute_command(self.brain, cmd, params)
"""

# 3. ADD SECURITY STATUS to get_status() method in CompleteBrainV44 class:
"""
def get_status(self):
    \"\"\"Get complete brain status with security info\"\"\"
    status = {
        "version": "4.5",
        "tick": self.tick_count,
        "phase": self.current_phase,
        "paused": self.paused,
        "heart": self.heart.get_metrics() if hasattr(self, 'heart') else None,
        "stomach": self.stomach.get_status() if hasattr(self, 'stomach') else None,
        "thyroid": self.thyroid.get_status() if self.thyroid else None,
        "liver": self.liver.get_status() if self.liver else None,
        "kidneys": self.kidneys.get_status() if self.kidneys else None,
        "lungs": self.lungs.get_status() if self.lungs else None,
        "security": self.socket_server.security.get_security_status() if hasattr(self.socket_server, 'security') else None
    }
    return status
"""

# === DEPLOYMENT STEPS ===

"""
1. Copy the new files:
   cp brain_security_v1.py /root/.aos/aos/
   cp brain_socket_commands.py /root/.aos/aos/

2. Backup the current brain:
   cp /root/.aos/aos/complete_brain_v45.py /root/.aos/aos/complete_brain_v45.py.backup

3. Apply the patch above to complete_brain_v45.py

4. Test the security layer:
   python3 /root/.aos/aos/brain_security_v1.py

5. Restart the brain service:
   sudo systemctl restart aos-brain-v4

6. Verify security is active:
   echo '{"cmd":"ping"}' | nc -U /tmp/aos_brain.sock
   echo '{"cmd":"eval"}' | nc -U /tmp/aos_brain.sock  # Should be blocked
"""

print(__doc__)
