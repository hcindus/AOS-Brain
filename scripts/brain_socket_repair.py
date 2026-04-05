#!/usr/bin/env python3
"""
🔧 Brain Socket Repair Tool
Attempts 5 fixes before restart
"""

import socket
import os
import sys
import time
import subprocess
from datetime import datetime

BRAIN_SOCK = "/tmp/aos_brain.sock"
REPAIR_LOG = []

def log(msg):
    entry = f"[{datetime.utcnow().strftime('%H:%M:%S')}] {msg}"
    REPAIR_LOG.append(entry)
    print(entry)

def attempt_fix(num):
    log(f"\n{'='*60}")
    log(f"🔧 ATTEMPT {num}/5")
    log(f"{'='*60}")
    
    # Check if socket exists
    if os.path.exists(BRAIN_SOCK):
        log(f"Socket file exists at {BRAIN_SOCK}")
        try:
            # Try to connect
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect(BRAIN_SOCK)
            s.send(b'{"action": "ping"}')
            response = s.recv(1024)
            s.close()
            log(f"✅ Socket responsive: {response.decode()[:50]}")
            return True
        except Exception as e:
            log(f"❌ Socket not responding: {e}")
            # Try to remove stale socket
            try:
                os.remove(BRAIN_SOCK)
                log(f"🗑️ Removed stale socket file")
            except:
                pass
    else:
        log(f"Socket file does not exist")
    
    # Check brain process
    try:
        result = subprocess.run(['pgrep', '-f', 'complete_brain_v4.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            log(f"Brain PIDs found: {pids}")
            
            # Try signal to recreate socket
            for pid in pids[:2]:
                try:
                    log(f"Sending SIGUSR1 to PID {pid} to trigger socket recreation...")
                    subprocess.run(['kill', '-USR1', pid], check=False)
                    time.sleep(1)
                except Exception as e:
                    log(f"Signal failed: {e}")
        else:
            log("❌ No brain process found")
            return False
    except Exception as e:
        log(f"Process check failed: {e}")
    
    # Wait and recheck
    time.sleep(2)
    if os.path.exists(BRAIN_SOCK):
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect(BRAIN_SOCK)
            s.close()
            log("✅ Socket now responsive after fix attempt")
            return True
        except:
            log("❌ Socket still not responsive")
    
    return False

def restart_brain():
    log(f"\n{'='*60}")
    log(f"🔄 RESTARTING BRAIN SERVICE")
    log(f"{'='*60}")
    
    try:
        # Stop service
        log("Stopping aos-brain-v4 service...")
        result = subprocess.run(['systemctl', 'stop', 'aos-brain-v4'], 
                              capture_output=True, text=True)
        log(f"Stop result: {result.returncode}")
        time.sleep(3)
        
        # Clean up any stale socket
        if os.path.exists(BRAIN_SOCK):
            os.remove(BRAIN_SOCK)
            log("Removed stale socket before restart")
        
        # Start service
        log("Starting aos-brain-v4 service...")
        result = subprocess.run(['systemctl', 'start', 'aos-brain-v4'], 
                              capture_output=True, text=True)
        log(f"Start result: {result.returncode}")
        time.sleep(5)
        
        # Verify
        result = subprocess.run(['systemctl', 'is-active', 'aos-brain-v4'], 
                              capture_output=True, text=True)
        if 'active' in result.stdout:
            log("✅ Service restarted successfully")
            time.sleep(3)
            
            # Check socket
            if os.path.exists(BRAIN_SOCK):
                try:
                    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    s.settimeout(3)
                    s.connect(BRAIN_SOCK)
                    s.close()
                    log("✅ Socket now responsive after restart")
                    return True
                except Exception as e:
                    log(f"❌ Socket still not responding after restart: {e}")
                    return False
            else:
                log("❌ Socket file still not created after restart")
                return False
        else:
            log(f"❌ Service failed to start: {result.stdout}")
            return False
            
    except Exception as e:
        log(f"❌ Restart failed: {e}")
        return False

def main():
    log("\n" + "="*60)
    log("🔧 BRAIN SOCKET REPAIR TOOL v1.0")
    log("="*60)
    log(f"Target socket: {BRAIN_SOCK}")
    log(f"Time: {datetime.utcnow().isoformat()}")
    
    # Attempt 5 fixes
    for i in range(1, 6):
        if attempt_fix(i):
            log("\n" + "="*60)
            log("✅ REPAIR SUCCESSFUL - Socket restored")
            log("="*60)
            print("\n📋 REPAIR LOG:")
            for entry in REPAIR_LOG:
                print(entry)
            return 0
        time.sleep(2)
    
    # All 5 attempts failed - restart
    log("\n" + "="*60)
    log("⚠️  ALL 5 FIX ATTEMPTS FAILED")
    log("="*60)
    
    if restart_brain():
        log("\n" + "="*60)
        log("✅ RESTART SUCCESSFUL")
        log("="*60)
    else:
        log("\n" + "="*60)
        log("❌ RESTART FAILED - Manual intervention required")
        log("="*60)
    
    print("\n📋 FULL REPAIR LOG:")
    for entry in REPAIR_LOG:
        print(entry)
    
    return 0

if __name__ == "__main__":
    main()
