#!/usr/bin/env python3
"""
DAILY HEALTH SUMMARY v1.0
Collects and reports system health trends over time.

Usage:
    python3 daily_health_summary.py              # Generate today's summary
    python3 daily_health_summary.py --trend 7    # Show 7-day trend
    python3 daily_health_summary.py --report     # Full report with charts
"""

import json
import sqlite3
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Database location
DB_PATH = Path("/var/log/aos/health_trends.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

class HealthMonitor:
    """System health monitoring and trending."""
    
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database for health tracking."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                date TEXT NOT NULL,
                brain_status TEXT,
                brain_uptime TEXT,
                bhsi_status TEXT,
                bhsi_uptime TEXT,
                mission_control TEXT,
                roblox_bridge TEXT,
                minecraft_status TEXT,
                minecraft_memory TEXT,
                system_memory_percent INTEGER,
                disk_percent INTEGER,
                mortimer_status TEXT,
                active_agents INTEGER,
                notes TEXT
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_date ON health_checks(date)
        """)
        
        conn.commit()
        conn.close()
    
    def collect_current_health(self) -> Dict:
        """Run health check and parse results."""
        try:
            result = subprocess.run(
                ["bash", "/root/.openclaw/workspace/scripts/agent_keepalive.sh", "--no-restart"],
                capture_output=True,
                text=True,
                timeout=60
            )
            return self._parse_health_output(result.stdout)
        except Exception as e:
            return {"error": str(e)}
    
    def _parse_health_output(self, output: str) -> Dict:
        """Parse health check script output."""
        data = {
            "timestamp": datetime.utcnow().isoformat(),
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
        }
        
        for line in output.split('\n'):
            line = line.strip()
            
            if 'Brain v4' in line and 'MONITORED' in line:
                data['brain_status'] = 'RUNNING'
                # Extract uptime
                if 'uptime:' in line:
                    parts = line.split('uptime:')
                    if len(parts) > 1:
                        data['brain_uptime'] = parts[1].strip()
            
            elif 'BHSI v4' in line and 'MONITORED' in line:
                data['bhsi_status'] = 'RUNNING'
                if 'uptime:' in line:
                    parts = line.split('uptime:')
                    if len(parts) > 1:
                        data['bhsi_uptime'] = parts[1].strip()
            
            elif 'Mission Control' in line:
                data['mission_control'] = 'RUNNING' if 'RUNNING' in line else 'OFFLINE'
            
            elif 'Roblox Bridge' in line:
                data['roblox_bridge'] = 'RUNNING' if 'RUNNING' in line else 'OFFLINE'
            
            elif 'Minecraft Server' in line:
                data['minecraft_status'] = 'RUNNING' if 'RUNNING' in line else 'OFFLINE'
                if 'Memory:' in line:
                    mem_part = line.split('Memory:')[1].split('-')[0].strip()
                    data['minecraft_memory'] = mem_part
            
            elif 'System Memory:' in line:
                try:
                    mem_str = line.split(':')[1].split('%')[0].strip()
                    data['system_memory_percent'] = int(mem_str)
                except:
                    pass
            
            elif 'Disk Space:' in line:
                try:
                    disk_str = line.split(':')[1].split('%')[0].strip()
                    data['disk_percent'] = int(disk_str)
                except:
                    pass
            
            elif 'Mortimer' in line:
                data['mortimer_status'] = 'RESPONSIVE' if 'RESPONSIVE' in line else 'OFFLINE'
            
            elif 'Agent Service:' in line and 'ACTIVE' in line:
                data['active_agents'] = data.get('active_agents', 0) + 1
        
        return data
    
    def save_health_check(self, data: Dict):
        """Save health check to database."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO health_checks (
                timestamp, date, brain_status, brain_uptime, bhsi_status, bhsi_uptime,
                mission_control, roblox_bridge, minecraft_status, minecraft_memory,
                system_memory_percent, disk_percent, mortimer_status, active_agents, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('timestamp'),
            data.get('date'),
            data.get('brain_status'),
            data.get('brain_uptime'),
            data.get('bhsi_status'),
            data.get('bhsi_uptime'),
            data.get('mission_control'),
            data.get('roblox_bridge'),
            data.get('minecraft_status'),
            data.get('minecraft_memory'),
            data.get('system_memory_percent'),
            data.get('disk_percent'),
            data.get('mortimer_status'),
            data.get('active_agents', 0),
            data.get('notes', '')
        ))
        
        conn.commit()
        conn.close()
    
    def get_daily_summary(self, days: int = 1) -> List[Dict]:
        """Get daily summary for past N days."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        since = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        cursor.execute("""
            SELECT 
                date,
                COUNT(*) as checks,
                AVG(system_memory_percent) as avg_memory,
                MAX(system_memory_percent) as max_memory,
                MIN(system_memory_percent) as min_memory,
                AVG(disk_percent) as avg_disk,
                MAX(active_agents) as max_agents,
                GROUP_CONCAT(DISTINCT brain_status) as brain_statuses,
                GROUP_CONCAT(DISTINCT mortimer_status) as mortimer_statuses
            FROM health_checks
            WHERE date >= ?
            GROUP BY date
            ORDER BY date DESC
        """, (since,))
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = ['date', 'checks', 'avg_memory', 'max_memory', 'min_memory', 
                   'avg_disk', 'max_agents', 'brain_statuses', 'mortimer_statuses']
        
        return [dict(zip(columns, row)) for row in rows]
    
    def generate_summary_table(self, days: int = 7) -> str:
        """Generate ASCII table of health trends."""
        data = self.get_daily_summary(days)
        
        if not data:
            return "No health data available. Run health checks first."
        
        lines = []
        lines.append("=" * 100)
        lines.append("📊 SYSTEM HEALTH TRENDS - Last {} Days".format(days))
        lines.append("=" * 100)
        lines.append("")
        
        # Header
        header = f"{'Date':<12} {'Checks':<8} {'Avg Mem':<10} {'Max Mem':<10} {'Min Mem':<10} {'Disk':<8} {'Agents':<8} {'Brain':<12} {'Mortimer':<12}"
        lines.append(header)
        lines.append("-" * 100)
        
        # Data rows
        for row in data:
            date_str = row['date']
            checks = row['checks']
            avg_mem = f"{row['avg_memory']:.1f}%" if row['avg_memory'] else "N/A"
            max_mem = f"{row['max_memory']:.0f}%" if row['max_memory'] else "N/A"
            min_mem = f"{row['min_memory']:.0f}%" if row['min_memory'] else "N/A"
            disk = f"{row['avg_disk']:.0f}%" if row['avg_disk'] else "N/A"
            agents = str(row['max_agents']) if row['max_agents'] else "0"
            brain = row['brain_statuses'] if row['brain_statuses'] else "N/A"
            mortimer = row['mortimer_statuses'] if row['mortimer_statuses'] else "N/A"
            
            lines.append(f"{date_str:<12} {checks:<8} {avg_mem:<10} {max_mem:<10} {min_mem:<10} {disk:<8} {agents:<8} {brain:<12} {mortimer:<12}")
        
        lines.append("-" * 100)
        
        # Summary stats
        if data:
            all_mem = [r['avg_memory'] for r in data if r['avg_memory']]
            if all_mem:
                lines.append(f"")
                lines.append(f"📈 MEMORY TREND: Avg {sum(all_mem)/len(all_mem):.1f}% | Range {min(all_mem):.0f}% - {max(all_mem):.0f}%")
        
        lines.append("")
        lines.append("Legend: Brain/Mortimer status shows all unique states recorded that day")
        lines.append("=" * 100)
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Daily Health Summary')
    parser.add_argument('--trend', type=int, default=7, help='Show trend for N days')
    parser.add_argument('--collect', action='store_true', help='Collect current health check')
    parser.add_argument('--report', action='store_true', help='Generate full report')
    
    args = parser.parse_args()
    
    monitor = HealthMonitor()
    
    if args.collect:
        print("Collecting health data...")
        data = monitor.collect_current_health()
        monitor.save_health_check(data)
        print(f"✅ Saved health check for {data.get('date', 'today')}")
    
    elif args.report:
        # Collect current first
        data = monitor.collect_current_health()
        monitor.save_health_check(data)
        # Then show summary
        print(monitor.generate_summary_table(args.trend))
    
    else:
        # Default: collect and show summary
        data = monitor.collect_current_health()
        monitor.save_health_check(data)
        print(monitor.generate_summary_table(args.trend))


if __name__ == "__main__":
    main()
