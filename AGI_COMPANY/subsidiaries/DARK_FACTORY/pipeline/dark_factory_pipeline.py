#!/usr/bin/env python3
"""
Dark Factory Pipeline Manager
Ongoing production pipeline with THIS integration and automated processing
"""

import sqlite3
import json
import time
import uuid
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('/var/log/dark_factory/pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DarkFactoryPipeline')

class DarkFactoryPipeline:
    """Manages the ongoing Dark Factory production pipeline"""
    
    VERSION = "1.0.0"
    DB_PATH = "/root/.openclaw/workspace/data/factory/dark_factory.db"
    
    # Production stages
    STAGES = [
        "queued",           # 0 - Waiting to start
        "design",           # 1 - Design phase
        "vendor_sourcing",  # 2 - Finding vendors
        "procurement",      # 3 - Ordering materials
        "production",       # 4 - Manufacturing
        "assembly",         # 5 - Putting it together
        "qc",               # 6 - Quality control
        "packaging",        # 7 - Packaging
        "shipping_prep",    # 8 - Ready to ship
        "distribution",     # 9 - In transit
        "delivered"         # 10 - Complete
    ]
    
    def __init__(self):
        self.db_path = Path(self.DB_PATH)
        self.ensure_db()
        logger.info(f"🌑 Dark Factory Pipeline v{self.VERSION} initialized")
    
    def ensure_db(self):
        """Ensure database exists with proper schema"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        # Production orders table
        c.execute('''
            CREATE TABLE IF NOT EXISTS production_orders (
                id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                product_type TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                status TEXT DEFAULT 'queued',
                stage INTEGER DEFAULT 0,
                total_stages INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                priority TEXT DEFAULT 'normal',
                assigned_agents TEXT,
                metadata TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Pipeline metrics table
        c.execute('''
            CREATE TABLE IF NOT EXISTS pipeline_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                orders_queued INTEGER DEFAULT 0,
                orders_in_progress INTEGER DEFAULT 0,
                orders_completed INTEGER DEFAULT 0,
                avg_processing_time REAL,
                defect_count INTEGER DEFAULT 0,
                sigma_level REAL DEFAULT 0.0
            )
        ''')
        
        # Patricia integration log
        c.execute('''
            CREATE TABLE IF NOT EXISTS patricia_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT,
                report_type TEXT,
                status TEXT,
                metrics TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Database schema verified")
    
    def add_order(self, product_name: str, product_type: str, 
                  quantity: int = 1, priority: str = "normal",
                  client: str = None, metadata: Dict = None) -> str:
        """Add a new order to the pipeline"""
        order_id = f"DF-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO production_orders 
            (id, product_name, product_type, quantity, status, stage, priority, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, product_name, product_type, quantity, 'queued', 0, priority,
              json.dumps(metadata or {})))
        conn.commit()
        conn.close()
        
        logger.info(f"📦 New order added: {order_id} - {product_name} x{quantity}")
        self.sync_to_github(f"New order: {order_id}")
        return order_id
    
    def advance_order(self, order_id: str) -> bool:
        """Advance an order to the next stage"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT stage, status FROM production_orders WHERE id = ?', (order_id,))
        result = c.fetchone()
        
        if not result:
            logger.error(f"❌ Order not found: {order_id}")
            conn.close()
            return False
        
        current_stage, status = result
        
        if status == 'completed':
            logger.warning(f"⚠️ Order {order_id} already completed")
            conn.close()
            return False
        
        new_stage = current_stage + 1
        new_status = self.STAGES[min(new_stage, len(self.STAGES) - 1)]
        
        # Mark as started if advancing from queued
        started_at = None
        if current_stage == 0:
            started_at = datetime.now().isoformat()
        
        # Mark completed if at final stage
        completed_at = None
        if new_stage >= len(self.STAGES) - 1:
            completed_at = datetime.now().isoformat()
            new_status = 'completed'
            logger.info(f"✅ Order {order_id} COMPLETED!")
        
        c.execute('''
            UPDATE production_orders 
            SET stage = ?, status = ?, started_at = COALESCE(?, started_at),
                completed_at = ?, last_updated = ?
            WHERE id = ?
        ''', (new_stage, new_status, started_at, completed_at, 
              datetime.now().isoformat(), order_id))
        
        conn.commit()
        conn.close()
        
        stage_name = self.STAGES[new_stage] if new_stage < len(self.STAGES) else "completed"
        logger.info(f"⏩ Order {order_id} advanced to: {stage_name}")
        
        # Report to Patricia
        self.report_to_patricia(order_id, "stage_advanced", {"stage": stage_name})
        
        return True
    
    def get_queue(self, status_filter: str = None) -> List[Dict]:
        """Get current pipeline queue"""
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        if status_filter:
            c.execute('''
                SELECT * FROM production_orders 
                WHERE status = ? 
                ORDER BY priority DESC, created_at ASC
            ''', (status_filter,))
        else:
            c.execute('''
                SELECT * FROM production_orders 
                WHERE status != 'completed'
                ORDER BY priority DESC, stage DESC, created_at ASC
            ''')
        
        orders = [dict(row) for row in c.fetchall()]
        conn.close()
        return orders
    
    def get_metrics(self) -> Dict:
        """Get pipeline metrics"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE status = "queued"')
        queued = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE status NOT IN ("queued", "completed", "delivered")')
        in_progress = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE status IN ("completed", "delivered")')
        completed = c.fetchone()[0]
        
        c.execute('''
            SELECT AVG(
                julianday(completed_at) - julianday(started_at)
            ) FROM production_orders 
            WHERE completed_at IS NOT NULL
        ''')
        avg_time = c.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "queued": queued,
            "in_progress": in_progress,
            "completed": completed,
            "avg_days": round(avg_time, 2) if avg_time else 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def report_to_patricia(self, order_id: str, report_type: str, data: Dict):
        """Send report to Patricia/THIS system"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO patricia_reports (order_id, report_type, status, metrics)
            VALUES (?, ?, ?, ?)
        ''', (order_id, report_type, 'pending', json.dumps(data)))
        conn.commit()
        conn.close()
        
        # Try to notify Patricia if available
        try:
            patricia_path = "/root/.openclaw/workspace/agent_sandboxes/patricia/patricia_this_integration.py"
            if Path(patricia_path).exists():
                subprocess.run([
                    "python3", patricia_path, 
                    "--report", json.dumps({
                        "order_id": order_id,
                        "type": report_type,
                        "data": data
                    })
                ], capture_output=True, timeout=10)
                logger.info(f"📊 Reported to Patricia: {order_id}")
        except Exception as e:
            logger.debug(f"Patricia notification skipped: {e}")
    
    def sync_to_github(self, message: str = "Pipeline update"):
        """Sync state to GitHub"""
        try:
            workspace = "/root/.openclaw/workspace"
            subprocess.run(
                ["git", "add", "-A"],
                cwd=workspace, capture_output=True, timeout=10
            )
            subprocess.run(
                ["git", "commit", "-m", f"Dark Factory: {message}"],
                cwd=workspace, capture_output=True, timeout=10
            )
            subprocess.run(
                ["git", "push", "origin", "master"],
                cwd=workspace, capture_output=True, timeout=30
            )
            logger.info("☁️ Synced to GitHub")
        except Exception as e:
            logger.debug(f"GitHub sync skipped: {e}")
    
    def run_pipeline_tick(self):
        """Process one pipeline tick - advance orders, check status"""
        logger.info("🔄 Running pipeline tick...")
        
        # Get orders ready to advance (simulate processing time)
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        # Advance orders that have been in current stage long enough
        # (In real system, this would check external APIs, vendor status, etc.)
        c.execute('''
            SELECT id, stage, status, last_updated FROM production_orders
            WHERE status NOT IN ('completed', 'queued')
            AND datetime(last_updated) < datetime('now', '-1 hour')
            ORDER BY priority DESC, stage ASC
            LIMIT 3
        ''')
        
        ready_orders = c.fetchall()
        conn.close()
        
        for order_id, stage, status, last_updated in ready_orders:
            self.advance_order(order_id)
            time.sleep(0.5)  # Rate limiting
        
        # Update metrics
        metrics = self.get_metrics()
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO pipeline_metrics 
            (orders_queued, orders_in_progress, orders_completed, avg_processing_time)
            VALUES (?, ?, ?, ?)
        ''', (metrics['queued'], metrics['in_progress'], 
              metrics['completed'], metrics['avg_days']))
        conn.commit()
        conn.close()
        
        logger.info(f"📈 Metrics: {metrics['queued']} queued, "
                   f"{metrics['in_progress']} active, "
                   f"{metrics['completed']} completed")
        
        return metrics
    
    def generate_report(self) -> str:
        """Generate a status report"""
        metrics = self.get_metrics()
        queue = self.get_queue()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           🌑 DARK FACTORY PIPELINE REPORT                    ║
╠══════════════════════════════════════════════════════════════╣
║ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
╠══════════════════════════════════════════════════════════════╣
║ METRICS
║ ─────────────────────────────────────────────────────────────
║  • Queued:      {metrics['queued']:>3} orders
║  • In Progress:  {metrics['in_progress']:>3} orders  
║  • Completed:   {metrics['completed']:>3} orders
║  • Avg Time:    {metrics['avg_days']:>5.1f} days
╠══════════════════════════════════════════════════════════════╣
║ ACTIVE ORDERS
║ ─────────────────────────────────────────────────────────────"""
        
        for order in queue[:10]:
            status_emoji = {
                'queued': '⏳',
                'design': '🎨',
                'production': '🔧',
                'qc': '🔍',
                'distribution': '🚚',
            }.get(order['status'], '⏳')
            
            report += f"\n║  {status_emoji} {order['id'][:20]:<20} | {order['product_name'][:25]:<25} | {order['status']:<12}"
        
        if len(queue) > 10:
            report += f"\n║  ... and {len(queue) - 10} more orders"
        
        report += """
╚══════════════════════════════════════════════════════════════╝"""
        
        return report
    
    def run_continuous(self, interval_seconds: int = 300):
        """Run pipeline continuously"""
        logger.info(f"🚀 Starting continuous pipeline (tick every {interval_seconds}s)")
        
        while True:
            try:
                self.run_pipeline_tick()
                logger.info(f"⏱️  Sleeping {interval_seconds}s...")
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                logger.info("🛑 Pipeline stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Pipeline error: {e}")
                time.sleep(60)  # Retry after 1 min on error


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Dark Factory Pipeline')
    parser.add_argument('command', choices=[
        'status', 'queue', 'add', 'advance', 'tick', 'report', 'run'
    ])
    parser.add_argument('--product', '-p', help='Product name')
    parser.add_argument('--type', '-t', help='Product type')
    parser.add_argument('--quantity', '-q', type=int, default=1)
    parser.add_argument('--priority', default='normal', 
                       choices=['low', 'normal', 'high', 'urgent'])
    parser.add_argument('--client', '-c', help='Client name')
    parser.add_argument('--order-id', '-o', help='Order ID to advance')
    parser.add_argument('--interval', '-i', type=int, default=300,
                       help='Tick interval in seconds')
    
    args = parser.parse_args()
    
    pipeline = DarkFactoryPipeline()
    
    if args.command == 'status':
        print(json.dumps(pipeline.get_metrics(), indent=2))
    
    elif args.command == 'queue':
        queue = pipeline.get_queue()
        for order in queue:
            print(f"{order['id']} | {order['product_name']} | {order['status']} | {order['priority']}")
    
    elif args.command == 'add':
        if not args.product:
            print("Error: --product required")
            return
        order_id = pipeline.add_order(
            product_name=args.product,
            product_type=args.type or 'general',
            quantity=args.quantity,
            priority=args.priority,
            client=args.client
        )
        print(f"Created order: {order_id}")
    
    elif args.command == 'advance':
        if not args.order_id:
            print("Error: --order-id required")
            return
        success = pipeline.advance_order(args.order_id)
        print(f"Advanced: {'✅' if success else '❌'}")
    
    elif args.command == 'tick':
        metrics = pipeline.run_pipeline_tick()
        print(json.dumps(metrics, indent=2))
    
    elif args.command == 'report':
        print(pipeline.generate_report())
    
    elif args.command == 'run':
        pipeline.run_continuous(args.interval)


if __name__ == "__main__":
    main()
