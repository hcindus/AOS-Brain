#!/usr/bin/env python3
"""
Self-Improvement Module for AOS Brain
Autonomous gap-filling and capability enhancement
"""

import json
import time
import os
import sqlite3
from datetime import datetime

class SelfImprovementModule:
    """
    Monitors system gaps and proposes/implement improvements
    """
    
    def __init__(self, brain_state_path="~/.aos/brain/state/brain_state.json"):
        self.brain_state_path = os.path.expanduser(brain_state_path)
        self.improvements_db = os.path.expanduser("~/.aos/brain/state/improvements.db")
        self.gaps_identified = []
        self.improvements_made = []
        
        self._init_db()
        
    def _init_db(self):
        """Initialize improvements database"""
        os.makedirs(os.path.dirname(self.improvements_db), exist_ok=True)
        conn = sqlite3.connect(self.improvements_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS improvements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                gap_type TEXT,
                description TEXT,
                solution TEXT,
                implemented BOOLEAN,
                effectiveness REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                metric TEXT,
                value REAL,
                threshold REAL,
                status TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def scan_for_gaps(self):
        """Scan system for gaps and weaknesses"""
        gaps = []
        
        # Gap 1: Brain process monitoring
        if not self._check_brain_running():
            gaps.append({
                'type': 'reliability',
                'description': 'Brain process not auto-restarting on crash',
                'severity': 'high',
                'solution': 'Implement watchdog with auto-restart'
            })
        
        # Gap 2: Memory growth unchecked
        memory_count = self._get_memory_count()
        if memory_count > 10000:
            gaps.append({
                'type': 'performance',
                'description': f'Memory clusters ({memory_count}) exceeding optimal threshold',
                'severity': 'medium',
                'solution': 'Implement automatic memory compression/archival'
            })
        
        # Gap 3: No error prediction
        gaps.append({
            'type': 'prediction',
            'description': 'Reactive error handling, no predictive capability',
            'severity': 'medium',
            'solution': 'Implement trend analysis for early warning'
        })
        
        # Gap 4: Static thresholds
        gaps.append({
            'type': 'adaptation',
            'description': 'GrowingNN thresholds are static (0.8, 0.6)',
            'severity': 'low',
            'solution': 'Implement dynamic threshold adjustment based on performance'
        })
        
        # Gap 5: No self-modification
        gaps.append({
            'type': 'autonomy',
            'description': 'Cannot modify own code or configuration',
            'severity': 'high',
            'solution': 'Create safe self-modification framework with human approval'
        })
        
        self.gaps_identified = gaps
        return gaps
    
    def _check_brain_running(self):
        """Check if brain process is running"""
        import subprocess
        try:
            result = subprocess.run(['pgrep', '-f', 'brain.py'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _get_memory_count(self):
        """Get current memory count"""
        try:
            conn = sqlite3.connect(os.path.expanduser("~/.aos/memory/brain.db"))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memories")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def implement_improvement(self, gap):
        """Implement a specific improvement"""
        improvement = {
            'timestamp': time.time(),
            'gap_type': gap['type'],
            'description': gap['description'],
            'solution': gap['solution'],
            'implemented': True,
            'effectiveness': 0.0  # Will be measured
        }
        
        # Store in database
        conn = sqlite3.connect(self.improvements_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO improvements 
            (timestamp, gap_type, description, solution, implemented, effectiveness)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (improvement['timestamp'], improvement['gap_type'], 
              improvement['description'], improvement['solution'],
              improvement['implemented'], improvement['effectiveness']))
        conn.commit()
        conn.close()
        
        self.improvements_made.append(improvement)
        return improvement
    
    def generate_watchdog_script(self):
        """Generate auto-restart watchdog script"""
        script = '''#!/bin/bash
# AOS Brain Watchdog - Auto-restart on crash
# Generated by Self-Improvement Module

LOG_FILE="/root/.aos/logs/watchdog.log"
BRAIN_CHECK_INTERVAL=30

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

log "Watchdog started"

while true; do
    if ! pgrep -f "brain.py" > /dev/null; then
        log "⚠️ Brain not running! Restarting..."
        
        # Restart brain
        tmux new-session -d -s aos-brain \
            "cd /root/.openclaw/workspace/AOS/brain && python3 brain.py 2>&1 | tee ~/.aos/logs/brain.log"
        
        sleep 5
        
        if pgrep -f "brain.py" > /dev/null; then
            log "✅ Brain restarted successfully"
        else
            log "❌ Failed to restart brain"
        fi
    fi
    
    sleep $BRAIN_CHECK_INTERVAL
done
'''
        
        script_path = os.path.expanduser("~/.aos/scripts/watchdog.sh")
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        
        with open(script_path, 'w') as f:
            f.write(script)
        
        os.chmod(script_path, 0o755)
        return script_path
    
    def generate_improvement_report(self):
        """Generate report of improvements"""
        report = {
            'timestamp': time.time(),
            'gaps_identified': len(self.gaps_identified),
            'improvements_made': len(self.improvements_made),
            'gaps': self.gaps_identified,
            'improvements': self.improvements_made
        }
        
        return report
    
    def run_self_improvement(self):
        """Main self-improvement loop"""
        print("🔧 Starting Self-Improvement Module...")
        
        # Scan for gaps
        gaps = self.scan_for_gaps()
        print(f"📊 Found {len(gaps)} gaps:")
        for i, gap in enumerate(gaps, 1):
            print(f"   {i}. [{gap['severity'].upper()}] {gap['type']}: {gap['description'][:50]}...")
        
        # Implement high-priority improvements
        high_priority = [g for g in gaps if g['severity'] == 'high']
        print(f"\n🔨 Implementing {len(high_priority)} high-priority improvements...")
        
        for gap in high_priority:
            if gap['type'] == 'reliability':
                script_path = self.generate_watchdog_script()
                self.implement_improvement(gap)
                print(f"   ✅ Created watchdog: {script_path}")
            
            elif gap['type'] == 'autonomy':
                # Document the gap, but don't implement yet (needs approval)
                print(f"   ⏸️  {gap['type']}: Requires human approval for self-modification")
        
        # Generate report
        report = self.generate_improvement_report()
        
        print(f"\n📈 Self-Improvement Complete:")
        print(f"   Gaps identified: {report['gaps_identified']}")
        print(f"   Improvements made: {report['improvements_made']}")
        
        return report

if __name__ == "__main__":
    sim = SelfImprovementModule()
    sim.run_self_improvement()
