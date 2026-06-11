#!/usr/bin/env python3
"""
The Key Master - Bootstrap Script
Initialize vault and store current secrets
"""

import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from vault_core import get_vault

def bootstrap():
    """Initialize vault with known secrets"""
    vault = get_vault()
    
    print("🗝️  The Key Master - Vault Bootstrap")
    print("=" * 50)
    
    # Check existing status
    status = vault.vault_status()
    print(f"Vault Status: {status['status']}")
    print(f"Current Secrets: {status['active_secrets']}")
    print()
    
    # Load secrets from environment or prompt
    secrets_to_store = []
    
    # ElevenLabs API Key
    elevenlabs_key = os.environ.get('ELEVENLABS_API_KEY')
    if elevenlabs_key:
        secrets_to_store.append({
            'id': 'elevenlabs-api-key',
            'service': 'elevenlabs',
            'type': 'api_key',
            'value': elevenlabs_key,
            'classification': 'high',
            'rotation_days': 90,
            'metadata': {'purpose': 'TTS for Miles voice'}
        })
    
    # Telegram Bot Token
    telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if telegram_token:
        secrets_to_store.append({
            'id': 'telegram-bot-token',
            'service': 'telegram-bot',
            'type': 'token',
            'value': telegram_token,
            'classification': 'high',
            'rotation_days': 90,
            'metadata': {'purpose': 'Miles Telegram integration'}
        })
    
    # OpenAI API Key
    openai_key = os.environ.get('OPENAI_API_KEY')
    if openai_key:
        secrets_to_store.append({
            'id': 'openai-api-key',
            'service': 'openai',
            'type': 'api_key',
            'value': openai_key,
            'classification': 'high',
            'rotation_days': 90,
            'metadata': {'purpose': 'AI completions'}
        })
    
    # Binance API Keys (for Knox)
    binance_key = os.environ.get('BINANCE_API_KEY')
    binance_secret = os.environ.get('BINANCE_API_SECRET')
    if binance_key and binance_secret:
        secrets_to_store.append({
            'id': 'binance-api-key',
            'service': 'binance',
            'type': 'api_key',
            'value': binance_key,
            'classification': 'critical',
            'rotation_days': 30,
            'metadata': {'purpose': 'Knox trading access', 'scope': 'read-only'}
        })
        secrets_to_store.append({
            'id': 'binance-api-secret',
            'service': 'binance',
            'type': 'api_key',
            'value': binance_secret,
            'classification': 'critical',
            'rotation_days': 30,
            'metadata': {'purpose': 'Knox trading authentication', 'scope': 'read-only'}
        })
    
    # Store secrets
    if secrets_to_store:
        print(f"Found {len(secrets_to_store)} secrets to store...")
        for s in secrets_to_store:
            try:
                vault.store_secret(
                    secret_id=s['id'],
                    value=s['value'],
                    service=s['service'],
                    secret_type=s['type'],
                    classification=s['classification'],
                    rotation_days=s['rotation_days'],
                    metadata=s['metadata']
                )
                print(f"  ✅ Stored: {s['id']} ({s['service']})")
            except Exception as e:
                print(f"  ❌ Failed: {s['id']} - {e}")
    else:
        print("No secrets found in environment variables.")
        print("\nTo add secrets, set these environment variables:")
        print("  - ELEVENLABS_API_KEY")
        print("  - TELEGRAM_BOT_TOKEN")
        print("  - OPENAI_API_KEY")
        print("  - BINANCE_API_KEY + BINANCE_API_SECRET")
    
    # Final status
    print()
    print("=" * 50)
    status = vault.vault_status()
    print(f"Vault now contains {status['active_secrets']} secrets")
    print()
    print("Commands:")
    print("  keymaster status     - Show vault status")
    print("  keymaster list       - List all secrets")
    print("  keymaster queue      - Show rotation queue")
    print("  keymaster audit      - View audit log")

if __name__ == '__main__':
    bootstrap()