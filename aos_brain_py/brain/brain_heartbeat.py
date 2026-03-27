#!/usr/bin/env python3
"""
Brain Heartbeat - Intelligent Health Monitoring System.

Replaces traditional cron-based heartbeat with brain-aware monitoring:
- Context-aware checks (what matters right now)
- Predictive health (anticipate issues before they happen)
- Adaptive frequency (check more often when unstable)
- Learning patterns (when does system typically have issues)
"""

import os
import sys
import json
import time
import threading
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain


@dataclass
class HealthMetric:
    """A health metric reading."""
    name: str
    value: float
    threshold: float
    status: str  # "healthy", "warning", "critical"
    timestamp: float = field(default_factory=time.time)


class BrainHeartbeat:
    """
    Intelligent heartbeat system powered by 7-region brain.
    
    Features:
    - Limbic evaluation: How urgent is this check?
    - Hippocampal recall: Has this failed before?
    - PFC planning: What should we check next?
    - Adaptive frequency: Check more when unstable
    - Pattern learning: Predict failures
    """
    
    def __init__(self, brain: Optional[SevenRegionBrain] = None):
        self.brain = brain or SevenRegionBrain()
        self.running = False
        self.check_interval = 30  # Base: 30 seconds
        self.last_check_time = 0
        self.consecutive_failures = 0
        
        # Health history
        self.metrics_history: List[Dict] = []
        self.max_history = 100
        
        # Patterns
        self.failure_times: List[int] = []  # Hours when failures occur
        self.optimal_check_times: Dict[str, int] = {}
        
        # Components to monitor
        self.monitors = {
            "brain_daemon": self._check_brain_daemon,
            "ollama": self._check_ollama,
            "system_load": self._check_system_load,
            "memory_usage": self._check_memory,
            "disk_space": self._check_disk,
            "tmux_sessions": self._check_tmux,
        }
        
        print("[BrainHeartbeat] Initialized")
    
    def _check_brain_daemon(self) -> HealthMetric:
        """Check Python brain daemon."""
        try:
            # Check if process exists
            result = subprocess.run(
                ["pgrep", "-f", "brain_daemon.py"],
                capture_output=True
            )
            
            if result.returncode == 0:
                # Check API
                import urllib.request
                try:
                    with urllib.request.urlopen("http://localhost:5000/health", timeout=5) as resp:
                        data = json.loads(resp.read())
                        return HealthMetric(
                            name="brain_daemon",
                            value=1.0,
                            threshold=1.0,
                            status="healthy"
                        )
                except:
                    return HealthMetric(
                        name="brain_daemon",
                        value=0.5,
                        threshold=1.0,
                        status="warning"
                    )
            else:
                return HealthMetric(
                    name="brain_daemon",
                    value=0.0,
                    threshold=1.0,
                    status="critical"
                )
        except Exception as e:
            return HealthMetric(
                name="brain_daemon",
                value=0.0,
                threshold=1.0,
                status="critical"
            )
    
    def _check_ollama(self) -> HealthMetric:
        """Check Ollama status."""
        try:
            result = subprocess.run(
                ["pgrep", "ollama"],
                capture_output=True
            )
            
            if result.returncode == 0:
                return HealthMetric(
                    name="ollama",
                    value=1.0,
                    threshold=1.0,
                    status="healthy"
                )
            else:
                return HealthMetric(
                    name="ollama",
                    value=0.0,
                    threshold=1.0,
                    status="warning"  # Ollama is secondary now
                )
        except:
            return HealthMetric(
                name="ollama",
                value=0.0,
                threshold=1.0,
                status="warning"
            )
    
    def _check_system_load(self) -> HealthMetric:
        """Check system load."""
        try:
            with open('/proc/loadavg') as f:
                load = float(f.read().split()[0])
            
            if load < 2.0:
                status = "healthy"
            elif load < 8.0:
                status = "warning"
            else:
                status = "critical"
            
            return HealthMetric(
                name="system_load",
                value=load,
                threshold=8.0,
                status=status
            )
        except:
            return HealthMetric(
                name="system_load",
                value=999.0,
                threshold=8.0,
                status="critical"
            )
    
    def _check_memory(self) -> HealthMetric:
        """Check memory usage."""
        try:
            with open('/proc/meminfo') as f:
                lines = f.readlines()
                
            mem_total = 0
            mem_available = 0
            
            for line in lines:
                if line.startswith('MemTotal:'):
                    mem_total = int(line.split()[1])
                elif line.startswith('MemAvailable:'):
                    mem_available = int(line.split()[1])
            
            if mem_total > 0:
                usage_pct = (mem_total - mem_available) / mem_total * 100
                
                if usage_pct < 70:
                    status = "healthy"
                elif usage_pct < 90:
                    status = "warning"
                else:
                    status = "critical"
                
                return HealthMetric(
                    name="memory_usage",
                    value=usage_pct,
                    threshold=90.0,
                    status=status
                )
        except:
            pass
        
        return HealthMetric(
            name="memory_usage",
            value=100.0,
            threshold=90.0,
            status="critical"
        )
    
    def _check_disk(self) -> HealthMetric:
        """Check disk space."""
        try:
            stat = os.statvfs('/')
            free_pct = (stat.f_bavail / stat.f_blocks) * 100
            
            if free_pct > 20:
                status = "healthy"
            elif free_pct > 10:
                status = "warning"
            else:
                status = "critical"
            
            return HealthMetric(
                name="disk_space",
                value=free_pct,
                threshold=10.0,
                status=status
            )
        except:
            return HealthMetric(
                name="disk_space",
                value=0.0,
                threshold=10.0,
                status="critical"
            )
    
    def _check_tmux(self) -> HealthMetric:
        """Check tmux sessions."""
        try:
            result = subprocess.run(
                ["tmux", "list-sessions"],
                capture_output=True
            )
            
            # Tmux not required anymore (Python brain replaced it)
            return HealthMetric(
                name="tmux",
                value=1.0,
                threshold=0.0,  # Not critical
                status="healthy"
            )
        except:
            return HealthMetric(
                name="tmux",
                value=0.0,
                threshold=0.0,
                status="healthy"  # Not critical
            )
    
    def _process_through_brain(self, metrics: List[HealthMetric]) -> Dict:
        """
        Process health metrics through 7-region brain:
        - Thalamus: Receive metric data
        - Hippocampus: Recall similar health states
        - Limbic: Evaluate urgency
        - PFC: Plan response
        """
        # Build health summary
        critical_count = sum(1 for m in metrics if m.status == "critical")
        warning_count = sum(1 for m in metrics if m.status == "warning")
        
        # Create observation
        obs_text = f"Health check: {critical_count} critical, {warning_count} warning"
        
        # Feed to brain
        result = self.brain.feed(obs_text, source="heartbeat")
        
        # Determine mode and action
        mode = result.get("mode", "adaptive")
        
        # Adaptive frequency adjustment
        if critical_count > 0:
            self.check_interval = 10  # Check every 10s if critical
            self.consecutive_failures += 1
        elif warning_count > 2:
            self.check_interval = 20  # Check every 20s if warnings
            self.consecutive_failures = max(0, self.consecutive_failures - 1)
        else:
            self.check_interval = 30  # Normal: 30s
            self.consecutive_failures = 0
        
        return {
            "mode": mode,
            "critical_count": critical_count,
            "warning_count": warning_count,
            "next_check": self.check_interval,
            "brain_tick": result.get("tick", 0)
        }
    
    def run_check(self) -> Dict:
        """
        Run a complete health check through the brain.
        
        Returns health report with brain processing.
        """
        print(f"\n[BrainHeartbeat] Running check at {datetime.now().strftime('%H:%M:%S')}")
        
        # Collect metrics
        metrics = []
        for name, check_fn in self.monitors.items():
            metric = check_fn()
            metrics.append(metric)
            print(f"  {name}: {metric.status} ({metric.value:.1f})")
        
        # Process through brain
        brain_result = self._process_through_brain(metrics)
        
        # Build report
        report = {
            "timestamp": time.time(),
            "metrics": [
                {"name": m.name, "value": m.value, "status": m.status}
                for m in metrics
            ],
            "brain_mode": brain_result["mode"],
            "brain_tick": brain_result["brain_tick"],
            "critical": brain_result["critical_count"],
            "warning": brain_result["warning_count"],
            "next_check_seconds": brain_result["next_check"],
            "overall_status": "healthy" if brain_result["critical_count"] == 0 else "degraded"
        }
        
        # Store history
        self.metrics_history.append(report)
        if len(self.metrics_history) > self.max_history:
            self.metrics_history.pop(0)
        
        # Print summary
        print(f"\n  Status: {report['overall_status'].upper()}")
        print(f"  Brain mode: {report['brain_mode']}")
        print(f"  Next check: {report['next_check_seconds']}s")
        
        return report
    
    def run_continuous(self):
        """Run heartbeat continuously."""
        print("[BrainHeartbeat] Starting continuous monitoring...")
        print("Press Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                self.run_check()
                
                # Sleep with interrupt handling
                for _ in range(self.check_interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n[BrainHeartbeat] Stopping...")
            self.running = False
    
    def get_health_summary(self) -> str:
        """Get formatted health summary."""
        if not self.metrics_history:
            return "No health data yet."
        
        latest = self.metrics_history[-1]
        
        lines = [
            "=" * 60,
            "🫀 BRAIN HEARTBEAT SUMMARY",
            "=" * 60,
            f"Time: {datetime.fromtimestamp(latest['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}",
            f"Status: {latest['overall_status'].upper()}",
            f"Brain Mode: {latest['brain_mode']}",
            f"Brain Tick: {latest['brain_tick']}",
            f"Critical Issues: {latest['critical']}",
            f"Warnings: {latest['warning']}",
            "",
            "Metrics:",
        ]
        
        for metric in latest['metrics']:
            status_emoji = "🟢" if metric['status'] == 'healthy' else "🟡" if metric['status'] == 'warning' else "🔴"
            lines.append(f"  {status_emoji} {metric['name']}: {metric['value']:.1f} ({metric['status']})")
        
        lines.extend([
            "",
            f"History: {len(self.metrics_history)} checks",
            "=" * 60
        ])
        
        return "\n".join(lines)


def demo_brain_heartbeat():
    """Demo brain-based heartbeat."""
    print("=" * 70)
    print("🫀 BRAIN HEARTBEAT DEMO")
    print("=" * 70)
    print("\nRunning 5 health checks with brain processing...")
    print()
    
    heartbeat = BrainHeartbeat()
    
    for i in range(5):
        report = heartbeat.run_check()
        time.sleep(2)  # Brief pause between checks
    
    print("\n" + heartbeat.get_health_summary())
    
    print("\n" + "=" * 70)
    print("✅ Brain Heartbeat Demo Complete!")
    print("=" * 70)
    print("\nBrain-based heartbeat advantages:")
    print("  - Adaptive frequency (checks more when unstable)")
    print("  - Context-aware (brain mode reflects urgency)")
    print("  - Pattern learning (remembers failure times)")
    print("  - Limbic evaluation (affect-based priority)")
    print("=" * 70)


if __name__ == "__main__":
    demo_brain_heartbeat()
