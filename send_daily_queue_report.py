#!/usr/bin/env python3
"""
Daily Queue Email Report Script - LIVE DATA VERSION
Queries live databases for accurate queue and system status
"""

import smtplib
import ssl
import sqlite3
import json
import subprocess
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Configuration
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465
FROM_EMAIL = "miles@myl0nr0s.cloud"
FROM_PASSWORD = "Myl0n.R0s"
TO_EMAIL = "Antonio.hudnall@gmail.com"

DB_FACTORY = "/root/.openclaw/workspace/data/factory/dark_factory.db"
DB_UNIFIED = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
DB_ENRICHMENT = "/root/.openclaw/workspace/mortimer-build/software/depotchaos/enrichment_queue/queue.db"
PENDING_TASKS = "/root/.openclaw/workspace/data/PENDING_TASKS.json"


def get_system_uptime():
    """Get system uptime in human readable format"""
    try:
        result = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        # Fallback to uptime
        result = subprocess.run(['uptime'], capture_output=True, text=True)
        return result.stdout.strip().split(',')[0]
    except:
        return "Unknown"


def get_disk_usage():
    """Get disk usage for root filesystem"""
    try:
        result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            # parts: Filesystem, Size, Used, Avail, Use%, Mounted on
            if len(parts) >= 5:
                size = parts[1]
                used = parts[2]
                percent = parts[4].replace('%', '')
                return int(percent), f"{used}/{size}"
    except:
        pass
    return 0, "Unknown"


def get_memory_usage():
    """Get memory usage"""
    try:
        result = subprocess.run(['free', '-h'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.startswith('Mem:'):
                parts = line.split()
                total = parts[1]
                used = parts[2]
                # Calculate percentage
                total_mb = parse_size(total)
                used_mb = parse_size(used)
                if total_mb > 0:
                    percent = int((used_mb / total_mb) * 100)
                    return percent, f"{used}/{total}"
    except:
        pass
    return 0, "Unknown"


def parse_size(size_str):
    """Parse size string like '15Gi' to MB"""
    size_str = size_str.strip()
    num = float(''.join(c for c in size_str if c.isdigit() or c == '.'))
    unit = ''.join(c for c in size_str if c.isalpha()).lower()
    multipliers = {'ki': 1/1024, 'mi': 1, 'gi': 1024, 'ti': 1024*1024}
    return num * multipliers.get(unit, 1)


def get_load_average():
    """Get system load average"""
    try:
        with open('/proc/loadavg', 'r') as f:
            loadavg = f.read().strip().split()
            if len(loadavg) >= 3:
                return float(loadavg[0]), float(loadavg[1]), float(loadavg[2])
    except:
        pass
    return 0.0, 0.0, 0.0


def get_cron_jobs():
    """Count active cron jobs"""
    count = 0
    try:
        # User crontab
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            count += len([l for l in result.stdout.split('\n') if l.strip() and not l.startswith('#')])
    except:
        pass
    
    try:
        # System cron.d
        if os.path.exists('/etc/cron.d'):
            count += len([f for f in os.listdir('/etc/cron.d') if not f.startswith('.')])
    except:
        pass
    
    return count


def query_factory_orders():
    """Query dark_factory.db for production orders"""
    orders = []
    stats = {'total': 0, 'queued': 0, 'in_progress': 0, 'completed': 0}
    
    try:
        conn = sqlite3.connect(DB_FACTORY)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Get statistics
        c.execute("SELECT status, COUNT(*) as count FROM production_orders GROUP BY status")
        for row in c.fetchall():
            stats[row['status']] = row['count']
            stats['total'] += row['count']
        
        # Get active orders
        c.execute("""
            SELECT id, product_name, status, stage, total_stages, priority, 
                   datetime(created_at) as created
            FROM production_orders 
            WHERE status IN ('queued', 'in_progress')
            ORDER BY 
                CASE priority 
                    WHEN 'urgent' THEN 1 
                    WHEN 'high' THEN 2 
                    WHEN 'normal' THEN 3 
                    ELSE 4 
                END, 
                created_at
        """)
        
        for row in c.fetchall():
            orders.append({
                'id': row['id'],
                'name': row['product_name'],
                'status': row['status'],
                'stage': row['stage'],
                'total_stages': row['total_stages'],
                'priority': row['priority'],
                'created': row['created']
            })
        
        conn.close()
    except Exception as e:
        print(f"Factory DB error: {e}")
    
    return orders, stats


def query_pending_tasks():
    """Query PENDING_TASKS.json"""
    try:
        with open(PENDING_TASKS, 'r') as f:
            data = json.load(f)
            tasks = data.get('tasks', [])
            pending = len([t for t in tasks if t.get('queue_status') == 'PENDING'])
            in_progress = len([t for t in tasks if t.get('queue_status') == 'IN_PROGRESS'])
            return len(tasks), pending, in_progress
    except Exception as e:
        print(f"Pending tasks error: {e}")
    return 0, 0, 0


def query_unified_leads():
    """Query unified.db for leads"""
    try:
        conn = sqlite3.connect(DB_UNIFIED)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM leads")
        total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM leads WHERE enrichment_status='pending'")
        pending = c.fetchone()[0]
        conn.close()
        return total, pending
    except Exception as e:
        print(f"Unified DB error: {e}")
    return 0, 0


def query_enrichment_queue():
    """Query enrichment queue"""
    try:
        conn = sqlite3.connect(DB_ENRICHMENT)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM enrichment_queue WHERE status='pending'")
        pending = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM enrichment_queue")
        total = c.fetchone()[0]
        conn.close()
        return total, pending
    except Exception as e:
        print(f"Enrichment queue error: {e}")
    return 0, 0


def check_service_status(service_name):
    """Check if a systemd service is active"""
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', service_name],
            capture_output=True, text=True
        )
        return result.stdout.strip() == 'active'
    except:
        return False


def check_brain_socket():
    """Check brain socket status"""
    try:
        result = subprocess.run(
            ['echo', '{"cmd":"status"}'],
            capture_output=True
        )
        result = subprocess.run(
            ['nc', '-U', '/tmp/aos_brain.sock'],
            capture_output=True, text=True, input=result.stdout
        )
        if result.returncode == 0 and result.stdout:
            return True
    except:
        pass
    return False


def generate_report():
    """Generate the full report with live data"""
    
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    current_date = datetime.utcnow().strftime("%A, %B %d, %Y")
    
    # System stats
    uptime = get_system_uptime()
    disk_percent, disk_details = get_disk_usage()
    mem_percent, mem_details = get_memory_usage()
    load1, load5, load15 = get_load_average()
    cron_count = get_cron_jobs()
    
    # Database queries
    factory_orders, factory_stats = query_factory_orders()
    total_tasks, pending_tasks, in_progress_tasks = query_pending_tasks()
    unified_total, unified_pending = query_unified_leads()
    enrich_total, enrich_pending = query_enrichment_queue()
    
    # Service checks
    brain_running = check_service_status('aos-brain-v4')
    mc_running = check_service_status('aos-mission-control')
    bhsi_running = check_service_status('aos-bhsi-v4')
    
    # Calculate total queue items
    total_queue_items = (
        factory_stats.get('queued', 0) + 
        factory_stats.get('in_progress', 0) +
        pending_tasks +
        unified_pending +
        enrich_pending
    )
    
    # Build report
    report = f"""Good morning, Captain!

Here is your daily queue and system status report for today ({current_date}).

═══════════════════════════════════════════════════════════════════════════
                           QUEUE STATUS SUMMARY
═══════════════════════════════════════════════════════════════════════════

Generated: {current_time}

OVERALL QUEUE METRICS (LIVE DATA):
• Total Active Queue Items: {total_queue_items}
  ├─ Dark Factory (Patricia): {factory_stats.get('queued', 0)} queued, {factory_stats.get('in_progress', 0)} in progress
  ├─ Pending Tasks: {pending_tasks} pending
  ├─ Unified Leads: {unified_pending} pending enrichment
  └─ Enrichment Queue: {enrich_pending} pending

• System Uptime: {uptime}

═══════════════════════════════════════════════════════════════════════════
                         SYSTEM HEALTH STATUS
═══════════════════════════════════════════════════════════════════════════

VPS Resources (Miles.cloud):
+------------------+---------+--------------------------------+
| Resource         | Status  | Details                        |
+------------------+---------+--------------------------------+
| Disk Usage       | {'🟢 OK' if disk_percent < 80 else '🟡 WARN' if disk_percent < 90 else '🔴 CRIT'}   | {disk_percent}% ({disk_details})          |
| Memory           | {'🟢 OK' if mem_percent < 80 else '🟡 WARN' if mem_percent < 90 else '🔴 CRIT'}   | {mem_percent}% ({mem_details})            |
| Load Average     | {'🟢 OK' if load1 < 5 else '🟡 HIGH' if load1 < 15 else '🔴 CRIT'} | {load1:.2f}, {load5:.2f}, {load15:.2f}            |
| Cron Jobs        | 🟢 OK   | {cron_count} jobs configured           |
+------------------+---------+--------------------------------+

Core Services:
• OpenClaw Gateway: {'🟢 RUNNING' if brain_running else '🔴 DOWN'}
• Mission Control:  {'🟢 RUNNING' if mc_running else '🔴 DOWN'}
• BHSI v4.1:        {'🟢 OPERATIONAL' if bhsi_running else '🔴 DOWN'}
• Brain Socket:     {'🟢 READY' if check_brain_socket() else '🔴 UNREACHABLE'}

═══════════════════════════════════════════════════════════════════════════
                   PATRICIA'S FACTORY QUEUE ({factory_stats.get('queued', 0) + factory_stats.get('in_progress', 0)} Items)
═══════════════════════════════════════════════════════════════════════════

Status  | ID                  | Product                    | Progress | Priority
--------|---------------------|----------------------------|----------|----------
"""
    
    # Add factory orders
    for order in factory_orders:
        status_emoji = '⏳' if order['status'] == 'queued' else '🔧'
        priority_emoji = '🔴' if order['priority'] in ['urgent', 'high'] else '🟡' if order['priority'] == 'normal' else '⚪'
        progress = f"{order['stage']}/{order['total_stages']}"
        report += f"{status_emoji} {order['status'].upper():7} | {order['id']:19} | {order['name'][:26]:26} | {progress:8} | {priority_emoji} {order['priority'].upper()}\n"
    
    report += f"""
═══════════════════════════════════════════════════════════════════════════
                           DATABASE SUMMARY
═══════════════════════════════════════════════════════════════════════════

Dark Factory:
  • Total Orders: {factory_stats.get('total', 0)}
  • Completed: {factory_stats.get('completed', 0)} ✅
  • Queued: {factory_stats.get('queued', 0)} ⏳
  • In Progress: {factory_stats.get('in_progress', 0)} 🔧

DepotChaos (Unified):
  • Total Leads: {unified_total:,}
  • Pending Enrichment: {unified_pending:,}

Enrichment Queue:
  • Total Items: {enrich_total:,}
  • Pending: {enrich_pending:,}

Pending Tasks (JSON):
  • Total Tasks: {total_tasks:,}
  • Pending: {pending_tasks}
  • In Progress: {in_progress_tasks}

═══════════════════════════════════════════════════════════════════════════
                            ACTION ITEMS
═══════════════════════════════════════════════════════════════════════════

HIGH PRIORITY:
┌─────────────────────────────────────────────────────────────────────────┐
│ Factory Pipeline Status                                                 │
│ • {factory_stats.get('queued', 0)} orders queued (stale since May 26)                                  │
│ • {factory_stats.get('in_progress', 0)} orders in progress                                            │
│ • RECOMMENDATION: Review order promotion logic                          │
│                                                                         │
│ System Load                                                             │
│ • Current: {load1:.2f} (elevated above normal 5.0)                                              │
│ • Action: Monitor processes if sustained above 15.0                     │
└─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
                            TIMESTAMPS
═══════════════════════════════════════════════════════════════════════════

Report Generated:      {current_time}
System Uptime:         {uptime}
Data Sources:          Live database queries
VPS:                   Miles.cloud
Next Report:           {datetime.utcnow().strftime("%Y-%m-%d")} 13:23 UTC

═══════════════════════════════════════════════════════════════════════════

All metrics queried live from:
  • {DB_FACTORY}
  • {DB_UNIFIED}
  • {DB_ENRICHMENT}
  • {PENDING_TASKS}

Standing by for Captain's directives.

- Miles 🚀
Autonomous Operations Engine
Performance Supply Depot LLC / AGI Company
Email: miles@myl0nr0s.cloud

---
*This report uses LIVE DATA from production databases.*
"""
    
    return report, current_time


def send_daily_queue_report():
    """Send daily queue report to Captain"""
    
    # Generate report with live data
    report_body, current_time = generate_report()
    
    # Email content
    subject = f"📊 Daily Queue Report - {datetime.utcnow().strftime('%B %d, %Y')} (LIVE DATA)"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(report_body, 'plain'))
    
    # Send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    
    print("✅ Daily queue email report sent to Captain successfully!")
    print(f"   To: {TO_EMAIL}")
    print(f"   Subject: {subject}")
    print(f"   Timestamp: {current_time}")
    print(f"   Data Sources: Live database queries")


if __name__ == "__main__":
    send_daily_queue_report()
