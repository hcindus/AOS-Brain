#!/usr/bin/env python3
"""
Test MiniMax API with real credentials
"""

import requests
import json

API_KEY = "sk-api-TX-XTNb1QOfiC0DmcpFU6rfGKJ6iiRMVsQjMsC8nnIBFWqNMKGd8Dg8tzQMmmSxLdgLD12Y1YO9azhrrYDRAihxR-fHwcNYvopauDyeR8ZppkTb3IpTaS0Q"
API_BASE = "https://api.minimax.io"

def test_minimax_connection():
    """Test if MiniMax API is accessible."""
    print("🔌 Testing MiniMax API connection...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Try to get model info (lightweight test)
    try:
        response = requests.get(
            f"{API_BASE}/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ MiniMax API connection successful!")
            print(f"   Status: {response.status_code}")
            return True
        else:
            print(f"⚠️  MiniMax API returned: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MiniMax API")
        print("   Possible causes:")
        print("   - API endpoint incorrect")
        print("   - Network issues")
        print("   - API service down")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_minimax_connection()
