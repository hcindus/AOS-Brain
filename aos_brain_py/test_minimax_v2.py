#!/usr/bin/env python3
"""
Test MiniMax API with correct endpoint
MiniMax API v2 documentation: https://www.minimaxi.com/en
"""

import requests
import json

API_KEY = "sk-api-TX-XTNb1QOfiC0DmcpFU6rfGKJ6iiRMVsQjMsC8nnIBFWqNMKGd8Dg8tzQMmmSxLdgLD12Y1YO9azhrrYDRAihxR-fHwcNYvopauDyeR8ZppkTb3IpTaS0Q"

# Try different endpoints
ENDPOINTS = [
    "https://api.minimax.io/v1/models",
    "https://api.minimax.io/v1/text/chatcompletion_v2",
    "https://api.minimax.chat/v1/models",
    "https://api.minimaxi.com/v1/models",
]

def test_endpoints():
    """Try multiple MiniMax endpoints."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("🔌 Testing MiniMax API endpoints...")
    print()
    
    for endpoint in ENDPOINTS:
        print(f"Trying: {endpoint}")
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ SUCCESS!")
                print(f"  Response: {response.text[:200]}")
                return endpoint
            else:
                print(f"  Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"  Error: {e}")
        print()
    
    print("❌ No working endpoint found")
    return None

if __name__ == "__main__":
    test_endpoints()
