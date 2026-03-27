#!/usr/bin/env python3
"""
Brain Cron Hooks - Integration with existing cron system.

This module allows the ternary brain to gradually take over cron jobs
by intercepting, learning, and eventually replacing them with 
intelligent brain-based scheduling.

Features:
- Intercept existing cron jobs
- Learn execution patterns
- Adapt schedules based on success/failure
- Resource-aware execution
- User style adaptation
"""

import os
import sys
import json
import time
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain


@dataclass
class CronJob:
    """Represents a cron job."""
    name: str
    schedule: str  # Cron expression or time
    command: str
    user: str
    enabled: bool = True
    last_run: Optional[float] = None
    last_output: str = ""
    success_count: int = 0
    failure_count: int = 0
    avg_duration: float = 0.0
    resource_usage: Dict = field(default_factory=dict)


class CronInterceptor:
    """
    Intercepts and learns from existing cron jobs.
    
    Phase 1: Monitor (learn patterns)
    Phase 2: Assist (brain validates before execution)
    Phase 3: Replace (brain takes full control)
    """
    
    def __init__(self, brain: SevenRegionBrain):
        self.brain = brain
        self.phase = "monitor"  # monitor, assist, replace
        self.cron_jobs: Dict[str, CronJob] = {}
        self.execution_history: List[Dict] = []
        self.pattern_db = Path.home() / ".aos" / "brain" / "cron_patterns.json"
        self.pattern_db.parent.mkdir(parents=True, exist_ok=True)
        
        self._load_patterns()
        self._scan_cron_jobs()
        
    def _scan_cron_jobs(self):
        """Scan system cron jobs."""
        try:
            # Get user crontab
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self._parse_crontab(result.stdout, os.getenv("USER", "root"))
                
        except Exception as e:
            print(f"[CronInterceptor] Could not scan crontab: {e}")
        
        # Also check system cron directories
        self._scan_cron_dirs()
    
    def _parse_crontab(self, content: str, user: str):
        """Parse crontab content."""
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse cron line: * * * * * command
            match = re.match(r'^(\S+\s+\S+\s+\S+\s+\S+\s+\S+)\s+(.+)$', line)
            if match:
                schedule = match.group(1)
                command = match.group(2)
                
                # Extract name from command or use command as name
                name = self._extract_job_name(command)
                
                self.cron_jobs[name] = CronJob(
                    name=name,
                    schedule=schedule,
                    command=command,
                    user=user
                )
                
        print(f"[CronInterceptor] Found {len(self.cron_jobs)} cron jobs")
    
    def _scan_cron_dirs(self):
        """Scan system cron directories."""
        cron_dirs = [
            "/etc/cron.d",
            "/etc/cron.hourly",
            "/etc/cron.daily",
            "/etc/cron.weekly",
            "/etc/cron.monthly"
        ]
        
        for cron_dir in cron_dirs:
            if os.path.exists(cron_dir):
                for item in os.listdir(cron_dir):
                    path = os.path.join(cron_dir, item)
                    if os.path.isfile(path):
                        self._parse_cron_file(path, item)
    
    def _parse_cron_file(self, path: str, name: str):
        """Parse a cron file."""
        try:
            with open(path) as f:
                content = f.read()
                
            # Determine schedule from directory
            schedule = "* * * * *"
            if "hourly" in path:
                schedule = "0 * * * *"
            elif "daily" in path:
                schedule = "0 0 * * *"
            elif "weekly" in path:
                schedule = "0 0 * * 0"
            elif "monthly" in path:
                schedule = "0 0 1 * *"
            
            self.cron_jobs[name] = CronJob(
                name=name,
                schedule=schedule,
                command=f"bash {path}",
                user="root"
            )
            
        except Exception as e:
            print(f"[CronInterceptor] Error parsing {path}: {e}")
    
    def _extract_job_name(self, command: str) -> str:
        """Extract job name from command."""
        # Try to find a meaningful name
        if "lead" in command.lower():
            return "lead_scraper"
        elif "health" in command.lower():
            return "health_check"
        elif "price" in command.lower():
            return "price_sync"
        elif "git" in command.lower():
            return "git_push"
        elif "backup" in command.lower():
            return "backup"
        else:
            # Use first word or hash
            words = command.split()
            if words:
                return words[0].split('/')[-1].replace('.', '_')
            return f"job_{hash(command) % 10000}"
    
    def _load_patterns(self):
        """Load learned patterns from disk."""
        if self.pattern_db.exists():
            try:
                with open(self.pattern_db) as f:
                    data = json.load(f)
                    self.execution_history = data.get("history", [])
                    print(f"[CronInterceptor] Loaded {len(self.execution_history)} execution records")
            except Exception as e:
                print(f"[CronInterceptor] Could not load patterns: {e}")
    
    def _save_patterns(self):
        """Save learned patterns to disk."""
        data = {
            "history": self.execution_history[-100:],  # Keep last 100
            "jobs": {name: {
                "schedule": job.schedule,
                "success_count": job.success_count,
                "failure_count": job.failure_count,
                "avg_duration": job.avg_duration
            } for name, job in self.cron_jobs.items()}
        }
        
        try:
            with open(self.pattern_db, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[CronInterceptor] Could not save patterns: {e}")
    
    def intercept_execution(self, job_name: str) -> bool:
        """
        Intercept a cron job execution.
        
        Returns True if brain allows execution, False to skip.
        """
        if job_name not in self.cron_jobs:
            return True  # Unknown job, let it run
        
        job = self.cron_jobs[job_name]
        
        # Phase-based behavior
        if self.phase == "monitor":
            # Just monitor, always allow
            print(f"[CronInterceptor] Monitoring: {job_name}")
            return True
        
        elif self.phase == "assist":
            # Brain validates before execution
            print(f"[CronInterceptor] Validating: {job_name}")
            
            # Check system resources
            load = self._get_system_load()
            if load > 8.0:
                print(f"  Skipping: system load {load:.1f}")
                return False
            
            # Check failure pattern
            if job.failure_count > 3 and job.success_count == 0:
                print(f"  Warning: {job_name} has repeated failures")
            
            return True
        
        elif self.phase == "replace":
            # Brain takes over execution
            print(f"[CronInterceptor] Brain executing: {job_name}")
            return self._brain_execute(job)
        
        return True
    
    def _brain_execute(self, job: CronJob) -> bool:
        """Execute job through brain."""
        # Process through brain
        obs = f"Execute cron job: {job.name}"
        result = self.brain.feed(obs, source="cron_intercept")
        
        # Brainstem safety check
        mode = result.get("mode", "Unknown")
        if mode == "Cautious" and job.failure_count > 5:
            print(f"  Brain says: Cautious mode, high failure rate - skipping")
            return False
        
        # Execute the actual command
        try:
            start_time = time.time()
            result = subprocess.run(
                job.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            duration = time.time() - start_time
            
            # Update job stats
            job.last_run = time.time()
            job.last_output = result.stdout[:500]  # Keep first 500 chars
            job.avg_duration = (job.avg_duration * job.success_count + duration) / (job.success_count + 1)
            
            if result.returncode == 0:
                job.success_count += 1
                success = True
            else:
                job.failure_count += 1
                success = False
            
            # Log execution
            self.execution_history.append({
                "job": job.name,
                "timestamp": time.time(),
                "success": success,
                "duration": duration,
                "mode": mode
            })
            
            self._save_patterns()
            return success
            
        except Exception as e:
            job.failure_count += 1
            print(f"  Execution error: {e}")
            return False
    
    def _get_system_load(self) -> float:
        """Get system load."""
        try:
            with open('/proc/loadavg') as f:
                return float(f.read().split()[0])
        except:
            return 0.0
    
    def get_insights(self) -> Dict:
        """Get insights from learned patterns."""
        insights = {
            "total_jobs": len(self.cron_jobs),
            "total_executions": len(self.execution_history),
            "phase": self.phase,
            "patterns": {}
        }
        
        # Analyze patterns
        for name, job in self.cron_jobs.items():
            total = job.success_count + job.failure_count
            if total > 0:
                success_rate = job.success_count / total
                insights["patterns"][name] = {
                    "success_rate": f"{success_rate:.1%}",
                    "avg_duration": f"{job.avg_duration:.1f}s",
                    "reliability": "high" if success_rate > 0.9 else "medium" if success_rate > 0.5 else "low"
                }
        
        return insights
    
    def advance_phase(self):
        """Advance to next phase."""
        phases = ["monitor", "assist", "replace"]
        current_idx = phases.index(self.phase)
        if current_idx < len(phases) - 1:
            self.phase = phases[current_idx + 1]
            print(f"[CronInterceptor] Advanced to phase: {self.phase}")
    
    def generate_brain_cron_config(self) -> str:
        """Generate brain-native cron configuration."""
        config = "# Brain Cron Configuration\n"
        config += f"# Generated: {datetime.now().isoformat()}\n\n"
        
        for name, job in self.cron_jobs.items():
            config += f"# Job: {name}\n"
            config += f"# Original schedule: {job.schedule}\n"
            config += f"# Success rate: {job.success_count}/{job.success_count + job.failure_count}\n"
            config += f"schedule('{name}', '{job.command}', '{job.schedule}')\n\n"
        
        return config


def demo_cron_interceptor():
    """Demo cron interception."""
    print("=" * 70)
    print("🔗 CRON INTERCEPTOR DEMO")
    print("=" * 70)
    
    brain = SevenRegionBrain()
    interceptor = CronInterceptor(brain)
    
    print("\n--- Discovered Cron Jobs ---")
    for name, job in interceptor.cron_jobs.items():
        print(f"  {name}: {job.schedule}")
        print(f"    Command: {job.command[:60]}...")
    
    print("\n--- Insights ---")
    insights = interceptor.get_insights()
    print(f"Total jobs: {insights['total_jobs']}")
    print(f"Current phase: {insights['phase']}")
    
    if insights['patterns']:
        print("\nJob Patterns:")
        for name, pattern in insights['patterns'].items():
            print(f"  {name}: {pattern['success_rate']} success, {pattern['avg_duration']} avg")
    
    print("\n--- Generated Brain Cron Config ---")
    config = interceptor.generate_brain_cron_config()
    print(config[:500] + "..." if len(config) > 500 else config)
    
    print("\n" + "=" * 70)
    print("✅ Cron Interceptor ready!")
    print("=" * 70)


if __name__ == "__main__":
    demo_cron_interceptor()
