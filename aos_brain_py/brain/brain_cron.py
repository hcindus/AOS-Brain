#!/usr/bin/env python3
"""
Brain Cron - Intelligent Scheduling System for Ternary Brain.

Replaces traditional cron with context-aware, adaptive scheduling.
Uses only standard library (no schedule module dependency).
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ScheduledTask:
    """A task scheduled in the brain."""
    name: str
    handler: Callable
    schedule_type: str
    schedule_value: str
    mode: str
    priority: TaskPriority
    guard: bool
    last_run: Optional[float] = None
    next_run: Optional[float] = None
    run_count: int = 0
    success_count: int = 0
    failure_count: int = 0


class BrainCron:
    """
    Intelligent cron system powered by 7-region ternary brain.
    """
    
    def __init__(self, brain: Optional[SevenRegionBrain] = None):
        self.brain = brain or SevenRegionBrain()
        self.tasks: Dict[str, ScheduledTask] = {}
        self.running = False
        self.scheduler_thread = None
        self.lock = threading.Lock()
        self.failure_patterns: Dict[str, int] = {}
        
        print("[BrainCron] Initialized")
    
    def _get_system_load(self) -> float:
        """Get current system load."""
        try:
            with open('/proc/loadavg') as f:
                return float(f.read().split()[0])
        except:
            return 0.0
    
    def _should_run(self, task: ScheduledTask) -> bool:
        """Check if task should run."""
        load = self._get_system_load()
        if load > 8.0:
            print(f"[BrainCron] Skipping {task.name}: load {load:.1f}")
            return False
        return True
    
    def _execute_with_brain(self, task: ScheduledTask):
        """Execute task with brain processing."""
        print(f"\n[BrainCron] Executing: {task.name} (mode: {task.mode})")
        
        result = self.brain.feed(f"[CRON] Execute {task.name}", source="cron")
        
        try:
            with self.lock:
                task.last_run = time.time()
                task.run_count += 1
            
            task.handler()
            
            with self.lock:
                task.success_count += 1
            
            print(f"[BrainCron] ✅ {task.name} completed")
            
        except Exception as e:
            with self.lock:
                task.failure_count += 1
            self.failure_patterns[task.name] = self.failure_patterns.get(task.name, 0) + 1
            print(f"[BrainCron] ❌ {task.name} failed: {e}")
    
    def schedule_interval(self, name: str, handler: Callable, 
                          seconds: int, mode: str = "adaptive",
                          priority: TaskPriority = TaskPriority.MEDIUM,
                          guard: bool = True):
        """Schedule task by interval."""
        task = ScheduledTask(
            name=name,
            handler=handler,
            schedule_type="interval",
            schedule_value=str(seconds),
            mode=mode,
            priority=priority,
            guard=guard,
            next_run=time.time() + seconds
        )
        
        with self.lock:
            self.tasks[name] = task
        
        print(f"[BrainCron] Scheduled: {name} (every {seconds}s, mode: {mode})")
    
    def _check_and_run(self):
        """Check all tasks and run due ones."""
        now = time.time()
        
        with self.lock:
            tasks_copy = list(self.tasks.values())
        
        for task in tasks_copy:
            if task.next_run and now >= task.next_run:
                if self._should_run(task):
                    self._execute_with_brain(task)
                
                # Schedule next run
                interval = int(task.schedule_value)
                with self.lock:
                    task.next_run = now + interval
    
    def run_continuous(self):
        """Run scheduler continuously."""
        print("[BrainCron] Starting scheduler...")
        self.running = True
        
        try:
            while self.running:
                self._check_and_run()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[BrainCron] Stopping...")
            self.running = False
    
    def start(self):
        """Start in background."""
        self.scheduler_thread = threading.Thread(target=self.run_continuous)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        print("[BrainCron] Scheduler started")
    
    def get_status(self) -> Dict:
        """Get status."""
        return {
            "running": self.running,
            "tasks": len(self.tasks),
            "brain_tick": self.brain.tick_count,
            "load": self._get_system_load()
        }


def demo_task():
    """Demo task."""
    print("[Task] Demo task executed")

def demo_brain_cron():
    """Demo brain cron."""
    print("=" * 60)
    print("🧠 BRAIN CRON DEMO")
    print("=" * 60)
    
    cron = BrainCron()
    
    # Schedule tasks
    cron.schedule_interval("health_check", demo_task, seconds=5, mode="Cautious")
    cron.schedule_interval("data_sync", demo_task, seconds=10, mode="Analytical")
    
    print("\nRunning for 30 seconds...")
    cron.start()
    
    try:
        time.sleep(30)
    except KeyboardInterrupt:
        pass
    
    cron.running = False
    
    print("\n" + "=" * 60)
    print("✅ Brain Cron Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    demo_brain_cron()
