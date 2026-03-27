#!/usr/bin/env python3
"""
Critical Heartbeat - Life Support System.

The heartbeat monitors the brain. If brain fails, heartbeat restarts it.
If heartbeat fails, system is brain-dead (coma).

This is the failsafe layer. No recovery from heartbeat failure.

Architecture:
  Heartbeat (Critical Layer) ──► Monitors ──► Brain (7 regions)
       │                              │
       │                              ▼
       │                        Brain Down?
       │                              │
       └────────── Restart ◄─── Yes ──┘
       
  Heartbeat Fails?
       │
       ▼
  SYSTEM COMA - No recovery
"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class LifeSupportState:
    """Life support system state."""
    brain_pid: Optional[int] = None
    heart_pid: Optional[int] = None
    last_brain_heartbeat: float = 0.0
    last_heartbeat: float = 0.0
    brain_restarts: int = 0
    max_restarts: int = 3  # Max 3 restarts before giving up
    system_status: str = "healthy"  # healthy, degraded, critical, coma


class CriticalHeartbeat:
    """
    Critical life support heartbeat.
    
    Responsibilities:
    1. Monitor brain health
    2. Auto-restart brain if down
    3. Maintain own heartbeat
    4. If this fails, system enters coma
    
    This is the failsafe of last resort.
    """
    
    def __init__(self):
        self.state = LifeSupportState()
        self.running = False
        self.critical_log = []
        self.max_log = 100
        
        # Setup signal handlers for graceful death
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        print("=" * 70)
        print("🚨 CRITICAL HEARTBEAT - LIFE SUPPORT SYSTEM")
        print("=" * 70)
        print()
        print("⚠️  WARNING: This is the failsafe layer.")
        print("    If heartbeat fails, system enters COMA.")
        print("    No recovery possible.")
        print()
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\n[CriticalHeartbeat] Received signal {signum}")
        self._log("CRITICAL", "Signal received, entering controlled shutdown")
        self.running = False
    
    def _log(self, level: str, message: str):
        """Log critical event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        self.critical_log.append(entry)
        if len(self.critical_log) > self.max_log:
            self.critical_log.pop(0)
        
        # Also print
        print(f"[{level}] {message}")
    
    def _check_brain_health(self) -> bool:
        """
        Check if brain is healthy.
        
        Returns True if brain is up and responsive.
        """
        try:
            # Check if brain daemon process exists
            result = subprocess.run(
                ["pgrep", "-f", "brain_daemon.py"],
                capture_output=True
            )
            
            if result.returncode != 0:
                self._log("WARNING", "Brain process not found")
                return False
            
            # Check if API responds
            import urllib.request
            try:
                with urllib.request.urlopen(
                    "http://localhost:5000/health",
                    timeout=5
                ) as resp:
                    data = json.loads(resp.read())
                    if data.get("status") == "healthy":
                        self.state.last_brain_heartbeat = time.time()
                        return True
            except:
                self._log("WARNING", "Brain API not responding")
                return False
            
            return False
            
        except Exception as e:
            self._log("ERROR", f"Brain check failed: {e}")
            return False
    
    def _restart_brain(self) -> bool:
        """
        Attempt to restart the brain.
        
        Returns True if restart successful.
        """
        if self.state.brain_restarts >= self.state.max_restarts:
            self._log("CRITICAL", f"Max restarts ({self.state.max_restarts}) reached")
            self.state.system_status = "coma"
            return False
        
        self._log("ALERT", f"Attempting brain restart #{self.state.brain_restarts + 1}")
        
        try:
            # Kill existing brain if any
            subprocess.run(
                ["pkill", "-9", "-f", "brain_daemon.py"],
                capture_output=True
            )
            time.sleep(2)
            
            # Start brain
            brain_path = Path(__file__).parent.parent / "brain_daemon.py"
            subprocess.Popen(
                ["python3", str(brain_path), "foreground"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            # Wait for startup
            time.sleep(5)
            
            # Verify
            if self._check_brain_health():
                self.state.brain_restarts += 1
                self._log("SUCCESS", f"Brain restarted successfully")
                return True
            else:
                self._log("FAILURE", "Brain restart failed verification")
                return False
                
        except Exception as e:
            self._log("ERROR", f"Brain restart error: {e}")
            return False
    
    def _check_self_health(self) -> bool:
        """
        Check if heartbeat itself is healthy.
        
        This is critical - if this fails, system enters coma.
        """
        # Basic self-check
        try:
            # Can we still process?
            self.state.last_heartbeat = time.time()
            
            # Check we haven't been stuck
            if hasattr(self, '_last_tick'):
                if time.time() - self._last_tick > 60:
                    self._log("CRITICAL", "Heartbeat appears stuck!")
                    return False
            
            self._last_tick = time.time()
            return True
            
        except Exception as e:
            self._log("CRITICAL", f"Self-check failed: {e}")
            return False
    
    def _enter_coma(self):
        """
        Enter system coma.
        
        This is the end state. No recovery.
        """
        self._log("COMA", "SYSTEM ENTERING COMA STATE")
        self._log("COMA", "Heart has failed. Brain cannot function.")
        self._log("COMA", "System requires manual intervention.")
        self._log("COMA", "No automatic recovery possible.")
        
        self.state.system_status = "coma"
        self.running = False
        
        # Write coma state to file
        coma_file = Path.home() / ".aos" / "coma_state.json"
        try:
            with open(coma_file, 'w') as f:
                json.dump({
                    "status": "coma",
                    "timestamp": datetime.now().isoformat(),
                    "reason": "heartbeat_failure",
                    "last_brain_heartbeat": self.state.last_brain_heartbeat,
                    "last_critical_heartbeat": self.state.last_heartbeat
                }, f, indent=2)
        except:
            pass
    
    def _display_status(self):
        """Display current life support status."""
        status_emoji = {
            "healthy": "🟢",
            "degraded": "🟡",
            "critical": "🔴",
            "coma": "💀"
        }
        
        emoji = status_emoji.get(self.state.system_status, "⚪")
        
        print(f"\n{emoji} CRITICAL STATUS: {self.state.system_status.upper()}")
        print(f"   Brain Restarts: {self.state.brain_restarts}/{self.state.max_restarts}")
        print(f"   Last Brain Pulse: {time.time() - self.state.last_brain_heartbeat:.1f}s ago")
        print(f"   Last Heartbeat: {time.time() - self.state.last_heartbeat:.1f}s ago")
        
        if self.state.system_status == "coma":
            print(f"\n   💀 SYSTEM IS IN COMA")
            print(f"   Manual intervention required")
    
    def run_life_support(self):
        """
        Run critical life support loop.
        
        This is the main loop that keeps the system alive.
        If this stops, the system dies.
        """
        print("[CriticalHeartbeat] Starting life support...")
        print("[CriticalHeartbeat] Heartbeat interval: 5 seconds")
        print("[CriticalHeartbeat] Press Ctrl+C to trigger controlled shutdown")
        print()
        
        self.running = True
        self._last_tick = time.time()
        
        try:
            while self.running:
                # 1. Check self (am I alive?)
                if not self._check_self_health():
                    self._log("CRITICAL", "Heartbeat self-check failed")
                    self._enter_coma()
                    break
                
                # 2. Check brain (is patient alive?)
                brain_healthy = self._check_brain_health()
                
                if not brain_healthy:
                    self.state.system_status = "degraded"
                    
                    # Attempt restart
                    if not self._restart_brain():
                        self._log("CRITICAL", "Brain restart failed")
                        self.state.system_status = "critical"
                        
                        # One more try after longer wait
                        time.sleep(10)
                        if not self._restart_brain():
                            self._enter_coma()
                            break
                else:
                    # Brain is healthy
                    if self.state.system_status != "healthy":
                        self._log("RECOVERY", "Brain health restored")
                        self.state.system_status = "healthy"
                
                # 3. Display status periodically
                if int(time.time()) % 30 == 0:
                    self._display_status()
                
                # 4. Sleep until next heartbeat
                time.sleep(5)
                
        except Exception as e:
            self._log("CRITICAL", f"Unexpected error: {e}")
            self._enter_coma()
        
        # Shutdown
        if self.state.system_status == "coma":
            print("\n" + "=" * 70)
            print("💀 SYSTEM COMA")
            print("=" * 70)
            print("The heartbeat has failed.")
            print("The system is brain-dead.")
            print("No automatic recovery is possible.")
            print("=" * 70)
        else:
            print("\n[CriticalHeartbeat] Life support stopped")
    
    def get_coma_report(self) -> Optional[Dict]:
        """Get coma state if system is in coma."""
        coma_file = Path.home() / ".aos" / "coma_state.json"
        if coma_file.exists():
            try:
                with open(coma_file) as f:
                    return json.load(f)
            except:
                pass
        return None


def demo_critical_heartbeat():
    """Demo critical heartbeat system."""
    print("\n" + "=" * 70)
    print("🚨 CRITICAL HEARTBEAT DEMO")
    print("=" * 70)
    print()
    print("This is the failsafe layer that keeps the system alive.")
    print("If brain fails, heartbeat restarts it.")
    print("If heartbeat fails, system enters COMA.")
    print()
    print("Running for 30 seconds (simulated)...")
    print()
    
    heartbeat = CriticalHeartbeat()
    
    # Run for limited time for demo
    heartbeat.running = True
    start = time.time()
    
    try:
        while heartbeat.running and time.time() - start < 30:
            # Simulate checks
            brain_ok = heartbeat._check_brain_health()
            
            if not brain_ok:
                print("[Demo] Brain not detected, would attempt restart")
            else:
                if int(time.time()) % 5 == 0:
                    print("[Demo] Brain healthy, monitoring...")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[Demo] Stopped")
    
    print("\n" + "=" * 70)
    print("✅ Critical Heartbeat Demo Complete")
    print("=" * 70)
    print()
    print("In production:")
    print("  - Heartbeat runs continuously")
    print("  - Auto-restarts brain if down")
    print("  - If heartbeat fails: SYSTEM COMA")
    print("  - No recovery from coma")
    print("=" * 70)


if __name__ == "__main__":
    demo_critical_heartbeat()
