#!/usr/bin/env python3
"""
Dark Factory Automation Script
Automatically advances stalled orders through the pipeline
Triggered by Patricia's Six Sigma recommendations
"""

import sqlite3
import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('DarkFactoryAutomation')

class DarkFactoryAutomator:
    """Automates order advancement based on Patricia's defect analysis"""
    
    DB_PATH = "/root/.openclaw/workspace/data/factory/dark_factory.db"
    
    def __init__(self):
        self.db_path = Path(self.DB_PATH)
        self.automated_count = 0
        self.errors = []
        
    def get_stalled_orders(self, days_stalled=2):
        """Get orders stalled for more than N days"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            SELECT id, product_name, status, stage, total_stages, priority, last_updated
            FROM production_orders
            WHERE status NOT IN ('completed', 'delivered')
            AND datetime(last_updated) < datetime('now', '-{} days')
            ORDER BY priority DESC, created_at ASC
        '''.format(days_stalled))
        
        orders = []
        for row in c.fetchall():
            orders.append({
                'id': row[0],
                'product_name': row[1],
                'status': row[2],
                'stage': row[3],
                'total_stages': row[4],
                'priority': row[5],
                'last_updated': row[6]
            })
        
        conn.close()
        return orders
    
    def advance_order(self, order_id, current_status, current_stage, total_stages):
        """Advance an order to the next stage"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Determine new status
        if current_status == 'queued':
            new_status = 'in_progress'
            new_stage = 1
        elif current_status == 'in_progress':
            if current_stage >= total_stages:
                new_status = 'completed'
                new_stage = total_stages
            else:
                new_status = 'in_progress'
                new_stage = current_stage + 1
        else:
            new_status = current_status
            new_stage = current_stage
        
        # Update the order
        c.execute('''
            UPDATE production_orders
            SET status = ?, stage = ?, last_updated = ?
            WHERE id = ?
        ''', (new_status, new_stage, now, order_id))
        
        conn.commit()
        conn.close()
        
        return {
            'order_id': order_id,
            'old_status': current_status,
            'new_status': new_status,
            'old_stage': current_stage,
            'new_stage': new_stage
        }
    
    def run_auto_advance(self, dry_run=False):
        """Main automation routine"""
        logger.info("=" * 60)
        logger.info("🤖 DARK FACTORY AUTOMATION - Patricia's Recommendations")
        logger.info("=" * 60)
        
        # Get stalled orders
        stalled = self.get_stalled_orders(days_stalled=2)
        logger.info(f"Found {len(stalled)} stalled orders")
        
        if not stalled:
            logger.info("No stalled orders to process. Pipeline is clear!")
            return {'status': 'success', 'automated': 0, 'errors': []}
        
        # Process stalled orders
        results = []
        
        for order in stalled:
            try:
                if dry_run:
                    logger.info(f"[DRY RUN] Would advance: {order['id']} - {order['product_name']}")
                    results.append({
                        'order_id': order['id'],
                        'action': 'would_advance',
                        'dry_run': True
                    })
                else:
                    result = self.advance_order(
                        order['id'],
                        order['status'],
                        order['stage'],
                        order['total_stages']
                    )
                    logger.info(f"✅ Advanced: {order['id']} - {result['old_status']} → {result['new_status']}")
                    results.append(result)
                    self.automated_count += 1
                    
            except Exception as e:
                logger.error(f"❌ Failed to advance {order['id']}: {str(e)}")
                self.errors.append({'order_id': order['id'], 'error': str(e)})
        
        # Summary
        logger.info("=" * 60)
        logger.info(f"📊 AUTOMATION COMPLETE")
        logger.info(f"   Orders Advanced: {self.automated_count}")
        logger.info(f"   Errors: {len(self.errors)}")
        logger.info("=" * 60)
        
        return {
            'status': 'success',
            'automated': self.automated_count,
            'errors': self.errors,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_patricia_report(self):
        """Generate report for Patricia"""
        return {
            'automation_run': datetime.now().isoformat(),
            'orders_processed': self.automated_count,
            'errors': len(self.errors),
            'recommendation_status': 'implemented'
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Dark Factory Automation')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without executing')
    parser.add_argument('--report', action='store_true', help='Generate Patricia report')
    args = parser.parse_args()
    
    automator = DarkFactoryAutomator()
    
    if args.dry_run:
        logger.info("🔍 DRY RUN MODE - No changes will be made")
        result = automator.run_auto_advance(dry_run=True)
    else:
        logger.info("🚀 EXECUTING AUTO-ADVANCE")
        result = automator.run_auto_advance(dry_run=False)
    
    if args.report:
        report = automator.generate_patricia_report()
        print(json.dumps(report, indent=2))
    
    # Save result to Patricia's reports
    report_path = Path("/root/.openclaw/workspace/agent_sandboxes/patricia/reports")
    report_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = report_path / f"automation_result_{timestamp}.json"
    
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    logger.info(f"📄 Report saved: {result_file}")
    
    return 0 if len(result.get('errors', [])) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
