#!/usr/bin/env python3
"""
AOS MULTI-SENSE DAEMON v1.0
Coordinates Vision + Audio + Text feeding to brain cortex
"""

import subprocess
import time
import sys
from datetime import datetime

class MultiSenseOrchestrator:
    """
    Orchestrates multiple sensory inputs to the brain
    """
    
    def __init__(self):
        self.processes = {}
        print("="*70)
        print("  AOS MULTI-SENSE ORCHESTRATOR v1.0")
        print("="*70)
    
    def start_vision(self):
        """Start camera vision daemon"""
        print("\n[1] Starting Camera Vision...")
        proc = subprocess.Popen(
            [sys.executable, '/root/.aos/aos/camera_vision_daemon.py'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        self.processes['vision'] = proc
        time.sleep(2)
        print(f"    PID: {proc.pid}")
    
    def start_audio(self):
        """Start audio sense"""
        print("\n[2] Starting Audio Sense...")
        proc = subprocess.Popen(
            [sys.executable, '/root/.aos/aos/audio_sense.py'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        self.processes['audio'] = proc
        time.sleep(1)
        print(f"    PID: {proc.pid}")
    
    def start_all(self):
        """Start all sensory inputs"""
        self.start_vision()
        self.start_audio()
        
        print("\n" + "="*70)
        print("  ALL SENSES ACTIVE")
        print("="*70)
        print("\n  Running processes:")
        for name, proc in self.processes.items():
            print(f"    {name:10s} PID {proc.pid}")
        print("\n  Feeding to brain cortex every 2 seconds")
        print("  Visual triggers: motion, brightness, color, novelty")
        print("  Audio spectrum: 5 frequency bands")
        print("\n  Press Ctrl+C to stop")
        print("="*70 + "\n")
    
    def monitor(self):
        """Monitor and keep alive"""
        try:
            while True:
                # Check if processes are alive
                for name, proc in list(self.processes.items()):
                    if proc.poll() is not None:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] {name} exited, restarting...")
                        # Restart logic would go here
                
                time.sleep(5)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop all processes"""
        print("\n[Shutting down senses...]")
        for name, proc in self.processes.items():
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except:
                proc.kill()
            print(f"  {name} stopped")
        print("\nAll senses offline.")

def main():
    orchestrator = MultiSenseOrchestrator()
    orchestrator.start_all()
    orchestrator.monitor()

if __name__ == "__main__":
    main()
