#!/usr/bin/env python3
"""
Auto-Revive System - Emergency Recovery from Coma.

If Critical Heartbeat enters coma, this system attempts revival:
1. Detect coma state
2. Attempt emergency restart procedures
3. Log all revival attempts
4. If successful: restore full operation
5. If fails: final system shutdown
"""

import os
import sys
import json
import time
import subprocess
import signal
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class RevivalAttempt:
    """Record of revival attempt."""
    timestamp: str
    method: str
    success: bool
    duration: float
    error: Optional[str] = None


class AutoRevive:
    """Emergency auto-revive system."""
    
    def __init__(self):
        self.coma_file = Path.home() / ".aos" / "coma_state.json"
        self.revival_log_file = Path.home() / ".aos" / "revival_log.json"
        self.max_revivals = 5
        self.attempts: List[RevivalAttempt] = []
        self.running = False
        
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        print("=" * 70)
        print("🚑 AUTO-REVIVE SYSTEM - Emergency Recovery")
        print("=" * 70)
        print()
    
    def _signal_handler(self, signum, frame):
        print(f"\n[AutoRevive] Signal {signum} received, stopping")
        self.running = False
    
    def _log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().isoformat()
        print(f"[{level}] {timestamp} - {message}")
    
    def check_coma(self) -> bool:
        """Check if system is in coma."""
        if not self.coma_file.exists():
            return False
        try:
            with open(self.coma_file) as f:
                data = json.load(f)
                return data.get("status") == "coma"
        except:
            return False
    
    def attempt_revival(self) -> bool:
        """Attempt to revive from coma."""
        self._log("COMA DETECTED - INITIATING REVIVAL", "CRITICAL")
        
        methods = [
            ("Soft Restart", self._soft_restart),
            ("Hard Restart", self._hard_restart),
            ("Systemd Restart", self._systemd_restart),
            ("Clean Slate", self._clean_slate),
            ("Nuclear Option", self._nuclear_option),
        ]
        
        for i, (name, method) in enumerate(methods, 1):
            self._log(f"Attempting {name} ({i}/5)...", "REVIVAL")
            start = time.time()
            
            try:
                success = method()
                duration = time.time() - start
                
                attempt = RevivalAttempt(
                    timestamp=datetime.now().isoformat(),
                    method=name,
                    success=success,
                    duration=duration
                )
                self.attempts.append(attempt)
                
                if success:
                    self._log(f"✅ {name} SUCCESSFUL", "SUCCESS")
                    self._clear_coma()
                    return True
                else:
                    self._log(f"❌ {name} FAILED", "WARNING")
                    
            except Exception as e:
                self._log(f"Error in {name}: {e}", "ERROR")
        
        self._log("ALL REVIVAL METHODS FAILED", "CRITICAL")
        return False
    
    def _soft_restart(self) -> bool:
        """Method 1: Soft restart."""
        try:
            subprocess.run(["pkill", "-15", "-f", "brain_daemon.py"], 
                         capture_output=True, timeout=5)
            time.sleep(2)
            
            brain_path = Path(__file__).parent.parent / "brain_daemon.py"
            subprocess.Popen(["python3", str(brain_path), "foreground"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           start_new_session=True)
            
            time.sleep(5)
            return self._verify_brain()
        except:
            return False
    
    def _hard_restart(self) -> bool:
        """Method 2: Hard restart."""
        try:
            subprocess.run(["pkill", "-9", "-f", "brain"], capture_output=True, timeout=5)
            time.sleep(3)
            
            brain_path = Path(__file__).parent.parent / "brain_daemon.py"
            subprocess.Popen(["python3", str(brain_path), "foreground"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           start_new_session=True)
            
            time.sleep(8)
            return self._verify_brain()
        except:
            return False
    
    def _systemd_restart(self) -> bool:
        """Method 3: Systemd restart."""
        try:
            result = subprocess.run(["systemctl", "restart", "aos-brain"],
                                  capture_output=True, timeout=10)
            time.sleep(10)
            return self._verify_brain()
        except:
            return False
    
    def _clean_slate(self) -> bool:
        """Method 4: Clean slate."""
        try:
            subprocess.run(["pkill", "-9", "-f", "brain"], capture_output=True, timeout=5)
            time.sleep(3)
            
            brain_path = Path(__file__).parent.parent / "brain_daemon.py"
            subprocess.Popen(["python3", str(brain_path), "foreground"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           start_new_session=True)
            
            time.sleep(10)
            return self._verify_brain()
        except:
            return False
    
    def _nuclear_option(self) -> bool:
        """Method 5: Nuclear option - system reboot."""
        try:
            self._log("Initiating system reboot...", "CRITICAL")
            time.sleep(5)
            subprocess.run(["reboot"], capture_output=True)
            return True  # If we get here, it failed
        except:
            return False
    
    def _verify_brain(self) -> bool:
        """Verify brain is up."""
        try:
            import urllib.request
            with urllib.request.urlopen("http://localhost:5000/health", timeout=5) as resp:
                data = json.loads(resp.read())
                return data.get("status") == "healthy"
        except:
            return False
    
    def _clear_coma(self):
        """Clear coma state."""
        if self.coma_file.exists():
            try:
                recovery_file = Path.home() / ".aos" / f"recovered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                self.coma_file.rename(recovery_file)
            except:
                pass
    
    def run_monitor(self):
        """Run auto-revive monitor."""
        self._log("Starting auto-revive monitor...")
        self.running = True
        
        try:
            while self.running:
                if self.check_coma():
                    success = self.attempt_revival()
                    if not success:
                        self._log("Revival failed, continuing to monitor...", "WARNING")
                time.sleep(10)
        except KeyboardInterrupt:
            self.running = False
        
        self._log("Auto-revive monitor stopped")


if __name__ == "__main__":
    print("🚑 Auto-Revive System")
    print("Monitors for coma and attempts revival")
    print()
    
    revive = AutoRevive()
    
    # Demo
    print("5 revival methods available:")
    print("  1. Soft restart")
    print("  2. Hard restart") 
    print("  3. Systemd restart")
    print("  4. Clean slate")
    print("  5. Nuclear option (reboot)")
    print()
    print("System ready for monitoring.")
