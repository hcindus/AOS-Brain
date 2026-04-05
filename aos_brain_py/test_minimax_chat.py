#!/usr/bin/env python3
"""
Test MiniMax API with chat completion endpoint
Common MiniMax endpoints based on documentation
"""

import requests
import json

API_KEY = "sk-api-TX-XTNb1QOfiC0DmcpFU6rfGKJ6iiRMVsQjMsC8nnIBFWqNMKGd8Dg8tzQMmmSxLdgLD12Y1YO9azhrrYDRAihxR-fHwcNYvopauDyeR8ZppkTb3IpTaS0Q"

# MiniMax API v2 endpoints
ENDPOINTS = [
    {
        "url": "https://api.minimax.chat/v1/text/chatcompletion_v2",
        "model": "abab6.5-chat",  # Latest model
    },
    {
        "url": "https://api.minimax.chat/v1/text/chatcompletion",
        "model": "abab5.5-chat",
    },
    {
        "url": "https://api.minimax.io/v1/chat/completions",
        "model": "MiniMax-M2.5",
    }
]

def test_chat_completion():
    """Test MiniMax chat completion API."""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "abab6.5-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful technical assistant."},
            {"role": "user", "content": "What is 2+2?"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    print("🔌 Testing MiniMax Chat Completion...")
    print()
    
    for endpoint in ENDPOINTS:
        url = endpoint["url"]
        print(f"Trying: {url}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ SUCCESS!")
                print(f"  Response: {result.get('choices', [{}])[0].get('message', {}).get('content', 'No content')}")
                return True
            else:
                print(f"  Response: {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            print(f"  ⏱️  Timeout")
        except Exception as e:
            print(f"  Error: {e}")
        print()
    
    print("❌ Chat completion test failed")
    print()
    print("Possible issues:")
    print("  - API endpoint may be different")
    print("  - API key may need different format")
    print("  - Network connectivity to MiniMax")
    print("  - API service region restrictions")
    return False

if __name__ == "__main__":
    test_chat_completion()
