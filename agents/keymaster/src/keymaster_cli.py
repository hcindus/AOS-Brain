#!/usr/bin/env python3
"""
The Key Master - CLI Tool v1.0.0
Command-line interface for vault operations
"""

import os
import sys
import json
import argparse
import getpass
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from vault_core import get_vault, VaultCore

class KeyMasterCLI:
    """Command-line interface to the vault"""
    
    def __init__(self):
        self.vault = get_vault()
        
    def status(self):
        """Show vault status"""
        status = self.vault.vault_status()
        print(f"\n🗝️  The Key Master - Vault Status")
        print(f"{'='*40}")
        print(f"Status: {status['status'].upper()}")
        print(f"Active Secrets: {status['active_secrets']}")
        print(f"Revoked Secrets: {status['revoked_secrets']}")
        print(f"Rotations Due: {status['rotations_due']}")
        print(f"Access Today: {status['access_today']}")
        print(f"Vault Path: {status['vault_path']}")
        print(f"Last Check: {status['timestamp']}")
        
    def store(self, args):
        """Store a new secret"""
        value = args.value or getpass.getpass("Enter secret value: ")
        
        secret = self.vault.store_secret(
            secret_id=args.secret_id,
            value=value,
            service=args.service,
            secret_type=args.type,
            classification=args.classification,
            rotation_days=args.rotation_days,
            metadata=json.loads(args.metadata) if args.metadata else {}
        )
        
        print(f"\n✅ Secret stored successfully")
        print(f"ID: {secret.secret_id}")
        print(f"Service: {secret.service}")
        print(f"Type: {secret.secret_type}")
        print(f"Classification: {secret.classification}")
        print(f"Rotates: {secret.expires_at.strftime('%Y-%m-%d') if secret.expires_at else 'Never'}")
        
    def get(self, args):
        """Retrieve a secret value"""
        value = self.vault.retrieve_secret(
            secret_id=args.secret_id,
            requester=args.requester,
            reason=args.reason
        )
        
        if args.quiet:
            print(value)
        else:
            print(f"\n🗝️  Secret retrieved")
            print(f"Value: {value}")
            print(f"\n⚠️  This value is sensitive. Handle with care.")
            
    def rotate(self, args):
        """Rotate a secret"""
        new_value = args.new_value or getpass.getpass("Enter new value: ")
        
        secret = self.vault.rotate_secret(
            secret_id=args.secret_id,
            new_value=new_value,
            rotated_by=args.rotated_by,
            reason=args.reason
        )
        
        print(f"\n🔄 Secret rotated successfully")
        print(f"ID: {secret.secret_id}")
        print(f"New expiry: {secret.expires_at.strftime('%Y-%m-%d') if secret.expires_at else 'Never'}")
        
    def revoke(self, args):
        """Revoke a secret"""
        self.vault.revoke_secret(
            secret_id=args.secret_id,
            revoked_by=args.revoked_by,
            reason=args.reason
        )
        
        print(f"\n⛔ Secret revoked")
        print(f"ID: {args.secret_id}")
        print(f"This secret can no longer be retrieved.")
        
    def list(self, args):
        """List secrets"""
        secrets = self.vault.list_secrets(
            service=args.service,
            active_only=not args.all
        )
        
        print(f"\n🗝️  Secrets in the Vault")
        print(f"{'='*80}")
        print(f"{'ID':<30} {'Service':<15} {'Type':<12} {'Class':<8} {'Status':<8}")
        print(f"{'-'*80}")
        
        for s in secrets:
            status = 'ACTIVE' if s.active else 'REVOKED'
            print(f"{s.secret_id:<30} {s.service:<15} {s.secret_type:<12} "
                  f"{s.classification:<8} {status:<8}")
                  
    def queue(self, args):
        """Show rotation queue"""
        secrets = self.vault.get_rotation_queue()
        
        print(f"\n⏰ Rotation Queue")
        print(f"{'='*80}")
        
        if not secrets:
            print("No secrets require rotation.")
            return
            
        print(f"{'ID':<30} {'Service':<15} {'Expires':<20} {'Days Left':<10}")
        print(f"{'-'*80}")
        
        now = datetime.now()
        for s in secrets:
            if s.expires_at:
                days = (s.expires_at - now).days
                expires_str = s.expires_at.strftime('%Y-%m-%d')
                print(f"{s.secret_id:<30} {s.service:<15} {expires_str:<20} {days:<10}")
            else:
                print(f"{s.secret_id:<30} {s.service:<15} {'No expiry':<20} {'N/A':<10}")
                
    def audit(self, args):
        """Show audit log"""
        logs = self.vault.get_audit_log(limit=args.limit)
        
        print(f"\n📜 Audit Log (last {len(logs)} entries)")
        print(f"{'='*100}")
        print(f"{'Time':<20} {'Actor':<15} {'Action':<12} {'Secret':<20} {'Success':<8}")
        print(f"{'-'*100}")
        
        for log in logs:
            ts = log['timestamp'][:19] if isinstance(log['timestamp'], str) else str(log['timestamp'])[:19]
            success = '✅' if log['success'] else '❌'
            print(f"{ts:<20} {log['actor']:<15} {log['action']:<12} "
                  f"{log['secret_id'] or '':<20} {success:<8}")

def main():
    parser = argparse.ArgumentParser(
        description='The Key Master - Vault CLI',
        prog='keymaster'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Status command
    subparsers.add_parser('status', help='Show vault status')
    
    # Store command
    store_parser = subparsers.add_parser('store', help='Store a new secret')
    store_parser.add_argument('secret_id', help='Unique identifier for the secret')
    store_parser.add_argument('service', help='Service that owns the secret')
    store_parser.add_argument('--type', default='api_key', 
                             choices=['api_key', 'token', 'certificate', 'password', 'encryption_key'],
                             help='Type of secret')
    store_parser.add_argument('--value', help='Secret value (prompt if not provided)')
    store_parser.add_argument('--classification', default='standard',
                             choices=['critical', 'high', 'standard', 'legacy'],
                             help='Security classification')
    store_parser.add_argument('--rotation-days', type=int, default=90,
                             help='Days until rotation required')
    store_parser.add_argument('--metadata', help='JSON metadata string')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Retrieve a secret')
    get_parser.add_argument('secret_id', help='ID of the secret to retrieve')
    get_parser.add_argument('--requester', default=os.environ.get('USER', 'cli'),
                           help='Who is requesting the secret')
    get_parser.add_argument('--reason', required=True, help='Why the secret is needed')
    get_parser.add_argument('--quiet', '-q', action='store_true',
                           help='Output only the value')
    
    # Rotate command
    rotate_parser = subparsers.add_parser('rotate', help='Rotate a secret')
    rotate_parser.add_argument('secret_id', help='ID of the secret to rotate')
    rotate_parser.add_argument('--new-value', help='New secret value (prompt if not provided)')
    rotate_parser.add_argument('--rotated-by', default=os.environ.get('USER', 'cli'),
                              help='Who is performing the rotation')
    rotate_parser.add_argument('--reason', required=True, help='Why the rotation is happening')
    
    # Revoke command
    revoke_parser = subparsers.add_parser('revoke', help='Revoke a secret')
    revoke_parser.add_argument('secret_id', help='ID of the secret to revoke')
    revoke_parser.add_argument('--revoked-by', default=os.environ.get('USER', 'cli'),
                              help='Who is performing the revocation')
    revoke_parser.add_argument('--reason', required=True, help='Why the secret is being revoked')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List secrets')
    list_parser.add_argument('--service', help='Filter by service')
    list_parser.add_argument('--all', action='store_true', help='Include revoked secrets')
    
    # Queue command
    subparsers.add_parser('queue', help='Show rotation queue')
    
    # Audit command
    audit_parser = subparsers.add_parser('audit', help='Show audit log')
    audit_parser.add_argument('--limit', type=int, default=50, help='Number of entries to show')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cli = KeyMasterCLI()
    
    commands = {
        'status': cli.status,
        'store': lambda: cli.store(args),
        'get': lambda: cli.get(args),
        'rotate': lambda: cli.rotate(args),
        'revoke': lambda: cli.revoke(args),
        'list': lambda: cli.list(args),
        'queue': cli.queue,
        'audit': lambda: cli.audit(args),
    }
    
    if args.command in commands:
        commands[args.command]()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()