#!/usr/bin/env python3
"""
The Key Master - Rotation Automation v1.0.0
Automated secret rotation scheduler
"""

import os
import sys
import json
import logging
import smtplib
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from vault_core import get_vault

# Configuration
ROTATION_DAYS_WARNING = 7  # Warn when secret expires in 7 days
ROTATION_DAYS_CRITICAL = 1  # Critical when expires in 1 day
NOTIFY_EMAIL = os.environ.get('KEYMASTER_NOTIFY_EMAIL')
LOG_FILE = Path('/root/.openclaw/workspace/agents/keymaster/storage/logs/rotation.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('keymaster-rotation')

class RotationAutomator:
    """Automated rotation management"""
    
    def __init__(self):
        self.vault = get_vault()
        
    def check_rotation_queue(self) -> dict:
        """Check for secrets requiring rotation"""
        secrets = self.vault.get_rotation_queue()
        
        now = datetime.now()
        warnings = []
        critical = []
        overdue = []
        
        for secret in secrets:
            if not secret.expires_at:
                continue
                
            days_left = (secret.expires_at - now).days
            
            if days_left < 0:
                overdue.append(secret)
            elif days_left <= ROTATION_DAYS_CRITICAL:
                critical.append((secret, days_left))
            elif days_left <= ROTATION_DAYS_WARNING:
                warnings.append((secret, days_left))
                
        return {
            'overdue': overdue,
            'critical': critical,
            'warnings': warnings,
            'total_due': len(secrets)
        }
        
    def generate_rotation_report(self) -> str:
        """Generate rotation status report"""
        status = self.check_rotation_queue()
        
        report = []
        report.append("🗝️  The Key Master - Rotation Report")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("=" * 60)
        
        if status['overdue']:
            report.append(f"\n⛔ OVERDUE ({len(status['overdue'])}):")
            for s in status['overdue']:
                report.append(f"  - {s.secret_id} ({s.service}) - EXPIRED")
                
        if status['critical']:
            report.append(f"\n🚨 CRITICAL ({len(status['critical'])}):")
            for s, days in status['critical']:
                report.append(f"  - {s.secret_id} ({s.service}) - {days} days")
                
        if status['warnings']:
            report.append(f"\n⚠️  WARNING ({len(status['warnings'])}):")
            for s, days in status['warnings']:
                report.append(f"  - {s.secret_id} ({s.service}) - {days} days")
                
        if not status['total_due']:
            report.append("\n✅ All secrets are current. No rotation required.")
            
        return "\n".join(report)
        
    def auto_rotate(self, dry_run: bool = True) -> list:
        """Attempt automatic rotation for supported services"""
        rotated = []
        
        # Check for auto-rotatable services
        # This would integrate with specific APIs:
        # - Cloud providers (AWS, GCP, Azure)
        # - SaaS platforms with API rotation support
        # - Self-hosted services with rotation endpoints
        
        status = self.check_rotation_queue()
        
        for secret, days in status['critical'] + [(s, 0) for s in status['overdue']]:
            logger.info(f"Attempting auto-rotation for {secret.secret_id}")
            
            # Service-specific rotation logic
            if secret.service == 'elevenlabs':
                rotated.append(self._rotate_elevenlabs(secret, dry_run))
            elif secret.service == 'telegram-bot':
                rotated.append(self._rotate_telegram(secret, dry_run))
            elif secret.service == 'binance':
                rotated.append(self._rotate_binance(secret, dry_run))
            else:
                logger.warning(f"Auto-rotation not implemented for service: {secret.service}")
                
        return rotated
        
    def _rotate_elevenlabs(self, secret, dry_run: bool) -> dict:
        """Rotate ElevenLabs API key (manual - requires dashboard)"""
        logger.info(f"{'[DRY-RUN] ' if dry_run else ''}ElevenLabs rotation for {secret.secret_id}")
        return {
            'secret_id': secret.secret_id,
            'service': 'elevenlabs',
            'status': 'manual_required',
            'instructions': 'Log in to ElevenLabs dashboard, revoke old key, generate new one'
        }
        
    def _rotate_telegram(self, secret, dry_run: bool) -> dict:
        """Rotate Telegram bot token (via BotFather)"""
        logger.info(f"{'[DRY-RUN] ' if dry_run else ''}Telegram rotation for {secret.secret_id}")
        return {
            'secret_id': secret.secret_id,
            'service': 'telegram',
            'status': 'manual_required',
            'instructions': 'Message @BotFather, use /revoke command, then /newbot or token refresh'
        }
        
    def _rotate_binance(self, secret, dry_run: bool) -> dict:
        """Rotate Binance API key (requires 2FA)"""
        logger.info(f"{'[DRY-RUN] ' if dry_run else ''}Binance rotation for {secret.secret_id}")
        return {
            'secret_id': secret.secret_id,
            'service': 'binance',
            'status': 'manual_required',
            'instructions': 'Log in to Binance, API Management, delete old key, create new one with same permissions'
        }
        
    def notify(self, message: str):
        """Send notification about rotation status"""
        if NOTIFY_EMAIL:
            try:
                msg = MIMEText(message)
                msg['Subject'] = 'Key Master - Rotation Report'
                msg['From'] = 'keymaster@agi-company.cloud'
                msg['To'] = NOTIFY_EMAIL
                
                # Configure your SMTP server
                # with smtplib.SMTP('smtp.gmail.com', 587) as server:
                #     server.starttls()
                #     server.login('user', 'pass')
                #     server.send_message(msg)
                
                logger.info(f"Notification would be sent to {NOTIFY_EMAIL}")
            except Exception as e:
                logger.error(f"Failed to send notification: {e}")
        else:
            logger.info("No notification email configured")
            
    def run(self, dry_run: bool = True, notify: bool = False):
        """Run rotation check and optionally auto-rotate"""
        report = self.generate_rotation_report()
        print(report)
        
        if not dry_run:
            rotated = self.auto_rotate(dry_run=False)
            if rotated:
                print(f"\n🔄 Auto-rotated {len(rotated)} secrets")
                for r in rotated:
                    print(f"  - {r['secret_id']}: {r['status']}")
                    
        if notify:
            self.notify(report)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Key Master Rotation Automation')
    parser.add_argument('--execute', action='store_true', 
                       help='Execute rotations (default is dry-run)')
    parser.add_argument('--notify', action='store_true',
                       help='Send notification email')
    parser.add_argument('--cron', action='store_true',
                       help='Run in cron mode (quiet, exit code based on status)')
    
    args = parser.parse_args()
    
    automator = RotationAutomator()
    
    if args.cron:
        # Cron mode: quiet, exit code indicates status
        status = automator.check_rotation_queue()
        if status['overdue']:
            logger.error(f"CRITICAL: {len(status['overdue'])} secrets overdue")
            sys.exit(2)
        elif status['critical']:
            logger.warning(f"WARNING: {len(status['critical'])} secrets critical")
            sys.exit(1)
        sys.exit(0)
    else:
        automator.run(dry_run=not args.execute, notify=args.notify)

if __name__ == '__main__':
    main()