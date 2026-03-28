#!/usr/bin/env python3
"""
Check if MiniMax API key has activated (delayed activation)
Run every 1-5 minutes after key creation
"""

import time
import yaml
from pathlib import Path
import requests

API_KEY = "sk-api-AiDiIM7K52eyXaxwrW4nhu2bakhQ0xoa5yWV8avoLFGBIRpeIeEpcC0HjR2wUixnqfni4O-xdWK5hwFkTt8h9JtasU6-nbLUT5iMn5vaWWRNHQpNJKifK1w"
CONFIG_FILE = Path.home() / ".mini-agent" / "config" / "config_minimax_pending.yaml"

def check_activation():
    """Check if MiniMax key is active."""
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'abab6.5-chat',
        'messages': [
            {'role': 'user', 'content': 'Hello'}
        ],
        'max_tokens': 10
    }
    
    url = 'https://api.minimax.chat/v1/text/chatcompletion_v2'
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        result = response.json()
        
        if response.status_code == 200:
            if 'base_resp' in result and result['base_resp'].get('status_code') == 0:
                print(f"✅ MiniMax API key ACTIVE!")
                print(f"   Response: {result.get('choices', [{}])[0].get('message', {}).get('content', 'OK')}")
                update_config_status("active")
                return True
            else:
                status = result.get('base_resp', {}).get('status_code')
                msg = result.get('base_resp', {}).get('status_msg')
                print(f"⏳ Still pending (code {status}): {msg}")
                return False
        else:
            print(f"⏳ HTTP {response.status_code} - waiting for activation")
            return False
            
    except Exception as e:
        print(f"⏳ Error checking: {e}")
        return False

def update_config_status(status):
    """Update config file with activation status."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = yaml.safe_load(f)
        
        config['activation_status'] = status
        config['activated_at'] = time.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config, f)
        
        print(f"   Config updated: {status}")

def main():
    """Check activation status."""
    print("="*70)
    print("🔌 Checking MiniMax API Key Activation...")
    print("="*70)
    print()
    print(f"Key created: ~2 minutes ago")
    print("Status: PENDING (keys may take 1-5 minutes to activate)")
    print()
    
    active = check_activation()
    
    if not active:
        print()
        print("Instructions:")
        print("  1. Keys from platform.minimax.io may take 1-5 minutes to activate")
        print("  2. Run this script again in 2 minutes")
        print("  3. Or wait - system will auto-retry on next use")
        print()
        print("Current fallback: Local brain (fully functional)")
    
    return active

if __name__ == "__main__":
    main()
