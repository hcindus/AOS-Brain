#!/usr/bin/env python3
"""
AOS SECURITY MONITOR v1.0
Continuous monitoring and alerting for brain security

Patricia's recommendations implemented:
- Real-time violation pattern detection
- Threshold-based alerting
- Automated response triggers
- Metrics dashboard
"""

import time
import json
import socket
import threading
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from collections import defaultdict
import statistics


@dataclass
class Alert:
    """Security alert structure"""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # ATTACK_PATTERN, ANOMALY, THRESHOLD
    description: str
    timestamp: float
    data: dict


class SecurityMonitor:
    """
    Continuous security monitoring for AOS Brain
    
    Monitors:
    - Violation patterns (attack signatures)
    - Rate anomalies (unusual traffic)
    - Threat actor tracking (repeat offenders)
    - System health (response times, error rates)
    """
    
    def __init__(self, brain_socket_path='/tmp/aos_brain.sock'):
        self.socket_path = brain_socket_path
        self.running = False
        self.monitor_thread = None
        
        # Alert thresholds (Patricia's CONTROL metrics)
        self.thresholds = {
            'violations_per_minute': 10,
            'blocked_per_minute': 5,
            'new_connections_per_minute': 20,
            'response_time_ms': 100,
            'error_rate_percent': 5
        }
        
        # Alert handlers
        self.alert_handlers: List[Callable[[Alert], None]] = []
        self.alerts: List[Alert] = []
        self.max_alerts = 1000
        
        # Pattern tracking
        self.violation_history: List[Dict] = []
        self.connection_history: List[Dict] = []
        self.threat_actors: Dict[str, Dict] = defaultdict(lambda: {
            'first_seen': time.time(),
            'violation_count': 0,
            'last_violation': 0,
            'patterns': set()
        })
        
        # Metrics
        self.metrics = {
            'total_checks': 0,
            'alerts_triggered': 0,
            'avg_response_time_ms': 0
        }
        
        print("[Security Monitor v1.0] Initialized")
        print(f"  Socket: {self.socket_path}")
        print(f"  Check interval: 30s")
    
    def add_alert_handler(self, handler: Callable[[Alert], None]):
        """Add a handler for security alerts"""
        self.alert_handlers.append(handler)
    
    def start(self):
        """Start monitoring"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("[Security Monitor] Started")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        print("[Security Monitor] Stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                start_time = time.time()
                self._check_security_status()
                self._check_patterns()
                self._check_anomalies()
                
                elapsed_ms = (time.time() - start_time) * 1000
                self.metrics['avg_response_time_ms'] = (
                    self.metrics['avg_response_time_ms'] * 0.9 + elapsed_ms * 0.1
                )
                
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"[Security Monitor] Error: {e}")
                time.sleep(5)
    
    def _get_brain_status(self) -> Optional[Dict]:
        """Query brain security status via socket"""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(self.socket_path)
            sock.sendall(json.dumps({'cmd': 'security'}).encode() + b'\n')
            
            response = b''
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            sock.close()
            return json.loads(response.decode())
        except Exception as e:
            return None
    
    def _check_security_status(self):
        """Check current security status from brain"""
        status = self._get_brain_status()
        if not status:
            self._trigger_alert(
                severity='CRITICAL',
                category='SYSTEM',
                description='Cannot reach brain security endpoint',
                data={'socket': self.socket_path}
            )
            return
        
        # Update metrics
        self.metrics['total_checks'] += 1
        
        # Check violation rate
        recent_violations = status.get('recent_violations', 0)
        if recent_violations > self.thresholds['violations_per_minute']:
            self._trigger_alert(
                severity='HIGH',
                category='THRESHOLD',
                description=f'High violation rate: {recent_violations}/min',
                data={'threshold': self.thresholds['violations_per_minute'], 'actual': recent_violations}
            )
        
        # Check blocked connections
        blocked = status.get('blocked_connections', 0)
        if blocked > self.thresholds['blocked_per_minute']:
            self._trigger_alert(
                severity='MEDIUM',
                category='THRESHOLD',
                description=f'High block rate: {blocked} connections',
                data={'threshold': self.thresholds['blocked_per_minute'], 'actual': blocked}
            )
    
    def _check_patterns(self):
        """Detect attack patterns in audit log"""
        # Pattern: Rapid-fire violations from same source
        now = time.time()
        recent = [v for v in self.violation_history if now - v['timestamp'] < 60]
        
        # Group by client
        by_client = defaultdict(list)
        for v in recent:
            by_client[v.get('client', 'unknown')].append(v)
        
        for client, violations in by_client.items():
            if len(violations) >= 5:  # 5+ violations in 1 minute
                self.threat_actors[client]['violation_count'] += len(violations)
                self.threat_actors[client]['last_violation'] = now
                for v in violations:
                    self.threat_actors[client]['patterns'].add(v.get('violation', 'unknown'))
                
                self._trigger_alert(
                    severity='HIGH',
                    category='ATTACK_PATTERN',
                    description=f'Rapid violations from {client[:8]}: {len(violations)}/min',
                    data={
                        'client': client[:16],
                        'patterns': list(self.threat_actors[client]['patterns'])[:5],
                        'total_violations': self.threat_actors[client]['violation_count']
                    }
                )
    
    def _check_anomalies(self):
        """Detect statistical anomalies"""
        now = time.time()
        
        # Check connection rate anomaly
        recent_connections = [
            c for c in self.connection_history
            if now - c.get('timestamp', 0) < 60
        ]
        
        if len(recent_connections) > self.thresholds['new_connections_per_minute']:
            self._trigger_alert(
                severity='MEDIUM',
                category='ANOMALY',
                description=f'Unusual connection rate: {len(recent_connections)}/min',
                data={'threshold': self.thresholds['new_connections_per_minute']}
            )
    
    def _trigger_alert(self, severity: str, category: str, description: str, data: dict):
        """Trigger security alert"""
        alert = Alert(
            severity=severity,
            category=category,
            description=description,
            timestamp=time.time(),
            data=data
        )
        
        self.alerts.append(alert)
        if len(self.alerts) > self.max_alerts:
            self.alerts = self.alerts[-self.max_alerts:]
        
        self.metrics['alerts_triggered'] += 1
        
        # Call handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"[Security Monitor] Alert handler error: {e}")
        
        # Console output for critical/high
        if severity in ['CRITICAL', 'HIGH']:
            print(f"\n🚨 SECURITY ALERT [{severity}] {category}")
            print(f"   {description}")
            print(f"   Time: {time.strftime('%H:%M:%S', time.localtime(alert.timestamp))}")
    
    def record_violation(self, client: str, violation_type: str):
        """Record a violation for pattern analysis"""
        self.violation_history.append({
            'client': client,
            'violation': violation_type,
            'timestamp': time.time()
        })
        
        # Keep last 1000
        if len(self.violation_history) > 1000:
            self.violation_history = self.violation_history[-1000:]
    
    def record_connection(self, client: str):
        """Record a new connection"""
        self.connection_history.append({
            'client': client,
            'timestamp': time.time()
        })
        
        # Keep last 1000
        if len(self.connection_history) > 1000:
            self.connection_history = self.connection_history[-1000:]
    
    def get_dashboard(self) -> Dict:
        """Get security dashboard data"""
        now = time.time()
        
        # Calculate stats
        recent_alerts = [a for a in self.alerts if now - a.timestamp < 3600]
        recent_violations = [v for v in self.violation_history if now - v['timestamp'] < 3600]
        
        top_threats = sorted(
            self.threat_actors.items(),
            key=lambda x: x[1]['violation_count'],
            reverse=True
        )[:5]
        
        return {
            'status': 'ACTIVE' if self.running else 'STOPPED',
            'metrics': self.metrics,
            'last_hour': {
                'alerts': len(recent_alerts),
                'violations': len(recent_violations),
                'unique_threat_actors': len(top_threats)
            },
            'top_threats': [
                {
                    'client': t[0][:16],
                    'violations': t[1]['violation_count'],
                    'patterns': list(t[1]['patterns'])[:3]
                }
                for t in top_threats
            ],
            'recent_alerts': [
                {
                    'severity': a.severity,
                    'category': a.category,
                    'description': a.description[:60],
                    'time': time.strftime('%H:%M:%S', time.localtime(a.timestamp))
                }
                for a in self.alerts[-10:]
            ]
        }


def console_alert_handler(alert: Alert):
    """Simple console alert handler"""
    icon = {
        'CRITICAL': '🔴',
        'HIGH': '🟠',
        'MEDIUM': '🟡',
        'LOW': '🟢'
    }.get(alert.severity, '⚪')
    
    print(f"{icon} [{alert.severity}] {alert.category}: {alert.description[:80]}")


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("  🔒 SECURITY MONITOR v1.0 - Test Mode")
    print("=" * 70)
    
    monitor = SecurityMonitor()
    monitor.add_alert_handler(console_alert_handler)
    
    # Simulate some violations
    print("\nSimulating violations...")
    for i in range(7):
        monitor.record_violation(f"attacker_1", "SQL_INJECTION")
    
    # Check patterns
    monitor._check_patterns()
    
    # Show dashboard
    print("\n" + "=" * 70)
    print("  Security Dashboard:")
    dashboard = monitor.get_dashboard()
    for key, value in dashboard.items():
        print(f"    {key}: {value}")
    print("=" * 70)
