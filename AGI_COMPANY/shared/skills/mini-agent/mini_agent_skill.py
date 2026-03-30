#!/usr/bin/env python3
"""
Mini-Agent Skill - Autonomous Task Execution
Actually runs tasks, workflows, cron jobs
"""

import os
import json
import time
import schedule
import threading
from typing import Dict, List, Callable, Optional
from datetime import datetime
from pathlib import Path

class MiniAgentSkill:
    """Real task automation skill"""
    
    def __init__(self):
        self.tasks: Dict[str, Dict] = {}
        self.workflows: Dict[str, List] = {}
        self.running = False
        self.scheduler_thread = None
        self.task_queue = []
        print("[Mini-Agent] Skill activated")
    
    def add_task(self, name: str, func: Callable, schedule_str: str = None) -> bool:
        """Add a task to execute"""
        self.tasks[name] = {
            "func": func,
            "schedule": schedule_str,
            "last_run": None,
            "run_count": 0
        }
        
        if schedule_str:
            # Parse schedule (e.g., "every 1 minutes")
            parts = schedule_str.split()
            if len(parts) >= 3 and parts[0] == "every":
                interval = int(parts[1])
                unit = parts[2]
                
                if unit in ["minute", "minutes"]:
                    schedule.every(interval).minutes.do(self._run_task, name)
                elif unit in ["hour", "hours"]:
                    schedule.every(interval).hours.do(self._run_task, name)
                elif unit in ["day", "days"]:
                    schedule.every(interval).days.do(self._run_task, name)
        
        return True
    
    def _run_task(self, name: str):
        """Execute a task"""
        if name in self.tasks:
            task = self.tasks[name]
            try:
                print(f"[Mini-Agent] Running task: {name}")
                task["func"]()
                task["last_run"] = datetime.now().isoformat()
                task["run_count"] += 1
            except Exception as e:
                print(f"[Mini-Agent] Task {name} failed: {e}")
    
    def run_task_now(self, name: str) -> bool:
        """Run a task immediately"""
        if name in self.tasks:
            self._run_task(name)
            return True
        return False
    
    def create_workflow(self, name: str, steps: List[Dict]) -> bool:
        """Create a multi-step workflow"""
        self.workflows[name] = steps
        return True
    
    def run_workflow(self, name: str) -> bool:
        """Execute a workflow"""
        if name not in self.workflows:
            return False
        
        print(f"[Mini-Agent] Running workflow: {name}")
        for step in self.workflows[name]:
            step_name = step.get("name", "unnamed")
            action = step.get("action")
            
            print(f"  Step: {step_name}")
            try:
                if callable(action):
                    action()
                elif isinstance(action, str) and action in self.tasks:
                    self._run_task(action)
            except Exception as e:
                print(f"    Failed: {e}")
                if step.get("critical", False):
                    print(f"  Workflow {name} aborted at {step_name}")
                    return False
        
        print(f"[Mini-Agent] Workflow {name} complete")
        return True
    
    def start_scheduler(self):
        """Start the scheduler in a thread"""
        if self.running:
            return
        
        self.running = True
        
        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        self.scheduler_thread = threading.Thread(target=run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        print("[Mini-Agent] Scheduler started")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        print("[Mini-Agent] Scheduler stopped")
    
    def get_status(self) -> Dict:
        """Get current status"""
        return {
            "tasks": len(self.tasks),
            "workflows": len(self.workflows),
            "running": self.running,
            "scheduled_jobs": len(schedule.jobs)
        }

if __name__ == "__main__":
    mini = MiniAgentSkill()
    
    # Add sample task
    def sample_task():
        print("Sample task executed")
    
    mini.add_task("heartbeat", sample_task, "every 1 minutes")
    mini.start_scheduler()
    
    print("Mini-Agent skill ready")
    print(mini.get_status())
