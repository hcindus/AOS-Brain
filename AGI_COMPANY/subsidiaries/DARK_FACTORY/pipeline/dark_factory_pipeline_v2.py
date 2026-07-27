#!/usr/bin/env python3
"""
Dark Factory Pipeline Manager v2.0
Actually builds things. Verifies outputs. Reports truth.
"""

import os
import sqlite3
import json
import time
import uuid
import subprocess
import subprocess as sp
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Setup logging - works in both CI and local environments
log_dir = os.environ.get('DF_LOG_DIR', '/var/log/dark_factory')
log_file = os.path.join(log_dir, 'pipeline_v2.log')

try:
    os.makedirs(log_dir, exist_ok=True)
    handlers = [logging.FileHandler(log_file), logging.StreamHandler()]
except (OSError, PermissionError):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_log = os.path.join(script_dir, 'logs', 'pipeline_v2.log')
    os.makedirs(os.path.dirname(local_log), exist_ok=True)
    handlers = [logging.FileHandler(local_log), logging.StreamHandler()]
    log_file = local_log

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=handlers
)
logger = logging.getLogger('DarkFactoryV2')


class DarkFactoryV2:
    """Pipeline that actually builds things"""
    
    VERSION = "2.0.0"
    DB_PATH = "/root/.openclaw/workspace/data/factory/dark_factory_v2.db"
    OUTPUT_DIR = "/root/.openclaw/workspace/data/factory/output"
    
    # Build types we support
    BUILD_TYPES = {
        "bubblewrap_apk": {
            "name": "Bubblewrap Android APK",
            "requires": ["manifest.json"],
            "produces": [".apk"],
            "timeout": 600
        },
        "static_web": {
            "name": "Static Website",
            "requires": ["index.html"],
            "produces": ["index.html"],
            "timeout": 60
        },
        "python_package": {
            "name": "Python Package",
            "requires": ["setup.py"],
            "produces": [".whl"],
            "timeout": 300
        }
    }
    
    def __init__(self):
        self.db_path = Path(self.DB_PATH)
        self.output_dir = Path(self.OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.ensure_db()
        logger.info(f"🌑 Dark Factory Pipeline v{self.VERSION} initialized")
        logger.info(f"📁 Output directory: {self.OUTPUT_DIR}")
    
    def ensure_db(self):
        """Ensure database exists with proper schema"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        # Production orders with build tracking
        c.execute('''
            CREATE TABLE IF NOT EXISTS production_orders (
                id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                product_type TEXT NOT NULL,
                build_type TEXT NOT NULL DEFAULT 'bubblewrap_apk',
                source_path TEXT,
                quantity INTEGER DEFAULT 1,
                status TEXT DEFAULT 'queued',
                stage INTEGER DEFAULT 0,
                total_stages INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                build_started_at TIMESTAMP,
                build_completed_at TIMESTAMP,
                priority TEXT DEFAULT 'normal',
                assigned_agents TEXT,
                metadata TEXT,
                output_paths TEXT,
                build_logs TEXT,
                verified INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Build execution log
        c.execute('''
            CREATE TABLE IF NOT EXISTS build_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT,
                build_type TEXT,
                command TEXT,
                exit_code INTEGER,
                stdout TEXT,
                stderr TEXT,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                output_files TEXT,
                verified INTEGER DEFAULT 0,
                FOREIGN KEY (order_id) REFERENCES production_orders(id)
            )
        ''')
        
        # Pipeline metrics with truth
        c.execute('''
            CREATE TABLE IF NOT EXISTS pipeline_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                orders_queued INTEGER DEFAULT 0,
                orders_building INTEGER DEFAULT 0,
                orders_completed INTEGER DEFAULT 0,
                orders_failed INTEGER DEFAULT 0,
                orders_verified INTEGER DEFAULT 0,
                avg_build_time REAL,
                build_success_rate REAL DEFAULT 0.0
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Database schema verified")
    
    def add_build_order(self, product_name: str, build_type: str,
                       source_path: str, output_name: str = None,
                       priority: str = "normal", metadata: Dict = None) -> str:
        """Add a build order to the pipeline"""
        order_id = f"DF2-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        if build_type not in self.BUILD_TYPES:
            raise ValueError(f"Unknown build type: {build_type}. Available: {list(self.BUILD_TYPES.keys())}")
        
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO production_orders 
            (id, product_name, product_type, build_type, source_path, quantity, 
             priority, metadata, output_paths)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, product_name, build_type, build_type, source_path, 1,
              priority, json.dumps(metadata or {}), 
              json.dumps({"expected_name": output_name or product_name})))
        conn.commit()
        conn.close()
        
        logger.info(f"📦 New build order: {order_id} - {product_name} ({build_type})")
        return order_id
    
    def update_order_status(self, order_id: str, status: str, 
                          output_paths: Dict = None, build_logs: str = None):
        """Update order status and outputs"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        updates = ["status = ?, last_updated = ?"]
        params = [status, datetime.now().isoformat()]
        
        if status == 'building':
            updates.append("started_at = COALESCE(?, started_at)")
            params.append(datetime.now().isoformat())
            updates.append("build_started_at = ?")
            params.append(datetime.now().isoformat())
        
        if status in ('completed', 'failed'):
            updates.append("build_completed_at = ?")
            params.append(datetime.now().isoformat())
        
        if output_paths:
            updates.append("output_paths = ?")
            params.append(json.dumps(output_paths))
        
        if build_logs:
            updates.append("build_logs = ?")
            params.append(build_logs)
        
        params.append(order_id)
        
        c.execute(f'''
            UPDATE production_orders 
            SET {', '.join(updates)}
            WHERE id = ?
        ''', params)
        
        conn.commit()
        conn.close()
        logger.info(f"📝 Order {order_id} status: {status}")
    
    def verify_build_output(self, order_id: str) -> bool:
        """Verify that build actually produced expected files"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('SELECT build_type, output_paths FROM production_orders WHERE id = ?', (order_id,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return False
        
        build_type, output_paths_json = result
        output_paths = json.loads(output_paths_json or '{}')
        expected_extensions = self.BUILD_TYPES[build_type]["produces"]
        
        verified = False
        verification_details = []
        
        for ext in expected_extensions:
            # Check output directory for files with expected extension
            matching_files = list(self.output_dir.glob(f"*{ext}"))
            if matching_files:
                # Check file size > 0
                for f in matching_files:
                    if f.stat().st_size > 0:
                        verified = True
                        verification_details.append(f"✅ {f.name} ({f.stat().st_size} bytes)")
                        # Update order with actual path
                        if 'actual_paths' not in output_paths:
                            output_paths['actual_paths'] = []
                        output_paths['actual_paths'].append(str(f))
            else:
                verification_details.append(f"❌ No {ext} file found")
        
        # Update verification status
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''
            UPDATE production_orders 
            SET verified = ?, output_paths = ?, build_logs = ?
            WHERE id = ?
        ''', (1 if verified else 0, json.dumps(output_paths), 
              '\n'.join(verification_details), order_id))
        conn.commit()
        conn.close()
        
        if verified:
            logger.info(f"✅ Build verified for {order_id}")
        else:
            logger.error(f"❌ Build verification failed for {order_id}")
        
        return verified
    
    def execute_bubblewrap_build(self, order_id: str, source_path: str, 
                                  output_name: str) -> Dict:
        """Actually execute bubblewrap build"""
        result = {
            "success": False,
            "order_id": order_id,
            "stdout": "",
            "stderr": "",
            "exit_code": -1,
            "output_files": [],
            "duration": 0
        }
        
        start_time = time.time()
        
        try:
            # Update status to building
            self.update_order_status(order_id, 'building')
            
            manifest_path = Path(source_path) / "manifest.json"
            if not manifest_path.exists():
                result["stderr"] = f"No manifest.json found at {manifest_path}"
                self.update_order_status(order_id, 'failed', build_logs=result["stderr"])
                return result
            
            # Create temp build directory
            build_dir = f"/tmp/bubblewrap_v2/{output_name}_{order_id[-8:]}"
            Path(build_dir).mkdir(parents=True, exist_ok=True)
            
            # Find bubblewrap
            bubblewrap = shutil.which("bubblewrap") or shutil.which("npx")
            if not bubblewrap:
                result["stderr"] = "bubblewrap or npx not found"
                self.update_order_status(order_id, 'failed', build_logs=result["stderr"])
                return result
            
            # Run bubblewrap init (with --yes to auto-accept prompts)
            logger.info(f"🔧 {order_id}: Initializing Bubblewrap...")
            if bubblewrap.endswith("npx"):
                init_cmd = [bubblewrap, "@bubblewrap/cli", "init", 
                           "--manifest", str(manifest_path),
                           "--directory", build_dir, "--yes"]
            else:
                init_cmd = [bubblewrap, "init", 
                           "--manifest", str(manifest_path),
                           "--directory", build_dir, "--yes"]
            
            # Run with stdin pipe to auto-answer prompts
            import subprocess as sp
            init_proc = sp.Popen(
                init_cmd,
                stdin=sp.PIPE,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                text=True,
                cwd=build_dir
            )
            init_stdout, init_stderr = init_proc.communicate(input="Y\nY\nY\nY\nY\n", timeout=120)
            init_result = sp.CompletedProcess(
                init_cmd, init_proc.returncode,
                stdout=init_stdout, stderr=init_stderr
            )
            
            result["stdout"] += f"=== INIT ===\n{init_result.stdout}\n"
            result["stderr"] += f"=== INIT ===\n{init_result.stderr}\n"
            result["exit_code"] = init_result.returncode
            
            if init_result.returncode != 0:
                result["stderr"] += "\nBubblewrap init failed"
                self.update_order_status(order_id, 'failed', 
                                       build_logs=result["stderr"])
                return result
            
            # Run bubblewrap build (with --yes to auto-accept prompts)
            logger.info(f"🔨 {order_id}: Building APK...")
            if bubblewrap.endswith("npx"):
                build_cmd = [bubblewrap, "@bubblewrap/cli", "build", "--yes"]
            else:
                build_cmd = [bubblewrap, "build", "--yes"]
            
            # Run build with stdin pipe
            build_proc = sp.Popen(
                build_cmd,
                stdin=sp.PIPE,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                text=True,
                cwd=build_dir
            )
            build_stdout, build_stderr = build_proc.communicate(input="Y\nY\nY\nY\nY\n", timeout=300)
            build_result = sp.CompletedProcess(
                build_cmd, build_proc.returncode,
                stdout=build_stdout, stderr=build_stderr
            )
            
            result["stdout"] += f"\n=== BUILD ===\n{build_result.stdout}\n"
            result["stderr"] += f"\n=== BUILD ===\n{build_result.stderr}\n"
            result["exit_code"] = build_result.returncode
            
            if build_result.returncode != 0:
                result["stderr"] += "\nBubblewrap build failed"
                self.update_order_status(order_id, 'failed',
                                       build_logs=result["stderr"])
                return result
            
            # Move outputs to factory output directory
            build_path = Path(build_dir)
            output_files = []
            
            for apk_file in build_path.glob("*.apk"):
                dest = self.output_dir / f"{output_name}.apk"
                shutil.copy(apk_file, dest)
                output_files.append(str(dest))
                logger.info(f"📱 APK created: {dest}")
            
            for aab_file in build_path.glob("*.aab"):
                dest = self.output_dir / f"{output_name}.aab"
                shutil.copy(aab_file, dest)
                output_files.append(str(dest))
                logger.info(f"📦 AAB created: {dest}")
            
            # Copy keystore
            for key_file in list(build_path.glob("*.keystore")) + list(build_path.glob("*.jks")):
                dest = self.output_dir / f"{output_name}.keystore"
                shutil.copy(key_file, dest)
                output_files.append(str(dest))
            
            result["output_files"] = output_files
            result["duration"] = time.time() - start_time
            result["success"] = True
            
            # Update order
            self.update_order_status(order_id, 'completed',
                                   output_paths={"files": output_files},
                                   build_logs=result["stdout"])
            
            # Verify the build
            if self.verify_build_output(order_id):
                logger.info(f"🎉 {order_id}: Build successful and verified!")
            else:
                logger.warning(f"⚠️ {order_id}: Build reported success but verification failed")
            
        except subprocess.TimeoutExpired as e:
            result["stderr"] += f"\nBuild timed out after {e.timeout}s"
            self.update_order_status(order_id, 'failed', build_logs=result["stderr"])
        except Exception as e:
            result["stderr"] += f"\nException: {str(e)}"
            self.update_order_status(order_id, 'failed', build_logs=result["stderr"])
        
        return result
    
    def process_single_order(self, order_id: str) -> Dict:
        """Process a single queued order"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''
            SELECT product_name, build_type, source_path, metadata 
            FROM production_orders 
            WHERE id = ? AND status = 'queued'
        ''', (order_id,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return {"error": f"Order {order_id} not found or not queued"}
        
        product_name, build_type, source_path, metadata_json = result
        metadata = json.loads(metadata_json or '{}')
        output_name = metadata.get('output_name', product_name.replace(' ', '_').lower())
        
        logger.info(f"🚀 Processing order: {order_id} ({product_name})")
        
        if build_type == 'bubblewrap_apk':
            return self.execute_bubblewrap_build(order_id, source_path, output_name)
        else:
            return {"error": f"Build type {build_type} not yet implemented"}
    
    def run_pipeline_tick(self, max_concurrent: int = 1):
        """Process queued orders - actually builds things"""
        logger.info("🔄 Running pipeline tick...")
        
        # Get queued orders by priority
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''
            SELECT id FROM production_orders 
            WHERE status = 'queued'
            ORDER BY 
                CASE priority 
                    WHEN 'urgent' THEN 0 
                    WHEN 'high' THEN 1 
                    WHEN 'normal' THEN 2 
                    ELSE 3 
                END,
                created_at ASC
            LIMIT ?
        ''', (max_concurrent,))
        
        queued_orders = [row[0] for row in c.fetchall()]
        conn.close()
        
        if not queued_orders:
            logger.info("ℹ️ No queued orders to process")
        else:
            logger.info(f"📋 Processing {len(queued_orders)} order(s)")
        
        results = []
        for order_id in queued_orders:
            result = self.process_single_order(order_id)
            results.append(result)
            time.sleep(1)  # Brief pause between builds
        
        # Update metrics
        self.update_metrics()
        
        return results
    
    def update_metrics(self):
        """Update pipeline metrics with truth"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE status = "queued"')
        queued = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE status = "building"')
        building = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE status = "completed"')
        completed = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE status = "failed"')
        failed = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE verified = 1')
        verified = c.fetchone()[0]
        
        # Calculate success rate
        total_done = completed + failed
        success_rate = (completed / total_done * 100) if total_done > 0 else 0
        
        # Calculate avg build time for successful builds
        c.execute('''
            SELECT AVG(
                julianday(build_completed_at) - julianday(build_started_at)
            ) * 24 * 60 FROM production_orders 
            WHERE status = 'completed' AND build_started_at IS NOT NULL
        ''')
        avg_minutes = (c.fetchone()[0] or 0)
        
        c.execute('''
            INSERT INTO pipeline_metrics 
            (orders_queued, orders_building, orders_completed, orders_failed, 
             orders_verified, avg_build_time, build_success_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (queued, building, completed, failed, verified, 
              round(avg_minutes, 2), round(success_rate, 2)))
        
        conn.commit()
        conn.close()
        
        logger.info(f"📊 Metrics: {queued} queued | {building} building | "
                   f"{completed} completed | {failed} failed | "
                   f"{verified} verified | {success_rate:.1f}% success")
    
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
                ORDER BY priority DESC, created_at ASC
            ''')
        
        orders = [dict(row) for row in c.fetchall()]
        conn.close()
        return orders
    
    def get_metrics(self) -> Dict:
        """Get current pipeline metrics"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT * FROM pipeline_metrics ORDER BY timestamp DESC LIMIT 1')
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                "queued": row[2],
                "building": row[3],
                "completed": row[4],
                "failed": row[5],
                "verified": row[6],
                "avg_build_time_min": row[7],
                "success_rate_pct": row[8],
                "timestamp": row[1]
            }
        return {"error": "No metrics yet"}
    
    def generate_report(self) -> str:
        """Generate a status report with truth"""
        metrics = self.get_metrics()
        
        # Get recent orders
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''
            SELECT * FROM production_orders 
            ORDER BY created_at DESC
            LIMIT 10
        ''')
        recent = [dict(row) for row in c.fetchall()]
        conn.close()
        
        # Status emojis
        def status_emoji(s):
            return {
                'queued': '⏳', 'building': '🔨', 'completed': '✅',
                'failed': '❌', 'verified': '🎉'
            }.get(s, '⏳')
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║           🌑 DARK FACTORY PIPELINE v2.0 REPORT                   ║
╠══════════════════════════════════════════════════════════════════╣
║ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
╠══════════════════════════════════════════════════════════════════╣
║ METRICS (TRUTH, NOT LOGGING)
║ ─────────────────────────────────────────────────────────────────
║  • Queued:      {metrics.get('queued', 0):>3} orders
║  • Building:    {metrics.get('building', 0):>3} orders  
║  • Completed:   {metrics.get('completed', 0):>3} orders
║  • Failed:      {metrics.get('failed', 0):>3} orders
║  • Verified:    {metrics.get('verified', 0):>3} orders ✅
║  • Success:     {metrics.get('success_rate_pct', 0):>5.1f}%
║  • Avg Build:   {metrics.get('avg_build_time_min', 0):>5.1f} min
╠══════════════════════════════════════════════════════════════════╣
║ RECENT ORDERS
║ ─────────────────────────────────────────────────────────────────"""
        
        for order in recent:
            emoji = status_emoji(order['status'])
            verified = "✓" if order.get('verified') else " "
            report += f"\n║ {emoji}│{verified}│ {order['id'][:16]:<16} │ {order['product_name'][:20]:<20} │ {order['status']:<10}"
        
        report += """
╚══════════════════════════════════════════════════════════════════╝
"""
        return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Dark Factory Pipeline v2.0')
    parser.add_argument('command', choices=[
        'status', 'queue', 'add', 'tick', 'report', 'build', 'verify'
    ])
    parser.add_argument('--product', '-p', help='Product name')
    parser.add_argument('--source', '-s', help='Source path (directory with manifest.json)')
    parser.add_argument('--type', '-t', default='bubblewrap_apk',
                       choices=['bubblewrap_apk', 'static_web', 'python_package'])
    parser.add_argument('--output', '-o', help='Output name')
    parser.add_argument('--priority', default='normal',
                       choices=['low', 'normal', 'high', 'urgent'])
    parser.add_argument('--order-id', help='Order ID to process')
    
    args = parser.parse_args()
    
    pipeline = DarkFactoryV2()
    
    if args.command == 'status':
        print(json.dumps(pipeline.get_metrics(), indent=2))
    
    elif args.command == 'queue':
        queue = pipeline.get_queue()
        print(f"{'ID':<20} {'Product':<25} {'Type':<15} {'Status':<12} {'Verified'}")
        print("-" * 85)
        for order in queue:
            verified = "✅" if order.get('verified') else "  "
            print(f"{order['id'][:20]:<20} {order['product_name'][:25]:<25} "
                  f"{order['build_type']:<15} {order['status']:<12} {verified}")
    
    elif args.command == 'add':
        if not args.product or not args.source:
            print("Error: --product and --source required")
            return
        if not Path(args.source).exists():
            print(f"Error: Source path does not exist: {args.source}")
            return
        order_id = pipeline.add_build_order(
            product_name=args.product,
            build_type=args.type,
            source_path=args.source,
            output_name=args.output,
            priority=args.priority
        )
        print(f"Created build order: {order_id}")
    
    elif args.command == 'tick':
        results = pipeline.run_pipeline_tick()
        print(json.dumps(results, indent=2, default=str))
    
    elif args.command == 'report':
        print(pipeline.generate_report())
    
    elif args.command == 'build':
        if not args.order_id:
            print("Error: --order-id required")
            return
        result = pipeline.process_single_order(args.order_id)
        print(json.dumps(result, indent=2, default=str))
    
    elif args.command == 'verify':
        if not args.order_id:
            print("Error: --order-id required")
            return
        verified = pipeline.verify_build_output(args.order_id)
        print(f"Verification: {'✅ PASSED' if verified else '❌ FAILED'}")


if __name__ == "__main__":
    main()
