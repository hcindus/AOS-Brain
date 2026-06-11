#!/usr/bin/env python3
"""
Daily Queue Report Emailer
Sends Patricia's complete work queue status to Captain
"""

import sqlite3
import json
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Configuration
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
FROM_EMAIL = "miles@myl0nr0s.cloud"
FROM_PASSWORD = "Myl0n.R0s"
TO_EMAIL = "antonio.hudnall@gmail.com"
DB_PATH = "/root/.openclaw/workspace/data/factory/dark_factory.db"


class DailyQueueReporter:
    """Generates and sends daily queue reports"""
    
    def __init__(self):
        self.timestamp = datetime.utcnow()
        self.report_date = self.timestamp.strftime("%Y-%m-%d")
        self.report_time = self.timestamp.strftime("%H:%M UTC")
    
    def get_queue_statistics(self):
        """Get queue statistics from database"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        stats = {}
        
        # Overall counts
        c.execute("SELECT status, COUNT(*) as count FROM production_orders GROUP BY status")
        stats['by_status'] = {row['status']: row['count'] for row in c.fetchall()}
        
        # Priority breakdown
        c.execute("SELECT status, priority, COUNT(*) as count FROM production_orders GROUP BY status, priority")
        stats['by_priority'] = {}
        for row in c.fetchall():
            status = row['status']
            if status not in stats['by_priority']:
                stats['by_priority'][status] = {}
            stats['by_priority'][status][row['priority']] = row['count']
        
        # Recent activity (last 7 days)
        c.execute('''
            SELECT COUNT(*) as count FROM production_orders 
            WHERE created_at >= datetime('now', '-7 days')
        ''')
        stats['recent_created'] = c.fetchone()['count']
        
        c.execute('''
            SELECT COUNT(*) as count FROM production_orders 
            WHERE completed_at >= datetime('now', '-7 days')
        ''')
        stats['recent_completed'] = c.fetchone()['count'] or 0
        
        conn.close()
        return stats
    
    def get_active_orders(self, status_filter=None, limit=20):
        """Get active orders"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        if status_filter:
            c.execute('''
                SELECT id, product_name, status, stage, total_stages, priority,
                       datetime(created_at) as created, metadata
                FROM production_orders
                WHERE status = ?
                ORDER BY CASE priority 
                    WHEN 'urgent' THEN 1 
                    WHEN 'high' THEN 2 
                    WHEN 'normal' THEN 3 
                    ELSE 4 
                END, created_at DESC
                LIMIT ?
            ''', (status_filter, limit))
        else:
            c.execute('''
                SELECT id, product_name, status, stage, total_stages, priority,
                       datetime(created_at) as created, metadata
                FROM production_orders
                WHERE status != 'completed'
                ORDER BY CASE priority 
                    WHEN 'urgent' THEN 1 
                    WHEN 'high' THEN 2 
                    WHEN 'normal' THEN 3 
                    ELSE 4 
                END, created_at DESC
                LIMIT ?
            ''', (limit,))
        
        orders = []
        for row in c.fetchall():
            meta = json.loads(row['metadata']) if row['metadata'] else {}
            orders.append({
                'id': row['id'],
                'product': row['product_name'],
                'status': row['status'],
                'stage': row['stage'],
                'total_stages': row['total_stages'] or 10,
                'priority': row['priority'],
                'created': row['created'],
                'client': meta.get('client', 'AGI Company'),
                'progress': f"{row['stage']}/{row['total_stages'] or 10}"
            })
        
        conn.close()
        return orders
    
    def generate_report(self):
        """Generate the daily queue report"""
        stats = self.get_queue_statistics()
        active_orders = self.get_active_orders(limit=15)
        
        total_orders = sum(stats['by_status'].values())
        completed = stats['by_status'].get('completed', 0)
        active = total_orders - completed
        queued = stats['by_status'].get('queued', 0)
        in_progress = stats['by_status'].get('in_progress', 0)
        
        # Priority emoji mapping
        priority_emojis = {
            'urgent': '🚨',
            'high': '🔴',
            'normal': '🟡',
            'low': '🟢'
        }
        
        status_emojis = {
            'queued': '⏳',
            'in_progress': '🔧',
            'stalled': '⛔',
            'completed': '✅',
            'pending': '📋'
        }
        
        # Build report
        report = f"""╔══════════════════════════════════════════════════════════════════════════╗
║          📊 DAILY QUEUE EMAIL REPORT - PATRICIA'S FACTORY                ║
╠══════════════════════════════════════════════════════════════════════════╣
║ Report Date: {self.report_date:<56} ║
║ Generated:   {self.report_time:<56} ║
║ From:        Miles <miles@myl0nr0s.cloud>{' ' * 35} ║
╚══════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 QUEUE STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Total Orders:      {total_orders:>4}
  ├─ Completed:      {completed:>4} ✅
  ├─ Active:         {active:>4} 🔧
  │   ├─ Queued:     {queued:>4} ⏳
  │   └─ In Progress:{in_progress:>4} 🔧
  └─ This Week:      +{stats['recent_created']:>3} new / {stats['recent_completed']:>3} completed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 ACTIVE ORDERS (Top {len(active_orders)})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        for i, order in enumerate(active_orders, 1):
            p_emoji = priority_emojis.get(order['priority'], '⚪')
            s_emoji = status_emojis.get(order['status'], '⏳')
            report += f"""  {i:2d}. {p_emoji} {order['product'][:50]}
      ID: {order['id']:<20} Client: {order['client']}
      Status: {s_emoji} {order['status'].upper():<12} Progress: {order['progress']}
      Created: {order['created']}

"""
        
        report += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 PRIORITY BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        for status in ['queued', 'in_progress', 'stalled']:
            if status in stats['by_priority']:
                report += f"  {status.upper()}:\n"
                for prio, count in sorted(stats['by_priority'][status].items(), 
                                          key=lambda x: {'urgent': 0, 'high': 1, 'normal': 2, 'low': 3}.get(x[0], 2)):
                    emoji = priority_emojis.get(prio, '⚪')
                    report += f"    {emoji} {prio.capitalize():<8}: {count:>3} orders\n"
                report += "\n"
        
        report += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 DATABASE INFO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Database:  {DB_PATH}
  Location:  Dark Factory Production System
  Manager:   Patricia (Head of Production)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*This is an automated daily report from the AGI Company Dark Factory.*
*Next report: Tomorrow at 13:00 UTC*

---
Miles 🚀
AGI Company Operations
miles@myl0nr0s.cloud
"""
        
        return report
    
    def send_email(self, report_content):
        """Send the report via email"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"📊 Daily Queue Report - {self.report_date}"
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        
        text_part = MIMEText(report_content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(FROM_EMAIL, FROM_PASSWORD)
                server.send_message(msg)
            return True, "Email sent successfully"
        except Exception as e:
            return False, str(e)
    
    def save_report(self, report_content):
        """Save report to file"""
        reports_dir = Path("/root/.openclaw/workspace/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = reports_dir / f"daily_queue_report_{self.timestamp.strftime('%Y%m%d_%H%M')}.md"
        report_file.write_text(report_content, encoding='utf-8')
        return report_file
    
    def run(self):
        """Execute the daily queue report"""
        print("🚀 Miles - Daily Queue Report Emailer")
        print("=" * 60)
        print(f"Timestamp: {self.timestamp.isoformat()}")
        print()
        
        # Generate report
        print("📊 Generating queue report...")
        report = self.generate_report()
        
        # Save locally
        print("💾 Saving report to file...")
        report_file = self.save_report(report)
        print(f"   Saved: {report_file}")
        
        # Send email
        print(f"📧 Sending email to {TO_EMAIL}...")
        success, message = self.send_email(report)
        
        if success:
            print(f"✅ {message}")
            print(f"\n📬 Email delivered!")
            print(f"   To: {TO_EMAIL}")
            print(f"   From: {FROM_EMAIL}")
            print(f"   Subject: 📊 Daily Queue Report - {self.report_date}")
        else:
            print(f"❌ Failed to send: {message}")
            print(f"\n📄 Report saved locally at:")
            print(f"   {report_file}")
            return 1
        
        return 0


if __name__ == "__main__":
    reporter = DailyQueueReporter()
    exit(reporter.run())
