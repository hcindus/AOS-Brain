#!/usr/bin/env python3
"""
Forge Factory Controller v1.0
Agent: Forge
Role: Builder, Android Developer, RS-80 Lead
Tick: Every 300 seconds
"""

import sys
import os
import json
import time
from datetime import datetime

# Paths
WORKSPACE = "/root/.openclaw/workspace"
FACTORY_QUEUE = f"{WORKSPACE}/factory_queue"
AGENT_DIR = f"{WORKSPACE}/agent_sandboxes/forge"
LOG_FILE = f"{AGENT_DIR}/forge.log"

class ForgeController:
    def __init__(self):
        self.name = "Forge"
        self.role = "Factory Builder"
        self.current_task = None
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{self.name}] {message}\n"
        with open(LOG_FILE, "a") as f:
            f.write(log_line)
        print(log_line.strip())
        
    def check_factory_queue(self):
        """Check for RS-80 tasks"""
        rs80_task = f"{FACTORY_QUEUE}/DF-RS80-001-v2_Chelios2.md"
        # Note: Chelios2 has this task, but Forge is backup
        
        if os.path.exists(rs80_task):
            self.log(f"Found RS-80 task: {rs80_task}")
            return "RS-80_BUILD"
        return None
        
    def execute_tick(self):
        """Main tick execution"""
        self.log("Tick executing...")
        
        # Check for tasks
        task = self.check_factory_queue()
        
        if task == "RS-80_BUILD":
            self.log("RS-80 build in progress. Monitoring...")
            # Check if RS-80 directory exists and has activity
            rs80_dir = f"{WORKSPACE}/reggiestarr-rs80"
            if os.path.exists(rs80_dir):
                file_count = len([f for f in os.listdir(rs80_dir) if os.path.isfile(os.path.join(rs80_dir, f))])
                self.log(f"RS-80 project has {file_count} files")
        else:
            self.log("No active tasks. Standing by.")
            
        self.log("Tick complete.")

def main():
    controller = ForgeController()
    
    if len(sys.argv) > 1 and sys.argv[1] == "tick":
        controller.execute_tick()
    else:
        print(f"Usage: {sys.argv[0]} tick")
        print("  Execute single tick cycle")

if __name__ == "__main__":
    main()
